from __future__ import annotations


from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI


@dataclass(frozen=True)
class Tool:
    func: Callable[..., Any]
    schema: dict[str, Any]


# Registry data structure: group -> tool name -> Tool
registry: MutableMapping[str, MutableMapping[str, Tool]] = {}


def mcp_tool(group: str, name: str, schema: dict[str, Any]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator registering callables for MCP."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        group_map = registry.setdefault(group, {})
        if name in group_map:
            raise ValueError(f"duplicate MCP tool registration: {group}/{name}")
        group_map[name] = Tool(func=func, schema=schema)

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



def get_registry() -> Mapping[str, Mapping[str, Tool]]:
    return registry


def add_schema_endpoint(app: FastAPI) -> None:
    """Expose registered tool schemas via FastAPI."""

    @app.get("/mcp/schema.json")
    async def schema_endpoint() -> Mapping[str, Mapping[str, dict[str, Any]]]:
        return {group: {name: info.schema for name, info in tools.items()} for group, tools in registry.items()}
=======
def get_tool(group: str, name: str) -> Tool | None:
    return _registry.get((group, name))


def schema() -> list[dict[str, Any]]:
    return [
        {"group": tool.group, "name": tool.name, "schema": tool.schema}
        for tool in _registry.values()
    ]

