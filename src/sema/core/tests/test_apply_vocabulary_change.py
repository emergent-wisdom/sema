"""Tests for the canonical vocabulary apply workflow."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def load_workflow_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "apply_vocabulary_change.py"
    spec = importlib.util.spec_from_file_location("apply_vocabulary_change", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_workflow_environment_overrides_active_database(monkeypatch):
    workflow = load_workflow_module()
    monkeypatch.setenv("SEMA_DB_PATH", "/tmp/other-taxonomy.db")

    env = workflow.workflow_environment()

    assert env["SEMA_DB_PATH"] == str(workflow.REPO_DB)


def test_workflow_environment_prefers_current_checkout_source(monkeypatch):
    workflow = load_workflow_module()
    monkeypatch.setenv("PYTHONPATH", "/tmp/other-checkout/src")

    env = workflow.workflow_environment()

    assert env["PYTHONPATH"].split(workflow.os.pathsep) == [
        str(workflow.REPO_SRC),
        "/tmp/other-checkout/src",
    ]


def test_step_passes_pinned_database_to_subprocess(monkeypatch):
    workflow = load_workflow_module()
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured.update(kwargs)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(workflow.subprocess, "run", fake_run)

    workflow.step("fixture", ["sema", "apply"])

    assert captured["cwd"] == workflow.REPO_ROOT
    assert captured["env"]["SEMA_DB_PATH"] == str(workflow.REPO_DB)
    assert captured["env"]["PYTHONPATH"].split(workflow.os.pathsep)[0] == str(workflow.REPO_SRC)


def test_check_forwards_retarget_extends(monkeypatch, tmp_path):
    workflow = load_workflow_module()
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "Child.json").write_text("{}")
    commands = []

    def fake_step(label, command, allow_drift=False):
        commands.append((label, command, allow_drift))
        return ""

    monkeypatch.setattr(workflow, "step", fake_step)
    monkeypatch.setattr(workflow, "python_executable", lambda: "python")
    monkeypatch.setattr(
        workflow.sys,
        "argv",
        [
            "apply_vocabulary_change.py",
            "--staging",
            str(staging),
            "--check",
            "--retarget-extends",
        ],
    )

    assert workflow.main() == 0
    assert len(commands) == 1
    assert commands[0][0] == "validate"
    assert "--check" in commands[0][1]
    assert "--retarget-extends" in commands[0][1]


def test_apply_forwards_retarget_extends_to_validation_and_mutation(monkeypatch, tmp_path):
    workflow = load_workflow_module()
    staging = tmp_path / "staging"
    staging.mkdir()
    (staging / "Child.json").write_text("{}")
    commands = []

    def fake_step(label, command, allow_drift=False):
        commands.append((label, command, allow_drift))
        return ""

    monkeypatch.setattr(workflow, "step", fake_step)
    monkeypatch.setattr(workflow, "python_executable", lambda: "python")
    monkeypatch.setattr(
        workflow.sys,
        "argv",
        [
            "apply_vocabulary_change.py",
            "--staging",
            str(staging),
            "--keep-staging",
            "--retarget-extends",
        ],
    )

    assert workflow.main() == 0
    validate = next(command for label, command, _ in commands if label == "validate")
    apply = next(command for label, command, _ in commands if label == "apply to database")
    assert "--retarget-extends" in validate
    assert "--retarget-extends" in apply
