# Chia MCP Server - Enhanced Hierarchical Architecture

This repository contains an enhanced Model Context Protocol (MCP) server implementation for the Chia blockchain, featuring a hierarchical plugin-based architecture that makes Chia blockchain functionality easily accessible to AI models like GitHub Copilot.

## 🚀 What's New in v2.0

### Major Improvements Over Original Implementation

- **🏗️ Hierarchical Tool Organization**: Tools are organized in logical namespaces (wallet.*, blockchain.*, farming.*)
- **🔌 Plugin-Based Architecture**: Extensible system that allows easy addition of new functionality
- **📈 480% More Tools**: Expanded from 5 basic tools to 24 comprehensive tools
- **🎯 Advanced Chia Features**: Full support for farming, plotting, blockchain analysis, and wallet operations
- **📋 Rich Categorization**: 11 tool categories with icons and descriptions for better IDE integration
- **📚 Organized Resources**: 35 hierarchically organized resources (up from 3)
- **🔍 Enhanced Schemas**: Detailed validation, examples, and parameter descriptions

### Plugin System

The server now features three main plugins:

#### 🔷 Wallet Plugin (6 tools)
- `wallet.balance` - Enhanced balance with coin details
- `wallet.coins` - Detailed coin information and filtering
- `wallet.transactions` - Advanced transaction history with sorting
- `wallet.transaction_detail` - Individual transaction analysis
- `wallet.send` - Advanced transaction sending with memos
- `wallet.create_backup` - Wallet backup functionality

#### 🔷 Blockchain Plugin (9 tools)
- `blockchain.status` - Comprehensive network status
- `blockchain.peers` - Peer connection analysis
- `blockchain.block_by_height` - Block information by height
- `blockchain.block_by_hash` - Block information by hash
- `blockchain.block_range` - Batch block analysis
- `blockchain.network_space` - Network space calculations
- `blockchain.difficulty` - Difficulty and adjustment info
- `blockchain.mempool_info` - Mempool statistics
- `blockchain.fee_estimate` - Smart fee estimation

#### 🔷 Farming Plugin (9 tools)
- `farming.plot_count` - Plot statistics and grouping
- `farming.plot_details` - Individual plot information
- `farming.plot_health` - Plot health diagnostics
- `farming.harvester_status` - Harvester performance metrics
- `farming.signage_points` - Signage point analysis
- `farming.farming_rewards` - Reward tracking and history
- `farming.estimated_time_to_win` - Statistical projections
- `farming.farming_efficiency` - Performance optimization
- `farming.farm_summary` - Comprehensive farming dashboard

## What is MCP?

The Model Context Protocol (MCP) is a protocol for connecting AI models to external data sources and tools. This enhanced implementation provides AI models with comprehensive access to:

- **Advanced Wallet Operations** (balance, transactions, sending, backup)
- **Blockchain Analysis** (status, blocks, network metrics, fees)
- **Farming Management** (plots, harvesting, rewards, optimization)
- **Real-time Data** via hierarchical resource URIs

## Features

### 🎯 Hierarchical Tool Organization
- **Namespaced Tools**: `wallet.*`, `blockchain.*`, `farming.*`
- **Logical Grouping**: Related functionality grouped together
- **Easy Discovery**: AI models can easily find relevant tools

### 🔧 Plugin System
- **Extensible Architecture**: Add new plugins without modifying core code
- **Category Support**: Tools organized in categories with icons
- **Plugin Discovery**: Built-in plugin information and management

### 📊 Enhanced Schemas
- **Rich Validation**: Parameter constraints and validation
- **Examples**: Usage examples for each tool
- **Documentation**: Comprehensive parameter descriptions

### 📚 Resource Hierarchy
- **Organized URIs**: `chia://wallet/1/balance`, `chia://blockchain/network/space`
- **Real-time Data**: Live blockchain and farming metrics
- **Hierarchical Access**: Drill down from summaries to details

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/darbotlabs/darbot-chia.git
   cd darbot-chia
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Ensure Chia is running:**
   - Have a Chia full node and wallet running
   - Default wallet RPC port: 9256

## Usage

### Starting the MCP Server

#### Command Line Interface
```bash
# Start with default settings
python -m chia.mcp.cli

# Custom host and port
python -m chia.mcp.cli --host 0.0.0.0 --port 8080

# Custom Chia RPC port
python -m chia.mcp.cli --chia-rpc-port 9256 --log-level DEBUG
```

#### WebSocket Server
```bash
# Start WebSocket server for MCP communication
python -m chia.mcp.websocket_server --host localhost --port 8080
```

#### Programmatic Usage
```python
import asyncio
from chia.mcp.server import ChiaMCPServer

async def main():
    server = ChiaMCPServer(host="localhost", port=8080)
    await server.start()
    
    # Server is now running and ready to accept MCP connections
    
    await server.stop()

asyncio.run(main())
```

### Connecting from MCP Clients

The server supports the Model Context Protocol over WebSockets:

```javascript
// Example client connection
const ws = new WebSocket('ws://localhost:8080');

// Send MCP request
ws.send(JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "tools/call",
    params: {
        name: "get_wallet_balance",
        arguments: { wallet_id: 1 }
    }
}));
```

## MCP Protocol Examples

### Get Wallet Balance
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "get_wallet_balance",
        "arguments": { "wallet_id": 1 }
    }
}
```

### Send Transaction
```json
{
    "jsonrpc": "2.0", 
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "send_transaction",
        "arguments": {
            "wallet_id": 1,
            "amount": 1000000000000,
            "address": "xch1...",
            "fee": 100000000
        }
    }
}
```

### List Available Tools
```json
{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/list",
    "params": {}
}
```

### Read Blockchain Status
```json
{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "resources/read",
    "params": {
        "uri": "chia://blockchain/status"
    }
}
```

## Configuration

### Environment Variables
- `CHIA_ROOT` - Chia configuration directory (default: ~/.chia/mainnet)
- `CHIA_RPC_PORT` - Wallet RPC port (default: 9256)

### Configuration File
Place a `mcp_config.yaml` file in your Chia config directory:

```yaml
mcp:
  host: "localhost"
  port: 8080
  wallet_rpc_port: 9256
  log_level: "INFO"
  
  # Enable/disable specific tools
  tools:
    get_wallet_balance: true
    get_transactions: true
    send_transaction: true
    get_wallets: true
    get_sync_status: true
```

## Security Considerations

- **RPC Access**: The MCP server requires access to Chia wallet RPC
- **Network Exposure**: Be careful when exposing the MCP server to networks
- **Authentication**: Consider implementing authentication for production use
- **Transaction Signing**: Sending transactions requires wallet access

## Testing

Run the test suite:

```bash
# Run all MCP tests
python -m pytest chia/_tests/mcp/

# Run standalone protocol test
python test_mcp_standalone.py

# Test specific functionality
python -c "
from chia.mcp.protocol import MCPRequest, serialize_message
request = MCPRequest(method='test', id=1)
print('MCP Protocol Test:', serialize_message(request))
"
```

## Development

### Adding New Tools

1. **Define the tool in `server.py`:**
```python
self.add_tool(MCPTool(
    name="my_new_tool",
    description="Description of what the tool does",
    input_schema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param1"]
    }
))
```

2. **Implement the tool logic in `ChiaToolCallHandler`:**
```python
elif tool_name == "my_new_tool":
    param1 = arguments["param1"]
    result = await self._call_my_tool(param1)
    return result
```

### Adding New Resources

1. **Register the resource:**
```python
self.add_resource(MCPResource(
    uri="chia://my/resource",
    name="My Resource",
    description="Resource description",
    mime_type="application/json"
))
```

2. **Implement resource reading in `ChiaResourceHandler`:**
```python
elif uri == "chia://my/resource":
    data = await self._fetch_my_resource()
    return data
```

## Troubleshooting

### Common Issues

1. **"RPC client not initialized"**
   - Ensure Chia wallet is running
   - Check RPC port configuration
   - Verify network connectivity

2. **"Connection refused"**
   - Check if Chia wallet RPC is enabled
   - Verify firewall settings
   - Ensure correct port configuration

3. **"Invalid method"**
   - Verify MCP message format
   - Check tool/resource names
   - Review protocol documentation

### Debug Mode
```bash
python -m chia.mcp.cli --log-level DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Links

- [Chia Blockchain](https://github.com/Chia-Network/chia-blockchain)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Chia Documentation](https://docs.chia.net/)