import json
import sqlite3

import numpy as np

from sema.core.registry import RegistryManager
from sema.taxonomy_graph import embedding_service
from sema.taxonomy_graph.graph_store import GraphStore


def _search_database(path):
    connection = sqlite3.connect(path)
    connection.execute(
        """
        CREATE TABLE nodes (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            metadata TEXT NOT NULL,
            node_type TEXT NOT NULL,
            embedding BLOB
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE edges (
            id TEXT PRIMARY KEY,
            source_id TEXT,
            target_id TEXT,
            edge_type TEXT,
            alias TEXT
        )
        """
    )
    pattern = {
        "handle": "Alpha",
        "sema_ref": "Alpha#0000",
        "gloss": "First pattern",
        "mechanism": "A test mechanism",
        "sema_category": "Tests",
        "sema_layer": "Mind",
    }
    connection.execute(
        "INSERT INTO nodes (id, text, metadata, node_type, embedding) VALUES (?, ?, ?, ?, ?)",
        (
            "node-alpha",
            "Alpha",
            json.dumps({"pattern": pattern}),
            "PATTERN",
            np.ones(384, dtype=np.float32).tobytes(),
        ),
    )
    connection.commit()
    connection.close()


def test_semantic_search_reuses_service_and_candidates(tmp_path, monkeypatch):
    database = tmp_path / "taxonomy.db"
    _search_database(database)

    class FakeEmbeddingService:
        init_calls = 0
        queries = []

        def __init__(self, db_path):
            self.db_path = db_path
            FakeEmbeddingService.init_calls += 1

        def get_embedding(self, text):
            FakeEmbeddingService.queries.append(text)
            return np.ones(384, dtype=np.float32)

        def find_similar(self, query_embedding, candidates, threshold, top_k):
            assert query_embedding.shape == (384,)
            assert threshold == 0.2
            assert top_k == 20
            return [(candidates[0][0], 0.9)]

    monkeypatch.setattr(embedding_service, "EmbeddingService", FakeEmbeddingService)
    registry = RegistryManager(vocab_dir=tmp_path / "vocabulary", db_path=str(database))

    first = registry.search("first concept", use_semantic=True)

    connection = sqlite3.connect(database)
    connection.execute("UPDATE nodes SET embedding = NULL")
    connection.commit()
    connection.close()

    second = registry.search("second concept", use_semantic=True)

    assert FakeEmbeddingService.init_calls == 1
    assert FakeEmbeddingService.queries == ["first concept", "second concept"]
    assert first[0]["handle"] == "Alpha"
    assert first[0]["sema_ref"] == "Alpha#0000"
    assert second[0]["handle"] == "Alpha"
    assert second[0]["sema_ref"] == "Alpha#0000"


def test_graph_context_keeps_neighbor_cards_compact(tmp_path):
    database = tmp_path / "taxonomy.db"
    store = GraphStore(str(database))
    store.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
    dependency = {
        "handle": "Dependency",
        "gloss": "A reusable dependency",
        "mechanism": "Carries detailed behavior that search context must not duplicate.",
        "invariants": ["The detailed contract remains available through resolve."],
        "_meta": {
            "path": ["Infrastructure", "Primitives"],
            "ring": 0,
            "tier": 1,
        },
    }
    assert store.add_pattern(dependency)["success"] is True
    parent = {
        "handle": "Parent",
        "gloss": "Uses one dependency",
        "mechanism": "Uses {{dependency}} without embedding its full card in search.",
        "dependencies": {"references": {"dependency": dependency["sema_id"]}},
        "_meta": {
            "path": ["Mind", "Reasoning"],
            "ring": 1,
            "tier": 1,
        },
    }
    assert store.add_pattern(parent)["success"] is True

    context = RegistryManager(db_path=str(database)).get_context("Parent")

    assert context["dependencies"] == [
        {
            "handle": "Dependency",
            "sema_ref": dependency["sema_ref"],
            "gloss": "A reusable dependency",
        }
    ]
    assert "mechanism" not in context["dependencies"][0]
    assert "invariants" not in context["dependencies"][0]
