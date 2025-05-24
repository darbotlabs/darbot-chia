from __future__ import annotations

from typing import Any, Optional

from chia.types.transaction_record import TransactionRecord
from chia_rs.sized_bytes import bytes32
from chia_rs.sized_ints import uint32, uint64

from chia.mcp.client_pool import get_client
from chia.pools.pool_wallet_info import PoolWalletInfo
from chia.rpc.farmer_rpc_client import FarmerRpcClient
from chia.rpc.wallet_rpc_client import WalletRpcClient


async def _wallet() -> WalletRpcClient:
    client = await get_client("wallet")
    assert isinstance(client, WalletRpcClient)
    return client


async def _farmer() -> FarmerRpcClient:
    client = await get_client("farmer")
    assert isinstance(client, FarmerRpcClient)
    return client


async def create_new_pool_wallet(
    target_puzzlehash: Optional[bytes32],
    pool_url: Optional[str],
    relative_lock_height: uint32,
    backup_host: str,
    mode: str,
    state: str,
    fee: uint64,
    p2_singleton_delay_time: Optional[uint64] = None,
    p2_singleton_delayed_ph: Optional[bytes32] = None,
    extra_conditions: tuple[Any, ...] = tuple(),
) -> TransactionRecord:
    """Create a new pool wallet via the wallet RPC."""
    wallet = await _wallet()
    return await wallet.create_new_pool_wallet(
        target_puzzlehash,
        pool_url,
        relative_lock_height,
        backup_host,
        mode,
        state,
        fee,
        p2_singleton_delay_time,
        p2_singleton_delayed_ph,
        extra_conditions,
    )


async def pw_self_pool(wallet_id: int, fee: uint64) -> dict[str, Any]:
    """Leave a pool and revert to self pooling."""
    wallet = await _wallet()
    return await wallet.pw_self_pool(wallet_id, fee)


async def pw_join_pool(
    wallet_id: int,
    target_puzzlehash: bytes32,
    pool_url: str,
    relative_lock_height: uint32,
    fee: uint64,
) -> dict[str, Any]:
    """Join a pool with the specified parameters."""
    wallet = await _wallet()
    return await wallet.pw_join_pool(
        wallet_id,
        target_puzzlehash,
        pool_url,
        relative_lock_height,
        fee,
    )


async def pw_absorb_rewards(
    wallet_id: int,
    fee: uint64 = uint64(0),
    max_spends_in_tx: Optional[int] = None,
) -> dict[str, Any]:
    """Claim rewards for a pool wallet."""
    wallet = await _wallet()
    return await wallet.pw_absorb_rewards(wallet_id, fee, max_spends_in_tx)


async def pw_status(wallet_id: int) -> tuple[PoolWalletInfo, list[TransactionRecord]]:
    """Return the pooling status for a wallet."""
    wallet = await _wallet()
    return await wallet.pw_status(wallet_id)


async def get_pool_state() -> dict[str, Any]:
    """Return pooling state from the farmer."""
    farmer = await _farmer()
    return await farmer.get_pool_state()


async def set_payout_instructions(launcher_id: bytes32, payout_instructions: str) -> dict[str, Any]:
    """Update payout instructions for a pool launcher."""
    farmer = await _farmer()
    return await farmer.set_payout_instructions(launcher_id, payout_instructions)


async def set_reward_targets(
    farmer_target: Optional[str] = None,
    pool_target: Optional[str] = None,
) -> dict[str, Any]:
    """Update farmer and pool reward targets."""
    farmer = await _farmer()
    return await farmer.set_reward_targets(farmer_target, pool_target)


async def get_pool_login_link(launcher_id: bytes32) -> Optional[str]:
    """Return the login link for a pool dashboard."""
    farmer = await _farmer()
    return await farmer.get_pool_login_link(launcher_id)


async def get_pool_stats() -> dict[str, Any]:
    """Convenience helper returning farmer pooling statistics."""
    return await get_pool_state()
