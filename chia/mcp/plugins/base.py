"""
Base classes for MCP plugin system.

Provides the foundation for creating hierarchical, extensible MCP tools
organized by functional domains.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..protocol import MCPResource, MCPTool

logger = logging.getLogger(__name__)


@dataclass
class ToolCategory:
    """Represents a category of related tools."""

    name: str
    description: str
    icon: Optional[str] = None
    tags: Optional[List[str]] = None


class MCPPlugin(ABC):
    """Base class for MCP plugins that provide categorized tools and resources."""

    def __init__(self, rpc_client=None):
        self.rpc_client = rpc_client
        self._tools: Dict[str, MCPTool] = {}
        self._resources: Dict[str, MCPResource] = {}
        self._categories: Dict[str, ToolCategory] = {}

    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Return the name of this plugin (e.g., 'wallet', 'farming')."""

    @property
    @abstractmethod
    def plugin_description(self) -> str:
        """Return a description of this plugin's functionality."""

    def get_tools(self) -> Dict[str, MCPTool]:
        """Get all tools provided by this plugin."""
        if not self._tools:
            self._register_tools()
        return self._tools

    def get_resources(self) -> Dict[str, MCPResource]:
        """Get all resources provided by this plugin."""
        if not self._resources:
            self._register_resources()
        return self._resources

    def get_categories(self) -> Dict[str, ToolCategory]:
        """Get all tool categories defined by this plugin."""
        if not self._categories:
            self._register_categories()
        return self._categories

    @abstractmethod
    def _register_tools(self) -> None:
        """Register tools provided by this plugin."""

    @abstractmethod
    def _register_resources(self) -> None:
        """Register resources provided by this plugin."""

    def _register_categories(self) -> None:
        """Register tool categories. Override if plugin defines categories."""

    def add_tool(self, tool: MCPTool) -> None:
        """Add a tool to this plugin."""
        full_name = f"{self.plugin_name}.{tool.name}"
        self._tools[full_name] = MCPTool(name=full_name, description=tool.description, input_schema=tool.input_schema)

    def add_resource(self, resource: MCPResource) -> None:
        """Add a resource to this plugin."""
        self._resources[resource.uri] = resource

    def add_category(self, category: ToolCategory) -> None:
        """Add a tool category to this plugin."""
        self._categories[category.name] = category

    @abstractmethod
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool provided by this plugin."""

    @abstractmethod
    async def read_resource(self, uri: str) -> Any:
        """Read a resource provided by this plugin."""


class PluginManager:
    """Manages MCP plugins and provides unified access to tools and resources."""

    def __init__(self):
        self.plugins: Dict[str, MCPPlugin] = {}
        self.logger = logging.getLogger(__name__ + ".PluginManager")

    def register_plugin(self, plugin: MCPPlugin) -> None:
        """Register a plugin with the manager."""
        self.plugins[plugin.plugin_name] = plugin
        self.logger.info(f"Registered MCP plugin: {plugin.plugin_name}")

    def get_all_tools(self) -> Dict[str, MCPTool]:
        """Get all tools from all registered plugins."""
        all_tools = {}
        for plugin in self.plugins.values():
            all_tools.update(plugin.get_tools())
        return all_tools

    def get_all_resources(self) -> Dict[str, MCPResource]:
        """Get all resources from all registered plugins."""
        all_resources = {}
        for plugin in self.plugins.values():
            all_resources.update(plugin.get_resources())
        return all_resources

    def get_all_categories(self) -> Dict[str, ToolCategory]:
        """Get all categories from all registered plugins."""
        all_categories = {}
        for plugin in self.plugins.values():
            all_categories.update(plugin.get_categories())
        return all_categories

    def get_tools_by_category(self, category: str) -> Dict[str, MCPTool]:
        """Get all tools in a specific category."""
        tools = {}
        for tool_name, tool in self.get_all_tools().items():
            plugin_name = tool_name.split(".")[0]
            if plugin_name == category:
                tools[tool_name] = tool
        return tools

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool by routing to the appropriate plugin."""
        try:
            if "." not in tool_name:
                raise ValueError(f"Tool name must include plugin prefix: {tool_name}")

            plugin_name, local_tool_name = tool_name.split(".", 1)

            if plugin_name not in self.plugins:
                available_plugins = list(self.plugins.keys())
                raise ValueError(f"Unknown plugin: {plugin_name}. Available plugins: {available_plugins}")

            plugin = self.plugins[plugin_name]

            # Validate tool exists in plugin
            plugin_tools = plugin.get_tools()
            if tool_name not in plugin_tools:
                available_tools = [name for name in plugin_tools.keys() if name.startswith(f"{plugin_name}.")]
                raise ValueError(
                    f"Tool '{tool_name}' not found in plugin '{plugin_name}'. Available tools: {available_tools}"
                )

            # Execute with enhanced error context
            try:
                result = await plugin.execute_tool(local_tool_name, arguments)
                self.logger.debug(f"Successfully executed tool: {tool_name}")
                return result
            except Exception as e:
                self.logger.error(f"Tool execution failed for {tool_name}: {e}")
                raise ValueError(f"Tool execution failed for {tool_name}: {e!s}")

        except Exception as e:
            self.logger.error(f"Error in tool execution routing: {e}")
            raise

    async def read_resource(self, uri: str) -> Any:
        """Read a resource by routing to the appropriate plugin."""
        try:
            # Find which plugin handles this resource
            handling_plugin = None
            for plugin in self.plugins.values():
                if uri in plugin.get_resources():
                    handling_plugin = plugin
                    break

            if handling_plugin is None:
                available_resources = list(self.get_all_resources().keys())
                raise ValueError(f"Unknown resource: {uri}. Available resources: {available_resources[:10]}...")

            try:
                result = await handling_plugin.read_resource(uri)
                self.logger.debug(f"Successfully read resource: {uri}")
                return result
            except Exception as e:
                self.logger.error(f"Resource reading failed for {uri}: {e}")
                raise ValueError(f"Resource reading failed for {uri}: {e!s}")

        except Exception as e:
            self.logger.error(f"Error in resource reading routing: {e}")
            raise

    def get_plugin_info(self) -> List[Dict[str, Any]]:
        """Get information about all registered plugins."""
        return [
            {
                "name": plugin.plugin_name,
                "description": plugin.plugin_description,
                "tools_count": len(plugin.get_tools()),
                "resources_count": len(plugin.get_resources()),
                "categories": list(plugin.get_categories().keys()),
            }
            for plugin in self.plugins.values()
        ]
