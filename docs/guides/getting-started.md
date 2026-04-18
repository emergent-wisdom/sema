# Getting Started

Sema is a growing vocabulary of cognitive patterns with cryptographic identity. Each pattern has a handle (e.g. `StateLock#5602`) that is a hash of its definition — two agents using the same handle are provably talking about the same thing.

## Install

### Claude Code plugin (easiest)

```bash
claude plugin marketplace add emergent-wisdom/marketplace
claude plugin install sema@emergent-wisdom
```

This installs the MCP server plus the `sema-usage` skill that teaches the agent the search/resolve/mint/handshake workflow.

### MCP Server (any client)

Add to your MCP client config (Claude Code, Cursor, VS Code, Claude Desktop):

```json
{
  "mcpServers": {
    "sema": {
      "command": "uvx",
      "args": ["--from", "semahash[mcp]", "sema", "mcp"]
    }
  }
}
```

Or via Claude Code CLI:

```bash
claude mcp add sema -- uvx --from "semahash[mcp]" sema mcp
```

### Via pip

```bash
pip install "semahash[mcp]"
```

### Disabling minting (optional)

`sema_mint` is exposed by default. Deployments that want a read-only server (no pattern creation from MCP clients) can hide the tool with:

```bash
SEMA_DISABLE_MINT=true claude
```

A matching `SEMA_DISABLE_PULL=true` hides `sema_pull` for pinned-vocabulary deployments.

## Verify it works

Ask your agent:

> Search sema for coordination patterns

You should see results like `Consensus#376f`, `Vote#37f8`, `StateLock#5602`.

## Use handles as words

Sema handles are thinking tools, not footnotes:

> "This uses `StateLock#5602` to prevent concurrent mutation"

> "Apply `Decompose#dcf9` first, then `Prioritize#274c` the subproblems"

## Create your own vocabulary

The bundled vocabulary is read-only. To mint your own patterns:

```bash
sema build my-project.db --preset full
sema use my-project.db
```

Then `sema_mint` works. Your project DB survives package upgrades.

Presets: `full` (all default patterns), `standard` (curated subset), `empty` (blank).

Or pick specific patterns:

```bash
printf "ChainOfThought\nVote\nConsensus\n" > patterns.txt
sema build my-project.db --from patterns.txt
```

Dependencies are resolved automatically.

## CLI

```bash
sema search "consensus"
sema show StateLock
sema resolve Vote
sema build my.db --preset standard
sema use my.db
sema list
```

## Stay updated

After upgrading the package (`pip install -U semahash`) or whenever a new
vocabulary release ships, sync your active DB:

```bash
sema pull             # apply upstream changes to your active DB
sema pull --dry-run   # preview without writing
```

`pull` is non-destructive — your custom patterns are preserved, your local
`_meta.caution` and `_meta.related` annotations survive, and the whole
operation is atomic (rolls back on failure). See
[CLI reference](../tools/cli.md#pull---sync-vocabulary-from-upstream) for
the exclusion list and version-pinning options.

## Tools available via MCP

| Tool | What it does |
|------|-------------|
| `sema_search(query)` | Find patterns by concept |
| `sema_resolve(handle)` | Full definition with dependencies |
| `sema_tree()` | Browse the taxonomy tree |
| `sema_handshake(ref)` | Verify two agents share the same definition |
| `sema_lookup(ref)` | Get pattern by exact reference |
| `sema_root()` | Vocabulary fingerprint — one hash for the whole DB |
| `sema_graph_skeleton()` | High-level layout of patterns + relationships |
| `sema_use(db_path)` | Switch active vocabulary database |
| `sema_stats()` | Vocabulary statistics |
| `sema_mint(pattern_json)` | Create a new pattern (hide with `SEMA_DISABLE_MINT=true`) |
| `sema_pull()` | Sync the active DB with upstream; returns structured stats (hide with `SEMA_DISABLE_PULL=true`) |

## Next

- [Core Philosophy](../core/philosophy.md) — why Sema exists
- [The Pattern Card](../specification/schema.md) — how patterns are structured
- [CLI Reference](../tools/cli.md) — full command reference
