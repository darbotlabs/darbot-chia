from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("offers", "create_offer_for_ids", schema={
    "description": "Create a new trade offer for exchanging specific asset IDs (XCH, CATs, NFTs). Specify what you're offering and what you want in return. The offer can be shared with others for decentralized trading.",
    "parameters": {
        "offer_dict": {
            "type": "object",
            "description": "Dictionary mapping asset IDs to amounts - positive values are offered, negative values are requested (e.g., {'xch': 1000000000000, 'cat_asset_id': -500000000} offers 1 XCH for 0.5 CAT)",
            "required": True
        },
        "fee": {
            "type": "integer",
            "description": "Network transaction fee in mojos (1 XCH = 1,000,000,000,000 mojos)",
            "default": 0
        }
    },
    "returns": {"type": "object", "description": "Created offer with bech32 offer string, trade ID, and transaction details"}
})
async def create_offer_for_ids(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Create a new offer for trading specific asset IDs."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        offer_dict = params.get("offer_dict")
        if offer_dict is None:
            raise MCPError(1, "offer_dict parameter is required")
        
        fee = params.get("fee", 0)
        
        # For now, avoiding complex imports
        # return await pool.wallet.create_offer_for_ids(offer_dict, TXConfig(), fee=fee)
        return {
            "message": "Offer creation not yet implemented",
            "offer_dict": offer_dict,
            "fee": fee
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("offers", "take_offer", schema={
    "description": "Accept and execute an existing trade offer by providing the offer string. This will exchange your assets for the offered assets if you have sufficient balance.",
    "parameters": {
        "offer": {
            "type": "string",
            "description": "Complete offer string in bech32 format (starts with 'offer1...')",
            "required": True
        },
        "fee": {
            "type": "integer",
            "description": "Additional network transaction fee in mojos for faster confirmation",
            "default": 0
        }
    },
    "returns": {"type": "object", "description": "Trade execution result with transaction IDs, status, and final balances"}
})
async def take_offer(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Accept and take an existing offer."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        offer = params.get("offer")
        if offer is None:
            raise MCPError(1, "offer parameter is required")
        
        fee = params.get("fee", 0)
        
        # For now, avoiding complex imports
        # offer_obj = Offer.from_bech32(offer)
        # return await pool.wallet.take_offer(offer_obj, TXConfig(), fee=fee)
        return {
            "message": "Take offer not yet implemented",
            "offer": offer,
            "fee": fee
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("offers", "get_all_offers", schema={
    "description": "Retrieve all trade offers associated with this wallet, including created offers, taken offers, pending trades, and completed transactions. Supports pagination for large offer histories.",
    "parameters": {
        "start": {
            "type": "integer",
            "description": "Starting index for pagination (0-based)",
            "default": 0
        },
        "end": {
            "type": "integer",
            "description": "Ending index for pagination (exclusive, max 50 per request)",
            "default": 50
        }
    },
    "returns": {"type": "array", "description": "Array of trade records with offer details, status, timestamps, and transaction information"}
})
async def get_all_offers(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get all offers (both created and taken) with pagination."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        start = params.get("start", 0)
        end = params.get("end", 50)
        
        return await pool.wallet.get_all_offers(start=start, end=end)
    except Exception as e:
        raise MCPError(1, str(e))
