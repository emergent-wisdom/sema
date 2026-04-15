---
name: sema-mint
description: |
  How to mint new sema patterns — the full pipeline from concept to
  content-addressed vocabulary entry. Covers required fields, dependency
  wiring, validation rules, and the hashing model.
user-invocable: false
allowed-tools: |
  mcp__sema__sema_search
  mcp__sema__sema_resolve
  mcp__sema__sema_mint
  mcp__sema__sema_validate
  mcp__sema__sema_tree
---

# Minting Sema Patterns

Minting creates a new content-addressed pattern in the sema vocabulary. The definition IS the identity — hash the content, get the name. Change one invariant, get a different hash.

## Before you start a minting session

**1. Check that minting is enabled.** If `sema_mint` is not in your available MCP tools, the server was started without `SEMA_ALLOW_MINT=true`. Tell the user:

> "Minting isn't currently enabled. To turn it on, exit Claude Code and restart with `SEMA_ALLOW_MINT=true` set in your environment, then come back and we can mint."

**2. Make sure the active DB is writable.** The bundled vocabulary is read-only — minting into it will be blocked with an error. If the user wants to mint, they need a project DB:

```bash
sema build my-project.db --preset full
sema use my-project.db
```

Or use `sema_use(db_path="...")` via MCP.

**3. Offer the UI.** Ask: *"Want to open the Sema UI to watch the patterns appear as they get minted?"* If yes, invoke the `sema-ui` skill. The UI refreshes every 5 seconds locally, so each new pattern appears within a few seconds of being minted.

## When to mint

**Minting is rare.** Before minting, search at least three different glosses. Only mint when:
- You've explained the same concept 3+ times across conversations
- The concept has stable, non-negotiable invariants
- Another agent needs the exact protocol to coordinate
- A graph concept has been refined 3+ times (stable enough to crystallize)

## The pipeline

`sema_mint(pattern_json)` runs a full validation + hash + store pipeline:

1. **Parse** — JSON syntax check
2. **Schema validate** — required fields, handle format, layer/category validity
3. **Dependency wiring** — every `{{placeholder}}` in text must be declared in dependencies; every declared dependency must be used
4. **DAG check** — no cycles in the dependency graph; topological sort
5. **Layer direction** — lower layers cannot depend on higher layers (Infrastructure < Physics < Mind < Society)
6. **Merkle hash** — hash only the semantic fields to produce the content-addressed identity
7. **Store** — add to vocabulary database with computed `sema_id`, `sema_ref`, `sema_stub`

If any step fails, the pattern is rejected with an error message. No partial writes.

## Required fields

```json
{
  "handle": "MyPattern",
  "mechanism": "How it works, referencing {{dependency_key}} placeholders",
  "gloss": "One-line summary",
  "_meta": {
    "layer": "Mind",
    "category": "Reasoning",
    "ring": 1,
    "tier": 2
  }
}
```

| Field | Rules |
|-------|-------|
| `handle` | PascalCase, alphanumeric, 1-50 chars. Must be unique in the vocabulary |
| `mechanism` | How the pattern works. Must reference all dependencies via `{{snake_case_key}}` |
| `gloss` | One-line summary of what the pattern IS |
| `_meta.layer` | One of: `Infrastructure`, `Physics`, `Mind`, `Society` |
| `_meta.category` | Valid for the layer (see category table below) |
| `_meta.ring` | `0` (core), `1` (extended), `2` (experimental) |
| `_meta.tier` | `0` (primitive), `1` (ironclad), `2` (honesty-dependent), `3` (experimental) |
| `_meta.caution` | Optional. One-sentence warning about elevated risk. Add only if the risk isn't already obvious from the pattern's invariants or failure_modes, and adding it promotes safer use. |

### When to add a `caution` flag

Add `_meta.caution` if:
- The pattern enables irreversible action (data loss, financial commitment, governance changes)
- The pattern bypasses safety checks or oversight
- The pattern enables evasion, manipulation, or covert coordination
- The risk isn't already explicit in the mechanism, invariants, or failure_modes

Skip the flag if:
- The pattern's existing fields make the risk self-evident
- The pattern is purely cognitive (a reasoning lens) with no external effect

The caution sits in `_meta` (unhashed), so it can be revised without changing the pattern's identity.

### Layer categories

| Layer | Categories |
|-------|-----------|
| Infrastructure | Primitives, Data Structures, Safety, Verification |
| Physics | Dynamics, Primitives, Time |
| Mind | Inference, Memory, Reasoning, Strategy |
| Society | Coordination, Economics, Governance, Protocols, Roles |

## Recommended fields

| Field | What | Format |
|-------|------|--------|
| `invariants` | Conditions that must always hold | List of strings |
| `preconditions` | What must be true before applying | List of strings |
| `postconditions` | What is guaranteed after applying | List of strings |
| `failure_modes` | Known ways the pattern can fail | List of strings |
| `signature` | Type signature | List in `Verb(Noun)` format |
| `parameters` | Configurable knobs | List of `{name, type, range, description}` |

**Never use empty lists `[]` or empty objects `{}`.** Omit the field instead.

## Dependencies

Dependencies are the structural wiring between patterns. Four categories:

| Category | Meaning |
|----------|---------|
| `references` | Pattern mentions or builds on another |
| `composes_with` | Pattern combines with another at runtime |
| `accepts` | Input types the pattern consumes |
| `yields` | Output types the pattern produces |

Each key must be `snake_case` and used as a `{{placeholder}}` in mechanism, invariants, preconditions, postconditions, or failure_modes.

```json
"dependencies": {
  "references": {
    "think": "sema:Think#mh:SHA-256:e1bd..."
  },
  "composes_with": {
    "reflexion": "sema:Reflexion#mh:SHA-256:51b9..."
  },
  "accepts": {
    "context": "sema:Context#mh:SHA-256:510a..."
  },
  "yields": {
    "datum": "sema:Datum#mh:SHA-256:31cf..."
  }
}
```

### Wiring rules

- **Forward rule**: every `{{key}}` used in text fields MUST be declared in dependencies
- **Inverse rule**: every key declared in dependencies MUST be used at least once in text fields
- **Uniqueness**: each key appears in exactly one category
- **Layer direction**: cannot depend on a pattern from a higher layer

### Getting dependency hashes

Before minting, resolve the full `sema_id` of each dependency:

```
sema_resolve("Think")  →  sema_id: "sema:Think#mh:SHA-256:e1bd..."
```

Use the full `sema_id` as the dependency value. During initial minting (before the pattern has been hashed), you can use the handle alone — the pipeline will resolve it.

## The content hash

Only **semantic fields** are hashed — metadata and computed fields are excluded:

**Hashed:** `mechanism`, `gloss`, `invariants`, `preconditions`, `postconditions`, `failure_modes`, `dependencies`, `signature`, `parameters`, `data_schema`, `derived_from`

**NOT hashed:** `handle`, `_meta`, `sema_id`, `sema_ref`, `sema_stub`

This means: rename a pattern (change `handle`) and the hash stays the same. Change one invariant and you get a different hash. Same semantic content = same identity, guaranteed.

The hash uses a Merkle tree: strings are NFC-normalized, dicts are sorted by key, lists preserve order. The result is a SHA-256 digest truncated to a 4-char stub for human readability.

## Before you mint: the checklist

1. **Search three glosses** — `sema_search` with different phrasings. If >80% similar exists, don't mint.
2. **Resolve dependencies** — `sema_resolve` each pattern you'll reference. Get full `sema_id` values.
3. **Validate first** — `sema_validate` with your draft JSON. Fix all errors before minting.
4. **Check layer direction** — your pattern's layer must be >= all dependency layers.
5. **Wire all placeholders** — every `{{key}}` in text has a dependency; every dependency appears in text.
6. **No empty fields** — omit rather than `[]` or `{}`.

## Example: minting a pattern

```javascript
// 1. Search first
sema_search({ query: "pre-mortem risk analysis" })
// Nothing close enough — proceed

// 2. Resolve dependencies
sema_resolve({ handle: "Strategy" })   // → sema_id: "sema:Strategy#mh:SHA-256:47a4..."
sema_resolve({ handle: "Risk" })       // → sema_id: "sema:Risk#mh:SHA-256:8b2c..."

// 3. Validate draft
sema_validate({ pattern_json: JSON.stringify({
  "handle": "PreMortem",
  "mechanism": "Before committing to a {{strategy}}, assume it has already failed. Work backward to identify the most likely {{risk}} factors that caused the failure. Each identified risk becomes an input to mitigation planning.",
  "gloss": "Assume failure, then find what caused it",
  "invariants": [
    "Must be applied BEFORE commitment, not after",
    "Every identified {{risk}} must have a corresponding mitigation"
  ],
  "failure_modes": [
    "Anchoring: team fixates on one failure mode and misses others",
    "Premature closure: stopping after 2-3 obvious {{risk}} factors"
  ],
  "_meta": {
    "layer": "Mind",
    "category": "Strategy",
    "ring": 1,
    "tier": 2
  },
  "dependencies": {
    "references": {
      "strategy": "sema:Strategy#mh:SHA-256:47a4...",
      "risk": "sema:Risk#mh:SHA-256:8b2c..."
    }
  }
}) })

// 4. Mint
sema_mint({ pattern_json: "..." })
// → { success: true, handle: "PreMortem", sema_ref: "PreMortem#f69d", sema_id: "sema:PreMortem#mh:SHA-256:f69d..." }
```

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Missing required field | `handle` or `mechanism` absent | Add both |
| Unknown placeholder `{{key}}` | Used in text but not in dependencies | Add to dependencies |
| Unused dependency `key` | In dependencies but not used in text | Remove from dependencies or use it |
| Cycle detected | A→B→C→A | Restructure to break cycle |
| Invalid handle | Not PascalCase or has special chars | Rename to `PascalCase` |
| Empty list `[]` | Field present but empty | Omit the field entirely |
| Layer violation | Physics depends on Society | Reverse direction or reclassify |
| Dangling reference | Dependency target not in vocabulary | Mint the target first |
