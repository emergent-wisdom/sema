# Sema Documentation

Welcome to the Sema documentation. Start at the top and read down — each section builds on the previous one.

## Safety

Sema ships no executable code — it's a library of pattern *definitions* (handles, mechanisms, invariants, dependency graphs). The MCP server hands patterns to clients as data; it does not execute the behaviors they describe.

**Intended use: reasoning and reference.** Patterns are thinking tools — named concepts agents can search, resolve, and handshake on to reason about coordination, risk, and procedure. See [`manuals/vocabulary-design.md`](manuals/vocabulary-design.md) for the intent behind each pattern and the design choices.

**Running patterns as executable recipes is untested.** Many patterns describe procedures an agent could step through. That path is still a research phase — the mechanism text has not been validated end-to-end, and we make no claims about safety when a pattern is executed rather than referenced. If you go this route, run the agent's execution step in a sandboxed environment. Patterns with known risks carry a `caution` field in their metadata; absence of that flag means the pattern has not been classified as risky, not that it has been certified safe.

The long-term goal is cryptographically enforced safety constraints on agent-to-agent communication — an active research direction.

## Orientation

- **[Overview](README.md):** You are here.
- **[Getting Started](guides/getting-started.md):** Install Sema, select a vocabulary, and use the core tools.
- **[Core Philosophy](core/philosophy.md):** Why Sema exists — content-addressing, "Text is Code", the Civilization Stack.

## The Pattern Card

- **[Schema Spec](specification/schema.md):** The JSON structure of a Pattern Card — hashed fields, metadata, dependency map.
- **[Naming Taxonomy](specification/naming.md):** Rules for Handles, Layers, Categories, and naming suffixes.

## Lifecycle & Rules

- **[Validation Rules](specification/validation.md):** Rules A-K enforced by the compiler (dependency integrity, signatures, schemas).
- **[Validation Matrix](specification/validation-matrix.md):** All compiler checks with implementation status and code locations.
- **[Versioning & Refinement](specification/versioning.md):** How immutable hashes coexist with mutable handles; refinement and supersession.

## Practical Guides

- **[Pattern Lifecycle](guides/lifecycle.md):** The full loop: create, validate, hash, apply, export, distribute, pull, rebuild.
- **[Pattern Authoring Guide](guides/authoring.md):** Step-by-step workflow for minting and modifying patterns.
- **[Publishing and Installing Vocabulary Libraries](guides/libraries.md):** Build a DeFi-style library, package and verify it, publish GitHub Release assets, and install or update the result.
- **[Reviewing a Pattern Card](guides/review-method.md):** The judgment layer — how to decide whether a card is right, the defect classes that recur in practice, and the tools and theories already tried and abandoned.
- **[CLI Reference](tools/cli.md):** The `sema` command — build, package, install, update, use, list, root, apply, search, resolve, show, pull, and serve.

## Integrations

- **[Understanding Graph](guides/understanding-graph.md):** Composing semantic memory (Sema) with episodic memory (UG).
- MCP server setup for Claude Code, OpenClaw, and other clients is in the [main README](../README.md#install).

## Reference

- **[Vocabulary Information](information/vocabulary_information.md):** Versioned semantic-set and catalog roots plus the current vocabulary's statistical breakdown.

## Getting Started

```bash
# Install
pip install semahash

# Create and select a writable project vocabulary
sema build my-project.db --preset full
sema use ./my-project.db

# Add a pattern (validates before applying)
sema apply --add MyPattern.json

# Validate without applying
sema apply --check --add MyPattern.json

# Search the vocabulary
sema search "coordination"

# Inspect the active vocabulary's aggregate identities
sema root

# Start the MCP server for AI integration
sema mcp
```

## Community

- **[Discord](https://discord.gg/hRhVqAuDYQ)** — Questions, feedback, pattern discussions
- **[GitHub](https://github.com/emergent-wisdom/sema)** — Issues, PRs, full specification
