"""JSON vault files on disk. Payload is XOR-wrapped, not a real cipher."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from adacip.models import Account, Vault


def _xor(data: bytes, passphrase: str) -> bytes:
    key = hashlib.sha256(passphrase.encode()).digest()
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


class VaultStore:
    """Read and write vault JSON files."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def path_for(self, vault_id: str) -> Path:
        return self.directory / f"{vault_id}.vault"

    def save(self, vault: Vault, passphrase: str) -> Path:
        """Persist a vault. Returns the file path."""
        payload = json.dumps(
            {
                "vault_id": vault.vault_id,
                "name": vault.name,
                "coin": vault.coin,
                "created_at": vault.created_at,
                "accounts": [asdict(a) for a in vault.accounts],
            }
        ).encode()
        wrapped = _xor(payload, passphrase)
        target = self.path_for(vault.vault_id)
        target.write_bytes(wrapped)
        return target

    def load(self, vault_id: str, passphrase: str) -> Vault | None:
        """Open a vault or return None when the file is missing."""
        target = self.path_for(vault_id)
        if not target.exists():
            return None
        raw = _xor(target.read_bytes(), passphrase)
        data = json.loads(raw.decode())
        accounts = [Account(**row) for row in data["accounts"]]
        return Vault(
            vault_id=data["vault_id"],
            name=data["name"],
            coin=data["coin"],
            created_at=data["created_at"],
            accounts=accounts,
        )

    def list_ids(self) -> list[str]:
        return sorted(p.stem for p in self.directory.glob("*.vault"))
