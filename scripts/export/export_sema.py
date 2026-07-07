#!/usr/bin/env python3
"""
ExportSema Vocabulary (Pinned)
Exports patterns with Weak Links in content (for stable hashing)
and Strong Links in metadata (for precise resolution).
"""

import json
import os
import sys

# Fix paths
# Add 'src' to path relative to this script (../../src)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../.."))
src_path = os.path.join(project_root, "src")
sys.path.append(src_path)

# Imports
from sema.core.config import get_config  # noqa: E402
from sema.core.hashing import generate_sema_hash  # noqa: E402
from sema.taxonomy_graph.graph_store import GraphStore, NodeType  # noqa: E402


def get_db_path():
    cfg = get_config()
    profile = cfg.get_active_profile()
    # Default to data/taxonomy.db relative to project_root
    default_db = os.path.join(project_root, "data/taxonomy.db")
    db_path = profile.get("db_path", default_db)

    # Resolve relative paths against project_root if they don't exist in CWD
    if not os.path.isabs(db_path) and not os.path.exists(db_path):
        candidate = os.path.join(project_root, db_path)
        if os.path.exists(candidate):
            return candidate

    return db_path


EXPORT_DIR = os.path.join(project_root, "data/vocabulary")


def normalize_export_order(card):
    """Keep derived compatibility fields after dependencies to avoid export churn."""
    if "dependencies" not in card:
        return card

    layer = card.pop("sema_layer", None)
    category = card.pop("sema_category", None)
    dependencies = card.pop("dependencies")

    card["dependencies"] = dependencies
    if layer is not None:
        card["sema_layer"] = layer
    if category is not None:
        card["sema_category"] = category
    return card


def wipe_directory(path):
    """Remove all .json files from a directory."""
    if os.path.exists(path):
        for f in os.listdir(path):
            if f.endswith(".json"):
                os.remove(os.path.join(path, f))


def get_linked_text(store, node_id, edge_type):
    """Helper to fetch text of all nodes connected by a specific edge type.

    MultiDiGraph.get_edge_data returns {key: attrs}; we iterate values so
    parallel edges between the same nodes are all examined.
    """
    texts = []
    for succ in store.graph.successors(node_id):
        for edge_data in (store.graph.get_edge_data(node_id, succ) or {}).values():
            if edge_data.get("edge_type") == edge_type:
                texts.append(store.graph.nodes[succ]["text"])
                break
    return sorted(texts)


def export_vocabulary():
    taxonomy_db = get_db_path()

    if not os.path.exists(taxonomy_db):
        print(f"Error: Database {taxonomy_db} not found. Run ingest script first.")
        return

    store = GraphStore(taxonomy_db)
    print(f"📦 Exporting from {taxonomy_db}...")

    # Wipe and recreate vocabulary directory (safe - it's just an export from DB)
    wipe_directory(EXPORT_DIR)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # 1. First Pass: Generate Hashes & Build Map
    handle_to_id = {}
    patterns = []

    for node_id, data in store.graph.nodes(data=True):
        node_type = data.get("node_type")
        # Accept both PATTERN and SOLUTION (for backwards compatibility during transition)
        if node_type not in [NodeType.PATTERN, NodeType.SOLUTION]:
            continue

        metadata = data.get("metadata", {})
        pattern = metadata.get("pattern", {})

        # Just export the pattern as-is from the database
        if not pattern:
            continue  # Skip if no pattern data

        handle = pattern.get("handle")
        if not handle:
            continue

        # Pattern is already complete from database. Derive sema_layer /
        # sema_category from _meta.path (path[0] / path[1]) for legacy
        # consumer compat. Falls back to legacy _meta.layer / _meta.category
        # for pre-migration DBs that haven't been touched yet.
        meta = pattern.get("_meta", {}) or {}
        path = meta.get("path") or []
        if path:
            pattern["sema_layer"] = path[0]
            if len(path) >= 2:
                pattern["sema_category"] = path[1]
        else:
            layer = meta.get("layer")
            category = meta.get("category")
            if layer:
                pattern["sema_layer"] = layer
            if category:
                pattern["sema_category"] = category
        # Strip the legacy fields if they leaked into the stored pattern —
        # they're derived, not canonical, and shouldn't appear in exports.
        meta.pop("layer", None)
        meta.pop("category", None)

        # Validate
        if not pattern.get("handle"):
            continue

        # Reconstruct dependencies from graph edges (Merkle DAG source of truth)
        deps = store.get_dependencies_from_edges(handle)
        if deps:
            pattern["dependencies"] = deps

        # Mint Hash
        try:
            # Use DB state for dependency resolution
            def hash_lookup(h):
                return store.get_pattern_hash(h)

            hash_info = generate_sema_hash(pattern, hash_lookup=hash_lookup)

            # Store everything needed for Second Pass
            entry = {"pattern": pattern, "hash_info": hash_info, "node_id": node_id}
            patterns.append(entry)
            handle_to_id[pattern["handle"]] = hash_info["reference"]  # Store 'Handle#Hash'

        except Exception as e:
            print(f"  ❌ Hashing failed for {pattern.get('handle')}: {e}")
            continue

    # 2. Second Pass: Resolve Links and Save
    count = 0
    archived_count = 0

    # Ensure Archive Exists
    archive_dir = os.path.join(EXPORT_DIR, "experimental")
    os.makedirs(archive_dir, exist_ok=True)

    for p in patterns:
        card = p["pattern"].copy()
        hash_info = p["hash_info"]

        card["sema_id"] = hash_info["full_id"]
        card["sema_ref"] = hash_info["reference"]
        card["sema_stub"] = hash_info["stub"]

        # Remove deprecated 'links' field - edges are stored in graph database
        card.pop("links", None)
        normalize_export_order(card)

        # Determine Destination (Archive vs Root)
        # Check mechanism for placeholders
        mech = card.get("mechanism", "").lower()
        is_naked = "mechanism not defined" in mech or len(mech) < 10

        if is_naked:
            dest_dir = archive_dir
            archived_count += 1
        else:
            dest_dir = EXPORT_DIR
            count += 1

        filename = f"{hash_info['handle']}.json"
        with open(os.path.join(dest_dir, filename), "w") as f:
            json.dump(card, f, indent=2)

        # print(f"  -> {hash_info['reference']}")

    print(f"\n✅ Exported {count} core patterns to {EXPORT_DIR}")
    print(f"📦 Archived {archived_count} experimental patterns to {archive_dir}")


if __name__ == "__main__":
    export_vocabulary()
