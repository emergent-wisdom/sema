import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from sema.core.workspace import GraphWorkspace, WorkspaceCatalog, WorkspaceSource
from sema.server import api


class TenantRegistry:
    source = "stub"

    def __init__(self, handle: str, hash_char: str):
        self.db_path = f"/private/{handle.lower()}.db"
        self.vocab_dir = f"/private/{handle.lower()}"
        self.registry = {
            handle: {
                "handle": handle,
                "gloss": f"{handle} gloss",
                "sema_id": f"sema:{handle}#mh:SHA-256:" + (hash_char * 64),
                "sema_ref": f"{handle}#{hash_char * 4}",
                "sema_stub": hash_char * 4,
                "sema_layer": "Mind",
                "sema_category": "Reasoning",
            }
        }

    def refresh(self):
        pass

    def search(self, query, use_semantic=True):
        return list(self.registry.values())

    def get_pattern(self, handle):
        return self.registry.get(handle)

    def resolve(self, handle, depth=1):
        pattern = self.registry.get(handle)
        return {handle: pattern} if pattern else None


def make_catalog():
    catalog = WorkspaceCatalog()
    catalog.register_workspace(
        GraphWorkspace(
            WorkspaceSource(
                workspace_id="team-a",
                label="Team A",
                owner="acme",
                repo="alpha-vocab",
                ref="main",
                metadata={"github_installation_id": 123},
            ),
            registry_manager=TenantRegistry("Alpha", "a"),
        )
    )
    catalog.register_workspace(
        GraphWorkspace(
            WorkspaceSource(
                workspace_id="team-b",
                label="Team B",
                owner="beta",
                repo="beta-vocab",
                ref="stable",
            ),
            registry_manager=TenantRegistry("Beta", "b"),
        )
    )
    return catalog


def test_hosted_workspace_description_hides_internal_fields(monkeypatch):
    monkeypatch.setattr(api, "workspace_catalog", make_catalog())

    response = TestClient(api.app).get("/api/workspaces/team-a")

    assert response.status_code == 200
    assert response.json()["workspace_id"] == "team-a"
    assert response.json()["repo"] == "alpha-vocab"
    assert "db_path" not in response.json()
    assert "vocab_dir" not in response.json()
    assert "metadata" not in response.json()


def test_hosted_workspace_reads_are_tenant_scoped(monkeypatch):
    monkeypatch.setattr(api, "workspace_catalog", make_catalog())
    client = TestClient(api.app)

    team_a = client.get("/api/workspaces/team-a/search", params={"q": "pattern"})
    team_b = client.get("/api/workspaces/team-b/search", params={"q": "pattern"})

    assert team_a.status_code == 200
    assert team_b.status_code == 200
    assert [item["handle"] for item in team_a.json()] == ["Alpha"]
    assert [item["handle"] for item in team_b.json()] == ["Beta"]


def test_hosted_workspace_pattern_resolve_and_root(monkeypatch):
    monkeypatch.setattr(api, "workspace_catalog", make_catalog())
    client = TestClient(api.app)

    pattern = client.get("/api/workspaces/team-a/patterns/Alpha")
    resolved = client.get("/api/workspaces/team-a/resolve/Alpha")
    root = client.get("/api/workspaces/team-a/root")

    assert pattern.status_code == 200
    assert pattern.json()["handle"] == "Alpha"
    assert resolved.status_code == 200
    assert resolved.json()["count"] == 1
    assert root.status_code == 200
    assert root.json()["pattern_count"] == 1
    assert "db_path" not in root.json()


def test_hosted_workspace_returns_404_without_cross_tenant_fallback(monkeypatch):
    monkeypatch.setattr(api, "workspace_catalog", make_catalog())
    client = TestClient(api.app)

    missing_workspace = client.get("/api/workspaces/missing/search", params={"q": "Alpha"})
    wrong_tenant = client.get("/api/workspaces/team-b/patterns/Alpha")

    assert missing_workspace.status_code == 404
    assert wrong_tenant.status_code == 404
