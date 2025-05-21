from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from chia.rpc.data_layer_rpc_client import DataLayerRpcClient
from chia.rpc.farmer_rpc_client import FarmerRpcClient
from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.rpc.harvester_rpc_client import HarvesterRpcClient
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
