from __future__ import annotations


from typing import Any, Optional

from chia_rs.sized_ints import uint32

from chia.mcp import mcp_tool
from chia.rpc.wallet_request_types import LogIn, LogInResponse
from chia.rpc.wallet_rpc_client import WalletRpcClient


@mcp_tool({"request": "LogIn", "response": "LogInResponse"})
async def log_in(rpc: WalletRpcClient, fingerprint: int) -> LogInResponse:
    return await rpc.log_in(LogIn(uint32(fingerprint)))


@mcp_tool({"request": "wallet_id:int", "response": "WalletBalance"})
async def get_wallet_balance(rpc: WalletRpcClient, wallet_id: int) -> dict[str, Any]:
    return await rpc.get_wallet_balance(wallet_id)


@mcp_tool({"request": "wallet_type", "response": "list"})
async def get_wallets(rpc: WalletRpcClient, wallet_type: Optional[int] = None) -> list[dict[str, Any]]:
    return await rpc.get_wallets(wallet_type)

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

