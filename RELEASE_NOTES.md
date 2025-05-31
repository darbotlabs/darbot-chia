# Darbot Chia v0.1.0 Release Notes

This is the initial beta release of the Darbot Chia development tools suite, providing comprehensive VSCode integration and npm package for Chia blockchain development.

## 🎉 What's New

### VSCode Extension (`darbot-chia`)
- **Real-time Blockchain Explorer**: Monitor blockchain state, height, difficulty, and sync status
- **Wallet Dashboard**: Browse wallets, check balances, manage accounts  
- **Farming Console**: Monitor harvesters, plots, and farming operations
- **Offer Management**: Create and manage Chia offers directly in VSCode
- **CAT Token Support**: View and manage Chia Asset Tokens
- **Data Layer Integration**: Interact with Chia's data layer stores
- **DID & VC Support**: Manage Decentralized Identifiers and Verifiable Credentials
- **MCP Tool Explorer**: Browse and execute all 24+ available MCP tools

### NPM Package (`@darbotlabs/darbot-chia`)
- **TypeScript Support**: Full type definitions and IntelliSense
- **HTTP & WebSocket**: Dual connection modes for flexibility
- **High-Level APIs**: Simplified functions for common Chia operations
- **Error Handling**: Comprehensive error handling and retry logic
- **Modular Design**: Use only the features you need

### Enhanced MCP Server
- **24+ Tools**: Comprehensive coverage of Chia operations
- **Improved Descriptions**: Detailed, user-friendly tool documentation  
- **RESTful API**: HTTP endpoints for all tools
- **WebSocket Support**: Real-time communication capability
- **Type Safety**: Full JSON schema validation

## 🛠 MCP Tools Available

### Core Categories
- **Wallet** (4 tools): Authentication, balance queries, wallet management
- **Full Node** (3 tools): Blockchain state, block queries, network info
- **Farmer** (2 tools): Harvester monitoring, signage points
- **Harvester** (2 tools): Plot management, directory monitoring
- **Offers** (3 tools): Trade creation, execution, management
- **CAT** (3 tools): Token listing, wallet creation, stray cat detection
- **Data Layer** (3 tools): Store management, data queries
- **DID** (1 tool): Decentralized identifier creation
- **VC** (2 tools): Verifiable credential minting and retrieval

## 📦 Installation

### VSCode Extension
- Install from VSCode marketplace (search for "Darbot Chia")
- Manual installation from VSIX file

### NPM Package
```bash
npm install @darbotlabs/darbot-chia
```

## ⚡ Quick Start

### VSCode Extension
1. Install the extension
2. Configure MCP server settings
3. Run "Darbot Chia: Connect to Chia Node"
4. Explore blockchain data in the sidebar

### NPM Package
```typescript
import { DarbotChiaMCPClient, ChiaTools } from '@darbotlabs/darbot-chia';

const client = new DarbotChiaMCPClient();
await client.connect();

const tools = new ChiaTools(client);
const state = await tools.getBlockchainState();
```

## 🔧 Configuration

### Prerequisites
- Node.js 16.0.0 or higher
- Running Chia node with MCP server enabled
- VSCode 1.74.0 or higher (for extension)

### Settings
```json
{
    "darbotChia.mcpServer.host": "localhost",
    "darbotChia.mcpServer.port": 8550,
    "darbotChia.mcpServer.useSSL": false,
    "darbotChia.autoConnect": false
}
```

## 🎯 Beta Features

This is a beta release focused on core functionality:

✅ **Implemented**
- MCP server integration
- Basic blockchain monitoring
- Wallet and farming dashboards
- Offer and CAT management
- TypeScript client library
- Comprehensive documentation

🚧 **Known Limitations**
- Some MCP tools have placeholder implementations
- Assets and branding are using placeholders
- WebSocket real-time updates are basic
- Error handling could be more granular

## 📋 Asset Requirements

For proper branding, the following assets are needed:

- Extension icon (128x128)
- Activity bar icon (16x16 SVG)  
- Status indicators (16x16 SVG set)
- NPM package logo (512x512)
- GitHub social preview (1280x640)
- Marketplace banner (1376x80)

See `ASSETS_README.md` for detailed specifications.

## 🚀 Development

### Building from Source
```bash
git clone https://github.com/darbotlabs/darbot-chia.git
cd darbot-chia
./build-extensions.sh
```

### Project Structure
```
├── chia/mcp/              # Core MCP server and tools
├── vscode-extension/      # VSCode extension source
├── npm-package/          # NPM package source
├── ASSETS_README.md      # Asset requirements
├── EXTENSION_README.md   # Project documentation
└── build-extensions.sh   # Build script
```

## 🐛 Known Issues

- Some MCP tools need complete implementation (placeholders exist)
- WebSocket connection management could be improved
- Extension icons are using VS Code built-ins
- Error messages could be more user-friendly

## 🔮 Roadmap

### v0.2.0 (Next Release)
- Complete MCP tool implementations
- Real-time WebSocket updates
- Enhanced plot management UI
- Offer creation wizard
- Performance optimizations

### v1.0.0 (Production)
- Full feature parity with Chia RPC
- Advanced debugging tools
- Plugin architecture
- Enterprise features

## 🤝 Contributing

We welcome contributions! Please see the main repository for guidelines:
- Fork the repository
- Create a feature branch
- Test thoroughly
- Submit a pull request

## 📄 License

Apache-2.0

## 🔗 Links

- **GitHub**: https://github.com/darbotlabs/darbot-chia
- **Issues**: https://github.com/darbotlabs/darbot-chia/issues
- **VSCode Marketplace**: Coming soon
- **NPM Package**: Coming soon

## 💬 Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation in `EXTENSION_README.md`
- Use the "Show Available MCP Tools" command in VSCode for tool details

---

*This is a beta release for early adopters and contributors. Feedback and contributions are greatly appreciated!*