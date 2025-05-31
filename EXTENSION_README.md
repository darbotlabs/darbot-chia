# Darbot Chia - Development Tools & Extensions

A comprehensive suite of development tools for Chia blockchain, including a VSCode extension and npm package for MCP (Model Context Protocol) integration.

## Overview

This project provides:

1. **VSCode Extension**: `darbot-chia` - A full-featured VSCode extension for Chia development
2. **NPM Package**: `@darbotlabs/darbot-chia` - A TypeScript/JavaScript client library  
3. **MCP Server**: Built-in Model Context Protocol server with 24+ Chia tools

## Quick Start

### Prerequisites

- Node.js 16.0.0 or higher
- A running Chia node
- VSCode 1.74.0 or higher (for the extension)

### Installation

#### VSCode Extension
1. Install from VSCode marketplace (search for "Darbot Chia")
2. Or download the `.vsix` file and install manually

#### NPM Package
```bash
npm install @darbotlabs/darbot-chia
```

#### From Source
```bash
git clone https://github.com/darbotlabs/darbot-chia.git
cd darbot-chia
./build-extensions.sh
```

## Features

### 🎯 VSCode Extension Features
- **Real-time Blockchain Monitoring**: Live blockchain state, height, and sync status
- **Wallet Dashboard**: Comprehensive wallet management and balance tracking
- **Farming Console**: Monitor plots, harvesters, and farming operations
- **Offer Management**: Create and manage Chia offers directly in VSCode
- **CAT Token Support**: Full support for Chia Asset Tokens
- **Data Layer Integration**: Interact with Chia's data layer
- **DID & VC Management**: Decentralized identifiers and verifiable credentials
- **MCP Tool Explorer**: Browse and execute all 24+ available MCP tools

### 📦 NPM Package Features
- **TypeScript Support**: Full type definitions and IntelliSense
- **HTTP & WebSocket**: Dual connection modes for flexibility
- **High-Level APIs**: Simplified functions for common operations
- **Error Handling**: Comprehensive error handling and retry logic
- **Modular Design**: Use only the features you need

### 🛠 MCP Server Features
- **24+ Tools**: Comprehensive coverage of Chia operations
- **RESTful API**: HTTP endpoints for all tools
- **WebSocket Support**: Real-time communication
- **Type Safety**: Full JSON schema validation
- **Error Handling**: Consistent error responses

## MCP Tools Available

### Wallet (4 tools)
- `get_public_keys` - Get wallet public keys and fingerprints
- `get_wallet_balance` - Get detailed balance information
- `get_wallets` - List all wallets (XCH, CAT, NFT, DID)
- `log_in` - Authenticate with wallet fingerprint

### Full Node (3 tools)
- `get_blockchain_state` - Complete blockchain status
- `get_block` - Retrieve blocks by header hash
- `get_network_info` - Network and peer information

### Farming (4 tools)
- `get_harvesters` - Connected harvester information
- `get_signage_points` - Recent signage points
- `get_plots` - Plot information and statistics
- `get_plot_directories` - Monitored plot directories

### Trading (3 tools)
- `create_offer_for_ids` - Create new trade offers
- `take_offer` - Accept existing offers
- `get_all_offers` - List all offer history

### CAT Tokens (3 tools)
- `get_cat_list` - List known CAT assets
- `create_new_cat_and_wallet` - Create new CAT
- `get_stray_cats` - Find unassociated CATs

### Data Layer (3 tools)
- `get_owned_stores` - List owned data stores
- `create_data_store` - Create new data store
- `get_value` - Retrieve data by key

### Identity (3 tools)
- `create_new_did_wallet` - Create DID wallet
- `vc_mint` - Mint verifiable credentials
- `vc_get` - Retrieve VC details

## Configuration

### VSCode Extension Settings
```json
{
    "darbotChia.mcpServer.host": "localhost",
    "darbotChia.mcpServer.port": 8550,
    "darbotChia.mcpServer.useSSL": false,
    "darbotChia.autoConnect": false
}
```

### NPM Package Usage
```typescript
import { DarbotChiaMCPClient, ChiaTools } from '@darbotlabs/darbot-chia';

const client = new DarbotChiaMCPClient({
    host: 'localhost',
    port: 8550,
    useSSL: false
});

await client.connect();
const tools = new ChiaTools(client);

// Get blockchain state
const state = await tools.getBlockchainState();
console.log(`Height: ${state.blockchain_state.peak?.height}`);
```

## Development

### Project Structure
```
├── chia/mcp/                 # Core MCP server and tools
├── vscode-extension/         # VSCode extension source
├── npm-package/             # NPM package source  
├── build-extensions.sh      # Build script
└── ASSETS_README.md         # Asset requirements
```

### Building

```bash
# Build both packages
./build-extensions.sh

# Build VSCode extension only
cd vscode-extension
npm install && npm run compile

# Build npm package only
cd npm-package  
npm install && npm run build
```

### Testing

```bash
# Test MCP functionality
python test_mcp_basic.py

# Test VSCode extension
cd vscode-extension
npm run compile && code --extensionDevelopmentPath=.

# Test npm package
cd npm-package
npm test
```

## Publishing

### VSCode Marketplace
```bash
cd vscode-extension
npm install -g vsce
vsce package
vsce publish
```

### NPM Registry
```bash
cd npm-package
npm publish
```

## Asset Requirements

See [ASSETS_README.md](ASSETS_README.md) for detailed information about:
- Extension icons and logos
- Size specifications  
- Color palette
- Brand guidelines
- File organization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## License

Apache-2.0

## Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/darbotlabs/darbot-chia/issues)
- **Documentation**: See individual README files in each package
- **MCP Tools**: Use the "Show Available MCP Tools" command in VSCode

## Roadmap

### v0.1.0 (Current Beta)
- [x] Core MCP server with 24+ tools
- [x] VSCode extension with blockchain explorer
- [x] NPM package with TypeScript support
- [x] Basic error handling and validation
- [ ] Asset creation and branding
- [ ] Publishing to marketplaces

### v0.2.0 (Planned)
- [ ] Real-time updates via WebSocket
- [ ] Enhanced plot management
- [ ] Offer creation wizard
- [ ] CAT token management UI
- [ ] Performance optimizations

### v1.0.0 (Production)
- [ ] Full feature parity with Chia RPC
- [ ] Advanced debugging tools
- [ ] Plugin architecture
- [ ] Enterprise features

## Architecture

The project uses a layered architecture:

1. **MCP Layer**: Core protocol and tool registry
2. **Client Layer**: HTTP/WebSocket communication
3. **Tools Layer**: High-level abstraction for common operations  
4. **UI Layer**: VSCode extension interface
5. **API Layer**: NPM package for external integration

This design ensures modularity, testability, and ease of maintenance while providing multiple interfaces for different use cases.