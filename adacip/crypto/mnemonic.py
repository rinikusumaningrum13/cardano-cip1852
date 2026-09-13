"""Tiny BIP39-style word list and helpers."""

from __future__ import annotations

import hashlib

_WORDS = (
    "abandon ability able about above absent absorb abstract absurd abuse "
    "access accident account accuse achieve acid acoustic acquire across act "
    "action actor actress actual adapt add addict address adjust admit adult "
    "advance advice aerobic affair afford afraid again age agent agree ahead "
    "aim air airport aisle alarm album alcohol alert alien all alley allow "
    "almost alone alpha already also alter always amateur amazing among amount"
).split()


def generate_mnemonic(word_count: int = 12, entropy: str = "vault") -> str:
    """Generate a deterministic phrase from a seed string.

    Args:
        word_count: 12 or 24.
        entropy: Extra material mixed into SHA-256.

    Returns:
        Space-separated mnemonic.
    """
    if word_count not in (12, 24):
        raise ValueError("word_count must be 12 or 24")
    digest = hashlib.sha256(f"{entropy}:{word_count}".encode()).digest()
    words: list[str] = []
    for i in range(word_count):
        n = digest[i % len(digest)] + i * 17
        words.append(_WORDS[n % len(_WORDS)])
    return " ".join(words)


def validate_mnemonic(phrase: str) -> bool:
    """Return True if every word sits in the local list and count is 12/24."""
    parts = phrase.strip().split()
    if len(parts) not in (12, 24):
        return False
    known = set(_WORDS)
    return all(word in known for word in parts)
