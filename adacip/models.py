"""Domain models for adacip."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class Account:
    """A single derived account inside a vault."""

    index: int
    label: str
    address: str
    balance: int = 0
    coin: str = "ADA"


@dataclass(slots=True)
class Vault:
    """Encrypted vault metadata plus derived accounts."""

    vault_id: str
    name: str
    coin: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    accounts: list[Account] = field(default_factory=list)

    @property
    def total_balance(self) -> int:
        """Sum of stub balances across accounts."""
        return sum(item.balance for item in self.accounts)
