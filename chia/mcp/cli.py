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
    
    parser = argparse.ArgumentParser(description="Chia Model Context Protocol Server")
    parser.add_argument("--host", default="localhost", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind the server to")
    parser.add_argument("--chia-rpc-port", type=int, default=9256, help="Chia wallet RPC port")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, sync_signal_handler)
    signal.signal(signal.SIGTERM, sync_signal_handler)
    
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