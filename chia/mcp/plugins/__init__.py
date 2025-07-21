"""
MCP Plugin system for Chia blockchain.

This module provides a plugin-based architecture for organizing MCP tools
into hierarchical categories with better extensibility.
"""

from .base import MCPPlugin, PluginManager, ToolCategory

# Import plugins conditionally to avoid import errors during development
try:
    from .wallet import WalletPlugin
    from .blockchain import BlockchainPlugin  
    from .farming import FarmingPlugin
    
    __all__ = [
        "MCPPlugin",
        "PluginManager",
        "ToolCategory",
        "WalletPlugin", 
        "BlockchainPlugin",
        "FarmingPlugin"
    ]
except ImportError as e:
    # Allow partial imports during development
    __all__ = [
        "MCPPlugin",
        "PluginManager", 
        "ToolCategory"
    ]