# Pattern Lifecycle

A Sema pattern moves through a closed loop: **create → validate → hash → apply → export → distribute → pull → rebuild**. This document walks through each stage so you can see how the pieces fit together.

```
  create ──→ validate ──→ hash ──→ apply
    ↑                                │
    │                                ↓
 rebuild ←── pull ←── distribute ←── export
```

## 1. Creation

Write a new pattern as a JSON file in `data/staging/`:

```bash
data/staging/MyPattern.json
```

The file must conform to the [Pattern Card schema](../specification/schema.md). At minimum it needs: `handle`, `mechanism`, `gloss`, `dependencies` (or omit if none), `signature`, and `_meta` with `layer`, `category`, `ring`, `tier`.

See the [Pattern Authoring Guide](authoring.md) for the full workflow.

## 2. Validation

Run a dry-run check before committing anything to the database:

```bash
sema apply --check --add data/staging/MyPattern.json
```

The validator enforces all [Validation Rules](../specification/validation.md):

- **Schema conformance** — required fields, correct types, valid enums
- **Explicit Dependency Standard** — every `{{key}}` in text must be declared; every declared key must be used
- **Cycle detection** — topological sort over the full dependency graph
- **Layer direction** — dependencies should flow from specific to general
- **Complete categorization** — each dependency in exactly one category (`accepts`, `yields`, `composes_with`, `references`)
- **Empty field rule** — no `[]`, `{}`, or `null`; omit instead

If any check fails, nothing is applied. Fix and re-run.

## 3. Hashing

When validation passes, the system computes the pattern's identity via a **recursive Merkle tree** over 11 semantic fields:

`mechanism`, `gloss`, `derived_from`, `dependencies` (recursive), `parameters`, `data_schema`, `signature`, `invariants`, `preconditions`, `postconditions`, `failure_modes`

The result is a deterministic SHA-256 root hash:

```
sema:MyPattern#mh:SHA-256:a1b2c3d4...
```

Metadata fields (`handle`, `sema_id`, `_meta`) are excluded from the hash. Changing any hashed byte — even whitespace — produces a different identity. See [The Pattern Card](../specification/schema.md) §4 for the full algorithm.

## 4. Application

Apply the validated, hashed pattern to the database:

```bash
sema apply --add data/staging/MyPattern.json
```

This writes the pattern to `taxonomy.db`, the **single source of truth** for the vocabulary. The staging file can be deleted after a successful apply — the data now lives in the database.

Atomic add+remove is also supported for replacements:

```bash
sema apply --add NewVersion.json --remove OldHandle
```

See [CLI Reference](../tools/cli.md) for the full command set.

**Bundled DB guard:** The pip-installed vocabulary is read-only — `apply` will refuse to modify it. To work with a writable database, run `sema build my.db --preset full` then `sema use my.db`.

## 5. Export

After applying changes, regenerate the vocabulary JSON files from the database:

```bash
python3 scripts/export/export_sema.py
```

This exports every pattern from `taxonomy.db` into individual JSON files under `data/vocabulary/`. These files are **derived artifacts** — the database is authoritative, the JSON files are for human reading and version control.

**Key point:** `taxonomy.db` → `data/vocabulary/*.json` is the canonical direction. The vocabulary files are exports, not sources.

## 6. Pre-commit Hooks

The repository includes a pre-commit hook (installed via `scripts/setup_hooks.sh`) that automatically:

1. Recalculates the **Merkle root** over the entire vocabulary (`scripts/vocabulary_merkle_root.py`)
2. Regenerates the **shorthand reference** (`scripts/export/export_short_hand.py`)
3. Stages the updated `docs/information/vocabulary_information.md` and `reference/all_patterns_short.md`

This ensures that every commit reflects the true state of the database.

```bash
# One-time setup
./scripts/setup_hooks.sh
```

## 7. Distribution

The vocabulary ships via two channels:

- **PyPI:** `pip install semahash` bundles `taxonomy.db` and the vocabulary files inside the wheel. Every release captures a frozen snapshot of the vocabulary.
- **GitHub:** The repository itself is the living source. Contributors work against the repo; published wheels are point-in-time snapshots.

## 8. Pull

Downstream users sync their active database with the latest upstream vocabulary:

```bash
sema pull
```

### What pull does

`sema pull` walks the upstream DAG in topological order and upserts each
pattern into the active DB. It does **not** wipe the target — it reconciles.

- **User-only patterns are preserved.** If you've minted local patterns,
  pull won't touch them.
- **Hash cascade flows automatically.** When an upstream pattern's hash
  changes, your local patterns that depend on it get re-hashed too. Their
  identity stays mathematically consistent with the new upstream.
- **Metadata is field-merged.** Upstream owns `_meta.layer`, `category`,
  `tier`, `ring`, `supersedes` — taxonomy reorganizations propagate. You
  own `_meta.caution` and `_meta.related` — your local annotations survive.

### Exclusions and version pinning

If a user wants to opt out of a particular upstream pattern, they can list
the handle in `$XDG_CONFIG_HOME/sema/excluded` (defaults to
`~/.config/sema/excluded`). One handle per line; `#` for comments.

The exclusion mechanism has an emergent property: **if you exclude a handle
but keep your local copy, dependents resolve against the local (frozen)
version.** This acts as a per-pattern version pin against upstream changes.

### Failure semantics

The pull is atomic via SQLite's native backup API
(`sqlite3.Connection.backup()`). The active DB is snapshotted before the
loop; on any failure the snapshot is restored. There is no partial-apply
state.

A pre-flight pruning step skips upstream patterns whose dependencies are
missing from both the target DB and the upstream batch. This prevents the
common cascade-fail scenario where excluding one foundational pattern would
otherwise abort the entire pull. The same safety net protects against
upstream releases that ship with dangling dep refs.

## 9. Rebuild

If the database is lost or you need to regenerate it from the vocabulary JSON files:

```bash
./scripts/rebuild_db.sh
```

This script:
1. Backs up the existing `taxonomy.db`
2. Deletes it
3. Runs `sema apply --add data/vocabulary/` to ingest all patterns

You can also dry-run (`--dry-run`) or validate-only (`--check`).

**Bidirectional recovery:** Because either direction can rebuild the other — DB → JSON via `export_sema.py`, JSON → DB via `rebuild_db.sh` — no single failure destroys the vocabulary.

## Summary

| Stage | Command / Script | Input | Output |
|---|---|---|---|
| Create | (manual) | — | `data/staging/*.json` |
| Validate | `sema apply --check --add` | staging JSON | pass/fail |
| Hash | (automatic during apply) | pattern fields | `sema_id` |
| Apply | `sema apply --add` | staging JSON | `taxonomy.db` row |
| Export | `scripts/export/export_sema.py` | `taxonomy.db` | `data/vocabulary/*.json` |
| Hooks | `scripts/setup_hooks.sh` | DB state | updated Merkle root + reference |
| Distribute | `pip install semahash` / git | wheel / repo | user's local copy |
| Pull | `sema pull` | registry | local `taxonomy.db` |
| Rebuild | `scripts/rebuild_db.sh` | `data/vocabulary/*.json` | `taxonomy.db` |
