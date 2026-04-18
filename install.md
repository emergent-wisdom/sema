---
name: sema
description: Content-addressed vocabulary protocol for AI agents
homepage: https://semahash.org
github: https://github.com/emergent-wisdom/sema
---

# Install Sema

Sema is a growing vocabulary of cognitive patterns with cryptographic identity. Each pattern has a handle (e.g. `StateLock#5602`) that is a hash of its definition — two agents using the same handle are provably talking about the same thing.

Referencing a pattern is not authorization to perform the actions it describes. Patterns are definitions, not permissions.

## MCP Server (recommended)

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

## Verify it works

Ask your agent:

> Search sema for coordination patterns

You should see results like `Consensus#376f`, `Vote#37f8`, `StateLock#5602`.

## Tools available

| Tool | What it does |
|------|-------------|
| `sema_search(query)` | Find patterns by concept |
| `sema_resolve(handle)` | Full definition with dependencies |
| `sema_tree()` | Browse by layer and category |
| `sema_handshake(ref)` | Verify two agents share the same definition |
| `sema_lookup(ref)` | Get pattern by exact reference |
| `sema_use(db_path)` | Switch active vocabulary database |
| `sema_stats()` | Vocabulary statistics |
| `sema_mint(pattern_json)` | Create a new pattern (requires SEMA_ALLOW_MINT=true) |

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
echo "ChainOfThought\nVote\nConsensus" > patterns.txt
sema build my-project.db --from patterns.txt
```

Dependencies are resolved automatically.

## CLI

```bash
pip install semahash
sema search "consensus"
sema show StateLock
sema resolve Vote
sema build my.db --preset standard
sema use my.db
sema list
```

## Links

- Website: https://semahash.org
- GitHub: https://github.com/emergent-wisdom/sema
- Discord: https://discord.gg/hRhVqAuDYQ
- PyPI: https://pypi.org/project/semahash/
