import importlib
import os
import sys
from types import SimpleNamespace

from sema.audit import runner


def test_audit_modules_are_importable():
    for module, _title in runner.AUDITS:
        assert importlib.import_module(module)
    assert importlib.import_module("sema.audit.redundancy")
    assert importlib.import_module("sema.audit.speakability")


def test_run_audit_uses_module_entrypoint_without_pythonpath_mutation(monkeypatch):
    captured = {}
    original_pythonpath = os.environ.get("PYTHONPATH")

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured.update(kwargs)
        return SimpleNamespace(returncode=0, stdout="stdout\n", stderr="stderr\n")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    rc, output = runner.run_audit("sema.audit.hash_validity")

    assert rc == 0
    assert output == "stdout\nstderr"
    assert captured["command"] == [sys.executable, "-m", "sema.audit.hash_validity"]
    assert captured["cwd"] == runner.REPO_ROOT
    assert captured["env"].get("PYTHONPATH") == original_pythonpath
    assert captured["env"]["SEMA_DB_PATH"] == str(runner.REPO_ROOT / "data" / "taxonomy.db")


def test_main_writes_module_sources(monkeypatch, tmp_path):
    output = tmp_path / "audit.md"
    monkeypatch.setattr(runner, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(runner, "OUTPUT", output)
    monkeypatch.setattr(runner, "AUDITS", [("sema.audit.example", "Example audit")])
    monkeypatch.setattr(runner, "run_audit", lambda _module: (0, "all good"))

    runner.main()

    report = output.read_text()
    assert "Source: `sema.audit.example` (ok)" in report
    assert "all good" in report
