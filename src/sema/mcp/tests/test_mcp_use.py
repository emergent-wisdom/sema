"""Tests for active-vocabulary access information from ``sema_use``."""

from __future__ import annotations

import importlib.util
import json
import unittest

import pytest

if importlib.util.find_spec("mcp") is None:
    raise unittest.SkipTest("mcp extra is not installed")

from sema.core.registry import register_library
from sema.mcp import server
from sema.taxonomy_graph.graph_store import GraphStore


@pytest.fixture
def isolated_config(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    return tmp_path


def _empty_database(path):
    store = GraphStore(str(path))
    if hasattr(store, "conn"):
        store.conn.close()


def test_current_local_database_reports_writable_state(isolated_config, monkeypatch):
    database = isolated_config / "project.db"
    _empty_database(database)
    monkeypatch.setattr(server, "DEFAULT_DB_PATH", str(database))
    monkeypatch.setattr(server, "REGISTRY_MGR", server.RegistryManager(db_path=str(database)))

    result = json.loads(server.sema_use())

    assert result["bundled"] is False
    assert result["read_only"] is False
    assert result["writable"] is True


def test_installed_library_reports_read_only_state(isolated_config, monkeypatch):
    database = isolated_config / "installed.db"
    _empty_database(database)
    register_library(
        {
            "name": "example-library",
            "version": "1.0.0",
            "catalog_root": "a" * 64,
            "path": str(database),
        }
    )
    monkeypatch.setattr(server, "DEFAULT_DB_PATH", str(database))
    monkeypatch.setattr(server, "REGISTRY_MGR", server.RegistryManager(db_path=str(database)))

    result = json.loads(server.sema_use())

    assert result["bundled"] is False
    assert result["read_only"] is True
    assert result["writable"] is False
    assert result["kind"] == "installed-library"
