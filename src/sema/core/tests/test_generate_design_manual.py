"""Tests for the staging-aware vocabulary design manual."""

import importlib.util
import json
from pathlib import Path


def load_manual_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "generate_design_manual.py"
    spec = importlib.util.spec_from_file_location("generate_design_manual", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_pattern(path, pattern):
    path.write_text(json.dumps(pattern), encoding="utf-8")


def test_load_patterns_overlays_edits_and_includes_new_staging_patterns(tmp_path):
    manual = load_manual_module()
    vocab_dir = tmp_path / "vocabulary"
    staging_dir = tmp_path / "staging"
    vocab_dir.mkdir()
    staging_dir.mkdir()

    write_pattern(
        vocab_dir / "Existing.json",
        {
            "handle": "Existing",
            "mechanism": "Old",
            "sema_id": "sema:Existing#mh:SHA-256:" + ("a" * 64),
            "sema_ref": "Existing#aaaa",
            "sema_stub": "aaaa",
            "_meta": {"path": ["Mind", "Reasoning"]},
        },
    )
    write_pattern(
        staging_dir / "Existing.json",
        {
            "handle": "Existing",
            "mechanism": "Edited",
            "_meta": {"path": ["Mind", "Reasoning"]},
        },
    )
    write_pattern(
        staging_dir / "NewPattern.json",
        {
            "handle": "NewPattern",
            "mechanism": "New",
            "_meta": {"path": ["Infrastructure", "Primitives"]},
        },
    )

    patterns = manual.load_patterns(vocab_dir, staging_dir)

    assert set(patterns) == {"Existing", "NewPattern"}
    assert patterns["Existing"]["mechanism"] == "Edited"
    assert patterns["Existing"]["sema_ref"] == "Existing#aaaa"
    assert "sema_ref" not in patterns["NewPattern"]
    assert manual._pattern_location(patterns["NewPattern"]) == (
        "Infrastructure",
        "Primitives",
    )


def test_render_manual_has_no_wall_clock_content():
    manual = load_manual_module()

    rendered = manual.render_manual({}, {})

    assert "_Generated:" not in rendered
    assert "_Patterns covered: 0" in rendered
