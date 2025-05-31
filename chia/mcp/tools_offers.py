from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("offers", "create_offer_for_ids", schema={
    "description": "Create a new offer for trading specific asset IDs",
    "parameters": {
        "offer_dict": {
            "type": "object",
            "description": "Dictionary mapping asset IDs to amounts to offer",
            "required": True
        },
        "fee": {
            "type": "integer",
            "description": "Transaction fee in mojos",
            "default": 0
        }
    },
    "returns": {"type": "object", "description": "Created offer details and trade record"}
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
    "description": "Accept and take an existing offer",
    "parameters": {
        "offer": {
            "type": "string",
            "description": "Offer string in bech32 format",
            "required": True
        },
        "fee": {
            "type": "integer",
            "description": "Transaction fee in mojos",
            "default": 0
        }
    },
    "returns": {"type": "object", "description": "Trade record of the accepted offer"}
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
    "description": "Get all offers (both created and taken) with pagination",
    "parameters": {
        "start": {
            "type": "integer",
            "description": "Starting index for pagination",
            "default": 0
        },
        "end": {
            "type": "integer",
            "description": "Ending index for pagination",
            "default": 50
        }
    },
    "returns": {"type": "array", "description": "List of trade records"}
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
