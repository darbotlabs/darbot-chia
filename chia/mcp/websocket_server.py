"""
WebSocket server implementation for MCP (Model Context Protocol) over WebSockets.

This module provides WebSocket server functionality to handle MCP connections
and facilitate communication between AI models and the Chia blockchain.
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Set

import websockets
from websockets.server import WebSocketServerProtocol

from .server import ChiaMCPServer

logger = logging.getLogger(__name__)


class MCPWebSocketServer:
    """WebSocket server for MCP protocol communication."""

    def __init__(self, mcp_server: ChiaMCPServer):
        self.mcp_server = mcp_server
        self.clients: Set[WebSocketServerProtocol] = set()
        self.websocket_server = None

    async def start(self) -> None:
        """Start the WebSocket server."""
        try:
            # Start the underlying MCP server
            await self.mcp_server.start()

            # Start WebSocket server
            self.websocket_server = await websockets.serve(
                self.handle_client, self.mcp_server.host, self.mcp_server.port
            )

            logger.info(f"MCP WebSocket server started on ws://{self.mcp_server.host}:{self.mcp_server.port}")

        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise

    async def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.websocket_server:
            self.websocket_server.close()
            await self.websocket_server.wait_closed()

        await self.mcp_server.stop()
        logger.info("MCP WebSocket server stopped")

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """Handle a new WebSocket client connection."""
        self.clients.add(websocket)
        client_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"New MCP client connected: {client_address}")

        try:
            # Send initial capabilities message
            await self.send_capabilities(websocket)

            # Handle incoming messages
            async for message in websocket:
                try:
                    if isinstance(message, str):
                        await self.mcp_server.handle_message(websocket, message)
                    else:
                        logger.warning(f"Received non-text message from {client_address}")

                except Exception as e:
                    logger.error(f"Error handling message from {client_address}: {e}")
                    await self.send_error(websocket, f"Error processing message: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_address}")
        except Exception as e:
            logger.error(f"Error in client handler for {client_address}: {e}")
        finally:
            self.clients.discard(websocket)

    async def send_capabilities(self, websocket: WebSocketServerProtocol) -> None:
        """Send server capabilities to the client."""
        # Get plugin information to include in capabilities
        plugin_info = self.mcp_server.plugin_manager.get_plugin_info()
        all_tools = self.mcp_server.plugin_manager.get_all_tools()
        all_resources = self.mcp_server.plugin_manager.get_all_resources()
        categories = self.mcp_server.plugin_manager.get_all_categories()

        capabilities = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": True, "listChanged": True},
                    "experimental": {"plugins": True, "hierarchical_tools": True, "categories": True},
                },
                "serverInfo": {
                    "name": "chia-mcp-server",
                    "version": "2.0.0",
                    "description": "Hierarchical Chia blockchain MCP server with advanced plugin system",
                    "plugins": len(plugin_info),
                    "tools": len(all_tools),
                    "resources": len(all_resources),
                    "categories": len(categories),
                    "plugin_summary": [
                        {"name": info["name"], "tools": info["tools_count"], "resources": info["resources_count"]}
                        for info in plugin_info
                    ],
                },
            },
        }

        await websocket.send(json.dumps(capabilities, indent=2))

    async def send_error(self, websocket: WebSocketServerProtocol, error_message: str) -> None:
        """Send error message to client."""
        error_response = {"jsonrpc": "2.0", "error": {"code": -32603, "message": error_message}}

        await websocket.send(json.dumps(error_response))

    async def broadcast_notification(self, notification: dict) -> None:
        """Broadcast a notification to all connected clients."""
        if self.clients:
            message = json.dumps(notification)
            await asyncio.gather(*[client.send(message) for client in self.clients], return_exceptions=True)


async def run_mcp_websocket_server(host: str = "localhost", port: int = 8080, chia_rpc_port: int = 9256) -> None:
    """Run the MCP WebSocket server."""

    # Create MCP server
    mcp_server = ChiaMCPServer(host=host, port=port, chia_rpc_port=chia_rpc_port)

    # Create WebSocket server
    ws_server = MCPWebSocketServer(mcp_server)

    try:
        await ws_server.start()

        # Keep the server running
        logger.info("MCP WebSocket server is running. Press Ctrl+C to stop.")
        await asyncio.Future()  # Run forever

    except KeyboardInterrupt:
        logger.info("Shutting down MCP WebSocket server...")
    finally:
        await ws_server.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chia MCP WebSocket Server")
    parser.add_argument("--host", default="localhost", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind the server to")
    parser.add_argument("--chia-rpc-port", type=int, default=9256, help="Chia wallet RPC port")
    parser.add_argument(
        "--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Logging level"
    )

    args = parser.parse_args()

    # Setup logging
    numeric_level = getattr(logging, args.log_level.upper(), None)
    logging.basicConfig(level=numeric_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Run the server
    asyncio.run(run_mcp_websocket_server(args.host, args.port, args.chia_rpc_port))
