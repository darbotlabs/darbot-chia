from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("full_node", "get_blockchain_state", schema={
    "description": "Get comprehensive blockchain state including current height, peak block, difficulty, network space, sync status, and mempool information. Essential for monitoring blockchain health and progress.",
    "parameters": {},
    "returns": {"type": "object", "description": "Detailed blockchain state with peak block, sync status, difficulty, space, and mempool data"}
})
async def get_blockchain_state(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get the current state of the blockchain."""
    try:
        if pool.full_node is None:
            raise MCPError(1, "Full node client not available")
        return await pool.full_node.get_blockchain_state()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("full_node", "get_block", schema={
    "description": "Retrieve a complete block by its header hash, including all transactions, proofs, and metadata. Useful for detailed block analysis and transaction history.",
    "parameters": {
        "header_hash": {"type": "string", "description": "64-character hex string of the block header hash", "required": True}
    },
    "returns": {"type": "object", "description": "Complete block object with header, transactions, proofs, and metadata, or null if block not found"}
})
async def get_block(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get a block by its header hash."""
    try:
        if pool.full_node is None:
            raise MCPError(1, "Full node client not available")
        header_hash = params.get("header_hash")
        if header_hash is None:
            raise MCPError(1, "header_hash parameter is required")
        
        # For now, avoiding chia_rs dependency, would need:
        # from chia_rs.sized_bytes import bytes32
        # header_hash_bytes = bytes32.fromhex(header_hash)
        # return await pool.full_node.get_block(header_hash_bytes)
        
        # Placeholder implementation
        return {"message": "Block retrieval not yet implemented", "header_hash": header_hash}
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("full_node", "get_network_info", schema={
    "description": "Get detailed network information including peer connections, network space, difficulty adjustments, and node synchronization status. Critical for network health monitoring.",
    "parameters": {},
    "returns": {"type": "object", "description": "Network status with peer count, connection details, network space estimates, and sync information"}
})
async def get_network_info(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get network information and connection status."""
    try:
        if pool.full_node is None:
            raise MCPError(1, "Full node client not available")
        return await pool.full_node.get_network_info()
    except Exception as e:
        raise MCPError(1, str(e))
