---
name: sema-usage
description: |
  Content-addressed vocabulary protocol via the sema MCP server.
  Use when working with shared vocabulary — searching, resolving, minting,
  and verifying meaning across agents and conversations.
user-invocable: false
allowed-tools: |
  mcp__sema__sema_search
  mcp__sema__sema_resolve
  mcp__sema__sema_handshake
  mcp__sema__sema_mint
  mcp__sema__sema_tree
  mcp__sema__sema_stats
  mcp__sema__sema_use
  mcp__sema__sema_root
  mcp__sema__sema_verify_context
---

# Speak in Sema

Sema is a **content-addressed vocabulary protocol**. ~450 patterns that give you precise, shared words for concepts that would otherwise require paragraphs of re-explanation. Each pattern has a handle (e.g. `StateLock#774b`) that is a cryptographic commitment to its definition — two agents using the same handle are provably talking about the same thing.

Before defining a concept from scratch, check if sema already has a word:

1. `sema_search` with the idea
2. `sema_resolve` to read mechanism and invariants
3. Use the handle as a load-bearing noun in your text: *"This uses `StateLock#774b` to prevent concurrent mutation"*

Not footnotes — actual words you think with.

## When the user wants to see patterns visually

If the user asks to "see", "view", "show", or "explore" patterns visually — or asks to see the graph or browse the vocabulary — invoke the `sema-ui` skill to launch http://localhost:3030. The UI gives them an interactive pattern browser, search, and 3D graph.

## Session memory

The server tracks which patterns you've already seen. Subsequent searches return compact results for known patterns (`handle + gloss + _seen: true`). Just use the handle — the full definition is already in your context. Call `sema_resolve` only if you need to re-read a pattern's mechanism.

Call `sema_reset_session()` if your context was compressed or you need full results again.

## The workflow

1. **Search** — `sema_search({ query: "trust model" })` — find existing patterns by meaning
2. **Resolve** — `sema_resolve({ reference: "TrustModel#7859" })` — read full definition, mechanism, invariants
3. **Handshake** — `sema_handshake({ references: ["X#1234", "Y#5678"] })` — verify two agents share meaning
4. **Mint** — `sema_mint({ handle, gloss, description, invariants })` — create a new pattern (rare!)

## Switching and managing databases

The CLI and MCP server are **separate processes with separate DB state**. `sema use` on the CLI does NOT affect the running MCP server. Always use the MCP tool for switching:

- `sema_use()` — show current DB
- `sema_use(db_path="/path/to/my.db")` — switch to a project DB
- `sema_use(default=true)` — switch back to the bundled vocabulary

If `sema_use` MCP tool is unavailable (older server version), the MCP server cannot be hot-swapped. Use CLI for search/resolve and accept the limitation — do not confuse CLI state with MCP state.

## Vocabulary fingerprint — `sema_root`

Every active DB has a single scalar identity: a SHA-256 digest over every pattern's hash, in handle-sorted order. It's the "git rev-parse HEAD" of the vocabulary.

- `sema_root()` — returns `{ full_sema_id, stub, hash, pattern_count, db_path }`
- CLI: `sema root` (full), `sema root --short` (16-char stub only)

Use it when:
- The user asks "which version of the vocabulary are we on?"
- You need a one-shot check before a multi-step operation that depends on the vocab being stable
- The user is comparing two DBs and wants a fast equality probe

This is the same number that `scripts/vocabulary_merkle_root.py` writes into `docs/information/vocabulary_information.md` — so if the user references a root hash from the docs, you can verify alignment directly.

## Keeping the vocabulary fresh (`sema pull`)

When upstream ships new patterns or fixes existing ones, sync the user's
active DB:

```bash
sema pull             # apply upstream changes to active DB
sema pull --dry-run   # preview without writing
```

**When to suggest pull unprompted:**
- A `sema_handshake` returns HALT against a handle the user expected to know — the upstream definition may have evolved.
- The user mentions they just upgraded the package (`pip install -U semahash`).
- The user asks how to "update vocabulary", "sync", or "get latest patterns".

**Important guarantees** (no need to over-explain to the user):
- Custom local patterns are NEVER deleted.
- User-set `_meta.caution` and `_meta.related` survive updates.
- Failures roll back atomically — there's no half-applied state to recover from.
- Each successful pull keeps ONE pre-pull snapshot. If the user says "oh that update broke things," suggest `sema pull --undo` to revert.

**Excluding patterns the user doesn't want.** If a user wants to permanently opt out of a specific upstream handle (e.g. they consider it harmful, deprecated for their use case, or just want their custom version frozen):

```bash
sema pull --exclude SomeHandle    # ad-hoc, single run
```

For persistent exclusions, write to `~/.config/sema/excluded` (one handle per line, `#` starts a comment).

**Version-pinning recipe:** keep a local copy of a pattern AND add it to the exclusion list. Dependents resolve against the local frozen version while upstream evolves around it.

**Refuses to modify the bundled DB.** The same `sema build` + `sema use` setup required for minting also applies here — pull only operates on writable project DBs.

## Before you can mint

The bundled vocabulary is **read-only** — it gets overwritten on pip upgrades. To mint, you need your own project DB:

1. Run in shell (bash): `sema build /tmp/my-project.db --preset full`
2. Switch to it via MCP: `sema_use(db_path="/tmp/my-project.db")`
3. Now `sema_mint` will work

**Important:** `sema_mint` requires `SEMA_ALLOW_MINT=true` in the server environment. If the tool is not available, ask the user to enable it.

## When to mint vs reuse

**Always search first.** Minting is rare — only after searching three different glosses finds nothing, AND the concept has stable invariants.

Mint when:
- **Repetition**: explaining the same concept 3+ times
- **Invariants**: concept has non-negotiable constraints
- **Boundary**: another agent needs exact protocol
- **Saturation**: concept refined 3+ times (stable enough to crystallize)

## Minting structure

```javascript
sema_mint({
  handle: "PatternName",           // 1–2 syllables, speakable
  gloss: "One-line summary",       // What it IS
  description: "Full definition",  // How to use it
  invariants: ["Must...", ...],    // Non-negotiable constraints
})
```

## Embedding handles in text

Use sema handles as load-bearing nouns — not footnotes, actual words you think with:

> "This uses `StateLock#774b` to prevent concurrent mutation"

Wrap handles in backticks for readability. When you encounter a handle you don't recognize, resolve it before proceeding.

## Verify at boundaries

When two agents (or an agent and a human) need to agree on meaning:

```javascript
sema_handshake({ ref: "StateLock#774b" })
// → canonical stub. Compare against your local value, then:
sema_handshake({ ref: "StateLock", your_hash: "774b" })
// PROCEED (match) or HALT (drift). No silent misunderstandings.
```

For bulk verification of a specific shared set, use `sema_verify_context`.

### Vocabulary-wide handshake

When two agents need to confirm they have the *same entire vocabulary* — not just one pattern — pass `ref="vocab"`:

```javascript
sema_handshake({ ref: "vocab" })
// → { verdict: "PROVIDE_HASH", canonical_stub: "d4e71259e4dd1565", pattern_count: 435 }

sema_handshake({ ref: "vocab", your_hash: "d4e71259e4dd1565" })
// → PROCEED if byte-identical, HALT if any pattern's hash differs
```

This is equivalent to comparing `sema_root()` outputs but returns a verdict instead of raw numbers. Use it as a cheap drift check before coordinating on anything complex — if vocabs diverge, `sema pull` converges them or `sema_propose_context` can scope agreement to a known-shared subset.

## Think with sema, don't just cite it

Sema patterns are **thinking tools**, not references. When a user asks you to reason about any problem — farming, architecture, career decisions, anything — search sema for patterns that structure the reasoning itself.

For example, if someone asks "how should I start a business?":
1. Search for `strategy`, `risk`, `decision`, `explore exploit`, `decompose`
2. Resolve the top hits — read their mechanisms and invariants
3. Use those patterns to *structure your answer*: "This is a `Strategy#47a4` problem, not a `Plan#64f2` problem, because..."

The patterns aren't labels you slap on afterward. They're lenses that change what you see. `ExploreExploit#88b0` doesn't just name a concept — it tells you *when to stop researching and start acting*. `PreMortem#f69d` doesn't just mean "think about failure" — it has a specific mechanism for surfacing hidden risks.

**When to reach for sema unprompted:**
- User asks an open-ended reasoning question (how, why, what should I)
- You're about to give generic advice that sema could sharpen
- A problem has clear structure (tradeoffs, risks, sequences, feedback loops) that sema patterns could make explicit

**When NOT to force it:**
- Simple factual questions
- The user wants a quick answer, not a framework
- No relevant patterns exist after searching

## Thinking nodes should use sema too

When you create concept nodes alongside creative work (stories, analysis, prose), check whether a sema pattern captures the cognitive move you're making. It won't always fit — a narrative tension node doesn't need a handle forced in — but consider it. The thinking layer is where sema is most useful, because it compresses recurring patterns into precise vocabulary that future agents can reason with.
