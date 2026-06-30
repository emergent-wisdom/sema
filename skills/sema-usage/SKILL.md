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
  mcp__sema__sema_pull
  mcp__sema__sema_tree
  mcp__sema__sema_stats
  mcp__sema__sema_use
  mcp__sema__sema_root
  mcp__sema__sema_verify_context
---

# Speak in Sema

Sema is a **content-addressed vocabulary protocol**. ~450 patterns that give you precise, shared words for concepts that would otherwise require paragraphs of re-explanation. Each pattern has a handle (e.g. `StateLock#5602`) that is a cryptographic commitment to its definition — two agents using the same handle are provably talking about the same thing.

Before defining a concept from scratch, check if sema already has a word:

1. `sema_search` with the idea
2. `sema_resolve` to read mechanism and invariants
3. Use the handle as a load-bearing noun in your text: *"This uses `StateLock#5602` to prevent concurrent mutation"*

Not footnotes — actual words you think with.

## When the user wants to see patterns visually

If the user asks to "see", "view", "show", or "explore" patterns visually — or asks to see the graph or browse the vocabulary — invoke the `sema-ui` skill to launch http://localhost:3030. The UI gives them an interactive pattern browser, search, and 3D graph.

## Session memory

The server tracks which patterns you've already seen. Subsequent searches return compact results for known patterns (`handle + gloss + _seen: true`). Just use the handle — the full definition is already in your context. Call `sema_resolve` only if you need to re-read a pattern's mechanism.

Call `sema_reset_session()` if your context was compressed or you need full results again.

## The workflow

1. **Search** — `sema_search({ query: "trust model" })` — find existing patterns by meaning
2. **Resolve** — `sema_resolve({ handle: "TrustModel#7859" })` — read full definition, mechanism, invariants
3. **Handshake** — `sema_handshake({ ref: "X#1234" })` — verify exact meaning before relying on a handle
4. **Mint** — `sema_mint({ pattern_json: "..." })` — create a new pattern (rare!)

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

## Keeping the vocabulary fresh (`sema_pull` / `sema pull`)

When upstream ships new patterns or fixes existing ones, sync the user's active DB. This is available both as an MCP tool (prefer this — you get structured output) and as a CLI command:

```javascript
sema_pull()                              // apply upstream → active DB
sema_pull({ dry_run: true })             // preview without writing
sema_pull({ preserve_superseded: true }) // keep old handles alongside new
sema_pull({ exclude: ["SomeHandle"] })   // ad-hoc skip
```

The tool returns structured JSON: `added`, `updated`, `superseded_removed`, `superseded_kept_orphan`, `upstream_removed`, `vocabulary_root_before`, `vocabulary_root_after`. Read those fields rather than re-parsing the human log.

**When to suggest pull unprompted:**
- A `sema_handshake` returns HALT against a handle the user expected to know — the upstream definition may have evolved.
- The user mentions they just upgraded the package (`pip install -U semahash`).
- The user asks how to "update vocabulary", "sync", or "get latest patterns".

**When NOT to pull.** Do not call `sema_pull` as part of routine orientation. It's not a "check in" — it's an update. Pulling removes locally-superseded handles by default, which can drop patterns the user has intentionally pinned. The orient phase is `sema_graph_skeleton()` + `sema_search()` — both read-only. Reserve `sema_pull` for the specific triggers above.

**Supersession cleanup.** When upstream ships a pattern whose `_meta.supersedes` lists a sema_id you have locally, `sema_pull` removes the superseded local pattern by default and adds the replacement. Two guard cases:

- **Orphan guard** — if a *user-only* local pattern still depends on the superseded one (references its exact sema_id), pull keeps the superseded pattern in place and reports the orphan in `superseded_kept_orphan`. Re-point the dependents and re-run to complete the cleanup.
- **Opt-out** — pass `preserve_superseded: true` to keep both old and new handles coexisting. Useful when the user wants to compare, or has reason to pin the old pattern.

**Other guarantees** (no need to over-explain to the user):
- Custom local patterns are NEVER deleted unless upstream explicitly supersedes them (and even then the orphan guard kicks in when dependents exist).
- User-set `_meta.caution` and `_meta.related` survive updates.
- Failures roll back atomically — there's no half-applied state to recover from.
- Each successful pull keeps ONE pre-pull snapshot. If the user says "oh that update broke things," suggest `sema pull --undo` (CLI) to revert.

**Excluding patterns the user doesn't want.** For persistent exclusions, write to `~/.config/sema/excluded` (one handle per line, `#` starts a comment). **Version-pinning recipe:** keep a local copy of a pattern AND add it to the exclusion list. Dependents resolve against the local frozen version while upstream evolves around it.

**Refuses to modify the bundled DB.** The same `sema build` + `sema use` setup required for minting also applies here — pull only operates on writable project DBs.

**Deployment opt-outs.** Environment variables control which mutating tools are exposed by the MCP server. Both are off (i.e., tools exposed) by default:
- `SEMA_DISABLE_PULL=true` — hides `sema_pull` (deployments that want a pinned vocabulary)
- `SEMA_DISABLE_MINT=true` — hides `sema_mint` (read-only deployments)

## Before you can mint

The bundled vocabulary is **read-only** — it gets overwritten on pip upgrades. To mint, you need your own project DB:

1. Run in shell (bash): `sema build /tmp/my-project.db --preset full`
2. Switch to it via MCP: `sema_use(db_path="/tmp/my-project.db")`
3. Now `sema_mint` will work

**Note:** As of 0.2.1, `sema_mint` is exposed by default. If the tool is unavailable, the deployment has explicitly disabled it via `SEMA_DISABLE_MINT=true`; ask the user to re-enable it if they want to mint.

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
  pattern_json: JSON.stringify({
    handle: "PatternName",          // 1–2 syllables, speakable
    mechanism: "How the pattern works",
    gloss: "One-line summary",      // What it IS
    invariants: ["Must...", ...],   // Non-negotiable constraints
    _meta: {
      path: ["Mind", "Reasoning"],
      ring: 1,
      tier: 2,
    },
  })
})
```

## Embedding handles in text

Use sema handles as load-bearing nouns — not footnotes, actual words you think with:

> "This uses `StateLock#5602` to prevent concurrent mutation"

Wrap handles in backticks for readability. When you encounter a handle you don't recognize, resolve it before proceeding.

## Verify at boundaries

When two agents (or an agent and a human) need to agree on meaning:

```javascript
sema_handshake({ ref: "StateLock#5602" })
// → canonical stub. Compare against your local value, then:
sema_handshake({ ref: "StateLock", your_hash: "774b" })
// PROCEED (match) or HALT (drift). No silent misunderstandings.
```

For bulk verification of a specific shared set, use `sema_verify_context`.

### Vocabulary-wide handshake

When two agents need to confirm they have the *same entire vocabulary* — not just one pattern — pass `ref="vocab"`:

```javascript
sema_handshake({ ref: "vocab" })
// → { verdict: "PROVIDE_HASH", canonical_stub: "39ca671a4dcb3075", pattern_count: 452 }

sema_handshake({ ref: "vocab", your_hash: "39ca671a4dcb3075" })
// → PROCEED if byte-identical, HALT if any pattern's hash differs
```

This is equivalent to comparing `sema_root()` outputs but returns a verdict instead of raw numbers. Use it as a cheap drift check before coordinating on anything complex — if vocabs diverge, `sema pull` converges them or `sema_propose_context` can scope agreement to a known-shared subset.

## Think with sema, don't just cite it

Sema patterns are **thinking tools**, not references. When a user asks you to reason about any problem — farming, architecture, career decisions, anything — search sema for patterns that structure the reasoning itself.

For example, if someone asks "how should I start a business?":
1. Search for `strategy`, `risk`, `decision`, `explore exploit`, `decompose`
2. Resolve the top hits — read their mechanisms and invariants
3. Use those patterns to *structure your answer*: "This is a `Strategy#cd1d` problem, not a `Plan#c009` problem, because..."

The patterns aren't labels you slap on afterward. They're lenses that change what you see. `ExploreExploit#d500` doesn't just name a concept — it tells you *when to stop researching and start acting*. `PreMortem#6cc4` doesn't just mean "think about failure" — it has a specific mechanism for surfacing hidden risks.

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
