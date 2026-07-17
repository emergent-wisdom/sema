"""Canonicalization v2 invariants for the core hashing pipeline.

word = hash(canonical(definition)) only holds if:
  1. structurally different values never share a hash (domain separation),
  2. the hash is a pure function of the canonical form (normalization
     happens before ordering), and
  3. nothing is silently dropped from the hash input.

Every collision pair below hashed IDENTICALLY under v1.
"""

import pytest

from sema.core.hashing import (
    _TAG_DICT,
    _TAG_LIST,
    _TAG_PRIMITIVE,
    _TAG_STR,
    canonicalize_dependency_keys,
    generate_sema_hash,
    merkle_hash,
    resolve_dependencies_to_sema_ids,
)


class TestDomainSeparation:
    """v1 collision pairs — each must now hash differently."""

    def test_production_tags_match_verified_lean_model(self):
        """Keep Python's bytes connected to CanonicalEncoding.lean."""
        assert {
            "string": _TAG_STR,
            "primitive": _TAG_PRIMITIVE,
            "list": _TAG_LIST,
            "dictionary": _TAG_DICT,
        } == {
            "string": bytes([115, 58]),
            "primitive": bytes([112, 58]),
            "list": bytes([108, 58]),
            "dictionary": bytes([100, 58]),
        }

    @pytest.mark.parametrize(
        "a,b",
        [
            ("1", 1),
            ("true", True),
            ("null", None),
            ("1.5", 1.5),
            ("", []),
            ("", {}),
            ([], {}),
            (["a", "b"], {"a": "b"}),
            (0, False),  # canonical JSON distinguishes: "0" vs "false"
            (1, True),
        ],
    )
    def test_structurally_different_values_hash_differently(self, a, b):
        hash_a, _ = merkle_hash(a)
        hash_b, _ = merkle_hash(b)
        assert hash_a != hash_b, f"collision: {a!r} vs {b!r}"

    def test_nested_shape_confusion(self):
        """A list of two digests must not imitate a one-entry dict."""
        hash_list, _ = merkle_hash([["x"], ["y"]])
        hash_dict, _ = merkle_hash({"x": "y"})
        assert hash_list != hash_dict

    def test_end_to_end_data_schema_shape_distinct(self):
        """The original repro: dict-shaped vs list-shaped data_schema."""
        base = {"handle": "Shape", "mechanism": "m", "gloss": "g"}
        dict_shape = generate_sema_hash({**base, "data_schema": {"fields": {"a": "b"}}})
        list_shape = generate_sema_hash({**base, "data_schema": {"fields": ["a", "b"]}})
        assert dict_shape["hash"] != list_shape["hash"]

    def test_end_to_end_parameter_type_distinct(self):
        base = {"handle": "Shape", "mechanism": "m", "gloss": "g"}
        str_param = generate_sema_hash({**base, "parameters": {"n": "0"}})
        int_param = generate_sema_hash({**base, "parameters": {"n": 0}})
        assert str_param["hash"] != int_param["hash"]


class TestCanonicalFormIsHashInput:
    """The hash must be a pure function of the canonical form."""

    def test_key_whitespace_normalizes_before_ordering(self):
        """v1 sorted raw keys but hashed normalized keys, so these two
        identical canonical dicts hashed differently."""
        hash_a, canon_a = merkle_hash({" c": 1, "b": 2})
        hash_b, canon_b = merkle_hash({"c": 1, "b": 2})
        assert canon_a == canon_b
        assert hash_a == hash_b

    def test_normalized_key_collision_fails_closed(self):
        """v1 silently dropped one entry; v2 refuses to produce a hash."""
        with pytest.raises(ValueError, match="collide after normalization"):
            merkle_hash({"a ": 1, "a": 2})

    def test_string_normalization_still_applies(self):
        hash_a, _ = merkle_hash("  hello   world  ")
        hash_b, _ = merkle_hash("hello world")
        assert hash_a == hash_b

    def test_list_order_still_matters(self):
        hash_a, _ = merkle_hash(["a", "b"])
        hash_b, _ = merkle_hash(["b", "a"])
        assert hash_a != hash_b

    def test_determinism(self):
        obj = {"gloss": "g", "invariants": ["i1", "i2"], "parameters": {"k": 1}}
        assert merkle_hash(obj) == merkle_hash(obj)


class TestDependencyAliasCanonicalization:
    def test_single_alias_keyed_by_handle(self):
        deps = {"references": {"base": "TargetHandle#abc1"}}
        canon = canonicalize_dependency_keys(deps)
        assert canon == {"references": {"targethandle": "TargetHandle#abc1"}}

    def test_multiple_aliases_to_same_handle_all_survive(self):
        """v1 kept exactly one of these (insertion-order-dependent)."""
        deps = {"references": {"gate_in": "Gate#aa11", "gate_out": "Gate#bb22"}}
        canon = canonicalize_dependency_keys(deps)
        assert canon == {"references": {"gate": ["Gate#aa11", "Gate#bb22"]}}

    def test_multi_alias_canonical_form_is_insertion_order_independent(self):
        forward = {"references": {"x": "Gate#aa11", "y": "Gate#bb22"}}
        backward = {"references": {"y": "Gate#bb22", "x": "Gate#aa11"}}
        assert canonicalize_dependency_keys(forward) == canonicalize_dependency_keys(backward)

    def test_arity_changes_the_hash(self):
        """One reference to Gate vs two references to Gate must differ."""
        base = {"handle": "P", "mechanism": "m", "gloss": "g"}
        lookup = {"Gate": "f" * 64}.get
        one = generate_sema_hash({**base, "dependencies": {"references": {"gate": "Gate"}}}, lookup)
        two = generate_sema_hash(
            {**base, "dependencies": {"references": {"a": "Gate", "b": "Gate"}}}, lookup
        )
        assert one["hash"] != two["hash"]

    def test_alias_spelling_does_not_change_the_hash(self):
        base = {"handle": "P", "mechanism": "m", "gloss": "g"}
        lookup = {"Gate": "f" * 64}.get
        mine = generate_sema_hash(
            {**base, "dependencies": {"references": {"my_gate": "Gate"}}}, lookup
        )
        yours = generate_sema_hash(
            {**base, "dependencies": {"references": {"the_gate": "Gate"}}}, lookup
        )
        assert mine["hash"] == yours["hash"]

    def test_resolver_handles_multi_ref_lists(self):
        deps = canonicalize_dependency_keys({"references": {"a": "Gate#aa11", "b": "Gate#bb22"}})
        resolved = resolve_dependencies_to_sema_ids(deps, {"Gate": "e" * 64}.get)
        refs = resolved["references"]["gate"]
        assert isinstance(refs, list) and len(refs) == 2
        assert all(r == f"sema:Gate#mh:SHA-256:{'e' * 64}" for r in refs)
