"""Placeholder bindings and the pattern identity.

A card's mechanism names its dependencies by alias, as placeholders such as
``{{judge}}``, and its ``dependencies`` map binds each alias to a target. Under
canonicalization v2 the hashed form keys each dependency by its target's handle,
so the alias is dropped: the identity records which definitions a category
binds, and how many times, but not which placeholder each one fills.
"""

import copy
import itertools
import json
from graphlib import TopologicalSorter
from pathlib import Path

import pytest

from sema.core.hashing import (
    CANONICALIZATION_V2,
    CANONICALIZATION_V3,
    DEFAULT_CANONICALIZATION,
    EXPLICIT_BINDINGS_KEY,
    canonicalize_dependency_bindings,
    explicit_pairings,
    extract_handle_from_ref,
    generate_sema_hash,
    pattern_hash_from_sema_id,
    resolve_ref_to_sema_id,
    semantic_hash_input,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
VOCAB_DIR = REPO_ROOT / "data" / "vocabulary"


def _load(handle: str) -> dict:
    return json.loads((VOCAB_DIR / f"{handle}.json").read_text(encoding="utf-8"))


def _swap(card: dict, category: str, first: str, second: str) -> dict:
    """Return a copy of ``card`` with the targets of two aliases exchanged."""
    swapped = copy.deepcopy(card)
    bindings = swapped["dependencies"][category]
    bindings[first], bindings[second] = bindings[second], bindings[first]
    return swapped


class TestV2PlaceholderBindingGap:
    """The gap, as released: v2 cannot see an exchange of two targets."""

    def test_exchanging_judge_and_check_keeps_the_v2_identity(self):
        card = _load("SteelmanCheck")
        swapped = _swap(card, "composes_with", "judge", "check")

        # The swap is a real change of meaning: the mechanism now invokes Check
        # to score the counter-argument and Judge to test robustness.
        assert "{{judge}} to score" in card["mechanism"]
        assert "{{check}} to test" in card["mechanism"]
        assert swapped["dependencies"] != card["dependencies"]

        original = generate_sema_hash(card, canonicalization=CANONICALIZATION_V2)
        exchanged = generate_sema_hash(swapped, canonicalization=CANONICALIZATION_V2)

        assert exchanged["full_id"] == original["full_id"]


# ---------------------------------------------------------------------------
# Canonicalization v3: a pairing is implied when the alias names its own
# target, and hashed explicitly otherwise.
# ---------------------------------------------------------------------------


def _library() -> dict[str, dict]:
    cards = {}
    for path in sorted(VOCAB_DIR.glob("*.json")):
        card = json.loads(path.read_text(encoding="utf-8"))
        cards[card["handle"]] = card
    return cards


def _targets(card: dict, handles) -> set[str]:
    """Handles a card pins: dependency targets and its specialization parent."""
    found = set()
    for items in (card.get("dependencies") or {}).values():
        if isinstance(items, dict):
            found |= {
                extract_handle_from_ref(ref) for ref in items.values() if isinstance(ref, str)
            }
    if isinstance(card.get("extends"), str):
        found.add(extract_handle_from_ref(card["extends"]))
    return found & handles


def _migrate(cards: dict[str, dict], version: int) -> dict[str, str]:
    """Every card's digest under ``version``, computed in dependency order in memory."""
    handles = cards.keys()
    order = TopologicalSorter({h: _targets(c, handles) for h, c in cards.items()})
    digests: dict[str, str] = {}
    for handle in order.static_order():
        card = copy.deepcopy(cards[handle])
        if isinstance(card.get("extends"), str):
            card["extends"] = resolve_ref_to_sema_id(card["extends"], digests.get)
        digests[handle] = generate_sema_hash(card, digests.get, canonicalization=version)["hash"]
    return digests


@pytest.fixture(scope="module")
def library() -> dict[str, dict]:
    return _library()


@pytest.fixture(scope="module")
def v3_digests(library) -> dict[str, str]:
    return _migrate(library, CANONICALIZATION_V3)


@pytest.fixture(scope="module")
def v2_digests(library) -> dict[str, str]:
    return _migrate(library, CANONICALIZATION_V2)


class TestTheLibraryUnderV3:
    def test_v3_is_the_default(self):
        assert DEFAULT_CANONICALIZATION == CANONICALIZATION_V3

    def test_the_library_recomputes_byte_for_byte(self, library):
        stored = {
            h: pattern_hash_from_sema_id(c["sema_id"], expected_handle=h)
            for h, c in library.items()
        }
        for handle, card in library.items():
            assert generate_sema_hash(card, stored.get)["full_id"] == card["sema_id"], handle

    def test_v2_still_yields_each_card_s_previous_identity(self, library, v2_digests):
        """Regeneration changed the canonicalization only, never a card's content.

        Under v2 a card that kept its identity recomputes to it, and a card whose
        identity changed recomputes to the one it supersedes.
        """
        for handle, card in library.items():
            stored = pattern_hash_from_sema_id(card["sema_id"], expected_handle=handle)
            if v2_digests[handle] == stored:
                continue
            previous = (card.get("_meta") or {}).get("supersedes", [])[-1:]
            assert previous, handle
            assert v2_digests[handle] == pattern_hash_from_sema_id(
                previous[0], expected_handle=handle
            ), handle


class TestV3OnTheLibrary:
    def test_exchanging_judge_and_check_changes_the_v3_identity(self, library, v3_digests):
        card = library["SteelmanCheck"]
        swapped = _swap(card, "composes_with", "judge", "check")

        original = generate_sema_hash(card, v3_digests.get, canonicalization=CANONICALIZATION_V3)
        exchanged = generate_sema_hash(
            swapped, v3_digests.get, canonicalization=CANONICALIZATION_V3
        )

        assert original["full_id"] == card["sema_id"]  # all its pairings are implied
        assert exchanged["full_id"] != original["full_id"]

    def test_only_role_named_cards_and_their_dependents_change(
        self, library, v2_digests, v3_digests
    ):
        handles = library.keys()
        role_named = {
            h for h, c in library.items() if explicit_pairings(c.get("dependencies") or {})
        }
        dependents: dict[str, set[str]] = {}
        for h, c in library.items():
            for target in _targets(c, handles):
                dependents.setdefault(target, set()).add(h)
        expected, todo = set(role_named), list(role_named)
        while todo:
            for d in dependents.get(todo.pop(), ()):
                if d not in expected:
                    expected.add(d)
                    todo.append(d)

        changed = {h for h in library if v3_digests[h] != v2_digests[h]}
        assert changed == expected
        assert role_named and len(changed) < len(library)


TARGETS = {
    "Gate": "a" * 64,
    "Lock": "b" * 64,
    "Check": "c" * 64,
    "Vector": "d" * 64,
    "Base": "e" * 64,
}


def _probe() -> dict:
    return {
        "handle": "Probe",
        "mechanism": "The {{check}} opens the {{gate}}, holds the {{lock}} and reads the {{weights}}.",
        "gloss": "g",
        "dependencies": {
            "composes_with": {"gate": "Gate", "lock": "Lock", "weights": "Vector"},
            "references": {"check": "Check"},
        },
    }


def _hash(card: dict, version: int, targets: dict[str, str] = TARGETS) -> str:
    return generate_sema_hash(card, targets.get, canonicalization=version)["hash"]


def _mutations():
    def retarget(c):
        c["dependencies"]["composes_with"]["lock"] = "Check"

    def add(c):
        c["dependencies"]["references"]["base"] = "Base"

    def remove(c):
        del c["dependencies"]["composes_with"]["lock"]

    def move_category(c):
        c["dependencies"]["references"]["lock"] = c["dependencies"]["composes_with"].pop("lock")

    def arity(c):
        c["dependencies"]["composes_with"]["second_gate"] = "Gate"

    def retarget_role(c):
        c["dependencies"]["composes_with"]["weights"] = "Base"

    def text(c):
        c["mechanism"] = c["mechanism"].replace("holds", "releases")

    return [retarget, add, remove, move_category, arity, retarget_role, text]


class TestV3Bindings:
    @pytest.mark.parametrize(
        "first,second", [("gate", "lock"), ("gate", "weights")], ids=["implied", "mixed"]
    )
    def test_exchanged_targets_change_v3_only(self, first, second):
        card = _probe()
        swapped = _swap(card, "composes_with", first, second)
        if second == "lock":
            assert _hash(swapped, 2) == _hash(card, 2)  # the v2 gap
        assert _hash(swapped, 3) != _hash(card, 3)

    @pytest.mark.parametrize("mutate", _mutations(), ids=lambda f: f.__name__)
    def test_every_change_v2_detects_v3_detects(self, mutate):
        card = _probe()
        changed = copy.deepcopy(card)
        mutate(changed)
        assert _hash(changed, 2) != _hash(card, 2)
        assert _hash(changed, 3) != _hash(card, 3)

    @pytest.mark.parametrize("version", [CANONICALIZATION_V2, CANONICALIZATION_V3])
    def test_a_changed_target_or_parent_changes_both(self, version):
        card = _probe()
        assert _hash(card, version, {**TARGETS, "Gate": "f" * 64}) != _hash(card, version)
        parent = {**card, "extends": f"sema:Base#mh:SHA-256:{'e' * 64}"}
        other = {**card, "extends": f"sema:Base#mh:SHA-256:{'f' * 64}"}
        assert _hash(parent, version) != _hash(other, version)

    def test_self_naming_pairings_hash_as_in_v2(self):
        card = _probe()
        del card["dependencies"]["composes_with"]["weights"]
        card["mechanism"] = "The {{check}} opens the {{gate}} and holds the {{lock}}."
        v2 = semantic_hash_input(card, TARGETS.get)
        v3 = semantic_hash_input(card, TARGETS.get, canonicalization=CANONICALIZATION_V3)
        assert v3 == v2
        assert _hash(card, 3) == _hash(card, 2)

    def test_role_named_pairings_are_hashed_explicitly(self):
        content = semantic_hash_input(_probe(), TARGETS.get, canonicalization=CANONICALIZATION_V3)
        category = content["dependencies"]["composes_with"]
        assert category[EXPLICIT_BINDINGS_KEY] == {"weights": f"sema:Vector#mh:SHA-256:{'d' * 64}"}
        assert "vector" not in category
        assert _hash(_probe(), 3) != _hash(_probe(), 2)

    def test_folding_ignores_case_underscores_and_hyphens(self):
        items = {"ontology_handshake": "OntologyHandshake#aaaa", "state-lock": "StateLock#bbbb"}
        assert explicit_pairings({"references": items}) == set()

    def test_folding_touches_ascii_only(self):
        """The Kelvin sign lower-cases to ``k`` in Unicode; the fold leaves it alone.

        As an alias it never gets this far: NFC turns it into ``K``, so
        ``canonicalize_dependency_bindings`` refuses it as not normalized.
        """
        assert explicit_pairings({"references": {"\u212aey": "Key#aaaa"}}) == {
            ("references", "\u212aey")
        }
        assert explicit_pairings({"references": {"key": "\u212aey#aaaa"}}) == {
            ("references", "key")
        }

    def test_a_malformed_handle_is_never_implied(self):
        for ref in ("9lives#aaaa", "", "#aaaa", "@bindings"):
            alias = ref.split("#")[0]
            assert explicit_pairings({"references": {alias: ref}}) == {("references", alias)}, ref

    def test_handles_that_fold_alike_are_hashed_explicitly(self):
        """Two targets whose handles fold alike could otherwise be exchanged unseen."""
        targets = {"Gate": "a" * 64, "Ga_te": "b" * 64}
        card = {
            "handle": "Probe",
            "mechanism": "Uses {{gate}} and {{ga_te}}.",
            "gloss": "g",
            "dependencies": {"composes_with": {"gate": "Gate", "ga_te": "Ga_te"}},
        }
        swapped = _swap(card, "composes_with", "gate", "ga_te")
        assert explicit_pairings(card["dependencies"]) == {
            ("composes_with", "gate"),
            ("composes_with", "ga_te"),
        }
        assert _hash(swapped, 2, targets) == _hash(card, 2, targets)
        assert _hash(swapped, 3, targets) != _hash(card, 3, targets)

    def test_aliases_of_one_handle_pinning_different_versions(self):
        """Two self-naming aliases of one handle, pinned to different versions."""
        card = {
            "handle": "Probe",
            "mechanism": "Compares {{gate}} with {{ga_te}}.",
            "gloss": "g",
            "dependencies": {
                "composes_with": {
                    "gate": f"sema:Gate#mh:SHA-256:{'a' * 64}",
                    "ga_te": f"sema:Gate#mh:SHA-256:{'b' * 64}",
                }
            },
        }
        swapped = _swap(card, "composes_with", "gate", "ga_te")
        assert explicit_pairings(card["dependencies"]) == {
            ("composes_with", "gate"),
            ("composes_with", "ga_te"),
        }
        v2 = CANONICALIZATION_V2
        assert (
            generate_sema_hash(swapped, canonicalization=v2)["hash"]
            == generate_sema_hash(card, canonicalization=v2)["hash"]
        )
        v3 = generate_sema_hash(card, canonicalization=CANONICALIZATION_V3)["hash"]
        v3_swapped = generate_sema_hash(swapped, canonicalization=CANONICALIZATION_V3)["hash"]
        assert v3_swapped != v3

    @pytest.mark.parametrize(
        "second",
        [f"sema:Ga_te#mh:SHA-256:{'b' * 64}", f"sema:Gate#mh:SHA-256:{'b' * 64}"],
        ids=["handles-folding-alike", "one-handle-two-pins"],
    )
    def test_names_that_fold_alike_in_different_categories(self, second):
        """Placeholders are not scoped to a category, so neither is the rule.

        Two names that fold alike, each naming its own target in its own
        category, could be exchanged across the categories with both pairings
        still implied if the rule looked at one category at a time.
        """
        first = f"sema:Gate#mh:SHA-256:{'a' * 64}"
        card = {
            "handle": "Probe",
            "mechanism": "Opens {{gate}} and closes {{ga_te}}.",
            "gloss": "g",
            "dependencies": {"composes_with": {"gate": first}, "references": {"ga_te": second}},
        }
        exchanged = copy.deepcopy(card)
        exchanged["dependencies"] = {
            "composes_with": {"ga_te": first},
            "references": {"gate": second},
        }
        assert explicit_pairings(card["dependencies"]) == {
            ("composes_with", "gate"),
            ("references", "ga_te"),
        }
        v2 = [
            generate_sema_hash(c, canonicalization=CANONICALIZATION_V2)["hash"]
            for c in (card, exchanged)
        ]
        v3 = [
            generate_sema_hash(c, canonicalization=CANONICALIZATION_V3)["hash"]
            for c in (card, exchanged)
        ]
        assert v2[0] == v2[1]
        assert v3[0] != v3[1]

    def test_one_name_in_two_categories_stays_implied(self):
        """The same name is one name: nothing else in the text could take its place."""
        card = {
            "handle": "Probe",
            "mechanism": "Takes a {{gate}} and returns it.",
            "gloss": "g",
            "dependencies": {"accepts": {"gate": "Gate"}, "yields": {"gate": "Gate"}},
        }
        assert explicit_pairings(card["dependencies"]) == set()
        assert _hash(card, 3) == _hash(card, 2)

    def test_non_string_dependency_values_are_refused(self):
        card = _probe()
        card["dependencies"]["composes_with"]["gate"] = 5
        with pytest.raises(ValueError, match="must be a reference string"):
            generate_sema_hash(card, canonicalization=CANONICALIZATION_V3)

    def test_non_string_aliases_are_refused(self):
        card = _probe()
        card["dependencies"]["composes_with"][5] = "Gate"
        with pytest.raises(ValueError, match="must be a string"):
            generate_sema_hash(card, canonicalization=CANONICALIZATION_V3)

    @pytest.mark.parametrize(
        "alias",
        ["judge ", " judge", "ju  dge", "judge\u00a0", "e\u0301"],
        ids=["trailing", "leading", "doubled", "no-break", "not-nfc"],
    )
    def test_an_alias_that_normalization_would_change_is_refused(self, alias):
        """The Merkle hash normalizes object keys, so it would read another name."""
        card = _probe()
        card["dependencies"]["references"][alias] = "Base"
        with pytest.raises(ValueError, match="not a normalized string"):
            generate_sema_hash(card, canonicalization=CANONICALIZATION_V3)
        generate_sema_hash(card, canonicalization=CANONICALIZATION_V2)  # v2 is unchanged

    def test_a_name_and_its_padded_spelling_cannot_stand_in_for_each_other(self):
        """``judge `` would be hashed as ``judge``, a name the pairing rule did not see.

        Each pair below shared a digest while binding ``judge``, as the hash
        reads it, to different definitions.
        """
        pairs = [
            (
                {"accepts": {"j_udge": "Judge#1", "judge ": "Other#2"}},
                {"accepts": {"judge": "Judge#1", "judge ": "Other#2"}},
            ),
            (
                {"accepts": {"judge": "Judge"}, "references": {"judge ": "Judge"}},
                {"accepts": {"j_udge": "Judge"}, "references": {"judge ": "Judge"}},
            ),
        ]
        for dependencies in (d for pair in pairs for d in pair):
            card = {"handle": "Probe", "mechanism": "m", "gloss": "g", "dependencies": dependencies}
            with pytest.raises(ValueError, match="not a normalized string"):
                generate_sema_hash(card, canonicalization=CANONICALIZATION_V3)

    @pytest.mark.parametrize("category", ["Judge#1", ["Judge#1"], None, 5], ids=repr)
    def test_a_category_that_is_not_an_object_is_hashed_as_in_v2(self, category):
        card = _probe()
        del card["dependencies"]["composes_with"]["weights"]
        card["mechanism"] = "The {{check}} opens the {{gate}} and holds the {{lock}}."
        card["dependencies"]["accepts"] = category
        assert _hash(card, 3) == _hash(card, 2)

    def test_several_aliases_to_one_target(self):
        """Exchanging aliases of one target changes nothing; their number still counts."""
        card = {
            "handle": "Probe",
            "mechanism": "Compares {{gate}} with {{entry_gate}} and {{exit_gate}}.",
            "gloss": "g",
            "dependencies": {
                "composes_with": {"gate": "Gate", "entry_gate": "Gate", "exit_gate": "Gate"}
            },
        }
        content = semantic_hash_input(card, TARGETS.get, canonicalization=CANONICALIZATION_V3)
        gate = f"sema:Gate#mh:SHA-256:{'a' * 64}"
        assert content["dependencies"]["composes_with"] == {
            "gate": gate,
            EXPLICIT_BINDINGS_KEY: {"entry_gate": gate, "exit_gate": gate},
        }
        swapped = _swap(card, "composes_with", "entry_gate", "exit_gate")
        assert _hash(swapped, 3) == _hash(card, 3)
        fewer = copy.deepcopy(card)
        del fewer["dependencies"]["composes_with"]["exit_gate"]
        fewer["mechanism"] = "Compares {{gate}} with {{entry_gate}}."
        assert _hash(fewer, 3) != _hash(card, 3)

    def test_an_alias_spelled_like_the_reserved_key_is_explicit(self):
        """An implied key begins with a letter, so the reserved key is never one."""
        assert not EXPLICIT_BINDINGS_KEY[0].isalpha()
        card = _probe()
        card["dependencies"]["composes_with"][EXPLICIT_BINDINGS_KEY] = "Gate"
        content = semantic_hash_input(card, TARGETS.get, canonicalization=CANONICALIZATION_V3)
        bound = content["dependencies"]["composes_with"][EXPLICIT_BINDINGS_KEY]
        assert EXPLICIT_BINDINGS_KEY in bound and "weights" in bound
        assert _hash(card, 3) != _hash(_probe(), 3)

    def test_shared_names_are_bound_alike_whenever_two_forms_coincide(self):
        """Exhaustive on a small universe: every dependency map over three names
        (two folding alike), three references (two to one handle) and two
        categories. Whenever two maps share a hashed form, every name both
        declare is bound in both to the same references in the same categories.
        """
        names = ["gate", "ga_te", "lock"]
        refs = [
            f"sema:Gate#mh:SHA-256:{'a' * 64}",
            f"sema:Gate#mh:SHA-256:{'b' * 64}",
            f"sema:Lock#mh:SHA-256:{'c' * 64}",
        ]
        slots = [(category, name) for category in ("composes_with", "references") for name in names]
        by_form: dict[str, list[dict]] = {}
        for choice in itertools.product([None, *refs], repeat=len(slots)):
            deps: dict[str, dict[str, str]] = {}
            for (category, name), ref in zip(slots, choice, strict=True):
                if ref is not None:
                    deps.setdefault(category, {})[name] = ref
            form = json.dumps(canonicalize_dependency_bindings(deps), sort_keys=True)
            by_form.setdefault(form, []).append(deps)

        def bindings(deps, name):
            return {(category, items[name]) for category, items in deps.items() if name in items}

        for maps in by_form.values():
            for first, second in itertools.combinations(maps, 2):
                shared = {n for items in first.values() for n in items} & {
                    n for items in second.values() for n in items
                }
                for name in shared:
                    assert bindings(first, name) == bindings(second, name), (first, second)

    @pytest.mark.parametrize("bad", [1, 4, "3", 3.0, True, None])
    def test_unknown_canonicalization_fails_closed(self, bad):
        with pytest.raises(ValueError, match="Unsupported canonicalization"):
            generate_sema_hash(_probe(), canonicalization=bad)
