# Contributing to Sema

There are two registries you might be contributing to, and they have very
different processes.

## Local vs canonical

**Your own private vocabulary.** Anyone can build a registry from scratch
without touching this repo:

```bash
sema build mylib.db --preset full   # or --preset empty, --preset standard
sema use mylib.db
sema apply --add path/to/MyPattern.json
```

`sema build` creates a writable copy of the vocabulary (or an empty DB).
`sema use` switches all subsequent `sema` commands — `search`, `resolve`,
`mcp`, etc. — to read from your project database. No PR required, no
review, no maintainer in the loop.

**The canonical vocabulary.** The bundled patterns that ship with
`pip install semahash` live in `data/taxonomy.db`. The JSON files under
`data/vocabulary/` are reviewable exports, not authoring sources.
Contributions to the canonical vocabulary go through GitHub PRs. The rest of
this document is about that path.

## 1. Author a pattern

Create a JSON file in `data/staging/<NewPattern>.json`. To refine an existing
pattern, copy its current export from `data/vocabulary/` into `data/staging/`
and edit the staging copy. Required fields include `handle`, `mechanism`,
`gloss`, and `_meta` with `path`, `ring`, and `tier`. See the
[Pattern Authoring Guide](docs/guides/authoring.md) and
[Pattern Card schema](docs/specification/schema.md) for the full rules. A
minimal pattern:

```json
{
  "handle": "MyPattern",
  "mechanism": "Description of what this pattern does and how it works.",
  "gloss": "One-line summary used by semantic search.",
  "_meta": {
    "path": ["Mind", "Reasoning"],
    "ring": 2,
    "tier": 1
  }
}
```

Use `{{snake_case}}` placeholders to reference other patterns; declare each one
in exactly one dependency category. Look up dependency hashes with
`sema show <Handle>`. Add or update the matching entry in
`data/design_critique.json`, then preview the staging-aware design manual with
`python scripts/generate_design_manual.py`.

## 2. Validate locally

Validate, apply, and export through the authoritative database:

```bash
# Schema, dependency wiring, layer direction, and dependency-key usage
sema apply --check --add data/staging/MyPattern.json

# Apply to the canonical development database
sema apply --add data/staging/MyPattern.json

# Export reviewable JSON from the database, then remove the staging file
python scripts/export/export_sema.py
```

`sema apply --check` is a dry run. The non-check command writes the canonical
database and updates the staging file with its resolved hash. Export only after
the complete batch applies successfully. Delete applied staging JSON before
final verification; an unexpected staging file means work is still in flight.

Then run the same complete workflow CI uses:

```bash
python scripts/verify_vocabulary_change.py --refresh
python scripts/verify_vocabulary_change.py
pytest
```

The refresh command keeps generated manuals, audit reports, root information,
and current documentation refs. The check command is non-destructive and also
proves database/export parity, exported hash validity, and deterministic
reconstruction.

## 3. PR checklist

A pattern PR is ready to review when:

- [ ] **The definition is tight.** Every `{{placeholder}}` resolves to
      a declared dependency (`sema apply --check` enforces this). Failure
      modes are concrete, not hand-wavy. Parameters, where used, have
      `name`, `type`, `range`, `description`.
- [ ] **A general handle stays general.** Short parent handles contain only the
      broad-use intersection. Strategy belongs in descendants, deployment
      policy in callers, and contextual diagnostics in the design sidecar.
- [ ] **It is not a duplicate.** Run `sema search "<your gloss>"` and
      `sema search "<your handle>"` first. If a near-match exists, the
      PR description should explain how this pattern is distinct (or
      why the existing one should be refined instead).
- [ ] **It has a use case.** The PR description names at least one
      concrete situation in which an agent would reach for this pattern.
- [ ] **Layer and category are honest.** A pattern about coordination
      between agents belongs in `Society`, not `Mind`. A primitive
      data shape belongs in `Infrastructure`, not `Society`.

## 4. What reviewers look for

Three things, in order:

1. **Novelty.** Does it name something that doesn't already have a
   canonical entry? If a near-duplicate exists, can we refine the
   existing one instead? (Refinement produces a new hash; see
   [Pattern Lifecycle](docs/guides/lifecycle.md).)
2. **Identity and specificity.** Is the mechanism testable without importing
   unstated domain policy? Is a general parent broad enough for every listed
   context while concrete descendants remain precise?
3. **Coverage fit.** Does it fill a gap in the layer and category it
   claims, or is it cross-cutting in a way that suggests a different
   placement?

## 5. After merge

CI reruns the canonical non-destructive vocabulary workflow. Releases are not
cut per PR; the merged pattern becomes available through the living GitHub
source immediately and through PyPI at the next versioned release. If the
change affects paper content or paper-cited hashes, the maintainer compiles the
paper with its existing style in the same PR.

## Refining or removing existing patterns

Pattern definitions are content-addressed: editing a pattern's mechanism
produces a new hash, not an in-place identity update. See
[Pattern Lifecycle](docs/guides/lifecycle.md) for refinement, supersession, and
consumer migration. The short version is: edit a staging copy, include the
last public `sema_id` in `_meta.supersedes`, apply through `sema apply`, export,
and run the canonical verification workflow.

To remove a pattern from the vocabulary database:

```bash
sema apply --remove HandleName
```

This fails if other patterns depend on the one being removed. The error message
will list the dependents; remove or update them atomically, then export and
verify the resulting vocabulary.

## Local development

```bash
git clone https://github.com/emergent-wisdom/sema.git
cd sema
python -m venv .venv && source .venv/bin/activate
pip install -e ".[full]"
pytest

# Run the complete non-destructive vocabulary workflow
python scripts/verify_vocabulary_change.py
```

Audits remain importable modules, so an individual diagnostic can also be run
directly, for example `python -m sema.audit.rigor`. The full workflow includes
the consolidated audit and all blocking vocabulary checks.

To browse the vocabulary in the web UI while you work:

```bash
# Terminal 1: API
sema serve --port 3001

# Terminal 2: dev frontend with hot reload
cd web && npm install && npm run dev
# http://localhost:5173
```

## Cutting a release

We don't release per PR — PRs add entries to the `[Unreleased]` section of
`CHANGELOG.md`. A release is a separate act: rename that section to
`[X.Y.Z] - YYYY-MM-DD`, bump `pyproject.toml`, merge, then run the
release script.

1. **Prep commit (on a branch):**
   - Rename `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md`
     (add a fresh empty `## [Unreleased]` above it).
   - Edit `pyproject.toml` → `version = "X.Y.Z"`.
   - Commit. The `sync-release-metadata` pre-commit hook auto-updates
     `.claude-plugin/plugin.json` and `server.json` to match.
   - Open PR, merge to main.

2. **Ship (from main, after merge):**
   ```
   scripts/release.sh
   ```
   Pre-flights (clean tree, on main, tests green, metadata synced), then
   prompts through: create tag → push → `gh release create` (triggers
   `publish.yml` → PyPI) → `mcp-publisher publish server.json`. Use
   `--dry-run` for a preview, `--yes` to skip prompts.

PyPI publishing is automated (trusted publishing via
`.github/workflows/publish.yml` on GitHub release). The MCP Registry
push requires a one-time `mcp-publisher login` (GitHub OAuth, cached).

## Documentation

- [docs/guides/lifecycle.md](docs/guides/lifecycle.md) — hash identity,
  refinement, supersession, handshake semantics
- [docs/guides/authoring.md](docs/guides/authoring.md) —
  full schema and authoring rules
- [docs/specification/validation.md](docs/specification/validation.md) —
  Forward/Inverse rules, Gravity, Empty Fields
- [docs/specification/naming.md](docs/specification/naming.md) — handle
  conventions, layer/category placement
- [docs/core/philosophy.md](docs/core/philosophy.md) — why
  content-addressing works
