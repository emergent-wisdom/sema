# Sema: Content-Addressed Semantics for Multi-Agent Coordination

**Hash the meaning, get the word.**

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/sema.pdf)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Sema is a semantic commons that content-addresses meaning itself: the definition *is* the identifier. By deriving identifiers from the cryptographic hash of a pattern's definition, any divergence in meaning produces a distinct hash, guaranteeing that misaligned agents halt rather than fail silently.

**Web:** [semahash.org](https://semahash.org)

## Install

```bash
pip install git+https://github.com/emergent-wisdom/sema.git
```

For MCP server support (recommended for AI agents):

```bash
pip install "semahash[mcp] @ git+https://github.com/emergent-wisdom/sema.git"
```

> **PyPI release coming soon.** Once published, install will simplify to `pip install semahash`.

## Quick Start

### Use with AI Agents (MCP)

Add Sema to **Claude Code** in one command:

```bash
claude mcp add sema -- sema mcp
```

Add Sema to **OpenClaw** via mcporter:

```bash
npm install -g mcporter
mcporter config add sema --command sema --arg mcp --scope home
```

Or clone and install locally:

```bash
git clone https://github.com/emergent-wisdom/sema.git
pip install -e "./sema[mcp]"
claude mcp add sema -- sema mcp
```

Your agent now has access to `sema_search`, `sema_lookup`, `sema_handshake`, and 5 more tools. Any MCP-compatible framework works — Sema exposes a standard stdio server.

**Verify it works** — ask your agent: *"Search sema for coordination patterns and handshake on StateLock"*

Full integration guides: [Claude Code](integrations/claude-code.md) | [OpenClaw](integrations/openclaw.md)

### Use via CLI

```bash
# Search the vocabulary
sema search "coordination"

# Look up a specific pattern
sema resolve StateLock

# Browse the graph structure
sema skeleton

# Start local API + web frontend
sema serve
```

### Use in Python

```python
from sema.core.actions import sema_handshake
import json

# Look up the canonical hash
result = json.loads(sema_handshake("StateLock"))
print(result["canonical_ref"])  # StateLock#a375

# Verify alignment
result = json.loads(sema_handshake("StateLock#a375"))
print(result["verdict"])  # PROCEED
```

### Try the Protocol (No API Keys Needed)

```bash
python experiments/demos/local_handshake.py
```

See the handshake in action: matching hashes PROCEED, mismatched hashes HALT, unknown patterns HALT. Takes 2 seconds.

## How It Works

```
word = hash(canonical(definition))
```

Take any concept (a coordination protocol, a reasoning pattern, a trust mechanism), express it in canonical form, hash it. That hash IS the word. Change one byte in the definition, get a different word.

```
Agent A: "Let's use StateLock#a375"
Agent B: sema_handshake("StateLock#a375")
         -> PROCEED (hashes match) or HALT (drift detected)
```

This is the **Anti-Postel principle**: same bytes = PROCEED, different bytes = HALT. No ambiguity, no silent failures.

## The Vocabulary

450 patterns across 13 categories and 4 layers:

- **Physics** — Immutable substrate (locks, entropy, causality)
- **Mind** — Hybrid cognition (reasoning, inference, strategy)
- **Society** — Multi-agent coordination (economics, governance, protocols)
- **Infrastructure** — Operational constraints (data structures, verification)

Each pattern is an executable specification containing machine-verifiable contracts, invariants, failure modes, and typed dependencies.

## MCP Tools

When running as an MCP server (`sema mcp`), these tools are available:

| Tool | Description |
|------|-------------|
| `sema_search` | Search patterns by name, description, or meaning |
| `sema_lookup` | Get a pattern by its reference (e.g., `StateLock#a375`) |
| `sema_resolve` | Get a pattern with dependencies expanded |
| `sema_handshake` | Fail-closed semantic verification between agents |
| `sema_mint` | Create a new pattern (validate, hash, add to vocabulary) |
| `sema_propose_context` | Generate a Merkle root for a multi-agent context set |
| `sema_verify_context` | Verify a context proposal from another agent |
| `sema_tree` | Browse vocabulary by layer and category |
| `sema_validate` | Validate a pattern JSON for correctness |
| `sema_stats` | Vocabulary statistics |
| `sema_graph_skeleton` | Ultra-minimal graph overview (~150 tokens) |

## Web Frontend

```bash
pip install "semahash[api]"
sema serve
# Open http://localhost:3000
```

Interactive 3D graph visualization, pattern browser, and search. Built with React + Three.js.

## Experiments

The `experiments/` directory contains a controlled multi-agent design challenge comparing three conditions:

| Condition | Sema | Turns | Outcome |
|-----------|------|-------|---------|
| A: Natural language only | No | 4 | Design rejected |
| B: Sema vocabulary | Yes | 11 | SAD Engine approved |
| C: Sema + protocol | Yes | 25 | SAD Engine with exhaustive vetting |

Agents with Sema patterns produced physics-grounded designs that survived adversarial scrutiny. Agents without Sema produced shallow designs that failed safety review.

To reproduce:

```bash
cd experiments/sema_design_challenge
export GOOGLE_API_KEY=your_key
./reproduce.sh
```

See [`experiments/sema_design_challenge/README.md`](experiments/sema_design_challenge/README.md) for details.

## Key Properties

- **Zero semantic collisions** across the full vocabulary
- **16.9x average token compression** via content-addressed stubs
- **Fail-closed architecture** — mismatches halt, never fail silently
- **Mean embedding similarity of 0.21** — high structural distinctness

## Repository Structure

```
sema/
├── src/sema/              Core library (hashing, validation, MCP server, API)
├── data/                  Vocabulary (450 pattern cards + taxonomy database)
├── docs/                  Documentation (philosophy, schema spec, CLI reference)
├── paper/                 Academic paper (sema.tex)
├── web/                   Web frontend (React + Three.js graph visualization)
├── experiments/
│   ├── emergent-swarm/    Multi-agent engine (bundled for experiment reproduction)
│   ├── sema_design_challenge/  Main experiment (3 conditions, 5 runs, full traces)
│   └── demos/             Standalone demos (local handshake, Babel Test)
├── integrations/          Integration guides (Claude Code, OpenClaw, any MCP client)
└── pyproject.toml         Package config (extras: [mcp], [api], [full])
```

## Contributing

Want to add patterns, improve existing ones, or host the frontend locally? See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citing

```bibtex
@unpublished{westerberg2026sema,
  title={Sema: Content-Addressing Meaning for Safe Multi-Agent Coordination},
  author={Westerberg, Henrik},
  year={2026},
  note={Preprint}
}
```

## License

MIT
