# Getting Started

Sema is a growing vocabulary of cognitive patterns with cryptographic identity. Each pattern has a handle (e.g. `StateLock#7859`) that is a hash of its definition — two agents using the same handle are provably talking about the same thing.

## Install

### MCP Server (recommended)

Add to your MCP client (Claude Code, Cursor, VS Code, Claude Desktop):

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

## Verify it works

Ask your agent:

> Search sema for coordination patterns

You should see results like `Consensus#b862`, `Vote#05a7`, `StateLock#b91b`.

## Use handles as words

Sema handles are thinking tools, not footnotes:

> "This uses `StateLock#7859` to prevent concurrent mutation"

> "Apply `Decompose#a1ef` first, then `Prioritize#7c3b` the subproblems"

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

## Tools available via MCP

| Tool | What it does |
|------|-------------|
| `sema_search(query)` | Find patterns by concept |
| `sema_resolve(handle)` | Full definition with dependencies |
| `sema_tree()` | Browse by layer and category |
| `sema_handshake(ref)` | Verify two agents share the same definition |
| `sema_lookup(ref)` | Get pattern by exact reference |
| `sema_use(db_path)` | Switch active vocabulary database |
| `sema_stats()` | Vocabulary statistics |
| `sema_mint(pattern_json)` | Create a new pattern (requires `SEMA_ALLOW_MINT=true`) |

## Next

- [Core Philosophy](../core/philosophy.md) — why Sema exists
- [The Pattern Card](../specification/schema.md) — how patterns are structured
- [CLI Reference](../tools/cli.md) — full command reference
