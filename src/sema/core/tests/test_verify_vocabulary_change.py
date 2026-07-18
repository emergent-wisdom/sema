"""Tests for the canonical vocabulary verification workflow."""

import importlib.util
from pathlib import Path


def load_workflow_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "verify_vocabulary_change.py"
    spec = importlib.util.spec_from_file_location("verify_vocabulary_change", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_check_reports_drift_and_restores_original(tmp_path):
    workflow = load_workflow_module()
    output = tmp_path / "generated.md"
    output.write_text("old")
    step = workflow.Step("fixture", ("generate",), (output,))

    def runner(_step):
        output.write_text("new")
        return 0

    failure = workflow.verify_generated_step(step, runner)

    assert failure == f"fixture is stale: {output}"
    assert output.read_text() == "old"


def test_workflow_environment_targets_repo_database_and_writable_cache(monkeypatch):
    workflow = load_workflow_module()
    monkeypatch.delenv("SEMA_CACHE_DIR", raising=False)

    env = workflow.workflow_environment()

    assert env["SEMA_DB_PATH"] == str(workflow.REPO_ROOT / "data" / "taxonomy.db")
    assert env["SEMA_CACHE_DIR"].endswith("sema-cache")


def test_generated_refresh_keeps_updated_output(tmp_path):
    workflow = load_workflow_module()
    output = tmp_path / "generated.md"
    output.write_text("old")
    step = workflow.Step("fixture", ("generate",), (output,))

    def runner(_step):
        output.write_text("new")
        return 0

    assert workflow.refresh_generated_step(step, runner) is None
    assert output.read_text() == "new"


def test_rebuild_check_restores_changed_and_added_vocabulary_files(tmp_path, monkeypatch):
    workflow = load_workflow_module()
    vocab_dir = tmp_path / "vocabulary"
    vocab_dir.mkdir()
    original = vocab_dir / "Alpha.json"
    original.write_text("alpha")
    archived = vocab_dir / "experimental" / "Archived.json"
    archived.parent.mkdir()
    archived.write_text("archived")
    monkeypatch.setattr(workflow, "VOCAB_DIR", vocab_dir)

    def runner(_step):
        original.write_text("changed")
        archived.write_text("changed archive")
        (vocab_dir / "Beta.json").write_text("added")
        return 1

    failure = workflow.verify_rebuild(runner)

    assert failure == "deterministic vocabulary rebuild exited with status 1"
    assert original.read_text() == "alpha"
    assert archived.read_text() == "archived"
    assert not (vocab_dir / "Beta.json").exists()


def test_workflow_runs_every_gate_and_collects_failures(monkeypatch):
    workflow = load_workflow_module()
    seen = []

    monkeypatch.setattr(workflow, "GENERATED_STEPS", ())
    monkeypatch.setattr(workflow, "snapshot_vocabulary", lambda: {})

    def runner(step):
        seen.append(step.name)
        return 1 if step is workflow.DOC_REFS_CHECK else 0

    failures = workflow.run_workflow(refresh=False, runner=runner)

    assert seen == [
        "database/export parity",
        "documentation hash references",
        "exported hash validity",
        "deterministic vocabulary rebuild",
    ]
    assert failures == ["documentation hash reference check failed"]
