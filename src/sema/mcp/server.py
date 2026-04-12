"""Sema MCP Server - Query Sema vocabulary via MCP tools."""

import json
import sys
from collections import defaultdict
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

from mcp.server.fastmcp import FastMCP

# Relative Imports
from ..core.config import get_config
from ..core.registry import RegistryManager, get_default_db_path, get_default_vocab_dir

# Initialize Config
CONFIG = get_config()
PROFILE = CONFIG.get_active_profile()

# Resolve our own package version dynamically so the MCP `initialize` response
# advertises semahash's version rather than the FastMCP SDK's version.
try:
    _SEMA_VERSION = _pkg_version("semahash")
except PackageNotFoundError:
    _SEMA_VERSION = "unknown"

# Initialize server
mcp = FastMCP(
    name="Sema Vocabulary Server",
    instructions=(
        "Sema is a shared namespace where agents mint, share, and verify cognitive patterns.\n"
        "Hash the thought, get the name. Same bytes = same meaning, guaranteed.\n\n"
        "WORKFLOW:\n"
        "1. ORIENT: `sema_graph_skeleton()` - map the terrain\n"
        "2. EXPLORE: `sema_search(query)` - find existing patterns by concept\n"
        "3. DEEPEN: `sema_resolve(handle)` - inspect mechanism & dependencies\n"
        "4. ALIGN: `sema_handshake(ref)` - verify exact definition match\n"
        "5. COORDINATE: `sema_propose_context` / `sema_verify_context` - multi-agent alignment\n"
        "6. CREATE: `sema_mint(pattern_json)` - mint new patterns into the vocabulary\n\n"
        "Patterns are reusable thought-chunks. Reference them to compress communication; "
        "verify them to ensure alignment. Mint new ones when existing patterns don't fit."
    ),
)

# FastMCP's constructor does not expose `version=`, but the underlying low-level
# Server (which renders the MCP `initialize` response) does. Set it directly so
# `serverInfo.version` reflects semahash's release, not the FastMCP SDK version.
mcp._mcp_server.version = _SEMA_VERSION


# Configuration - use shared path resolution from registry
DEFAULT_VOCAB_DIR = get_default_vocab_dir()
DEFAULT_DB_PATH = get_default_db_path()

# Registry Manager
REGISTRY_MGR = RegistryManager(DEFAULT_VOCAB_DIR, db_path=DEFAULT_DB_PATH)

# Session state: track which patterns have been fully served this session.
# When a pattern has already been served (full mechanism shown), subsequent
# search results return only handle + gloss to save context window space.
# The agent can always sema_resolve() to get the full pattern again.
_served_patterns: set[str] = set()


@mcp.tool()
def sema_reset_session() -> str:
    """Reset the session pattern cache.

    Clears the record of which patterns have been served this session,
    so subsequent searches return full results again. Use when context
    has been compressed or you need fresh full-detail results.

    Returns:
        Confirmation with count of patterns cleared.
    """
    count = len(_served_patterns)
    _served_patterns.clear()
    return json.dumps({"reset": True, "patterns_cleared": count})


@mcp.tool()
def sema_search(query: str) -> str:
    """Search Sema patterns by name, description, or meaning (semantic search).

    Patterns you've already seen this session are returned in compact form
    (handle + gloss only). Use sema_resolve() to re-fetch full details.

    Args:
        query: Search term or concept description.

    Returns:
        JSON array of matching patterns.
    """
    REGISTRY_MGR.refresh()

    # Use RegistryManager's hybrid search (keyword + semantic)
    results = REGISTRY_MGR.search(query, use_semantic=True)

    # Compact already-seen patterns; enrich new ones
    compacted = []
    new_count = 0
    for _i, result in enumerate(results):
        ref = result.get("sema_ref") or result.get("handle", "")
        if ref in _served_patterns:
            # Already served this session — compact form
            compacted.append({
                "handle": result.get("handle"),
                "sema_ref": ref,
                "gloss": result.get("gloss"),
                "score": result.get("score"),
                "_seen": True,
            })
        else:
            # New pattern — full result
            _served_patterns.add(ref)
            # Enrich top 3 new results with graph context
            if new_count < 3:
                handle = result.get("handle")
                if handle:
                    clean_handle = handle.split("#")[0]
                    context = REGISTRY_MGR.get_context(clean_handle)
                    if context["dependencies"] or context["used_by"]:
                        result["graph_context"] = context
            new_count += 1
            compacted.append(result)

    return json.dumps(compacted, indent=2)


@mcp.tool()
def sema_resolve(handle: str, depth: int = 1) -> str:
    """Get a pattern with its dependencies expanded.

    Args:
        handle: Pattern handle (e.g., "ChainOfThought")
        depth: How many hops to expand (1 = direct deps, 2 = deps of deps)

    Returns:
        JSON object with the pattern and its resolved dependencies
    """
    REGISTRY_MGR.refresh()
    subgraph = REGISTRY_MGR.resolve(handle, depth=depth)

    if not subgraph:
        return json.dumps({"error": f"Pattern '{handle}' not found"})

    # Re-fetch each pattern via get_pattern() so template placeholders like
    # {{vote}} are resolved to their canonical refs (e.g. Vote#cae4). This
    # keeps sema_resolve and sema_lookup output consistent — both go through
    # the same template-resolution path. Without this, sema_resolve leaks
    # raw {{...}} placeholders that sema_lookup never shows.
    rendered = {}
    for entry_handle in subgraph.keys():
        clean = entry_handle.split("#")[0]
        resolved_pattern = REGISTRY_MGR.get_pattern(clean)
        # Fall back to the raw subgraph entry if get_pattern misses (shouldn't
        # happen for anything resolve() returned, but be defensive).
        rendered[entry_handle] = resolved_pattern or subgraph[entry_handle]

    # Mark all resolved patterns as served this session
    for entry_handle in rendered:
        _served_patterns.add(entry_handle)

    return json.dumps(
        {"root": handle, "depth": depth, "patterns": rendered, "count": len(rendered)}, indent=2
    )


@mcp.tool()
def sema_tree(layer: str | None = None, category: str | None = None, verbose: bool = False) -> str:
    """Browse the vocabulary structure organized by layer and category.

    Args:
        layer: Filter to specific layer (Physics, Mind, Society, Infrastructure)
        category: Filter to specific category
        verbose: If True, includes the gloss (description) for each pattern.

    Returns:
        JSON tree structure of patterns
    """
    REGISTRY_MGR.refresh()
    registry = REGISTRY_MGR.registry
    patterns = []

    for handle, data in registry.items():
        p_layer = data.get("sema_layer") or data.get("layer", "Unknown")
        p_category = data.get("sema_category") or data.get("category", "UNCATEGORIZED")

        # Apply filters
        if layer and p_layer != layer:
            continue
        if category and p_category != category:
            continue

        if verbose:
            gloss = data.get("gloss", "")
            entry = f"{handle}: {gloss}" if gloss else handle
        else:
            entry = handle

        patterns.append({"entry": entry, "category": p_category, "layer": p_layer})

    # Group by layer -> category
    tree = defaultdict(lambda: defaultdict(list))
    for p in patterns:
        tree[p["layer"]][p["category"]].append(p["entry"])

    # Convert to regular dict for JSON
    result = {
        layer_name: {cat: sorted(entries) for cat, entries in cats.items()}
        for layer_name, cats in tree.items()
    }

    return json.dumps(
        {
            "tree": result,
            "total_patterns": len(patterns),
            "layers": list(tree.keys()),
            "filter": {"layer": layer, "category": category, "verbose": verbose},
        },
        indent=2,
    )


@mcp.tool()
def sema_lookup(ref: str) -> str:
    """Lookup a pattern by its Sema reference (Handle#stub).

    Args:
        ref: Pattern reference like "ChainOfThought#a1b2" or just "ChainOfThought"

    Returns:
        Full pattern JSON
    """
    REGISTRY_MGR.refresh()

    # Parse reference
    parts = ref.split("#")
    handle = parts[0]
    stub = parts[1] if len(parts) > 1 else None

    pattern = REGISTRY_MGR.get_pattern(handle)
    if not pattern:
        return json.dumps({"error": f"Pattern '{handle}' not found"})

    # Verify stub if provided
    if stub:
        pattern_stub = pattern.get("sema_stub", "")
        if stub != pattern_stub:
            return json.dumps(
                {
                    "warning": f"Stub mismatch: requested '{stub}' but pattern has '{pattern_stub}'",
                    "pattern": pattern,
                }
            )

    return json.dumps(pattern, indent=2)


@mcp.tool()
def sema_validate(pattern_json: str) -> str:
    """Validate a pattern JSON for correctness.

    Args:
        pattern_json: JSON string of a pattern to validate

    Returns:
        Validation result with any errors or warnings
    """
    try:
        pattern = json.loads(pattern_json)
    except json.JSONDecodeError as e:
        return json.dumps({"valid": False, "errors": [f"Invalid JSON: {e}"]})

    errors = []
    warnings = []

    # Required fields
    if "handle" not in pattern:
        errors.append("Missing required field: 'handle'")
    if "mechanism" not in pattern:
        errors.append("Missing required field: 'mechanism'")

    # Recommended fields
    if "gloss" not in pattern:
        warnings.append("Missing recommended field: 'gloss'")
    if "invariants" not in pattern:
        warnings.append("Missing recommended field: 'invariants'")

    # Validate links if present
    REGISTRY_MGR.refresh()
    registry = REGISTRY_MGR.registry
    if "links" in pattern:
        for _rel, targets in pattern.get("links", {}).items():
            for target in targets:
                target_handle = target.split("#")[0]
                if target_handle not in registry:
                    warnings.append(f"Link target not in vocabulary: '{target}'")

    return json.dumps(
        {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "handle": pattern.get("handle", "Unknown"),
        },
        indent=2,
    )


@mcp.tool()
def sema_stats() -> str:
    """Get statistics about the Sema vocabulary.

    Returns:
        JSON with vocabulary statistics
    """
    REGISTRY_MGR.refresh()
    registry = REGISTRY_MGR.registry

    # Count by layer and category
    layers = defaultdict(int)
    categories = defaultdict(int)

    for _handle, data in registry.items():
        layers[data.get("sema_layer") or data.get("layer", "Unknown")] += 1
        categories[data.get("sema_category") or data.get("category", "Unknown")] += 1

    return json.dumps(
        {
            "total_patterns": len(registry),
            "by_layer": dict(layers),
            "by_category": dict(categories),
            "vocab_dir": DEFAULT_VOCAB_DIR,
            "data_source": REGISTRY_MGR.source,
            "db_path": REGISTRY_MGR.db_path,
        },
        indent=2,
    )


@mcp.tool()
def sema_graph_skeleton() -> str:
    """Ultra-minimal graph overview (~150 tokens). Shows regions, hubs, and recent activity.

    Returns:
        Text summary of the graph structure.
    """
    REGISTRY_MGR.refresh()
    return REGISTRY_MGR.get_graph_skeleton()


@mcp.tool()
def sema_handshake(ref: str, your_hash: str | None = None) -> str:
    """Byte-level definition agreement check between two agents.

    Verifies that the requesting agent and the local registry have the
    *same definition* of a pattern, by comparing hash stubs. This is a
    necessary precondition for shared reasoning about a pattern, but it
    is NOT a guarantee of shared behavior: two agents can agree on the
    definition text and still implement it differently. Think of it as
    "we read the same paragraph," not "we will do the same thing."

    Use this when you need to rule out silent vocabulary drift before
    coordinating on a pattern. It does not replace behavioral testing.

    Args:
        ref: Pattern reference (e.g., "StateLock#2f3c" or "StateLock")
        your_hash: Your local 4-char hash stub. If provided, verifies match.
                   If omitted, returns the canonical hash for you to compare.

    Returns:
        JSON with verdict: PROCEED (hashes match), HALT (mismatch), or
        PROVIDE_HASH (canonical hash for your comparison)

    Example workflow:
        1. Agent A: sema_handshake("StateLock") -> gets canonical hash "2f3c"
        2. Agent A: sema_handshake("StateLock", "2f3c") -> PROCEED
        3. Agent B with drift: sema_handshake("StateLock", "9x7z") -> HALT
    """
    REGISTRY_MGR.refresh()
    registry = REGISTRY_MGR.registry

    # Parse reference
    parts = ref.split("#")
    handle = parts[0]
    ref_stub = parts[1] if len(parts) > 1 else None

    if handle not in registry:
        return json.dumps(
            {
                "verdict": "HALT",
                "reason": f"Pattern '{handle}' not found in vocabulary",
                "action": "Cannot coordinate - pattern unknown",
            },
            indent=2,
        )

    pattern = registry[handle]
    canonical_stub = pattern.get("sema_stub", "")
    canonical_ref = pattern.get("sema_ref", f"{handle}#{canonical_stub}")
    full_hash = pattern.get("sema_id", "")

    # If no hash provided, return the canonical for comparison
    if your_hash is None and ref_stub is None:
        return json.dumps(
            {
                "verdict": "PROVIDE_HASH",
                "handle": handle,
                "canonical_stub": canonical_stub,
                "canonical_ref": canonical_ref,
                "full_sema_id": full_hash,
                "action": (
                    "Compare this hash with your local definition. "
                    "Call again with your_hash to verify."
                ),
            },
            indent=2,
        )

    # Determine which hash to compare
    compare_hash = your_hash or ref_stub

    # Perform fail-closed verification
    if compare_hash == canonical_stub:
        return json.dumps(
            {
                "verdict": "PROCEED",
                "handle": handle,
                "verified_ref": canonical_ref,
                "message": "Semantic alignment confirmed. Safe to coordinate.",
                "invariants": pattern.get("invariants", []),
                "tier": pattern.get("tier", 1),
            },
            indent=2,
        )
    else:
        return json.dumps(
            {
                "verdict": "HALT",
                "handle": handle,
                "your_hash": compare_hash,
                "canonical_hash": canonical_stub,
                "reason": "SEMANTIC DRIFT DETECTED",
                "action": (
                    "DO NOT PROCEED. Your definition differs from the canonical vocabulary. "
                    "Either update your local definition or escalate to OntologyHandshake."
                ),
                "canonical_ref": canonical_ref,
                "full_sema_id": full_hash,
            },
            indent=2,
        )


@mcp.tool()
def sema_mint(pattern_json: str) -> str:
    """Create a new pattern and add it to the vocabulary.

    The pattern is validated (schema, dependency wiring, DAG check),
    hashed to produce a content-addressed identity, and added to the
    local database. Returns the new pattern's sema_id on success.

    Args:
        pattern_json: JSON string of the pattern to mint. Required fields:
            - handle: PascalCase name (e.g., "MyPattern")
            - mechanism: How the pattern works
            - gloss: One-line summary
            Recommended: invariants, preconditions, postconditions,
            failure_modes, dependencies, _meta (layer, category, tier)

    Returns:
        JSON with the minted pattern's sema_id, or validation errors.
    """
    import os
    import tempfile

    try:
        pattern = json.loads(pattern_json)
    except json.JSONDecodeError as e:
        return json.dumps({"success": False, "errors": [f"Invalid JSON: {e}"]})

    handle = pattern.get("handle")
    if not handle:
        return json.dumps({"success": False, "errors": ["Missing required field: 'handle'"]})
    if not pattern.get("mechanism"):
        return json.dumps({"success": False, "errors": ["Missing required field: 'mechanism'"]})

    # Write to a temp file for the apply pipeline
    tmp_dir = tempfile.mkdtemp(prefix="sema_mint_")
    tmp_file = os.path.join(tmp_dir, f"{handle}.json")
    with open(tmp_file, "w") as f:
        json.dump(pattern, f, indent=2)

    try:
        # Use the CLI apply pipeline (validate + hash + add)
        import io
        from contextlib import redirect_stdout

        from ..cli.main import apply_changes

        buf = io.StringIO()
        with redirect_stdout(buf):
            result = apply_changes(add_files=[tmp_file], check_only=False)

        output = buf.getvalue()

        # Check if it was added
        if result is False or "failed" in output.lower():
            return json.dumps(
                {"success": False, "errors": [output.strip()]},
                indent=2,
            )

        # Refresh registry and get the new pattern
        REGISTRY_MGR.refresh()
        new_pattern = REGISTRY_MGR.get_pattern(handle)
        if new_pattern:
            return json.dumps(
                {
                    "success": True,
                    "handle": handle,
                    "sema_ref": new_pattern.get("sema_ref"),
                    "sema_id": new_pattern.get("sema_id"),
                    "message": f"Pattern '{handle}' minted successfully.",
                },
                indent=2,
            )
        else:
            return json.dumps(
                {"success": True, "handle": handle, "message": output.strip()},
                indent=2,
            )
    except Exception as e:
        return json.dumps({"success": False, "errors": [str(e)]}, indent=2)
    finally:
        # Cleanup temp file
        try:
            os.remove(tmp_file)
            os.rmdir(tmp_dir)
        except OSError:
            pass


@mcp.tool()
def sema_propose_context(handles: list[str]) -> str:
    """Propose a shared definition set for multi-agent coordination.

    Computes a truncated SHA-256 digest over the sorted set of canonicalized
    pattern definitions in `handles`. The receiving agent calls
    sema_verify_context with the same handles and compares digests.

    Properties of the digest:
      - Order-independent: this is a SET digest, not a Merkle tree. Two
        agents that submit the same handles in different orders produce
        the same digest.
      - 32 bits wide (8 hex chars). That gives roughly a 65k collision
        domain — sufficient to catch ACCIDENTAL vocabulary drift between
        cooperating agents, but NOT a security primitive: an active
        adversary can trivially brute-force a matching 4-byte prefix.
      - What it verifies: that both agents have byte-identical definitions
        for every pattern in the set.
      - What it does NOT verify: that both agents will behave compatibly
        when executing those patterns.

    Workflow:
        1. Agent A: sema_propose_context(["StateLock", "Check", "Task"])
           -> returns context_hash "7f3a..."
        2. Agent A sends context_hash to Agent B
        3. Agent B: sema_verify_context(["StateLock", "Check", "Task"], "7f3a...")
           -> PROCEED or HALT

    Args:
        handles: List of pattern handles to include in the context.

    Returns:
        JSON with the context_hash (truncated SHA-256 set digest) and pattern refs.
    """
    from ..core.actions import _compute_context_hash

    REGISTRY_MGR.refresh()

    patterns = []
    refs = []
    missing = []

    for handle in handles:
        clean = handle.split("#")[0]
        pattern = REGISTRY_MGR.get_pattern(clean)
        if pattern:
            patterns.append(pattern)
            refs.append(pattern.get("sema_ref", clean))
        else:
            missing.append(handle)

    if missing:
        return json.dumps(
            {
                "verdict": "HALT",
                "reason": "Patterns not found",
                "missing": missing,
            },
            indent=2,
        )

    context_hash = _compute_context_hash(patterns)

    return json.dumps(
        {
            "context_hash": context_hash,
            "digest_kind": "truncated SHA-256 set digest, 32 bits",
            "patterns": refs,
            "count": len(patterns),
            "action": "Send context_hash to the other agent. They verify with sema_verify_context.",
        },
        indent=2,
    )


@mcp.tool()
def sema_verify_context(handles: list[str], remote_hash: str) -> str:
    """Verify a semantic context proposed by another agent.

    Computes the local truncated SHA-256 set digest for the given pattern set
    and compares it against the remote agent's digest. PROCEED if identical,
    HALT if not. The digest is a drift-detection primitive between cooperating
    agents, not a security primitive against an adversary (see
    sema_propose_context for details).

    Args:
        handles: List of pattern handles in the proposed context.
        remote_hash: The context_hash received from the proposing agent.

    Returns:
        JSON with verdict: PROCEED (contexts match) or HALT (drift detected).
    """
    from ..core.actions import _compute_context_hash

    REGISTRY_MGR.refresh()

    patterns = []
    missing = []

    for handle in handles:
        clean = handle.split("#")[0]
        pattern = REGISTRY_MGR.get_pattern(clean)
        if pattern:
            patterns.append(pattern)
        else:
            missing.append(handle)

    if missing:
        return json.dumps(
            {
                "verdict": "HALT",
                "reason": "Patterns not found locally",
                "missing": missing,
            },
            indent=2,
        )

    local_hash = _compute_context_hash(patterns)

    if local_hash == remote_hash:
        return json.dumps(
            {
                "verdict": "PROCEED",
                "context_hash": local_hash,
                "patterns": [p.get("sema_ref", h) for p, h in zip(patterns, handles, strict=True)],
                "count": len(patterns),
                "message": "Context verified. All patterns match. Safe to coordinate.",
            },
            indent=2,
        )
    else:
        return json.dumps(
            {
                "verdict": "HALT",
                "reason": "Context digest mismatch",
                "local_hash": local_hash,
                "remote_hash": remote_hash,
                "patterns": handles,
                "action": (
                    "Vocabularies differ on at least one pattern in this set. "
                    "Inspect which handles resolved to which hashes (sema_handshake) "
                    "to find the disagreement. This is a drift-detection signal between "
                    "cooperating agents, not an authenticated security check."
                ),
            },
            indent=2,
        )


def main():
    """Run the Sema MCP server."""

    # Check for custom paths via args
    for i, arg in enumerate(sys.argv):
        if arg == "--vocab-dir" and i + 1 < len(sys.argv):
            global DEFAULT_VOCAB_DIR
            DEFAULT_VOCAB_DIR = sys.argv[i + 1]
        elif arg == "--db-path" and i + 1 < len(sys.argv):
            global DEFAULT_DB_PATH
            DEFAULT_DB_PATH = sys.argv[i + 1]

    # Run in stdio mode for MCP
    mcp.run()


if __name__ == "__main__":
    main()
