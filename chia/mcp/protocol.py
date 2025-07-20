"""
MCP Protocol definitions and types for Chia blockchain integration.

Defines the Model Context Protocol structures for communicating with AI models
and providing access to Chia blockchain functionality.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Union, Literal
from abc import ABC, abstractmethod


@dataclass
class MCPMessage:
    """Base class for all MCP messages."""
    jsonrpc: str = "2.0"


@dataclass 
class MCPRequest(MCPMessage):
    """MCP request message."""
    method: str = ""
    id: Optional[Union[str, int]] = None
    params: Optional[Dict[str, Any]] = None


@dataclass
class MCPResponse(MCPMessage):
    """MCP response message."""
    id: Optional[Union[str, int]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass
class MCPNotification(MCPMessage):
    """MCP notification message (no response expected)."""
    method: str = ""
    params: Optional[Dict[str, Any]] = None


@dataclass
class MCPError:
    """MCP error details."""
    code: int
    message: str
    data: Optional[Any] = None


@dataclass
class MCPTool:
    """Defines a tool that can be called via MCP."""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class MCPResource:
    """Defines a resource that can be accessed via MCP."""
    uri: str
    name: str
    description: Optional[str] = None
    mime_type: Optional[str] = None


@dataclass
class ChiaWalletInfo:
    """Information about a Chia wallet."""
    id: int
    name: str
    type: int
    data: str


@dataclass
class ChiaTransactionRecord:
    """Information about a Chia transaction."""
    confirmed_at_height: int
    created_at_time: int
    to_puzzle_hash: str
    amount: int
    fee_amount: int
    confirmed: bool
    sent: int
    spend_bundle: Optional[Dict[str, Any]] = None
    additions: List[Dict[str, Any]] = None
    removals: List[Dict[str, Any]] = None
    wallet_id: int = 1
    sent_to: List[str] = None
    trade_id: Optional[str] = None
    type: int = 1
    name: str = ""
    memos: Dict[str, Any] = None


class MCPHandler(ABC):
    """Abstract base class for MCP message handlers."""
    
    @abstractmethod
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle an MCP request and return a response."""
        pass
    
    @abstractmethod
    async def handle_notification(self, notification: MCPNotification) -> None:
        """Handle an MCP notification."""
        pass


def serialize_message(message: Union[MCPRequest, MCPResponse, MCPNotification]) -> str:
    """Serialize an MCP message to JSON string."""
    return json.dumps(asdict(message))


def deserialize_message(data: str) -> Union[MCPRequest, MCPResponse, MCPNotification]:
    """Deserialize a JSON string to an MCP message."""
    parsed = json.loads(data)
    
    if "method" in parsed:
        if "id" in parsed:
            return MCPRequest(**parsed)
        else:
            return MCPNotification(**parsed)
    else:
        return MCPResponse(**parsed)