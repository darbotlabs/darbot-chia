"""
Wallet plugin for Chia MCP server.

Provides hierarchical wallet-related tools and resources with enhanced functionality.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from .base import MCPPlugin, ToolCategory
from ..protocol import MCPTool, MCPResource


logger = logging.getLogger(__name__)


class WalletPlugin(MCPPlugin):
    """Plugin providing comprehensive wallet management tools."""
    
    @property
    def plugin_name(self) -> str:
        return "wallet"
    
    @property  
    def plugin_description(self) -> str:
        return "Comprehensive Chia wallet management tools for balances, transactions, and operations"
    
    def _register_categories(self) -> None:
        """Register wallet tool categories."""
        self.add_category(ToolCategory(
            name="balance",
            description="Wallet balance and coin management tools",
            icon="💰",
            tags=["balance", "coins", "spendable"]
        ))
        
        self.add_category(ToolCategory(
            name="transactions", 
            description="Transaction history and management tools",
            icon="📊",
            tags=["history", "transactions", "transfers"]
        ))
        
        self.add_category(ToolCategory(
            name="operations",
            description="Wallet operations and advanced functions", 
            icon="⚡",
            tags=["send", "receive", "operations"]
        ))
    
    def _register_tools(self) -> None:
        """Register wallet tools with enhanced functionality."""
        
        # Balance-related tools
        self.add_tool(MCPTool(
            name="balance",
            description="Get detailed balance information for a wallet including spendable coins",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer", 
                        "description": "ID of the wallet to check (default: 1 for XCH wallet)",
                        "default": 1,
                        "minimum": 1
                    },
                    "include_pending": {
                        "type": "boolean",
                        "description": "Include pending transactions in balance calculation",
                        "default": True
                    }
                },
                "examples": [
                    {"wallet_id": 1},
                    {"wallet_id": 2, "include_pending": False}
                ]
            }
        ))
        
        self.add_tool(MCPTool(
            name="coins",
            description="Get detailed information about wallet coins and their status",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "ID of the wallet to get coins for",
                        "default": 1
                    },
                    "min_coin_amount": {
                        "type": "integer", 
                        "description": "Minimum coin amount in mojos to include",
                        "default": 0
                    },
                    "max_coin_amount": {
                        "type": "integer",
                        "description": "Maximum coin amount in mojos to include (optional)"
                    },
                    "confirmed_only": {
                        "type": "boolean",
                        "description": "Only include confirmed coins",
                        "default": True
                    }
                }
            }
        ))
        
        # Transaction-related tools
        self.add_tool(MCPTool(
            name="transactions",
            description="Get comprehensive transaction history with filtering and sorting",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "ID of the wallet to get transactions for", 
                        "default": 1
                    },
                    "start": {
                        "type": "integer",
                        "description": "Starting index for pagination",
                        "default": 0,
                        "minimum": 0
                    },
                    "end": {
                        "type": "integer", 
                        "description": "Ending index for pagination",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "sort_key": {
                        "type": "string",
                        "description": "Sort transactions by field",
                        "enum": ["CONFIRMED_AT_HEIGHT", "CREATED_AT_TIME"],
                        "default": "CONFIRMED_AT_HEIGHT"
                    },
                    "reverse": {
                        "type": "boolean",
                        "description": "Reverse sort order (newest first)",
                        "default": True
                    },
                    "type_filter": {
                        "type": "integer",
                        "description": "Filter by transaction type (0=outgoing, 1=incoming)",
                        "enum": [0, 1]
                    }
                },
                "examples": [
                    {"wallet_id": 1, "end": 20},
                    {"wallet_id": 1, "type_filter": 1, "end": 10}
                ]
            }
        ))
        
        self.add_tool(MCPTool(
            name="transaction_detail",
            description="Get detailed information about a specific transaction",
            input_schema={
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "Transaction ID to get details for"
                    }
                },
                "required": ["transaction_id"],
                "examples": [
                    {"transaction_id": "0x1a2b3c4d5e6f..."}
                ]
            }
        ))
        
        # Operation tools  
        self.add_tool(MCPTool(
            name="send",
            description="Send XCH or other tokens to an address with advanced options",
            input_schema={
                "type": "object",
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "ID of the wallet to send from",
                        "default": 1
                    },
                    "amount": {
                        "type": "integer", 
                        "description": "Amount to send in mojos (1 XCH = 1,000,000,000,000 mojos)"
                    },
                    "address": {
                        "type": "string",
                        "description": "Destination Chia address (xch1...)",
                        "pattern": "^xch1[a-z0-9]{58}$"
                    },
                    "fee": {
                        "type": "integer",
                        "description": "Transaction fee in mojos",
                        "default": 0,
                        "minimum": 0
                    },
                    "memo": {
                        "type": "string",
                        "description": "Optional memo to attach to transaction",
                        "maxLength": 256
                    },
                    "coins": {
                        "type": "array",
                        "description": "Specific coins to use for transaction (optional)",
                        "items": {"type": "string"}
                    }
                },
                "required": ["amount", "address"],
                "examples": [
                    {
                        "amount": 1000000000000,
                        "address": "xch1...",
                        "fee": 100000000,
                        "memo": "Payment for services"
                    }
                ]
            }
        ))
        
        self.add_tool(MCPTool(
            name="create_backup",
            description="Create a backup of wallet data and mnemonics",
            input_schema={
                "type": "object", 
                "properties": {
                    "wallet_id": {
                        "type": "integer",
                        "description": "ID of wallet to backup (optional, backs up all if not specified)"
                    },
                    "include_private_keys": {
                        "type": "boolean", 
                        "description": "Include private key information (requires wallet unlock)",
                        "default": False
                    }
                }
            }
        ))
    
    def _register_resources(self) -> None:
        """Register wallet resources."""
        
        # Individual wallet resources
        for wallet_id in range(1, 10):  # Support up to 10 wallets
            self.add_resource(MCPResource(
                uri=f"chia://wallet/{wallet_id}/balance",
                name=f"Wallet {wallet_id} Balance",
                description=f"Real-time balance information for wallet {wallet_id}",
                mime_type="application/json"
            ))
            
            self.add_resource(MCPResource(
                uri=f"chia://wallet/{wallet_id}/transactions",
                name=f"Wallet {wallet_id} Transactions", 
                description=f"Recent transaction history for wallet {wallet_id}",
                mime_type="application/json"
            ))
        
        # Aggregate resources
        self.add_resource(MCPResource(
            uri="chia://wallet/summary",
            name="Wallet Summary",
            description="Summary of all wallets with balances and activity",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://wallet/recent_activity",
            name="Recent Wallet Activity",
            description="Recent activity across all wallets",
            mime_type="application/json"
        ))
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a wallet tool."""
        if not self.rpc_client:
            raise Exception("RPC client not initialized")
        
        if tool_name == "balance":
            return await self._get_wallet_balance(arguments)
        elif tool_name == "coins":
            return await self._get_wallet_coins(arguments)
        elif tool_name == "transactions":
            return await self._get_wallet_transactions(arguments)
        elif tool_name == "transaction_detail":
            return await self._get_transaction_detail(arguments)
        elif tool_name == "send":
            return await self._send_transaction(arguments)
        elif tool_name == "create_backup":
            return await self._create_wallet_backup(arguments)
        else:
            raise ValueError(f"Unknown wallet tool: {tool_name}")
    
    async def read_resource(self, uri: str) -> Any:
        """Read a wallet resource."""
        if not self.rpc_client:
            raise Exception("RPC client not initialized")
        
        if uri.startswith("chia://wallet/") and uri.endswith("/balance"):
            wallet_id = int(uri.split('/')[3])
            return await self._get_wallet_balance({"wallet_id": wallet_id})
        elif uri.startswith("chia://wallet/") and uri.endswith("/transactions"):
            wallet_id = int(uri.split('/')[3])
            return await self._get_wallet_transactions({"wallet_id": wallet_id, "end": 20})
        elif uri == "chia://wallet/summary":
            return await self._get_wallet_summary()
        elif uri == "chia://wallet/recent_activity":
            return await self._get_recent_activity()
        else:
            raise ValueError(f"Unknown wallet resource: {uri}")
    
    async def _get_wallet_balance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get enhanced wallet balance information."""
        wallet_id = args.get("wallet_id", 1)
        include_pending = args.get("include_pending", True)
        
        # Get basic balance
        balance_response = await self.rpc_client.fetch("get_wallet_balance", {"wallet_id": wallet_id})
        
        # Get additional wallet info
        wallet_info = await self.rpc_client.fetch("get_wallets", {})
        
        # Enhance with additional details
        result = {
            "wallet_id": wallet_id,
            "balance": balance_response.get("wallet_balance", {}),
            "wallet_info": next((w for w in wallet_info.get("wallets", []) if w["id"] == wallet_id), None),
            "include_pending": include_pending,
            "timestamp": self._get_current_timestamp()
        }
        
        return result
    
    async def _get_wallet_coins(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed coin information."""
        wallet_id = args.get("wallet_id", 1)
        min_amount = args.get("min_coin_amount", 0)
        max_amount = args.get("max_coin_amount")
        confirmed_only = args.get("confirmed_only", True)
        
        coins_response = await self.rpc_client.fetch("get_spendable_coins", {
            "wallet_id": wallet_id,
            "min_coin_amount": min_amount,
            "max_coin_amount": max_amount,
            "excluded_coin_amounts": [],
            "excluded_coins": []
        })
        
        return {
            "wallet_id": wallet_id,
            "coins": coins_response.get("confirmed_records", []) if confirmed_only else coins_response.get("records", []),
            "filter_criteria": {
                "min_amount": min_amount,
                "max_amount": max_amount,
                "confirmed_only": confirmed_only
            },
            "timestamp": self._get_current_timestamp()
        }
    
    async def _get_wallet_transactions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get enhanced transaction history."""
        wallet_id = args.get("wallet_id", 1)
        start = args.get("start", 0)
        end = args.get("end", 50)
        sort_key = args.get("sort_key", "CONFIRMED_AT_HEIGHT")
        reverse = args.get("reverse", True)
        type_filter = args.get("type_filter")
        
        tx_response = await self.rpc_client.fetch("get_transactions", {
            "wallet_id": wallet_id,
            "start": start,
            "end": end,
            "sort_key": sort_key,
            "reverse": reverse,
            "type_filter": type_filter
        })
        
        return {
            "wallet_id": wallet_id,
            "transactions": tx_response.get("transactions", []),
            "pagination": {
                "start": start,
                "end": end,
                "total_count": len(tx_response.get("transactions", []))
            },
            "sort_criteria": {
                "sort_key": sort_key,
                "reverse": reverse,
                "type_filter": type_filter
            },
            "timestamp": self._get_current_timestamp()
        }
    
    async def _get_transaction_detail(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed transaction information."""
        tx_id = args["transaction_id"]
        
        tx_response = await self.rpc_client.fetch("get_transaction", {"transaction_id": tx_id})
        
        return {
            "transaction_id": tx_id,
            "transaction": tx_response.get("transaction", {}),
            "timestamp": self._get_current_timestamp()
        }
    
    async def _send_transaction(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send transaction with enhanced features."""
        wallet_id = args.get("wallet_id", 1)
        amount = args["amount"]
        address = args["address"]
        fee = args.get("fee", 0)
        memo = args.get("memo")
        coins = args.get("coins")
        
        tx_params = {
            "wallet_id": wallet_id,
            "amount": amount,
            "address": address,
            "fee": fee
        }
        
        if memo:
            tx_params["memos"] = [memo]
        if coins:
            tx_params["coins"] = coins
        
        tx_response = await self.rpc_client.fetch("send_transaction", tx_params)
        
        return {
            "transaction": tx_response,
            "parameters": tx_params,
            "timestamp": self._get_current_timestamp()
        }
    
    async def _create_wallet_backup(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create wallet backup."""
        wallet_id = args.get("wallet_id")
        include_private = args.get("include_private_keys", False)
        
        if wallet_id:
            wallets_response = await self.rpc_client.fetch("get_wallet_info", {"wallet_id": wallet_id})
        else:
            wallets_response = await self.rpc_client.fetch("get_wallets", {})
        
        backup_data = {
            "wallets": wallets_response,
            "backup_timestamp": self._get_current_timestamp(),
            "includes_private_keys": include_private
        }
        
        if include_private:
            # Note: This would require additional security and wallet unlock
            backup_data["warning"] = "Private key backup requires wallet to be unlocked"
        
        return backup_data
    
    async def _get_wallet_summary(self) -> Dict[str, Any]:
        """Get summary of all wallets."""
        wallets_response = await self.rpc_client.fetch("get_wallets", {})
        
        summary = {
            "wallets": [],
            "total_wallets": 0,
            "timestamp": self._get_current_timestamp()
        }
        
        for wallet in wallets_response.get("wallets", []):
            balance_response = await self.rpc_client.fetch("get_wallet_balance", {"wallet_id": wallet["id"]})
            summary["wallets"].append({
                "id": wallet["id"],
                "name": wallet["name"],
                "type": wallet["type"],
                "balance": balance_response.get("wallet_balance", {})
            })
        
        summary["total_wallets"] = len(summary["wallets"])
        return summary
    
    async def _get_recent_activity(self) -> Dict[str, Any]:
        """Get recent activity across all wallets."""
        wallets_response = await self.rpc_client.fetch("get_wallets", {})
        all_transactions = []
        
        for wallet in wallets_response.get("wallets", []):
            tx_response = await self.rpc_client.fetch("get_transactions", {
                "wallet_id": wallet["id"],
                "start": 0,
                "end": 10
            })
            
            for tx in tx_response.get("transactions", []):
                tx["wallet_id"] = wallet["id"]
                tx["wallet_name"] = wallet["name"]
                all_transactions.append(tx)
        
        # Sort by creation time
        all_transactions.sort(key=lambda x: x.get("created_at_time", 0), reverse=True)
        
        return {
            "recent_transactions": all_transactions[:20],  # Top 20 most recent
            "timestamp": self._get_current_timestamp()
        }
    
    def _get_current_timestamp(self) -> int:
        """Get current timestamp."""
        import time
        return int(time.time())