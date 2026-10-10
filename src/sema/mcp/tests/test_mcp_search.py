"""MCP search response-size regression tests."""

from __future__ import annotations

import importlib.util
import json
import unittest

if importlib.util.find_spec("mcp") is None:
    raise unittest.SkipTest("mcp extra is not installed")

from sema.core.registry import RegistryManager, get_bundled_db_path
from sema.mcp import server


def test_broad_search_is_bounded_and_compact(monkeypatch):
    database = get_bundled_db_path()
    assert database is not None
    monkeypatch.setattr(server, "DEFAULT_DB_PATH", database)
    monkeypatch.setattr(server, "REGISTRY_MGR", RegistryManager(db_path=database))
    server._SESSION.reset()

    results = json.loads(server.sema_search("the", limit=500))

    assert len(results) == 20
    assert all("_summary" not in result for result in results[:3])
    assert all(result.get("_summary") is True for result in results[3:])
    assert all("mechanism" not in result for result in results[3:])
    assert len(server._SESSION.served_patterns) == 3


def test_search_inside_a_category(monkeypatch):
    database = get_bundled_db_path()
    assert database is not None
    monkeypatch.setattr(server, "DEFAULT_DB_PATH", database)
    monkeypatch.setattr(server, "REGISTRY_MGR", RegistryManager(db_path=database))
    server._SESSION.reset()

    results = json.loads(server.sema_search("the", limit=20, category="verification"))

    assert results
    assert {r.get("category") for r in results} == {"Verification"}


def test_search_with_an_unknown_category_lists_the_valid_ones(monkeypatch):
    database = get_bundled_db_path()
    assert database is not None
    monkeypatch.setattr(server, "DEFAULT_DB_PATH", database)
    monkeypatch.setattr(server, "REGISTRY_MGR", RegistryManager(db_path=database))
    server._SESSION.reset()

    response = json.loads(server.sema_search("lock", category="Verificaton"))

    assert "Unknown category 'Verificaton'" in response["error"]
    assert "Verification" in response["error"]
