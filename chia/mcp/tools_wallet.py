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
