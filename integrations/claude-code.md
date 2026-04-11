# Sema + Claude Code Integration

Use Sema patterns as semantic contracts in your Claude Code projects.

## Setup

### Fastest: zero-install via uvx

If you have [uv](https://docs.astral.sh/uv/) installed, you can skip the pip
step entirely and let uvx manage an isolated environment for you:

```bash
claude mcp add sema -- uvx --from "semahash[mcp]" sema mcp
```

`uvx` downloads, caches, and runs `semahash` on first invocation; subsequent
calls reuse the cache. No global install pollution, no virtualenv juggling.

### Alternative: pip install

```bash
pip install "semahash[mcp]"
claude mcp add sema -- sema mcp
```

Or install from source for development:

```bash
pip install "semahash[mcp] @ git+https://github.com/emergent-wisdom/sema.git"
claude mcp add sema -- sema mcp
```

### Verify

Ask Claude Code:

```
Search sema for "coordination" patterns
```

It should call `sema_search` and return matching patterns.

## Usage

Once added, Claude Code can call any of the 11 Sema tools:

```
sema_search query="coordination"
sema_handshake ref="StateLock#b91b"
sema_resolve handle="ChainOfThought"
sema_lookup ref="Abduction#fe2b"
sema_tree layer="Society"
sema_validate pattern_json='{"handle": "MyPattern", ...}'
sema_stats
sema_graph_skeleton
sema_mint pattern_json='{"handle": "NewIdea", ...}'
sema_propose_context handles='["StateLock", "Check"]'
sema_verify_context handles='["StateLock", "Check"]' remote_hash="..."
```

## Project Configuration

Add Sema instructions to your project's `CLAUDE.md` to make coordination automatic:

```markdown
## Semantic Coordination Protocol

This project uses Sema for semantic alignment between agents.

Before coordinating with other agents on a shared concept, verify alignment:

1. Search for the relevant pattern: use `sema_search`
2. Handshake to verify you share the same definition:
   use `sema_handshake` with the pattern's ref (e.g., "StateLock#b91b")
3. Only proceed if verdict is `PROCEED`. On `HALT`, stop and report the mismatch.

Key patterns for this project:
- `StateLock#b91b` — mutex for shared state
- `Check#1544` — non-blocking truth evaluation
- `MechanisticDesignProposal#8cf7` — structured design contract
```

## Multi-Agent Example

Two Claude Code instances coordinating on a design task:

**Agent 1 (Architect)** — CLAUDE.md:
```markdown
Before delegating a design task, handshake on MechanisticDesignProposal#8cf7
to ensure the other agent shares your contract for what a valid proposal looks like.
```

**Agent 2 (Engineer)** — CLAUDE.md:
```markdown
When receiving a design task, verify the contract:
Use sema_handshake with ref="MechanisticDesignProposal#8cf7"
Only begin work if verdict is PROCEED.
```

The handshake guarantees both agents are working from the exact same definition. If either side has drifted, the hash won't match and coordination halts before silent failures compound.

## Quick Demo

Run the local handshake demo to see the protocol in action (no API keys needed):

```bash
python experiments/demos/local_handshake.py
```

## Also works with

- **OpenClaw**: See [openclaw.md](openclaw.md)
- **Any MCP client**: Sema exposes a standard MCP stdio server (`sema mcp`)
- **Direct Python**: `from sema.core.actions import sema_handshake`
