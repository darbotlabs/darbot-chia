from __future__ import annotations

import asyncio
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
    """Pool of RPC clients for different Chia services."""
    wallet: Optional[WalletRpcClient] = None
    full_node: Optional[FullNodeRpcClient] = None
    farmer: Optional[FarmerRpcClient] = None
    harvester: Optional[HarvesterRpcClient] = None
    data_layer: Optional[DataLayerRpcClient] = None

    async def start(self, config: dict[str, Any]) -> None:
        """Initialize and start all RPC clients."""
        root_path = Path(config["root_path"])
        hostname = config.get("self_hostname", "localhost")
        
        # Start wallet client
        self.wallet = await WalletRpcClient.create(
            self_hostname=hostname,
            port=config["wallet"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        
        # Start full node client
        self.full_node = await FullNodeRpcClient.create(
            self_hostname=hostname,
            port=config["full_node"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        
        # Start farmer client
        self.farmer = await FarmerRpcClient.create(
            self_hostname=hostname,
            port=config["farmer"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        
        # Start harvester client
        self.harvester = await HarvesterRpcClient.create(
            self_hostname=hostname,
            port=config["harvester"]["rpc_port"],
            root_path=root_path,
            net_config=config,
        )
        
        # Start data layer client if enabled
        if config.get("data_layer", {}).get("enable", False):
            self.data_layer = await DataLayerRpcClient.create(
                self_hostname=hostname,
                port=config["data_layer"]["rpc_port"],
                root_path=root_path,
                net_config=config,
            )

    async def close(self) -> None:
        """Close all RPC clients."""
        clients = [self.wallet, self.full_node, self.farmer, self.harvester, self.data_layer]
        for client in clients:
            if client is not None:
                client.close()
        
        # Wait for all to close
        await asyncio.gather(
            *[client.await_closed() for client in clients if client is not None],
            return_exceptions=True
        )

