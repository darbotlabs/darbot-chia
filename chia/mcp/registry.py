from __future__ import annotations

from collections.abc import Awaitable
from dataclasses import dataclass
from typing import Any, Callable

from chia.mcp.client_pool import ClientPool


@dataclass
class Tool:
    group: str
    name: str
    schema: dict[str, Any]
    handler: Callable[[ClientPool, dict[str, Any]], Awaitable[Any]]


_registry: dict[tuple[str, str], Tool] = {}


def mcp_tool(
    group: str,
    name: str,
    schema: dict[str, Any],
) -> Callable[
    [Callable[[ClientPool, dict[str, Any]], Awaitable[Any]]],
    Callable[[ClientPool, dict[str, Any]], Awaitable[Any]],
]:
    def decorator(
        func: Callable[[ClientPool, dict[str, Any]], Awaitable[Any]]
    ) -> Callable[[ClientPool, dict[str, Any]], Awaitable[Any]]:
        _registry[group, name] = Tool(group, name, schema, func)
        return func

    return decorator


def get_tool(group: str, name: str) -> Tool | None:
    return _registry.get((group, name))


def schema() -> list[dict[str, Any]]:
    return [
        {"group": tool.group, "name": tool.name, "schema": tool.schema}
        for tool in _registry.values()
    ]
