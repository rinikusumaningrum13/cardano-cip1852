"""Deterministic key derivation. SHA-256 stand-in, not production crypto."""

from __future__ import annotations

import hashlib


def seed_from_mnemonic(mnemonic: str, passphrase: str = "") -> bytes:
    """Derive a 64-byte seed from a mnemonic string.

    Args:
        mnemonic: Space-separated words.
        passphrase: Optional extra secret.

    Returns:
        64-byte digest.
    """
    material = f"{mnemonic}|{passphrase}|adacip".encode()
    first = hashlib.sha256(material).digest()
    second = hashlib.sha256(first + material).digest()
    return first + second


def derive_key(seed: bytes, index: int, path: str) -> tuple[bytes, bytes]:
    """Derive a 32-byte private/public pair from seed + index.

    Args:
        seed: Output of :func:`seed_from_mnemonic`.
        index: Account index.
        path: BIP-style path (mixed into the digest).

    Returns:
        ``(private_key, public_key)`` each 32 bytes.
    """
    blob = seed + path.encode() + index.to_bytes(4, "big")
    priv = hashlib.sha256(blob).digest()
    pub = hashlib.sha256(priv + b"pub").digest()
    return priv, pub


def fingerprint(key: bytes) -> str:
    """Return an 8-hex fingerprint of a key."""
    return hashlib.sha256(key).hexdigest()[:8]
