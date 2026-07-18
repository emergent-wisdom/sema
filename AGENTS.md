# Repository Agent Guide

This file is the repository-level operating context for coding agents. Detailed
domain rules remain in the linked specifications; do not duplicate or invent
them from prompt context.

## Development Workflow

- Work on a focused feature branch and use a pull request. Do not merge until
  required CI is green.
- Keep unrelated user changes intact and surface unrelated defects separately.
- Use `Henrik Westerberg <henrik.westerberg@emergentwisdom.org>` for locally
  authored commits. GitHub-created merge commits may use the account's noreply
  address; merge locally when every commit must use the organization address.
- Website and frontend experiments must remain on an isolated branch and
  staging service until Henrik explicitly approves production deployment.
- Paper typography or stylesheet work must remain separate from semantic paper
  updates unless visual redesign is the stated scope.

## Vocabulary Changes

Read these before editing patterns:

- `docs/guides/authoring.md`
- `docs/guides/lifecycle.md`
- `docs/specification/schema.md`
- `docs/specification/validation.md`

The database is authoritative. Copy exported JSON from `data/vocabulary/` into
`data/staging/`, edit staging, update `data/design_critique.json`, preview the
manual, apply through `sema apply`, export from `data/taxonomy.db`, and remove
the staging file. Never edit canonical vocabulary exports directly.

General handles contain only the broad-use intersection. Put qualitatively
different strategies in descendants, quantitative identity axes in parameters,
deployment policy in callers, and contextual risks in the design sidecar.
Missing invariants or failure modes are not automatically defects. Sidecar
critique is diagnostic evidence, not a backlog of contracts to add.

After apply/export and staging cleanup, run:

```bash
python scripts/verify_vocabulary_change.py --refresh
python scripts/verify_vocabulary_change.py
```

`--refresh` retains regenerated manuals, audit reports, vocabulary information,
and current documentation hash references. Check mode is non-destructive and
also verifies database/export parity, every exported hash, and a clean
deterministic rebuild. Review all generated changes before committing.

If paper content or a paper-cited hash changes, also run
`scripts/compile_paper.sh` using the existing style. Do not use semantic work as
an opportunity to alter typography.
