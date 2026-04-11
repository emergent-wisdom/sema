# Sema CLI

The **Sema CLI** (`sema`) is the primary tool for managing the vocabulary. It ensures database integrity, strict validation, and atomic operations.

## Installation

```bash
pip install semahash
```

For development against this repo:

```bash
pip install -e ".[full]"
```

## Features

*   **Strict Validation:** Enforces "Truth in Advertising" (dependencies must be used in text), Schema rules, and Taxonomy constraints.
*   **Atomic Operations:** Validates everything before making any changes.
*   **Dependency Checking:** Prevents removing patterns that are still in use.

## Commands

### init - Create an Empty Registry

Creates a fresh, empty taxonomy database at `<path>` so you can build your
own vocabulary from scratch without touching the bundled canonical one.

```bash
sema init ./mylib.db
```

The output prints the `export SEMA_DB_PATH=...` line to set in your shell.
Once exported, every subsequent `sema` command (`search`, `apply`, `mcp`,
`serve`, ...) reads from your private registry instead of the bundled one.

### apply - Atomic Add/Remove

The `apply` command performs atomic add and remove operations. All changes are validated before execution.

```bash
# Add a pattern
sema apply --add <path_to_json>

# Add multiple patterns (or a directory)
sema apply --add patterns/

# Remove a pattern
sema apply --remove <Handle>

# Atomic add + remove (e.g., replacing a pattern)
sema apply --add NewPattern.json --remove OldPattern
```

**Validation:**
- Patterns to remove must exist
- Patterns to add must pass schema validation
- Dependency graph is checked (cannot remove a pattern that others depend on, unless those are also being removed or re-added)

### search - Search the Vocabulary

```bash
# Keyword search
sema search "coordination"

# Semantic search (uses embeddings)
sema search --semantic "how to handle consensus"

# Verbose output with details
sema search -v "trust"

# JSON output
sema search --json "verification"
```

### resolve - Resolve Dependencies

Shows the dependency subgraph for a pattern. Accepts a bare handle or a
handle with a stub (`Handle#stub`).

```bash
sema resolve <Handle>
sema resolve 'Stigmergy#f624'
```

### show - Print Pattern Definition

Prints a pattern's full body: gloss, mechanism, invariants, pre/post
conditions, failure modes, parameters, and dependencies. The primary
read-path for "give me the definition behind this inline ref."

```bash
sema show <Handle>
sema show 'StateLock#b91b'
```

### skeleton - Graph Overview

Displays the graph skeleton (layers, categories, counts).

```bash
sema skeleton
```

### pull - Update Database

Downloads the latest vocabulary database from the registry.

```bash
sema pull
```

### serve - Start API Server

Starts the REST API server. Defaults to `127.0.0.1` (loopback only) so
local-dev installs are not exposed to the LAN. Pass `--host 0.0.0.0`
explicitly when you actually want to bind on all interfaces (e.g.
when running inside a container or on a remote box).

```bash
sema serve                           # localhost only (recommended)
sema serve --port 3001               # different port
sema serve --host 0.0.0.0 --port 80  # explicit external bind
```

### mcp - Start MCP Server

Starts the Model Context Protocol server for AI integration.

```bash
sema mcp
```

## Validation Rules

The CLI enforces the following strictly:

1.  **Truth in Advertising:** If you declare a dependency in `dependencies`, you MUST use it in the text (e.g., `{{Dependency}}`).
2.  **Forward Declaration:** If you use `{{Handle}}` in text, it MUST be declared in `dependencies`.
3.  **Taxonomy:** Layer and Category must match the allowed list.
4.  **Schema:** Patterns in `Data Structures` must have a `data_schema`.
5.  **Signature:** Signatures must follow `Verb(Noun)` syntax.

For the complete rule set (Rules A-K), see [Validation Rules](../specification/validation.md).

## Troubleshooting

### Explicit Dependency Violation

```
Forward dependency violations: '{{tool_invoke}}' used in 'mechanism' but not declared in dependencies
```

**Fix:** Add `"tool_invoke": "sema:ToolInvoke#..."` to `dependencies.references` (or the appropriate category).

### Empty Field Violation

```
EMPTY FIELD RULE VIOLATION: dependencies = {}
```

**Fix:** Delete the field entirely. If a pattern has no dependencies, omit the `dependencies` block.

### Missing Metadata

```
_meta.ring; Field required
```

**Fix:** Ensure `_meta` has all four fields: `layer`, `category`, `ring`, `tier`.

## Best Practices

- **Validate first:** Always run with `--check` before applying
- **Small batches:** Debugging 3 new patterns is easier than 30
- **Review dependencies:** A dependency is a semantic claim. Don't auto-fix without understanding the relationship
- **Use staging:** Put work-in-progress patterns in `data/staging/`, move to `data/vocabulary/` when ready
