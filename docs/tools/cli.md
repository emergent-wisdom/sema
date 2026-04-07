# Sema CLI

The **Sema CLI** (`sema`) is the primary tool for managing the vocabulary. It ensures database integrity, strict validation, and atomic operations.

## Installation

```bash
pip install -e .
```

## Features

*   **Strict Validation:** Enforces "Truth in Advertising" (dependencies must be used in text), Schema rules, and Taxonomy constraints.
*   **Atomic Operations:** Validates everything before making any changes.
*   **Dependency Checking:** Prevents removing patterns that are still in use.

## Commands

### apply - Atomic Add/Remove

The `apply` command performs atomic add and remove operations. All changes are validated before execution.

```bash
# Add a pattern
sema apply --add <path_to_json>

# Add multiple patterns (or a directory)
sema apply --add patterns/

# Remove a pattern
sema apply --remove <Handle>

# Atomic add + remove (e.g., replacing a pattern)
sema apply --add NewPattern.json --remove OldPattern
```

**Validation:**
- Patterns to remove must exist
- Patterns to add must pass schema validation
- Dependency graph is checked (cannot remove a pattern that others depend on, unless those are also being removed or re-added)

### search - Search the Vocabulary

```bash
# Keyword search
sema search "coordination"

# Semantic search (uses embeddings)
sema search --semantic "how to handle consensus"

# Verbose output with details
sema search -v "trust"

# JSON output
sema search --json "verification"
```

### resolve - Resolve Dependencies

Shows the dependency subgraph for a pattern.

```bash
sema resolve <Handle>
```

### skeleton - Graph Overview

Displays the graph skeleton (layers, categories, counts).

```bash
sema skeleton
```

### pull - Update Database

Downloads the latest vocabulary database from the registry.

```bash
sema pull
```

### serve - Start API Server

Starts the REST API server.

```bash
sema serve --host 0.0.0.0 --port 3000
```

### mcp - Start MCP Server

Starts the Model Context Protocol server for AI integration.

```bash
sema mcp
```

## Validation Rules

The CLI enforces the following strictly:

1.  **Truth in Advertising:** If you declare a dependency in `dependencies`, you MUST use it in the text (e.g., `{{Dependency}}`).
2.  **Forward Declaration:** If you use `{{Handle}}` in text, it MUST be declared in `dependencies`.
3.  **Taxonomy:** Layer and Category must match the allowed list.
4.  **Schema:** Patterns in `Data Structures` must have a `data_schema`.
5.  **Signature:** Signatures must follow `Verb(Noun)` syntax.
