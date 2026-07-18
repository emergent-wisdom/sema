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

After creating the database, switch to it with `sema use`:

```bash
sema use ./mylib.db
```

Every subsequent `sema` command (`search`, `apply`, `mcp`, `serve`, ...)
now reads from your private registry instead of the bundled one.

### build - Build a Project Database

Creates a new vocabulary database from a preset or a patterns file. The
bundled DB is read-only (overwritten on upgrade), so use `build` to create
a writable copy for your project.

```bash
# Full copy of the bundled vocabulary
sema build my_project.db --preset full

# Empty database (add patterns later with `apply`)
sema build my_project.db --preset empty

# Standard subset (curated default selection)
sema build my_project.db --preset standard

# Custom selection from a patterns file (one handle per line)
sema build my_project.db --from patterns.txt

# Build from a different source database
sema build my_project.db --preset full --source other.db
```

Transitive dependencies are resolved automatically — the resulting DB is
self-contained. After building, switch to it with `sema use my_project.db`.

### use - Switch Active Vocabulary

Switches which vocabulary database all `sema` commands read from.

```bash
# Switch to a project database
sema use my_project.db

# Show current active database
sema use

# Reset to the bundled (default) vocabulary
sema use --default
```

The active DB is stored in `~/.config/sema/active_db`. If `SEMA_DB_PATH`
is set in the environment, it takes priority over `sema use`.

### list - List Known Databases

Lists all vocabulary databases that Sema knows about, with the active one
marked.

```bash
sema list
```

Output shows each database's path, pattern count, and status (active,
read-only, missing).

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

**Note:** `apply` refuses to modify the bundled (pip-installed) vocabulary — it
is read-only and gets overwritten on upgrade. Run `sema build` + `sema use`
first to create a writable project database.

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
sema resolve 'Stigmergy#6282'
```

### show - Print Pattern Definition

Prints a pattern's full body: gloss, mechanism, invariants, pre/post
conditions, failure modes, parameters, and dependencies. The primary
read-path for "give me the definition behind this inline ref."

```bash
sema show <Handle>
sema show 'StateLock#8bde'
```

### skeleton - Graph Overview

Displays the graph skeleton (layers, categories, counts).

```bash
sema skeleton
```

### pull - Sync Vocabulary from Upstream

Walks the upstream DAG in topological order and updates the active database
in place. Custom patterns the user added locally are preserved. Hashes
cascade automatically when their upstream deps change.

```bash
# Basic pull (bundled DB → active DB)
sema pull

# Preview what would change without writing
sema pull --dry-run

# Pull from a specific source DB instead of the bundled vocabulary
sema pull --source ./snapshots/2026-04-vocab.db

# Verify all hashes after the pull (extra safety check)
sema pull --verify

# Skip a specific upstream pattern (repeatable)
sema pull --exclude SomeHandle --exclude AnotherHandle

# Keep locally superseded patterns alongside their upstream replacements
sema pull --preserve-superseded

# Revert to the state before the last successful pull
sema pull --undo
```

**Recovery.** Each successful pull that changes something saves a pre-pull
snapshot as `<db>.pull_previous`. `sema pull --undo` restores from it using
SQLite's backup API (safe with WAL mode — a plain `cp` would leave an
orphaned -wal file that corrupts the DB on next open). The snapshot is
consumed by `--undo`; only one snapshot is kept (each successful pull with
changes replaces the previous). A no-op pull does NOT overwrite the
snapshot, so running `sema pull` twice in a row is safe.

**Behavior contract**

- **User-only patterns are never silently deleted.** Anything in your active
  DB that isn't in upstream stays put — with one explicit exception:
  supersession cleanup (below).
- **`_meta` is field-merged.** Upstream owns `layer`, `category`, `tier`,
  `ring`, `supersedes` (taxonomy reorganizations propagate to you). User
  owns `caution` and `related` (your local annotations survive).
- **Hash cascade is automatic.** When an upstream pattern's hash changes,
  your local patterns that depend on it get re-hashed too.
- **Atomic.** The active DB is snapshotted via `sqlite3.Connection.backup()`
  before the loop. Any failure during the pull restores the snapshot — no
  half-applied state.
- **Fast-path skip.** Patterns whose stored sema_id already matches upstream
  are skipped without a write.

**Supersession cleanup**

When an upstream pattern declares `_meta.supersedes: [<local_sema_id>]`,
upstream has explicitly said "this obsoletes that." By default pull acts
on that claim:

- The superseded local pattern is removed.
- The replacement is added in the same run.
- Output shows `→ OldHandle → NewHandle`.

Two guards keep this safe:

- **Orphan protection** — if a user-only local pattern still depends on the
  superseded one (references its `sema_id`), pull keeps the superseded
  pattern in place and warns. Fix the dependent and re-run.
- **Opt-out** — `--preserve-superseded` keeps the old handle alongside the
  replacement. Both coexist in the DB.

The pre-pull snapshot covers recovery either way: `sema pull --undo`
restores the exact prior state.

**Persistent exclusions**

For exclusions you want to keep across runs, write to
`$XDG_CONFIG_HOME/sema/excluded` (defaults to `~/.config/sema/excluded`).
One handle per line. `#` starts a comment. Blank lines are ignored.

```text
# patterns I don't want
LegacyDoodad

# pin local Foo against upstream changes (keep local copy AND exclude)
Foo
```

CLI `--exclude` flags are unioned with the file.

**Version pinning (emergent)**

If you exclude a handle but keep your local copy, dependents resolve against
your local (frozen) version. Useful when you've customized a pattern and
want upstream changes to propagate everywhere except that one.

**Dependency safety**

If an upstream pattern depends on a handle that's excluded AND missing
locally, that pattern is auto-skipped (no abort). The same machinery also
shields you from malformed upstream graphs that ship with dangling refs.

**Refuses to modify the bundled DB.** Run `sema build` + `sema use` to
create a writable project DB first. See [lifecycle.md](../guides/lifecycle.md)
for the full conceptual model.

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

**Fix:** Ensure `_meta` has a valid `path` plus `ring` and `tier`.

## Best Practices

- **Validate first:** Always run with `--check` before applying
- **Small batches:** Debugging 3 new patterns is easier than 30
- **Review dependencies:** A dependency is a semantic claim. Don't auto-fix without understanding the relationship
- **Use staging:** Put work-in-progress patterns in `data/staging/`, move to `data/vocabulary/` when ready
