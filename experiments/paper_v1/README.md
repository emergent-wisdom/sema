# Paper v1 Experiment Artifacts

This directory contains the vocabulary database used for the experiments
reported in the paper "Sema: When the Hash Is the Word."

## Files

- `taxonomy_v1.db` — The 450-pattern vocabulary (SQLite) against which
  all experiments in Section 6 were run: hash stability, semantic
  embedding analysis, token compression, Babel test, and multi-agent
  demonstration.

## Why a separate DB?

The main vocabulary (`data/taxonomy.db`) was subsequently improved:
- 78 layer violations fixed (Infrastructure→Mind dependencies corrected)
- 3 patterns added (ToolDiscovery, TaskLifecycle, AuditTrail)
- 1 pattern removed (FractalContext, merged into HolographicShard)
- Parameter descriptions and ranges improved
- Category assignments reviewed (Bid remains Society/Economics)

These changes cascade through the Merkle DAG, changing 75% of pattern
hashes. The experiment results in the paper correspond to the v1 hashes
in this DB, not the current vocabulary.

To reproduce paper experiments, use this DB:
```bash
sema serve --db experiments/paper_v1/taxonomy_v1.db
```
