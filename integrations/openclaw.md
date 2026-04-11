# Sema + OpenClaw Integration

Use Sema patterns as semantic contracts in your OpenClaw agents.

## Setup

### Fastest: zero-install via uvx

If you have [uv](https://docs.astral.sh/uv/) installed, let `uvx` manage an
isolated environment and skip the pip step:

```bash
npm install -g mcporter
mcporter config add sema \
  --command uvx \
  --arg --from --arg semahash --arg sema --arg mcp \
  --scope home \
  --description "Sema: Content-addressed semantics for multi-agent coordination"
```

### Alternative: pip install

```bash
pip install "semahash[mcp]"
npm install -g mcporter
mcporter config add sema --command sema --arg mcp --scope home \
  --description "Sema: Content-addressed semantics for multi-agent coordination"
```

Or install from source for development:

```bash
pip install "semahash[mcp] @ git+https://github.com/emergent-wisdom/sema.git"
```

### Verify

```bash
mcporter list sema --schema     # should show 11 tools
mcporter call sema.sema_stats   # vocabulary stats
```

## Usage

Any OpenClaw agent with the `mcporter` skill can now call Sema tools:

```
mcporter call sema.sema_search query="coordination"
mcporter call sema.sema_handshake ref="StateLock#f165"
mcporter call sema.sema_resolve handle="ChainOfThought"
```

## Agent Configuration

Add Sema instructions to your agent's `AGENTS.md` or `SOUL.md`:

```markdown
## Semantic Coordination Protocol

Before coordinating with other agents on a shared concept, verify alignment:

1. Search for the relevant pattern: `mcporter call sema.sema_search query="..."`
2. Handshake to verify you share the same definition:
   `mcporter call sema.sema_handshake ref="PatternName#stub"`
3. Only proceed if verdict is `PROCEED`. On `HALT`, stop and report the mismatch.

Key patterns for this workspace:
- `StateLock#f165` — mutex for shared state
- `Check#1544` — non-blocking truth evaluation
- `PUREBrainstorming#9191` — structured ideation (Filter -> Refine -> Specify)
```

## Multi-Agent Example

Set up two OpenClaw agents that coordinate via Sema:

```bash
# Create two agents with separate workspaces
openclaw agents add architect --workspace ~/.openclaw/agents/architect/workspace --non-interactive --accept-risk
openclaw agents add engineer --workspace ~/.openclaw/agents/engineer/workspace --non-interactive --accept-risk
```

In `architect`'s AGENTS.md, add:
```markdown
Before delegating a design task, handshake on MechanisticDesignProposal#8cf7
to ensure the engineer shares your contract for what a valid proposal looks like.
```

In `engineer`'s AGENTS.md, add:
```markdown
When receiving a design task, verify the contract:
mcporter call sema.sema_handshake ref="MechanisticDesignProposal#8cf7"
Only begin work if verdict is PROCEED.
```

## Also works with

- **Claude Code**: See [claude-code.md](claude-code.md)
- **Any MCP client**: Sema exposes a standard MCP stdio server (`sema mcp`)
- **Direct Python**: `from sema.core.actions import sema_handshake`
