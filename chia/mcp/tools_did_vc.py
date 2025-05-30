from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("vc", "vc_mint", schema={
    "description": "Mint a new Verifiable Credential (VC)",
    "parameters": {
        "target_address": {
            "type": "string",
            "description": "Address to mint the VC to",
            "required": False
        },
        "fee": {
            "type": "integer",
            "description": "Transaction fee in mojos",
            "default": 0
        }
    },
    "returns": {"type": "object", "description": "Details of the minted VC"}
})
async def vc_mint(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Mint a new Verifiable Credential (VC)."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        target_address = params.get("target_address")
        fee = params.get("fee", 0)
        
        # For now, avoiding complex imports
        # request = VCMint(target_address=target_address, fee=fee)
        # return await pool.wallet.vc_mint(request)
        return {
            "message": "VC minting not yet implemented",
            "target_address": target_address,
            "fee": fee
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("vc", "vc_get", schema={
    "description": "Get details of a Verifiable Credential by launcher ID",
    "parameters": {
        "launcher_id": {
            "type": "string",
            "description": "Launcher ID of the VC in hex format",
            "required": True
        }
    },
    "returns": {"type": "object", "description": "VC details and data"}
})
async def vc_get(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get details of a Verifiable Credential by launcher ID."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        launcher_id = params.get("launcher_id")
        if launcher_id is None:
            raise MCPError(1, "launcher_id parameter is required")
        
        # For now, avoiding complex imports
        # request = VCGet(launcher_id=launcher_id)
        # return await pool.wallet.vc_get(request)
        return {
            "message": "VC get not yet implemented",
            "launcher_id": launcher_id
        }
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("did", "create_new_did_wallet", schema={
    "description": "Create a new DID (Decentralized Identifier) wallet",
    "parameters": {
        "amount": {
            "type": "integer", 
            "description": "Amount to fund the DID wallet in mojos",
            "default": 1
        },
        "fee": {
            "type": "integer",
            "description": "Transaction fee in mojos",
            "default": 0
        }
    },
    "returns": {"type": "object", "description": "Details of the created DID wallet"}
})
async def create_new_did_wallet(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Create a new DID (Decentralized Identifier) wallet."""
    try:
        if pool.wallet is None:
            raise MCPError(1, "Wallet client not available")
        
        amount = params.get("amount", 1)
        fee = params.get("fee", 0)
        
        # For now, placeholder implementation
        return {
            "message": "DID wallet creation not yet implemented",
            "amount": amount,
            "fee": fee
        }
    except Exception as e:
        raise MCPError(1, str(e))
