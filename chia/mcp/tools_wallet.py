from __future__ import annotations

from typing import Any

from chia.mcp.client_pool import ClientPool
from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool


@mcp_tool("wallet", "get_public_keys", schema={})
async def get_public_keys(pool: ClientPool, params: dict[str, Any]) -> Any:
    try:
        assert pool.wallet is not None
        return await pool.wallet.get_public_keys()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("wallet", "get_wallet_balance", schema={"wallet_id": int})
async def get_wallet_balance(pool: ClientPool, params: dict[str, Any]) -> Any:
    try:
        assert pool.wallet is not None
        wallet_id = int(params.get("wallet_id", 1))
        return await pool.wallet.get_wallet_balance(wallet_id)
    except Exception as e:
        raise MCPError(1, str(e))
