# Chia MCP Server

This repository contains a Model Context Protocol (MCP) server implementation for the Chia blockchain, enabling AI models to interact with Chia blockchain data and operations.

## What is MCP?

The Model Context Protocol (MCP) is a protocol for connecting AI models to external data sources and tools. This implementation provides AI models with access to:

- Chia wallet operations (balance, transactions, sending)
- Blockchain status and sync information
- Transaction history and analysis
- Wallet management capabilities

## Features

### MCP Tools
- `get_wallet_balance` - Get balance of any Chia wallet
- `get_transactions` - Get transaction history with pagination
- `send_transaction` - Send XCH or other tokens to addresses
- `get_wallets` - List all available wallets
- `get_sync_status` - Check blockchain synchronization status

### MCP Resources
- `chia://blockchain/status` - Real-time blockchain information
- `chia://wallet/balance` - Current wallet balance data
- `chia://wallet/transactions` - Recent transaction history

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