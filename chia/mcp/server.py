"""
MCP Server implementation for Chia blockchain integration.

Provides Model Context Protocol server functionality to expose Chia blockchain
operations and data access to AI models using a hierarchical plugin system.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Optional

from ..rpc.rpc_client import RpcClient
from ..util.config import load_config
from .plugins import BlockchainPlugin, FarmingPlugin, PluginManager, WalletPlugin
from .protocol import (
    MCPHandler,
    MCPNotification,
    MCPRequest,
    MCPResource,
    MCPResponse,
    MCPTool,
    deserialize_message,
    serialize_message,
)

logger = logging.getLogger(__name__)


class MCPServer:
    """Base MCP server implementation."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.handlers: Dict[str, MCPHandler] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.server = None

    def add_handler(self, method: str, handler: MCPHandler) -> None:
        """Add a handler for a specific MCP method."""
        self.handlers[method] = handler

    def add_tool(self, tool: MCPTool) -> None:
        """Add a tool that can be called via MCP."""
        self.tools[tool.name] = tool

    def add_resource(self, resource: MCPResource) -> None:
        """Add a resource that can be accessed via MCP."""
        self.resources[resource.uri] = resource

    async def handle_message(self, websocket, message: str) -> None:
        """Handle an incoming MCP message."""
        try:
            parsed_message = deserialize_message(message)

            if isinstance(parsed_message, MCPRequest):
                response = await self._handle_request(parsed_message)
                if response:
                    await websocket.send(serialize_message(response))

            elif isinstance(parsed_message, MCPNotification):
                await self._handle_notification(parsed_message)

        except Exception as e:
            logger.error(f"Error handling MCP message: {e}")
            error_response = MCPResponse(
                id=getattr(parsed_message, "id", None), error={"code": -32603, "message": f"Internal error: {e!s}"}
            )
            await websocket.send(serialize_message(error_response))

    async def _handle_request(self, request: MCPRequest) -> Optional[MCPResponse]:
        """Handle an MCP request."""
        if request.method in self.handlers:
            return await self.handlers[request.method].handle_request(request)
        else:
            return MCPResponse(id=request.id, error={"code": -32601, "message": f"Method not found: {request.method}"})

    async def _handle_notification(self, notification: MCPNotification) -> None:
        """Handle an MCP notification."""
        if notification.method in self.handlers:
            await self.handlers[notification.method].handle_notification(notification)
        else:
            logger.warning(f"No handler for notification method: {notification.method}")


class ChiaMCPServer(MCPServer):
    """MCP server specifically for Chia blockchain integration with plugin system."""

    def __init__(self, host: str = "localhost", port: int = 8080, chia_rpc_port: int = 9256):
        super().__init__(host, port)
        self.chia_rpc_port = chia_rpc_port
        self.rpc_client: Optional[RpcClient] = None
        self.config = None

        # Initialize plugin manager
        self.plugin_manager = PluginManager()

        # Register default Chia plugins
        self._register_default_plugins()

    async def start(self) -> None:
        """Start the Chia MCP server."""
        try:
            # Load Chia configuration
            self.config = load_config(Path.home() / ".chia" / "mainnet", "config.yaml")

            # Initialize RPC client
            self.rpc_client = await RpcClient.create(
                self.config["wallet"]["rpc_port"], RpcClient.get_client_base_path() + "wallet/"
            )

            # Initialize plugins with RPC client
            for plugin in self.plugin_manager.plugins.values():
                plugin.rpc_client = self.rpc_client

            # Register plugin handlers
            self._register_plugin_handlers()

            logger.info(f"Chia MCP Server starting on {self.host}:{self.port}")
            logger.info(f"Connected to Chia wallet RPC on port {self.chia_rpc_port}")
            logger.info(
                f"Loaded {len(self.plugin_manager.plugins)} plugins: {list(self.plugin_manager.plugins.keys())}"
            )

        except Exception as e:
            logger.error(f"Failed to start Chia MCP server: {e}")
            raise

    async def stop(self) -> None:
        """Stop the Chia MCP server."""
        if self.rpc_client:
            self.rpc_client.close()
            self.rpc_client = None

        logger.info("Chia MCP Server stopped")

    def _register_default_plugins(self) -> None:
        """Register default Chia plugins."""
        # Register core plugins
        self.plugin_manager.register_plugin(WalletPlugin())
        self.plugin_manager.register_plugin(BlockchainPlugin())
        self.plugin_manager.register_plugin(FarmingPlugin())

    def _register_plugin_handlers(self) -> None:
        """Register MCP handlers that work with the plugin system."""
        # Override tools and resources with plugin data
        self.tools = self.plugin_manager.get_all_tools()
        self.resources = self.plugin_manager.get_all_resources()

        # Register enhanced handlers
        self.add_handler("tools/call", PluginToolCallHandler(self))
        self.add_handler("tools/list", PluginToolListHandler(self))
        self.add_handler("resources/read", PluginResourceHandler(self))
        self.add_handler("resources/list", PluginResourceListHandler(self))
        self.add_handler("plugins/list", PluginInfoHandler(self))
        self.add_handler("categories/list", CategoryListHandler(self))

    def get_plugin_manager(self) -> PluginManager:
        """Get the plugin manager for external access."""
        return self.plugin_manager


class PluginToolCallHandler(MCPHandler):
    """Handler for tool calls using the plugin system."""

    def __init__(self, server: ChiaMCPServer):
        self.server = server

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle tool call requests."""
        try:
            params = request.params or {}
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if not tool_name:
                return MCPResponse(id=request.id, error={"code": -32602, "message": "Missing tool name"})

            if tool_name not in self.server.tools:
                return MCPResponse(id=request.id, error={"code": -32601, "message": f"Tool not found: {tool_name}"})

            # Execute the tool through plugin manager
            result = await self.server.plugin_manager.execute_tool(tool_name, arguments)

            return MCPResponse(
                id=request.id, result={"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            )

        except Exception as e:
            return MCPResponse(id=request.id, error={"code": -32603, "message": f"Tool execution failed: {e!s}"})

    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle tool call notifications."""


class PluginToolListHandler(MCPHandler):
    """Handler for listing available tools with plugin information."""

    def __init__(self, server: ChiaMCPServer):
        self.server = server

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle tool list requests."""
        tools_list = []

        for tool_name, tool in self.server.tools.items():
            plugin_name = tool_name.split(".")[0] if "." in tool_name else "core"

            tool_info = {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema,
                "plugin": plugin_name,
                "category": plugin_name,  # Plugin name serves as category
            }
            tools_list.append(tool_info)

        # Group tools by plugin for better organization
        tools_by_plugin = {}
        for tool_info in tools_list:
            plugin = tool_info["plugin"]
            if plugin not in tools_by_plugin:
                tools_by_plugin[plugin] = []
            tools_by_plugin[plugin].append(tool_info)

        return MCPResponse(
            id=request.id,
            result={
                "tools": tools_list,
                "tools_by_plugin": tools_by_plugin,
                "total_tools": len(tools_list),
                "plugins": list(tools_by_plugin.keys()),
            },
        )

    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle tool list notifications."""


class PluginResourceHandler(MCPHandler):
    """Handler for reading resources using the plugin system."""

    def __init__(self, server: ChiaMCPServer):
        self.server = server

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle resource read requests."""
        try:
            params = request.params or {}
            uri = params.get("uri")

            if not uri:
                return MCPResponse(id=request.id, error={"code": -32602, "message": "Missing resource URI"})

            if uri not in self.server.resources:
                return MCPResponse(id=request.id, error={"code": -32601, "message": f"Resource not found: {uri}"})

            # Read the resource through plugin manager
            content = await self.server.plugin_manager.read_resource(uri)

            return MCPResponse(
                id=request.id,
                result={
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": self.server.resources[uri].mime_type,
                            "text": json.dumps(content, indent=2),
                        }
                    ]
                },
            )

        except Exception as e:
            return MCPResponse(id=request.id, error={"code": -32603, "message": f"Resource read failed: {e!s}"})

    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle resource read notifications."""


class PluginResourceListHandler(MCPHandler):
    """Handler for listing available resources with plugin information."""

    def __init__(self, server: ChiaMCPServer):
        self.server = server

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle resource list requests."""
        resources_list = []

        for uri, resource in self.server.resources.items():
            # Determine plugin from URI
            plugin_name = "core"
            if uri.startswith("chia://"):
                uri_parts = uri.split("/")
                if len(uri_parts) > 2:
                    plugin_name = uri_parts[2]  # e.g., wallet, blockchain, farming

            resource_info = {
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "mimeType": resource.mime_type,
                "plugin": plugin_name,
            }
            resources_list.append(resource_info)

        # Group resources by plugin
        resources_by_plugin = {}
        for resource_info in resources_list:
            plugin = resource_info["plugin"]
            if plugin not in resources_by_plugin:
                resources_by_plugin[plugin] = []
            resources_by_plugin[plugin].append(resource_info)

        return MCPResponse(
            id=request.id,
            result={
                "resources": resources_list,
                "resources_by_plugin": resources_by_plugin,
                "total_resources": len(resources_list),
                "plugins": list(resources_by_plugin.keys()),
            },
        )

    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle resource list notifications."""


class PluginInfoHandler(MCPHandler):
    """Handler for getting plugin information."""

    def __init__(self, server: ChiaMCPServer):
        self.server = server

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle plugin info requests."""
        plugin_info = self.server.plugin_manager.get_plugin_info()

        return MCPResponse(id=request.id, result={"plugins": plugin_info, "total_plugins": len(plugin_info)})

    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle plugin info notifications."""


class CategoryListHandler(MCPHandler):
    """Handler for listing tool categories."""

    def __init__(self, server: ChiaMCPServer):
        self.server = server

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle category list requests."""
        categories = self.server.plugin_manager.get_all_categories()

        categories_list = []
        for category_name, category in categories.items():
            category_info = {
                "name": category.name,
                "description": category.description,
                "icon": category.icon,
                "tags": category.tags or [],
            }
            categories_list.append(category_info)

        return MCPResponse(
            id=request.id, result={"categories": categories_list, "total_categories": len(categories_list)}
        )

    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle category list notifications."""
