"""Search endpoint response bounds for interactive clients."""

import pytest

pytest.importorskip("fastapi")

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


def test_search_reports_an_unknown_category(monkeypatch):
    class ScopedRegistry:
        def search(self, query, use_semantic=True, *, layer=None, category=None):
            raise ValueError(f"Unknown category '{category}'. Categories: Verification")

    monkeypatch.setattr(api, "registry", ScopedRegistry())

    response = TestClient(api.app).get(
        "/api/search", params={"q": "lock", "category": "Verificaton"}
    )

    assert response.status_code == 400
    assert "Categories: Verification" in response.json()["detail"]


class RankedRegistry:
    def __init__(self, results: list[tuple[str, float, str]]) -> None:
        self._results = results

    def search(self, query, use_semantic=True, **scope):
        return [
            {"handle": handle, "score": score, "source": source, "gloss": ""}
            for handle, score, source in self._results
        ]


def _search(monkeypatch, results, q):
    monkeypatch.setattr(api, "registry", RankedRegistry(results))
    response = TestClient(api.app).get("/api/search", params={"q": q})
    assert response.status_code == 200
    return response.json()


def test_search_keeps_the_registry_score_and_source(monkeypatch):
    body = _search(
        monkeypatch,
        [("Weak", 0.01, "semantic"), ("Closer", 0.19, "semantic")],
        "unrelated words entirely",
    )

    assert [(r["handle"], r["score"], r["source"]) for r in body] == [
        ("Closer", 0.19, "semantic"),
        ("Weak", 0.01, "semantic"),
    ]


def test_search_short_or_single_shared_words_do_not_lift_a_name(monkeypatch):
    body = _search(
        monkeypatch,
        [
            ("Bisect", 0.39, "semantic"),
            ("Build", 0.3, "semantic"),
            ("Analogysnap", 0.25, "semantic"),
        ],
        "binary search for a commit that broke the build",
    )

    assert [r["handle"] for r in body] == ["Bisect", "Build", "Analogysnap"]


def test_search_exact_prefix_and_all_word_names_rank_first(monkeypatch):
    results = [("Lock", 0.9, "keyword"), ("StateLock", 0.4, "keyword")]

    for q in ("statelock", "state lock", "StateLo"):
        assert _search(monkeypatch, results, q)[0]["handle"] == "StateLock"
