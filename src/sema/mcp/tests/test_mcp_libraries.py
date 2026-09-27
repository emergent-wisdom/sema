"""Search, install, and publish published libraries from an agent's chat."""

from __future__ import annotations

import importlib.util
import json
import unittest

import httpx
import pytest

if importlib.util.find_spec("mcp") is None:
    raise unittest.SkipTest("mcp extra is not installed")

from sema.cli import registry_client as rc
from sema.core import libraries
from sema.mcp import server

REGISTRY = "https://registry.test"
MANIFEST = "https://github.com/alice/reasoning/releases/latest/download/library.json"
KEY = "sema_" + "k" * 43
ROW = {
    "slug": "reasoning",
    "library_id": "reasoning",
    "version": "0.1.0",
    "owner": "alice",
    "repo": "reasoning",
    "pattern_count": 3,
    "root": "8cc3" * 16,
    "license": "CC-BY-4.0",
    "manifest_url": MANIFEST,
}


def _handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    authorized = request.headers.get("authorization") == f"Bearer {KEY}"
    if path == "/api/vocabularies":
        return httpx.Response(200, json=[ROW])
    if path == "/api/vocabularies/reasoning":
        return httpx.Response(200, json={"record": ROW})
    if path == "/api/me" and authorized:
        return httpx.Response(
            200,
            json={
                "authenticated": True,
                "user": {"login": "alice"},
                "token_id": "tok_0011223344556677",
            },
        )
    if path == "/api/registry/import" and authorized:
        assert json.loads(request.content) == {"manifest_url": MANIFEST}
        return httpx.Response(200, json={"operation": "created", "record": ROW})
    if path in {"/api/me", "/api/registry/import"}:
        return httpx.Response(401, json={"detail": "Invalid or revoked API token"})
    return httpx.Response(404, json={"detail": "Vocabulary not found"})


@pytest.fixture
def fake_registry(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv(rc.REGISTRY_ENV, REGISTRY)
    monkeypatch.delenv(rc.TOKEN_ENV, raising=False)
    monkeypatch.setattr(
        rc, "_client", lambda _timeout: httpx.Client(transport=httpx.MockTransport(_handler))
    )


def test_an_agent_finds_and_installs_a_library_by_name(fake_registry, monkeypatch):
    installed: list[str] = []

    def fake_install(source, expected=None):
        installed.append(source)
        assert expected is not None and expected.semantic_root == ROW["root"]
        assert expected.registry_url == REGISTRY
        return {
            "name": "reasoning",
            "version": "0.1.0",
            "pattern_count": 3,
            "semantic_root": ROW["root"],
            "catalog_root": "9a9c" * 16,
        }

    monkeypatch.setattr(libraries, "install_library", fake_install)

    found = json.loads(server.sema_library_search("reason"))
    assert [row["slug"] for row in found["libraries"]] == ["reasoning"]
    assert found["libraries"][0]["manifest_url"] == MANIFEST

    result = json.loads(server.sema_library_install("reasoning"))
    assert result["success"] is True
    assert installed == [MANIFEST]
    assert "sema_use(db_path='reasoning')" in result["next"]

    missing = json.loads(server.sema_library_install("nothing-here"))
    assert "No published library named nothing-here" in missing["error"]


def test_publishing_needs_a_key_and_says_how_to_get_one(fake_registry):
    refused = json.loads(server.sema_library_publish(MANIFEST))
    assert "sema_library_login" in refused["error"]
    assert refused["error"].count("sema login") == 1

    rejected = json.loads(server.sema_library_login("sema_" + "x" * 43))
    assert "did not accept the key" in rejected["error"]

    accepted = json.loads(server.sema_library_login(KEY))
    assert accepted == {"success": True, "registry": REGISTRY, "account": "alice"}

    published = json.loads(server.sema_library_publish(MANIFEST))
    assert published["success"] is True
    assert published["page"] == f"{REGISTRY}/vocabularies/reasoning"


def test_an_agent_is_told_when_the_publisher_serves_a_different_release(fake_registry, monkeypatch):
    def swapped_install(source, expected=None):
        raise libraries.ReleaseMismatchError(
            "The release on offer is not the one the registry verified: it has a different "
            "semantic root"
        )

    monkeypatch.setattr(libraries, "install_library", swapped_install)

    refused = json.loads(server.sema_library_install("reasoning"))
    assert "refused" in refused["error"]
    assert "Nothing was installed" in refused["error"]
    assert MANIFEST in refused["error"]
    assert "Ask the user" in refused["error"]
