from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("data_layer", "create_data_store", schema={
    "description": "Create a new data store on the Chia data layer",
    "parameters": {
        "fee": {
            "type": "integer",
            "description": "Transaction fee in mojos",
            "required": False
        },
        "verbose": {
            "type": "boolean",
            "description": "Return verbose output",
            "default": False
        }
    },
    "returns": {"type": "object", "description": "Details of the created data store"}
})
async def create_data_store(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Create a new data store on the Chia data layer."""
    try:
        if pool.data_layer is None:
            raise MCPError(1, "Data layer client not available")
        
        fee = params.get("fee")
        verbose = params.get("verbose", False)
        
        # For now, avoiding chia_rs dependency
        # fee_uint = uint64(fee) if fee is not None else None
        # return await pool.data_layer.create_data_store(fee_uint, verbose)
        return {
            "message": "Data store creation not yet implemented",
            "fee": fee,
            "verbose": verbose
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("data_layer", "get_value", schema={
    "description": "Get a value from a data store by key",
    "parameters": {
        "store_id": {
            "type": "string",
            "description": "Data store ID in hex format",
            "required": True
        },
        "key": {
            "type": "string",
            "description": "Key to look up (hex encoded)",
            "required": True
        }
    },
    "returns": {"type": "object", "description": "Value associated with the key"}
})
async def get_value(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get a value from a data store by key."""
    try:
        if pool.data_layer is None:
            raise MCPError(1, "Data layer client not available")
        
        store_id = params.get("store_id")
        key = params.get("key")
        
        if store_id is None:
            raise MCPError(1, "store_id parameter is required")
        if key is None:
            raise MCPError(1, "key parameter is required")
        
        # For now, avoiding chia_rs dependency
        # store_id_bytes = bytes32.fromhex(store_id)
        # key_bytes = bytes.fromhex(key)
        # return await pool.data_layer.get_value(store_id_bytes, key_bytes, None)
        return {
            "message": "Data layer get_value not yet implemented",
            "store_id": store_id,
            "key": key
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("data_layer", "get_owned_stores", schema={
    "description": "Get all data stores owned by this node",
    "parameters": {},
    "returns": {"type": "array", "description": "List of owned data store IDs"}
})
async def get_owned_stores(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get all data stores owned by this node."""
    try:
        if pool.data_layer is None:
            raise MCPError(1, "Data layer client not available")
        
        return await pool.data_layer.get_owned_stores()
    except Exception as e:
        raise MCPError(1, str(e))
