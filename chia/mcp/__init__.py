from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=Callable[..., Awaitable[Any]])


def mcp_tool(schema: dict[str, Any]) -> Callable[[T], T]:
    """Decorator to attach MCP metadata to a tool function."""

    def decorator(func: T) -> T:
        setattr(func, "mcp_schema", schema)
        return func

    return decorator
