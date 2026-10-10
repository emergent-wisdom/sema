"""Search restricted to a layer or category."""

import json
import sqlite3

import numpy as np
import pytest

from sema.core.registry import RegistryManager
from sema.taxonomy_graph import embedding_service

PATTERNS = [
    ("LockA", "Infrastructure", "Primitives", "a lock for shared state"),
    ("LockB", "Mind", "Strategy", "a lock on a decision until review"),
    ("Plan", "Mind", "Strategy", "a plan with steps"),
    ("Measure", "Physics", "Primitives", "a measurement of state"),
]


def _database(path):
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE nodes (id TEXT PRIMARY KEY, text TEXT NOT NULL, metadata TEXT NOT NULL,"
        " node_type TEXT NOT NULL, embedding BLOB)"
    )
    connection.execute(
        "CREATE TABLE edges (id TEXT PRIMARY KEY, source_id TEXT, target_id TEXT,"
        " edge_type TEXT, alias TEXT)"
    )
    for handle, layer, category, gloss in PATTERNS:
        pattern = {
            "handle": handle,
            "sema_ref": f"{handle}#0000",
            "gloss": gloss,
            "mechanism": "",
            "sema_layer": layer,
            "sema_category": category,
        }
        connection.execute(
            "INSERT INTO nodes VALUES (?, ?, ?, 'PATTERN', ?)",
            (
                f"node-{handle}",
                handle,
                json.dumps({"pattern": pattern}),
                np.ones(384, dtype=np.float32).tobytes(),
            ),
        )
    connection.commit()
    connection.close()


@pytest.fixture
def registry(tmp_path):
    database = tmp_path / "taxonomy.db"
    _database(database)
    return RegistryManager(vocab_dir=tmp_path / "vocabulary", db_path=str(database))


def _handles(results):
    return sorted(r["handle"] for r in results)


def test_category_restricts_keyword_matches(registry):
    assert _handles(registry.search("lock", use_semantic=False)) == ["LockA", "LockB"]
    assert _handles(registry.search("lock", use_semantic=False, category="strategy")) == ["LockB"]


def test_layer_and_category_combine(registry):
    results = registry.search("a", use_semantic=False, layer="Physics", category="Primitives")
    assert _handles(results) == ["Measure"]


def test_semantic_pass_only_ranks_patterns_in_scope(registry, monkeypatch):
    seen = []

    class FakeEmbeddingService:
        def __init__(self, db_path):
            pass

        def get_embedding(self, text):
            return np.ones(384, dtype=np.float32)

        def find_similar(self, query_embedding, candidates, threshold, top_k):
            seen.append((sorted(node_id for node_id, _vec in candidates), threshold))
            return [(node_id, 0.1) for node_id, _vec in candidates]

    monkeypatch.setattr(embedding_service, "EmbeddingService", FakeEmbeddingService)

    results = registry.search("anything", use_semantic=True, layer="mind")

    # Only the layer's patterns are ranked, and weak matches are kept.
    assert seen == [(["node-LockB", "node-Plan"], 0.0)]
    assert _handles(results) == ["LockB", "Plan"]


def test_unknown_category_names_the_valid_ones(registry):
    with pytest.raises(ValueError, match="Categories: Primitives, Strategy"):
        registry.search("lock", use_semantic=False, category="Strategi")


def test_category_outside_the_layer_names_that_layers_categories(registry):
    with pytest.raises(ValueError, match="in layer 'Physics'. Categories: Primitives$"):
        registry.search("lock", use_semantic=False, layer="Physics", category="Strategy")


def test_unknown_layer_names_the_valid_layers(registry):
    with pytest.raises(ValueError, match="Layers: Infrastructure, Mind, Physics"):
        registry.search("lock", use_semantic=False, layer="Minds")
