"""Selective database-build regression tests."""

from unittest.mock import patch

import numpy as np

from sema.cli.main import build_db
from sema.taxonomy_graph.graph_store import EdgeType, GraphStore, NodeType


def _card(handle: str, *, extends: str | None = None) -> dict:
    pattern = {
        "handle": handle,
        "mechanism": f"Mechanism for {handle}",
        "gloss": f"Gloss for {handle}",
        "_meta": {
            "path": ["Infrastructure", "Primitives"],
            "ring": 0,
            "tier": 1,
        },
    }
    if extends:
        pattern["extends"] = extends
    return pattern


def test_selective_build_includes_exact_extends_parent_and_is_a_edge(tmp_path):
    source_db = tmp_path / "source.db"
    destination_db = tmp_path / "selected.db"
    selection_file = tmp_path / "patterns.txt"
    source = GraphStore(str(source_db))
    source.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)

    parent = _card("Parent")
    assert source.add_pattern(parent)["success"] is True
    parent_sema_id = parent["sema_id"]
    child = _card("Child", extends=parent_sema_id)
    assert source.add_pattern(child)["success"] is True
    selection_file.write_text("Child\n")

    with patch("sema.cli.main.register_db") as register_db:
        assert (
            build_db(
                str(destination_db),
                patterns_file=str(selection_file),
                source_db=str(source_db),
            )
            is True
        )

    register_db.assert_called_once_with(str(destination_db.resolve()))
    built = GraphStore(str(destination_db))
    handles = {
        data["text"]
        for _node_id, data in built.get_nodes_by_type(NodeType.PATTERN)
        if data.get("text")
    }
    assert handles == {"Parent", "Child"}

    parent_id = built._find_pattern_id("Parent")
    child_id = built._find_pattern_id("Child")
    built_parent = built.graph.nodes[parent_id]["metadata"]["pattern"]
    built_child = built.graph.nodes[child_id]["metadata"]["pattern"]
    assert built_parent["sema_id"] == parent_sema_id
    assert built_child["extends"] == parent_sema_id

    is_a_edges = [
        edge
        for edge in built._edges_between(child_id, parent_id)
        if edge.get("edge_type") == EdgeType.IS_A
    ]
    assert len(is_a_edges) == 1
    assert is_a_edges[0]["metadata"] == {
        "parent_sema_id": parent_sema_id,
        "source_field": "extends",
    }
