"""
Tests for the enhanced MCP plugin system.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from chia.mcp.plugins import BlockchainPlugin, FarmingPlugin, MCPPlugin, PluginManager, WalletPlugin
from chia.mcp.protocol import MCPResource, MCPTool


class TestPluginSystem:
    """Test the plugin system architecture."""

    def test_plugin_manager_initialization(self):
        """Test plugin manager can be created."""
        manager = PluginManager()
        assert len(manager.plugins) == 0
        assert isinstance(manager.plugins, dict)

    def test_plugin_registration(self):
        """Test plugin registration works correctly."""
        manager = PluginManager()
        wallet_plugin = WalletPlugin()

        manager.register_plugin(wallet_plugin)

        assert "wallet" in manager.plugins
        assert manager.plugins["wallet"] == wallet_plugin

    def test_hierarchical_tool_naming(self):
        """Test that tools are correctly namespaced by plugin."""
        manager = PluginManager()
        wallet_plugin = WalletPlugin()
        manager.register_plugin(wallet_plugin)

        tools = manager.get_all_tools()

        # Check that wallet tools are properly prefixed
        wallet_tools = [name for name in tools.keys() if name.startswith("wallet.")]
        assert len(wallet_tools) > 0
        assert "wallet.balance" in tools
        assert "wallet.transactions" in tools
        assert "wallet.send" in tools

    def test_plugin_tool_categories(self):
        """Test that plugins properly define tool categories."""
        wallet_plugin = WalletPlugin()
        categories = wallet_plugin.get_categories()

        assert len(categories) > 0
        assert "balance" in categories
        assert "transactions" in categories
        assert "operations" in categories

        # Test category structure
        balance_category = categories["balance"]
        assert balance_category.name == "balance"
        assert balance_category.description is not None
        assert balance_category.icon == "💰"

    def test_multiple_plugins(self):
        """Test that multiple plugins can be registered and work together."""
        manager = PluginManager()

        wallet_plugin = WalletPlugin()
        blockchain_plugin = BlockchainPlugin()
        farming_plugin = FarmingPlugin()

        manager.register_plugin(wallet_plugin)
        manager.register_plugin(blockchain_plugin)
        manager.register_plugin(farming_plugin)

        # Check all plugins registered
        assert len(manager.plugins) == 3
        assert "wallet" in manager.plugins
        assert "blockchain" in manager.plugins
        assert "farming" in manager.plugins

        # Check tools from all plugins
        tools = manager.get_all_tools()
        assert any(name.startswith("wallet.") for name in tools)
        assert any(name.startswith("blockchain.") for name in tools)
        assert any(name.startswith("farming.") for name in tools)

    def test_tools_by_category(self):
        """Test filtering tools by category/plugin."""
        manager = PluginManager()
        wallet_plugin = WalletPlugin()
        blockchain_plugin = BlockchainPlugin()

        manager.register_plugin(wallet_plugin)
        manager.register_plugin(blockchain_plugin)

        # Test wallet tools
        wallet_tools = manager.get_tools_by_category("wallet")
        assert all(name.startswith("wallet.") for name in wallet_tools)
        assert len(wallet_tools) > 0

        # Test blockchain tools
        blockchain_tools = manager.get_tools_by_category("blockchain")
        assert all(name.startswith("blockchain.") for name in blockchain_tools)
        assert len(blockchain_tools) > 0

    def test_plugin_resources(self):
        """Test that plugins properly define resources."""
        manager = PluginManager()
        wallet_plugin = WalletPlugin()
        manager.register_plugin(wallet_plugin)

        resources = manager.get_all_resources()

        # Check wallet resources exist
        wallet_resources = [uri for uri in resources.keys() if "wallet" in uri]
        assert len(wallet_resources) > 0
        assert "chia://wallet/summary" in resources
        assert "chia://wallet/recent_activity" in resources

    def test_plugin_info(self):
        """Test plugin information gathering."""
        manager = PluginManager()
        wallet_plugin = WalletPlugin()
        manager.register_plugin(wallet_plugin)

        plugin_info = manager.get_plugin_info()

        assert len(plugin_info) == 1
        wallet_info = plugin_info[0]

        assert wallet_info["name"] == "wallet"
        assert wallet_info["description"] == wallet_plugin.plugin_description
        assert wallet_info["tools_count"] > 0
        assert wallet_info["resources_count"] > 0

    @pytest.mark.asyncio
    async def test_tool_execution_routing(self):
        """Test that tool execution is properly routed to plugins."""
        manager = PluginManager()

        # Create mock plugin
        mock_plugin = MagicMock(spec=MCPPlugin)
        mock_plugin.plugin_name = "test"
        mock_plugin.execute_tool = AsyncMock(return_value={"result": "success"})
        mock_plugin.get_tools.return_value = {
            "test.tool": MCPTool(name="test.tool", description="Test", input_schema={})
        }
        mock_plugin.get_resources.return_value = {}
        mock_plugin.get_categories.return_value = {}

        manager.register_plugin(mock_plugin)

        # Test tool execution
        result = await manager.execute_tool("test.tool", {"arg": "value"})

        mock_plugin.execute_tool.assert_called_once_with("tool", {"arg": "value"})
        assert result == {"result": "success"}

    @pytest.mark.asyncio
    async def test_resource_reading_routing(self):
        """Test that resource reading is properly routed to plugins."""
        manager = PluginManager()

        # Create mock plugin
        mock_plugin = MagicMock(spec=MCPPlugin)
        mock_plugin.plugin_name = "test"
        mock_plugin.read_resource = AsyncMock(return_value={"data": "test"})
        mock_plugin.get_tools.return_value = {}
        mock_plugin.get_resources.return_value = {
            "test://resource": MCPResource(uri="test://resource", name="Test Resource")
        }
        mock_plugin.get_categories.return_value = {}

        manager.register_plugin(mock_plugin)

        # Test resource reading
        result = await manager.read_resource("test://resource")

        mock_plugin.read_resource.assert_called_once_with("test://resource")
        assert result == {"data": "test"}


class TestWalletPlugin:
    """Test wallet plugin specifically."""

    def test_wallet_plugin_tools(self):
        """Test wallet plugin defines expected tools."""
        plugin = WalletPlugin()
        tools = plugin.get_tools()

        expected_tools = [
            "wallet.balance",
            "wallet.coins",
            "wallet.transactions",
            "wallet.transaction_detail",
            "wallet.send",
            "wallet.create_backup",
        ]

        for tool_name in expected_tools:
            assert tool_name in tools
            tool = tools[tool_name]
            assert isinstance(tool, MCPTool)
            assert tool.description is not None
            assert tool.input_schema is not None

    def test_wallet_tool_schemas(self):
        """Test wallet tool schemas are properly defined."""
        plugin = WalletPlugin()
        tools = plugin.get_tools()

        # Test balance tool schema
        balance_tool = tools["wallet.balance"]
        schema = balance_tool.input_schema
        assert schema["type"] == "object"
        assert "wallet_id" in schema["properties"]
        assert "include_pending" in schema["properties"]
        assert "examples" in schema

    def test_wallet_resources(self):
        """Test wallet plugin defines expected resources."""
        plugin = WalletPlugin()
        resources = plugin.get_resources()

        # Should have multiple wallet balance resources
        balance_resources = [uri for uri in resources if "balance" in uri]
        assert len(balance_resources) > 0

        # Should have summary resources
        assert "chia://wallet/summary" in resources
        assert "chia://wallet/recent_activity" in resources


class TestBlockchainPlugin:
    """Test blockchain plugin specifically."""

    def test_blockchain_plugin_tools(self):
        """Test blockchain plugin defines expected tools."""
        plugin = BlockchainPlugin()
        tools = plugin.get_tools()

        expected_tools = [
            "blockchain.status",
            "blockchain.peers",
            "blockchain.block_by_height",
            "blockchain.block_by_hash",
            "blockchain.network_space",
            "blockchain.mempool_info",
        ]

        for tool_name in expected_tools:
            assert tool_name in tools

    def test_blockchain_categories(self):
        """Test blockchain plugin categories."""
        plugin = BlockchainPlugin()
        categories = plugin.get_categories()

        expected_categories = ["network", "blocks", "consensus", "mempool"]
        for cat_name in expected_categories:
            assert cat_name in categories
            category = categories[cat_name]
            assert category.description is not None
            assert category.icon is not None


class TestFarmingPlugin:
    """Test farming plugin specifically."""

    def test_farming_plugin_tools(self):
        """Test farming plugin defines expected tools."""
        plugin = FarmingPlugin()
        tools = plugin.get_tools()

        expected_tools = [
            "farming.plot_count",
            "farming.plot_details",
            "farming.harvester_status",
            "farming.farming_rewards",
            "farming.estimated_time_to_win",
            "farming.farm_summary",
        ]

        for tool_name in expected_tools:
            assert tool_name in tools

    def test_farming_advanced_schemas(self):
        """Test that farming tools have sophisticated schemas."""
        plugin = FarmingPlugin()
        tools = plugin.get_tools()

        # Test plot_details tool has advanced filtering options
        plot_details = tools["farming.plot_details"]
        schema = plot_details.input_schema
        properties = schema["properties"]

        assert "plot_id" in properties
        assert "directory" in properties
        assert "k_size" in properties
        assert "limit" in properties

        # Should have validation constraints
        assert properties["k_size"]["minimum"] == 32
        assert properties["limit"]["maximum"] == 1000


if __name__ == "__main__":
    pytest.main([__file__])
