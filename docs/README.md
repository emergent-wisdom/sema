# Sema Documentation

Welcome to the Sema documentation. Start at the top and read down — each section builds on the previous one.

## Disclaimer

Sema is an experimental research project. The patterns described here represent a set of technical capabilities and should not be interpreted as an endorsement of their execution. Sema has not been tested in, and is not ready for, production environments. We recommend running it in a sandboxed environment.

Some patterns are marked with a `caution` field in their metadata to flag them as potentially risky. The absence of a caution flag does not imply safety — many patterns carry no identifier regarding their safety status. Agents connecting via MCP are informed that referencing a pattern is not authorization to perform the actions it describes.

The long-term goal is cryptographically enforced safety constraints for agent-to-agent communication, but further research is required to achieve this.

## Orientation

- **[Overview](README.md):** You are here.
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
- **[CLI Reference](tools/cli.md):** The `sema` command — build, use, list, init, apply, search, resolve, show, pull, serve.

## Integrations

- **[Understanding Graph](guides/understanding-graph.md):** Composing semantic memory (Sema) with episodic memory (UG).
- MCP server setup for Claude Code, OpenClaw, and other clients is in the [main README](../README.md#install).

## Reference

- **[Vocabulary Information](information/vocabulary_information.md):** Cryptographic Merkle root and statistical breakdown of the current vocabulary.

## Getting Started

```bash
# Install
pip install semahash

# Add a pattern (validates before applying)
sema apply --add MyPattern.json

# Validate without applying
sema apply --check --add MyPattern.json

# Search the vocabulary
sema search "coordination"

# Start the MCP server for AI integration
sema mcp
```

## Community

- **[Discord](https://discord.gg/hRhVqAuDYQ)** — Questions, feedback, pattern discussions
- **[GitHub](https://github.com/emergent-wisdom/sema)** — Issues, PRs, full specification
