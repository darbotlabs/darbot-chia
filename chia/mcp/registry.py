from __future__ import annotations

from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@dataclass
class Tool:
    group: str
    name: str
    schema: dict[str, Any]
    handler: Callable[["ClientPool", dict[str, Any]], Awaitable[Any]]


_registry: dict[tuple[str, str], Tool] = {}


def mcp_tool(
    group: str,
    name: str,
    schema: dict[str, Any],
) -> Callable[
    [Callable[["ClientPool", dict[str, Any]], Awaitable[Any]]],
    Callable[["ClientPool", dict[str, Any]], Awaitable[Any]],
]:
    """Decorator to register MCP tools with the registry."""
    def decorator(
        func: Callable[["ClientPool", dict[str, Any]], Awaitable[Any]]
    ) -> Callable[["ClientPool", dict[str, Any]], Awaitable[Any]]:
        if (group, name) in _registry:
            raise ValueError(f"duplicate MCP tool registration: {group}/{name}")
        _registry[group, name] = Tool(group, name, schema, func)
        return func

    return decorator


def get_tool(group: str, name: str) -> Tool | None:
    """Get a registered tool by group and name."""
    return _registry.get((group, name))


def schema() -> list[dict[str, Any]]:
    """Get the schema for all registered tools."""
    return [
        {"group": tool.group, "name": tool.name, "schema": tool.schema}
        for tool in _registry.values()
    ]


def get_all_tools() -> dict[tuple[str, str], Tool]:
    """Get all registered tools."""
    return _registry.copy()

