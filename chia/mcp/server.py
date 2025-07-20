"""
MCP Server implementation for Chia blockchain integration.

Provides Model Context Protocol server functionality to expose Chia blockchain
operations and data access to AI models.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Callable, Union
from pathlib import Path

from .protocol import (
    MCPRequest, MCPResponse, MCPNotification, MCPHandler, MCPTool, MCPResource,
    MCPError, ChiaWalletInfo, ChiaTransactionRecord,
    serialize_message, deserialize_message
)

from ..rpc.rpc_client import RpcClient
from ..util.config import load_config


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
                id=getattr(parsed_message, 'id', None),
                error={
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            )
            await websocket.send(serialize_message(error_response))
    
    async def _handle_request(self, request: MCPRequest) -> Optional[MCPResponse]:
        """Handle an MCP request."""
        if request.method in self.handlers:
            return await self.handlers[request.method].handle_request(request)
        else:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": f"Method not found: {request.method}"
                }
            )
    
    async def _handle_notification(self, notification: MCPNotification) -> None:
        """Handle an MCP notification.""" 
        if notification.method in self.handlers:
            await self.handlers[notification.method].handle_notification(notification)
        else:
            logger.warning(f"No handler for notification method: {notification.method}")


class ChiaMCPServer(MCPServer):
    """MCP server specifically for Chia blockchain integration."""
    
    def __init__(self, host: str = "localhost", port: int = 8080, chia_rpc_port: int = 9256):
        super().__init__(host, port)
        self.chia_rpc_port = chia_rpc_port
        self.rpc_client: Optional[RpcClient] = None
        self.config = None
        
        # Register default Chia tools
        self._register_chia_tools()
        self._register_chia_resources()
        
    async def start(self) -> None:
        """Start the Chia MCP server."""
        try:
            # Load Chia configuration
            self.config = load_config(Path.home() / ".chia" / "mainnet", "config.yaml")
            
            # Initialize RPC client
            self.rpc_client = await RpcClient.create(
                self.config["wallet"]["rpc_port"], 
                RpcClient.get_client_base_path() + "wallet/"
            )
            
            logger.info(f"Chia MCP Server starting on {self.host}:{self.port}")
            logger.info(f"Connected to Chia wallet RPC on port {self.chia_rpc_port}")
            
        except Exception as e:
            logger.error(f"Failed to start Chia MCP server: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the Chia MCP server."""
        if self.rpc_client:
            self.rpc_client.close()
            self.rpc_client = None
            
        logger.info("Chia MCP Server stopped")
    
    def _register_chia_tools(self) -> None:
        """Register default Chia blockchain tools."""
        
        # Wallet balance tool
        self.add_tool(MCPTool(
            name="get_wallet_balance",
            description="Get the balance of a Chia wallet",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "The ID of the wallet to check balance for",
                        "default": 1
                    }
                }
            }
        ))
        
        # Transaction history tool
        self.add_tool(MCPTool(
            name="get_transactions",
            description="Get transaction history for a Chia wallet",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "The ID of the wallet to get transactions for",
                        "default": 1
                    },
                    "start": {
                        "type": "integer",
                        "description": "Starting index for transactions",
                        "default": 0
                    },
                    "end": {
                        "type": "integer", 
                        "description": "Ending index for transactions",
                        "default": 50
                    }
                }
            }
        ))
        
        # Send transaction tool
        self.add_tool(MCPTool(
            name="send_transaction",
            description="Send XCH or other tokens to another address",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "The ID of the wallet to send from",
                        "default": 1
                    },
                    "amount": {
                        "type": "integer",
                        "description": "Amount to send in mojos (1 XCH = 1e12 mojos)"
                    },
                    "address": {
                        "type": "string",
                        "description": "Destination address"
                    },
                    "fee": {
                        "type": "integer",
                        "description": "Transaction fee in mojos",
                        "default": 0
                    }
                },
                "required": ["amount", "address"]
            }
        ))
        
        # Get wallet info tool
        self.add_tool(MCPTool(
            name="get_wallets",
            description="Get list of all wallets",
            input_schema={
                "type": "object",
                "properties": {}
            }
        ))
        
        # Sync status tool
        self.add_tool(MCPTool(
            name="get_sync_status",
            description="Get wallet sync status",
            input_schema={
                "type": "object",
                "properties": {}
            }
        ))
        
        # Register handlers for these tools
        self.add_handler("tools/call", ChiaToolCallHandler(self))
        self.add_handler("tools/list", ChiaToolListHandler(self))
        
    def _register_chia_resources(self) -> None:
        """Register default Chia blockchain resources."""
        
        self.add_resource(MCPResource(
            uri="chia://blockchain/status",
            name="Blockchain Status",
            description="Current blockchain sync status and information",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://wallet/balance",
            name="Wallet Balance",
            description="Current wallet balance information",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://wallet/transactions",
            name="Wallet Transactions", 
            description="Transaction history for wallets",
            mime_type="application/json"
        ))
        
        # Register resource handlers
        self.add_handler("resources/read", ChiaResourceHandler(self))
        self.add_handler("resources/list", ChiaResourceListHandler(self))


class ChiaToolCallHandler(MCPHandler):
    """Handler for Chia tool calls."""
    
    def __init__(self, server: ChiaMCPServer):
        self.server = server
        
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle tool call requests."""
        try:
            params = request.params or {}
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                return MCPResponse(
                    id=request.id,
                    error={"code": -32602, "message": "Missing tool name"}
                )
                
            if tool_name not in self.server.tools:
                return MCPResponse(
                    id=request.id,
                    error={"code": -32601, "message": f"Tool not found: {tool_name}"}
                )
                
            # Execute the tool
            result = await self._execute_tool(tool_name, arguments)
            
            return MCPResponse(
                id=request.id,
                result={"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            )
            
        except Exception as e:
            return MCPResponse(
                id=request.id,
                error={"code": -32603, "message": f"Tool execution failed: {str(e)}"}
            )
    
    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle tool call notifications."""
        pass
        
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a specific Chia tool."""
        if not self.server.rpc_client:
            raise Exception("RPC client not initialized")
            
        if tool_name == "get_wallet_balance":
            wallet_id = arguments.get("wallet_id", 1)
            response = await self.server.rpc_client.fetch("get_wallet_balance", {"wallet_id": wallet_id})
            return response
            
        elif tool_name == "get_transactions":
            wallet_id = arguments.get("wallet_id", 1)
            start = arguments.get("start", 0)
            end = arguments.get("end", 50)
            response = await self.server.rpc_client.fetch("get_transactions", {
                "wallet_id": wallet_id,
                "start": start,
                "end": end
            })
            return response
            
        elif tool_name == "send_transaction":
            wallet_id = arguments.get("wallet_id", 1)
            amount = arguments["amount"]
            address = arguments["address"]
            fee = arguments.get("fee", 0)
            
            response = await self.server.rpc_client.fetch("send_transaction", {
                "wallet_id": wallet_id,
                "amount": amount,
                "address": address,
                "fee": fee
            })
            return response
            
        elif tool_name == "get_wallets":
            response = await self.server.rpc_client.fetch("get_wallets", {})
            return response
            
        elif tool_name == "get_sync_status":
            response = await self.server.rpc_client.fetch("get_sync_status", {})
            return response
            
        else:
            raise Exception(f"Unknown tool: {tool_name}")


class ChiaToolListHandler(MCPHandler):
    """Handler for listing available tools."""
    
    def __init__(self, server: ChiaMCPServer):
        self.server = server
        
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle tool list requests."""
        tools_list = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in self.server.tools.values()
        ]
        
        return MCPResponse(
            id=request.id,
            result={"tools": tools_list}
        )
    
    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle tool list notifications."""
        pass


class ChiaResourceHandler(MCPHandler):
    """Handler for reading Chia resources."""
    
    def __init__(self, server: ChiaMCPServer):
        self.server = server
        
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle resource read requests."""
        try:
            params = request.params or {}
            uri = params.get("uri")
            
            if not uri:
                return MCPResponse(
                    id=request.id,
                    error={"code": -32602, "message": "Missing resource URI"}
                )
                
            if uri not in self.server.resources:
                return MCPResponse(
                    id=request.id,
                    error={"code": -32601, "message": f"Resource not found: {uri}"}
                )
                
            # Read the resource
            content = await self._read_resource(uri)
            
            return MCPResponse(
                id=request.id,
                result={
                    "contents": [{
                        "uri": uri,
                        "mimeType": self.server.resources[uri].mime_type,
                        "text": json.dumps(content, indent=2)
                    }]
                }
            )
            
        except Exception as e:
            return MCPResponse(
                id=request.id,
                error={"code": -32603, "message": f"Resource read failed: {str(e)}"}
            )
    
    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle resource read notifications."""
        pass
        
    async def _read_resource(self, uri: str) -> Any:
        """Read a specific Chia resource."""
        if not self.server.rpc_client:
            raise Exception("RPC client not initialized")
            
        if uri == "chia://blockchain/status":
            response = await self.server.rpc_client.fetch("get_sync_status", {})
            return response
            
        elif uri == "chia://wallet/balance":
            response = await self.server.rpc_client.fetch("get_wallet_balance", {"wallet_id": 1})
            return response
            
        elif uri == "chia://wallet/transactions":
            response = await self.server.rpc_client.fetch("get_transactions", {
                "wallet_id": 1,
                "start": 0,
                "end": 10
            })
            return response
            
        else:
            raise Exception(f"Unknown resource: {uri}")


class ChiaResourceListHandler(MCPHandler):
    """Handler for listing available resources."""
    
    def __init__(self, server: ChiaMCPServer):
        self.server = server
        
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle resource list requests."""
        resources_list = [
            {
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "mimeType": resource.mime_type
            }
            for resource in self.server.resources.values()
        ]
        
        return MCPResponse(
            id=request.id,
            result={"resources": resources_list}
        )
    
    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle resource list notifications."""
        pass