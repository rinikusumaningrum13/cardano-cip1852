"""Address encoding for ADA."""

from __future__ import annotations

import hashlib

PREFIX = "addr"


def public_key_to_address(public_key: bytes) -> str:
    """Map a public key to a stub address.

    Args:
        public_key: 32-byte key.

    Returns:
        Checksummed address string.
    """
    digest = hashlib.sha256(public_key + PREFIX.encode()).hexdigest()
    return f"{PREFIX}{digest[:32]}"


def validate_address(address: str) -> bool:
    """Cheap structural check used by tests and the CLI."""
    if not address.startswith(PREFIX):
        return False
    body = address[len(PREFIX):]
    return len(body) == 32 and all(ch in "0123456789abcdef" for ch in body)
