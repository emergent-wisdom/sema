"""Executable contract for reconstructing one vocabulary release from another.

These tests compare cryptographic roots, logical pattern exports, and both the
pattern-relation graph and complete normalized read model. SQLite files contain
incidental row IDs and are not themselves a release identity.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np

from sema.cli.main import apply_changes
from sema.core.hashing import vocabulary_info
from sema.taxonomy_graph.graph_store import GraphStore, NodeType


def _reference(handle: str) -> str:
    """Return a schema-valid placeholder; GraphStore resolves the live hash."""
    return f"sema:{handle}#mh:SHA-256:{'0' * 64}"


def _pattern(
    handle: str,
    mechanism: str,
    *,
    dependency: str | None = None,
    caution: str | None = None,
    path: list[str] | None = None,
    invariants: list[str] | None = None,
) -> dict:
    meta: dict = {
        "path": path or ["Infrastructure", "Primitives"],
        "ring": 0,
        "tier": 1,
    }
    if caution is not None:
        meta["caution"] = caution

    pattern = {
        "handle": handle,
        "mechanism": mechanism,
        "gloss": "A synthetic definition used by the delta reconstruction contract.",
        "_meta": meta,
    }
    if dependency is not None:
        pattern["dependencies"] = {"references": {dependency.lower(): _reference(dependency)}}
    if invariants is not None:
        pattern["invariants"] = invariants
    return pattern


def _v1_patterns() -> dict[str, dict]:
    return {
        "Anchor": _pattern("Anchor", "Provide the first anchor definition."),
        "Relay": _pattern("Relay", "Use {{anchor}} to relay a result.", dependency="Anchor"),
        "MetadataCard": _pattern(
            "MetadataCard",
            "Keep this semantic definition stable.",
            caution="Review note from release one.",
            path=["Physics", "Time"],
        ),
        "Retired": _pattern(
            "Retired",
            "Provide a definition removed in release two.",
            path=["Society", "Economics"],
            invariants=["This contract belongs only to the retired definition."],
        ),
        "PreviousName": _pattern(
            "PreviousName",
            "Perform the rename-stable behavior.",
            path=["Physics", "Dynamics"],
        ),
    }


def _v2_patterns() -> dict[str, dict]:
    return {
        "Anchor": _pattern("Anchor", "Provide the second, revised anchor definition."),
        "Relay": _pattern("Relay", "Use {{anchor}} to relay a result.", dependency="Anchor"),
        "MetadataCard": _pattern(
            "MetadataCard",
            "Keep this semantic definition stable.",
            caution="Review note from release two.",
            path=["Mind", "Memory"],
        ),
        "CurrentName": _pattern(
            "CurrentName",
            "Perform the rename-stable behavior.",
            path=["Physics", "Dynamics"],
        ),
        "NewPattern": _pattern(
            "NewPattern",
            "Provide a definition added in release two.",
            path=["Society", "Coordination"],
        ),
    }


def _write_patterns(directory: Path, patterns: dict[str, dict]) -> Path:
    directory.mkdir(parents=True)
    for handle, pattern in patterns.items():
        (directory / f"{handle}.json").write_text(
            json.dumps(copy.deepcopy(pattern), indent=2), encoding="utf-8"
        )
    return directory


def _apply(
    db_path: Path,
    directory: Path,
    *,
    patterns: dict[str, dict] | None = None,
    removals: list[str] | None = None,
) -> bool:
    add_files: list[str] = []
    if patterns:
        add_files.append(str(_write_patterns(directory, patterns)))
    with (
        patch("sema.cli.main.get_default_db_path", return_value=str(db_path)),
        patch(
            "sema.taxonomy_graph.embedding_service.EmbeddingService.get_embedding",
            return_value=np.zeros(384, dtype=np.float32),
        ),
    ):
        return apply_changes(remove_handles=removals or [], add_files=add_files)


def _build_release(db_path: Path, directory: Path, patterns: dict[str, dict]) -> None:
    assert _apply(db_path, directory, patterns=patterns)


def _exported_patterns(db_path: Path) -> dict[str, dict]:
    store = GraphStore(str(db_path), enable_embeddings=False)
    exported = {}
    for _node_id, node in store.get_nodes_by_type(NodeType.PATTERN):
        handle = node["text"]
        exported[handle] = store._get_pattern_content(handle, include_deps=True)
    return dict(sorted(exported.items()))


def _pattern_edges(db_path: Path) -> list[tuple[str, str, str, str | None, str]]:
    """Export graph relationships without database-specific node or edge IDs."""
    store = GraphStore(str(db_path), enable_embeddings=False)
    edges = []
    for source_id, target_id, _edge_id, edge in store.graph.edges(keys=True, data=True):
        source = store.graph.nodes[source_id]
        target = store.graph.nodes[target_id]
        if (
            source.get("node_type") != NodeType.PATTERN
            or target.get("node_type") != NodeType.PATTERN
        ):
            continue
        edge_type = edge["edge_type"].value
        edge_metadata = json.dumps(
            edge.get("metadata") or {}, sort_keys=True, separators=(",", ":")
        )
        edges.append((source["text"], target["text"], edge_type, edge.get("alias"), edge_metadata))
    return sorted(edges)


def _logical_snapshot(db_path: Path) -> dict:
    return {
        "patterns": _exported_patterns(db_path),
        "pattern_edges": _pattern_edges(db_path),
    }


def _complete_logical_read_model(db_path: Path) -> dict[str, list[str]]:
    """Normalize every graph node and edge while excluding storage artifacts.

    Node and edge UUIDs, embeddings, SQLite row order, and file layout are not
    logical state. Node type, text, metadata, edge type, alias, and edge metadata are.
    JSON strings make duplicate nodes and parallel edges countable and sortable.
    """
    store = GraphStore(str(db_path), enable_embeddings=False)
    node_descriptors = {}
    nodes = []
    for node_id, node in store.graph.nodes(data=True):
        descriptor = json.dumps(
            {
                "node_type": node["node_type"].value,
                "text": node["text"],
                "metadata": node.get("metadata") or {},
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        node_descriptors[node_id] = descriptor
        nodes.append(descriptor)

    edges = []
    for source_id, target_id, _edge_id, edge in store.graph.edges(keys=True, data=True):
        edges.append(
            json.dumps(
                {
                    "source": node_descriptors[source_id],
                    "target": node_descriptors[target_id],
                    "edge_type": edge["edge_type"].value,
                    "alias": edge.get("alias"),
                    "metadata": edge.get("metadata") or {},
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    return {"nodes": sorted(nodes), "edges": sorted(edges)}


def _node_labels(read_model: dict[str, list[str]]) -> set[tuple[str, str]]:
    return {
        (node["node_type"], node["text"])
        for descriptor in read_model["nodes"]
        for node in [json.loads(descriptor)]
    }


def _roots(db_path: Path) -> tuple[str, str]:
    info = vocabulary_info(str(db_path))
    return info["semantic_root"], info["catalog_root"]


def _target_equivalent(candidate: Path, target: Path) -> bool:
    """Require both cryptographic commitments and the unhashed logical payload."""
    return _roots(candidate) == _roots(target) and _logical_snapshot(
        candidate
    ) == _logical_snapshot(target)


def _without_generated_fields(pattern: dict) -> dict:
    return {
        key: copy.deepcopy(value)
        for key, value in pattern.items()
        if key not in {"sema_id", "sema_ref", "sema_stub", "sema_layer", "sema_category"}
    }


def _target_sources(db_path: Path, handles: set[str] | None = None) -> dict[str, dict]:
    exported = _exported_patterns(db_path)
    selected = set(exported) if handles is None else handles
    return {handle: _without_generated_fields(exported[handle]) for handle in sorted(selected)}


def test_full_target_overlay_matches_payload_but_leaves_derived_read_model_residue(
    tmp_path: Path,
) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    _build_release(source_db, tmp_path / "source-files", _v1_patterns())
    _build_release(target_db, tmp_path / "target-files", _v2_patterns())

    source_handles = set(_exported_patterns(source_db))
    target_handles = set(_exported_patterns(target_db))
    assert _apply(
        source_db,
        tmp_path / "overlay-files",
        patterns=_target_sources(target_db),
        removals=sorted(source_handles - target_handles),
    )

    assert _target_equivalent(source_db, target_db)
    overlay_model = _complete_logical_read_model(source_db)
    target_model = _complete_logical_read_model(target_db)
    assert overlay_model != target_model

    # Removing a pattern removes its incident edges, not the now-unreachable
    # contract/path nodes. Reclassifying a pattern likewise leaves old path
    # prefixes in the read model. Roots and pattern exports cannot expose this.
    residue = _node_labels(overlay_model) - _node_labels(target_model)
    assert ("INVARIANT", "This contract belongs only to the retired definition.") in residue
    assert ("TAXONOMY_PATH", "Society/Economics") in residue
    assert ("TAXONOMY_PATH", "Physics/Time") in residue


def test_direct_semantic_delta_matches_payload_but_not_in_place_read_model(
    tmp_path: Path,
) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    _build_release(source_db, tmp_path / "source-files", _v1_patterns())
    _build_release(target_db, tmp_path / "target-files", _v2_patterns())
    relay_v1 = GraphStore(str(source_db), enable_embeddings=False).get_pattern_hash("Relay")

    # Relay is intentionally omitted. Its authored text did not change; its
    # identity must move solely because Anchor changed underneath it.
    direct_delta = _target_sources(target_db, {"Anchor", "CurrentName", "NewPattern"})
    assert _apply(
        source_db,
        tmp_path / "direct-delta-files",
        patterns=direct_delta,
        removals=["PreviousName", "Retired"],
    )

    source_store = GraphStore(str(source_db), enable_embeddings=False)
    target_store = GraphStore(str(target_db), enable_embeddings=False)
    assert source_store.get_pattern_hash("Relay") != relay_v1
    assert source_store.get_pattern_hash("Relay") == target_store.get_pattern_hash("Relay")
    assert _roots(source_db) == _roots(target_db)

    # The two roots cannot see the outstanding metadata-only edit.
    assert _logical_snapshot(source_db) != _logical_snapshot(target_db)
    assert not _target_equivalent(source_db, target_db)

    assert _apply(
        source_db,
        tmp_path / "metadata-delta-files",
        patterns=_target_sources(target_db, {"MetadataCard"}),
    )
    assert _target_equivalent(source_db, target_db)
    assert _complete_logical_read_model(source_db) != _complete_logical_read_model(target_db)


def test_staged_fresh_rebuild_from_complete_delta_matches_entire_read_model(
    tmp_path: Path,
) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    rebuilt_db = tmp_path / "rebuilt.db"
    _build_release(source_db, tmp_path / "source-files", _v1_patterns())
    _build_release(target_db, tmp_path / "target-files", _v2_patterns())

    # Integrate the direct semantic edits, additions, removals, rename, and
    # metadata edit into a complete staged pattern set. Relay remains the V1
    # authored card: rebuilding resolves its Anchor edge and derives its V2 hash.
    integrated = {
        handle: _without_generated_fields(pattern)
        for handle, pattern in _exported_patterns(source_db).items()
    }
    for removed in {"PreviousName", "Retired"}:
        del integrated[removed]
    integrated.update(
        _target_sources(target_db, {"Anchor", "CurrentName", "MetadataCard", "NewPattern"})
    )

    assert set(integrated) == set(_exported_patterns(target_db))
    _build_release(rebuilt_db, tmp_path / "rebuilt-files", integrated)

    assert _target_equivalent(rebuilt_db, target_db)
    assert _complete_logical_read_model(rebuilt_db) == _complete_logical_read_model(target_db)


def test_hash_changed_subset_is_root_equivalent_but_misses_metadata(tmp_path: Path) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    _build_release(source_db, tmp_path / "source-files", _v1_patterns())
    _build_release(target_db, tmp_path / "target-files", _v2_patterns())

    source_store = GraphStore(str(source_db), enable_embeddings=False)
    target_store = GraphStore(str(target_db), enable_embeddings=False)
    source_handles = set(_exported_patterns(source_db))
    target_handles = set(_exported_patterns(target_db))
    changed = {
        handle
        for handle in source_handles & target_handles
        if source_store.get_pattern_hash(handle) != target_store.get_pattern_hash(handle)
    }
    added = target_handles - source_handles

    assert changed == {"Anchor", "Relay"}
    assert "MetadataCard" not in changed
    assert _apply(
        source_db,
        tmp_path / "hash-delta-files",
        patterns=_target_sources(target_db, changed | added),
        removals=sorted(source_handles - target_handles),
    )

    assert _roots(source_db) == _roots(target_db)
    assert _logical_snapshot(source_db) != _logical_snapshot(target_db)
    assert not _target_equivalent(source_db, target_db)


def test_target_overlay_without_explicit_removals_keeps_stale_patterns(tmp_path: Path) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    _build_release(source_db, tmp_path / "source-files", _v1_patterns())
    _build_release(target_db, tmp_path / "target-files", _v2_patterns())

    assert _apply(
        source_db,
        tmp_path / "overlay-without-removals-files",
        patterns=_target_sources(target_db),
    )

    remaining = _exported_patterns(source_db)
    assert {"Retired", "PreviousName"} <= set(remaining)
    assert _roots(source_db) != _roots(target_db)
    assert not _target_equivalent(source_db, target_db)


def test_metadata_only_change_requires_payload_comparison(tmp_path: Path) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    source = {
        "MetadataCard": _pattern(
            "MetadataCard", "Keep the definition stable.", caution="First review note."
        )
    }
    target = {
        "MetadataCard": _pattern(
            "MetadataCard", "Keep the definition stable.", caution="Second review note."
        )
    }
    _build_release(source_db, tmp_path / "source-files", source)
    _build_release(target_db, tmp_path / "target-files", target)

    assert _roots(source_db) == _roots(target_db)
    assert _logical_snapshot(source_db) != _logical_snapshot(target_db)
    assert not _target_equivalent(source_db, target_db)

    assert _apply(
        source_db,
        tmp_path / "metadata-files",
        patterns=_target_sources(target_db),
    )
    assert _target_equivalent(source_db, target_db)


def test_handle_rename_preserves_semantic_root_but_changes_catalog_root(tmp_path: Path) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    _build_release(
        source_db,
        tmp_path / "source-files",
        {"PreviousName": _pattern("PreviousName", "Perform the rename-stable behavior.")},
    )
    _build_release(
        target_db,
        tmp_path / "target-files",
        {"CurrentName": _pattern("CurrentName", "Perform the rename-stable behavior.")},
    )

    source_semantic, source_catalog = _roots(source_db)
    target_semantic, target_catalog = _roots(target_db)
    assert source_semantic == target_semantic
    assert source_catalog != target_catalog
    assert not _target_equivalent(source_db, target_db)


def test_failed_or_wrong_delta_is_never_target_equivalent(tmp_path: Path) -> None:
    source_db = tmp_path / "source.db"
    target_db = tmp_path / "target.db"
    _build_release(source_db, tmp_path / "source-files", _v1_patterns())
    _build_release(target_db, tmp_path / "target-files", _v2_patterns())
    before_failure = _logical_snapshot(source_db)

    assert not _apply(
        source_db,
        tmp_path / "failed-delta-files",
        removals=["DoesNotExist"],
    )
    assert _logical_snapshot(source_db) == before_failure
    assert not _target_equivalent(source_db, target_db)

    wrong_delta = _target_sources(target_db, {"Anchor", "CurrentName", "NewPattern"})
    wrong_delta["Anchor"]["mechanism"] = "Provide a plausible but incorrect anchor definition."
    assert _apply(
        source_db,
        tmp_path / "wrong-delta-files",
        patterns=wrong_delta,
        removals=["PreviousName", "Retired"],
    )
    assert _roots(source_db) != _roots(target_db)
    assert not _target_equivalent(source_db, target_db)
