# Model Context Protocol (MCP)

The MCP server exposes Chia RPCs via HTTP and WebSocket. Enable it in `config.yaml`:

```yaml
mcp:
  enable: true
  port: 8550
```

Start the daemon and access `/mcp/ping` to verify. Available tools are listed at `/mcp/schema.json`.
