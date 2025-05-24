from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket

from chia.mcp.client_pool import ClientPool
from chia.mcp.error import MCPError
from chia.mcp.registry import get_tool, schema

log = logging.getLogger(__name__)

app = FastAPI()
mcp_app = FastAPI()
app.mount("/mcp", mcp_app)

pool = ClientPool()


@mcp_app.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "pong"}


@mcp_app.get("/schema.json")
async def schema_endpoint() -> list[dict[str, Any]]:
    return schema()


@mcp_app.post("/{group}/{name}")
async def call_tool(group: str, name: str, params: dict[str, Any]) -> Any:
    tool = get_tool(group, name)
    if tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    try:
        return await tool.handler(pool, params)
    except MCPError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())


@mcp_app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            group = data.get("group")
            name = data.get("name")
            params = data.get("params", {})
            tool = get_tool(group, name) if group and name else None
            if tool is None:
                await websocket.send_json({"error": "tool not found"})
                continue
            try:
                result = await tool.handler(pool, params)
                await websocket.send_json({"result": result})
            except MCPError as e:
                await websocket.send_json(e.to_dict())
    except Exception:
        pass


async def run_mcp_server(config: dict[str, Any]) -> None:
    mcp_conf = config.get("mcp", {})
    host = config.get("self_hostname", "localhost")
    port = mcp_conf.get("port", 8550)
    ssl_cert = Path(mcp_conf.get("ssl", {}).get("private_crt", ""))
    ssl_key = Path(mcp_conf.get("ssl", {}).get("private_key", ""))

    certfile = str(ssl_cert) if ssl_cert.exists() else None
    keyfile = str(ssl_key) if ssl_key.exists() else None

    uv_config = uvicorn.Config(
        app,
        host=host,
        port=port,
        ssl_certfile=certfile,
        ssl_keyfile=keyfile,
        log_level="info",
    )
    server = uvicorn.Server(uv_config)
    log.info("Starting MCP server on %s:%s", host, port)
    await pool.start(config)
    try:
        await server.serve()
    finally:
        await pool.close()
