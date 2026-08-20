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

# Build from a different source database or an installed library name
sema build my_project.db --preset full --source other.db
sema build editable-defi.db --preset full --source defi
```

Transitive dependencies are resolved automatically — the resulting DB is
self-contained. A managed installed-library source is verified before it is
copied, and the resulting project database is writable. After building, switch
to it with `sema use my_project.db`.

### package - Build a Publishable Library Release

Exports every pattern in a project database to a deterministic pattern ZIP,
generates `library.json`, and verifies the result through the same
card/closure/root/compiler path used during installation:

```bash
sema package ./defi-release.db \
  --name defi \
  --version 1.0.0 \
  --output-dir dist/defi-1.0.0 \
  --github-repo acme/sema-defi
```

This writes:

```text
dist/defi-1.0.0/library.json
dist/defi-1.0.0/defi-patterns-1.0.0.zip
```

`--github-repo OWNER/REPOSITORY` derives a stable published-manifest URL and
a version-pinned ZIP URL:

```text
https://github.com/OWNER/REPOSITORY/releases/latest/download/library.json
https://github.com/OWNER/REPOSITORY/releases/download/v1.0.0/defi-patterns-1.0.0.zip
```

For another HTTPS host, replace `--github-repo` with both explicit URLs:

```bash
sema package ./defi-release.db \
  --name defi \
  --version 1.0.0 \
  --output-dir dist/defi-1.0.0 \
  --update-url https://vocab.example/releases/latest/library.json \
  --artifact-url https://vocab.example/releases/1.0.0/defi-patterns-1.0.0.zip
```

The command packages every card in `SOURCE_DB`; it does not merge databases or
silently add the bundled vocabulary. To package selected entry points with a
complete transitive closure, first run:

```bash
sema build release.db --from handles.txt --source project.db
```

Packaging fails if the source is empty or invalid, the archive is not a
complete exact-ID closure, or the output directory already exists. A successful
command has already re-read the archive, recomputed its roots, compiled a fresh
SQLite read model, and verified that read model. See [Publishing and Installing
Vocabulary Libraries](../guides/libraries.md) for the complete GitHub Release
workflow.

### install - Install a Remote Library

The remote-library workflow installs and verifies the release named by a strict
`library.json` index:

```bash
sema install https://github.com/emergent-wisdom/sema/releases/latest/download/library.json
```

Pass a local `library.json` path or an HTTPS URL that resolves directly to the
published manifest file. A GitHub repository URL, branch, source archive, or
`blob/...` page is not an install source. For the generated `releases/latest`
URL, the release must be published and be the repository's latest ordinary
release; drafts and prereleases do not satisfy that pointer.

Installation downloads the declared pattern ZIP, validates every Pattern Card
and the complete dependency closure, builds a local read-only database, and
checks the pattern count plus semantic and catalog roots before registering the
library by name. Sema always compiles its local read model from the verified
JSON rather than accepting a publisher-supplied database. Installation does not
activate the library; follow it with `sema use <name>`, `sema list`, and
`sema root` to select and inspect the installed snapshot.

See [Publishing and Installing Vocabulary Libraries](../guides/libraries.md) for the exact
manifest, artifact, verification, and trust contract.

### use - Switch Active Vocabulary

Switches which vocabulary database all `sema` commands read from.

```bash
# Switch to a project database
sema use my_project.db

# Switch to an installed remote library
sema use bootstrap

# Show current active database
sema use

# Reset to the bundled (default) vocabulary
sema use --default
```

The active DB is stored in `~/.config/sema/active_db`. If `SEMA_DB_PATH`
is set in the environment, it takes priority over `sema use`.

An installed library name selects that library's verified snapshot; it does not
compose or merge it with the currently active vocabulary. `sema use --default`
resets the configured selection to the bundled vocabulary (an explicit
`SEMA_DB_PATH` still takes priority). Registered names take precedence over
same-named files in the current directory; use an explicit path such as `./defi`
when that collision is intentional.

### list - List Known Databases

Lists all vocabulary databases that Sema knows about, with the active one
marked.

```bash
sema list
```

Output shows each database's path, pattern count, and status (active,
read-only, missing).

### root - Print Aggregate Vocabulary Identities

Prints the active vocabulary's semantic-set root, catalog root, schemes,
pattern count, definition count, and database path:

```bash
sema root
```

The semantic root commits to the set of definitions. The catalog root also
commits to the exact handle-to-definition bindings. After installing or
updating a library, compare these values with `library.json` or the values
reported by `sema package`.

For compact diagnostics, print the semantic scheme and 16-character prefix:

```bash
sema root --short
```

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

# Explicitly retarget `extends` on staged cards to current parent IDs
sema apply --add reviewed-children/ --retarget-extends
```

`extends` is version-pinned by default. Updating a parent does not silently
change a child's hashed specialization claim. Because the current workspace
stores only one active definition per handle, apply fails before mutation if a
parent update would strand a child. Stage each reviewed child and use
`--retarget-extends` only when you intend to change its parent definition; the
option affects staged cards only. Keeping an older pin requires a historical
content store, which the current database does not yet provide.

**Note:** `apply` refuses to modify the bundled (pip-installed) vocabulary — it
is read-only and gets overwritten on upgrade. Run `sema build` + `sema use`
first to create a writable project database.

**Validation:**
- Patterns to remove must exist
- Patterns to add must pass schema validation
- Dependency graph is checked (cannot remove a pattern that others depend on, unless those are also being removed or re-added)

### search - Search the Vocabulary

```bash
# Semantic search (default)
sema search "coordination"

# Keyword-only search
sema search --keyword-only "how to handle consensus"

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
sema resolve 'Stigmergy#dd4f'
```

### show - Print Pattern Definition

Prints a pattern's full body: gloss, mechanism, invariants, pre/post
conditions, failure modes, parameters, and dependencies. The primary
read-path for "give me the definition behind this inline ref."

```bash
sema show <Handle>
sema show 'StateLock#c9c2'
```

### skeleton - Graph Overview

Displays the graph skeleton (layers, categories, counts).

```bash
sema skeleton
```

### update - Update an Installed Library

Checks the installed library's recorded `update_url` and explicitly replaces
its local snapshot with the newly declared release after full verification:

```bash
sema update defi
```

Updates are never automatic and never merge vocabularies. If verification
fails, the installed release and the active vocabulary remain unchanged. See
[Publishing and Installing Vocabulary Libraries](../guides/libraries.md) for the release and
verification contract.

### pull - Sync Vocabulary from Upstream

Walks the upstream DAG in topological order and updates the active database
in place. Custom patterns the user added locally are preserved. Hashes
cascade automatically when their upstream deps change.

`pull` reconciles one local database with another local upstream database. It
is distinct from `sema update <name>`, which installs a complete, verified
remote release snapshot.

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
