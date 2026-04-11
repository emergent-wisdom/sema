<!-- mcp-name: io.github.emergent-wisdom/semahash -->
<!-- deploy-trigger: 2026-04-11 -->

<p align="center">
  <img src="https://raw.githubusercontent.com/emergent-wisdom/sema/main/docs/images/sema_banner.png" alt="Sema — When the hash is the word" width="800">
</p>

# Sema: When the Hash Is the Word

**Content-addressed semantics for multi-agent coordination.**

[![PyPI](https://img.shields.io/pypi/v/semahash.svg)](https://pypi.org/project/semahash/)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-blue)](https://registry.modelcontextprotocol.io/servers/io.github.emergent-wisdom/semahash)
[![Paper](https://img.shields.io/badge/Paper-PDF-red)](https://github.com/emergent-wisdom/sema/blob/main/paper/sema.pdf)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19462703.svg)](https://doi.org/10.5281/zenodo.19462703)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-green)](https://github.com/emergent-wisdom/sema/blob/main/LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC%20BY%204.0-lightgrey)](https://github.com/emergent-wisdom/sema/blob/main/LICENSE-CONTENT)

Sema is a semantic commons that content-addresses meaning itself: the definition *is* the identifier. By deriving identifiers from the cryptographic hash of a pattern's definition, any divergence in meaning produces a distinct hash, guaranteeing that misaligned agents halt rather than fail silently.

**Web:** [semahash.org](https://semahash.org)

## Install

### MCP Server (recommended)

Add to any MCP client (Claude Code, Cursor, VS Code, Windsurf, Claude Desktop):

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

This uses [uv](https://docs.astral.sh/uv/) to download, install, and run sema
in an isolated environment on first invocation, then caches it for subsequent
calls.

### Permanent install (pip)

```bash
pip install "semahash[mcp]"
```

For CLI-only use (no MCP server):

```bash
pip install semahash
```

## Quick Start

### Use with AI Agents (MCP)

Already covered above via the JSON config or `pip install` path. For development against this repo:

```bash
git clone https://github.com/emergent-wisdom/sema.git
pip install -e "./sema[mcp]"
```

Your agent now has access to `sema_search`, `sema_lookup`, `sema_handshake`, and 8 more tools. Any MCP-compatible client works — Sema exposes a standard stdio server.

**Verify it works** — ask your agent: *"Search sema for coordination patterns and handshake on StateLock"*

Full integration guides: [Claude Code](integrations/claude-code.md) | [OpenClaw](integrations/openclaw.md)

### Use via CLI

```bash
# Search the vocabulary
sema search "coordination"

# Look up a specific pattern
sema resolve StateLock

# Print a pattern's full definition
sema show StateLock

# Browse the graph structure
sema skeleton

# Start local API + web frontend (binds to 127.0.0.1 by default)
sema serve
```

### Bring Your Own Vocabulary

Build a private registry from scratch — no PR or maintainer in the loop:

```bash
sema init ./mylib.db
export SEMA_DB_PATH=$(pwd)/mylib.db
sema apply --add path/to/MyPattern.json
sema search "..."
```

Subsequent `sema` commands (including `sema mcp`) read from your private
registry. See [CONTRIBUTING.md](CONTRIBUTING.md) for the canonical
contribution path and [docs/specification/versioning.md](docs/specification/versioning.md) for the
refinement and supersession policy.

### Use in Python

```python
from sema.core.actions import sema_handshake
import json

# Look up the canonical hash
result = json.loads(sema_handshake("StateLock"))
print(result["canonical_stub"])  # b91b

# Verify alignment
result = json.loads(sema_handshake("StateLock#b91b"))
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
Agent A: "Let's use StateLock#b91b"
Agent B: sema_handshake("StateLock#b91b")
         -> PROCEED (hashes match) or HALT (drift detected)
```

This is the **Anti-Postel principle**: same bytes = PROCEED, different bytes = HALT. No ambiguity, no silent failures.

## The Vocabulary

453 patterns across 13 categories and 4 layers:

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
| `sema_lookup` | Get a pattern by its reference (e.g., `StateLock#b91b`) |
| `sema_resolve` | Get a pattern with dependencies expanded |
| `sema_handshake` | Fail-closed semantic verification between agents |
| `sema_mint` | Create a new pattern (validate, hash, add to vocabulary) |
| `sema_propose_context` | Compute a context digest for a multi-agent definition set (drift detection) |
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

## Using with understanding-graph

Sema gives your agents shared *semantic* memory — a vocabulary of cognitive patterns with content-addressed identity. [Understanding Graph](https://github.com/emergent-wisdom/understanding-graph) gives them shared *episodic* memory — the actual thinking trail behind a decision. They compose:

```bash
claude mcp add sema -- uvx --from "semahash[mcp]" sema mcp
claude mcp add ug   -- npx -y understanding-graph mcp
```

With both installed, an agent can:

1. Anchor an understanding-graph decision node in a sema pattern hash (e.g. `StateLock#b91b`) so the meaning of the primitive can never drift.
2. Use `graph_semantic_search` to find all past graph nodes that reference a given sema pattern — hash-stable history, not keyword matching.
3. Call `sema_handshake` *before* writing a decision that depends on a shared concept; if it returns `HALT`, the agent writes a `tension` node instead and stops, preventing silent divergence.

Full walkthrough: [docs/guides/understanding-graph.md](docs/guides/understanding-graph.md)

## Repository Structure

```
sema/
├── src/sema/              Core library (hashing, validation, MCP server, API)
├── data/                  Vocabulary (453 pattern cards + taxonomy database)
├── docs/                  Documentation (philosophy, schema spec, CLI reference)
├── paper/                 Academic paper (sema.tex)
├── web/                   Web frontend (React + Three.js graph visualization)
├── experiments/
│   ├── orchestrator/      Multi-agent engine (bundled for experiment reproduction)
│   ├── sema_design_challenge/  Main experiment (3 conditions, 5 runs, full traces)
│   └── demos/             Standalone demos (local handshake, Babel Test)
├── integrations/          Integration guides (Claude Code, OpenClaw, any MCP client)
└── pyproject.toml         Package config (extras: [mcp], [api], [full])
```

## Contributing

Want to add patterns, improve existing ones, or host the frontend locally? See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citing

```bibtex
@misc{westerberg2026sema,
  title        = {Sema: When the Hash Is the Word},
  author       = {Westerberg, Henrik},
  year         = {2026},
  month        = apr,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.19462703},
  url          = {https://doi.org/10.5281/zenodo.19462703}
}
```

See [`CITATION.cff`](CITATION.cff) for the machine-readable version (GitHub
renders a "Cite this repository" button from it).

## License

Sema is dual-licensed:

- **Code** (everything in `src/`, `web/`, `experiments/`, `scripts/`, and the
  package config) — [MIT](LICENSE). Self-host it, fork it, build commercial
  products on top of it.
- **Content** (the pattern vocabulary in `data/`, the documentation in `docs/`,
  the academic paper in `paper/`, and the prose displayed on
  [semahash.org](https://semahash.org)) —
  [CC BY 4.0](LICENSE-CONTENT). Reuse the patterns and prose anywhere, for any
  purpose including commercial, as long as you attribute Henrik Westerberg.

For academic citation, see [`CITATION.cff`](CITATION.cff). GitHub renders this
as a "Cite this repository" button on the project page that generates APA and
BibTeX automatically.
