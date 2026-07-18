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
- [ ] `_meta` has a valid `path` plus `ring` and `tier`
- [ ] Handle follows [Naming Taxonomy](../specification/naming.md) conventions
- [ ] Short/general handles pass the Occupancy Test and contain only the
  broad-use intersection; specialized policy lives in descendants or callers
- [ ] Every hashed contract is identity-defining, cross-context, and testable
  without unstated domain policy
- [ ] `sema apply --check` passes
- [ ] No collisions: `sema search "your handle"` returns no conflicts

For the full rule set, see [Validation Rules](../specification/validation.md). For lifecycle context (what happens after apply), see [Pattern Lifecycle](lifecycle.md).

---

## Workflow (CLI First)

**The Database is the Source of Truth.** The `taxonomy.db` database is authoritative. Files in `data/vocabulary/` are **exports**, not sources. The bundled (pip-installed) DB is read-only; use `sema build` + `sema use` to create a writable project copy.

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

---

## Manual-Driven Refinement Loop

Editing the vocabulary is not a one-shot activity. Once the library exists, the way you improve it is to **read the design manual, act on what the analysis surfaces, and feed the result back into the manual**. The manual is both the review surface and the source of refinement pressure — it closes the loop.

### The Four Artifacts

| Artifact | Role |
|---|---|
| `data/vocabulary/<Handle>.json` | Canonical export — **do not edit directly** |
| `data/staging/<Handle>.json` | Work-in-progress edit buffer |
| `data/design_critique.json` | Sidecar: per-pattern design commentary (editable source of the manual's per-pattern sections) |
| `docs/manuals/vocabulary-design.md` | Rendered manual — the review surface |

The sidecar and the manual are **not** part of the hash input. Editing commentary never changes a pattern's `sema_id`. Editing a pattern *does* change its hash and cascades through the DAG.

### The Loop

```
┌─────────────────────────────────────────────────────────────┐
│ 1. READ the manual (docs/manuals/vocabulary-design.md)       │
│    Find a pattern whose commentary flags a defect, a         │
│    weak invariant, a jammed failure mode, a broken ref,      │
│    a stance-vs-mechanism gap, etc.                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. COPY data/vocabulary/<Handle>.json to data/staging/       │
│    Make the fix in the staging copy.                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. UPDATE data/design_critique.json for the same handle      │
│    in the same turn. The commentary must reflect the fix     │
│    — stale commentary is worse than no commentary.           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PREVIEW the manual before applying.                       │
│    `python scripts/generate_design_manual.py`                │
│    The generator is staging-aware — it prefers staging over  │
│    vocabulary when present, so the preview reflects the      │
│    edit without requiring an apply round-trip.               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. APPLY: `sema apply --add data/staging/<Handle>.json`      │
│    Patterns hash, cascade through dependents, export to      │
│    data/vocabulary/. Before applying: if the edit changes    │
│    the hash against the last public release, add the prior   │
│    sema_id to `_meta.supersedes` — required for every        │
│    change, not just renames. See Lifecycle §4 "Populating    │
│    _meta.supersedes" for the rule and its (non-)enforcement. │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. REGENERATE the manual post-apply.                         │
│    `python scripts/generate_design_manual.py`                │
│    Now the manual renders from the canonical vocabulary      │
│    (staging is clean). Commit the manual alongside the       │
│    pattern change.                                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. VERIFY and CLEAN.                                         │
│    - `python -m sema.audit.hash_validity` — exported hashes  │
│      match their recomputed definitions.                     │
│    - `python scripts/rebuild_vocabulary.py`                   │
│      A clean rebuild reproduces the same hashes.             │
│    - `pytest` — regression tests green.                      │
│    - Delete data/staging/<Handle>.json once applied.         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                   ── Loop back to step 1 ──
```

### Rules that hold across the loop

- **Change + commentary move together.** Never edit a pattern without updating its sidecar entry in the same turn. The manual rendered from a stale sidecar is actively misleading — it looks authoritative but describes a pattern that no longer exists.
- **Staging is ephemeral.** The presence of a file in `data/staging/` means "edit in flight." Once applied, delete it. The staging-aware generator uses file presence as the signal for which version to render.
- **Sidecar entries are keyed by handle, not sema_id.** Renames require moving the entry under the new handle and deleting the old one; pure content edits need no sidecar key change.
- **Never edit the manual directly.** It's a rendered artifact. Edits to `vocabulary-design.md` will be overwritten on the next regeneration. Edit the sidecar instead.
- **Commit in phase bundles, not per-pattern.** A single commit typically touches: one or more staging JSONs (via apply, so also the corresponding vocabulary JSONs), the sidecar, the manual, and — if it changes against a public release — also CHANGELOG.md. Keep them together so the review surface and the spec stay consistent at every commit.

### When the Manual Surfaces a Finding You Don't Want to Act On

Some manual findings are intentionally open — e.g., the mechanism deliberately leaves room for descendants to specialize, or the pattern captures a philosophical stance rather than a mechanism. In that case, update the sidecar to **record the intent** ("open by design — descendants fill this in") rather than closing the gap in the pattern. The commentary then becomes a pointer for future readers instead of an unresolved TODO.

Missing fields are not a coverage target. Before adding a contract, apply the
manual's constraint-placement test: the requirement belongs in a general
parent only when omitting it would make the implementation cease to be that
pattern across every listed broad-use context. Put quantitative identity axes
in parameters, qualitatively different strategies in descendants, deployment
policy in callers, and contextual risks or reviewer diagnostics in the
sidecar. Concrete leaf patterns may remain deliberately narrow; the reusable
ancestry spine is where over-specificity causes ecosystem-wide damage.

Treat sidecar commentary as review evidence, not as a second specification or
a backlog of contracts to add. Phrase critique around the semantic risk and
its likely placement. Field-count complaints such as "only two invariants" are
not actionable without an identity argument; rewrite them as a concrete
question, descendant opportunity, caller policy, or reviewer diagnostic.

### Prototypical Examples

- The 0.2.0 release's **50 post-audit structural fixes** (dedup, split, broken-ref cleanup) were driven by this loop: manual surfaced internal defects → staging edits addressed them → sidecar commentary updated → apply + regenerate → CHANGELOG reflected the batch. See the `Additional structural fixes (50 patterns)` section in `CHANGELOG.md`.
- The **full supersedes population** (360 patterns) was a batch-run through this loop focused on a single field (`_meta.supersedes`) rather than semantic content — a reminder that the loop scales from single-pattern refinement to full-library sweeps.
