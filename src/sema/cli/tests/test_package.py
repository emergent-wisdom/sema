"""CLI coverage for producing portable third-party library releases."""

import json
import sys
from pathlib import Path

import pytest

from sema.cli.main import main
from sema.taxonomy_graph.graph_store import GraphStore


def _project_database(path: Path) -> Path:
    store = GraphStore(str(path), enable_embeddings=False)
    pattern = {
        "handle": "DeFiGuard",
        "mechanism": "Checks a proposed DeFi action against its declared guard conditions.",
        "gloss": "Guard a DeFi action",
        "invariants": ["Every accepted action satisfies its declared guard conditions."],
        "_meta": {
            "path": ["Society", "Economics"],
            "ring": 1,
            "tier": 1,
        },
    }
    assert store.add_pattern(pattern)["success"] is True
    del store
    return path


def test_package_command_builds_github_release_assets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source = _project_database(tmp_path / "defi.db")
    output = tmp_path / "release"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "sema",
            "package",
            str(source),
            "--name",
            "defi",
            "--version",
            "1.0.0",
            "--output-dir",
            str(output),
            "--github-repo",
            "acme/sema-defi",
        ],
    )

    main()

    manifest = json.loads((output / "library.json").read_text())
    assert manifest["update_url"] == (
        "https://github.com/acme/sema-defi/releases/latest/download/library.json"
    )
    assert manifest["patterns"]["url"] == (
        "https://github.com/acme/sema-defi/releases/download/v1.0.0/defi-patterns-1.0.0.zip"
    )
    assert (output / "defi-patterns-1.0.0.zip").is_file()
    assert "verified a fresh local read model" in capsys.readouterr().out


def test_package_command_requires_complete_explicit_url_pair(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _project_database(tmp_path / "defi.db")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "sema",
            "package",
            str(source),
            "--name",
            "defi",
            "--version",
            "1.0.0",
            "--output-dir",
            str(tmp_path / "release"),
            "--update-url",
            "https://example.test/releases/latest/download/library.json",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1


def test_package_managed_library_explains_how_to_make_its_writable_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source = _project_database(tmp_path / "managed.db")
    record = {
        "name": "defi",
        "path": str(source),
        "kind": "installed-library",
        "version": "1.0.0",
    }
    monkeypatch.setattr("sema.cli.main.get_registered_db_by_path", lambda _path: record)
    monkeypatch.setattr("sema.cli.main.is_read_only_db", lambda _path: True)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "sema",
            "package",
            str(source),
            "--name",
            "defi",
            "--version",
            "1.0.0",
            "--output-dir",
            str(tmp_path / "release"),
            "--github-repo",
            "acme/sema-defi",
        ],
    )

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    assert "--source defi" in capsys.readouterr().out
