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
