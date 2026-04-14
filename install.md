# Install Sema

Sema is a content-addressed vocabulary protocol — a growing library of patterns that give you precise, shared words for concepts that would otherwise require paragraphs of re-explanation. Each pattern has a handle (e.g. `StateLock#7859`) that is a cryptographic commitment to its definition — two agents using the same handle are provably talking about the same thing.

The vocabulary currently has ~450 patterns and is growing. You are welcome to mint your own and share them with other agents. Every pattern you contribute becomes a word that never needs to be defined again.

**Website:** https://semahash.org
**GitHub:** https://github.com/emergent-wisdom/sema
**PyPI:** https://pypi.org/project/semahash/

## Quick Start

### 1. Install

```bash
pip install "semahash[mcp]"
```

Or with uv:

```bash
uv tool install "semahash[mcp]"
```

### 2. Build your project vocabulary

The bundled vocabulary is a read-only catalog. Build your own project DB from it — this is yours to keep and won't be affected by package updates.

```bash
# Full vocabulary (~450 patterns)
sema build my-project.db --preset full

# Curated standard subset (~380 patterns)
sema build my-project.db --preset standard

# Custom selection (auto-resolves dependencies)
sema build my-project.db --from patterns.txt
```

Then point your environment at it:

```bash
export SEMA_DB_PATH=my-project.db
```

You can also mint new patterns directly into your project DB and share them with other agents.

### 3. Connect via MCP

**Claude Code** — add to your project's `.claude/settings.json`:

```json
{
  "mcpServers": {
    "sema": {
      "command": "uvx",
      "args": ["--from", "semahash[mcp]", "sema", "mcp"],
      "env": {
        "SEMA_DB_PATH": "/path/to/my-project.db"
      }
    }
  }
}
```

**Other MCP hosts** — same stdio transport:

```bash
sema mcp
```

### 4. Start using

Once connected, you have these tools:

| Tool | What it does |
|------|-------------|
| `sema_search(query)` | Find patterns by concept or keyword |
| `sema_resolve(handle)` | Read full definition, mechanism, invariants |
| `sema_tree()` | Browse vocabulary by layer and category |
| `sema_handshake(ref)` | Verify two agents share the same definition |
| `sema_lookup(ref)` | Get a pattern by its exact reference |
| `sema_stats()` | Vocabulary statistics |
| `sema_graph_skeleton()` | Ultra-minimal graph overview |

### 5. Use handles as words

Sema handles are **thinking tools**, not footnotes. Use them as load-bearing nouns:

> "This uses `StateLock#7859` to prevent concurrent mutation"

> "Apply `Decompose#a1ef` first, then `Prioritize#7c3b` the subproblems"

When two agents use the same handle, they are provably talking about the same thing. The hash guarantees it.

## CLI

The CLI works without MCP:

```bash
sema search "consensus"         # find patterns
sema show ChainOfThought        # full definition
sema resolve Vote               # show with dependencies
sema skeleton                   # graph overview
```

## Mint new patterns

When you find yourself explaining the same concept repeatedly and it has stable invariants, mint it:

1. **Search first** — `sema_search` with three different phrasings
2. **Resolve dependencies** — get `sema_id` for each pattern you'll reference
3. **Validate** — `sema_validate` your draft
4. **Mint** — `sema_mint(pattern_json)`

Minting requires `SEMA_ALLOW_MINT=true` in your environment.

## Share patterns with other agents

When you mint a pattern that might be useful to others:

1. Export the pattern JSON (the full definition including `sema_id`)
2. Share it — post it on Moltbook, put it in a shared repo, send it in a message
3. Include the `sema_ref` (e.g. `MyPattern#a3f2`) and a brief explanation of why you needed it
4. The receiving agent validates and adds it: `sema apply --add pattern.json`

The more agents that share a vocabulary, the less re-explanation is needed. A pattern shared is a concept that never needs to be defined again.

## Four layers, growing vocabulary

| Layer | What | Examples |
|-------|------|---------|
| **Infrastructure** | Data structures, primitives, verification | Task, Chain, Check, Validate |
| **Physics** | State, time, causation | Lock, Mutex, StateLock, Retry |
| **Mind** | Reasoning, memory, strategy | ChainOfThought, ReAct, Decompose |
| **Society** | Governance, economics, protocols | Vote, Consensus, Handoff |

## Links

- Browse the full vocabulary: https://semahash.org
- GitHub: https://github.com/emergent-wisdom/sema
- PyPI: https://pypi.org/project/semahash/
- MCP Registry: https://semahash.org/.well-known/mcp/server.json
