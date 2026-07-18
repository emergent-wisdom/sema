"""Tests for the vocabulary export script."""

import importlib.util
from pathlib import Path


def load_export_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "export" / "export_sema.py"
    spec = importlib.util.spec_from_file_location("export_sema", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_normalize_export_order_keeps_compat_fields_after_dependencies():
    export_sema = load_export_module()
    card = {
        "handle": "Example",
        "mechanism": "Uses {{thing}}.",
        "sema_id": "sema:Example#mh:SHA-256:" + ("a" * 64),
        "sema_ref": "Example#aaaa",
        "sema_stub": "aaaa",
        "sema_layer": "Mind",
        "sema_category": "Reasoning",
        "dependencies": {
            "references": {
                "thing": "sema:Thing#mh:SHA-256:" + ("b" * 64),
            }
        },
    }

    export_sema.normalize_export_order(card)

    assert list(card)[-3:] == ["dependencies", "sema_layer", "sema_category"]


def test_exporter_prioritizes_checkout_source():
    export_sema = load_export_module()
    repo_root = Path(__file__).resolve().parents[4]

    assert Path(export_sema.sys.path[0]).resolve() == repo_root / "src"
    assert Path(export_sema.generate_sema_hash.__code__.co_filename).resolve() == (
        repo_root / "src" / "sema" / "core" / "hashing.py"
    )
