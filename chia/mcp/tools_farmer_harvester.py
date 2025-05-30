from __future__ import annotations

from typing import Any, TYPE_CHECKING

from chia.mcp.error import MCPError
from chia.mcp.registry import mcp_tool

if TYPE_CHECKING:
    from chia.mcp.client_pool import ClientPool


@mcp_tool("farmer", "get_harvesters", schema={
    "description": "Get information about all connected harvesters",
    "parameters": {},
    "returns": {"type": "object", "description": "Information about connected harvesters and their plots"}
})
async def get_harvesters(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get information about all connected harvesters."""
    try:
        if pool.farmer is None:
            raise MCPError(1, "Farmer client not available")
        return await pool.farmer.get_harvesters()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("farmer", "get_signage_points", schema={
    "description": "Get recent signage points from the farmer",
    "parameters": {},
    "returns": {"type": "array", "description": "List of recent signage points"}
})
async def get_signage_points(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get recent signage points from the farmer."""
    try:
        if pool.farmer is None:
            raise MCPError(1, "Farmer client not available")
        return await pool.farmer.get_signage_points()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("harvester", "get_plots", schema={
    "description": "Get information about all plots managed by the harvester",
    "parameters": {},
    "returns": {"type": "object", "description": "Information about plots including size and location"}
})
async def get_plots(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get information about all plots managed by the harvester."""
    try:
        if pool.harvester is None:
            raise MCPError(1, "Harvester client not available")
        return await pool.harvester.get_plots()
    except Exception as e:
        raise MCPError(1, str(e))


@mcp_tool("harvester", "get_plot_directories", schema={
    "description": "Get the directories that the harvester is monitoring for plots",
    "parameters": {},
    "returns": {"type": "array", "description": "List of plot directories being monitored"}
})
async def get_plot_directories(pool: "ClientPool", params: dict[str, Any]) -> Any:
    """Get the directories that the harvester is monitoring for plots."""
    try:
        if pool.harvester is None:
            raise MCPError(1, "Harvester client not available")
        return await pool.harvester.get_plot_directories()
    except Exception as e:
        raise MCPError(1, str(e))
