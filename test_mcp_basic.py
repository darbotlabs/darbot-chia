#!/usr/bin/env python3
"""Basic test for MCP registry functionality without chia_rs dependencies."""

import sys
import os

# Add the project path
sys.path.insert(0, os.path.dirname(__file__))

# Test basic registry functionality
from chia.mcp.registry import mcp_tool, get_tool, schema, get_all_tools
from chia.mcp.error import MCPError

print("Testing MCP Registry...")

# Test decorator registration
@mcp_tool("test", "simple_tool", schema={"description": "A simple test tool"})
async def simple_tool(pool, params):
    return {"message": "success", "params": params}

# Check registration
tool = get_tool("test", "simple_tool")
assert tool is not None, "Tool should be registered"
assert tool.group == "test", "Tool group should be 'test'"
assert tool.name == "simple_tool", "Tool name should be 'simple_tool'"

# Check schema
all_schemas = schema()
assert len(all_schemas) > 0, "Should have at least one tool"
test_schema = next((s for s in all_schemas if s["group"] == "test" and s["name"] == "simple_tool"), None)
assert test_schema is not None, "Test tool should be in schema"

print("✓ Registry functionality works")

# Test duplicate registration protection
try:
    @mcp_tool("test", "simple_tool", schema={"description": "Duplicate"})
    async def duplicate_tool(pool, params):
        return {}
    assert False, "Should have raised ValueError for duplicate registration"
except ValueError as e:
    assert "duplicate MCP tool registration" in str(e)
    print("✓ Duplicate registration protection works")

# Test importing wallet tools
print("Testing wallet tools import...")
try:
    import chia.mcp.tools_wallet
    wallet_schemas = [s for s in schema() if s["group"] == "wallet"]
    print(f"✓ Imported {len(wallet_schemas)} wallet tools:")
    for s in wallet_schemas:
        print(f"  - {s['name']}: {s['schema'].get('description', 'No description')}")
except Exception as e:
    print(f"Failed to import wallet tools: {e}")

print("All basic tests passed!")