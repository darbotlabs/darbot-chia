"""
Model Context Protocol (MCP) server for Chia blockchain integration.

This module provides MCP server functionality to allow AI models to interact with
the Chia blockchain, access wallet information, transaction data, and perform
various blockchain operations through the MCP protocol.
"""

from __future__ import annotations

__all__ = ["MCPNotification", "MCPRequest", "MCPResource", "MCPResponse", "MCPTool"]

# Import protocol types that don't require external dependencies
from .protocol import MCPNotification, MCPRequest, MCPResource, MCPResponse, MCPTool

__version__ = "1.0.0"


# Server classes require additional dependencies, import them explicitly when needed
def get_mcp_server():
    """Get MCPServer class (requires external dependencies)."""
    from .server import MCPServer

    return MCPServer


def get_chia_mcp_server():
    """Get ChiaMCPServer class (requires Chia RPC dependencies)."""
    from .server import ChiaMCPServer

    return ChiaMCPServer
