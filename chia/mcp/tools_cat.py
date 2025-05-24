from __future__ import annotations

from typing import Any

from chia_rs.sized_ints import uint64

from chia.mcp import mcp_tool
from chia.rpc.wallet_request_types import GetCATListResponse
from chia.rpc.wallet_rpc_client import WalletRpcClient


@mcp_tool({"request": "amount,fee,test", "response": "dict"})
async def create_new_cat_and_wallet(
    rpc: WalletRpcClient, amount: int, fee: int = 0, test: bool = False
) -> dict[str, Any]:
    return await rpc.create_new_cat_and_wallet(uint64(amount), uint64(fee), test)


@mcp_tool({"request": "none", "response": "GetCATListResponse"})
async def get_cat_list(rpc: WalletRpcClient) -> GetCATListResponse:
    return await rpc.get_cat_list()
