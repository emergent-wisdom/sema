"""Tests for doc ref rewriting, including deliberately-historical refs.

Regression cover: the rewriter had no way to tell a stale citation from a ref
cited precisely because it is not current. docs/specification/versioning.md
illustrates stub divergence by contrasting a superseded version with the one that
replaced it, and the rewriter overwrote both sides with the current stub — so the
two examples ended up quoting the same stub twice, which is unreadable as an
illustration of stubs differing.
"""

import importlib.util
from pathlib import Path


def load_module():
    repo_root = Path(__file__).resolve().parents[4]
    script = repo_root / "scripts" / "update_doc_refs.py"
    spec = importlib.util.spec_from_file_location("update_doc_refs", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CURRENT = {"PropheticQuorum": "91f6", "Lock": "abcd"}


def test_stale_refs_are_rewritten():
    mod = load_module()
    text = "See `PropheticQuorum#912b` and `Lock#0000`.\n"

    new_text, changes = mod.rewrite_doc(Path("docs/guide.md"), text, CURRENT)

    assert "PropheticQuorum#91f6" in new_text
    assert "Lock#abcd" in new_text
    assert sorted(c[0] for c in changes) == ["Lock", "PropheticQuorum"]


def test_pinned_region_is_left_alone():
    mod = load_module()
    text = (
        f"{mod.PIN_OPEN}\n"
        "Agents pinned to `PropheticQuorum#912b` still resolve it, even though\n"
        "`PropheticQuorum#91f6` has superseded it.\n"
        f"{mod.PIN_CLOSE}\n"
    )

    new_text, changes = mod.rewrite_doc(Path("docs/specification/versioning.md"), text, CURRENT)

    assert new_text == text
    assert changes == []
    # The whole point: the two stubs stay different.
    assert "PropheticQuorum#912b" in new_text
    assert "PropheticQuorum#91f6" in new_text


def test_refs_outside_a_pin_are_still_rewritten_in_the_same_file():
    """One pinned example must not freeze the rest of the document."""
    mod = load_module()
    text = (
        "Intro cites `Lock#0000`.\n"
        f"{mod.PIN_OPEN}\n"
        "Historical: `PropheticQuorum#912b`.\n"
        f"{mod.PIN_CLOSE}\n"
        "Outro cites `PropheticQuorum#0000`.\n"
    )

    new_text, changes = mod.rewrite_doc(Path("docs/specification/versioning.md"), text, CURRENT)

    assert "Historical: `PropheticQuorum#912b`" in new_text
    assert "Intro cites `Lock#abcd`" in new_text
    assert "Outro cites `PropheticQuorum#91f6`" in new_text
    assert len(changes) == 2


def test_generated_manual_supersedes_blocks_still_preserved():
    mod = load_module()
    text = (
        "**Supersedes (prior versions).**\n"
        "- `PropheticQuorum#912b`\n"
        "\n"
        "Body cites `PropheticQuorum#0000`.\n"
    )

    new_text, changes = mod.rewrite_doc(mod.GENERATED_MANUAL, text, CURRENT)

    assert "- `PropheticQuorum#912b`" in new_text
    assert "Body cites `PropheticQuorum#91f6`" in new_text
    assert len(changes) == 1


def test_the_shipped_versioning_spec_keeps_two_distinct_stubs():
    """Guards the actual file, not just the mechanism."""
    mod = load_module()
    repo_root = Path(__file__).resolve().parents[4]
    spec_doc = repo_root / "docs" / "specification" / "versioning.md"
    text = spec_doc.read_text()

    new_text, _ = mod.rewrite_doc(spec_doc, text, mod.load_current_stubs())

    assert new_text == text, "refreshing doc refs must not alter the versioning spec's examples"
    for section in ("semantics across versions", "Short stubs identify versions"):
        assert section in new_text
    # Both illustrations contrast a superseded stub with the current one.
    assert "PropheticQuorum#912b" in new_text
    assert "PropheticQuorum#91f6" in new_text
