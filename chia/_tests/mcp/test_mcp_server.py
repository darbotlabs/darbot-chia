import asyncio

import pytest
from httpx import AsyncClient

from chia.mcp.server import app


@pytest.mark.asyncio
async def test_ping() -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/mcp/ping")
    assert response.json() == {"ping": "pong"}

