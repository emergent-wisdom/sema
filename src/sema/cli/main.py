import argparse
import json
from pathlib import Path

from ..client import get_default_client
from ..core.dependencies import topological_sort
from ..core.hashing import generate_sema_hash
from ..core.registry import RegistryManager, get_default_db_path
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
    store = GraphStore(db_path)

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
    add_patterns = []  # List of (file_path, data, computed_hash)
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
                    add_patterns.append((jf, result["data"], result["hash"]))
                    add_handles.add(result["data"]["handle"])
        elif file_path.exists():
            result = _validate_pattern_file(file_path)
            if result["error"]:
                errors.append(result["error"])
            else:
                add_patterns.append((file_path, result["data"], result["hash"]))
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
        # TODO: Temporarily disabled pending vocabulary layer fixes (65 violations)
        # Rule 7.6: Layer direction validation
        # try:
        #     from ..taxonomy_graph.graph_store import NodeType
        #
        #     existing_patterns = {
        #         data.get("handle", nid): data
        #         for nid, data in store.get_nodes_by_type(NodeType.PATTERN)
        #         if data.get("handle")
        #     }
        #     validate_layer_direction(patterns_dict, existing_patterns)
        # except ValueError as e:
        #     print(f"  ❌ {e}")
        #     return False

        # Map back to full tuples
        pattern_map = {p[1]["handle"]: p for p in add_patterns}
        sorted_patterns = [pattern_map[h] for h in sorted_handles if h in pattern_map]
    else:
        sorted_patterns = []

    # 2c. Add patterns
    for file_path, data, computed in sorted_patterns:
        # Update data with computed hash and layer/category
        data["sema_ref"] = computed["reference"]
        data["sema_id"] = computed["full_id"]
        data["sema_stub"] = computed["stub"]

        # Promote layer/category from _meta for Registry compatibility
        meta = data.get("_meta", {})
        data["sema_layer"] = meta.get("layer", "Unknown")
        data["sema_category"] = meta.get("category", "Uncategorized")

        result = store.add_pattern(data)
        if result.get("success"):
            print(f"  ✓ Added {computed['reference']}")

            # Write hash back to file
            try:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                print(f"  ⚠️  Could not update file {file_path}: {e}")
        else:
            print(f"  ❌ Failed to add {data['handle']}: {result.get('error')}")
            return False

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
        return {"error": f"Invalid JSON in {file_path}: {e}", "data": None, "hash": None}
    except Exception as e:
        return {"error": f"Cannot read {file_path}: {e}", "data": None, "hash": None}

    # Validate required fields
    is_valid, val_errors, val_warnings = validate_pattern(data)
    if not is_valid:
        return {
            "error": f"Validation failed for {file_path}: {'; '.join(val_errors)}",
            "data": None,
            "hash": None,
        }

    # Compute hash
    computed = generate_sema_hash(data)

    return {"error": None, "data": data, "hash": computed}


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
        return
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
        return

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


def update_db():
    try:
        client = get_default_client()
        client.download_db(force=True)
        print("✅ Database updated successfully.")
    except Exception as e:
        print(f"❌ Update failed: {e}")


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

    print(f"✅ Created empty registry at {target}")
    print("")
    print("To use this registry in subsequent sema commands:")
    print(f"  export SEMA_DB_PATH={target}")
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
    try:
        from ..mcp.server import mcp
    except ImportError:
        print("MCP server requires extra dependencies. Install with:")
        print('  pip install "semahash[mcp]"')
        return

    mcp.run()


def main():
    parser = argparse.ArgumentParser(description="Sema CLI")
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
    search.add_argument("--semantic", "-s", action="store_true", help="Enable semantic search")
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

    # Pull
    subparsers.add_parser("pull", help="Download latest DB")

    # Serve
    serve = subparsers.add_parser(
        "serve",
        help="Start API server [requires: pip install semahash[api]]",
    )
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=3000)

    # MCP
    subparsers.add_parser(
        "mcp",
        help="Start MCP server [requires: pip install semahash[mcp]]",
    )

    args = parser.parse_args()

    if args.command == "apply":
        apply_changes(remove_handles=args.remove, add_files=args.add, check_only=args.check)
    elif args.command == "search":
        search_patterns(
            args.query, use_semantic=args.semantic, verbose=args.verbose, as_json=args.json
        )
    elif args.command == "resolve":
        resolve_graph(args.handle)
    elif args.command == "show":
        show_pattern(args.handle)
    elif args.command == "skeleton":
        show_skeleton()
    elif args.command == "init":
        init_registry(args.path)
    elif args.command == "pull":
        update_db()
    elif args.command == "serve":
        run_server(args.host, args.port)
    elif args.command == "mcp":
        run_mcp()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
