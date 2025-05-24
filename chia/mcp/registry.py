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
        return func

    return decorator


def get_registry() -> Mapping[str, Mapping[str, Tool]]:
    return registry


def add_schema_endpoint(app: FastAPI) -> None:
    """Expose registered tool schemas via FastAPI."""

    @app.get("/mcp/schema.json")
    async def schema_endpoint() -> Mapping[str, Mapping[str, dict[str, Any]]]:
        return {group: {name: info.schema for name, info in tools.items()} for group, tools in registry.items()}
