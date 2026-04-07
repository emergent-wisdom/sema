"""Tests for Pydantic pattern schema validation."""

import pytest

from sema.core.schema import (
    VALID_TAXONOMY,
    DependencyRefs,
    PatternMeta,
    SemaPattern,
    validate_pattern_schema,
)


class TestPatternMeta:
    """Test PatternMeta validation."""

    def test_valid_meta(self):
        """Valid metadata should parse."""
        meta = PatternMeta(layer="Infrastructure", category="Primitives", ring=0, tier=1)
        assert meta.layer == "Infrastructure"
        assert meta.category == "Primitives"

    def test_invalid_layer(self):
        """Invalid layer should fail."""
        with pytest.raises(ValueError, match="Input should be"):
            PatternMeta(layer="InvalidLayer", category="Primitives", ring=0, tier=1)

    def test_invalid_category_for_layer(self):
        """Category must be valid for the layer."""
        with pytest.raises(ValueError, match="Invalid category"):
            PatternMeta(
                layer="Infrastructure",
                category="Creativity",  # Creativity is in Mind, not Infrastructure
                ring=0,
                tier=1,
            )

    def test_invalid_ring(self):
        """Ring must be 0, 1, or 2."""
        with pytest.raises(ValueError):
            PatternMeta(layer="Infrastructure", category="Primitives", ring=5, tier=1)

    def test_invalid_tier(self):
        """Tier must be 0, 1, 2, or 3."""
        with pytest.raises(ValueError):
            PatternMeta(layer="Infrastructure", category="Primitives", ring=0, tier=10)


def make_sema_id(handle: str, suffix: str = "a") -> str:
    """Helper to create a valid full sema ID for testing."""
    return f"sema:{handle}#mh:SHA-256:{suffix * 64}"


class TestDependencyRefs:
    """Test DependencyRefs validation."""

    def test_valid_deps(self):
        """Valid dependencies with full hash format should parse."""
        deps = DependencyRefs(
            references={"gate": make_sema_id("Gate")},
            composes_with={"buffer": make_sema_id("Buffer", "b")},
        )
        assert "gate" in deps.references
        assert "buffer" in deps.composes_with

    def test_empty_category_fails(self):
        """Empty dependency category should fail."""
        with pytest.raises(ValueError, match="Empty dependency category"):
            DependencyRefs(references={})

    def test_get_all_keys(self):
        """get_all_keys should return all declared keys."""
        deps = DependencyRefs(
            references={"alpha": make_sema_id("Alpha"), "beta": make_sema_id("Beta")},
            accepts={"gamma": make_sema_id("Gamma")},
        )
        keys = deps.get_all_keys()
        assert keys == {"alpha", "beta", "gamma"}

    # --- Rule 2.3: Cross-Category Uniqueness ---

    def test_cross_category_uniqueness_fails(self):
        """2.3: Same key in multiple categories should fail."""
        with pytest.raises(ValueError, match="multiple categories"):
            DependencyRefs(
                references={"gate": make_sema_id("Gate")},
                composes_with={"gate": make_sema_id("Gate")},  # Duplicate key!
            )

    def test_cross_category_uniqueness_passes(self):
        """2.3: Different keys in different categories should pass."""
        deps = DependencyRefs(
            references={"gate": make_sema_id("Gate")},
            composes_with={"buffer": make_sema_id("Buffer")},
        )
        assert "gate" in deps.references
        assert "buffer" in deps.composes_with

    # --- Rule 2.4: Full Hash Standard ---

    def test_full_hash_standard_valid(self):
        """2.4: Valid sema:Handle#mh:SHA-256:hash format should pass."""
        deps = DependencyRefs(references={"gate": make_sema_id("Gate")})
        assert deps.references is not None

    def test_full_hash_standard_stub_fails(self):
        """2.4: Stub format (Handle#1234) should fail."""
        with pytest.raises(ValueError, match="Full Hash Standard"):
            DependencyRefs(references={"gate": "Gate#1234"})

    def test_full_hash_standard_bare_handle_fails(self):
        """2.4: Bare handle should fail."""
        with pytest.raises(ValueError, match="Full Hash Standard"):
            DependencyRefs(references={"gate": "Gate"})

    def test_full_hash_standard_wrong_algo_fails(self):
        """2.4: Wrong hash algorithm should fail."""
        with pytest.raises(ValueError, match="Full Hash Standard"):
            DependencyRefs(references={"gate": "sema:Gate#mh:MD5:" + "a" * 32})

    # --- Rule 2.5: Snake Case Keys ---

    def test_snake_case_valid(self):
        """2.5: Valid snake_case keys should pass."""
        deps = DependencyRefs(references={"my_gate": make_sema_id("Gate")})
        assert "my_gate" in deps.references

    def test_snake_case_single_word(self):
        """2.5: Single lowercase word is valid snake_case."""
        deps = DependencyRefs(references={"gate": make_sema_id("Gate")})
        assert "gate" in deps.references

    def test_snake_case_camel_fails(self):
        """2.5: CamelCase keys should fail."""
        with pytest.raises(ValueError, match="snake_case"):
            DependencyRefs(references={"MyGate": make_sema_id("Gate")})

    def test_snake_case_pascal_fails(self):
        """2.5: PascalCase keys should fail."""
        with pytest.raises(ValueError, match="snake_case"):
            DependencyRefs(references={"Gate": make_sema_id("Gate")})

    def test_snake_case_kebab_fails(self):
        """2.5: kebab-case keys should fail."""
        with pytest.raises(ValueError, match="snake_case"):
            DependencyRefs(references={"my-gate": make_sema_id("Gate")})


class TestParameters:
    """Test parameters field validation (Rule 4.3)."""

    @pytest.fixture
    def base_pattern(self):
        """Base pattern for parameters testing."""
        return {
            "handle": "TestPattern",
            "mechanism": "Test pattern.",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "ring": 0, "tier": 1},
        }

    def test_parameters_structure_valid(self, base_pattern):
        """4.3: Valid parameters with all required fields should pass."""
        base_pattern["parameters"] = [
            {
                "name": "threshold",
                "type": "Float",
                "range": "[0,1]",
                "description": "Cutoff value for filtering",
            }
        ]
        p = SemaPattern.model_validate(base_pattern)
        assert p.parameters is not None
        assert len(p.parameters) == 1

    def test_parameters_missing_name_fails(self, base_pattern):
        """4.3: Missing 'name' field should fail."""
        base_pattern["parameters"] = [{"type": "Float", "range": "[0,1]", "description": "Test"}]
        with pytest.raises(ValueError, match="missing required fields.*name"):
            SemaPattern.model_validate(base_pattern)

    def test_parameters_missing_type_fails(self, base_pattern):
        """4.3: Missing 'type' field should fail."""
        base_pattern["parameters"] = [{"name": "x", "range": "[0,1]", "description": "Test"}]
        with pytest.raises(ValueError, match="missing required fields.*type"):
            SemaPattern.model_validate(base_pattern)

    def test_parameters_missing_range_fails(self, base_pattern):
        """4.3: Missing 'range' field should fail."""
        base_pattern["parameters"] = [{"name": "x", "type": "Float", "description": "Test"}]
        with pytest.raises(ValueError, match="missing required fields.*range"):
            SemaPattern.model_validate(base_pattern)

    def test_parameters_missing_description_fails(self, base_pattern):
        """4.3: Missing 'description' field should fail."""
        base_pattern["parameters"] = [{"name": "x", "type": "Float", "range": "[0,1]"}]
        with pytest.raises(ValueError, match="missing required fields.*description"):
            SemaPattern.model_validate(base_pattern)

    def test_parameters_default_optional(self, base_pattern):
        """4.4: 'default' field is optional."""
        base_pattern["parameters"] = [
            {
                "name": "x",
                "type": "Int",
                "range": "[0,10]",
                "description": "Test param",
                "default": 5,
            }
        ]
        p = SemaPattern.model_validate(base_pattern)
        assert p.parameters[0]["default"] == 5

    def test_parameters_multiple_valid(self, base_pattern):
        """4.3: Multiple parameters with all required fields should pass."""
        base_pattern["parameters"] = [
            {"name": "a", "type": "Int", "range": "[0,10]", "description": "First"},
            {"name": "b", "type": "Float", "range": "[0,1]", "description": "Second"},
        ]
        p = SemaPattern.model_validate(base_pattern)
        assert len(p.parameters) == 2

    def test_parameters_string_rejected(self, base_pattern):
        """4.2: Parameters must be objects, not strings."""
        base_pattern["parameters"] = ["simple_param"]
        with pytest.raises(ValueError):
            SemaPattern.model_validate(base_pattern)


class TestSemaPattern:
    """Test full SemaPattern validation."""

    @pytest.fixture
    def valid_pattern(self):
        """A valid pattern dict."""
        return {
            "handle": "TestPattern",
            "mechanism": "A test pattern for validation.",
            "_meta": {"layer": "Infrastructure", "category": "Primitives", "ring": 0, "tier": 1},
        }

    def test_valid_pattern(self, valid_pattern):
        """Valid pattern should parse."""
        pattern = SemaPattern.model_validate(valid_pattern)
        assert pattern.handle == "TestPattern"
        assert pattern.mechanism == "A test pattern for validation."
        assert pattern.meta.layer == "Infrastructure"

    def test_invalid_handle_lowercase(self, valid_pattern):
        """Handle must be CamelCase."""
        valid_pattern["handle"] = "lowercase"
        with pytest.raises(ValueError, match="CamelCase"):
            SemaPattern.model_validate(valid_pattern)

    def test_invalid_handle_underscore(self, valid_pattern):
        """Handle cannot contain underscores."""
        valid_pattern["handle"] = "Test_Pattern"
        with pytest.raises(ValueError, match="CamelCase"):
            SemaPattern.model_validate(valid_pattern)

    def test_forward_dependency_violation(self, valid_pattern):
        """Used {{placeholder}} must be declared in dependencies."""
        valid_pattern["mechanism"] = "Uses {{undefined}} reference"
        with pytest.raises(ValueError, match="Forward dependency"):
            SemaPattern.model_validate(valid_pattern)

    def test_inverse_dependency_violation(self, valid_pattern):
        """Declared dependencies must be used in text."""
        valid_pattern["dependencies"] = {"references": {"unused": make_sema_id("SomePattern")}}
        with pytest.raises(ValueError, match="Inverse dependency"):
            SemaPattern.model_validate(valid_pattern)

    def test_valid_with_dependencies(self, valid_pattern):
        """Pattern with properly used dependencies should pass."""
        gate_id = make_sema_id("Gate")
        valid_pattern["mechanism"] = "Uses {{gate}} for control."
        valid_pattern["dependencies"] = {"references": {"gate": gate_id}}
        pattern = SemaPattern.model_validate(valid_pattern)
        assert pattern.dependencies.references == {"gate": gate_id}

    def test_signature_valid(self, valid_pattern):
        """Valid signature syntax should pass with explicit wiring."""
        valid_pattern["mechanism"] = "Uses {{accept}}, {{token}}, {{emit}}, {{result}}."
        valid_pattern["signature"] = ["Accept(Token)", "Emit(Result)"]
        valid_pattern["dependencies"] = {
            "references": {
                "accept": make_sema_id("Accept"),
                "token": make_sema_id("Token"),
                "emit": make_sema_id("Emit"),
                "result": make_sema_id("Result"),
            }
        }
        pattern = SemaPattern.model_validate(valid_pattern)
        assert pattern.signature == ["Accept(Token)", "Emit(Result)"]

    def test_signature_invalid(self, valid_pattern):
        """Invalid signature syntax should fail."""
        valid_pattern["signature"] = ["invalid_signature", "also-bad"]
        with pytest.raises(ValueError, match="Invalid signature syntax"):
            SemaPattern.model_validate(valid_pattern)

    def test_data_schema_required_for_data_structures(self):
        """Data Structures category requires data_schema (Rule J)."""
        pattern = {
            "handle": "TestNoun",
            "mechanism": "A data structure pattern.",
            "_meta": {
                "layer": "Infrastructure",
                "category": "Data Structures",
                "ring": 0,
                "tier": 1,
            },
        }
        with pytest.raises(ValueError, match="data_schema"):
            SemaPattern.model_validate(pattern)

    def test_data_schema_provided(self):
        """Data Structures with data_schema should pass."""
        pattern = {
            "handle": "TestNoun",
            "mechanism": "A data structure pattern.",
            "_meta": {
                "layer": "Infrastructure",
                "category": "Data Structures",
                "ring": 0,
                "tier": 1,
            },
            "data_schema": {"type": "object", "fields": {"value": "any"}},
        }
        p = SemaPattern.model_validate(pattern)
        assert p.data_schema is not None

    def test_empty_list_fails(self, valid_pattern):
        """Empty lists should fail (must be omitted instead)."""
        valid_pattern["invariants"] = []
        with pytest.raises(ValueError, match="too_short|at least 1"):
            SemaPattern.model_validate(valid_pattern)

    def test_forbidden_field_fails(self, valid_pattern):
        """Unknown fields should fail (extra='forbid')."""
        valid_pattern["unknown_field"] = "value"
        with pytest.raises(ValueError):
            SemaPattern.model_validate(valid_pattern)


class TestValidatePatternSchema:
    """Test the validate_pattern_schema helper function."""

    def test_returns_tuple(self):
        """Should return (is_valid, errors, warnings)."""
        pattern = {
            "handle": "TestPattern",
            "mechanism": "Test mechanism.",
            "_meta": {"layer": "Mind", "category": "Strategy", "ring": 1, "tier": 2},
        }
        result = validate_pattern_schema(pattern)
        assert isinstance(result, tuple)
        assert len(result) == 3
        is_valid, errors, warnings = result
        assert is_valid is True
        assert errors == []

    def test_returns_errors_on_invalid(self):
        """Should return errors for invalid pattern."""
        pattern = {
            "handle": "invalid",  # lowercase
            "mechanism": "Test",
            "_meta": {"layer": "Wrong", "category": "Bad", "ring": 0, "tier": 0},
        }
        is_valid, errors, warnings = validate_pattern_schema(pattern)
        assert is_valid is False
        assert len(errors) > 0


class TestDataSchema:
    """Test data_schema validation (Rule 5.2)."""

    @pytest.fixture
    def base_pattern(self):
        """Base pattern for data_schema testing."""
        return {
            "handle": "TestNoun",
            "mechanism": "A test data structure.",
            "_meta": {
                "layer": "Infrastructure",
                "category": "Data Structures",
                "ring": 0,
                "tier": 1,
            },
        }

    def test_valid_json_schema(self, base_pattern):
        """5.2: Valid JSON Schema should pass."""
        base_pattern["data_schema"] = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "value": {"type": "number"}},
            "required": ["name"],
        }
        p = SemaPattern.model_validate(base_pattern)
        assert p.data_schema is not None

    def test_invalid_json_schema_type(self, base_pattern):
        """5.2: Invalid JSON Schema 'type' value should fail."""
        base_pattern["data_schema"] = {
            "type": "not_a_valid_type"  # Invalid type
        }
        with pytest.raises(ValueError, match="not valid JSON Schema"):
            SemaPattern.model_validate(base_pattern)

    def test_data_schema_with_custom_fields(self, base_pattern):
        """5.2: JSON Schema with custom 'fields' (Sema extension) should pass."""
        base_pattern["data_schema"] = {
            "type": "object",
            "fields": {"value": "any"},  # Sema extension
        }
        p = SemaPattern.model_validate(base_pattern)
        assert p.data_schema.fields == {"value": "any"}


class TestLayerDirection:
    """Test layer direction validation (Rule 7.6)."""

    def test_valid_direction_high_to_low(self):
        """7.6: Society depending on Physics is valid (high -> low)."""
        from sema.core.dependencies import check_layer_direction

        patterns = {
            "HighLevel": {
                "handle": "HighLevel",
                "_meta": {"layer": "Society"},
                "dependencies": {"references": {"low": "sema:LowLevel#mh:SHA-256:" + "a" * 64}},
            }
        }
        existing = {"LowLevel": {"handle": "LowLevel", "_meta": {"layer": "Physics"}}}
        violations = check_layer_direction(patterns, existing)
        assert violations == []

    def test_invalid_direction_low_to_high(self):
        """7.6: Physics depending on Society is invalid (low -> high)."""
        from sema.core.dependencies import check_layer_direction

        patterns = {
            "LowLevel": {
                "handle": "LowLevel",
                "_meta": {"layer": "Physics"},
                "dependencies": {"references": {"high": "sema:HighLevel#mh:SHA-256:" + "a" * 64}},
            }
        }
        existing = {"HighLevel": {"handle": "HighLevel", "_meta": {"layer": "Society"}}}
        violations = check_layer_direction(patterns, existing)
        assert len(violations) == 1
        assert violations[0] == ("LowLevel", "Physics", "HighLevel", "Society")

    def test_same_layer_allowed(self):
        """7.6: Same layer dependencies are allowed."""
        from sema.core.dependencies import check_layer_direction

        patterns = {
            "PatternA": {
                "handle": "PatternA",
                "_meta": {"layer": "Mind"},
                "dependencies": {"references": {"b": "sema:PatternB#mh:SHA-256:" + "a" * 64}},
            }
        }
        existing = {"PatternB": {"handle": "PatternB", "_meta": {"layer": "Mind"}}}
        violations = check_layer_direction(patterns, existing)
        assert violations == []

    def test_validate_layer_direction_raises(self):
        """7.6: validate_layer_direction raises ValueError on violation."""
        from sema.core.dependencies import validate_layer_direction

        patterns = {
            "PhysicsPattern": {
                "handle": "PhysicsPattern",
                "_meta": {"layer": "Physics"},
                "dependencies": {
                    "references": {"soc": "sema:SocietyPattern#mh:SHA-256:" + "a" * 64}
                },
            }
        }
        existing = {"SocietyPattern": {"handle": "SocietyPattern", "_meta": {"layer": "Society"}}}
        with pytest.raises(ValueError, match="Layer direction violation"):
            validate_layer_direction(patterns, existing)


class TestTaxonomy:
    """Test taxonomy structure is complete."""

    def test_all_layers_present(self):
        """All four layers should be defined."""
        assert set(VALID_TAXONOMY.keys()) == {"Physics", "Mind", "Society", "Infrastructure"}

    def test_mind_categories(self):
        """Mind layer should have all expected categories."""
        mind_cats = VALID_TAXONOMY["Mind"]
        assert "Reasoning" in mind_cats
        assert "Strategy" in mind_cats
        assert "Inference" in mind_cats
        assert "Memory" in mind_cats

    def test_infrastructure_has_primitives(self):
        """Infrastructure should include Primitives category."""
        assert "Primitives" in VALID_TAXONOMY["Infrastructure"]
