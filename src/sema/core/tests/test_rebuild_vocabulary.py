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


def test_replace_is_honoured_only_when_there_is_a_rebuild_to_keep():
    """Regression: --replace on a failed rebuild kept an empty DB and deleted the backup.

    The next export then wrote zero patterns over data/vocabulary/, and a verify
    run afterwards overwrote the fixed-name backup, so the good database was gone.
    """
    rebuild = load_rebuild_module()

    keep, message = rebuild.restore_plan(replace=True, rebuild_succeeded=True, check_only_run=False)
    assert keep is True
    assert "Kept rebuilt DB" in message

    keep, message = rebuild.restore_plan(
        replace=True, rebuild_succeeded=False, check_only_run=False
    )
    assert keep is False
    assert "rebuild failed" in message

    # --check applies nothing, so the fresh DB is empty whatever --replace says.
    keep, message = rebuild.restore_plan(replace=True, rebuild_succeeded=False, check_only_run=True)
    assert keep is False
    assert "--check applies nothing" in message

    keep, message = rebuild.restore_plan(
        replace=False, rebuild_succeeded=True, check_only_run=False
    )
    assert keep is False
    assert message == "Restored original DB"


def test_backup_path_is_unique_per_run(tmp_path):
    """A fixed backup name let a later run destroy an earlier run's only backup."""
    rebuild = load_rebuild_module()
    db = str(tmp_path / "taxonomy.db")

    first = rebuild.backup_path_for(db, stamp="20260725-120000")
    second = rebuild.backup_path_for(db, stamp="20260725-120500")

    assert first != second
    assert first.startswith(db)
    assert not first.endswith(".rebuild_bak")


def test_hash_drift_keeps_the_rebuilt_database():
    """Regression: restoring on drift discarded the correction and caused an infinite loop.

    Hash drift means the stored hashes were stale — typically a dependency changed
    and its dependents were never rehashed — and the rebuild has just corrected them
    in place. The database it built is therefore the better copy. Restoring the
    backup threw that away, and a caller that re-exported afterwards wrote the stale
    hashes back, so the next rebuild found the same files again. Observed looping on
    a 207-dependent cascade from Trace.
    """
    rebuild = load_rebuild_module()

    # apply completed, hashes moved: keep it.
    keep, message = rebuild.restore_plan(
        replace=True, rebuild_succeeded=False, check_only_run=False, db_valid=True
    )
    assert keep is True
    assert "corrected, not lost" in message

    # apply itself failed, so there is no valid database: restore.
    keep, message = rebuild.restore_plan(
        replace=True, rebuild_succeeded=False, check_only_run=False, db_valid=False
    )
    assert keep is False
    assert "rebuild failed" in message

    # --check applies nothing, so the fresh database is empty whatever else is true.
    keep, _ = rebuild.restore_plan(
        replace=True, rebuild_succeeded=False, check_only_run=True, db_valid=True
    )
    assert keep is False

    # without --replace the caller asked for a dry run: restore regardless.
    keep, _ = rebuild.restore_plan(
        replace=False, rebuild_succeeded=True, check_only_run=False, db_valid=True
    )
    assert keep is False
