"""Pull stub balances into the active vault."""

from __future__ import annotations

from adacip.chain.rpc import RpcClient
from adacip.config import WalletConfig
from adacip.models import Vault


class SyncEngine:
    """Refresh account balances through :class:`RpcClient`."""

    def __init__(self, config: WalletConfig | None = None) -> None:
        self.client = RpcClient(config or WalletConfig())

    def sync(self, vault: Vault) -> Vault:
        """Mutate ``vault`` balances in place and return it."""
        for account in vault.accounts:
            account.balance = self.client.get_balance(account.address)
        return vault
