"""
Tests for the Chia MCP (Model Context Protocol) implementation.
"""

import asyncio
import json
import pytest
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

from chia.mcp.protocol import (
    MCPRequest, MCPResponse, MCPNotification, MCPTool, MCPResource,
    serialize_message, deserialize_message
)
from chia.mcp.server import ChiaMCPServer, ChiaToolCallHandler


class TestMCPProtocol:
    """Test MCP protocol message handling."""
    
    def test_serialize_request(self):
        """Test serializing MCP request."""
        request = MCPRequest(method="test_method", params={"key": "value"}, id=1)
        serialized = serialize_message(request)
        
        expected = {
            "jsonrpc": "2.0",
            "method": "test_method", 
            "params": {"key": "value"},
            "id": 1
        }
        
        assert json.loads(serialized) == expected
    
    def test_deserialize_request(self):
        """Test deserializing MCP request."""
        data = '{"jsonrpc": "2.0", "method": "test_method", "params": {"key": "value"}, "id": 1}'
        message = deserialize_message(data)
        
        assert isinstance(message, MCPRequest)
        assert message.method == "test_method"
        assert message.params == {"key": "value"}
        assert message.id == 1
    
    def test_serialize_response(self):
        """Test serializing MCP response."""
        response = MCPResponse(id=1, result={"success": True})
        serialized = serialize_message(response)
        
        expected = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"success": True},
            "error": None
        }
        
        assert json.loads(serialized) == expected
    
    def test_deserialize_response(self):
        """Test deserializing MCP response."""
        data = '{"jsonrpc": "2.0", "id": 1, "result": {"success": true}, "error": null}'
        message = deserialize_message(data)
        
        assert isinstance(message, MCPResponse)
        assert message.id == 1
        assert message.result == {"success": True}
        assert message.error is None


class TestChiaMCPServer:
    """Test Chia MCP server functionality."""
    
    @pytest.fixture
    def server(self):
        """Create a test MCP server."""
        return ChiaMCPServer(host="localhost", port=8080)
    
    def test_server_initialization(self, server):
        """Test server initialization."""
        assert server.host == "localhost"
        assert server.port == 8080
        assert server.chia_rpc_port == 9256
        assert len(server.tools) > 0  # Should have default Chia tools
        assert len(server.resources) > 0  # Should have default Chia resources
    
    def test_default_tools_registered(self, server):
        """Test that default Chia tools are registered."""
        expected_tools = [
            "get_wallet_balance",
            "get_transactions", 
            "send_transaction",
            "get_wallets",
            "get_sync_status"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in server.tools
            tool = server.tools[tool_name]
            assert isinstance(tool, MCPTool)
            assert tool.name == tool_name
            assert tool.description is not None
            assert tool.input_schema is not None
    
    def test_default_resources_registered(self, server):
        """Test that default Chia resources are registered."""
        expected_resources = [
            "chia://blockchain/status",
            "chia://wallet/balance",
            "chia://wallet/transactions"
        ]
        
        for resource_uri in expected_resources:
            assert resource_uri in server.resources
            resource = server.resources[resource_uri]
            assert isinstance(resource, MCPResource)
            assert resource.uri == resource_uri
            assert resource.name is not None
    
    @pytest.mark.asyncio
    async def test_tool_call_handler_unknown_tool(self, server):
        """Test tool call handler with unknown tool."""
        handler = ChiaToolCallHandler(server)
        request = MCPRequest(
            method="tools/call",
            params={"name": "unknown_tool", "arguments": {}},
            id=1
        )
        
        response = await handler.handle_request(request)
        
        assert isinstance(response, MCPResponse)
        assert response.id == 1
        assert response.error is not None
        assert "Tool not found" in response.error["message"]
    
    @pytest.mark.asyncio
    async def test_tool_call_handler_missing_name(self, server):
        """Test tool call handler without tool name."""
        handler = ChiaToolCallHandler(server)
        request = MCPRequest(
            method="tools/call",
            params={"arguments": {}},
            id=1
        )
        
        response = await handler.handle_request(request)
        
        assert isinstance(response, MCPResponse)
        assert response.id == 1
        assert response.error is not None
        assert "Missing tool name" in response.error["message"]
    
    @pytest.mark.asyncio
    @patch('chia.mcp.server.RpcClient')
    async def test_tool_execution_get_wallet_balance(self, mock_rpc_client, server):
        """Test executing get_wallet_balance tool."""
        # Mock RPC client
        mock_client_instance = AsyncMock()
        mock_client_instance.fetch.return_value = {
            "wallet_balance": {
                "confirmed_wallet_balance": 1000000000000,  # 1 XCH
                "unconfirmed_wallet_balance": 1000000000000,
                "spendable_balance": 1000000000000
            }
        }
        mock_rpc_client.create.return_value = mock_client_instance
        server.rpc_client = mock_client_instance
        
        handler = ChiaToolCallHandler(server)
        request = MCPRequest(
            method="tools/call",
            params={
                "name": "get_wallet_balance",
                "arguments": {"wallet_id": 1}
            },
            id=1
        )
        
        response = await handler.handle_request(request)
        
        assert isinstance(response, MCPResponse)
        assert response.id == 1
        assert response.error is None
        assert response.result is not None
        
        # Verify RPC was called correctly
        mock_client_instance.fetch.assert_called_once_with(
            "get_wallet_balance", 
            {"wallet_id": 1}
        )


class TestMCPIntegration:
    """Integration tests for MCP functionality."""
    
    @pytest.mark.asyncio
    async def test_server_start_stop(self):
        """Test server startup and shutdown."""
        server = ChiaMCPServer()
        
        # Mock the config loading and RPC client creation
        with patch('chia.mcp.server.load_config') as mock_load_config, \
             patch('chia.mcp.server.RpcClient') as mock_rpc_client:
            
            mock_load_config.return_value = {"wallet": {"rpc_port": 9256}}
            mock_client_instance = AsyncMock()
            mock_rpc_client.create.return_value = mock_client_instance
            
            # Test start
            await server.start()
            assert server.rpc_client is not None
            
            # Test stop
            await server.stop()
            assert server.rpc_client is None
    
    def test_mcp_tool_schema_validation(self):
        """Test that MCP tool schemas are valid."""
        server = ChiaMCPServer()
        
        for tool_name, tool in server.tools.items():
            # Verify required fields
            assert tool.name is not None
            assert tool.description is not None
            assert tool.input_schema is not None
            
            # Verify schema structure
            schema = tool.input_schema
            assert "type" in schema
            assert schema["type"] == "object"
            assert "properties" in schema
            
            # Verify properties are properly defined
            for prop_name, prop_def in schema["properties"].items():
                assert "type" in prop_def
                assert isinstance(prop_def["type"], str)


if __name__ == "__main__":
    pytest.main([__file__])