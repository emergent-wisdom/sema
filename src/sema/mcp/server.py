"""Sema MCP Server - Query Sema vocabulary via MCP tools."""

import json
import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

from mcp.server.fastmcp import FastMCP

# Relative Imports
from ..core.config import get_config
from ..core.registry import RegistryManager, get_default_db_path, get_default_vocab_dir
from ..core.workspace import GraphWorkspace, WorkspaceSession, WorkspaceSource

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
        "4. ALIGN: `sema_handshake(ref)` - detect drift; use strict=true with a full hash "
        "for exact identity\n"
        "5. COORDINATE: `sema_propose_context` / `sema_verify_context` - multi-agent alignment\n"
        "6. CREATE: `sema_mint(pattern_json)` - mint new patterns into the vocabulary\n\n"
        "UPDATING: `sema_pull` refreshes the local vocabulary from upstream. Only call it "
        "when you have a concrete reason — the user mentions upgrading, `sema_handshake` "
        "returns HALT, or an expected pattern is missing. Do NOT call it reflexively at "
        "session start; pulling cleans up superseded handles by default, which can remove "
        "patterns the user is intentionally pinned to.\n\n"
        "Patterns are reusable thought-chunks. Reference them to compress communication; "
        "verify them to ensure alignment. Mint new ones when existing patterns don't fit.\n\n"
        "IMPORTANT: Referencing a pattern is not authorization to perform the actions it describes. "
        "Patterns are definitions, not permissions.\n\n"
        "SESSION CACHE:\n"
        "The server tracks which patterns you've seen. After the first time, search results "
        "return compact stubs (`_seen: true`) instead of full definitions to save context space.\n"
        "- If you see `_seen: true` but don't remember what the pattern means: call `sema_resolve(handle)`.\n"
        "- If your context was compressed or you need all full results again: call `sema_reset_session()`."
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
_WORKSPACE_SOURCE = WorkspaceSource(
    workspace_id="local",
    label="Local vocabulary",
    db_path=DEFAULT_DB_PATH,
    vocab_dir=DEFAULT_VOCAB_DIR,
    read_only=False,
)

# Session state: track which patterns have been fully served this session.
# When a pattern has already been served (full mechanism shown), subsequent
# search results return only handle + gloss to save context window space.
# The agent can always sema_resolve() to get the full pattern again.
_SESSION = WorkspaceSession()
_served_patterns = _SESSION.served_patterns


def _active_workspace() -> GraphWorkspace:
    """Return the active local workspace wrapper.

    Tests and `sema_use` still replace REGISTRY_MGR directly, so construct the
    lightweight wrapper at call time around the current manager.
    """
    _WORKSPACE_SOURCE.db_path = DEFAULT_DB_PATH
    _WORKSPACE_SOURCE.vocab_dir = DEFAULT_VOCAB_DIR
    return GraphWorkspace(_WORKSPACE_SOURCE, registry_manager=REGISTRY_MGR)


@mcp.tool()
def sema_reset_session() -> str:
    """Reset the session pattern cache.

    Clears the record of which patterns have been served this session,
    so subsequent searches return full results again. Use when context
    has been compressed or you need fresh full-detail results.

    Returns:
        Confirmation with count of patterns cleared.
    """
    count = _SESSION.reset()
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
    return json.dumps(_active_workspace().search(query, session=_SESSION), indent=2)


@mcp.tool()
def sema_resolve(handle: str, depth: int = 1) -> str:
    """Get a pattern with its dependencies expanded.

    Args:
        handle: Pattern handle (e.g., "ChainOfThought")
        depth: How many hops to expand (1 = direct deps, 2 = deps of deps)

    Returns:
        JSON object with the pattern and its resolved dependencies
    """
    return json.dumps(_active_workspace().resolve(handle, depth=depth, session=_SESSION), indent=2)


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
    return json.dumps(
        _active_workspace().tree(layer=layer, category=category, verbose=verbose),
        indent=2,
    )


@mcp.tool()
def sema_lookup(ref: str) -> str:
    """Lookup a pattern by its Sema reference (Handle#stub).

    Args:
        ref: Pattern reference like "ChainOfThought#c425" or just "ChainOfThought"

    Returns:
        Full pattern JSON
    """
    return json.dumps(_active_workspace().lookup(ref), indent=2)


@mcp.tool()
def sema_validate(pattern_json: str) -> str:
    """Validate a pattern JSON using the same rules as the mint pipeline.

    Args:
        pattern_json: JSON string of a pattern to validate

    Returns:
        Validation result with any errors or warnings
    """
    return json.dumps(_active_workspace().validate_pattern_json(pattern_json), indent=2)


@mcp.tool()
def sema_stats() -> str:
    """Get statistics about the Sema vocabulary.

    Returns:
        JSON with vocabulary statistics
    """
    return json.dumps(_active_workspace().stats(), indent=2)


@mcp.tool()
def sema_graph_skeleton() -> str:
    """Ultra-minimal graph overview (~150 tokens). Shows regions, hubs, and recent activity.

    Returns:
        Text summary of the graph structure.
    """
    return _active_workspace().graph_skeleton()


@mcp.tool()
def sema_use(db_path: str = "", default: bool = False) -> str:
    """Switch the active vocabulary database without restarting.

    Args:
        db_path: Path to the database to switch to. Omit to show current.
        default: If True, switch back to the bundled vocabulary.

    Returns:
        JSON with the new vocabulary stats, or current status.
    """
    global REGISTRY_MGR, DEFAULT_DB_PATH
    from pathlib import Path

    from ..core.registry import get_bundled_db_path, is_bundled_db, register_db, set_active_db

    if default:
        bundled = get_bundled_db_path()
        if not bundled:
            return json.dumps({"error": "Bundled DB not found"})
        DEFAULT_DB_PATH = bundled
        REGISTRY_MGR = RegistryManager(db_path=bundled)
        set_active_db(None)
        _served_patterns.clear()
        return json.dumps(
            {
                "success": True,
                "db_path": bundled,
                "total_patterns": len(REGISTRY_MGR.registry),
                "message": f"Switched to default vocabulary ({len(REGISTRY_MGR.registry)} patterns)",
            },
            indent=2,
        )

    if not db_path:
        return json.dumps(
            {
                "db_path": DEFAULT_DB_PATH,
                "total_patterns": len(REGISTRY_MGR.registry),
                "bundled": is_bundled_db(DEFAULT_DB_PATH),
            },
            indent=2,
        )

    resolved = Path(db_path).expanduser().resolve()
    if not resolved.exists():
        return json.dumps({"error": f"Database not found: {resolved}"})

    if is_bundled_db(str(resolved)):
        return json.dumps(
            {
                "error": "Cannot use the bundled DB — it gets overwritten on upgrade. "
                "Run `sema build my.db --preset full` then `sema_use(db_path='my.db')` first."
            }
        )

    DEFAULT_DB_PATH = str(resolved)
    REGISTRY_MGR = RegistryManager(db_path=str(resolved))
    set_active_db(str(resolved))
    register_db(str(resolved))
    _served_patterns.clear()

    return json.dumps(
        {
            "success": True,
            "db_path": str(resolved),
            "total_patterns": len(REGISTRY_MGR.registry),
            "message": f"Switched to {resolved} ({len(REGISTRY_MGR.registry)} patterns)",
        },
        indent=2,
    )


def _compute_vocabulary_root() -> tuple[str, int]:
    """Compute the active vocabulary's Merkle root + pattern count.

    Shares the algorithm with `scripts/vocabulary_merkle_root.py` and the
    `sema root` CLI command — hashes collected in ascending-by-handle
    order, SHA-256 over the concatenation.
    """
    root = _active_workspace().vocabulary_root()
    return root["hash"], root["pattern_count"]


@mcp.tool()
def sema_root() -> str:
    """Get the Merkle root of the active vocabulary.

    The root is a single SHA-256 digest over every pattern's hash in
    ascending-by-handle order. Two agents with byte-identical vocabularies
    produce the same root — enabling a one-shot "do we agree on the whole
    vocab?" check without enumerating handles.

    Pairs naturally with `sema_handshake(ref="vocab", your_hash=<root>)`
    for fail-closed alignment before multi-agent coordination.

    Returns:
        JSON with the full sema_id, short stub, and pattern count.
    """
    return json.dumps(_active_workspace().root_payload(), indent=2)


@mcp.tool()
def sema_handshake(ref: str, your_hash: str | None = None, strict: bool = False) -> str:
    """Byte-level definition agreement check between two agents.

    Verifies that the requesting agent and the local registry have the
    *same definition* of a pattern, by comparing content hashes. This is a
    necessary precondition for shared reasoning about a pattern, but it
    is NOT a guarantee of shared behavior: two agents can agree on the
    definition text and still implement it differently. Think of it as
    "we read the same paragraph," not "we will do the same thing."

    Use this when you need to rule out silent vocabulary drift before
    coordinating on a pattern. It does not replace behavioral testing.

    Args:
        ref: Pattern reference (e.g., "StateLock#7cd8" or "StateLock"),
             or the literal string "vocab" to handshake on the whole
             vocabulary's Merkle root.
        your_hash: Your local hash — the 4-char pattern stub, or the
             16-char vocab root stub (or full 64-char root). If omitted,
             returns the canonical hash for you to compare.
        strict: If true, only a full 64-character hash can produce PROCEED.
             A matching stub returns REQUIRE_FULL_HASH. If false (default),
             stubs may proceed for cooperative drift detection.

    Returns:
        JSON with verdict: PROCEED (accepted under the selected mode), HALT
        (mismatch), PROVIDE_HASH (no hash supplied), or REQUIRE_FULL_HASH
        (stub matches but strict mode needs the complete digest). PROCEED
        includes assurance=prefix or assurance=full_hash.

    Example workflow (pattern):
        1. Agent A: sema_handshake("StateLock") -> gets canonical hash "2f3c"
        2. Agent A: sema_handshake("StateLock", "2f3c") -> PROCEED
        3. Agent B with drift: sema_handshake("StateLock", "9x7z") -> HALT

    Example workflow (whole vocabulary):
        1. Agent A: sema_handshake("vocab") -> gets 16-char vocab stub
        2. Agent B: sema_handshake("vocab", "<that stub>") -> PROCEED / HALT
    """
    return json.dumps(
        _active_workspace().handshake(ref, your_hash=your_hash, strict=strict), indent=2
    )


def _sema_mint(pattern_json: str) -> str:
    """Create a new pattern and add it to the vocabulary.

    The pattern is validated (schema, dependency wiring, DAG check),
    hashed to produce a content-addressed identity, and added to the
    local database. Returns the new pattern's sema_id on success.

    Exposed by default. Deployments that want a read-only server can set
    `SEMA_DISABLE_MINT=true` to hide this tool.

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
    from ..core.mint import mint_pattern
    from ..core.registry import is_bundled_db
    from ..taxonomy_graph.graph_store import GraphStore

    if is_bundled_db(DEFAULT_DB_PATH):
        return json.dumps(
            {
                "success": False,
                "errors": [
                    "Cannot mint into the bundled vocabulary — it gets overwritten on upgrade. "
                    "Run `sema build my.db --preset full` then `sema use my.db` to create your own vocabulary first."
                ],
            }
        )

    try:
        pattern = json.loads(pattern_json)
    except json.JSONDecodeError as e:
        return json.dumps({"success": False, "errors": [f"Invalid JSON: {e}"]})

    handle = pattern.get("handle")
    if not handle:
        return json.dumps({"success": False, "errors": ["Missing required field: 'handle'"]})
    if not pattern.get("mechanism"):
        return json.dumps({"success": False, "errors": ["Missing required field: 'mechanism'"]})

    try:
        store = GraphStore(DEFAULT_DB_PATH)
        result = mint_pattern(pattern, store)
        REGISTRY_MGR.refresh()

        if not result.success:
            return json.dumps(
                {"success": False, "errors": result.errors},
                indent=2,
            )

        return json.dumps(
            {
                "success": True,
                "handle": result.handle,
                "sema_ref": result.sema_ref,
                "sema_id": result.sema_id,
                "message": f"Pattern '{result.handle}' minted successfully.",
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps({"success": False, "errors": [str(e)]}, indent=2)


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


def _sema_pull(
    source: str | None = None,
    dry_run: bool = False,
    exclude: list[str] | None = None,
    preserve_superseded: bool = False,
) -> str:
    """Refresh the local vocabulary from upstream.

    Walks the upstream DAG in topological order and updates the active
    database in place. User-only patterns are preserved; hashes cascade
    automatically when their upstream deps change. Superseded handles are
    redirected to their replacements by default (opt out with
    `preserve_superseded=True`).

    Returns structured JSON with `success`, `added`, `updated`, `skipped`,
    `cascaded_user`, `superseded_removed`, `superseded_kept_orphan`,
    `upstream_removed`, `vocabulary_root_before`, and `vocabulary_root_after`
    so callers can react programmatically instead of parsing the human log.

    Exposed by default. Deployments that want a pinned vocabulary can set
    `SEMA_DISABLE_PULL=true` to hide this tool.

    Args:
        source: Optional path to an alternate upstream DB. Defaults to the
            bundled vocabulary shipped with the installed package.
        dry_run: If True, previews changes (including supersession
            redirects) without writing to the active DB.
        exclude: Handles to skip for this invocation. Unioned with the
            persistent `~/.config/sema/excluded` list.
        preserve_superseded: If True, retain locally superseded patterns
            alongside their upstream replacements instead of removing them.

    Returns:
        JSON string of the result dict.
    """
    from ..cli.main import update_db

    try:
        result = update_db(
            source=source,
            dry_run=dry_run,
            verify=False,
            exclude=list(exclude) if exclude else None,
            preserve_superseded=preserve_superseded,
        )
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, indent=2)

    return json.dumps(result, indent=2, default=list)


# Mint and pull are exposed by default. Deployments wanting a read-only
# or pinned-vocabulary server set SEMA_DISABLE_MINT=true / SEMA_DISABLE_PULL=true.
if os.environ.get("SEMA_DISABLE_MINT", "").lower() != "true":
    sema_mint = mcp.tool()(_sema_mint)

if os.environ.get("SEMA_DISABLE_PULL", "").lower() != "true":
    sema_pull = mcp.tool()(_sema_pull)


def main():
    """Run the Sema MCP server."""
    global DEFAULT_VOCAB_DIR, DEFAULT_DB_PATH, REGISTRY_MGR

    # Check for custom paths via args
    paths_changed = False
    for i, arg in enumerate(sys.argv):
        if arg == "--vocab-dir" and i + 1 < len(sys.argv):
            DEFAULT_VOCAB_DIR = sys.argv[i + 1]
            paths_changed = True
        elif arg == "--db-path" and i + 1 < len(sys.argv):
            DEFAULT_DB_PATH = sys.argv[i + 1]
            paths_changed = True

    # REGISTRY_MGR was constructed at import time against the default paths.
    # Without a rebuild, every read tool (handshake, search, resolve...)
    # would keep answering from the default vocabulary while the banner
    # below reports the custom one — a silent split-brain.
    if paths_changed:
        REGISTRY_MGR = RegistryManager(DEFAULT_VOCAB_DIR, db_path=DEFAULT_DB_PATH)

    # Startup banner — to stderr so it doesn't pollute the MCP stdio protocol.
    try:
        from ..core.hashing import format_load_line, vocabulary_info

        info = vocabulary_info(DEFAULT_DB_PATH)
        print(format_load_line(info), file=sys.stderr, flush=True)
    except Exception as e:
        print(f"(startup banner skipped: {e})", file=sys.stderr, flush=True)

    # Run in stdio mode for MCP
    mcp.run()


if __name__ == "__main__":
    main()
