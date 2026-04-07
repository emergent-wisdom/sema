"""Shared utilities for Sema."""

from typing import Any


def compact_dict(d: dict[str, Any]) -> dict[str, Any]:
    """Remove empty/null values to reduce context waste for LLM consumers.

    Filters out:
    - None values
    - Empty strings ""
    - Empty lists []
    - Empty dicts {}

    Recursively compacts nested dicts.
    """
    result = {}
    for k, v in d.items():
        # Skip None
        if v is None:
            continue
        # Skip empty strings (but keep "0" or False)
        if v == "":
            continue
        # Skip empty lists
        if isinstance(v, list) and len(v) == 0:
            continue
        # Skip empty dicts
        if isinstance(v, dict) and len(v) == 0:
            continue
        # Recursively compact nested dicts
        if isinstance(v, dict):
            compacted = compact_dict(v)
            if compacted:  # Only include if non-empty after compaction
                result[k] = compacted
        else:
            result[k] = v
    return result
