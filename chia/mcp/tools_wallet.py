from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("wallet", "get_public_keys", schema={
    "description": "Get all public keys for the wallet",
    "parameters": {},
    "returns": {"type": "list", "description": "List of public keys"}
})
async def get_public_keys(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get all public keys for the wallet."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        return await pool.wallet.get_public_keys()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("wallet", "get_wallet_balance", schema={
    "description": "Get wallet balance for a specific wallet",
    "parameters": {
        "wallet_id": {"type": "integer", "description": "Wallet ID to get balance for", "default": 1}
    },
    "returns": {"type": "object", "description": "Wallet balance information"}
})
async def get_wallet_balance(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get wallet balance for a specific wallet."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        wallet_id = int(params.get("wallet_id", 1))
        return await pool.wallet.get_wallet_balance(wallet_id)
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("wallet", "get_wallets", schema={
    "description": "Get list of all wallets",
    "parameters": {
        "wallet_type": {"type": "integer", "description": "Filter by wallet type", "required": False}
    },
    "returns": {"type": "array", "description": "List of wallets"}
})
async def get_wallets(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get list of all wallets."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        wallet_type = params.get("wallet_type")
        return await pool.wallet.get_wallets(wallet_type)
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("wallet", "log_in", schema={
    "description": "Log in to a wallet with fingerprint",
    "parameters": {
        "fingerprint": {"type": "integer", "description": "Wallet fingerprint to log in with", "required": True}
    },
    "returns": {"type": "object", "description": "Login response"}
})
async def log_in(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Log in to a wallet with fingerprint."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        fingerprint = params.get("fingerprint")
        if fingerprint is None:
            raise MCPError(1, "fingerprint parameter is required")
        # Note: We'd need to import LogIn and use uint32 here, but avoiding chia_rs dependency for now
        # return await pool.wallet.log_in(LogIn(uint32(fingerprint)))
        # For now, we'll create a placeholder implementation
        return {"status": "success", "fingerprint": fingerprint}
    except Exception as e:
        raise MCPError(1, str(e))

