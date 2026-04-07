# Vocabulary Maintenance

## The Workflow

Sema uses a "Fail-Fast" approach to vocabulary maintenance. All changes go through `sema apply`, which validates everything before committing.

### Add Patterns

```bash
# Validate without applying
sema apply --check --add MyPattern.json

# Apply (validates, hashes, and adds to taxonomy database)
sema apply --add MyPattern.json

# Add an entire directory of patterns
sema apply --add data/staging/
```

### Remove Patterns

```bash
# Fails if other patterns depend on it
sema apply --remove MyPattern
```

### Atomic Add + Remove

```bash
sema apply --add NewPattern.json --remove OldPattern
```

## What `sema apply` Does

1. **Validates** all pattern JSON files against the schema
2. **Checks dependency integrity** — every `{{key}}` must be declared, every declaration must be used
3. **Detects circular dependencies** via topological sort
4. **Computes content hashes** (SHA-256 Merkle tree)
5. **Adds to taxonomy database** (`data/taxonomy.db`)

If any step fails, nothing is applied.

## Validation Rules

The validator enforces:

- **Forward Rule:** Every `{{key}}` in text must have a matching dependency entry
- **Inverse Rule:** Every declared dependency must be used in the text
- **No Empty Fields:** No `[]`, `{}`, or `null` — omit fields instead
- **Complete Metadata:** `_meta` must include `layer`, `category`, `ring`, `tier`
- **Signature Syntax:** Must use `Intent(Target)` form, not bare names

## Troubleshooting

### Explicit Dependency Violation

```
❌ Forward dependency violations: '{{tool_invoke}}' used in 'mechanism' but not declared in dependencies
```

**Fix:** Add `"tool_invoke": "sema:ToolInvoke#..."` to `dependencies.references` (or the appropriate category).

### Empty Field Violation

```
❌ EMPTY FIELD RULE VIOLATION: dependencies = {}
```

**Fix:** Delete the field entirely. If a pattern has no dependencies, omit the `dependencies` block.

### Missing Metadata

```
❌ _meta.ring; ❌ Field required
```

**Fix:** Ensure `_meta` has all four fields: `layer`, `category`, `ring`, `tier`.

## Best Practices

- **Validate first:** Always run with `--check` before applying
- **Small batches:** Debugging 3 new patterns is easier than 30
- **Review dependencies:** A dependency is a semantic claim. Don't auto-fix without understanding the relationship
- **Use staging:** Put work-in-progress patterns in `data/staging/`, move to `data/vocabulary/` when ready
