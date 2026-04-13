# Sema Documentation

Welcome to the Sema documentation. Start at the top and read down — each section builds on the previous one.

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
- **[CLI Reference](tools/cli.md):** The `sema` command — apply, search, resolve, show, pull, serve.

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
