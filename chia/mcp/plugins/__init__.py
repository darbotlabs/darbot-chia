"""
MCP Plugin system for Chia blockchain.

This module provides a plugin-based architecture for organizing MCP tools
into hierarchical categories with better extensibility.
"""
from __future__ import annotations

from .base import MCPPlugin, PluginManager, ToolCategory

# Import plugins conditionally to avoid import errors during development
try:
    from .blockchain import BlockchainPlugin
    from .farming import FarmingPlugin
    from .wallet import WalletPlugin

    __all__ = ["BlockchainPlugin", "FarmingPlugin", "MCPPlugin", "PluginManager", "ToolCategory", "WalletPlugin"]
except ImportError:
    # Allow partial imports during development
    __all__ = ["MCPPlugin", "PluginManager", "ToolCategory"]
