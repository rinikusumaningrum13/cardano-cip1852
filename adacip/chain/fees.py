"""Fee table for ADA."""

from __future__ import annotations

PRESETS = {"low": 2, "medium": 8, "high": 24}


def estimate_fee(priority: str = "medium") -> int:
    """Return a stub fee in lovelace per virtual unit.

    Args:
        priority: ``low``, ``medium`` or ``high``.

    Returns:
        Integer fee rate.
    """
    key = priority.lower()
    if key not in PRESETS:
        raise ValueError(f"unknown priority: {priority}")
    return PRESETS[key]
