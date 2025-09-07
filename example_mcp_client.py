#!/usr/bin/env python3
"""
Example MCP client that demonstrates how to interact with the Chia MCP server.

This example shows how to:
1. Connect to the MCP server via WebSocket
2. List available tools and resources
3. Call Chia-specific tools
4. Read Chia blockchain resources
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Dict

import websockets


class ChiaMCPClient:
    """Example MCP client for interacting with Chia MCP server."""

    def __init__(self, uri: str = "ws://localhost:8080"):
        self.uri = uri
        self.websocket = None
        self.request_id = 0

    async def connect(self):
        """Connect to the MCP server."""
        print(f"Connecting to MCP server at {self.uri}")
        self.websocket = await websockets.connect(self.uri)
        print("✓ Connected to MCP server")

    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.websocket:
            await self.websocket.close()
            print("✓ Disconnected from MCP server")

    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send an MCP request and return the response."""
        self.request_id += 1
        request = {"jsonrpc": "2.0", "id": self.request_id, "method": method, "params": params or {}}

        print(f"\n📤 Sending request: {method}")
        print(f"   Params: {json.dumps(params, indent=2) if params else 'None'}")

        await self.websocket.send(json.dumps(request))
        response_text = await self.websocket.recv()
        response = json.loads(response_text)

        print("📥 Received response:")
        if response.get("error"):
            print(f"   ❌ Error: {response['error']}")
        else:
            print("   ✓ Success")
            if "result" in response:
                print(f"   Result: {json.dumps(response['result'], indent=4)}")

        return response

    async def list_tools(self):
        """List all available tools."""
        print("\n=== Listing Available Tools ===")
        response = await self.send_request("tools/list")

        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"\nFound {len(tools)} tools:")
            for tool in tools:
                print(f"  • {tool['name']}: {tool['description']}")

        return response

    async def list_resources(self):
        """List all available resources."""
        print("\n=== Listing Available Resources ===")
        response = await self.send_request("resources/list")

        if "result" in response and "resources" in response["result"]:
            resources = response["result"]["resources"]
            print(f"\nFound {len(resources)} resources:")
            for resource in resources:
                print(f"  • {resource['uri']}: {resource['name']}")
                if resource.get("description"):
                    print(f"    {resource['description']}")

        return response

    async def get_wallet_balance(self, wallet_id: int = 1):
        """Get the balance of a Chia wallet."""
        print(f"\n=== Getting Wallet {wallet_id} Balance ===")
        response = await self.send_request(
            "tools/call", {"name": "get_wallet_balance", "arguments": {"wallet_id": wallet_id}}
        )
        return response

    async def get_transactions(self, wallet_id: int = 1, count: int = 5):
        """Get recent transactions for a wallet."""
        print(f"\n=== Getting Recent Transactions for Wallet {wallet_id} ===")
        response = await self.send_request(
            "tools/call", {"name": "get_transactions", "arguments": {"wallet_id": wallet_id, "start": 0, "end": count}}
        )
        return response

    async def get_wallets(self):
        """Get list of all wallets."""
        print("\n=== Getting All Wallets ===")
        response = await self.send_request("tools/call", {"name": "get_wallets", "arguments": {}})
        return response

    async def get_sync_status(self):
        """Get blockchain sync status."""
        print("\n=== Getting Sync Status ===")
        response = await self.send_request("tools/call", {"name": "get_sync_status", "arguments": {}})
        return response

    async def read_blockchain_status(self):
        """Read blockchain status resource."""
        print("\n=== Reading Blockchain Status Resource ===")
        response = await self.send_request("resources/read", {"uri": "chia://blockchain/status"})
        return response

    async def read_wallet_balance_resource(self):
        """Read wallet balance resource."""
        print("\n=== Reading Wallet Balance Resource ===")
        response = await self.send_request("resources/read", {"uri": "chia://wallet/balance"})
        return response

    async def demonstrate_send_transaction(self):
        """Demonstrate send transaction (without actually sending)."""
        print("\n=== Send Transaction Example (Demo) ===")
        print("ℹ️  This is a demonstration - no actual transaction will be sent")

        # This would normally send a real transaction
        example_params = {
            "name": "send_transaction",
            "arguments": {
                "wallet_id": 1,
                "amount": 1000000000000,  # 1 XCH in mojos
                "address": "xch1example_address_not_real",
                "fee": 100000000,  # 0.1 XCH fee in mojos
            },
        }

        print("Example request:")
        print(json.dumps(example_params, indent=2))
        print("\n⚠️  To actually send transactions, ensure:")
        print("   1. Wallet is unlocked")
        print("   2. Sufficient balance exists")
        print("   3. Valid destination address")
        print("   4. Appropriate fee amount")


async def main():
    """Main demonstration function."""
    print("🚀 Chia MCP Client Example")
    print("=" * 50)

    client = ChiaMCPClient()

    try:
        # Connect to the server
        await client.connect()

        # Wait a moment for initialization
        await asyncio.sleep(1)

        # Demonstrate MCP functionality
        await client.list_tools()
        await client.list_resources()

        # Note: These will fail if Chia is not running, but demonstrate the protocol
        print("\n" + "=" * 50)
        print("🔗 Chia Blockchain Interactions")
        print("   (These require a running Chia node)")
        print("=" * 50)

        await client.get_wallets()
        await client.get_sync_status()
        await client.get_wallet_balance()
        await client.get_transactions()

        await client.read_blockchain_status()
        await client.read_wallet_balance_resource()

        await client.demonstrate_send_transaction()

    except ConnectionRefusedError:
        print("\n❌ Could not connect to MCP server")
        print("   Make sure the Chia MCP server is running:")
        print("   python -m chia.mcp.cli")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        await client.disconnect()


async def test_protocol_without_server():
    """Test MCP protocol functionality without requiring a server."""
    print("\n" + "=" * 50)
    print("🧪 Testing MCP Protocol (No Server Required)")
    print("=" * 50)

    # Import MCP protocol
    from .protocol import MCPRequest, MCPResponse, deserialize_message, serialize_message

    # Test request creation and serialization
    request = MCPRequest(
        method="tools/call", id=1, params={"name": "get_wallet_balance", "arguments": {"wallet_id": 1}}
    )

    serialized = serialize_message(request)
    print(f"✓ Created MCP request: {serialized}")

    # Test deserialization
    deserialized = deserialize_message(serialized)
    print(f"✓ Deserialized method: {deserialized.method}")
    print(f"✓ Deserialized params: {deserialized.params}")

    # Test response creation
    response = MCPResponse(
        id=1,
        result={
            "wallet_balance": {
                "confirmed_wallet_balance": 1000000000000,
                "unconfirmed_wallet_balance": 1000000000000,
                "spendable_balance": 1000000000000,
            }
        },
    )

    serialized_response = serialize_message(response)
    print(f"✓ Created MCP response: {serialized_response}")


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Connect to MCP server (requires running server)")
    print("2. Test protocol only (no server required)")

    try:
        choice = input("\nEnter choice (1 or 2): ").strip()

        if choice == "1":
            asyncio.run(main())
        elif choice == "2":
            asyncio.run(test_protocol_without_server())
        else:
            print("Invalid choice. Running protocol test...")
            asyncio.run(test_protocol_without_server())

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except EOFError:
        # Handle cases where input is not available (e.g., CI/CD)
        print("No input available, running protocol test...")
        asyncio.run(test_protocol_without_server())
