from __future__ import annotations

from typing import Any

from chia.mcp import mcp_tool
from chia.rpc.farmer_rpc_client import FarmerRpcClient
from chia.rpc.harvester_rpc_client import HarvesterRpcClient


@mcp_tool({"request": "none", "response": "dict"})
async def get_harvesters(rpc: FarmerRpcClient) -> dict[str, Any]:
    return await rpc.get_harvesters()


@mcp_tool({"request": "none", "response": "dict"})
async def get_plots(rpc: HarvesterRpcClient) -> dict[str, Any]:
    return await rpc.get_plots()
