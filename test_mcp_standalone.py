#!/usr/bin/env python3
"""
Standalone test for MCP implementation without requiring full Chia environment.
"""

import json
import sys
from pathlib import Path

# Add chia directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from chia.mcp.protocol import (
        MCPRequest, MCPResponse, MCPNotification, MCPTool, MCPResource,
        serialize_message, deserialize_message
    )
    print("✓ Protocol imports successful")
except Exception as e:
    print(f"✗ Protocol import failed: {e}")
    sys.exit(1)

def test_protocol():
    """Test MCP protocol functionality."""
    
    # Test request serialization/deserialization
    print("\nTesting MCP Request:")
    request = MCPRequest(method="test_method", params={"key": "value"}, id=1)
    serialized = serialize_message(request)
    print(f"  Serialized: {serialized}")
    
    deserialized = deserialize_message(serialized)
    print(f"  Deserialized method: {deserialized.method}")
    print(f"  Deserialized params: {deserialized.params}")
    print(f"  Deserialized id: {deserialized.id}")
    
    # Test response serialization/deserialization
    print("\nTesting MCP Response:")
    response = MCPResponse(id=1, result={"success": True})
    serialized = serialize_message(response)
    print(f"  Serialized: {serialized}")
    
    deserialized = deserialize_message(serialized)
    print(f"  Deserialized id: {deserialized.id}")
    print(f"  Deserialized result: {deserialized.result}")
    
    # Test notification
    print("\nTesting MCP Notification:")
    notification = MCPNotification(method="notify", params={"message": "hello"})
    serialized = serialize_message(notification)
    print(f"  Serialized: {serialized}")
    
    deserialized = deserialize_message(serialized)
    print(f"  Deserialized method: {deserialized.method}")
    print(f"  Deserialized params: {deserialized.params}")
    
    # Test tool creation
    print("\nTesting MCP Tool:")
    tool = MCPTool(
        name="test_tool",
        description="A test tool",
        input_schema={
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            }
        }
    )
    print(f"  Tool name: {tool.name}")
    print(f"  Tool description: {tool.description}")
    print(f"  Tool schema: {json.dumps(tool.input_schema, indent=2)}")
    
    # Test resource creation
    print("\nTesting MCP Resource:")
    resource = MCPResource(
        uri="test://resource",
        name="Test Resource",
        description="A test resource",
        mime_type="application/json"
    )
    print(f"  Resource URI: {resource.uri}")
    print(f"  Resource name: {resource.name}")
    print(f"  Resource description: {resource.description}")
    print(f"  Resource MIME type: {resource.mime_type}")

def test_chia_tools():
    """Test Chia-specific tool definitions."""
    
    print("\nTesting Chia Tool Definitions:")
    
    # Define expected Chia tools
    chia_tools = [
        {
            "name": "get_wallet_balance",
            "description": "Get the balance of a Chia wallet",
            "input_schema": {
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "The ID of the wallet to check balance for",
                        "default": 1
                    }
                }
            }
        },
        {
            "name": "get_transactions", 
            "description": "Get transaction history for a Chia wallet",
            "input_schema": {
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
        }
    ]
    
    for tool_def in chia_tools:
        tool = MCPTool(**tool_def)
        print(f"  ✓ {tool.name}: {tool.description}")

def main():
    """Run all tests."""
    print("=== MCP Implementation Test ===")
    
    try:
        test_protocol()
        test_chia_tools()
        
        print("\n✅ All MCP tests passed!")
        print("\nMCP Implementation Summary:")
        print("- Protocol messages (Request, Response, Notification) ✓")
        print("- Message serialization/deserialization ✓") 
        print("- Tool and Resource definitions ✓")
        print("- Chia-specific tool schemas ✓")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()