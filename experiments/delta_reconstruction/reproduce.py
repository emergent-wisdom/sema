#!/usr/bin/env python3
"""Reproduce the public Sema v0.3.0 -> v0.4.0 delta reconstruction experiment.

The source and target data inputs come only from public git tags. Reconstruction
uses the implementation in the current checkout. Every database mutation
happens in a temporary directory; the checkout and tagged artifacts remain
unchanged.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_TAG = "v0.3.0"
TARGET_TAG = "v0.4.0"
EXPECTED_RESULTS = Path(__file__).with_name("expected-results.json")

# Use the implementation in this checkout, not a separately installed Sema.
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from sema.core.hashing import (  # noqa: E402
    LEGACY_SPECIALIZATION_FIELD,
    SEMANTIC_FIELDS,
    extract_handle_from_ref,
    normalize_dependencies_to_handles,
    semantic_hash_input,
    vocabulary_info,
)
from sema.taxonomy_graph.graph_store import GraphStore, NodeType  # noqa: E402

Pattern = dict[str, Any]
PatternMap = dict[str, Pattern]
ReadModel = dict[str, Any]


def _git_bytes(*arguments: str) -> bytes:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(arguments)} failed: {detail}") from exc


def _tag_commit(tag: str) -> str:
    return _git_bytes("rev-list", "-n", "1", tag).decode("ascii").strip()


def _extract_tag(tag: str, destination: Path) -> None:
    """Extract only the public release DB and pattern JSON from one local tag."""
    archive = _git_bytes(
        "archive",
        "--format=tar",
        tag,
        "data/taxonomy.db",
        "data/vocabulary",
    )
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                (destination / member.name).mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                raise RuntimeError(f"Unexpected non-file entry in {tag}: {member.name}")
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination.resolve())
            except ValueError as exc:
                raise RuntimeError(f"Unsafe path in {tag}: {member.name}") from exc
            source = bundle.extractfile(member)
            if source is None:
                raise RuntimeError(f"Could not read {tag}:{member.name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def _load_patterns(directory: Path) -> PatternMap:
    patterns: PatternMap = {}
    for path in sorted((directory / "data" / "vocabulary").glob("*.json")):
        pattern = json.loads(path.read_text(encoding="utf-8"))
        handle = pattern["handle"]
        if handle in patterns:
            raise RuntimeError(f"Duplicate handle in {directory}: {handle}")
        patterns[handle] = pattern
    return patterns


def _dependency_handles(pattern: Pattern) -> set[str]:
    handles: set[str] = set()
    for entries in (pattern.get("dependencies") or {}).values():
        if not isinstance(entries, dict):
            continue
        for reference in entries.values():
            references = reference if isinstance(reference, list) else [reference]
            for item in references:
                if isinstance(item, str):
                    handles.add(extract_handle_from_ref(item))
    extends = pattern.get("extends")
    if isinstance(extends, str):
        handles.add(extract_handle_from_ref(extends))
    return handles


def _topological_order(patterns: PatternMap) -> list[str]:
    """Put every dependency before the pattern that consumes it."""
    in_degree = dict.fromkeys(patterns, 0)
    dependents: dict[str, list[str]] = {handle: [] for handle in patterns}
    for handle, pattern in patterns.items():
        for dependency in sorted(_dependency_handles(pattern)):
            if dependency not in patterns or dependency == handle:
                continue
            in_degree[handle] += 1
            dependents[dependency].append(handle)

    ready = sorted(handle for handle, degree in in_degree.items() if degree == 0)
    order: list[str] = []
    while ready:
        handle = ready.pop(0)
        order.append(handle)
        for dependent in sorted(dependents[handle]):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                ready.append(dependent)
                ready.sort()

    if len(order) != len(patterns):
        unresolved = sorted(set(patterns) - set(order))
        raise RuntimeError(f"Target vocabulary is cyclic: {', '.join(unresolved[:10])}")
    return order


def _semantic_projection(pattern: Pattern) -> Pattern:
    """Compare authored semantics while ignoring dependency hash cascades."""
    projection = copy.deepcopy(semantic_hash_input(pattern))
    if "dependencies" in projection:
        projection["dependencies"] = normalize_dependencies_to_handles(projection["dependencies"])
    return projection


def _metadata_projection(pattern: Pattern) -> Pattern:
    semantic_keys = set(SEMANTIC_FIELDS) | {LEGACY_SPECIALIZATION_FIELD}
    generated_keys = {"handle", "sema_id", "sema_ref", "sema_stub"}
    return {
        key: copy.deepcopy(value)
        for key, value in pattern.items()
        if key not in semantic_keys | generated_keys
    }


def _export_patterns(store: GraphStore) -> PatternMap:
    exported: PatternMap = {}
    for _node_id, node in store.get_nodes_by_type(NodeType.PATTERN):
        handle = node["text"]
        pattern = store._get_pattern_content(handle, include_deps=True)
        if pattern is None:
            raise RuntimeError(f"Could not export {handle}")
        exported[handle] = pattern
    return dict(sorted(exported.items()))


def _pattern_edges(store: GraphStore) -> list[list[Any]]:
    """Export logical pattern edges without incidental SQLite UUIDs."""
    edges: list[list[Any]] = []
    for source_id, target_id, _edge_key, edge in store.graph.edges(keys=True, data=True):
        source = store.graph.nodes[source_id]
        target = store.graph.nodes[target_id]
        if (
            source.get("node_type") != NodeType.PATTERN
            or target.get("node_type") != NodeType.PATTERN
        ):
            continue
        edges.append(
            [
                source["text"],
                target["text"],
                edge["edge_type"].value,
                edge.get("alias"),
                edge.get("metadata") or {},
            ]
        )
    return sorted(edges, key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))


def _canonical_record(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _records_digest(records: Counter[str]) -> str:
    digest = hashlib.sha256()
    for record, count in sorted(records.items()):
        encoded = record.encode("utf-8")
        digest.update(count.to_bytes(8, "big"))
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()


def _normalized_read_model(store: GraphStore) -> ReadModel:
    """Normalize all logical nodes and edges while ignoring storage identity."""
    nodes: Counter[str] = Counter()
    derived_nodes: Counter[str] = Counter()
    node_keys: dict[str, list[str]] = {}
    node_type_counts: Counter[str] = Counter()

    for node_id, node in store.graph.nodes(data=True):
        node_type_value = node.get("node_type")
        node_type = getattr(node_type_value, "value", str(node_type_value))
        endpoint = [node_type, node.get("text", "")]
        record = _canonical_record(
            {
                "node_type": node_type,
                "text": node.get("text", ""),
                "metadata": node.get("metadata") or {},
            }
        )
        nodes[record] += 1
        node_keys[node_id] = endpoint
        node_type_counts[node_type] += 1
        if node_type != NodeType.PATTERN.value:
            derived_nodes[record] += 1

    edges: Counter[str] = Counter()
    derived_edges: Counter[str] = Counter()
    edge_type_counts: Counter[str] = Counter()
    for source_id, target_id, _edge_key, edge in store.graph.edges(keys=True, data=True):
        edge_type_value = edge.get("edge_type")
        edge_type = getattr(edge_type_value, "value", str(edge_type_value))
        record = _canonical_record(
            {
                "source": node_keys[source_id],
                "target": node_keys[target_id],
                "edge_type": edge_type,
                "alias": edge.get("alias"),
                "metadata": edge.get("metadata") or {},
            }
        )
        edges[record] += 1
        edge_type_counts[edge_type] += 1
        if (
            node_keys[source_id][0] != NodeType.PATTERN.value
            or node_keys[target_id][0] != NodeType.PATTERN.value
        ):
            derived_edges[record] += 1

    node_digest = _records_digest(nodes)
    edge_digest = _records_digest(edges)
    combined_digest = hashlib.sha256(
        f"sema-normalized-read-model-v1\0{node_digest}\0{edge_digest}".encode("ascii")
    ).hexdigest()
    return {
        "nodes": nodes,
        "edges": edges,
        "derived_nodes": derived_nodes,
        "derived_edges": derived_edges,
        "summary": {
            "node_count": sum(nodes.values()),
            "edge_count": sum(edges.values()),
            "node_type_counts": dict(sorted(node_type_counts.items())),
            "edge_type_counts": dict(sorted(edge_type_counts.items())),
            "nodes_sha256": node_digest,
            "edges_sha256": edge_digest,
            "read_model_sha256": combined_digest,
        },
    }


def _counter_distance(candidate: Counter[str], reference: Counter[str]) -> dict[str, int]:
    return {
        "extra": sum((candidate - reference).values()),
        "missing": sum((reference - candidate).values()),
    }


def _read_model_comparison(candidate: ReadModel, reference: ReadModel) -> dict[str, Any]:
    node_distance = _counter_distance(candidate["nodes"], reference["nodes"])
    edge_distance = _counter_distance(candidate["edges"], reference["edges"])
    derived_node_distance = _counter_distance(
        candidate["derived_nodes"], reference["derived_nodes"]
    )
    derived_edge_distance = _counter_distance(
        candidate["derived_edges"], reference["derived_edges"]
    )
    return {
        "complete_matches_fresh_target": not any(node_distance.values())
        and not any(edge_distance.values()),
        "candidate_read_model_sha256": candidate["summary"]["read_model_sha256"],
        "logical_nodes": node_distance,
        "logical_edges": edge_distance,
        "derived_nodes_match": not any(derived_node_distance.values()),
        "derived_nodes": derived_node_distance,
        "derived_edges_match": not any(derived_edge_distance.values()),
        "derived_edges": derived_edge_distance,
    }


def _roots(db_path: Path) -> dict[str, Any]:
    info = vocabulary_info(str(db_path))
    return {
        "semantic": info["semantic_root"],
        "catalog": info["catalog_root"],
        "pattern_count": info["pattern_count"],
    }


def _copy_source_database(source_directory: Path, destination: Path) -> None:
    shutil.copy2(source_directory / "data" / "taxonomy.db", destination)


def _build_fresh_database(db_path: Path, patterns: PatternMap, order: list[str]) -> GraphStore:
    """Compile a complete card snapshot into a new current-code read model."""
    store = GraphStore(str(db_path), enable_embeddings=False)
    # The second pass resolves soft signature links whose targets were minted
    # later in the first pass. This mirrors the installed-library compiler.
    for _pass in range(2):
        for handle in order:
            candidate = copy.deepcopy(patterns[handle])
            result = store.add_pattern(
                candidate,
                skip_cascade=True,
                validated_extends_batch=True,
            )
            if not result.get("success"):
                raise RuntimeError(
                    f"Could not build fresh read model at {handle}: {result.get('error', result)}"
                )
    store.sweep_related_edges()
    return store


def _replace_metadata_projection(candidate: Pattern, target: Pattern) -> None:
    semantic_keys = set(SEMANTIC_FIELDS) | {LEGACY_SPECIALIZATION_FIELD}
    protected_keys = semantic_keys | {"handle", "sema_id", "sema_ref", "sema_stub"}
    metadata_keys = (set(candidate) | set(target)) - protected_keys
    for key in metadata_keys:
        candidate.pop(key, None)
        if key in target:
            candidate[key] = copy.deepcopy(target[key])


def _integrate_complete_delta(
    source_patterns: PatternMap,
    target_patterns: PatternMap,
    direct_semantic: set[str],
    metadata_patch_handles: set[str],
    added_handles: set[str],
    removed_handles: set[str],
) -> PatternMap:
    """Stage a complete target snapshot before compiling or activating it."""
    staged = copy.deepcopy(source_patterns)
    for handle in removed_handles:
        staged.pop(handle, None)
    for handle in direct_semantic:
        # A direct semantic edit is transported as the complete target card, so
        # its metadata arrives with it.
        staged[handle] = copy.deepcopy(target_patterns[handle])
    for handle in metadata_patch_handles:
        _replace_metadata_projection(staged[handle], target_patterns[handle])
    for handle in added_handles:
        staged[handle] = copy.deepcopy(target_patterns[handle])
    return staged


def _apply_subset(
    store: GraphStore,
    target_patterns: PatternMap,
    target_order: list[str],
    selected_handles: set[str],
) -> set[str]:
    """Apply target cards with the current GraphStore hash-cascade algorithm."""
    cascaded: set[str] = set()
    for handle in target_order:
        if handle not in selected_handles:
            continue
        candidate = copy.deepcopy(target_patterns[handle])
        result = store.add_pattern(candidate, validated_extends_batch=True)
        if not result.get("success"):
            raise RuntimeError(f"Could not apply {handle}: {result.get('error', result)}")
        cascaded.update(result.get("cascade", {}).get("updated", []))
    store.sweep_related_edges()
    return cascaded


def _variant_result(
    store: GraphStore,
    db_path: Path,
    target_patterns: PatternMap,
    target_edges: list[list[Any]],
    target_roots: dict[str, Any],
    target_read_model: ReadModel,
    applied_handles: set[str],
    cascaded_handles: set[str],
    cascade_only_expected: set[str],
) -> dict[str, Any]:
    actual_patterns = _export_patterns(store)
    all_handles = sorted(set(actual_patterns) | set(target_patterns))
    full_mismatches = [
        handle
        for handle in all_handles
        if actual_patterns.get(handle) != target_patterns.get(handle)
    ]
    semantic_mismatches = [
        handle
        for handle in all_handles
        if handle not in actual_patterns
        or handle not in target_patterns
        or _semantic_projection(actual_patterns[handle])
        != _semantic_projection(target_patterns[handle])
    ]
    metadata_mismatches = [
        handle
        for handle in all_handles
        if handle not in actual_patterns
        or handle not in target_patterns
        or _metadata_projection(actual_patterns[handle])
        != _metadata_projection(target_patterns[handle])
    ]
    actual_roots = _roots(db_path)
    actual_edges = _pattern_edges(store)
    actual_read_model = _normalized_read_model(store)
    omitted_cascade_only = cascade_only_expected - applied_handles
    omitted_matching_target = {
        handle
        for handle in omitted_cascade_only
        if handle in actual_patterns
        and actual_patterns[handle].get("sema_id") == target_patterns[handle].get("sema_id")
    }
    metadata_mismatch_digest = hashlib.sha256(
        "\n".join(metadata_mismatches).encode("utf-8")
    ).hexdigest()

    return {
        "applied_pattern_count": len(applied_handles),
        "result_pattern_count": len(actual_patterns),
        "semantic_root_matches": actual_roots["semantic"] == target_roots["semantic"],
        "catalog_root_matches": actual_roots["catalog"] == target_roots["catalog"],
        "semantic_patterns_match": not semantic_mismatches,
        "pattern_edges_match": actual_edges == target_edges,
        "read_model": _read_model_comparison(actual_read_model, target_read_model),
        "full_payload_matches": not full_mismatches,
        "semantic_mismatch_handles": semantic_mismatches,
        "metadata_mismatch_count": len(metadata_mismatches),
        "metadata_mismatch_examples": metadata_mismatches[:10],
        "metadata_mismatch_handles_sha256": metadata_mismatch_digest,
        "full_payload_mismatch_count": len(full_mismatches),
        "cascade_only_cards_omitted": len(omitted_cascade_only),
        "omitted_cascade_only_identities_matching_target": len(omitted_matching_target),
        "omitted_cascade_only_identities_seen_in_in_place_cascade": len(
            omitted_cascade_only & cascaded_handles
        ),
    }


def run_experiment() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="sema-delta-reconstruction-") as temporary:
        root = Path(temporary)
        source_directory = root / "source-tag"
        target_directory = root / "target-tag"
        source_directory.mkdir()
        target_directory.mkdir()
        _extract_tag(SOURCE_TAG, source_directory)
        _extract_tag(TARGET_TAG, target_directory)

        source_patterns = _load_patterns(source_directory)
        target_patterns = _load_patterns(target_directory)
        source_handles = set(source_patterns)
        target_handles = set(target_patterns)
        common_handles = source_handles & target_handles
        added_handles = target_handles - source_handles
        removed_handles = source_handles - target_handles

        hash_changed = {
            handle
            for handle in common_handles
            if source_patterns[handle]["sema_id"] != target_patterns[handle]["sema_id"]
        }
        direct_semantic = {
            handle
            for handle in common_handles
            if _semantic_projection(source_patterns[handle])
            != _semantic_projection(target_patterns[handle])
        }
        cascade_only = hash_changed - direct_semantic
        metadata_changed = {
            handle
            for handle in common_handles
            if _metadata_projection(source_patterns[handle])
            != _metadata_projection(target_patterns[handle])
        }
        metadata_only = metadata_changed - hash_changed

        tagged_target_db = target_directory / "data" / "taxonomy.db"
        tagged_target_store = GraphStore(str(tagged_target_db), enable_embeddings=False)
        tagged_target_roots = _roots(tagged_target_db)
        tagged_target_patterns = _export_patterns(tagged_target_store)
        tagged_target_edges = _pattern_edges(tagged_target_store)
        tagged_target_read_model = _normalized_read_model(tagged_target_store)
        target_order = _topological_order(target_patterns)

        fresh_target_db = root / "fresh-target.db"
        fresh_target_store = _build_fresh_database(fresh_target_db, target_patterns, target_order)
        fresh_target_patterns = _export_patterns(fresh_target_store)
        fresh_target_roots = _roots(fresh_target_db)
        fresh_target_edges = _pattern_edges(fresh_target_store)
        fresh_target_read_model = _normalized_read_model(fresh_target_store)

        selections = {
            "full_target_overlay": target_handles,
            "hash_changed_plus_added": hash_changed | added_handles,
            "direct_semantic_plus_added": direct_semantic | added_handles,
        }
        variants: dict[str, Any] = {}
        for name, selection in selections.items():
            db_path = root / f"{name}.db"
            _copy_source_database(source_directory, db_path)
            store = GraphStore(str(db_path), enable_embeddings=False)
            cascaded = _apply_subset(store, target_patterns, target_order, selection)
            variants[name] = _variant_result(
                store,
                db_path,
                target_patterns,
                fresh_target_edges,
                tagged_target_roots,
                fresh_target_read_model,
                selection,
                cascaded,
                cascade_only,
            )

        # Safe alternative to mutating the active read model: first integrate
        # the complete delta into a full card snapshot, then compile a new DB and
        # compare it with the independently built target before activation.
        metadata_patch_handles = metadata_changed - direct_semantic
        staged_patterns = _integrate_complete_delta(
            source_patterns,
            target_patterns,
            direct_semantic,
            metadata_patch_handles,
            added_handles,
            removed_handles,
        )
        staged_order = _topological_order(staged_patterns)
        staged_db = root / "staged-complete-delta-fresh-build.db"
        staged_store = _build_fresh_database(staged_db, staged_patterns, staged_order)
        staged_result = _variant_result(
            staged_store,
            staged_db,
            target_patterns,
            fresh_target_edges,
            tagged_target_roots,
            fresh_target_read_model,
            direct_semantic | added_handles,
            set(),
            cascade_only,
        )
        staged_result.update(
            {
                "build_strategy": "staged complete snapshot, then fresh current-code build",
                "metadata_patch_count": len(metadata_patch_handles),
                "explicit_removal_count": len(removed_handles),
            }
        )
        variants["staged_complete_delta_fresh_build"] = staged_result

        source_db = source_directory / "data" / "taxonomy.db"
        return {
            "experiment": f"{SOURCE_TAG}-to-{TARGET_TAG}",
            "tags": {
                "source": {"name": SOURCE_TAG, "commit": _tag_commit(SOURCE_TAG)},
                "target": {"name": TARGET_TAG, "commit": _tag_commit(TARGET_TAG)},
            },
            "release_counts": {
                "source_patterns": len(source_patterns),
                "target_patterns": len(target_patterns),
                "added": len(added_handles),
                "added_handles": sorted(added_handles),
                "removed": len(removed_handles),
                "removed_handles": sorted(removed_handles),
            },
            "change_classification": {
                "hash_changed_existing": len(hash_changed),
                "direct_semantic_edits_existing": len(direct_semantic),
                "cascade_only_existing": len(cascade_only),
                "metadata_changed_existing": len(metadata_changed),
                "metadata_only_existing": sorted(metadata_only),
            },
            "source_roots": _roots(source_db),
            "target_roots": tagged_target_roots,
            "fresh_target_roots": fresh_target_roots,
            "fresh_target_pattern_edge_count": len(fresh_target_edges),
            "fresh_target_read_model": fresh_target_read_model["summary"],
            "tagged_target_comparison": {
                "roots_match_fresh_build": tagged_target_roots == fresh_target_roots,
                "tagged_json_payload_matches_fresh_build": target_patterns == fresh_target_patterns,
                "tagged_db_payload_matches_fresh_build": tagged_target_patterns
                == fresh_target_patterns,
                "pattern_edges_match_fresh_build": tagged_target_edges == fresh_target_edges,
                "read_model": _read_model_comparison(
                    tagged_target_read_model, fresh_target_read_model
                ),
            },
            "variants": variants,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print newly computed results without checking expected-results.json.",
    )
    arguments = parser.parse_args()

    try:
        results = run_experiment()
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(results, indent=2, sort_keys=True))
    if arguments.print_only:
        return 0

    try:
        expected = json.loads(EXPECTED_RESULTS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: could not read {EXPECTED_RESULTS}: {exc}", file=sys.stderr)
        return 1
    if results != expected:
        print(
            "ERROR: results differ from expected-results.json; run with --print-only to inspect.",
            file=sys.stderr,
        )
        return 1
    print("PASS: computed results match expected-results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
