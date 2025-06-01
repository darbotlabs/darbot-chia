# Example configurations for Darbot Chia

## VSCode Extension Development

### Launch Configuration (.vscode/launch.json)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Extension",
            "type": "extensionHost",
            "request": "launch",
            "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
            "outFiles": ["${workspaceFolder}/dist/**/*.js"],
            "preLaunchTask": "${workspaceFolder}:npm: compile"
        }
    ]
}
```

### VSCode Settings (settings.json)
```json
{
    "darbotChia.mcpServer.host": "localhost",
    "darbotChia.mcpServer.port": 8550,
    "darbotChia.mcpServer.useSSL": false,
    "darbotChia.autoConnect": true
}
```

## NPM Package Usage Examples

### Basic Connection
```typescript
import { DarbotChiaMCPClient } from '@darbotlabs/darbot-chia';

const client = new DarbotChiaMCPClient({
    host: 'localhost',
    port: 8550,
    useSSL: false
});

await client.connect();
console.log('Connected:', client.isConnected());
```

### Using High-Level Tools
```typescript
import { DarbotChiaMCPClient, ChiaTools } from '@darbotlabs/darbot-chia';

const client = new DarbotChiaMCPClient();
await client.connect();

const tools = new ChiaTools(client);

// Get blockchain state
const state = await tools.getBlockchainState();
console.log(`Height: ${state.blockchain_state.peak?.height}`);

// Get wallets
const wallets = await tools.getWallets();
console.log(`Wallets: ${wallets.wallets.length}`);

// Get plots
const plots = await tools.getPlots();
console.log(`Plots: ${plots.plots.length}`);
```

### WebSocket Usage
```typescript
// Establish WebSocket connection
await client.connectWebSocket();

// Use WebSocket for calls
const state = await client.callToolViaWebSocket('full_node', 'get_blockchain_state');
```

### Error Handling
```typescript
try {
    await client.connect();
    const balance = await tools.getWalletBalance(1);
    console.log('Balance:', balance);
} catch (error) {
    if (error.message.includes('Cannot connect')) {
        console.error('MCP server is not running');
    } else if (error.message.includes('MCP Error')) {
        console.error('Server error:', error.message);
    } else {
        console.error('Unexpected error:', error.message);
    }
}
```

## MCP Server Configuration

### Starting the MCP Server
```bash
# Start Chia node with MCP server enabled
chia start node
# MCP server will be available on localhost:8550 by default
```

### Custom Configuration
```yaml
# In your Chia config.yaml
mcp:
  port: 8550
  host: "localhost"
  ssl:
    private_crt: "path/to/cert.crt"
    private_key: "path/to/cert.key"
```

## Development Setup

### Building the Extension
```bash
cd vscode-extension
npm install
npm run compile

# Package for distribution
npm install -g vsce
vsce package
```

### Building the NPM Package
```bash
cd npm-package
npm install
npm run build

# Test before publishing
npm test
npm run lint
```

### Testing MCP Tools
```bash
# Run basic MCP test
python test_mcp_basic.py

# Test specific tool category
python -c "
from chia.mcp.tools_wallet import get_wallets
from chia.mcp.client_pool import ClientPool
import asyncio

async def test():
    pool = ClientPool()
    result = await get_wallets(pool, {})
    print(result)

asyncio.run(test())
"
```

## Docker Development Environment

### Dockerfile for Development
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install -e .
RUN cd vscode-extension && npm install
RUN cd npm-package && npm install

EXPOSE 8550

CMD ["python", "-m", "chia.server.start_full_node"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  chia-dev:
    build: .
    ports:
      - "8550:8550"
    volumes:
      - .:/app
      - chia-data:/root/.chia
    environment:
      - CHIA_ROOT=/root/.chia

volumes:
  chia-data:
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Test Darbot Chia Extensions

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.11'
          
      - name: Test MCP Tools
        run: python test_mcp_basic.py
        
      - name: Build VSCode Extension
        run: |
          cd vscode-extension
          npm install
          npm run compile
          
      - name: Build NPM Package
        run: |
          cd npm-package
          npm install
          npm run build
          npm test
```

## Troubleshooting

### Common Issues

**"Cannot connect to MCP server"**
- Ensure Chia node is running
- Check MCP server port (default 8550)
- Verify firewall settings

**"Tool not found"**  
- Check tool name spelling
- Verify MCP server has the tool loaded
- Use `get_available_tools()` to list available tools

**TypeScript compilation errors**
- Run `npm install` in the appropriate directory
- Check TypeScript version compatibility
- Clear `node_modules` and reinstall if needed

### Debug Mode

Enable debug logging:
```typescript
// For npm package
const client = new DarbotChiaMCPClient({
    host: 'localhost',
    port: 8550,
    timeout: 60000  // Longer timeout for debugging
});

// Enable verbose logging in VSCode
// Open Developer Tools -> Console
```