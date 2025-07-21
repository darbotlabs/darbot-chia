#!/usr/bin/env python3
"""
Simple MCP protocol demonstration without external dependencies.

This example shows the core MCP functionality and protocol without requiring
a running server or additional dependencies.
"""

import json
import sys
from pathlib import Path

# Add the chia directory to path
sys.path.insert(0, str(Path(__file__).parent))

from chia.mcp.protocol import (
    MCPRequest, MCPResponse, MCPNotification, MCPTool, MCPResource,
    serialize_message, deserialize_message
)


def demonstrate_mcp_protocol():
    """Demonstrate MCP protocol functionality."""
    
    print("🚀 Chia MCP Protocol Demonstration")
    print("=" * 50)
    
    # 1. Tool Call Example
    print("\n📞 Tool Call Example: Get Wallet Balance")
    request = MCPRequest(
        method="tools/call",
        id=1,
        params={
            "name": "get_wallet_balance", 
            "arguments": {"wallet_id": 1}
        }
    )
    
    print("Request:")
    serialized_request = serialize_message(request)
    print(json.dumps(json.loads(serialized_request), indent=2))
    
    # Simulate response
    response = MCPResponse(
        id=1,
        result={
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "wallet_balance": {
                        "confirmed_wallet_balance": 2500000000000,  # 2.5 XCH
                        "unconfirmed_wallet_balance": 2500000000000,
                        "spendable_balance": 2400000000000,  # 2.4 XCH available
                        "pending_change": 100000000000,  # 0.1 XCH in change
                        "max_send_amount": 2400000000000,
                        "unspent_coin_count": 15,
                        "pending_coin_removal_count": 1
                    },
                    "success": True
                }, indent=2)
            }]
        }
    )
    
    print("\nResponse:")
    serialized_response = serialize_message(response)
    print(json.dumps(json.loads(serialized_response), indent=2))
    
    # 2. Transaction List Example
    print("\n📜 Tool Call Example: Get Transactions")
    tx_request = MCPRequest(
        method="tools/call",
        id=2,
        params={
            "name": "get_transactions",
            "arguments": {
                "wallet_id": 1,
                "start": 0,
                "end": 3
            }
        }
    )
    
    print("Request:")
    print(json.dumps(json.loads(serialize_message(tx_request)), indent=2))
    
    # Simulate transaction response
    tx_response = MCPResponse(
        id=2,
        result={
            "content": [{
                "type": "text", 
                "text": json.dumps({
                    "transactions": [
                        {
                            "transaction_id": "0x1a2b3c4d...",
                            "confirmed": True,
                            "confirmed_at_height": 4123456,
                            "created_at_time": 1703001234,
                            "amount": 1000000000000,  # 1 XCH received
                            "fee_amount": 0,
                            "type": 1,  # Incoming
                            "wallet_id": 1
                        },
                        {
                            "transaction_id": "0x5e6f7g8h...",
                            "confirmed": True,
                            "confirmed_at_height": 4123450,
                            "created_at_time": 1703000890,
                            "amount": -500000000000,  # 0.5 XCH sent
                            "fee_amount": 50000000,   # 0.05 XCH fee
                            "type": 0,  # Outgoing
                            "wallet_id": 1
                        },
                        {
                            "transaction_id": "0x9i0j1k2l...",
                            "confirmed": False,
                            "confirmed_at_height": 0,
                            "created_at_time": 1703002000,
                            "amount": 750000000000,  # 0.75 XCH receiving
                            "fee_amount": 0,
                            "type": 1,  # Incoming (pending)
                            "wallet_id": 1
                        }
                    ],
                    "success": True
                }, indent=2)
            }]
        }
    )
    
    print("\nResponse:")
    print(json.dumps(json.loads(serialize_message(tx_response)), indent=2))
    
    # 3. Resource Read Example
    print("\n📖 Resource Read Example: Blockchain Status")
    resource_request = MCPRequest(
        method="resources/read",
        id=3,
        params={"uri": "chia://blockchain/status"}
    )
    
    print("Request:")
    print(json.dumps(json.loads(serialize_message(resource_request)), indent=2))
    
    # Simulate blockchain status response
    status_response = MCPResponse(
        id=3,
        result={
            "contents": [{
                "uri": "chia://blockchain/status",
                "mimeType": "application/json",
                "text": json.dumps({
                    "blockchain_state": {
                        "peak": {
                            "height": 4123456,
                            "header_hash": "0xabcdef1234567890...",
                            "prev_header_hash": "0x1234567890abcdef...",
                            "timestamp": 1703001234
                        },
                        "sync": {
                            "sync_mode": False,
                            "synced": True,
                            "sync_tip_height": 4123456,
                            "sync_progress_height": 4123456
                        },
                        "difficulty": 1234567890,
                        "sub_slot_iters": 134217728,
                        "space": 32845932815360000000,  # Total network space
                        "mempool_size": 156,
                        "mempool_cost": 11234567890,
                        "mempool_min_fees": {
                            "cost_5000000": 10000000,   # Min fee for 5M cost
                            "cost_11000000": 20000000,  # Min fee for 11M cost
                            "cost_21000000": 50000000   # Min fee for 21M cost
                        }
                    },
                    "success": True
                }, indent=2)
            }]
        }
    )
    
    print("\nResponse:")
    print(json.dumps(json.loads(serialize_message(status_response)), indent=2))
    
    # 4. Tools List Example
    print("\n🛠️  Tools List Example")
    tools_request = MCPRequest(method="tools/list", id=4)
    
    print("Request:")
    print(json.dumps(json.loads(serialize_message(tools_request)), indent=2))
    
    # Simulate tools list response
    tools_response = MCPResponse(
        id=4,
        result={
            "tools": [
                {
                    "name": "get_wallet_balance",
                    "description": "Get the balance of a Chia wallet",
                    "inputSchema": {
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
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "wallet_id": {"type": "integer", "default": 1},
                            "start": {"type": "integer", "default": 0},
                            "end": {"type": "integer", "default": 50}
                        }
                    }
                },
                {
                    "name": "send_transaction",
                    "description": "Send XCH or other tokens to another address",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "wallet_id": {"type": "integer", "default": 1},
                            "amount": {"type": "integer", "description": "Amount in mojos"},
                            "address": {"type": "string", "description": "Destination address"},
                            "fee": {"type": "integer", "default": 0}
                        },
                        "required": ["amount", "address"]
                    }
                }
            ]
        }
    )
    
    print("\nResponse:")
    print(json.dumps(json.loads(serialize_message(tools_response)), indent=2))
    
    # 5. Error Example
    print("\n❌ Error Response Example")
    error_request = MCPRequest(
        method="tools/call",
        id=5,
        params={
            "name": "nonexistent_tool",
            "arguments": {}
        }
    )
    
    error_response = MCPResponse(
        id=5,
        error={
            "code": -32601,
            "message": "Tool not found: nonexistent_tool"
        }
    )
    
    print("Request:")
    print(json.dumps(json.loads(serialize_message(error_request)), indent=2))
    print("\nError Response:")
    print(json.dumps(json.loads(serialize_message(error_response)), indent=2))


def demonstrate_chia_tools():
    """Demonstrate Chia-specific tool definitions."""
    
    print("\n🔧 Chia MCP Tools")
    print("=" * 50)
    
    # Available tools
    tools = [
        MCPTool(
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
        ),
        MCPTool(
            name="get_transactions",
            description="Get transaction history for a Chia wallet",
            input_schema={
                "type": "object", 
                "properties": {
                    "wallet_id": {"type": "integer", "default": 1},
                    "start": {"type": "integer", "default": 0},
                    "end": {"type": "integer", "default": 50}
                }
            }
        ),
        MCPTool(
            name="send_transaction",
            description="Send XCH or other tokens to another address",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {"type": "integer", "default": 1},
                    "amount": {"type": "integer", "description": "Amount in mojos (1 XCH = 1e12 mojos)"},
                    "address": {"type": "string", "description": "Destination Chia address"},
                    "fee": {"type": "integer", "default": 0, "description": "Transaction fee in mojos"}
                },
                "required": ["amount", "address"]
            }
        ),
        MCPTool(
            name="get_wallets",
            description="Get list of all available wallets",
            input_schema={"type": "object", "properties": {}}
        ),
        MCPTool(
            name="get_sync_status",
            description="Get blockchain synchronization status",
            input_schema={"type": "object", "properties": {}}
        )
    ]
    
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool.name}")
        print(f"   Description: {tool.description}")
        print(f"   Input Schema:")
        print(json.dumps(tool.input_schema, indent=6))


def demonstrate_chia_resources():
    """Demonstrate Chia-specific resource definitions."""
    
    print("\n📚 Chia MCP Resources")
    print("=" * 50)
    
    resources = [
        MCPResource(
            uri="chia://blockchain/status",
            name="Blockchain Status",
            description="Current blockchain sync status and network information",
            mime_type="application/json"
        ),
        MCPResource(
            uri="chia://wallet/balance",
            name="Wallet Balance",
            description="Current wallet balance information for the default wallet",
            mime_type="application/json"
        ),
        MCPResource(
            uri="chia://wallet/transactions",
            name="Wallet Transactions",
            description="Recent transaction history for wallets",
            mime_type="application/json"
        )
    ]
    
    for i, resource in enumerate(resources, 1):
        print(f"\n{i}. {resource.name}")
        print(f"   URI: {resource.uri}")
        print(f"   Description: {resource.description}")
        print(f"   MIME Type: {resource.mime_type}")


def main():
    """Main demonstration."""
    try:
        demonstrate_mcp_protocol()
        demonstrate_chia_tools()
        demonstrate_chia_resources()
        
        print("\n" + "=" * 50)
        print("✅ MCP Protocol Demonstration Complete!")
        print("\nTo use this with a real Chia node:")
        print("1. Ensure Chia wallet is running")
        print("2. Start the MCP server: python -m chia.mcp.cli")
        print("3. Connect with an MCP client on ws://localhost:8080")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()