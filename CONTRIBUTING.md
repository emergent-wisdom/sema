# Contributing to Sema

## Setup

```bash
git clone https://github.com/emergent-wisdom/sema.git
cd sema
python -m venv .venv && source .venv/bin/activate
pip install -e ".[full]"
```

Verify:

```bash
sema search "coordination"
sema resolve StateLock
sema skeleton
```

## Browse the Vocabulary

Start the API server and web frontend:

```bash
# Terminal 1: API server
sema serve --port 3001

# Terminal 2: Frontend (dev mode with hot reload)
cd web
npm install
npm run dev
# Open http://localhost:5173
```

The frontend proxies `/api` requests to `localhost:3001`.

For production (no hot reload), build the frontend into the server:

```bash
cd web && npm run build
cp -r dist/* ../src/sema/server/static/
sema serve  # Frontend + API on http://localhost:3000
```

## Pattern Anatomy

Every pattern is a JSON file in `data/vocabulary/`. Minimum required fields:

```json
{
  "handle": "MyPattern",
  "mechanism": "Description of what this pattern does and how it works.",
  "gloss": "One-line summary for search results",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 2,
    "tier": 1
  }
}
```

### Fields

| Field | Required | Hashed | Description |
|-------|----------|--------|-------------|
| `handle` | Yes | Yes | PascalCase name, unique across vocabulary |
| `mechanism` | Yes | Yes | The definition. Use `{{key}}` to reference dependencies |
| `gloss` | Yes | Yes | Short summary (used for semantic search) |
| `_meta.layer` | Yes | No | `Physics`, `Mind`, `Society`, or `Infrastructure` |
| `_meta.category` | Yes | No | Functional group within the layer |
| `_meta.ring` | Yes | No | Stability: `0` = Kernel, `1` = StdLib, `2` = User |
| `_meta.tier` | Yes | No | Rigor: `0` = Primitive, `1` = Hard, `2` = Soft |
| `dependencies` | If `{{refs}}` used | Yes | Maps `{{key}}` placeholders to full sema IDs |
| `signature` | No | Yes | Type constructor, e.g. `["Check(Proof)"]` |
| `invariants` | No | Yes | Safety constraints that always hold |
| `preconditions` | No | Yes | Required state before execution |
| `postconditions` | No | Yes | Guaranteed state after execution |
| `failure_modes` | No | Yes | Known risks |

### Layers

| Layer | What lives here |
|-------|----------------|
| **Physics** | Immutable primitives: locks, entropy, causality, state |
| **Mind** | Reasoning patterns: inference, strategy, cognitive tools |
| **Society** | Multi-agent coordination: protocols, governance, economics |
| **Infrastructure** | Operational: data structures, verification, tooling |

### Dependencies

If your mechanism text references another pattern, use `{{snake_case_key}}` and declare it in `dependencies.references`:

```json
{
  "handle": "MyPattern",
  "mechanism": "First acquire a {{lock}} on the shared {{state}}, then verify using {{check}}.",
  "gloss": "Example pattern with dependencies",
  "_meta": { "layer": "Society", "category": "Protocols", "ring": 2, "tier": 1 },
  "dependencies": {
    "references": {
      "lock": "sema:Lock#mh:SHA-256:5bf2a80b6c73a11da68f702922d5180259c75ff50fb094607da3ab4d7c167dc2",
      "state": "sema:State#mh:SHA-256:4d582a0ac4af7ae886c83da9825e07c39f1e72ece21fd65a40b6a4fc71882721",
      "check": "sema:Check#mh:SHA-256:0a1b..."
    }
  }
}
```

Look up hashes with `sema resolve <Handle>`.

## Add a Pattern

1. **Write** your pattern JSON file (e.g. `MyPattern.json`)

2. **Validate** without applying:
   ```bash
   sema apply --check --add MyPattern.json
   ```
   The validator checks:
   - All required fields present
   - Every `{{key}}` in mechanism has a matching dependency
   - Every dependency is used in the text
   - No empty arrays or objects
   - No circular dependencies

3. **Apply** to the vocabulary:
   ```bash
   sema apply --add MyPattern.json
   ```
   This computes the content hash and adds the pattern to the taxonomy database.

4. **Verify** it works:
   ```bash
   sema search "your pattern topic"
   sema resolve MyPattern
   ```

5. **Submit** a pull request with your pattern JSON file.

## Improve an Existing Pattern

1. Find the pattern: `sema resolve <Handle>` or browse at `http://localhost:5173`
2. Edit the JSON file in `data/vocabulary/<Handle>.json`
3. Run `sema apply --check --add data/vocabulary/<Handle>.json` to validate
4. Apply and verify

Changing the mechanism, gloss, or dependencies will produce a new hash — this is by design. The old hash becomes invalid, which is how Sema detects semantic drift.

## Remove a Pattern

```bash
sema apply --remove HandleName
```

This fails if other patterns depend on the one being removed. Remove or update dependents first.

## Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Forward dependency violation: {{foo}} not declared` | Used `{{foo}}` in text without importing | Add to `dependencies.references` |
| `Field required: _meta` | Missing metadata block | Add `_meta` with layer, category, ring, tier |
| `Field required: _meta.ring` | Incomplete metadata | Add ring (0-2) and tier (0-2) |

## Documentation

- [Pattern Authoring Guide](docs/specification/authoring.md) — Complete guide: schema, all rules (A-K), hashing protocol, naming morphology, staging workflow
- [Validation Matrix](docs/specification/validation-matrix.md) — All 42 compiler checks with implementation status
- [Schema Specification](docs/specification/schema.md) — Full JSON schema reference
- [Validation Rules](docs/specification/validation.md) — Core invariants (Forward/Inverse rules, Gravity, Empty Fields)
- [Naming & Taxonomy](docs/specification/naming.md) — Handle conventions, layer/category rules
- [Philosophy](docs/core/philosophy.md) — Why content-addressing works

## Development

### Run tests
```bash
pytest
```

### Build the package
```bash
uv build
```

### MCP server (for AI agents)
```bash
sema mcp  # Starts stdio MCP server
```
