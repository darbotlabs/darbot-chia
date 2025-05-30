from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("cat", "create_new_cat_and_wallet", schema={
    "description": "Create a new CAT (Chia Asset Token) and associated wallet",
    "parameters": {
        "amount": {
            "type": "integer",
            "description": "Initial amount of tokens to mint in mojos",
            "required": True
        },
        "fee": {
            "type": "integer",
            "description": "Transaction fee in mojos",
            "default": 0
        },
        "test": {
            "type": "boolean",
            "description": "Whether to create a test CAT",
            "default": False
        }
    },
    "returns": {"type": "object", "description": "Details of the created CAT and wallet"}
})
async def create_new_cat_and_wallet(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Create a new CAT (Chia Asset Token) and associated wallet."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        amount = params.get("amount")
        if amount is None:
            raise MCPError(1, "amount parameter is required")
        
        fee = params.get("fee", 0)
        test = params.get("test", False)
        
        # For now, avoiding chia_rs dependency
        # return await pool.wallet.create_new_cat_and_wallet(uint64(amount), uint64(fee), test)
        return {
            "message": "CAT creation not yet implemented",
            "amount": amount,
            "fee": fee,
            "test": test
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("cat", "get_cat_list", schema={
    "description": "Get list of all known CAT (Chia Asset Token) assets",
    "parameters": {},
    "returns": {"type": "object", "description": "List of CAT assets with their details"}
})
async def get_cat_list(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get list of all known CAT (Chia Asset Token) assets."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        return await pool.wallet.get_cat_list()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("cat", "get_stray_cats", schema={
    "description": "Get stray CATs that don't have associated wallets",
    "parameters": {},
    "returns": {"type": "array", "description": "List of stray CAT coins"}
})
async def get_stray_cats(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get stray CATs that don't have associated wallets."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        return await pool.wallet.get_stray_cats()
    except Exception as e:
        raise MCPError(1, str(e))
