# Sema Documentation

Welcome to the Sema documentation. This library is organized into packages covering core philosophy, technical specifications, operational workflows, and tooling.

## 📚 Documentation Structure

### 1. [Core Philosophy](core/philosophy.md)
Understanding the "why" behind Sema.
- **[Philosophy](core/philosophy.md):** The fundamental principles of semantic stability, content-addressing, and "Text is Code".

### 2. [Specification](specification/naming.md)
The strict rules that define the Sema protocol.
- **[Pattern Authoring Guide](specification/authoring.md):** Complete guide to minting patterns — schema, rules A-K, hashing protocol, naming morphology, and the staging workflow.
- **[Naming & Taxonomy](specification/naming.md):** Rules for Handles, Layers, and Categories.
- **[Schema Specification](specification/schema.md):** The JSON structure of a Pattern Card.
- **[Validation Rules](specification/validation.md):** The invariants enforced by the compiler (e.g., Truth in Advertising).
- **[Validation Matrix](specification/validation-matrix.md):** All 42 compiler checks with implementation status and code locations.

### 3. [Tooling](tools/cli.md)
Tools for interacting with the vocabulary.
- **[CLI](tools/cli.md):** The primary tool for adding, updating, and removing patterns (`sema` command).

### 4. [Operations](operations/legacy_workflow.md)
Workflows for maintaining the vocabulary.
- **[Vocabulary Maintenance](operations/legacy_workflow.md):** Adding, removing, and validating patterns with `sema apply`.

### 5. [Information](information/vocabulary_information.md)
System status and cryptographic verification.
- **[Vocabulary Information](information/vocabulary_information.md):** The cryptographic root hash and statistical breakdown of the current vocabulary.

## 🚀 Getting Started

To modify the vocabulary, use the `sema` CLI:

```bash
# Install the package
pip install -e .

# Add patterns (validates before applying)
sema apply --add MyPattern.json

# Remove patterns (validates dependencies first)
sema apply --remove MyPattern

# Atomic add + remove in one operation
sema apply --add NewPattern.json --remove OldPattern
```
