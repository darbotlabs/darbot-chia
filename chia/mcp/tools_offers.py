from __future__ import annotations

from typing import Any

from chia.mcp import mcp_tool
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.wallet.trade_record import TradeRecord
from chia.wallet.trading.offer import Offer
from chia.wallet.util.tx_config import TXConfig


@mcp_tool({"request": "offer_dict,fee", "response": "CreateOfferForIDsResponse"})
async def create_offer_for_ids(
    rpc: WalletRpcClient,
    offer_dict: dict[str, int],
    fee: int = 0,
) -> Any:
    return await rpc.create_offer_for_ids(offer_dict, TXConfig(), fee=fee)


@mcp_tool({"request": "offer,fee", "response": "TakeOfferResponse"})
async def take_offer(rpc: WalletRpcClient, offer: Offer, fee: int = 0) -> Any:
    return await rpc.take_offer(offer, TXConfig(), fee=fee)


@mcp_tool({"request": "start,end", "response": "list[TradeRecord]"})
async def get_all_offers(
    rpc: WalletRpcClient,
    start: int = 0,
    end: int = 50,
) -> list[TradeRecord]:
    return await rpc.get_all_offers(start=start, end=end)
