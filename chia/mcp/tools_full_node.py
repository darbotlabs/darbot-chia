from __future__ import annotations

from typing import Any, Optional

from chia_rs import FullBlock
from chia_rs.sized_bytes import bytes32

from chia.mcp import mcp_tool
from chia.rpc.full_node_rpc_client import FullNodeRpcClient


@mcp_tool({"request": "none", "response": "dict"})
async def get_blockchain_state(rpc: FullNodeRpcClient) -> dict[str, Any]:
    return await rpc.get_blockchain_state()


@mcp_tool({"request": "header_hash", "response": "FullBlock|None"})
async def get_block(rpc: FullNodeRpcClient, header_hash: bytes32) -> Optional[FullBlock]:
    return await rpc.get_block(header_hash)
