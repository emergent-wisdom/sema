# Getting Started

Sema is a growing vocabulary of cognitive patterns with cryptographic identity. Each pattern has a handle (e.g. `StateLock#c9c2`) that is a hash of its definition — two agents using the same handle are provably talking about the same thing.

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

You should see results like `Consensus#b9a5`, `Vote#8493`, `StateLock#c9c2`.

## Use handles as words

Sema handles are thinking tools, not footnotes:

> "This uses `StateLock#c9c2` to prevent concurrent mutation"

> "Apply `Decompose#6994` first, then `Prioritize#99f0` the subproblems"

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

## Install a published vocabulary

Published libraries use a manifest-driven flow for installing a named,
read-only vocabulary snapshot:

```bash
sema install https://github.com/emergent-wisdom/sema/releases/latest/download/library.json
sema use bootstrap
sema list
sema root
```

Installing a library does not merge it with the bundled vocabulary or another
library. The bundled vocabulary remains the default, and `sema use --default`
returns to it. The [remote vocabulary library guide](libraries.md) specifies
how to author and package a library, publish both files as GitHub Release
assets, and install it. The install target is the Release asset URL for
`library.json`, not the repository URL or a branch.

## CLI

```bash
sema search "consensus"
sema show StateLock
sema resolve Vote
sema build my.db --preset standard
sema use my.db
sema list
sema root
```

## Keep the selected vocabulary updated

There are two deliberately different update operations.

For a **writable project database**, `pull` reconciles patterns from another
database—by default, the bundled database installed with the package—while
preserving user-only patterns:

```bash
pip install -U semahash
sema pull             # bundled DB -> active writable project DB
sema pull --dry-run   # preview without writing
```

`pull` is non-destructive — your custom patterns are preserved, your local
`_meta.caution` and `_meta.related` annotations survive, and the whole
operation is atomic (rolls back on failure). See
[CLI reference](../tools/cli.md#pull---sync-vocabulary-from-upstream) for
the exclusion list and version-pinning options.

For an **installed read-only library**, use its recorded remote update pointer:

```bash
sema update bootstrap
```

`update` downloads and verifies a complete replacement release. It does not
merge that release with the bundled vocabulary or another library. See the
[library publishing and installation guide](libraries.md) for the full
distinction.

## Tools available via MCP

| Tool | What it does |
|------|-------------|
| `sema_search(query)` | Find patterns by concept |
| `sema_resolve(handle)` | Full definition with dependencies |
| `sema_tree()` | Browse the taxonomy tree |
| `sema_handshake(ref, your_hash, strict, your_scheme)` | Detect drift by prefix; aggregate roots also require their scheme, and `strict=true` requires full-hash identity |
| `sema_lookup(ref)` | Get pattern by exact reference |
| `sema_root()` | Semantic-set and handle-binding fingerprints for the DB |
| `sema_graph_skeleton()` | High-level layout of patterns + relationships |
| `sema_use(db_path)` | Switch active vocabulary database |
| `sema_stats()` | Vocabulary statistics |
| `sema_mint(pattern_json)` | Create a new pattern (hide with `SEMA_DISABLE_MINT=true`) |
| `sema_pull()` | Sync the active DB with upstream; returns structured stats (hide with `SEMA_DISABLE_PULL=true`) |

## Next

- [Core Philosophy](../core/philosophy.md) — why Sema exists
- [The Pattern Card](../specification/schema.md) — how patterns are structured
- [CLI Reference](../tools/cli.md) — full command reference
