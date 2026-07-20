"""CLI contract tests for ``sema check``."""

import io
import sys

import pytest

from sema.cli.main import check_refs_stdin


def test_missing_registry_exits_one(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", io.StringIO("StateLock#0000"))

    with pytest.raises(SystemExit) as exc_info:
        check_refs_stdin(str(tmp_path / "missing.db"), as_json=False)

    assert exc_info.value.code == 1
    assert "registry unavailable" in capsys.readouterr().err
