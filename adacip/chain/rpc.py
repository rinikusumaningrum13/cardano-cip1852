"""Stub RPC client. Digests stand in for node responses."""

from __future__ import annotations

import hashlib

from adacip.config import WalletConfig


class RpcClient:
    """Deterministic stand-in for a ADA node."""

    def __init__(self, config: WalletConfig) -> None:
        self.config = config

    def ping(self) -> bool:
        """Always succeeds — no socket is opened."""
        return bool(self.config.rpc_endpoint)

    def get_balance(self, address: str) -> int:
        """Return a stable fake balance in lovelace."""
        raw = hashlib.sha256(f"{self.config.coin}:{address}".encode()).digest()
        return int.from_bytes(raw[:4], "big") % 10_000_000

    def get_height(self) -> int:
        """Return a stub chain height."""
        raw = hashlib.sha256(self.config.coin.encode()).digest()
        return 800_000 + int.from_bytes(raw[:2], "big")
