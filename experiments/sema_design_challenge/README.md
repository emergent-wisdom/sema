# Sema Design Challenge

A controlled experiment comparing three conditions for multi-agent coordination on a design task (Pump-and-Dump Detection Engine for DeFi).

## Experiment Design

| Condition | Config | Sema | Description |
|-----------|--------|------|-------------|
| A | `natural_language.yaml` | No | Agents coordinate using natural language only |
| B | `design_challenge.yaml` | Yes | Agents use Sema patterns (`PUREBrainstorming#55d8`, `PURECheck#0b12`, `MechanisticDesignProposal#ad31`) |
| C | `optimistic.yaml` | Yes | Agents use Sema patterns with optimistic coordination protocol |

All three conditions use the same team structure (Alice/Orchestrator, Bob/Designer, Charlie/Safety Engineer), same task, same model (Gemini 3.0 Flash Preview). Only the coordination mechanism varies.

## Results (N=5 runs, latest run)

| Condition | Avg Turns | Duration | Sema Tool Calls | Outcome |
|-----------|-----------|----------|-----------------|---------|
| A (Baseline) | 4 | 142s | 0 | Design **rejected** by safety review |
| B (Sema) | 11 | 213s | 16 (search + lookup) | SAD Engine **approved** |
| C (Sema + Protocol) | 25 | 310s | 19 (handshake + lookup) | SAD Engine **approved** with constraints |

### Key Findings

- **Without Sema (A):** Agents produced a shallow "Triple-Sieve Algorithm" in 4 turns. Charlie (Safety Engineer) rejected it for missing contract-level analysis and latency risks.
- **With Sema vocabulary (B):** Agents used `PUREBrainstorming#55d8` to structure exploration and `PURECheck#0b12` as quality gates. After 4 iterations of adversarial vetting, they converged on the **SAD (Slippage-Adjusted Depletion) Engine** — a physics-grounded design anchored in AMM invariants.
- **With Sema + protocol (C):** Same final design, but arrived through more extensive vetting (8+ iterations). Added ecosystem-level risk analysis, information hazard mitigation, and deployment constraints that B missed.

Sema patterns functioned as **variance reduction**: B and C consistently produced rigorous, physics-grounded designs while A was unstable (occasionally fast but prone to catastrophic coordination loops in other runs).

These results are discussed in Section 6 of the [Sema paper](../../paper/sema.pdf).

## Reproducing

### Prerequisites

1. **Google API key** (experiments use Gemini):
   ```bash
   export GOOGLE_API_KEY=your_key_here
   ```

2. **Sema** installed with MCP support:
   ```bash
   pip install "semahash[mcp]"
   ```

3. **emergent-swarm** is bundled at `../emergent-swarm/` (no separate install needed)

### Run

```bash
./reproduce.sh
```

This runs all three conditions in parallel. Results are saved to `traces/run_<timestamp>/`.

Override the model with:
```bash
MODEL=gemini-3.1-flash-lite-preview ./reproduce.sh
```

## Pre-recorded Traces

The `traces/` directory contains 5 archived runs from the original experiments (December 2025). Each run directory has per-condition subdirectories containing:

- `summary.json` — run metadata (turns, duration, status)
- `swarm.jsonl` — full event trace (messages, tool calls, thoughts, submissions)

## Architecture

Agents communicate exclusively via `send_message` tool calls (Actor Model with mailbox-based message passing). All other text is internal monologue, invisible to teammates. The Sema MCP server runs as a subprocess, providing vocabulary tools to Condition B and C agents.
