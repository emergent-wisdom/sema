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
`pip install semahash` live in `data/vocabulary/` in this repo.
Contributions to the canonical vocabulary go through GitHub PRs against
that directory. The rest of this document is about that path.

## 1. Author a pattern

Create a JSON file in `data/vocabulary/<NewPattern>.json`. Required
fields are `handle`, `mechanism`, `gloss`, and `_meta` with `layer`,
`category`, `ring`, `tier`. See [docs/specification/authoring.md](docs/specification/authoring.md)
for the full schema reference. A minimal pattern:

```json
{
  "handle": "MyPattern",
  "mechanism": "Description of what this pattern does and how it works.",
  "gloss": "One-line summary used by semantic search.",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  }
}
```

Use `{{snake_case}}` placeholders to reference other patterns; declare
each one in `dependencies.references`. Look up dependency hashes with
`sema show <Handle>`.

## 2. Validate locally

Before opening a PR, run all three:

```bash
# Schema, dependency wiring, and dependency-key usage check
sema apply --check --add data/vocabulary/MyPattern.json

# Fold into the local DB so search/show work against the new pattern
./scripts/rebuild_db.sh

# Sanity-check the result
sema show MyPattern
```

`sema apply --check` is a dry run — it never writes to the registry.
Once it passes, `rebuild_db.sh` rebuilds `data/taxonomy.db` from the
full `data/vocabulary/` directory and writes the new pattern's
canonical hash back into your JSON file.

## 3. PR checklist

A pattern PR is ready to review when:

- [ ] **The definition is tight.** Every `{{placeholder}}` resolves to
      a declared dependency (`sema apply --check` enforces this). Failure
      modes are concrete, not hand-wavy. Parameters, where used, have
      `name`, `type`, `range`, `description`.
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
   [docs/versioning.md](docs/versioning.md).)
2. **Specificity.** Is the mechanism concrete enough that two
   independent implementers would produce roughly the same thing? Vague
   patterns dilute the vocabulary.
3. **Coverage fit.** Does it fill a gap in the layer and category it
   claims, or is it cross-cutting in a way that suggests a different
   placement?

## 5. After merge

The maintainer runs `./scripts/rebuild_db.sh`, then
`./scripts/compile_paper.sh` to refresh the paper's hash references,
bumps the package version, and publishes a new PyPI release. Your
pattern is then available to anyone running `pip install --upgrade
semahash`, and to any MCP client that points at the bundled DB.

## Refining or removing existing patterns

Pattern definitions are content-addressed and immutable: editing a
pattern's mechanism produces a new hash, not an in-place update. Old
hashes remain valid forever. See [docs/versioning.md](docs/versioning.md)
for the full policy on refinement, supersession, and what
`sema_handshake` does across versions. The short version is: edit the
JSON, run `./scripts/rebuild_db.sh`, and the new hash becomes the
current canonical stub for the handle.

To remove a pattern from the vocabulary:

```bash
sema apply --remove HandleName
```

This fails if other patterns depend on the one being removed. The error
message will list the dependents; remove or update them in the same PR.

## Local development

```bash
git clone https://github.com/emergent-wisdom/sema.git
cd sema
python -m venv .venv && source .venv/bin/activate
pip install -e ".[full]"
pytest
```

To browse the vocabulary in the web UI while you work:

```bash
# Terminal 1: API
sema serve --port 3001

# Terminal 2: dev frontend with hot reload
cd web && npm install && npm run dev
# http://localhost:5173
```

## Documentation

- [docs/versioning.md](docs/versioning.md) — hash immutability,
  refinement, supersession, handshake semantics
- [docs/specification/authoring.md](docs/specification/authoring.md) —
  full schema and authoring rules
- [docs/specification/validation.md](docs/specification/validation.md) —
  Forward/Inverse rules, Gravity, Empty Fields
- [docs/specification/naming.md](docs/specification/naming.md) — handle
  conventions, layer/category placement
- [docs/core/philosophy.md](docs/core/philosophy.md) — why
  content-addressing works
