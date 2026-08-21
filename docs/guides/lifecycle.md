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

The file must conform to the [Pattern Card schema](../specification/schema.md). At minimum it needs: `handle`, `mechanism`, `gloss`, `dependencies` (or omit if none), `signature`, and `_meta` with a valid `path`, `ring`, and `tier`.

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

`mechanism`, `gloss`, `extends`, `dependencies` (recursive), `parameters`, `data_schema`, `signature`, `invariants`, `preconditions`, `postconditions`, `failure_modes`

The result is a deterministic SHA-256 root hash:

```
sema:MyPattern#mh:SHA-256:a1b2c3d4...
```

Metadata fields (`handle`, `sema_id`, `_meta`) are excluded from the hash. Changing
the canonical content of a hashed field produces a different identity. Raw key
order, Unicode composition, and whitespace differences that normalize to the
same canonical form do not. See [The Pattern Card](../specification/schema.md) §4
for the full algorithm.

## 4. Application

Apply the validated, hashed pattern to the database:

```bash
sema apply --add data/staging/MyPattern.json
```

This writes the pattern to `taxonomy.db`, the **single source of truth** for the vocabulary. The staging file can be deleted after a successful apply — the data now lives in the database.

An `extends` reference is different from an ordinary dependency: it names the
exact parent definition against which the child was authored. The current
workspace stores one active definition per handle, so a parent update that
would strand a child is rejected before any mutation. After review, stage the
children you intend to move and retarget only those staged cards:

```bash
sema apply --add data/staging/ --retarget-extends
```

The protocol permits an older pin only while that full parent Sema ID remains
resolvable. The current database does not retain historical definitions, so it
cannot keep such a pin locally; durable historical storage is future work.

Atomic add+remove is also supported for replacements:

```bash
sema apply --add NewVersion.json --remove OldHandle
```

See [CLI Reference](../tools/cli.md) for the full command set.

**Bundled DB guard:** The pip-installed vocabulary is read-only — `apply` will refuse to modify it. To work with a writable database, run `sema build my.db --preset full` then `sema use my.db`.

### Populating `_meta.supersedes` (author side)

Supersession is a two-sided convention. The author side — what you do when you modify a pattern — is independent of the consumer side (§9 Supersession cleanup).

**The rule.** Whenever an edit changes a pattern's `sema_id` against the last public release, the prior `sema_id` must appear in `_meta.supersedes`. This holds regardless of the *kind* of change:

- **Rename** (handle changed) — the successor's `_meta.supersedes` lists the old-handle sema_id.
- **Content edit** (handle unchanged, mechanism / invariants / dependencies / any hashed field changed) — the (same-handle) successor's `_meta.supersedes` lists the prior release's sema_id.
- **Rename + content edit** — one entry suffices; list the single prior sema_id.
- **No change since last release** — no `_meta.supersedes` entry is needed; the hash still matches.

`_meta.supersedes` is a flat list of full sema_id strings (`"sema:Handle#mh:SHA-256:..."`), pointing back to the **last public release**. Intermediate, unreleased sema_ids from a local rebuild must not appear — downstream consumers never saw them, so referencing them is meaningless. When a pattern goes through multiple public releases with changes in each, each release appends its own prior sema_id; the list grows over time and acts as the versioning chain.

**Why it matters.** Consumers running `sema pull` rely on `_meta.supersedes` to map their pinned hashes forward. Without it:

- A rename silently leaves the old handle in the consumer's DB as an orphan alongside the new one. Dependents keep resolving to the frozen old pattern. Drift accumulates.
- A content edit makes the consumer's `sema pull --verify` report a hash mismatch but offers no path to recognize the replacement. The consumer can't distinguish "the pattern changed" from "the pattern was corrupted."

With `_meta.supersedes` populated correctly, pull acts cleanly: removes the old local copy, adds the replacement, preserves dependent wiring via hash-cascade.

**What enforces this.** Honest answer: nothing blocks you on `sema apply` today. There is no compile-time gate that compares the new pattern's hash to the pip-installed pattern's hash and refuses the apply when the old sema_id isn't present in `_meta.supersedes`. The field is schema-optional (`supersedes: list[str] | None`) and excluded from the Merkle hash (see `SEMANTIC_FIELDS` in `src/sema/core/hashing.py`), so omitting it is silently permitted.

This is deliberate for now — the project is small enough that author discipline and CHANGELOG review cover the gap — but a future `sema apply` could grow a `--check-supersedes` gate that cross-references the bundled DB. If that lands, it will be additive; existing patterns won't be revalidated.

**What does use it.** `sema pull` is the consumer-side reader (§9). `sema pull --verify` re-hashes every stored pattern and flags mismatches but does not separately verify that `_meta.supersedes` is correctly populated. The MCP `sema_pull` tool exposes the same supersedes-based cleanup.

**Batch population when you missed it.** If you ship a release whose patterns don't yet carry the prior release's sema_ids, you can populate them after the fact by diffing the current staging tree against the previous public release's DB. A one-shot script (see `scripts/` history around the 0.2.0 release) reads `{handle: prior_sema_id}` from the prior DB, walks staging, and appends the prior sema_id to each pattern whose current sema_id differs from prior. Because `_meta.supersedes` is not hashed, running this does not cascade new hashes through the DAG.

## 5. Export

In the canonical Sema repository, regenerate the tracked vocabulary JSON files
from the database after applying changes:

```bash
python3 scripts/export/export_sema.py
```

This repository-specific script exports every pattern from `taxonomy.db` into
individual JSON files under `data/vocabulary/`. These files are **derived
artifacts**—the database is authoritative, and the JSON files are for human
reading and version control.

**Key point:** `taxonomy.db` → `data/vocabulary/*.json` is the canonical
direction. The vocabulary files are exports, not sources. An independent
library publisher does not need this repository script: `sema package` exports
and verifies the selected project database directly.

### Optional shorthand export

For a compact, locally generated view of the vocabulary, run:

```bash
python3 scripts/export/export_short_hand.py
```

This writes `data/shorthand/all_patterns_short.md`. The file is disposable,
ignored by Git, and not included in distributions. Regenerate it after database
changes when you need it; `taxonomy.db` remains the source of truth.

## 6. Pre-commit Hooks

The repository includes a pre-commit hook (installed via `scripts/setup_hooks.sh`) that automatically:

1. Recalculates the versioned **semantic-set and catalog roots** over the
   entire vocabulary (`scripts/vocabulary_merkle_root.py`)
2. Stages the updated `docs/information/vocabulary_information.md`

This keeps both committed aggregate roots synchronized with the database.

```bash
# One-time setup
./scripts/setup_hooks.sh
```

Before opening a vocabulary pull request, run the complete post-apply workflow:

```bash
python scripts/verify_vocabulary_change.py --refresh
python scripts/verify_vocabulary_change.py
```

The first command retains regenerated manuals, audit reports, vocabulary
information, and current documentation hash references. The second is
non-destructive and verifies those artifacts, all exported hashes, clean
staging, database/export parity, and deterministic reconstruction. CI runs the
same check command, so local and remote vocabulary gates cannot silently
diverge.

## 7. Distribution

Sema definitions can be distributed in three distinct forms:

- **Bundled vocabulary:** `pip install semahash` includes the canonical
  `taxonomy.db` and vocabulary exports. Every package release captures a frozen
  snapshot.
- **Independent library release:** `sema package` converts a project database
  into a verified `library.json` plus a versioned pattern ZIP. Publish both as
  GitHub Release assets (or on another HTTPS host), then consumers install the
  `library.json` asset URL.
- **Living source repository:** Git remains the authoring and review surface.
  A repository URL, branch, GitHub source archive, or `blob/...` page is not a
  library install target.

For example:

```bash
sema package ./defi-release.db \
  --name defi \
  --version 1.0.0 \
  --output-dir dist/defi-1.0.0 \
  --github-repo acme/sema-defi
```

The command packages every pattern in the source database, verifies the
complete dependency closure, recomputes both roots, and compiles a fresh local
read model before writing the final files. A remote library is a complete
standalone snapshot; it never overlays or merges with the bundled vocabulary.
Use `sema build RELEASE.db --from handles.txt --source PROJECT.db` first when a
release should contain only selected entry points and their transitive
dependencies.

For the complete authoring, packaging, GitHub Release, and installation path,
see [Publishing and Installing Vocabulary Libraries](libraries.md).

## 8. Install and Update a Published Library

Install from the published Release asset, activate the registered name, and
inspect the resulting identity:

```bash
sema install https://github.com/acme/sema-defi/releases/latest/download/library.json
sema use defi
sema list
sema root
```

The URL must resolve to the published `library.json` asset. The GitHub Release
must be published and be the latest ordinary release for the generated
`releases/latest/download/library.json` pointer; drafts and prereleases do not
satisfy that pointer.

When the publisher creates a newer complete release, update it explicitly:

```bash
sema update defi
```

`sema update` follows the installed library's recorded `update_url`, verifies a
complete replacement snapshot, and atomically repoints the active selection if
needed. It rejects downgrades and changed snapshot or ZIP content republished
under the same version. It does not merge releases.

## 9. Pull

`sema pull` is for a different lifecycle: it reconciles a writable local
database with another database. By default the source is the bundled vocabulary
installed with Sema:

```bash
sema pull
```

Do not use `pull` to update a named remote library; installed releases are
read-only snapshots. Use `sema update <name>` for that workflow.

### What pull does

`sema pull` walks the upstream DAG in topological order and upserts each
pattern into the active DB. It does **not** wipe the target — it reconciles.

- **User-only patterns are preserved.** If you've minted local patterns,
  pull won't touch them (unless they're explicitly superseded; see below).
- **Hash cascade flows automatically.** When an upstream pattern's hash
  changes, your local patterns that depend on it get re-hashed too. Their
  identity stays mathematically consistent with the new upstream.
- **Metadata is field-merged.** Upstream owns `_meta.path`, `tier`,
  `ring`, `supersedes` — taxonomy reorganizations propagate. You
  own `_meta.caution` and `_meta.related` — your local annotations survive.

### Supersession cleanup

When an upstream pattern's `_meta.supersedes` list names the `sema_id` of a
pattern in your local DB, upstream has explicitly declared the old pattern
obsolete. Pull acts on that declaration by default:

- The superseded local pattern is **removed** from the active DB.
- The replacement (the upstream pattern that declared the supersession) is
  added in the same run.
- Reported as `superseded_removed` in the pull output:
  `→ OldHandle → NewHandle`.

**Orphan guard.** If a *user-only* local pattern still depends on the
superseded one (its dependency map references the exact superseded
`sema_id`), pull **keeps** the superseded pattern rather than silently
breaking your dependent. The situation is reported as
`superseded_kept_orphan`; re-point the dependents (or mint a replacement)
and re-run pull to complete the cleanup.

**Opt-out: `--preserve-superseded`.** If you want the old handle to stick
around alongside the replacement (e.g. to compare, to pin an older
semantics, or because the upstream supersession claim is wrong for your
use case), pass the flag:

```bash
sema pull --preserve-superseded
```

Both the old and new handles end up in your DB; no supersession cleanup
occurs.

**Why the old bytes are still recoverable.** The pre-pull snapshot
(`<db>.pull_previous`) is retained on every successful pull that changed
something, and `sema pull --undo` restores it. So a cleaned-up
supersession is never destructive — the previous state is one command
away.

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

## 10. Rebuild

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
| Hooks | `scripts/setup_hooks.sh` | DB state | updated semantic-set root, catalog root, and references |
| Package | `sema package` | project DB | verified `library.json` + pattern ZIP |
| Distribute | PyPI / published Release assets | wheel / release files | bundled or installed snapshot |
| Install | `sema install` | published `library.json` asset URL | registered read-only library |
| Update | `sema update <name>` | recorded remote update URL | verified replacement snapshot |
| Pull | `sema pull` | source DB | reconciled writable local DB |
| Rebuild | `scripts/rebuild_db.sh` | `data/vocabulary/*.json` | `taxonomy.db` |
