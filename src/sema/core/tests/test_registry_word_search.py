"""Keyword search matches each meaningful query word, not only the whole query."""

import json
import sqlite3

import pytest

from sema.core.registry import RegistryManager


def _registry(tmp_path, patterns):
    database = tmp_path / "taxonomy.db"
    connection = sqlite3.connect(database)
    connection.execute(
        "CREATE TABLE nodes (id TEXT PRIMARY KEY, text TEXT NOT NULL, metadata TEXT NOT NULL,"
        " node_type TEXT NOT NULL, embedding BLOB)"
    )
    connection.execute(
        "CREATE TABLE edges (id TEXT PRIMARY KEY, source_id TEXT, target_id TEXT,"
        " edge_type TEXT, alias TEXT)"
    )
    for handle, gloss, layer, category in patterns:
        pattern = {
            "handle": handle,
            "sema_ref": f"{handle}#0000",
            "gloss": gloss,
            "mechanism": "",
            "sema_layer": layer,
            "sema_category": category,
        }
        connection.execute(
            "INSERT INTO nodes VALUES (?, ?, ?, 'PATTERN', NULL)",
            (f"node-{handle}", handle, json.dumps({"pattern": pattern})),
        )
    connection.commit()
    connection.close()
    return RegistryManager(vocab_dir=tmp_path / "vocabulary", db_path=str(database))


def _handles(results):
    return [r["handle"] for r in results]


@pytest.fixture
def registry(tmp_path):
    return _registry(
        tmp_path,
        [
            ("Shrink", "Reduce a failing input to the smallest case", "Mind", "Strategy"),
            ("Compress", "Make a message smaller", "Infrastructure", "Primitives"),
            ("Break", "Stop a loop", "Infrastructure", "Primitives"),
            ("CircuitBreaker", "Stop calls to a failing service", "Infrastructure", "Primitives"),
            ("Unrelated", "Something else entirely", "Society", "Protocols"),
        ],
    )


def test_a_question_finds_the_pattern_holding_its_words(registry):
    results = registry.search("make a failing test case smaller", use_semantic=False)

    assert _handles(results)[0] == "Shrink"
    assert "Unrelated" not in _handles(results)


def test_suffixes_are_stripped_on_both_sides(registry):
    results = registry.search("shrinking inputs", use_semantic=False)

    assert _handles(results)[0] == "Shrink"


def test_a_whole_name_beats_a_name_that_contains_it(registry):
    assert _handles(registry.search("Break", use_semantic=False))[0] == "Break"
    assert _handles(registry.search("circuit breaker", use_semantic=False))[0] == "CircuitBreaker"


def test_rare_words_count_more_than_common_ones(tmp_path):
    common = [(f"Common{i}", "a failing step", "Mind", "Strategy") for i in range(20)]
    registry = _registry(tmp_path, common + [("Rare", "an idempotent write", "Mind", "Strategy")])

    results = registry.search("idempotent failing", use_semantic=False)

    assert _handles(results)[0] == "Rare"


def test_word_matches_respect_the_scope(registry):
    results = registry.search("failing smaller", use_semantic=False, category="Primitives")

    assert set(_handles(results)) <= {"Compress", "Break", "CircuitBreaker"}
    assert "Shrink" not in _handles(results)


def test_word_matches_are_capped(tmp_path):
    many = [(f"Pattern{i}", "a failing step", "Mind", "Strategy") for i in range(80)]
    registry = _registry(tmp_path, many)

    assert len(registry.search("failing step", use_semantic=False)) == 50
