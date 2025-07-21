"""
Blockchain plugin for Chia MCP server.

Provides hierarchical blockchain-related tools and resources with comprehensive
network and consensus information.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .base import MCPPlugin, ToolCategory
from ..protocol import MCPTool, MCPResource


logger = logging.getLogger(__name__)


class BlockchainPlugin(MCPPlugin):
    """Plugin providing comprehensive blockchain information and analysis tools."""
    
    @property
    def plugin_name(self) -> str:
        return "blockchain"
    
    @property
    def plugin_description(self) -> str:
        return "Comprehensive Chia blockchain analysis tools for network status, blocks, and consensus"
    
    def _register_categories(self) -> None:
        """Register blockchain tool categories."""
        self.add_category(ToolCategory(
            name="network",
            description="Network status and connectivity tools",
            icon="🌐",
            tags=["network", "peers", "connections"]
        ))
        
        self.add_category(ToolCategory(
            name="blocks",
            description="Block information and chain analysis tools",
            icon="🧱", 
            tags=["blocks", "chain", "height"]
        ))
        
        self.add_category(ToolCategory(
            name="consensus",
            description="Consensus and validation information",
            icon="⚖️",
            tags=["consensus", "difficulty", "space"]
        ))
        
        self.add_category(ToolCategory(
            name="mempool",
            description="Mempool monitoring and transaction analysis",
            icon="🔄",
            tags=["mempool", "pending", "fees"]
        ))
    
    def _register_tools(self) -> None:
        """Register blockchain analysis tools."""
        
        # Network tools
        self.add_tool(MCPTool(
            name="status",
            description="Get comprehensive blockchain synchronization and network status",
            input_schema={
                "type": "object",
                "properties": {
                    "include_connections": {
                        "type": "boolean",
                        "description": "Include peer connection information",
                        "default": False
                    },
                    "include_mempool": {
                        "type": "boolean", 
                        "description": "Include mempool statistics",
                        "default": True
                    }
                },
                "examples": [
                    {"include_connections": True, "include_mempool": True}
                ]
            }
        ))
        
        self.add_tool(MCPTool(
            name="peers",
            description="Get information about connected peers and network topology",
            input_schema={
                "type": "object",
                "properties": {
                    "include_banned": {
                        "type": "boolean",
                        "description": "Include banned peer information",
                        "default": False
                    }
                }
            }
        ))
        
        # Block tools
        self.add_tool(MCPTool(
            name="block_by_height",
            description="Get detailed block information by height",
            input_schema={
                "type": "object",
                "properties": {
                    "height": {
                        "type": "integer",
                        "description": "Block height to retrieve",
                        "minimum": 0
                    },
                    "include_transactions": {
                        "type": "boolean",
                        "description": "Include transaction details in block",
                        "default": True
                    }
                },
                "required": ["height"],
                "examples": [
                    {"height": 4123456, "include_transactions": False}
                ]
            }
        ))
        
        self.add_tool(MCPTool(
            name="block_by_hash",
            description="Get detailed block information by header hash",
            input_schema={
                "type": "object", 
                "properties": {
                    "header_hash": {
                        "type": "string",
                        "description": "Block header hash (hex string)",
                        "pattern": "^0x[a-fA-F0-9]{64}$"
                    },
                    "include_transactions": {
                        "type": "boolean",
                        "description": "Include transaction details in block",
                        "default": True
                    }
                },
                "required": ["header_hash"],
                "examples": [
                    {"header_hash": "0x1a2b3c4d5e6f..."}
                ]
            }
        ))
        
        self.add_tool(MCPTool(
            name="block_range",
            description="Get information about a range of blocks",
            input_schema={
                "type": "object",
                "properties": {
                    "start_height": {
                        "type": "integer",
                        "description": "Starting block height",
                        "minimum": 0
                    },
                    "end_height": {
                        "type": "integer", 
                        "description": "Ending block height",
                        "minimum": 0
                    },
                    "include_transactions": {
                        "type": "boolean",
                        "description": "Include transaction details",
                        "default": False
                    }
                },
                "required": ["start_height", "end_height"],
                "examples": [
                    {"start_height": 4123400, "end_height": 4123410}
                ]
            }
        ))
        
        # Consensus tools
        self.add_tool(MCPTool(
            name="network_space",
            description="Get current network space and farming statistics",
            input_schema={
                "type": "object",
                "properties": {
                    "include_historical": {
                        "type": "boolean",
                        "description": "Include historical space data",
                        "default": False
                    },
                    "days_back": {
                        "type": "integer",
                        "description": "Days of historical data to include",
                        "default": 7,
                        "minimum": 1,
                        "maximum": 365
                    }
                }
            }
        ))
        
        self.add_tool(MCPTool(
            name="difficulty",
            description="Get current difficulty and adjustment information",
            input_schema={
                "type": "object",
                "properties": {
                    "include_history": {
                        "type": "boolean",
                        "description": "Include difficulty adjustment history",
                        "default": False
                    }
                }
            }
        ))
        
        # Mempool tools
        self.add_tool(MCPTool(
            name="mempool_info",
            description="Get comprehensive mempool statistics and fee information",
            input_schema={
                "type": "object",
                "properties": {
                    "include_transactions": {
                        "type": "boolean",
                        "description": "Include sample transactions from mempool",
                        "default": False
                    },
                    "fee_targets": {
                        "type": "array",
                        "description": "Target confirmation times for fee estimation",
                        "items": {"type": "integer"},
                        "default": [1, 3, 6, 12, 24]
                    }
                }
            }
        ))
        
        self.add_tool(MCPTool(
            name="fee_estimate",
            description="Estimate fees for different transaction priorities",
            input_schema={
                "type": "object",
                "properties": {
                    "cost": {
                        "type": "integer",
                        "description": "Transaction cost in compute units",
                        "default": 11000000
                    },
                    "target_minutes": {
                        "type": "integer",
                        "description": "Target confirmation time in minutes",
                        "default": 10,
                        "minimum": 1
                    }
                }
            }
        ))
    
    def _register_resources(self) -> None:
        """Register blockchain resources."""
        
        # Real-time status resources
        self.add_resource(MCPResource(
            uri="chia://blockchain/status",
            name="Blockchain Status",
            description="Real-time blockchain synchronization and network status",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://blockchain/peak",
            name="Current Peak Block",
            description="Information about the current peak block",
            mime_type="application/json"
        ))
        
        # Network resources
        self.add_resource(MCPResource(
            uri="chia://blockchain/network/space",
            name="Network Space",
            description="Current total network farming space",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://blockchain/network/difficulty",
            name="Network Difficulty", 
            description="Current network difficulty and adjustment info",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://blockchain/network/peers",
            name="Network Peers",
            description="Information about connected peers",
            mime_type="application/json"
        ))
        
        # Mempool resources
        self.add_resource(MCPResource(
            uri="chia://blockchain/mempool/status",
            name="Mempool Status",
            description="Current mempool size and fee statistics",
            mime_type="application/json"
        ))
        
        self.add_resource(MCPResource(
            uri="chia://blockchain/mempool/fees",
            name="Fee Estimates",
            description="Current fee estimates for different priorities",
            mime_type="application/json"
        ))
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a blockchain tool."""
        if not self.rpc_client:
            raise Exception("RPC client not initialized")
        
        if tool_name == "status":
            return await self._get_blockchain_status(arguments)
        elif tool_name == "peers":
            return await self._get_peer_info(arguments)
        elif tool_name == "block_by_height":
            return await self._get_block_by_height(arguments)
        elif tool_name == "block_by_hash":
            return await self._get_block_by_hash(arguments)
        elif tool_name == "block_range":
            return await self._get_block_range(arguments)
        elif tool_name == "network_space":
            return await self._get_network_space(arguments)
        elif tool_name == "difficulty":
            return await self._get_difficulty_info(arguments)
        elif tool_name == "mempool_info":
            return await self._get_mempool_info(arguments)
        elif tool_name == "fee_estimate":
            return await self._estimate_fees(arguments)
        else:
            raise ValueError(f"Unknown blockchain tool: {tool_name}")
    
    async def read_resource(self, uri: str) -> Any:
        """Read a blockchain resource."""
        if not self.rpc_client:
            raise Exception("RPC client not initialized")
        
        if uri == "chia://blockchain/status":
            return await self._get_blockchain_status({})
        elif uri == "chia://blockchain/peak":
            return await self._get_peak_block()
        elif uri == "chia://blockchain/network/space":
            return await self._get_network_space({})
        elif uri == "chia://blockchain/network/difficulty":
            return await self._get_difficulty_info({})
        elif uri == "chia://blockchain/network/peers":
            return await self._get_peer_info({})
        elif uri == "chia://blockchain/mempool/status":
            return await self._get_mempool_info({})
        elif uri == "chia://blockchain/mempool/fees":
            return await self._estimate_fees({})
        else:
            raise ValueError(f"Unknown blockchain resource: {uri}")
    
    async def _get_blockchain_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive blockchain status."""
        include_connections = args.get("include_connections", False)
        include_mempool = args.get("include_mempool", True)
        
        # Get basic blockchain state
        state_response = await self.rpc_client.fetch("get_blockchain_state", {})
        
        result = {
            "blockchain_state": state_response.get("blockchain_state", {}),
            "timestamp": self._get_current_timestamp()
        }
        
        if include_connections:
            connections = await self.rpc_client.fetch("get_connections", {})
            result["connections"] = connections.get("connections", [])
        
        if include_mempool:
            mempool = await self.rpc_client.fetch("get_all_mempool_items", {})
            result["mempool_stats"] = {
                "size": len(mempool.get("mempool_items", {})),
                "total_cost": sum(item.get("cost", 0) for item in mempool.get("mempool_items", {}).values())
            }
        
        return result
    
    async def _get_peer_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get peer connection information."""
        include_banned = args.get("include_banned", False)
        
        connections = await self.rpc_client.fetch("get_connections", {})
        
        result = {
            "connections": connections.get("connections", []),
            "connection_count": len(connections.get("connections", [])),
            "timestamp": self._get_current_timestamp()
        }
        
        if include_banned:
            # Note: This would require additional RPC call if available
            result["banned_peers"] = []
        
        return result
    
    async def _get_block_by_height(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get block by height."""
        height = args["height"]
        include_tx = args.get("include_transactions", True)
        
        block_response = await self.rpc_client.fetch("get_block_record_by_height", {"height": height})
        
        result = {
            "height": height,
            "block_record": block_response.get("block_record", {}),
            "timestamp": self._get_current_timestamp()
        }
        
        if include_tx and "header_hash" in block_response.get("block_record", {}):
            header_hash = block_response["block_record"]["header_hash"]
            full_block = await self.rpc_client.fetch("get_block", {"header_hash": header_hash})
            result["full_block"] = full_block.get("block", {})
        
        return result
    
    async def _get_block_by_hash(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get block by header hash."""
        header_hash = args["header_hash"]
        include_tx = args.get("include_transactions", True)
        
        block_response = await self.rpc_client.fetch("get_block", {"header_hash": header_hash})
        
        result = {
            "header_hash": header_hash,
            "block": block_response.get("block", {}),
            "timestamp": self._get_current_timestamp()
        }
        
        if not include_tx:
            # Remove transaction details to reduce payload
            if "transactions_generator" in result["block"]:
                result["block"]["transactions_generator"] = "[TRANSACTIONS_REMOVED]"
        
        return result
    
    async def _get_block_range(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get range of blocks."""
        start_height = args["start_height"]
        end_height = args["end_height"]
        include_tx = args.get("include_transactions", False)
        
        if end_height - start_height > 100:
            raise ValueError("Block range too large (max 100 blocks)")
        
        blocks = []
        for height in range(start_height, end_height + 1):
            try:
                block_data = await self._get_block_by_height({
                    "height": height,
                    "include_transactions": include_tx
                })
                blocks.append(block_data)
            except Exception as e:
                logger.warning(f"Failed to get block at height {height}: {e}")
        
        return {
            "start_height": start_height,
            "end_height": end_height,
            "blocks": blocks,
            "block_count": len(blocks),
            "timestamp": self._get_current_timestamp()
        }
    
    async def _get_network_space(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get network space information."""
        include_historical = args.get("include_historical", False)
        days_back = args.get("days_back", 7)
        
        state_response = await self.rpc_client.fetch("get_blockchain_state", {})
        blockchain_state = state_response.get("blockchain_state", {})
        
        result = {
            "current_space": blockchain_state.get("space", 0),
            "space_formatted": self._format_space(blockchain_state.get("space", 0)),
            "timestamp": self._get_current_timestamp()
        }
        
        if include_historical:
            # Note: This would require additional implementation for historical data
            result["historical_data"] = f"Historical data for last {days_back} days (not implemented)"
        
        return result
    
    async def _get_difficulty_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get difficulty information."""
        include_history = args.get("include_history", False)
        
        state_response = await self.rpc_client.fetch("get_blockchain_state", {})
        blockchain_state = state_response.get("blockchain_state", {})
        
        result = {
            "difficulty": blockchain_state.get("difficulty", 0),
            "sub_slot_iters": blockchain_state.get("sub_slot_iters", 0),
            "timestamp": self._get_current_timestamp()
        }
        
        if include_history:
            # Note: This would require additional implementation for historical data
            result["adjustment_history"] = "Difficulty adjustment history (not implemented)"
        
        return result
    
    async def _get_mempool_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get mempool information."""
        include_transactions = args.get("include_transactions", False)
        fee_targets = args.get("fee_targets", [1, 3, 6, 12, 24])
        
        mempool_response = await self.rpc_client.fetch("get_all_mempool_items", {})
        mempool_items = mempool_response.get("mempool_items", {})
        
        # Calculate mempool statistics
        total_size = len(mempool_items)
        total_cost = sum(item.get("cost", 0) for item in mempool_items.values())
        fee_rates = [item.get("fee", 0) / max(item.get("cost", 1), 1) for item in mempool_items.values()]
        
        result = {
            "size": total_size,
            "total_cost": total_cost,
            "average_fee_rate": sum(fee_rates) / max(len(fee_rates), 1),
            "fee_targets": fee_targets,
            "timestamp": self._get_current_timestamp()
        }
        
        if include_transactions:
            result["sample_transactions"] = list(mempool_items.values())[:10]  # First 10 transactions
        
        return result
    
    async def _estimate_fees(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate transaction fees."""
        cost = args.get("cost", 11000000)
        target_minutes = args.get("target_minutes", 10)
        
        # Get current mempool to estimate fees
        mempool_info = await self._get_mempool_info({})
        
        # Simple fee estimation based on average fee rate
        avg_fee_rate = mempool_info.get("average_fee_rate", 0.00001)  # fallback
        estimated_fee = max(int(cost * avg_fee_rate), 1)  # minimum 1 mojo
        
        return {
            "cost": cost,
            "target_minutes": target_minutes,
            "estimated_fee": estimated_fee,
            "fee_rate": avg_fee_rate,
            "estimates": {
                "fast": int(estimated_fee * 2),      # 2x for fast confirmation
                "normal": estimated_fee,             # normal confirmation
                "slow": max(int(estimated_fee * 0.5), 1)  # 0.5x for slow but cheap
            },
            "timestamp": self._get_current_timestamp()
        }
    
    async def _get_peak_block(self) -> Dict[str, Any]:
        """Get current peak block information."""
        state_response = await self.rpc_client.fetch("get_blockchain_state", {})
        blockchain_state = state_response.get("blockchain_state", {})
        peak = blockchain_state.get("peak", {})
        
        return {
            "peak": peak,
            "height": peak.get("height", 0),
            "timestamp": self._get_current_timestamp()
        }
    
    def _format_space(self, space_bytes: int) -> str:
        """Format space in human-readable format."""
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
        size = float(space_bytes)
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.2f} {units[unit_index]}"
    
    def _get_current_timestamp(self) -> int:
        """Get current timestamp."""
        import time
        return int(time.time())