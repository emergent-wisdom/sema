"""Current-schema coverage for the missing-field audit."""

import json

from sema.audit import missing_or_short


def write_pattern(directory, meta):
    pattern = {
        "handle": "Example",
        "gloss": "Example pattern",
        "mechanism": "A sufficiently detailed mechanism for the audit length threshold.",
        "_meta": meta,
    }
    (directory / "Example.json").write_text(json.dumps(pattern))


def test_current_path_metadata_passes(monkeypatch, tmp_path, capsys):
    write_pattern(tmp_path, {"path": ["Mind", "Reasoning"], "ring": 0, "tier": 1})
    monkeypatch.setattr(missing_or_short, "INVENTORY_DIR", str(tmp_path))

    missing_or_short.audit_patterns()

    assert "No issues found" in capsys.readouterr().out


def test_legacy_layer_category_metadata_reports_missing_path(monkeypatch, tmp_path, capsys):
    write_pattern(tmp_path, {"layer": "Mind", "category": "Reasoning", "ring": 0, "tier": 1})
    monkeypatch.setattr(missing_or_short, "INVENTORY_DIR", str(tmp_path))

    missing_or_short.audit_patterns()

    output = capsys.readouterr().out
    assert "Missing: _meta.path" in output
    assert "_meta.layer" not in output
    assert "_meta.category" not in output
