from __future__ import annotations

from typing import Any, Optional

from chia_rs.sized_bytes import bytes32
from chia_rs.sized_ints import uint64

from chia.mcp import mcp_tool
from chia.rpc.data_layer_rpc_client import DataLayerRpcClient


@mcp_tool({"request": "fee,verbose", "response": "dict"})
async def create_data_store(
    rpc: DataLayerRpcClient,
    fee: Optional[int] = None,
    verbose: bool = False,
) -> dict[str, Any]:
    fee_uint = uint64(fee) if fee is not None else None
    return await rpc.create_data_store(fee_uint, verbose)


@mcp_tool({"request": "store_id,key", "response": "dict"})
async def get_value(
    rpc: DataLayerRpcClient,
    store_id: bytes32,
    key: bytes,
) -> dict[str, Any]:
    return await rpc.get_value(store_id, key, None)
