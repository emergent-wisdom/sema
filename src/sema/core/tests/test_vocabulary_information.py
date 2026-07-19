"""Tests for generated vocabulary information."""

import importlib.util
from pathlib import Path


def load_information_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "vocabulary_merkle_root.py"
    spec = importlib.util.spec_from_file_location("vocabulary_merkle_root", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_calculate_stats_uses_canonical_path_with_legacy_fallback():
    information = load_information_module()
    patterns = [
        {"_meta": {"path": ["Mind", "Reasoning"]}},
        {"_meta": {"path": ["Mind", "Reasoning", "Search"]}},
        {"_meta": {"path": ["Infrastructure"]}},
        {"_meta": {"layer": "Society", "category": "Protocols"}},
        {},
    ]

    stats = information.calculate_stats(patterns)

    assert stats["Mind"]["Reasoning"] == 2
    assert stats["Infrastructure"]["Uncategorized"] == 1
    assert stats["Society"]["Protocols"] == 1
    assert stats["Unclassified"]["Uncategorized"] == 1
