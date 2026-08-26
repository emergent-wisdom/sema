"""Search endpoint response bounds for interactive clients."""

from fastapi.testclient import TestClient

from sema.server import api


class StubRegistry:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bool]] = []

    def search(self, query: str, use_semantic: bool = True) -> list[dict]:
        self.calls.append((query, use_semantic))
        return [
            {
                "handle": f"Pattern{index}#0000",
                "gloss": "",
                "mechanism": "",
                "category": "",
                "layer": "",
                "sema_ref": f"Pattern{index}#0000",
                "source": "keyword",
                "score": 1.0,
            }
            for index in range(12)
        ]


def test_search_honors_result_limit(monkeypatch):
    registry = StubRegistry()
    monkeypatch.setattr(api, "registry", registry)

    response = TestClient(api.app).get(
        "/api/search",
        params={"q": "pattern", "semantic": "false", "limit": 8},
    )

    assert response.status_code == 200
    assert len(response.json()) == 8
    assert registry.calls == [("pattern", False)]


def test_search_clamps_non_positive_limit(monkeypatch):
    registry = StubRegistry()
    monkeypatch.setattr(api, "registry", registry)

    response = TestClient(api.app).get(
        "/api/search",
        params={"q": "pattern", "semantic": "false", "limit": 0},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
