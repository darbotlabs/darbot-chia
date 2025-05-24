from __future__ import annotations

import asyncio

from pathlib import Path
from typing import Any, Optional

from chia_rs.sized_ints import uint16

from collections.abc import Awaitable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


from chia.rpc.data_layer_rpc_client import DataLayerRpcClient
from chia.rpc.farmer_rpc_client import FarmerRpcClient
from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.rpc.harvester_rpc_client import HarvesterRpcClient

from chia.rpc.rpc_client import RpcClient
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.task_referencer import create_referenced_task

CLIENT_TYPES: dict[str, type[RpcClient]] = {
    "wallet": WalletRpcClient,
    "full_node": FullNodeRpcClient,
    "farmer": FarmerRpcClient,
    "harvester": HarvesterRpcClient,
    "data_layer": DataLayerRpcClient,
}

TOOL_GROUP_TO_CLIENT: dict[str, str] = {
    "wallet": "wallet",
    "node": "full_node",
    "farmer": "farmer",
    "harvester": "harvester",
    "data": "data_layer",
    "data_layer": "data_layer",
}


class ClientPool:
    """Manage connections for RPC clients with automatic reconnection."""

    def __init__(self, root_path: Optional[Path] = None) -> None:
        self.root_path = root_path or DEFAULT_ROOT_PATH
        self._clients: dict[str, RpcClient] = {}
        self._config: Optional[dict[str, Any]] = None
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        self._config = load_config(self.root_path, "config.yaml", fill_missing_services=True)
        tasks = [create_referenced_task(self._connect(name, cls)) for name, cls in CLIENT_TYPES.items()]
        await asyncio.gather(*tasks)

    async def _connect(self, name: str, cls: type[RpcClient]) -> None:
        assert self._config is not None
        host = self._config["self_hostname"]
        port = uint16(self._config[name]["rpc_port"])
        while True:
            try:
                client = await cls.create(host, port, self.root_path, self._config)
                await client.healthz()
                async with self._lock:
                    old = self._clients.get(name)
                    self._clients[name] = client
                    if old is not None:
                        old.close()
                        await old.await_closed()
                break
            except asyncio.CancelledError:
                raise
            except Exception:
                await asyncio.sleep(5)

    async def _get_or_reconnect(self, name: str) -> RpcClient:
        async with self._lock:
            client = self._clients.get(name)
        if client is None:
            await self._connect(name, CLIENT_TYPES[name])
            async with self._lock:
                client = self._clients[name]
        else:
            try:
                await client.healthz()
            except asyncio.CancelledError:
                raise
            except Exception:
                await self._connect(name, CLIENT_TYPES[name])
                async with self._lock:
                    client = self._clients[name]
        return client

    async def get_client(self, tool_group: str) -> RpcClient:
        name = TOOL_GROUP_TO_CLIENT.get(tool_group)
        if name is None:
            raise ValueError(f"Unknown tool group: {tool_group}")
        return await self._get_or_reconnect(name)

    async def close(self) -> None:
        async with self._lock:
            clients = list(self._clients.values())
            self._clients.clear()
        for client in clients:
            client.close()
            await client.await_closed()


_pool: Optional[ClientPool] = None


async def init_pool(root_path: Optional[Path] = None) -> None:
    global _pool
    pool = ClientPool(root_path)
    await pool.initialize()
    _pool = pool


async def get_client(tool_group: str) -> RpcClient:
    if _pool is None:
        await init_pool()
    assert _pool is not None
    return await _pool.get_client(tool_group)
=======
from chia.rpc.wallet_rpc_client import WalletRpcClient


@dataclass
class ClientPool:
    wallet: Optional[WalletRpcClient] = None
    full_node: Optional[FullNodeRpcClient] = None
    farmer: Optional[FarmerRpcClient] = None
    harvester: Optional[HarvesterRpcClient] = None
    data_layer: Optional[DataLayerRpcClient] = None

    async def start(self, config: dict[str, Any]) -> None:
        root_path = Path(config["root_path"])
        self.wallet = await WalletRpcClient.create(
            self_hostname=config.get("self_hostname", "localhost"),
            port=config["wallet"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        self.full_node = await FullNodeRpcClient.create(
            self_hostname=config.get("self_hostname", "localhost"),
            port=config["full_node"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        self.farmer = await FarmerRpcClient.create(
            self_hostname=config.get("self_hostname", "localhost"),
            port=config["farmer"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        self.harvester = await HarvesterRpcClient.create(
            self_hostname=config.get("self_hostname", "localhost"),
            port=config["harvester"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        if config.get("data_layer", {}).get("enable", False):
            self.data_layer = await DataLayerRpcClient.create(
                self_hostname=config.get("self_hostname", "localhost"),
                port=config["data_layer"]["rpc_port"],
                root_path=root_path,
                net_config=config,
            )

    async def close(self) -> None:
        tasks: list[Awaitable[None]] = []
        for client in [self.wallet, self.full_node, self.farmer, self.harvester, self.data_layer]:
            if client is not None:
                tasks.append(client.close())
        if tasks:
            await asyncio.gather(*tasks)

