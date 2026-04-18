import argparse
import json
import os
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

from ..core.dependencies import get_dependencies_handles, topological_sort
from ..core.registry import (
    RegistryManager,
    get_bundled_db_path,
    get_default_db_path,
    is_bundled_db,
    list_dbs,
    register_db,
    set_active_db,
)
from ..core.utils import compact_dict
from ..core.validator import validate_pattern

# Initialize Registry (Lazy Load)
_registry_manager = None


def get_registry():
    global _registry_manager
    if _registry_manager is None:
        _registry_manager = RegistryManager()
    return _registry_manager


def apply_changes(
    remove_handles: list[str] = None, add_files: list[str] = None, check_only: bool = False
):
    """Atomic apply operation: validate everything, then execute all changes.

    Safe for AI autonomous use - validates before any modifications.

    Args:
        remove_handles: List of pattern handles to remove
        add_files: List of files/directories to add
        check_only: If True, only validate without applying changes
    """
    from ..taxonomy_graph.graph_store import GraphStore, NodeType

    remove_handles = remove_handles or []
    add_files = add_files or []

    if not remove_handles and not add_files:
        print("❌ Nothing to do. Specify --remove and/or --add")
        return False

    db_path = get_default_db_path()
    if is_bundled_db(db_path):
        print("❌ Cannot modify the bundled vocabulary — it gets overwritten on upgrade.")
        print("   Run `sema build my.db --preset full` then `sema use my.db` first.")
        return False
    store = GraphStore(db_path)

    # Banner: fingerprint the DB before mutating it, so the audit trail is
    # clear about which vocabulary state this apply ran against.
    try:
        from ..core.hashing import format_load_line, vocabulary_info

        print(format_load_line(vocabulary_info(db_path)))
    except Exception:
        pass

    # ============ PHASE 1: VALIDATION ============
    print("Validating...")
    errors = []

    # 1a. Validate removals exist
    remove_node_ids = {}
    for handle in remove_handles:
        found = False
        for nid, data in store.get_nodes_by_type(NodeType.PATTERN):
            if data["text"] == handle:
                remove_node_ids[handle] = nid
                found = True
                break
        if not found:
            errors.append(f"Pattern to remove not found: '{handle}'")

    if remove_handles and not errors:
        print(f"  ✓ {len(remove_handles)} patterns to remove: {', '.join(remove_handles)}")

    # 1b. Validate additions
    add_patterns = []  # List of (file_path, data)
    add_handles = set()

    for file_str in add_files:
        file_path = Path(file_str)

        # Handle directories
        if file_path.is_dir():
            json_files = sorted(file_path.glob("*.json"))
            for jf in json_files:
                result = _validate_pattern_file(jf)
                if result["error"]:
                    errors.append(result["error"])
                else:
                    add_patterns.append((jf, result["data"]))
                    add_handles.add(result["data"]["handle"])
        elif file_path.exists():
            result = _validate_pattern_file(file_path)
            if result["error"]:
                errors.append(result["error"])
            else:
                add_patterns.append((file_path, result["data"]))
                add_handles.add(result["data"]["handle"])
        else:
            errors.append(f"File not found: {file_path}")

    if add_patterns and not errors:
        handles_str = ", ".join(p[1]["handle"] for p in add_patterns)
        print(f"  ✓ {len(add_patterns)} patterns to add: {handles_str}")

    # 1c. Dependency graph check
    # Patterns being removed must not be referenced by patterns staying
    # (unless those references are also being re-added)
    if remove_handles and not errors:
        # Build map of what depends on what from edges (edge-only storage model)
        dependents = {}  # handle -> list of handles that depend on it
        for _nid, data in store.get_nodes_by_type(NodeType.PATTERN):
            h = data["text"]
            # Get dependencies from graph edges (not from stored pattern)
            edge_deps = store.get_dependencies_from_edges(h)
            # Check all dependency types
            for dep_type in ["references", "composes_with", "accepts", "yields"]:
                for _dep_key, dep_ref in edge_deps.get(dep_type, {}).items():
                    # Extract handle from full sema_id format: sema:Handle#mh:SHA-256:...
                    # Or legacy stub format: Handle#stub
                    if dep_ref.startswith("sema:"):
                        # Full format: sema:Handle#mh:SHA-256:hash
                        dep_handle = dep_ref[5:].split("#")[0]  # Remove "sema:" prefix
                    else:
                        # Legacy format: Handle#stub
                        dep_handle = dep_ref.split("#")[0]
                    if dep_handle not in dependents:
                        dependents[dep_handle] = []
                    dependents[dep_handle].append(h)

        # Check each pattern being removed
        for handle in remove_handles:
            if handle in add_handles:
                continue  # Being re-added, ok

            # Find patterns that depend on this one
            users = dependents.get(handle, [])
            for user in users:
                if user in remove_handles:
                    continue  # Also being removed, ok
                if user in add_handles:
                    continue  # Being re-added (presumably with updated deps), ok
                # Dangling reference!
                errors.append(
                    f"Cannot remove '{handle}': pattern '{user}' depends on it. "
                    f"Include '{user}' in --remove or supply updated version in --add."
                )

    if not errors:
        print("  ✓ Validation passed")

    # Abort if any validation errors
    if errors:
        print("\n❌ Validation failed:")
        for e in errors:
            print(f"  {e}")
        return False

    # Check-only mode: exit after validation
    if check_only:
        print("\n✓ Check passed - no changes made")
        return True

    # ============ PHASE 2: EXECUTION ============
    print("\nApplying...")

    # 2a. Remove patterns
    for handle in remove_handles:
        node_id = remove_node_ids[handle]
        result = store.delete_node_cascade(node_id)
        if result.get("success"):
            print(f"  ✓ Removed {handle}")
        else:
            print(f"  ❌ Failed to remove {handle}: {result.get('error')}")
            # Note: partial state - could add rollback here
            return False

    # 2b. Topological sort additions
    if add_patterns:
        patterns_dict = {p[1]["handle"]: p[1] for p in add_patterns}
        try:
            sorted_handles = topological_sort(patterns_dict)
        except ValueError as e:
            print(f"  ❌ Dependency error: {e}")
            return False

        # 2b2. Check layer direction (Rule 7.6)
        # Applies only to hard dependency buckets (accepts, composes_with).
        # yields and references are exempt — see dependencies._LAYER_CHECKED_BUCKETS.
        try:
            from ..core.dependencies import validate_layer_direction

            existing_patterns = {
                data.get("handle", nid): data
                for nid, data in store.get_nodes_by_type(NodeType.PATTERN)
                if data.get("handle")
            }
            validate_layer_direction(patterns_dict, existing_patterns)
        except ValueError as e:
            print(f"  ❌ {e}")
            return False

        # Map back to full tuples
        pattern_map = {p[1]["handle"]: p for p in add_patterns}
        sorted_patterns = [pattern_map[h] for h in sorted_handles if h in pattern_map]
    else:
        sorted_patterns = []

    # 2c. Add patterns via mint_pattern
    from ..core.mint import mint_pattern

    for file_path, data in sorted_patterns:
        mint_result = mint_pattern(data, store)
        if mint_result.success:
            print(f"  ✓ Added {mint_result.sema_ref}")

            # Write hash back to file (CLI-specific: persist hashes to source)
            try:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                print(f"  ⚠️  Could not update file {file_path}: {e}")
        else:
            err_msg = "; ".join(mint_result.errors)
            print(f"  ❌ Failed to add {data['handle']}: {err_msg}")
            return False

    # ============ POST-APPLY SWEEP ============
    # Topological sort orders by hard dependencies; _meta.related is a
    # soft link and doesn't participate. A pattern whose related target
    # is minted AFTER it silently gets no RELATED_TO edge at apply time.
    # Sweep once the full batch is loaded to catch those.
    if add_patterns:
        swept = store.sweep_related_edges()
        if swept:
            print(
                f"  ↔ Swept {swept} RELATED_TO edge(s) that the per-pattern apply couldn't create"
            )

    # ============ DONE ============
    total_removed = len(remove_handles)
    total_added = len(add_patterns)
    print(f"\nDone. {total_removed} removed, {total_added} added.")
    return True


def _validate_pattern_file(file_path: Path) -> dict:
    """Validate a single pattern file. Returns {error, data, hash}."""
    try:
        with open(file_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON in {file_path}: {e}", "data": None}
    except Exception as e:
        return {"error": f"Cannot read {file_path}: {e}", "data": None}

    # Validate required fields
    is_valid, val_errors, val_warnings = validate_pattern(data)
    if not is_valid:
        return {
            "error": f"Validation failed for {file_path}: {'; '.join(val_errors)}",
            "data": None,
        }

    return {"error": None, "data": data}


def search_patterns(query, use_semantic=False, verbose=False, as_json=False):
    print(f"🔍 Semantic Search for: '{query}'...")
    manager = get_registry()
    results = manager.search(query, use_semantic=use_semantic)

    if as_json:
        full_results = []
        for i, r in enumerate(results):
            raw_handle = r["handle"].split("#")[0]
            pattern = manager.get_pattern(raw_handle)
            if pattern:
                pattern["_search_score"] = r.get("score")
                pattern["_search_source"] = r.get("source")
                # Enrich top 3 with neighbors (same as MCP)
                if i < 3:
                    context = manager.get_context(raw_handle)
                    if context["dependencies"] or context["used_by"]:
                        pattern["graph_context"] = context
                # Compact to remove empty fields
                full_results.append(compact_dict(pattern))
        print(json.dumps(full_results, indent=2))
        return

    if results:
        print(f"  Found {len(results)} matches:")
        for r in results:
            score = r.get("score", 0)
            score_str = f" [Score: {score:.2f}]" if score > 0 else ""
            source = r.get("source", "unknown")
            source_str = f" ({source})" if source != "keyword" else ""
            print(f"  - {r['handle']}{score_str}{source_str}")
            print(f"    Gloss: {r['gloss']}")
            if verbose:
                print(f"    Mechanism: {r['mechanism']}")
                print(f"    Layer: {r['layer']}")
                print(f"    Category: {r['category']}")
                print(f"    Sema ID: {r['sema_ref']}")
                print("")
    else:
        print("  No matches found.")


def _strip_stub(handle: str) -> str:
    """Accept both bare handles ('Stigmergy') and stub-suffixed forms
    ('Stigmergy#f624' or even full sema IDs), and return the bare handle."""
    if not handle:
        return handle
    if handle.startswith("sema:"):
        handle = handle[5:]
    return handle.split("#", 1)[0]


def resolve_graph(handle):
    bare_handle = _strip_stub(handle)
    print(f"🕸️  Resolving Subgraph for: '{bare_handle}'...")
    manager = get_registry()
    subgraph = manager.resolve(bare_handle, depth=1)
    if not subgraph:
        print(f"❌ Pattern '{bare_handle}' not found or could not be resolved.")
        # Non-zero exit so scripts and shell pipelines can detect the failure.
        sys.exit(1)
    print(f"✅ Resolved Context ({len(subgraph)} patterns):")
    for k in subgraph.keys():
        print(f"  - {k}")
    return subgraph


def show_pattern(handle):
    """Print a pattern's full body: mechanism, invariants, pre/post conditions,
    failure modes, parameters, and dependencies. This is the primary read-path
    for literate-semantics use: 'give me the definition behind this inline ref'."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text

        _rich = True
        console = Console()
    except ImportError:
        _rich = False
        console = None

    bare_handle = _strip_stub(handle)
    manager = get_registry()
    pattern = manager.get_pattern(bare_handle)
    if not pattern:
        print(f"❌ Pattern '{bare_handle}' not found.")
        # Non-zero exit so scripts and shell pipelines can detect the failure.
        sys.exit(1)

    # Title with sema_ref if available
    ref = pattern.get("sema_ref") or bare_handle
    title = f"{ref}"

    def _print_field(label, value):
        if value is None or value == "" or value == [] or value == {}:
            return
        if _rich:
            console.print(f"[bold cyan]{label}[/bold cyan]")
            if isinstance(value, list):
                for item in value:
                    console.print(f"  • {item}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    console.print(f"  [dim]{k}[/dim]: {v}")
            else:
                console.print(f"  {value}")
            console.print()
        else:
            print(f"{label}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  • {item}")
            elif isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {value}")
            print()

    if _rich:
        console.print(Panel(Text(title, style="bold green"), expand=False))
        meta = pattern.get("_meta", {})
        if meta:
            layer = meta.get("layer", "—")
            category = meta.get("category", "—")
            tier = meta.get("tier", "—")
            console.print(
                f"[dim]Layer:[/dim] {layer}  "
                f"[dim]Category:[/dim] {category}  "
                f"[dim]Tier:[/dim] {tier}"
            )
            console.print()
    else:
        print(f"=== {title} ===")
        print()

    _print_field("Gloss", pattern.get("gloss"))
    _print_field("Mechanism", pattern.get("mechanism"))
    _print_field("Signature", pattern.get("signature"))
    _print_field("Invariants", pattern.get("invariants"))
    _print_field("Preconditions", pattern.get("preconditions"))
    _print_field("Postconditions", pattern.get("postconditions"))
    _print_field("Failure modes", pattern.get("failure_modes"))
    _print_field("Parameters", pattern.get("parameters"))

    deps = pattern.get("dependencies") or {}
    if deps:
        if _rich:
            console.print("[bold cyan]Dependencies[/bold cyan]")
        else:
            print("Dependencies:")
        for section in ("references", "composes_with", "accepts", "yields"):
            section_deps = deps.get(section) or {}
            if not section_deps:
                continue
            if _rich:
                console.print(f"  [dim]{section}[/dim]")
            else:
                print(f"  {section}")
            for key, ref_str in section_deps.items():
                # Shorten sema:Handle#mh:SHA-256:hash to Handle#stub
                short = ref_str
                if short.startswith("sema:"):
                    short = short[5:]
                if "#mh:SHA-256:" in short:
                    name, _, hashpart = short.partition("#mh:SHA-256:")
                    short = f"{name}#{hashpart[:4]}"
                if _rich:
                    console.print(f"    {key} → [green]{short}[/green]")
                else:
                    print(f"    {key} → {short}")
        if _rich:
            console.print()

    if _rich:
        console.print(f"[dim]ID: {pattern.get('sema_id', '—')}[/dim]")
    else:
        print(f"ID: {pattern.get('sema_id', '—')}")

    return pattern


def show_skeleton():
    manager = get_registry()
    print("🕸️  Graph Skeleton:")
    print(manager.get_graph_skeleton())


def _compute_active_vocabulary_root(db_path: str) -> tuple[str, int]:
    """Return (root_hash, pattern_count) for the given DB path.

    Hashes are collected in ascending-by-handle order so two DBs with the
    same pattern set always produce the same root regardless of insertion
    order.
    """
    from ..core.hashing import vocabulary_root
    from ..taxonomy_graph.graph_store import GraphStore, NodeType

    store = GraphStore(db_path)
    rows = []
    for _nid, data in store.get_nodes_by_type(NodeType.PATTERN):
        handle = data.get("text")
        pattern = data.get("metadata", {}).get("pattern", {})
        sema_id = pattern.get("sema_id", "")
        if handle and "#mh:SHA-256:" in sema_id:
            rows.append((handle, sema_id.split("#mh:SHA-256:")[1]))
    rows.sort(key=lambda r: r[0])
    hashes = [h for _, h in rows]
    return vocabulary_root(hashes), len(hashes)


def vocab_root(short: bool = False) -> bool:
    """Compute and print the vocabulary-wide Merkle root for the active DB.

    Same algorithm as `scripts/vocabulary_merkle_root.py` — SHA-256 over
    the concatenation of every pattern's hash, sorted by handle.
    """
    from ..core.hashing import HASH_ALGO

    db = get_default_db_path()
    if not db:
        print("❌ No active database.")
        return False
    if not Path(db).exists():
        print(f"❌ Database does not exist: {db}")
        return False

    try:
        root, count = _compute_active_vocabulary_root(db)
    except Exception as e:
        print(f"❌ Failed to compute vocabulary root: {e}")
        return False

    if short:
        print(root[:16])
    else:
        print(f"sema:vocab#mh:{HASH_ALGO}:{root}")
        print(f"patterns: {count}")
        print(f"db: {db}")
    return True


def undo_pull() -> bool:
    """Restore the active DB from the pre-pull snapshot.

    Uses `sqlite3.Connection.backup()` to safely overwrite the live DB
    regardless of WAL state — a plain `cp` would leave an orphaned -wal
    file that SQLite would replay over the restored content and corrupt
    the Merkle DAG.
    """
    target_db = get_default_db_path()
    if not target_db:
        print("❌ No active database.")
        return False

    previous_path = target_db + ".pull_previous"
    if not os.path.exists(previous_path):
        print(f"❌ No previous pull snapshot at {previous_path}.")
        print("   (Snapshots are created after each successful pull that changed something.)")
        return False

    print(f"Restoring {target_db} from {previous_path}...")
    try:
        with (
            closing(sqlite3.connect(previous_path)) as src_conn,
            closing(sqlite3.connect(target_db)) as dst_conn,
        ):
            src_conn.backup(dst_conn)
    except sqlite3.Error as e:
        # Locked DB / permission issue: preserve the snapshot for retry.
        print(f"❌ Failed to restore database (is it locked by another agent?): {e}")
        return False
    # Snapshot consumed only on successful restore. Tolerate Windows
    # PermissionError (file indexer holding the snapshot) — the restore
    # itself already succeeded, so this is just a cleanup hiccup.
    try:
        os.remove(previous_path)
    except OSError as e:
        print(f"⚠️  Database restored, but could not delete snapshot file: {e}")
    print("✅ Restored database to pre-pull state.")
    return True


def _load_exclusions() -> set[str]:
    """Read user's pull exclusion list.

    Location: $XDG_CONFIG_HOME/sema/excluded if XDG_CONFIG_HOME is set,
    else ~/.config/sema/excluded.

    Format: one handle per line. Blank lines and lines starting with '#'
    are ignored. Excluded handles are skipped during sema pull, so a user
    can permanently opt out of an upstream pattern they previously deleted
    (or pin a local-only version — see version-pinning behavior in pull).
    """
    xdg = os.environ.get("XDG_CONFIG_HOME")
    config_dir = Path(xdg) / "sema" if xdg else Path.home() / ".config" / "sema"
    excluded_file = config_dir / "excluded"
    if not excluded_file.is_file():
        return set()
    handles = set()
    for line in excluded_file.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            handles.add(line)
    return handles


def update_db(
    source: str = None,
    dry_run: bool = False,
    verify: bool = False,
    exclude: list[str] | None = None,
    preserve_superseded: bool = False,
) -> dict:
    """Pull latest vocabulary: walk upstream DAG in topological order, update each.

    Atomicity: the entire pull runs inside a single SQLite transaction. If
    anything fails partway, the target DB is rolled back to pre-pull state.

    For each upstream pattern (leaves first, roots last):
      - Fast-path: if upstream sema_id == target sema_id, skip.
      - If handle exists in target: deep-merge user's local _meta over upstream
        defaults, then re-mint. User annotations (caution, related) survive.
      - If handle is new: add it.
      - skip_cascade=True during the loop avoids O(N^2) write amplification;
        a single cascade sweep runs at the end keyed off changed handles.

    User-only patterns are left untouched. Their hashes cascade automatically
    when their upstream deps change (via the final sweep).

    Returns a structured dict with success flag, counts, full handle lists for
    each category (added/updated/skipped/cascaded_user/superseded_removed/
    superseded_kept_orphan/upstream_removed), and vocabulary_root_before /
    vocabulary_root_after so MCP callers can act on the outcome programmatically.
    """
    from ..core.dependencies import topological_sort
    from ..core.hashing import extract_handle_from_ref, vocabulary_info
    from ..core.mint import mint_pattern
    from ..taxonomy_graph.graph_store import GraphStore, NodeType

    outcome: dict = {
        "success": False,
        "dry_run": dry_run,
        "added": [],
        "updated": [],
        "skipped": [],
        "cascaded_user": [],
        "superseded_removed": [],
        "superseded_kept_orphan": [],
        "upstream_removed": [],
        "vocabulary_root_before": None,
        "vocabulary_root_after": None,
    }

    target_db = get_default_db_path()
    if not target_db:
        print("❌ No active database. Run `sema build` or `sema use` first.")
        outcome["error"] = "No active database. Run `sema build` or `sema use` first."
        return outcome

    if is_bundled_db(target_db):
        print("❌ Cannot pull into bundled DB — it's read-only.")
        print("   Run `sema build my.db --preset full` then `sema use my.db` first.")
        outcome["error"] = "Cannot pull into bundled DB — it's read-only."
        return outcome

    source_db = source or get_bundled_db_path()
    if not source_db:
        print("❌ No source database found.")
        outcome["error"] = "No source database found."
        return outcome

    if source_db == target_db:
        print("❌ Source and target are the same database.")
        outcome["error"] = "Source and target are the same database."
        return outcome

    try:
        outcome["vocabulary_root_before"] = vocabulary_info(target_db).get("root")
    except Exception:
        pass

    print(f"Upstream: {source_db}")
    print(f"Active:   {target_db}")
    try:
        from ..core.hashing import format_load_line

        print(format_load_line(vocabulary_info(target_db)))
    except Exception:
        pass

    # Build exclusion set: file + CLI args. Pull will not touch excluded
    # handles — this is the user's "I deleted this and meant it" knob.
    excluded = _load_exclusions() | set(exclude or [])

    source_store = GraphStore(source_db)

    upstream_patterns = {}
    upstream_sema_ids = {}  # handle -> stored sema_id (for fast-path skip)
    # Capture FULL upstream handle set in the same iteration so excluded
    # handles aren't falsely reported as "upstream removed" later.
    upstream_all_handles = set()
    for _nid, data in source_store.get_nodes_by_type(NodeType.PATTERN):
        h = data.get("text")
        if not h:
            continue
        upstream_all_handles.add(h)
        if h in excluded:
            continue
        meta = data.get("metadata", {})
        pattern = meta.get("pattern", {})
        if pattern:
            pattern["handle"] = h
            edge_deps = source_store.get_dependencies_from_edges(h)
            if edge_deps:
                pattern["dependencies"] = edge_deps
            upstream_patterns[h] = pattern
            upstream_sema_ids[h] = pattern.get("sema_id", "")

    target_store = GraphStore(target_db)
    target_handles = set()
    target_local_meta = {}  # handle -> user's local _meta (preserved on update)
    target_sema_ids = {}  # handle -> stored sema_id (for fast-path skip)
    for _nid, data in target_store.get_nodes_by_type(NodeType.PATTERN):
        h = data.get("text")
        if not h:
            continue
        target_handles.add(h)
        meta = data.get("metadata", {})
        local_pattern = meta.get("pattern", {}) or {}
        target_local_meta[h] = local_pattern.get("_meta", {})
        target_sema_ids[h] = local_pattern.get("sema_id", "")

    # Pre-flight transitive pruning: an upstream pattern can't be minted if
    # one of its deps doesn't exist in either the target DB or this batch.
    # Without this, a single excluded foundational pattern (e.g. Task) would
    # cascade-fail every dependent and abort the whole pull — forcing the
    # user to add 150 entries to their exclusion file one at a time.
    #
    # Elegant property: we only prune when the dep is missing from BOTH
    # sides. If the user excludes Foo BUT keeps a local copy in target,
    # dependents resolve against their local Foo — so exclusion + local-keep
    # acts as a "version pin" against upstream changes.
    auto_skipped = set()
    while True:
        round_pruned = set()
        for h, p in list(upstream_patterns.items()):
            for items in p.get("dependencies", {}).values():
                if not isinstance(items, dict):
                    continue
                for ref in items.values():
                    if not isinstance(ref, str):
                        continue
                    target_handle = extract_handle_from_ref(ref)
                    # Self-references are implicitly safe: h is still in
                    # upstream_patterns at this point, so target_handle == h
                    # passes the third check. We also leave the loop running
                    # even when `excluded` is empty — it doubles as a
                    # protector against malformed upstream graphs that ship
                    # with dangling refs.
                    if (
                        target_handle not in target_handles
                        and target_handle not in upstream_patterns
                    ):
                        round_pruned.add(h)
                        break
                if h in round_pruned:
                    break
        if not round_pruned:
            break
        for h in round_pruned:
            auto_skipped.add(h)
            del upstream_patterns[h]
            upstream_sema_ids.pop(h, None)

    new_count = len(upstream_patterns.keys() - target_handles)
    update_count = len(upstream_patterns.keys() & target_handles)
    # Use the unfiltered upstream set so excluded handles aren't falsely
    # reported as "upstream removed".
    upstream_removed = sorted(target_handles - upstream_all_handles)

    print(f"\nUpstream: {len(upstream_patterns)} patterns")
    print(f"Target:   {len(target_handles)} patterns")
    print(f"  New: {new_count}, Update: {update_count}")
    if excluded:
        print(f"  Excluded: {len(excluded)} handle(s) skipped per user opt-out")
        dormant = excluded - upstream_all_handles
        if dormant:
            print(
                f"  ℹ️  {len(dormant)} dormant exclusion(s) (no longer present upstream): "
                f"{', '.join(sorted(dormant)[:5])}"
            )
    if auto_skipped:
        print(
            f"⚠️  Auto-skipped {len(auto_skipped)} pattern(s) — their deps are excluded "
            f"or absent locally:"
        )
        for h in sorted(auto_skipped)[:10]:
            print(f"    {h}")

    try:
        sorted_handles = topological_sort(upstream_patterns)
    except ValueError as e:
        print(f"❌ Dependency cycle in upstream: {e}")
        outcome["error"] = f"Dependency cycle in upstream: {e}"
        return outcome

    if dry_run:
        print(f"\nWould apply {len(sorted_handles)} patterns in topological order.")
        if upstream_removed:
            print(f"User-only patterns (no longer in upstream): {len(upstream_removed)}")

        # Populate dry-run stats: added / updated splits, plus a supersedes
        # preview (pure analysis — no DB writes). This lets MCP callers decide
        # whether to run the real pull without executing it.
        outcome["added"] = sorted(upstream_patterns.keys() - target_handles)
        outcome["updated"] = sorted(upstream_patterns.keys() & target_handles)
        outcome["upstream_removed"] = list(upstream_removed)
        if not preserve_superseded:
            preview: dict[str, list[str]] = {}
            for u_handle, u_pattern in upstream_patterns.items():
                for old_sid in (u_pattern.get("_meta") or {}).get("supersedes") or []:
                    preview.setdefault(old_sid, []).append(u_handle)
            for _nid, data in target_store.get_nodes_by_type(NodeType.PATTERN):
                local_sid = data.get("metadata", {}).get("pattern", {}).get("sema_id", "")
                local_handle = data.get("text")
                if (
                    local_sid
                    and local_sid in preview
                    and local_handle
                    and local_handle not in upstream_patterns
                ):
                    outcome["superseded_removed"].append((local_handle, preview[local_sid]))
        outcome["success"] = True
        return outcome

    # Atomicity via SQLite's native backup API. Unlike `shutil.copy2`, this
    # safely captures DB state regardless of WAL mode (the WAL file would
    # otherwise leave a torn snapshot that, when restored, would replay over
    # the rolled-back DB and corrupt the Merkle DAG).
    #
    # NOTE: `with sqlite3.connect()` only manages the *transaction*, not the
    # connection lifecycle — connections stay open after the block, holding
    # locks. We use `contextlib.closing` to guarantee cleanup so the backup
    # file can be deleted afterward (matters on Windows, leak on POSIX).
    backup_path = target_db + ".pull_bak"
    if os.path.exists(backup_path):
        # A stranded .pull_bak means a prior pull suffered a catastrophic
        # rollback failure. Don't overwrite it — that would destroy the
        # user's only recoverable state. Abort and ask them to intervene.
        print(f"❌ Stranded backup found at {backup_path}")
        print("   A previous pull crashed critically during rollback. The backup may")
        print("   represent your only recoverable pre-pull state. To resolve:")
        print(f"     1. If you know your DB is healthy, delete {backup_path}")
        print("     2. If not, restore from it: sqlite3 backup API or manual inspection")
        print("   Aborting to protect your data.")
        outcome["error"] = f"Stranded backup at {backup_path} from a prior failed pull"
        return outcome
    # If the target DB is locked (e.g. another agent is mid-write), backup()
    # raises sqlite3.OperationalError. Without this guard, the partial 0-byte
    # `.pull_bak` file from the with-block would remain on disk and the next
    # pull would mistake it for a stranded backup from a catastrophic
    # rollback failure — terrifying false positive. Catch + cleanup.
    try:
        with (
            closing(sqlite3.connect(target_db)) as src_conn,
            closing(sqlite3.connect(backup_path)) as bak_conn,
        ):
            src_conn.backup(bak_conn)
    except sqlite3.Error as e:
        print(f"❌ Could not create pre-pull backup (is the database locked?): {e}")
        if os.path.exists(backup_path):
            try:
                os.remove(backup_path)
            except OSError:
                # Antivirus / file indexer might briefly hold the 0-byte
                # file. Tell the user explicitly — otherwise their next
                # pull will see this file and falsely report "stranded
                # backup from catastrophic rollback failure", a terrifying
                # jump-scare for what was actually a transient lock.
                print(f"⚠️  Note: Please manually delete the empty {backup_path} file.")
        outcome["error"] = f"Could not create pre-pull backup: {e}"
        return outcome

    added = []
    updated = []
    skipped = []
    failed = []
    cascaded_user = set()

    try:
        # Field-level merge policy for the unhashed _meta block:
        # - User OWNS these keys: caution, related (their personal annotations)
        # - Upstream OWNS everything else: layer, category, tier, ring, supersedes
        #   (taxonomy reorganizations propagate to users — paper §3.2 "Mutable Overlay")

        for handle in sorted_handles:
            pattern = upstream_patterns[handle]
            existed = handle in target_handles

            # Build merged _meta: start with upstream, layer user-owned keys on top.
            # `related` is a list — union, preserving order (upstream first).
            merged_meta = dict(pattern.get("_meta", {}))
            if existed and target_local_meta.get(handle):
                local = target_local_meta[handle]
                if "caution" in local:
                    merged_meta["caution"] = local["caution"]
                if "related" in local and isinstance(local["related"], list):
                    upstream_related = merged_meta.get("related", []) or []
                    # Defensive: if upstream data is malformed (e.g. a string
                    # instead of a list), coerce before unioning.
                    if isinstance(upstream_related, str):
                        upstream_related = [upstream_related]
                    merged_meta["related"] = list(
                        dict.fromkeys(list(upstream_related) + list(local["related"]))
                    )
            pattern = {**pattern, "_meta": merged_meta}

            # Fast-path: skip mint only if BOTH the semantic hash matches
            # AND the merged _meta equals the stored _meta. This catches
            # taxonomy-only changes (layer/category) — they don't change
            # the sema_id but DO need to update the IN_CATEGORY edges.
            if existed and upstream_sema_ids.get(handle) == target_sema_ids.get(handle):
                if merged_meta == target_local_meta.get(handle, {}):
                    skipped.append(handle)
                    continue

            result = mint_pattern(pattern, target_store, skip_cascade=True)
            if result.success:
                if existed:
                    updated.append(handle)
                else:
                    added.append(handle)
            else:
                failed.append((handle, result.errors))

        if failed:
            raise RuntimeError(f"{len(failed)} pattern(s) failed to mint")

        # ============ SUPERSESSION CLEANUP ============
        # Upstream patterns' `_meta.supersedes` names the sema_ids of older
        # patterns that upstream has explicitly retired. If the target has a
        # pattern at one of those sema_ids, remove it — the replacement is
        # already in place from the mint loop above. `--preserve-superseded`
        # opts out (keeps both coexisting).
        #
        # CRITICAL: this MUST run BEFORE the cascade sweep below. Cascade
        # rewrites user-local patterns' sema_ids when their deps change;
        # once rewritten, the supersedes lookup wouldn't find them anymore.
        #
        # Orphan guard: if a user-only local pattern still depends on the
        # soon-to-be-removed one (via edge), don't remove — report it as
        # `superseded_kept_orphan`. The user must re-point their dependents
        # (or opt in to `--preserve-superseded`) before the cleanup fires.
        superseded_removed = []  # (old_handle, [successor_handles])
        superseded_kept_orphan = []  # (old_handle, [successor_handles], [user_dependents])

        # Snapshot orphan-sub-node count before cleanup so we can report a
        # delta afterwards. Pattern deletion doesn't GC the invariant /
        # precondition / postcondition nodes that become unreachable — we
        # notify but don't auto-remove.
        def _count_isolated_subs():
            return (
                sqlite3.connect(target_db)
                .execute(
                    """
                SELECT COUNT(*) FROM nodes n
                WHERE n.node_type IN ('INVARIANT', 'PRECONDITION', 'POSTCONDITION')
                  AND NOT EXISTS (
                      SELECT 1 FROM edges e
                      WHERE e.source_id=n.id OR e.target_id=n.id
                  )
                """
                )
                .fetchone()[0]
            )

        orphan_subs_before = _count_isolated_subs()
        if not preserve_superseded:
            # Build reverse map: old_sema_id -> list of upstream handles that supersede it
            supersedes_to_successors = {}
            for u_handle, u_pattern in upstream_patterns.items():
                for old_sid in (u_pattern.get("_meta") or {}).get("supersedes") or []:
                    supersedes_to_successors.setdefault(old_sid, []).append(u_handle)

            # Find local patterns whose sema_id matches a superseded entry.
            # Iterate a snapshot because we'll mutate the DB during removal.
            to_remove = []
            for nid, data in list(target_store.get_nodes_by_type(NodeType.PATTERN)):
                local_sid = data.get("metadata", {}).get("pattern", {}).get("sema_id", "")
                if not local_sid or local_sid not in supersedes_to_successors:
                    continue
                local_handle = data.get("text")
                if not local_handle:
                    continue
                # If upstream also carries this handle (not a rename, just a
                # content edit), we don't remove — mint already updated it
                # in place. Supersession cleanup targets handles that are
                # gone from upstream but present locally at an old hash.
                if local_handle in upstream_patterns:
                    continue
                successors = supersedes_to_successors[local_sid]
                to_remove.append((nid, local_handle, successors))

            for nid, old_h, successors in to_remove:
                # Orphan guard: user-only dependents of this pattern?
                user_dependents = [
                    dep
                    for dep in target_store.get_dependents(old_h)
                    if dep not in upstream_patterns
                ]
                if user_dependents:
                    superseded_kept_orphan.append((old_h, successors, user_dependents))
                    continue
                # Safe to remove
                result = target_store.delete_node_cascade(nid)
                if result.get("success"):
                    superseded_removed.append((old_h, successors))
                    # Remove from target_handles so it doesn't later show up
                    # as "upstream_removed" — it's already been dealt with.
                    target_handles.discard(old_h)

        # Recompute upstream_removed after supersession cleanup so handles
        # that got cleaned up don't also appear as "user-only retained."
        # (upstream_removed was computed early for the preview print; now
        # it needs to reflect the actual post-cleanup state.)
        if superseded_removed:
            removed_now = {h for h, _ in superseded_removed}
            upstream_removed = sorted(set(upstream_removed) - removed_now)

        # How many new orphan sub-nodes did the cleanup leave behind?
        orphan_subs_new = _count_isolated_subs() - orphan_subs_before

        # Single cascade sweep over actually-changed upstream handles.
        # This catches user-only patterns whose deps just got new hashes.
        for handle in added + updated:
            cascade = target_store._cascade_dependents(handle)
            for dep in cascade.get("updated", []):
                if dep not in upstream_patterns:
                    cascaded_user.add(dep)

    except (Exception, KeyboardInterrupt) as e:
        # Roll back: restore the DB from backup via SQLite's backup API
        # (safe with WAL mode, unlike shutil.move). Use closing() so the
        # connections are fully closed before we try to remove the backup.
        # KeyboardInterrupt inherits from BaseException, not Exception, so
        # we catch it explicitly — otherwise Ctrl+C bypasses rollback and
        # leaves a stranded `.pull_bak` that the next run refuses to clobber.
        err_msg = "user interrupted (Ctrl+C)" if isinstance(e, KeyboardInterrupt) else str(e)
        print(f"\n❌ Pull aborted: {err_msg}")
        print("   Attempting to restore target DB from backup...")
        try:
            with (
                closing(sqlite3.connect(backup_path)) as bak_conn,
                closing(sqlite3.connect(target_db)) as dst_conn,
            ):
                bak_conn.backup(dst_conn)
            os.remove(backup_path)
            print("✅ Target DB restored from backup.")
        except (Exception, KeyboardInterrupt) as rollback_err:
            # Critical: if rollback itself fails, the backup is the user's
            # only remaining copy of the pre-pull state. Do NOT delete it.
            # Next pull will detect the stranded .pull_bak and refuse to
            # proceed, prompting the user to recover manually.
            #
            # KeyboardInterrupt explicitly: a panicked user mashing Ctrl+C
            # would otherwise hit the C-based sqlite backup() with a fresh
            # interrupt, bypass this handler, and never see the manual
            # recovery instructions — exactly when they need them most.
            err_str = (
                "user interrupted"
                if isinstance(rollback_err, KeyboardInterrupt)
                else str(rollback_err)
            )
            print(f"🚨 CRITICAL: Automatic rollback failed ({err_str})")
            print("   Your database may be in an inconsistent state.")
            print(f"   Your pre-pull backup is preserved at: {backup_path}")
            print("   To recover manually, restore from that file (sqlite3 backup API).")
        if failed:
            for h, errs in failed[:5]:
                print(f"    {h}: {'; '.join(errs)}")
        outcome["error"] = err_msg
        if failed:
            outcome["failed"] = [(h, errs) for h, errs in failed]
        return outcome

    # Success path — promote the backup to `.pull_previous` if something
    # actually changed, so the user can `sema pull --undo` to recover.
    # On a no-op pull (all fast-path skipped), discard this backup to keep
    # the older, genuinely-useful `.pull_previous` intact.
    has_changes = bool(added or updated or cascaded_user or superseded_removed)
    try:
        if has_changes:
            previous_path = target_db + ".pull_previous"
            os.replace(backup_path, previous_path)
        else:
            os.remove(backup_path)
    except OSError as e:
        # Another program (DB viewer, indexer) might have the file open on
        # Windows, causing PermissionError. The pull itself succeeded —
        # just warn about the stranded cleanup, don't fail.
        print(f"\n⚠️  Could not finalize backup file: {e}")
        print(f"   If {backup_path} lingers, close any program accessing it and delete manually.")

    # Reporting
    if added:
        print(f"  + {len(added)} new")
    if updated:
        print(f"  ~ {len(updated)} updated")
    if skipped:
        print(f"  = {len(skipped)} unchanged (fast-path)")
    # Full lists — primary consumer is an agent that may want to act on
    # every name. A human can still scan. No silent truncation.
    if cascaded_user:
        print(
            f"⚠️  {len(cascaded_user)} user pattern(s) had hashes auto-updated due to upstream changes:"
        )
        for h in sorted(cascaded_user):
            print(f"    {h}")
    if superseded_removed:
        print(f"→ {len(superseded_removed)} pattern(s) superseded by upstream, removed locally:")
        for old_h, new_handles in superseded_removed:
            print(f"    {old_h:<22} → {', '.join(new_handles)}")
    if superseded_kept_orphan:
        print(
            f"⚠️  {len(superseded_kept_orphan)} supersession(s) NOT applied — your patterns "
            "still depend on them:"
        )
        for old_h, new_handles, deps in superseded_kept_orphan:
            print(f"    {old_h:<22} → {', '.join(new_handles)}  (blocked by: {', '.join(deps)})")
        print(
            "    A rename replaces a pattern's *handle* (not just its hash), so cascade "
            "cannot bridge the reference automatically — the old and new patterns are "
            "separate nodes. To apply the supersession:"
        )
        print("      1. Edit your dependent patterns to reference the successor handle, OR")
        print("      2. Pass --preserve-superseded to keep both handles coexisting, OR")
        print("      3. Delete the dependent patterns if they're no longer needed.")
        print("    Then re-run `sema pull`.")
    if upstream_removed:
        print(
            f"ℹ️  Upstream removed {len(upstream_removed)} pattern(s); they remain locally as user patterns:"
        )
        for h in upstream_removed:
            print(f"    {h}")
    if orphan_subs_new > 0:
        print(
            f"ℹ️  {orphan_subs_new} orphan sub-node(s) (invariants/pre/postconditions) "
            "left behind by supersession cleanup. They don't affect queries but likely "
            "want cleaning up in a future pass:"
        )
        # Fetch the actual orphan texts so the caller (agent or human) knows
        # what's dangling. Same query as _count_isolated_subs but returning rows.
        with closing(sqlite3.connect(target_db)) as _c:
            orphan_rows = _c.execute(
                """
                SELECT node_type, text FROM nodes n
                WHERE n.node_type IN ('INVARIANT', 'PRECONDITION', 'POSTCONDITION')
                  AND NOT EXISTS (
                      SELECT 1 FROM edges e
                      WHERE e.source_id=n.id OR e.target_id=n.id
                  )
                """
            ).fetchall()
        for nt, text in orphan_rows:
            truncated = (text[:70] + "…") if len(text) > 70 else text
            print(f"    [{nt}] {truncated}")

    # User-owned patterns retained across this pull (i.e. present locally
    # but absent from upstream) are never rewritten by pull. If any of
    # them still carry pre-0.2.0 `_meta.layer` + `_meta.category` instead
    # of `_meta.path`, the next `sema apply` would reject them against
    # the strict path-based schema. Warn, don't fix — the user owns
    # these patterns and the migration is a content decision.
    if upstream_removed:
        with closing(sqlite3.connect(target_db)) as _c:
            stale_meta = []
            for handle in upstream_removed:
                row = _c.execute(
                    """
                    SELECT json_extract(metadata, '$.pattern._meta')
                    FROM nodes WHERE node_type='PATTERN' AND text=?
                    """,
                    (handle,),
                ).fetchone()
                if not row or not row[0]:
                    continue
                try:
                    meta = json.loads(row[0])
                except Exception:
                    continue
                if not isinstance(meta, dict):
                    continue
                # Missing path AND has legacy layer/category — stale.
                if "path" not in meta and ("layer" in meta or "category" in meta):
                    stale_meta.append(handle)
        if stale_meta:
            print(
                f"⚠️  {len(stale_meta)} retained user pattern(s) carry pre-0.2.0 "
                "_meta (layer+category) and will FAIL `sema apply` validation "
                "until migrated to _meta.path:"
            )
            for h in stale_meta:
                print(f"    {h}")
            print(
                "    Run `python3 scripts/migrate_taxonomy_to_path.py` against the "
                "JSONs, or edit each pattern's _meta to use `path: [<layer>, "
                "<category>]`."
            )

    print(
        f"\n✅ Pull complete. {len(added)} added, {len(updated)} updated, {len(skipped)} unchanged."
    )
    if has_changes:
        print("ℹ️  Pre-pull snapshot saved. Run `sema pull --undo` to revert.")

    outcome["added"] = list(added)
    outcome["updated"] = list(updated)
    outcome["skipped"] = list(skipped)
    outcome["cascaded_user"] = sorted(cascaded_user)
    outcome["superseded_removed"] = [(h, list(n)) for h, n in superseded_removed]
    outcome["superseded_kept_orphan"] = [
        (h, list(n), list(d)) for h, n, d in superseded_kept_orphan
    ]
    outcome["upstream_removed"] = list(upstream_removed)
    try:
        outcome["vocabulary_root_after"] = vocabulary_info(target_db).get("root")
    except Exception:
        pass

    if verify:
        invalid = _verify_hashes(target_db)
        if invalid:
            print(f"\n❌ Hash validity check failed: {len(invalid)} invalid patterns")
            for h in invalid[:5]:
                print(f"    {h}")
            outcome["error"] = f"{len(invalid)} pattern(s) failed hash verification"
            outcome["invalid_hashes"] = list(invalid)
            return outcome
        print("✓ Hash validity verified.")
        outcome["verified"] = True

    outcome["success"] = True
    return outcome


def _verify_hashes(db_path: str) -> list[str]:
    """Verify stored sema_ids match recomputed hashes via bottom-up traversal.

    Computes from leaves up, keeping a cache of *freshly computed* hashes.
    Parents resolve their dep refs against the cache (true hashes), not
    against potentially-corrupted stored values. This catches the case
    where a child's stored hash is stale and a parent self-validates against
    the corruption.
    """
    from ..core.dependencies import topological_sort
    from ..core.hashing import generate_sema_hash
    from ..taxonomy_graph.graph_store import GraphStore, NodeType

    store = GraphStore(db_path)
    patterns = {}
    for _, data in store.get_nodes_by_type(NodeType.PATTERN):
        h = data.get("text")
        if not h:
            continue
        meta = data.get("metadata", {})
        p = meta.get("pattern", {}) or {}
        p["handle"] = h
        deps = store.get_dependencies_from_edges(h)
        if deps:
            p["dependencies"] = deps
        patterns[h] = p

    stored = {}
    for h, p in patterns.items():
        sid = p.get("sema_id", "")
        if "#mh:SHA-256:" in sid:
            stored[h] = sid.split("#mh:SHA-256:")[1]

    # Topo-sort gives us leaves-first ordering; compute hashes in that order
    # so by the time we hash a parent, all its dep hashes are in `fresh`.
    try:
        order = topological_sort(patterns)
    except ValueError:
        # Cycle — fall back to stored-hash lookup (best effort)
        order = list(patterns.keys())

    fresh = {}
    mismatches = []

    def lookup(h):
        # Prefer freshly computed hash (bottom-up correctness); fall back
        # to stored only for handles outside this batch.
        return fresh.get(h, stored.get(h))

    for handle in order:
        p = patterns[handle]
        if handle not in stored:
            continue
        computed = generate_sema_hash(p, lookup)["hash"]
        fresh[handle] = computed
        if computed != stored[handle]:
            mismatches.append(handle)
    return mismatches


def use_db(path: str = None, default: bool = False):
    """Switch the active DB or reset to default."""
    if default:
        set_active_db(None)
        bundled = get_bundled_db_path()
        print(f"✅ Switched to default vocabulary ({bundled})")
        return True

    if not path:
        # Show current
        db = get_default_db_path()
        if is_bundled_db(db):
            print(f"Using: default (bundled) — {db}")
        else:
            print(f"Using: {db}")
        return True

    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        print(f"❌ Database not found: {resolved}")
        return False

    if is_bundled_db(str(resolved)):
        print("❌ Cannot use the bundled DB as active — it gets overwritten on upgrade.")
        print("   Run `sema build my.db --preset full` to create your own copy.")
        return False

    set_active_db(str(resolved))
    register_db(str(resolved))
    count = RegistryManager(db_path=str(resolved)).count()
    print(f"✅ Switched to {resolved} ({count} patterns)")

    # Banner: show the vocabulary fingerprint right after the switch, so
    # users can verify at a glance which state they just pointed at.
    try:
        from ..core.hashing import format_load_line, vocabulary_info

        print(format_load_line(vocabulary_info(str(resolved))))
    except Exception:
        pass

    if os.environ.get("SEMA_DB_PATH"):
        print(f"⚠️  SEMA_DB_PATH is set to '{os.environ['SEMA_DB_PATH']}'")
        print(
            "   This env var takes priority. Run `unset SEMA_DB_PATH` for `sema use` to take effect."
        )
    return True


def categorize_pattern(handle: str, path_str: str) -> bool:
    """Re-categorize a pattern by rewriting its `_meta.path`. Uses the
    existing apply-path so edge re-wiring (TAXONOMY_PATH linking, IN_PATH
    edges) happens via the canonical mint logic.

    `path_str` is slash-separated, e.g. 'Physics/Primitives'. Must be in
    VALID_PATHS (enforced by the Pydantic schema).
    """
    from ..core.schema import VALID_PATHS, path_to_string
    from ..taxonomy_graph.graph_store import GraphStore, NodeType

    segments = [s for s in path_str.split("/") if s]
    if not segments:
        print(f"❌ Invalid --path '{path_str}': empty")
        return False
    if tuple(segments) not in VALID_PATHS:
        print(f"❌ Path '{path_to_string(segments)}' is not in VALID_PATHS.")
        print("   Valid paths:")
        for p in sorted(VALID_PATHS):
            print(f"     {path_to_string(list(p))}")
        return False

    db_path = get_default_db_path()
    if is_bundled_db(db_path):
        print("❌ Cannot modify the bundled vocabulary.")
        print("   Run `sema build my.db --preset full` then `sema use my.db` first.")
        return False

    store = GraphStore(db_path)
    target = None
    for _nid, data in store.get_nodes_by_type(NodeType.PATTERN):
        if data.get("text") == handle:
            target = data
            break
    if not target:
        print(f"❌ Pattern '{handle}' not found in {db_path}")
        return False

    pattern = target.get("metadata", {}).get("pattern", {}) or {}
    if not pattern:
        print(f"❌ Pattern '{handle}' has no stored content")
        return False

    # Clone + update path
    pattern = json.loads(json.dumps(pattern))  # deep copy
    pattern["handle"] = handle
    # Reconstruct dependencies from edges (canonical source)
    deps = store.get_dependencies_from_edges(handle)
    if deps:
        pattern["dependencies"] = deps
    meta = pattern.setdefault("_meta", {})
    old_path = meta.get("path") or []
    meta["path"] = segments
    # Drop any stale derived fields so mint re-derives cleanly.
    meta.pop("layer", None)
    meta.pop("category", None)
    pattern.pop("sema_layer", None)
    pattern.pop("sema_category", None)

    # Write to a temporary staging file and apply via the canonical path.
    tmp_dir = Path(db_path).parent / "staging"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_file = tmp_dir / f"{handle}.json"
    with tmp_file.open("w") as f:
        json.dump(pattern, f, indent=2, ensure_ascii=False)

    print(f"Moving {handle}: {path_to_string(old_path) or '(empty)'} → {path_to_string(segments)}")
    ok = apply_changes(add_files=[str(tmp_file)])
    # Clean up staging file on success
    if ok:
        try:
            tmp_file.unlink()
        except Exception:
            pass
    return ok


def list_databases():
    """List all known vocabulary databases."""
    dbs = list_dbs()
    if not dbs:
        print("No databases found.")
        return

    for db in dbs:
        marker = "→ " if db["active"] else "  "
        status = ""
        if not db["exists"]:
            status = " (missing)"
        elif db["bundled"]:
            status = " (read-only)"

        if db["exists"]:
            try:
                conn = sqlite3.connect(db["path"])
                count = conn.execute(
                    "SELECT COUNT(*) FROM nodes WHERE node_type='PATTERN'"
                ).fetchone()[0]
                conn.close()
                print(f"{marker}{db['name']}: {db['path']} ({count} patterns){status}")
            except sqlite3.Error:
                print(f"{marker}{db['name']}: {db['path']} (corrupted){status}")
        else:
            print(f"{marker}{db['name']}: {db['path']}{status}")


def _get_presets_dir() -> Path:
    """Find bundled presets directory."""
    pkg = Path(__file__).parent.parent / "data" / "presets"
    if pkg.exists():
        return pkg
    dev = Path(__file__).parent.parent.parent.parent / "data" / "presets"
    if dev.exists():
        return dev
    return pkg


def _read_patterns_file(path: Path) -> list[str]:
    """Read handles from a patterns file (one per line, # comments)."""
    return [
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _create_empty_db(path: Path):
    """Create DB with schema only, no data. Uses GraphStore to avoid schema drift."""
    from ..taxonomy_graph.graph_store import GraphStore

    store = GraphStore(str(path))
    if hasattr(store, "conn"):
        store.conn.close()


def build_db(dest: str, preset: str = None, patterns_file: str = None, source_db: str = None):
    """Build a project DB from a preset or patterns file.

    Copies validated nodes and edges directly from the bundled catalog —
    no re-minting, no re-hashing. Transitive dependencies are
    auto-resolved so the project DB is self-contained.
    """
    import shutil

    dest_path = Path(dest).expanduser().resolve()
    if dest_path.exists():
        print(f"❌ {dest_path} already exists. Remove it first to rebuild.")
        return False

    source_db_path = source_db or get_bundled_db_path()
    if not source_db_path or not Path(source_db_path).exists():
        print("❌ Source DB not found. Run `sema pull` first.")
        return False

    if preset:
        if preset == "full":
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_db_path, dest_path)
            count = RegistryManager(db_path=str(dest_path)).count()
            print(f"✅ Built {dest_path} (full: {count} patterns)")
            register_db(str(dest_path))
            print(f"\nTo use: sema use {dest_path}")
            return True

        if preset == "empty":
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            _create_empty_db(dest_path)
            print(f"✅ Built {dest_path} (empty: 0 patterns)")
            register_db(str(dest_path))
            print(f"\nTo use: sema use {dest_path}")
            return True

        preset_file = _get_presets_dir() / f"{preset}.txt"
        if not preset_file.exists():
            available = [f.stem for f in _get_presets_dir().glob("*.txt")]
            print(f"❌ Unknown preset '{preset}'. Available: {', '.join(available)}")
            return False
        requested = _read_patterns_file(preset_file)
    elif patterns_file:
        pf = Path(patterns_file)
        if not pf.exists():
            print(f"❌ File not found: {patterns_file}")
            return False
        requested = _read_patterns_file(pf)
    else:
        print("❌ Specify --preset or --from")
        return False

    if not requested:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        _create_empty_db(dest_path)
        print(f"✅ Built {dest_path} (empty: 0 patterns)")
        register_db(str(dest_path))
        print(f"\nTo use: sema use {dest_path}")
        return True

    source = RegistryManager(db_path=source_db_path)

    # Resolve transitive dependencies via BFS
    resolved = set()
    queue = list(requested)
    missing = []

    while queue:
        handle = queue.pop(0)
        if handle in resolved:
            continue
        if handle not in source.registry:
            if handle in requested:
                missing.append(handle)
            continue
        resolved.add(handle)
        for dep_handle in get_dependencies_handles(source.registry[handle]):
            if dep_handle not in resolved:
                queue.append(dep_handle)

    if missing:
        print(f"⚠️  Not found in source: {', '.join(missing[:10])}")
        if len(missing) > 10:
            print(f"   ...and {len(missing) - 10} more")

    if not resolved:
        print("❌ No valid patterns to build")
        return False

    # Copy nodes and edges directly from source DB
    src_conn = sqlite3.connect(source_db_path)
    src_conn.row_factory = sqlite3.Row

    pattern_node_ids = set()
    all_node_ids = set()
    cur = src_conn.cursor()

    cur.execute("SELECT id, text FROM nodes WHERE node_type = 'PATTERN'")
    for row in cur.fetchall():
        if row["text"] in resolved:
            pattern_node_ids.add(row["id"])
            all_node_ids.add(row["id"])

    if not pattern_node_ids:
        src_conn.close()
        print("❌ No matching patterns found in source DB")
        return False

    # Get all edges (filter in Python to avoid SQLite variable limits)
    cur.execute("SELECT * FROM edges")
    all_edges_raw = cur.fetchall()

    for row in all_edges_raw:
        if row["source_id"] in pattern_node_ids and row["edge_type"] in ("IN_LAYER", "IN_CATEGORY"):
            all_node_ids.add(row["target_id"])

    # CATEGORY -> LAYER edges
    cat_ids = all_node_ids - pattern_node_ids
    for row in all_edges_raw:
        if row["source_id"] in cat_ids and row["edge_type"] == "IN_LAYER":
            all_node_ids.add(row["target_id"])

    # Fetch nodes and filter edges in Python (avoids SQLite variable limits)
    cur.execute("SELECT * FROM nodes")
    nodes = [dict(row) for row in cur.fetchall() if row["id"] in all_node_ids]

    edges = [
        dict(row)
        for row in all_edges_raw
        if row["source_id"] in all_node_ids and row["target_id"] in all_node_ids
    ]
    src_conn.close()

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    _create_empty_db(dest_path)
    dst_conn = sqlite3.connect(str(dest_path))

    for node in nodes:
        dst_conn.execute(
            "INSERT INTO nodes (id, node_type, text, metadata, embedding) VALUES (?, ?, ?, ?, ?)",
            (node["id"], node["node_type"], node["text"], node["metadata"], node["embedding"]),
        )
    for edge in edges:
        dst_conn.execute(
            "INSERT INTO edges (id, source_id, target_id, edge_type, metadata) VALUES (?, ?, ?, ?, ?)",
            (edge["id"], edge["source_id"], edge["target_id"], edge["edge_type"], edge["metadata"]),
        )

    dst_conn.commit()
    dst_conn.close()

    dep_count = len(resolved) - len([h for h in requested if h in resolved])
    print(
        f"✅ Built {dest_path}: {len(resolved)} patterns "
        f"({len(resolved) - dep_count} requested + {dep_count} dependencies)"
    )
    register_db(str(dest_path))
    print(f"\nTo use: sema use {dest_path}")
    return True


def init_registry(path: str):
    """Create an empty taxonomy DB at <path>.

    Calls GraphStore(path), which auto-initializes the schema (nodes, edges,
    indexes) when given a fresh path. Prints the export line so subsequent
    `sema` commands use the new registry.
    """
    from ..taxonomy_graph.graph_store import GraphStore

    target = Path(path).expanduser().resolve()
    if target.exists():
        print(f"❌ Path already exists: {target}")
        print("   Choose a different path, or remove the existing file first.")
        return False

    target.parent.mkdir(parents=True, exist_ok=True)

    # GraphStore auto-creates schema on a fresh path
    GraphStore(str(target))

    register_db(str(target))
    print(f"✅ Created empty registry at {target}")
    print("")
    print("To use this registry:")
    print(f"  sema use {target}")
    print("")
    print("Then add patterns with:")
    print("  sema apply --add path/to/MyPattern.json")
    return True


def run_server(host="127.0.0.1", port=3000):
    try:
        import uvicorn
    except ImportError:
        print("API server requires extra dependencies. Install with:")
        print('  pip install "semahash[api]"')
        return

    from pathlib import Path

    static_dir = Path(__file__).parent.parent / "server" / "static"
    has_ui = (static_dir / "index.html").exists()

    print(f"Starting Sema Server on http://{host}:{port}")
    if has_ui:
        print(f"  UI available at http://localhost:{port}")
    else:
        print("  API only (no frontend bundled)")
        print("  For the full UI, visit https://semahash.org")
    uvicorn.run("sema.server.api:app", host=host, port=port, reload=False)


def run_mcp():
    # Loud, fast failure if the optional `mcp` dependency is missing.
    # The previous version printed to stdout and returned exit-0, which made
    # `sema mcp` look successful to a parent process (an MCP host like
    # OpenClaw bundle-mcp) while actually never starting the JSON-RPC loop.
    # The host then connects to a process that has already exited and sees
    # "MCP error -32000: Connection closed", which is a useless symptom.
    # Print to stderr, exit with non-zero, so the parent gets a real signal.
    try:
        from ..mcp.server import mcp
    except ImportError as e:
        print(
            "ERROR: sema mcp requires the optional `mcp` dependency.\n"
            "Install with:\n"
            '  pip install "semahash[mcp]"\n'
            "or with uv:\n"
            "  uv tool install 'semahash[mcp]'\n"
            f"underlying ImportError: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    mcp.run()


def _resolve_version() -> str:
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version("semahash")
    except PackageNotFoundError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Sema CLI")
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"sema (semahash) {_resolve_version()}",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Apply - atomic add/remove
    apply_cmd = subparsers.add_parser("apply", help="Atomic add/remove patterns")
    apply_cmd.add_argument(
        "--remove", "-r", action="append", default=[], help="Pattern handle to remove (can repeat)"
    )
    apply_cmd.add_argument(
        "--add", "-a", action="append", default=[], help="File or directory to add (can repeat)"
    )
    apply_cmd.add_argument(
        "--check", "-c", action="store_true", help="Validate only, don't apply changes"
    )

    # Search
    search = subparsers.add_parser("search", help="Search the registry")
    search.add_argument("query")
    search.add_argument(
        "--keyword-only",
        "-k",
        action="store_true",
        help="Disable semantic search (keyword/name matching only)",
    )
    search.add_argument("--verbose", "-v", action="store_true", help="Show details")
    search.add_argument("--json", action="store_true", help="JSON output")

    # Resolve
    resolve = subparsers.add_parser(
        "resolve",
        help="Resolve pattern dependencies (accepts 'Handle' or 'Handle#stub')",
    )
    resolve.add_argument("handle")

    # Show
    show = subparsers.add_parser(
        "show",
        help="Print a pattern's full definition (accepts 'Handle' or 'Handle#stub')",
    )
    show.add_argument("handle")

    # Skeleton
    subparsers.add_parser("skeleton", help="Show the graph skeleton")

    # Init - create an empty registry
    init_cmd = subparsers.add_parser(
        "init",
        help="Create an empty taxonomy DB at <path> (for building your own vocabulary)",
    )
    init_cmd.add_argument("path", help="Filesystem path for the new SQLite registry")

    # Root - vocabulary-wide Merkle root
    root_cmd = subparsers.add_parser(
        "root",
        help="Print the Merkle root of the active vocabulary",
    )
    root_cmd.add_argument("--short", "-s", action="store_true", help="Print the 16-char stub only")

    # Pull
    pull_cmd = subparsers.add_parser(
        "pull",
        help="Sync patterns from source DB into active DB (topological DAG walk)",
    )
    pull_cmd.add_argument("--source", help="Source DB path (default: bundled vocabulary)")
    pull_cmd.add_argument(
        "--dry-run", action="store_true", help="Show what would change without applying"
    )
    pull_cmd.add_argument(
        "--verify", action="store_true", help="Run hash validity check after pull"
    )
    pull_cmd.add_argument(
        "--exclude",
        action="append",
        metavar="HANDLE",
        help=(
            "Skip a specific upstream handle (repeatable). Persistent exclusions "
            "go in ~/.config/sema/excluded (one handle per line, # for comments)."
        ),
    )
    pull_cmd.add_argument(
        "--undo",
        action="store_true",
        help="Restore the DB from the snapshot saved by the last successful pull.",
    )
    pull_cmd.add_argument(
        "--preserve-superseded",
        action="store_true",
        help=(
            "Keep locally superseded patterns alongside their upstream replacements. "
            "Default: when upstream declares a pattern supersedes one local pattern "
            "(via _meta.supersedes), the local copy is removed."
        ),
    )

    # Serve
    serve = subparsers.add_parser(
        "serve",
        help="Start API server [requires: pip install semahash[api]]",
    )
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=3000)

    # Build - create project DB from preset or patterns file
    build_cmd = subparsers.add_parser(
        "build",
        help="Build a project DB from a preset (full, standard, empty) or patterns file",
    )
    build_cmd.add_argument("dest", help="Path for the new project DB")
    build_group = build_cmd.add_mutually_exclusive_group(required=True)
    build_group.add_argument(
        "--preset", "-p", choices=["full", "standard", "empty"], help="Built-in preset"
    )
    build_group.add_argument(
        "--from", dest="from_file", help="Path to patterns file (one handle per line)"
    )
    build_cmd.add_argument("--source", help="Source DB (default: bundled vocabulary)")

    # Use - switch active DB
    use_cmd = subparsers.add_parser(
        "use",
        help="Switch active vocabulary DB (or show current)",
    )
    use_cmd.add_argument("path", nargs="?", default=None, help="Path to DB (omit to show current)")
    use_cmd.add_argument("--default", "-d", action="store_true", help="Reset to bundled vocabulary")

    # Categorize - move a pattern to a different taxonomy path
    cat_cmd = subparsers.add_parser(
        "categorize",
        help="Re-categorize a pattern by updating its _meta.path",
    )
    cat_cmd.add_argument("handle", help="Pattern handle (e.g. 'BeliefTracking')")
    cat_cmd.add_argument(
        "--path",
        required=True,
        help="New taxonomy path, slash-separated (e.g. 'Mind/Memory')",
    )

    # List - show known databases
    subparsers.add_parser(
        "list",
        help="List all known vocabulary databases",
    )

    # MCP
    subparsers.add_parser(
        "mcp",
        help="Start MCP server [requires: pip install semahash[mcp]]",
    )

    args = parser.parse_args()

    # Mutating/stateful subcommands return a bool; propagate False as exit 1
    # so CI pipelines and shell scripts can detect failure. Read-only commands
    # (search, show, resolve, skeleton, list, serve, mcp) manage their own
    # exit codes or don't need one.
    ok: bool | None = None
    if args.command == "apply":
        ok = apply_changes(remove_handles=args.remove, add_files=args.add, check_only=args.check)
    elif args.command == "search":
        search_patterns(
            args.query, use_semantic=not args.keyword_only, verbose=args.verbose, as_json=args.json
        )
    elif args.command == "resolve":
        resolve_graph(args.handle)
    elif args.command == "show":
        show_pattern(args.handle)
    elif args.command == "skeleton":
        show_skeleton()
    elif args.command == "init":
        ok = init_registry(args.path)
    elif args.command == "root":
        ok = vocab_root(short=args.short)
    elif args.command == "build":
        ok = build_db(
            args.dest, preset=args.preset, patterns_file=args.from_file, source_db=args.source
        )
    elif args.command == "use":
        ok = use_db(path=args.path, default=args.default)
    elif args.command == "list":
        list_databases()
    elif args.command == "categorize":
        ok = categorize_pattern(handle=args.handle, path_str=args.path)
    elif args.command == "pull":
        if args.undo:
            ok = undo_pull()
        else:
            pull_result = update_db(
                source=args.source,
                dry_run=args.dry_run,
                verify=args.verify,
                exclude=args.exclude,
                preserve_superseded=args.preserve_superseded,
            )
            ok = pull_result.get("success", False)
    elif args.command == "serve":
        run_server(args.host, args.port)
    elif args.command == "mcp":
        run_mcp()
    else:
        parser.print_help()

    if ok is False:
        sys.exit(1)


if __name__ == "__main__":
    main()
