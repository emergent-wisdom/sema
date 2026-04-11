# Pattern Authoring Guide

This guide covers the practical workflow for creating and modifying patterns. It assumes you've read the [Core Philosophy](../core/philosophy.md), [Pattern Card schema](../specification/schema.md), and [Validation Rules](../specification/validation.md).

## Authoring Checklist

Before submitting a pattern, verify:

- [ ] JSON conforms to the [Pattern Card schema](../specification/schema.md)
- [ ] Every `{{key}}` in text is declared in `dependencies` (Forward Rule)
- [ ] Every key in `dependencies` is used as `{{key}}` in text (Inverse Rule)
- [ ] Dependencies use **snake_case keys** and **Full Hashes** (`sema:Handle#mh:SHA-256:...`)
- [ ] Each dependency is in exactly one category (`accepts`, `yields`, `composes_with`, `references`)
- [ ] No empty fields (`[]`, `{}`, `null`) — omit instead
- [ ] Signatures use `Intent(Target)` form, not bare names
- [ ] Nouns / data structures define `data_schema`
- [ ] `_meta` has all four fields: `layer`, `category`, `ring`, `tier`
- [ ] Handle follows [Naming Taxonomy](../specification/naming.md) conventions
- [ ] `sema apply --check` passes
- [ ] No collisions: `sema search "your handle"` returns no conflicts

For the full rule set, see [Validation Rules](../specification/validation.md). For lifecycle context (what happens after apply), see [Pattern Lifecycle](lifecycle.md).

---

## Workflow (CLI First)

**The Database is the Source of Truth.** The `taxonomy.db` database is authoritative. Files in `data/vocabulary/` are **exports**, not sources.

**Never edit vocabulary files directly — use `sema apply` to make changes.**

### Adding a New Pattern

1.  **Create**: Write your new pattern JSON in `data/staging/`.
    ```bash
    # Example: data/staging/NewPattern.json
    ```
2.  **Validate**: Run `sema apply --add data/staging/NewPattern.json --check`.
    *   This catches dependency cycles and schema errors *before* applying.
3.  **Apply**: Run `sema apply --add data/staging/NewPattern.json`.
    *   This adds the pattern to `taxonomy.db`.
4.  **Commit**: Git commit your changes.
5.  **Clean**: Delete the staging file (it's now in the database).

### Modifying an Existing Pattern

1.  **Copy**: Copy the pattern from `data/vocabulary/` to `data/staging/`.
2.  **Edit**: Modify the file in `data/staging/`.
3.  **Apply**: Run `sema apply --add data/staging/PatternName.json`.
4.  **Commit**: Git commit your changes.
5.  **Clean**: Delete the staging file.

### Verification

*   To check for collisions or duplicates: `sema search "term"`
*   To resolve dependencies: `sema resolve <Handle>`

See [CLI Reference](../tools/cli.md) for the full command set.

---

## The "Deep Fix" Protocol

When the linter reports an **Unused Dependency** (Inverse Rule violation), do NOT blindly delete it. The dependency represents a semantic signal from a previous author. Triage:

1. **Keep & Explain (Missing Text):** The relationship is real (e.g., Task yields Solution), but the text failed to describe it.
   * *Action:* Update `mechanism` to explicitly reference `{{solution}}`.
2. **Refine Link (Wrong Target):** The relationship is real, but the target pattern is imprecise.
   * *Action:* Swap dependency for a better existing pattern.
3. **Mint New (Missing Concept):** The relationship implies a concept that doesn't exist yet.
   * *Action:* Create a new pattern.
4. **Remove (Hallucination):** The relationship is truly irrelevant or legacy.
   * *Action:* Delete the dependency key.

### Dependency Key Style

Use **snake_case keys** for dependency references:

* **Bad:** `mechanism: "Uses {{sema:Trace#...}}"` (embedding raw hash)
* **Bad:** `dependencies: { "composes_with": { "Logger": "..." } }, mechanism: "Uses {{Logger}}"` (PascalCase key)
* **Good:** `dependencies: { "composes_with": { "logger": "sema:Trace#..." } }, mechanism: "Uses {{logger}}"`
