"""
Pydantic Schema for Sema Patterns.

Provides strict validation with clear error messages.
Used by the CLI and validation pipeline.
"""

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# Canonical taxonomy paths. Each tuple is a valid `_meta.path` in strict
# order: first element is the layer, subsequent elements refine it.
#
# Layers (non-negotiable root set):
#   Infrastructure — Nouns, file formats, execution primitives
#   Physics        — Immutable laws of the simulation
#   Mind           — Active cognitive processes
#   Society        — Multi-agent coordination
#
# Two paths sharing the same leaf segment (e.g. `Physics/Primitives` vs
# `Infrastructure/Primitives`) are distinct identities — the full path,
# not the leaf, is the canonical key. Schema migration in 0.2.0 replaced
# the separate `_meta.layer` + `_meta.category` fields with a single
# `_meta.path` list to make this explicit.
#
# Adding a new path: extend the set. Schema and graph will pick it up
# on the next apply. Deeper hierarchies (3+ levels) are supported by the
# data model — just add a longer tuple.
VALID_PATHS: set[tuple[str, ...]] = {
    ("Infrastructure", "Data Structures"),
    ("Infrastructure", "Primitives"),
    ("Infrastructure", "Safety"),
    ("Infrastructure", "Verification"),
    ("Physics", "Dynamics"),
    ("Physics", "Primitives"),
    ("Physics", "Time"),
    ("Mind", "Inference"),
    ("Mind", "Memory"),
    ("Mind", "Reasoning"),
    ("Mind", "Strategy"),
    ("Society", "Coordination"),
    ("Society", "Economics"),
    ("Society", "Governance"),
    ("Society", "Protocols"),
    ("Society", "Roles"),
}

# Top-level layers (derived from VALID_PATHS for self-consistency).
VALID_LAYERS: frozenset[str] = frozenset(p[0] for p in VALID_PATHS)

# Legacy dict view (kept for tooling + tests that pre-date the path rewrite).
# Derived from VALID_PATHS so there's a single source of truth.
VALID_TAXONOMY: dict[str, set[str]] = {}
for _p in VALID_PATHS:
    _layer = _p[0]
    _rest = _p[1:]
    VALID_TAXONOMY.setdefault(_layer, set())
    if _rest:
        VALID_TAXONOMY[_layer].add("/".join(_rest))

LayerType = Literal["Physics", "Mind", "Society", "Infrastructure"]
RingType = Literal[0, 1, 2]
TierType = Literal[0, 1, 2, 3]

# Separator for rendering paths as strings (Society/Governance). The path
# field is ALWAYS stored as a list; string form is derived on demand.
PATH_SEPARATOR = "/"


def path_to_string(path: list[str]) -> str:
    """Join path segments with PATH_SEPARATOR. No escaping — segments
    cannot contain the separator (enforced by the schema validator)."""
    return PATH_SEPARATOR.join(path)


def path_from_string(s: str) -> list[str]:
    """Split a path string back into segments. Inverse of path_to_string."""
    return [seg for seg in s.split(PATH_SEPARATOR) if seg]


class PatternMeta(BaseModel):
    """Metadata block for patterns (_meta field).

    Path-based taxonomy: `_meta.path` is a list of segments ordered from
    root (the layer) to leaf. The full path, not any individual segment,
    is the canonical identity — `Physics/Primitives` and
    `Infrastructure/Primitives` are different things even though they
    share a leaf name.
    """

    model_config = ConfigDict(extra="allow")  # Allow extra fields like 'caution'

    path: list[str] = Field(
        min_length=1,
        description=(
            "Taxonomic path from layer to leaf, e.g. ['Society', 'Governance']. "
            "path[0] is the layer; subsequent segments refine. Full path must be "
            "in VALID_PATHS."
        ),
    )
    ring: RingType = Field(
        description="Constitution ring: 0 (core), 1 (extended), or 2 (experimental)"
    )
    tier: TierType = Field(
        description=(
            "Formalism tier: 0 (primitive), 1 (ironclad), 2 (honesty-dependent), 3 (experimental)"
        )
    )
    # Optional fields that exist in some patterns
    related: list[str] | None = Field(default=None, description="Related patterns")
    # Versioning hook. Optional list of full sema_id strings of older
    # definitions this pattern is intended to replace. Read by `sema pull`
    # to clean up retired local handles on upgrade.
    supersedes: list[str] | None = Field(
        default=None, description="Older sema_ids this pattern is intended to replace"
    )

    @field_validator("path")
    @classmethod
    def validate_path_value(cls, v: list[str]) -> list[str]:
        """Validate path shape + membership in VALID_PATHS."""
        if not v:
            raise ValueError("path must have at least one segment")
        for i, seg in enumerate(v):
            if not isinstance(seg, str) or not seg:
                raise ValueError(f"path segment {i} must be a non-empty string, got: {seg!r}")
            if PATH_SEPARATOR in seg:
                raise ValueError(
                    f"path segment {i} ('{seg}') cannot contain '{PATH_SEPARATOR}' "
                    "(reserved as path separator)"
                )
        if v[0] not in VALID_LAYERS:
            raise ValueError(
                f"path[0] must be a valid layer (one of {sorted(VALID_LAYERS)}), got '{v[0]}'"
            )
        if tuple(v) not in VALID_PATHS:
            raise ValueError(
                f"invalid taxonomy path '{path_to_string(v)}': not in VALID_PATHS. "
                f"Valid paths: {sorted(path_to_string(list(p)) for p in VALID_PATHS)}"
            )
        return v

    @property
    def layer(self) -> str:
        """Derived: the first path segment (the layer).

        Kept as a property for tooling / docs that still speak in terms
        of layer+category. Do not set directly — edit `path` instead.
        """
        return self.path[0]

    @property
    def category(self) -> str:
        """Derived: the second path segment (the category within a layer),
        or empty string if the path is layer-only."""
        return self.path[1] if len(self.path) >= 2 else ""


class DependencyRefs(BaseModel):
    """Dependency references structure."""

    model_config = ConfigDict(extra="forbid")

    references: dict[str, str] | None = Field(
        default=None, description="Patterns this pattern references"
    )
    composes_with: dict[str, str] | None = Field(
        default=None, description="Patterns this pattern composes with"
    )
    accepts: dict[str, str] | None = Field(
        default=None, description="Input patterns (for type-accepting patterns)"
    )
    yields: dict[str, str] | None = Field(
        default=None, description="Output patterns (for type-yielding patterns)"
    )

    @model_validator(mode="after")
    def no_empty_categories(self) -> "DependencyRefs":
        """Ensure no empty dependency categories exist."""
        for field_name in ["references", "composes_with", "accepts", "yields"]:
            val = getattr(self, field_name)
            if val is not None and len(val) == 0:
                raise ValueError(
                    f"Empty dependency category '{field_name}'. "
                    f"Omit the field instead of using empty dict."
                )
        return self

    @model_validator(mode="after")
    def validate_cross_category_uniqueness(self) -> "DependencyRefs":
        """Ensure dependency keys appear in exactly one category (Rule 2.3)."""
        key_locations: dict[str, list[str]] = {}
        for field_name in ["references", "composes_with", "accepts", "yields"]:
            val = getattr(self, field_name)
            if val:
                for key in val.keys():
                    if key not in key_locations:
                        key_locations[key] = []
                    key_locations[key].append(field_name)

        duplicates = {k: v for k, v in key_locations.items() if len(v) > 1}
        if duplicates:
            raise ValueError(
                f"Dependency keys appear in multiple categories: {duplicates}. "
                f"Each key must be unique across all dependency categories."
            )
        return self

    @model_validator(mode="after")
    def validate_snake_case_keys(self) -> "DependencyRefs":
        """Ensure dependency keys are snake_case (Rule 2.5)."""
        snake_pattern = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
        errors = []
        for field_name in ["references", "composes_with", "accepts", "yields"]:
            val = getattr(self, field_name)
            if val:
                for key in val.keys():
                    if not snake_pattern.match(key):
                        errors.append(f"{field_name}.{key}")

        if errors:
            raise ValueError(
                f"Dependency keys must be snake_case: {errors}. "
                f"Use lowercase with underscores (e.g., 'my_tool', not 'MyTool')."
            )
        return self

    @model_validator(mode="after")
    def validate_full_hash_standard(self) -> "DependencyRefs":
        """Ensure dependency values match Full Hash format (Rule 2.4)."""
        hash_pattern = re.compile(r"^sema:[A-Z][a-zA-Z0-9]+#mh:SHA-256:[a-f0-9]{64}$")
        errors = []
        for field_name in ["references", "composes_with", "accepts", "yields"]:
            val = getattr(self, field_name)
            if val:
                for key, value in val.items():
                    if not hash_pattern.match(value):
                        errors.append(f"{field_name}.{key}: '{value}'")

        if errors:
            raise ValueError(
                f"Full Hash Standard violation (Rule 2.4): {errors}. "
                f"All dependency values must match 'sema:Handle#mh:SHA-256:<64-char-hash>'."
            )
        return self

    def get_all_keys(self) -> set:
        """Get all declared dependency keys."""
        keys = set()
        for field_name in ["references", "composes_with", "accepts", "yields"]:
            val = getattr(self, field_name)
            if val:
                keys.update(val.keys())
        return keys


class DataSchema(BaseModel):
    """Schema for data structure patterns (Rule J).

    Must be a valid JSON Schema (Rule 5.2).
    """

    model_config = ConfigDict(extra="allow")  # Allow flexible schema fields

    # Minimal required structure - patterns can extend this
    type: str | None = None
    fields: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_json_schema(self) -> "DataSchema":
        """Validate that this is a valid JSON Schema (Rule 5.2)."""
        try:
            from jsonschema import Draft7Validator

            # Convert to dict for validation
            schema_dict = self.model_dump(exclude_none=True)
            Draft7Validator.check_schema(schema_dict)
        except ImportError:
            # jsonschema not available, skip validation
            pass
        except Exception as e:
            raise ValueError(f"data_schema is not valid JSON Schema (Rule 5.2): {e}") from e
        return self


class SemaPattern(BaseModel):
    """
    Complete Sema Pattern schema.

    Validates all required fields, taxonomy, signatures, and dependency usage.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,  # Allow both 'meta' and '_meta'
    )

    # Required fields
    handle: str = Field(min_length=1, max_length=50, description="CamelCase pattern identifier")
    mechanism: str = Field(min_length=1, description="Core mechanism description")
    meta: PatternMeta = Field(
        alias="_meta", description="Pattern metadata (layer, category, ring, tier)"
    )

    # Optional semantic fields
    gloss: str | None = Field(default=None, min_length=1, description="Brief one-line description")
    invariants: list[str] | None = Field(
        default=None, min_length=1, description="Conditions that must remain true"
    )
    preconditions: list[str] | None = Field(
        default=None, min_length=1, description="Conditions required before application"
    )
    postconditions: list[str] | None = Field(
        default=None, min_length=1, description="Conditions guaranteed after application"
    )
    parameters: list[dict[str, Any]] | None = Field(
        default=None, min_length=1, description="Configurable parameter objects (Rule 4.2)"
    )
    failure_modes: list[str] | None = Field(
        default=None, min_length=1, description="Known failure modes"
    )
    signature: list[str] | None = Field(
        default=None, min_length=1, description="Type signature entries"
    )
    dependencies: DependencyRefs | None = Field(default=None, description="Pattern dependencies")
    derived_from: str | None = Field(
        default=None, description="Parent pattern this was derived from"
    )
    data_schema: DataSchema | None = Field(
        default=None, description="Schema for Data Structures category"
    )

    # Computed fields (added during processing)
    sema_id: str | None = Field(default=None)
    sema_ref: str | None = Field(default=None)
    sema_stub: str | None = Field(default=None)
    sema_layer: str | None = Field(default=None)
    sema_category: str | None = Field(default=None)

    @field_validator("handle")
    @classmethod
    def validate_handle_format(cls, v: str) -> str:
        """Validate handle is CamelCase and doesn't contain path separator."""
        if not re.match(r"^[A-Z][a-zA-Z0-9]+$", v):
            raise ValueError(
                f"Handle '{v}' must be CamelCase (start with uppercase, "
                f"alphanumeric only, no underscores or hyphens)"
            )
        if PATH_SEPARATOR in v:
            raise ValueError(
                f"Handle '{v}' cannot contain '{PATH_SEPARATOR}' (reserved for taxonomy paths)"
            )
        return v

    @field_validator("signature")
    @classmethod
    def validate_signature_syntax(cls, v: list[str] | None) -> list[str] | None:
        """Validate signature entries match Verb(Noun) syntax."""
        if v is None:
            return v
        pattern = re.compile(r"^[A-Z][A-Za-z]*\(.+\)$")
        invalid = [sig for sig in v if not pattern.match(sig)]
        if invalid:
            raise ValueError(
                f"Invalid signature syntax: {invalid}. "
                f"Must match 'Verb(Noun)' format, e.g., 'Accept(Token)'"
            )
        return v

    @field_validator("parameters")
    @classmethod
    def validate_parameters_structure(
        cls, v: list[dict[str, Any]] | None
    ) -> list[dict[str, Any]] | None:
        """Validate parameters are objects with required fields (Rules 4.2, 4.3)."""
        if v is None:
            return v
        required_fields = {"name", "type", "range", "description"}
        for i, param in enumerate(v):
            missing = required_fields - set(param.keys())
            if missing:
                raise ValueError(
                    f"parameters[{i}] missing required fields: {missing}. "
                    f"Each parameter must have: name, type, range, description"
                )
        return v

    @model_validator(mode="after")
    def validate_data_schema_required(self) -> "SemaPattern":
        """Data Structures category must have data_schema (Rule J).

        Checks the leaf path segment rather than a `category` field —
        any path ending in 'Data Structures' triggers the requirement.
        """
        if self.meta.path and self.meta.path[-1] == "Data Structures" and self.data_schema is None:
            raise ValueError(
                "Patterns whose path ends in 'Data Structures' must define 'data_schema' (Rule J)"
            )
        return self

    @model_validator(mode="after")
    def validate_dependency_usage(self) -> "SemaPattern":
        """Validate forward and inverse dependency rules."""
        # Get declared dependency keys
        declared_keys = set()
        if self.dependencies:
            declared_keys = self.dependencies.get_all_keys()

        # Find all {{placeholder}} references in text fields
        ref_pattern = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")
        used_keys = set()
        errors = []

        def scan_text(text: str, field_name: str):
            if not text:
                return
            for match in ref_pattern.findall(text):
                used_keys.add(match)
                if match not in declared_keys:
                    errors.append(
                        f"'{{{{{match}}}}}' used in '{field_name}' but not declared in dependencies"
                    )

        # Scan text fields
        scan_text(self.mechanism, "mechanism")
        if self.gloss:
            scan_text(self.gloss, "gloss")

        # Scan list fields
        for field_name in ["invariants", "preconditions", "postconditions", "failure_modes"]:
            items = getattr(self, field_name)
            if items:
                for i, item in enumerate(items):
                    scan_text(item, f"{field_name}[{i}]")

        # Forward dependency check
        if errors:
            raise ValueError(f"Forward dependency violations: {'; '.join(errors)}")

        # Inverse dependency check (declared but not used)
        unused = declared_keys - used_keys
        if unused:
            raise ValueError(
                f"Inverse dependency violation: {unused} declared but never used in text"
            )

        return self

    @model_validator(mode="after")
    def validate_signature_types_in_dependencies(self) -> "SemaPattern":
        """
        Enforce Explicit Wiring Rule (Section 1.2):
        Every type in signature must appear in dependencies.
        The inverse dependency rule then ensures they're used in text.
        """
        if not self.signature:
            return self

        # Get declared dependency keys
        declared_keys = set()
        if self.dependencies:
            declared_keys = self.dependencies.get_all_keys()

        # Parse signature entries: "Verb(Noun)" or "Verb(Noun1, Noun2)"
        sig_pattern = re.compile(r"^([A-Z][A-Za-z]*)\((.+)\)$")
        missing = []

        for sig in self.signature:
            match = sig_pattern.match(sig)
            if not match:
                continue  # Syntax validation handled elsewhere

            verb = match.group(1)
            nouns_str = match.group(2)

            # Collect all types from signature (verb + all nouns)
            types = [verb]
            # Split nouns by comma, handle "Noun1, Noun2" and "Criteria=PURE"
            for noun in nouns_str.split(","):
                noun = noun.strip()
                # Handle assignment syntax like "Criteria=PURE"
                if "=" in noun:
                    noun = noun.split("=")[0].strip()
                if noun:
                    types.append(noun)

            # Convert CamelCase to snake_case for dependency key lookup
            for t in types:
                snake_key = re.sub(r"(?<!^)(?=[A-Z])", "_", t).lower()
                if snake_key not in declared_keys:
                    missing.append(f"'{t}' (as '{snake_key}') from signature '{sig}'")

        if missing:
            raise ValueError(
                f"Explicit Wiring Rule violation: Signature types must be in dependencies. "
                f"Missing: {', '.join(missing)}"
            )

        return self

    @model_validator(mode="after")
    def no_empty_lists(self) -> "SemaPattern":
        """Ensure no empty lists exist (must be omitted instead)."""
        list_fields = [
            "invariants",
            "preconditions",
            "postconditions",
            "parameters",
            "failure_modes",
            "signature",
        ]
        for field_name in list_fields:
            val = getattr(self, field_name)
            if val is not None and len(val) == 0:
                raise ValueError(f"Empty list for '{field_name}'. Omit the field instead.")
        return self

    @model_validator(mode="after")
    def no_dependency_in_related(self) -> "SemaPattern":
        """
        Enforce Dependency/Related Separation Rule:
        Patterns that appear in dependencies should NOT also appear in _meta.related.
        Dependencies are structural wiring; related is for conceptual associations.
        """
        # Get related patterns from _meta
        related = self.meta.related or []
        if not related:
            return self

        # Collect all dependency target handles
        dep_handles = set()
        if self.dependencies:
            for field_name in ["references", "composes_with", "accepts", "yields"]:
                refs = getattr(self.dependencies, field_name)
                if refs:
                    for ref_value in refs.values():
                        # Extract handle from "sema:Handle#hash" or "sema:Handle" or "Handle"
                        handle = ref_value.replace("sema:", "").split("#")[0].strip()
                        if handle:
                            dep_handles.add(handle)

        # Check for overlap
        overlap = set(related) & dep_handles
        if overlap:
            raise ValueError(
                f"Dependency/Related separation violation: {sorted(overlap)} "
                f"appear in both dependencies and _meta.related. "
                f"Remove them from 'related' since they are already dependencies."
            )

        return self


def validate_pattern_schema(pattern: dict) -> tuple[bool, list[str], list[str]]:
    """
    Validate a pattern dict against the Pydantic schema.

    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    try:
        SemaPattern.model_validate(pattern)
    except Exception as e:
        # Extract error messages from Pydantic validation
        error_msg = str(e)
        # Clean up pydantic error formatting for readability
        if "validation error" in error_msg.lower():
            # Parse Pydantic v2 error format
            for line in error_msg.split("\n"):
                line = line.strip()
                if line and not line.startswith("For further") and "SemaPattern" not in line:
                    if line.startswith("Value error,"):
                        errors.append(f"❌ {line[13:]}")  # Strip "Value error, "
                    elif "Input should be" in line or "Field required" in line:
                        errors.append(f"❌ {line}")
                    elif line and not line[0].isdigit():
                        errors.append(f"❌ {line}")
        else:
            errors.append(f"❌ {error_msg}")

    return (len(errors) == 0, errors, warnings)
