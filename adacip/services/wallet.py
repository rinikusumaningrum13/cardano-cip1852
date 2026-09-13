"""High-level wallet operations."""

from __future__ import annotations

import hashlib

from adacip.config import WalletConfig
from adacip.crypto.address import public_key_to_address
from adacip.crypto.keys import derive_key, seed_from_mnemonic
from adacip.crypto.mnemonic import generate_mnemonic
from adacip.models import Account, Vault
from adacip.storage.vault import VaultStore


class WalletService:
    """Create vaults and derive accounts."""

    def __init__(self, config: WalletConfig | None = None) -> None:
        self.config = config or WalletConfig()
        self.store = VaultStore(self.config.storage_path())
        self.active: Vault | None = None

    def create_vault(self, name: str, passphrase: str) -> Vault:
        """Create a vault with one derived account."""
        mnemonic = generate_mnemonic(12, f"{name}:{self.config.coin}")
        vault_id = hashlib.sha256(f"{name}:{mnemonic}".encode()).hexdigest()[:16]
        vault = Vault(vault_id=vault_id, name=name, coin=self.config.coin)
        account = self._account(mnemonic, 0, "Primary")
        vault.accounts.append(account)
        self.store.save(vault, passphrase)
        self.active = vault
        self._mnemonic = mnemonic
        return vault

    def open_vault(self, vault_id: str, passphrase: str) -> Vault | None:
        vault = self.store.load(vault_id, passphrase)
        self.active = vault
        return vault

    def add_account(self, passphrase: str, label: str) -> Account:
        if self.active is None:
            raise RuntimeError("no active vault")
        mnemonic = generate_mnemonic(12, f"{self.active.name}:{self.config.coin}")
        account = self._account(mnemonic, len(self.active.accounts), label)
        self.active.accounts.append(account)
        self.store.save(self.active, passphrase)
        return account

    def _account(self, mnemonic: str, index: int, label: str) -> Account:
        seed = seed_from_mnemonic(mnemonic, self.config.coin)
        _, pub = derive_key(seed, index, self.config.derivation_path)
        return Account(
            index=index,
            label=label,
            address=public_key_to_address(pub),
            coin="ADA",
        )
