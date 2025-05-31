# Darbot Chia - VSCode Extension

A Visual Studio Code extension for Chia blockchain development and operations via MCP (Model Context Protocol).

## Features

- **Real-time Blockchain Monitoring**: View blockchain state, height, difficulty, and sync status
- **Wallet Management**: Browse wallets, check balances, and manage accounts
- **Farming Dashboard**: Monitor harvesters, plots, and farming operations
- **Offer Management**: Create and manage Chia offers directly from VSCode
- **CAT Token Support**: View and manage Chia Asset Tokens (CATs)
- **Data Layer Integration**: Interact with Chia's data layer stores
- **DID & VC Support**: Manage Decentralized Identifiers and Verifiable Credentials
- **MCP Tool Explorer**: Browse and execute all available MCP tools

## Requirements

- Visual Studio Code 1.74.0 or higher
- A running Chia node with MCP server enabled
- Node.js 16.0.0 or higher (for the underlying MCP client)

## Installation

1. Install from the VSCode marketplace (search for "Darbot Chia")
2. Or install manually from VSIX file

## Setup

1. **Start your Chia node** with MCP server enabled
2. **Configure the extension** via VSCode settings:
   - `darbotChia.mcpServer.host`: MCP server hostname (default: localhost)
   - `darbotChia.mcpServer.port`: MCP server port (default: 8550)
   - `darbotChia.mcpServer.useSSL`: Use SSL/TLS (default: false)
   - `darbotChia.autoConnect`: Auto-connect on startup (default: false)

3. **Connect to your node** using the command palette:
   - `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type "Darbot Chia: Connect to Chia Node"

## Usage

### Explorer Panel

Once connected, the Chia Blockchain explorer panel shows:

- **Blockchain**: Current height, difficulty, sync status
- **Wallets**: All configured wallets with types and IDs
- **Farmer**: Connected harvesters and plot counts
- **Harvester**: Plot information organized by directory
- **Offers**: Recent offers with status
- **CATs**: Known Chia Asset Tokens
- **Data Layer**: Owned data stores
- **DIDs & VCs**: Decentralized identity management

### Commands

Access all commands via the command palette (`Ctrl+Shift+P`):

- `Darbot Chia: Connect to Chia Node` - Establish connection
- `Darbot Chia: Disconnect from Chia Node` - Close connection
- `Darbot Chia: Get Blockchain State` - View detailed blockchain status
- `Darbot Chia: Get Wallets` - List all wallets
- `Darbot Chia: Show Available MCP Tools` - Browse all available tools

### Output Channels

The extension creates several output channels for detailed information:

- **Chia Blockchain State**: Detailed blockchain information
- **Chia Wallets**: Wallet details and balances
- **MCP Tool Details**: Information about selected MCP tools

## Configuration

Configure the extension through VSCode settings:

```json
{
    "darbotChia.mcpServer.host": "localhost",
    "darbotChia.mcpServer.port": 8550,
    "darbotChia.mcpServer.useSSL": false,
    "darbotChia.autoConnect": false
}
```

### Remote Connections

To connect to a remote Chia node:

```json
{
    "darbotChia.mcpServer.host": "my-chia-node.local",
    "darbotChia.mcpServer.port": 8550,
    "darbotChia.mcpServer.useSSL": true
}
```

## MCP Server Setup

This extension requires a Chia node running the MCP server. See the [darbot-chia repository](https://github.com/darbotlabs/darbot-chia) for detailed setup instructions.

## Troubleshooting

### Connection Issues

1. **Verify MCP server is running**: Check that your Chia node has the MCP server enabled
2. **Check network connectivity**: Ensure VSCode can reach the specified host and port
3. **SSL/TLS configuration**: Verify SSL settings match your server configuration
4. **Firewall settings**: Ensure the MCP port is not blocked

### Common Error Messages

- `Cannot connect to MCP server`: MCP server is not running or unreachable
- `MCP Error (404): tool not found`: Requested tool is not available
- `Network Error`: Connection timeout or network issue
- `WebSocket not connected`: WebSocket connection failed (optional feature)

### Debug Output

Enable debug output in the VSCode Developer Console:

1. Open Developer Tools (`Help > Toggle Developer Tools`)
2. Look for "Darbot Chia" log messages
3. Check the Network tab for MCP server requests

## Development

For development and contribution information, see the [main repository](https://github.com/darbotlabs/darbot-chia).

### Building from Source

```bash
git clone https://github.com/darbotlabs/darbot-chia.git
cd darbot-chia/vscode-extension
npm install
npm run compile
```

### Packaging

```bash
npm install -g vsce
vsce package
```

## Architecture

The extension uses:

- **MCP Client**: HTTP/WebSocket client for communicating with Chia MCP server
- **Tree Data Provider**: VSCode tree view for blockchain data exploration
- **Command Handlers**: VSCode commands for various Chia operations
- **Configuration Management**: VSCode settings integration

## Available MCP Tools

The extension provides access to 24+ MCP tools across categories:

- **Wallet** (4 tools): Authentication, balance queries, wallet management
- **Full Node** (3 tools): Blockchain state, block queries, network info
- **Farmer** (2 tools): Harvester monitoring, signage points
- **Harvester** (2 tools): Plot management, directory monitoring
- **Offers** (3 tools): Offer creation, trading, management
- **CAT** (3 tools): Token listing, wallet creation, stray cat detection
- **Data Layer** (3 tools): Store management, data queries
- **DID** (1 tool): Decentralized identifier creation
- **VC** (2 tools): Verifiable credential minting and retrieval

## License

Apache-2.0

## Support

For issues and feature requests, please use the [GitHub repository](https://github.com/darbotlabs/darbot-chia/issues).

## Release Notes

### 0.1.0 (Beta)

Initial release with core functionality:

- MCP server connection management
- Blockchain state monitoring
- Wallet and farming dashboards
- Offer and CAT management
- Data layer integration
- DID and VC support
- Comprehensive tool explorer