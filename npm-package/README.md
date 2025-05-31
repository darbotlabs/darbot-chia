# @darbotlabs/darbot-chia

A TypeScript/JavaScript client library for interacting with Chia blockchain via MCP (Model Context Protocol).

## Installation

```bash
npm install @darbotlabs/darbot-chia
```

## Quick Start

```typescript
import { DarbotChiaMCPClient, ChiaTools } from '@darbotlabs/darbot-chia';

// Create client
const client = new DarbotChiaMCPClient({
    host: 'localhost',
    port: 8550,
    useSSL: false
});

// Connect to MCP server
await client.connect();

// Use high-level tools
const tools = new ChiaTools(client);

// Get blockchain state
const state = await tools.getBlockchainState();
console.log(`Blockchain height: ${state.blockchain_state.peak?.height}`);

// Get wallets
const wallets = await tools.getWallets();
console.log(`Found ${wallets.wallets.length} wallets`);

// Get plots
const plots = await tools.getPlots();
console.log(`Total plots: ${plots.plots.length}`);
```

## Features

### MCP Client
- HTTP and WebSocket connections to Chia MCP server
- Automatic error handling and retries
- TypeScript support with full type definitions
- Configurable timeouts and SSL support

### High-Level Tools
- **Wallet operations**: Get wallets, balances, public keys
- **Blockchain queries**: Get state, blocks, network info
- **Farming**: Monitor harvesters, plots, signage points
- **Trading**: Create and manage offers
- **CAT tokens**: List and manage Chia Asset Tokens
- **Data Layer**: Interact with Chia's data layer
- **DIDs & VCs**: Decentralized identifiers and verifiable credentials

## API Reference

### MCPClient

```typescript
const client = new DarbotChiaMCPClient({
    host: 'localhost',        // MCP server host
    port: 8550,              // MCP server port
    useSSL: false,           // Use HTTPS/WSS
    timeout: 30000           // Request timeout in ms
});

// Connection
await client.connect();
await client.disconnect();
client.isConnected();

// Tools
const tools = await client.getAvailableTools();
const result = await client.callTool('group', 'name', params);

// WebSocket (optional)
await client.connectWebSocket();
const result = await client.callToolViaWebSocket('group', 'name', params);
```

### ChiaTools

```typescript
const tools = new ChiaTools(client);

// Wallet
const wallets = await tools.getWallets();
const balance = await tools.getWalletBalance(walletId);
const keys = await tools.getPublicKeys();
await tools.loginWallet(fingerprint);

// Blockchain
const state = await tools.getBlockchainState();
const block = await tools.getBlock(headerHash);
const network = await tools.getNetworkInfo();

// Farming
const harvesters = await tools.getHarvesters();
const plots = await tools.getPlots();
const signagePoints = await tools.getSignagePoints();

// Offers
const offers = await tools.getAllOffers(0, 50);
const newOffer = await tools.createOfferForIds(offer, payments, fee);
await tools.takeOffer(offerString, fee);

// CATs
const cats = await tools.getCATList();
const newCAT = await tools.createNewCATWallet(amount, fee);
const strayCats = await tools.getStrayCats();

// Data Layer
const stores = await tools.getOwnedStores();
const newStore = await tools.createDataStore(fee);
const value = await tools.getValue(storeId, key);

// DIDs & VCs
const did = await tools.createNewDIDWallet(amount, fee);
const vc = await tools.mintVC(didId, targetAddress, fee);
const vcDetails = await tools.getVC(launcherId);
```

## Configuration

The client can be configured with various options:

```typescript
const client = new DarbotChiaMCPClient({
    host: 'my-chia-node.local',
    port: 8550,
    useSSL: true,
    timeout: 60000
});
```

## Error Handling

The library throws descriptive errors for different failure scenarios:

```typescript
try {
    await client.connect();
    const state = await tools.getBlockchainState();
} catch (error) {
    if (error.message.includes('Cannot connect')) {
        console.error('MCP server is not running');
    } else if (error.message.includes('MCP Error')) {
        console.error('Server-side error:', error.message);
    } else {
        console.error('Unexpected error:', error.message);
    }
}
```

## WebSocket Support

For real-time updates, you can use WebSocket connections:

```typescript
// Establish WebSocket connection
await client.connectWebSocket();

// Use WebSocket for calls (optional)
const state = await client.callToolViaWebSocket('full_node', 'get_blockchain_state');
```

## Requirements

- Node.js 16.0.0 or higher
- A running Chia node with MCP server enabled
- TypeScript 4.9+ (for TypeScript projects)

## Setup MCP Server

This library requires a Chia node running the MCP server. See the [darbot-chia repository](https://github.com/darbotlabs/darbot-chia) for setup instructions.

## TypeScript Support

Full TypeScript definitions are included:

```typescript
import { 
    DarbotChiaMCPClient,
    ChiaTools,
    ChiaWallet,
    ChiaBlockchainState,
    MCPTool
} from '@darbotlabs/darbot-chia';
```

## License

Apache-2.0

## Contributing

Contributions are welcome! Please see the [main repository](https://github.com/darbotlabs/darbot-chia) for contribution guidelines.

## Changelog

### 0.1.0 (Beta)
- Initial release
- Basic MCP client functionality
- High-level tools for common operations
- TypeScript support
- WebSocket support
- Error handling