#!/usr/bin/env python3
"""
Command-line interface for the Chia MCP Server.

This script provides a command-line interface to start and manage the
Chia Model Context Protocol server.
"""

import asyncio
import argparse
import logging
import signal
import sys
from pathlib import Path
from typing import Optional

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from chia.mcp.server import ChiaMCPServer


# Global server instance for cleanup
server_instance: Optional[ChiaMCPServer] = None


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


async def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logging.info(f"Received signal {signum}, shutting down...")
    if server_instance:
        await server_instance.stop()
    sys.exit(0)


async def main():
    """Main entry point for the Chia MCP server CLI."""
    global server_instance
    
    parser = argparse.ArgumentParser(description="Chia Model Context Protocol Server with Hierarchical Plugin System")
    parser.add_argument("--host", default="localhost", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind the server to")
    parser.add_argument("--chia-rpc-port", type=int, default=9256, help="Chia wallet RPC port")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       help="Logging level")
    parser.add_argument("--list-tools", action="store_true", help="List all available tools and exit")
    parser.add_argument("--list-plugins", action="store_true", help="List all plugins and exit")
    parser.add_argument("--demo", action="store_true", help="Show demo of hierarchical tools")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Create server instance for tool listing (doesn't require RPC connection)
    if args.list_tools or args.list_plugins or args.demo:
        server_instance = ChiaMCPServer(
            host=args.host, 
            port=args.port, 
            chia_rpc_port=args.chia_rpc_port
        )
        
        if args.list_plugins:
            await show_plugins_info(server_instance)
            return
        elif args.list_tools:
            await show_tools_info(server_instance)
            return
        elif args.demo:
            await show_demo(server_instance)
            return
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, sync_signal_handler)
    signal.signal(signal.SIGTERM, sync_signal_handler)

def sync_signal_handler(signum, frame):
    """Synchronous signal handler that wraps the async signal handler."""
    asyncio.run(signal_handler(signum, frame))


async def show_plugins_info(server: ChiaMCPServer) -> None:
    """Display information about all available plugins."""
    print("🔌 Chia MCP Server - Plugin Information")
    print("=" * 50)
    
    plugin_info = server.plugin_manager.get_plugin_info()
    
    print(f"Total Plugins: {len(plugin_info)}")
    print()
    
    for info in plugin_info:
        print(f"📦 {info['name'].upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Tools: {info['tools_count']}")
        print(f"   Resources: {info['resources_count']}")
        if info['categories']:
            print(f"   Categories: {', '.join(info['categories'])}")
        print()


async def show_tools_info(server: ChiaMCPServer) -> None:
    """Display information about all available tools."""
    print("🛠️  Chia MCP Server - Hierarchical Tools")
    print("=" * 50)
    
    all_tools = server.plugin_manager.get_all_tools()
    print(f"Total Tools: {len(all_tools)}")
    print()
    
    # Group tools by plugin
    tools_by_plugin = {}
    for tool_name, tool in all_tools.items():
        plugin_name = tool_name.split('.')[0] if '.' in tool_name else 'core'
        if plugin_name not in tools_by_plugin:
            tools_by_plugin[plugin_name] = []
        tools_by_plugin[plugin_name].append((tool_name, tool))
    
    for plugin_name, tools in tools_by_plugin.items():
        print(f"📂 {plugin_name.upper()} ({len(tools)} tools)")
        for tool_name, tool in sorted(tools):
            print(f"   • {tool_name}")
            print(f"     {tool.description}")
        print()


async def show_demo(server: ChiaMCPServer) -> None:
    """Show a demo of the hierarchical tool system."""
    print("🚀 Chia MCP Server - Hierarchical Tools Demo")
    print("=" * 60)
    
    print("This enhanced MCP server provides a hierarchical plugin-based architecture")
    print("for exposing Chia blockchain functionality to AI models like GitHub Copilot.")
    print()
    
    # Show plugin overview
    plugin_info = server.plugin_manager.get_plugin_info()
    all_tools = server.plugin_manager.get_all_tools()
    categories = server.plugin_manager.get_all_categories()
    
    print(f"📊 OVERVIEW:")
    print(f"   • {len(plugin_info)} plugins loaded")
    print(f"   • {len(all_tools)} tools available")
    print(f"   • {len(categories)} tool categories")
    print()
    
    # Show hierarchical organization
    print("🏗️  HIERARCHICAL ORGANIZATION:")
    for info in plugin_info:
        print(f"   {info['name']}: {info['tools_count']} tools, {info['resources_count']} resources")
    print()
    
    # Show sample tools from each category
    print("🛠️  SAMPLE TOOLS BY CATEGORY:")
    tools_by_plugin = {}
    for tool_name, tool in all_tools.items():
        plugin_name = tool_name.split('.')[0] if '.' in tool_name else 'core'
        if plugin_name not in tools_by_plugin:
            tools_by_plugin[plugin_name] = []
        tools_by_plugin[plugin_name].append(tool_name)
    
    for plugin_name, tool_names in tools_by_plugin.items():
        print(f"   💎 {plugin_name}.*")
        for tool_name in sorted(tool_names)[:3]:  # Show first 3
            print(f"      - {tool_name}")
        if len(tool_names) > 3:
            print(f"      - ... and {len(tool_names) - 3} more")
        print()
    
    # Show categories with icons
    print("📋 TOOL CATEGORIES:")
    for cat_name, category in list(categories.items())[:8]:  # Show first 8
        icon = category.icon or "📁"
        print(f"   {icon} {cat_name}: {category.description}")
    print()
    
    # Show connection info
    print("🔗 CONNECTION:")
    print(f"   WebSocket: ws://{server.host}:{server.port}")
    print(f"   Protocol: MCP 2024-11-05")
    print(f"   Features: Hierarchical tools, Plugin system, Categories")
    print()
    
    print("💡 USAGE EXAMPLES:")
    print("   # Get wallet balance")
    print('   {"method": "tools/call", "params": {"name": "wallet.balance", "arguments": {"wallet_id": 1}}}')
    print()
    print("   # Check farming status")
    print('   {"method": "tools/call", "params": {"name": "farming.plot_count", "arguments": {}}}')
    print()
    print("   # Get blockchain info")
    print('   {"method": "tools/call", "params": {"name": "blockchain.status", "arguments": {}}}')
    print()
    
    print("🎯 FOR GITHUB COPILOT:")
    print("   This hierarchical structure makes it easy for AI models to discover")
    print("   and use Chia blockchain functionality through well-organized namespaces.")
    print("   Each tool includes comprehensive schemas for better IDE integration.")
    print()
    print("To start the server: python -m chia.mcp.cli")
    print("=" * 60)
    
    try:
        # Create and start the MCP server
        server_instance = ChiaMCPServer(
            host=args.host, 
            port=args.port, 
            chia_rpc_port=args.chia_rpc_port
        )
        
        logger.info("Starting Chia MCP Server...")
        await server_instance.start()
        
        # Keep the server running
        logger.info("Chia MCP Server is running. Press Ctrl+C to stop.")
        try:
            # Simple event loop to keep the server running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
    finally:
        if server_instance:
            await server_instance.stop()


if __name__ == "__main__":
    asyncio.run(main())