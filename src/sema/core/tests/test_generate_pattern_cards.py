"""Tests for the paper's canonical pattern-card appendix generator."""

import importlib.util
import json
from pathlib import Path

import pytest


def load_generator_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "generate_pattern_cards.py"
    spec = importlib.util.spec_from_file_location("generate_pattern_cards", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_legacy_specialization_key_is_rendered_verbatim():
    generator = load_generator_module()
    legacy = {
        "handle": "LegacyChild",
        "mechanism": "A pre-0.4 card.",
        "derived_from": "sema:RetiredParent",
    }

    rendered = json.loads(generator.format_card_for_latex(legacy))

    assert rendered == {
        "mechanism": "A pre-0.4 card.",
        "derived_from": "sema:RetiredParent",
    }


def test_ambiguous_specialization_keys_fail_closed():
    generator = load_generator_module()
    pattern = {
        "handle": "Child",
        "mechanism": "A malformed card.",
        "extends": "sema:Parent#mh:SHA-256:" + ("a" * 64),
        "derived_from": None,
    }

    with pytest.raises(ValueError, match="both extends"):
        generator.format_card_for_latex(pattern)
