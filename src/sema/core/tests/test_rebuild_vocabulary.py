"""Tests for deterministic vocabulary rebuild helpers."""

import importlib.util
import os
from pathlib import Path


def load_rebuild_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "rebuild_vocabulary.py"
    spec = importlib.util.spec_from_file_location("rebuild_vocabulary", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_changed_vocabulary_files_compares_with_pre_rebuild_snapshot(tmp_path):
    rebuild = load_rebuild_module()
    (tmp_path / "Alpha.json").write_text('{"handle":"Alpha"}')
    (tmp_path / "Beta.json").write_text('{"handle":"Beta"}')
    before = rebuild.snapshot_vocabulary(tmp_path)

    assert rebuild.changed_vocabulary_files(before, tmp_path) == []

    (tmp_path / "Alpha.json").write_text('{"handle":"Alpha","gloss":"changed"}')
    (tmp_path / "Beta.json").unlink()
    (tmp_path / "Gamma.json").write_text('{"handle":"Gamma"}')

    assert rebuild.changed_vocabulary_files(before, tmp_path) == [
        "Alpha.json",
        "Beta.json",
        "Gamma.json",
    ]


def test_isolated_registry_environment_replaces_home_without_losing_environment(tmp_path):
    rebuild = load_rebuild_module()

    env = rebuild.isolated_registry_environment(str(tmp_path))

    assert env["HOME"] == str(tmp_path)
    assert all(env.get(key) == value for key, value in os.environ.items() if key != "HOME")
