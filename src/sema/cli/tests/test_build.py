"""Selective database-build regression tests."""

import stat
from pathlib import Path
from unittest.mock import patch

import numpy as np

from sema.cli.main import build_db
from sema.core.registry import RegistryManager
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


def test_standard_preset_only_references_default_vocabulary():
    repo_root = Path(__file__).resolve().parents[4]
    preset_path = repo_root / "data" / "presets" / "standard.txt"
    database_path = repo_root / "data" / "taxonomy.db"

    requested = {
        line.strip()
        for line in preset_path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    available = RegistryManager(db_path=str(database_path)).registry

    missing = sorted(requested - available.keys())
    assert missing == [], f"standard preset references missing patterns: {missing}"


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


def test_full_build_resolves_and_verifies_installed_library_name(tmp_path):
    source_db = tmp_path / "managed.db"
    destination_db = tmp_path / "project.db"
    source = GraphStore(str(source_db))
    source.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
    assert source.add_pattern(_card("DomainPattern"))["success"] is True
    source_db.chmod(0o444)

    record = {
        "name": "defi",
        "path": str(source_db),
        "kind": "installed-library",
        "version": "1.0.0",
    }
    with (
        patch("sema.cli.main.get_registered_db", return_value=record),
        patch("sema.core.libraries.verify_installed_library") as verify,
        patch("sema.cli.main.register_db") as register_db,
    ):
        assert build_db(str(destination_db), preset="full", source_db="defi") is True

    verify.assert_called_once_with(record)
    register_db.assert_called_once_with(str(destination_db.resolve()))
    assert destination_db.stat().st_mode & stat.S_IWUSR
    assert RegistryManager(db_path=str(destination_db)).count() == 1


def test_full_build_preserves_database_path_source(tmp_path):
    source_db = tmp_path / "source.db"
    destination_db = tmp_path / "project.db"
    source = GraphStore(str(source_db))
    source.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
    assert source.add_pattern(_card("PathPattern"))["success"] is True

    with (
        patch("sema.cli.main.get_registered_db", return_value=None) as resolve_name,
        patch("sema.cli.main.register_db"),
    ):
        assert build_db(str(destination_db), preset="full", source_db=str(source_db)) is True

    resolve_name.assert_called_once_with(str(source_db))
    assert RegistryManager(db_path=str(destination_db)).count() == 1


def test_full_build_reverifies_managed_source_selected_by_path(tmp_path):
    source_db = tmp_path / "managed.db"
    destination_db = tmp_path / "project.db"
    source = GraphStore(str(source_db))
    source.embedding_service.get_embedding = lambda _text: np.zeros(384, dtype=np.float32)
    assert source.add_pattern(_card("DomainPattern"))["success"] is True
    record = {
        "name": "defi",
        "path": str(source_db),
        "kind": "installed-library",
        "version": "1.0.0",
    }

    with (
        patch("sema.cli.main.get_registered_db", return_value=None),
        patch("sema.cli.main.get_registered_db_by_path", return_value=record) as resolve_path,
        patch("sema.core.libraries.verify_installed_library") as verify,
        patch("sema.cli.main.register_db"),
    ):
        assert build_db(str(destination_db), preset="full", source_db=str(source_db)) is True

    resolve_path.assert_called_once_with(source_db)
    verify.assert_called_once_with(record)
