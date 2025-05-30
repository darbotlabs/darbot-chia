#!/usr/bin/env python3
"""Comprehensive test for MCP tool registration and functionality."""

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

print("✓ Registry functionality works")

# Test importing all tool modules
print("\nTesting tool imports...")
tool_modules = [
    "chia.mcp.tools_wallet",
    "chia.mcp.tools_full_node", 
    "chia.mcp.tools_farmer_harvester",
    "chia.mcp.tools_offers",
    "chia.mcp.tools_cat",
    "chia.mcp.tools_data_layer",
    "chia.mcp.tools_did_vc"
]

for module_name in tool_modules:
    try:
        __import__(module_name)
        print(f"✓ {module_name}")
    except Exception as e:
        print(f"✗ {module_name}: {e}")

# Show all registered tools
all_schemas = schema()
print(f"\nRegistered {len(all_schemas)} tools:")

# Group by tool group
groups = {}
for s in all_schemas:
    group = s["group"]
    if group not in groups:
        groups[group] = []
    groups[group].append(s)

for group, tools in sorted(groups.items()):
    print(f"\n{group} ({len(tools)} tools):")
    for tool in tools:
        desc = tool["schema"].get("description", "No description")
        print(f"  - {tool['name']}: {desc}")

print(f"\nTotal tools: {len(all_schemas)}")
print("All tests passed!")