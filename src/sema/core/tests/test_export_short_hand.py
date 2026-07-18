"""Tests for the optional shorthand vocabulary exporter."""

import importlib.util
from pathlib import Path


def load_export_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "export" / "export_short_hand.py"
    spec = importlib.util.spec_from_file_location("export_short_hand", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_pattern_path_uses_current_metadata_and_supports_legacy_fallback():
    export = load_export_module()

    assert export.pattern_path({"_meta": {"path": ["Mind", "Reasoning"]}}) == (
        "Mind",
        "Reasoning",
    )
    assert export.pattern_path({"_meta": {"layer": "Infrastructure", "category": "Security"}}) == (
        "Infrastructure",
        "Security",
    )
    assert export.pattern_path({}) == ("Unclassified",)


def test_pattern_sort_key_orders_by_path_then_handle():
    export = load_export_module()
    patterns = [
        {"handle": "Beta", "_meta": {"path": ["Mind", "Reasoning"]}},
        {"handle": "Alpha", "_meta": {"path": ["Mind", "Reasoning"]}},
        {"handle": "Protocol", "_meta": {"path": ["Infrastructure"]}},
    ]

    assert [p["handle"] for p in sorted(patterns, key=export.pattern_sort_key)] == [
        "Protocol",
        "Alpha",
        "Beta",
    ]


def test_shorten_obj_does_not_rewrite_taxonomy_path():
    export = load_export_module()
    pattern = {"_meta": {"path": ["Mind", "Agent"]}}

    shortened = export.shorten_obj(
        pattern,
        id_lookup={},
        handle_lookup={"Mind": "Mind#1234", "Agent": "Agent#5678"},
        handle_to_short={"Mind": "Mind#1234", "Agent": "Agent#5678"},
    )

    assert shortened["_meta"]["path"] == ["Mind", "Agent"]
