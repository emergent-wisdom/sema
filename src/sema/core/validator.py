"""
Shared Validation Logic for Sema Patterns.
Used by both the batch ingestion pipeline and the CLI compiler.

Now uses Pydantic schema for structured validation with clear error messages.
"""

import re

from .schema import validate_pattern_schema


def clean_handle(ref_string: str) -> str | None:
    """Extract Handle from "Handle", "sema:Handle", or "sema:Handle#hash"."""
    if not ref_string or not isinstance(ref_string, str):
        return None
    s = ref_string.replace("sema:", "")
    s = s.split("#")[0]
    return s.strip()


def validate_signature_syntax(signature_list: list[str]) -> list[str]:
    """Validate that every signature entry matches strict syntax (e.g., 'Verb(Noun)')."""
    invalid_entries = []
    if not signature_list:
        return invalid_entries
    valid_pattern = re.compile(r"^[A-Z][A-Za-z]*\(.+\)$")
    for item in signature_list:
        if not valid_pattern.match(item):
            invalid_entries.append(item)
    return invalid_entries


def validate_empty_fields_recursive(data, path="") -> list[str]:
    """Recursively check for empty arrays, objects, or null values."""
    errors = []
    if data is None:
        return [f"❌ EMPTY FIELD RULE: Null value found at '{path}'"]

    if isinstance(data, dict):
        if not data and path:
            return [f"❌ EMPTY FIELD RULE: Empty object '{{}}' found at '{path}' (Must be omitted)"]
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            errors.extend(validate_empty_fields_recursive(v, new_path))

    elif isinstance(data, list):
        if not data:
            return [f"❌ EMPTY FIELD RULE: Empty array '[]' found at '{path}' (Must be omitted)"]
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            errors.extend(validate_empty_fields_recursive(item, new_path))

    return errors


def validate_dependencies_usage(pattern: dict) -> list[str]:
    """Enforce Explicit Dependency Rule (Forward and Inverse)."""
    errors = []

    # 1. Gather all declared dependency keys
    deps = pattern.get("dependencies", {})
    declared_keys = set()
    if isinstance(deps, dict):
        for cat in ["accepts", "yields", "composes_with", "references"]:
            if cat in deps and isinstance(deps[cat], dict):
                declared_keys.update(deps[cat].keys())

    # 2. Gather all used keys in hashed text fields
    text_fields = ["mechanism", "gloss"]
    list_fields = ["failure_modes", "invariants", "preconditions", "postconditions"]

    used_keys = set()
    ref_pattern = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

    def scan_text(text, field_name):
        if not isinstance(text, str):
            return
        matches = ref_pattern.findall(text)
        for m in matches:
            used_keys.add(m)
            if m not in declared_keys:
                errors.append(
                    f"❌ FORWARD DEPENDENCY VIOLATION: '{{{{{m}}}}}' used in '{field_name}' but not declared in dependencies."
                )

    for field in text_fields:
        if field in pattern:
            scan_text(pattern[field], field)

    for field in list_fields:
        if field in pattern and isinstance(pattern[field], list):
            for i, item in enumerate(pattern[field]):
                scan_text(item, f"{field}[{i}]")

    # 3. Inverse Check (Declared but not used)
    for k in declared_keys:
        if k not in used_keys:
            errors.append(
                f"❌ INVERSE DEPENDENCY VIOLATION: Dependency '{k}' declared but never used in text."
            )

    return errors


def validate_pattern(
    pattern: dict, known_handles: set[str] | None = None, use_pydantic: bool = True
) -> tuple[bool, list[str], list[str]]:
    """
    Validate pattern against strict rules.

    Args:
        pattern: Pattern dict to validate
        known_handles: Optional set of existing handles for reference validation
        use_pydantic: If True, use Pydantic schema (recommended). If False, use legacy validation.

    Returns: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # Validate the raw value before Pydantic can coerce Python-only inputs.
    # Direct MCP callers do not pass through a JSON decoder, and local JSON
    # historically admitted non-finite numbers. Both must fail before GraphStore
    # creates nodes or edges.
    from .hashing import validate_json_domain, validate_semantic_hash_input

    try:
        validate_json_domain(pattern)
        if isinstance(pattern, dict):
            validate_semantic_hash_input(pattern)
    except ValueError as exc:
        return False, [f"❌ INVALID CANONICAL JSON: {exc}"], warnings

    if use_pydantic:
        # Use Pydantic schema for structured validation
        is_valid, schema_errors, schema_warnings = validate_pattern_schema(pattern)
        errors.extend(schema_errors)
        warnings.extend(schema_warnings)
    else:
        # Legacy validation (kept for backward compatibility)
        # 1. Empty Fields Rule
        errors.extend(validate_empty_fields_recursive(pattern))

        # 2. Explicit Dependency Rule (Forward & Inverse)
        errors.extend(validate_dependencies_usage(pattern))

        # 4. Valid Taxonomy (Strict) — path-based
        meta = pattern.get("_meta", {})
        path = meta.get("path")

        if not path or not isinstance(path, list):
            errors.append("❌ INVALID PATH: '_meta.path' must be a non-empty list of strings.")
        else:
            from .schema import VALID_LAYERS, VALID_PATHS, path_to_string

            if path[0] not in VALID_LAYERS:
                errors.append(
                    f"❌ INVALID LAYER: '{path[0]}' (path[0] must be one of {sorted(VALID_LAYERS)})"
                )
            elif tuple(path) not in VALID_PATHS:
                errors.append(f"❌ INVALID PATH: '{path_to_string(path)}' not in VALID_PATHS")

        # 4b. Constitution Check (Ring & Tier)
        ring = meta.get("ring")
        tier = meta.get("tier")

        if ring is None:
            errors.append("❌ MISSING METADATA: '_meta.ring' is required (0, 1, or 2).")
        elif ring not in [0, 1, 2]:
            errors.append(f"❌ INVALID RING: '{ring}' (Must be 0, 1, or 2).")

        if tier is None:
            errors.append("❌ MISSING METADATA: '_meta.tier' is required (0, 1, 2, or 3).")
        elif tier not in [0, 1, 2, 3]:
            errors.append(f"❌ INVALID TIER: '{tier}' (Must be 0, 1, 2, or 3).")

        # 5. Noun Schema Requirement (Rule J)
        if path and path[-1] == "Data Structures" and "data_schema" not in pattern:
            errors.append(
                "❌ NOUN SCHEMA VIOLATION (Rule J): "
                "Pattern whose path ends in 'Data Structures' must define 'data_schema'."
            )

        # 6. Signature Syntax
        signature = pattern.get("signature", [])
        if signature:
            bad_sig = validate_signature_syntax(signature)
            if bad_sig:
                errors.append(f"❌ SIGNATURE SYNTAX VIOLATION: {bad_sig}")

        # 7. Forbidden Fields Check
        ALLOWED_FIELDS = {
            "handle",
            "extends",
            "derived_from",
            "dependencies",
            "signature",
            "data_schema",
            "mechanism",
            "gloss",
            "invariants",
            "preconditions",
            "postconditions",
            "parameters",
            "failure_modes",
            "sema_id",
            "sema_ref",
            "sema_stub",
            "_meta",
            "sema_layer",
            "sema_category",
        }

        for key in pattern.keys():
            if key not in ALLOWED_FIELDS:
                warnings.append(
                    f"⚠️ FORBIDDEN FIELD: '{key}' is not allowed in INSTRUCTION.md. Please remove it."
                )

        if "extends" in pattern and "derived_from" in pattern:
            errors.append("❌ SPECIALIZATION VIOLATION: use `extends` or `derived_from`, not both.")

    if "derived_from" in pattern and "extends" not in pattern:
        warnings.append(
            "⚠️ DEPRECATED FIELD: `derived_from` is accepted for pre-0.4 hash "
            "compatibility; new cards should use `extends`."
        )

    # Reference Existence Check (applies to both modes)
    # This requires knowledge of existing handles, so it's done separately
    if known_handles is not None:
        deps = pattern.get("dependencies", {})
        if isinstance(deps, dict):
            for cat in ["accepts", "yields", "composes_with", "references"]:
                if cat in deps and isinstance(deps[cat], dict):
                    for key, val in deps[cat].items():
                        target = clean_handle(val)
                        if target and target not in known_handles:
                            errors.append(
                                f"❌ MISSING DEPENDENCY: '{key}' refers to '{target}', "
                                f"which does not exist in vocabulary."
                            )

        parent = clean_handle(pattern.get("extends"))
        if parent and parent not in known_handles:
            errors.append(f"❌ MISSING EXTENDS TARGET: '{parent}' does not exist in vocabulary.")

    return (len(errors) == 0, errors, warnings)
