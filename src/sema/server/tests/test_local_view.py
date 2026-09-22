"""The local view shows the vocabulary an agent is working in."""

import shutil
from pathlib import Path

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from sema.core.registry import get_bundled_db_path, set_active_db
from sema.server import api


@pytest.fixture()
def local_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("SEMA_DB_PATH", raising=False)
    saved = (api.DB_PATH, api.registry, api.workspace)
    try:
        yield TestClient(api.app)
    finally:
        api.DB_PATH, api.registry, api.workspace = saved


def _writable_copy(tmp_path: Path, name: str) -> Path:
    bundled = get_bundled_db_path()
    assert bundled is not None
    destination = tmp_path / f"{name}.db"
    shutil.copy(bundled, destination)
    return destination


def test_local_view_follows_the_vocabulary_an_agent_selects(
    local_client: TestClient, tmp_path: Path
):
    mine = _writable_copy(tmp_path, "mine")
    # What `sema use` and the MCP tool `sema_use` do in another process.
    set_active_db(str(mine))

    described = local_client.get("/api/workspace").json()
    assert described["db_path"] == str(mine.resolve())
    assert api.DB_PATH == str(mine.resolve())
    assert local_client.get("/api/graph").json()["nodes"]

    # Switching back to the bundled vocabulary is followed too.
    set_active_db(None)
    assert local_client.get("/api/workspace").json()["db_path"] == get_bundled_db_path()


def test_explicit_db_path_pins_the_local_view(
    local_client: TestClient, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    pinned = api.DB_PATH
    monkeypatch.setenv("SEMA_DB_PATH", pinned)
    set_active_db(str(_writable_copy(tmp_path, "other")))

    local_client.get("/api/workspace")
    assert api.DB_PATH == pinned


def test_a_deleted_active_vocabulary_falls_back_to_the_bundled_one(
    local_client: TestClient, tmp_path: Path
):
    mine = _writable_copy(tmp_path, "mine")
    set_active_db(str(mine))
    local_client.get("/api/workspace")
    mine.unlink()

    assert local_client.get("/api/workspace").json()["db_path"] == get_bundled_db_path()
