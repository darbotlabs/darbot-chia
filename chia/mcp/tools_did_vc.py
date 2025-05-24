from __future__ import annotations

from chia.mcp import mcp_tool
from chia.rpc.wallet_request_types import VCGet, VCGetResponse, VCMint, VCMintResponse
from chia.rpc.wallet_rpc_client import WalletRpcClient


@mcp_tool({"request": "VCMint", "response": "VCMintResponse"})
async def vc_mint(rpc: WalletRpcClient, request: VCMint) -> VCMintResponse:
    return await rpc.vc_mint(request)


@mcp_tool({"request": "VCGet", "response": "VCGetResponse"})
async def vc_get(rpc: WalletRpcClient, request: VCGet) -> VCGetResponse:
    return await rpc.vc_get(request)
