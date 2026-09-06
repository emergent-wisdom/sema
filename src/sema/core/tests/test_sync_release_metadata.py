"""Regression tests for the MCP Registry's pinned launch recipe."""

import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def metadata_module(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[4] / "scripts" / "sync_release_metadata.py"
    spec = importlib.util.spec_from_file_location("sync_release_metadata", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "SERVER_JSON", tmp_path / "server.json")
    return module


def write_server_metadata(module, requirement, version="0.5.4"):
    data = {
        "name": "io.github.emergent-wisdom/semahash",
        "version": version,
        "description": "A test server.",
        "packages": [
            {
                "registryType": "pypi",
                "identifier": "semahash",
                "version": version,
                "runtimeHint": "uvx",
                "runtimeArguments": [
                    {"type": "positional", "value": "--from"},
                    {"type": "positional", "value": requirement},
                    {"type": "positional", "value": "sema"},
                ],
                "packageArguments": [{"type": "positional", "value": "mcp"}],
                "transport": {"type": "stdio"},
            }
        ],
    }
    module.SERVER_JSON.write_text(json.dumps(data, indent=2) + "\n")
    return data


@pytest.mark.parametrize("requirement", ["semahash", "semahash==0.5.4"])
def test_sync_repairs_missing_mcp_extra(metadata_module, requirement):
    expected = write_server_metadata(metadata_module, requirement)
    expected["packages"][0]["runtimeArguments"][1]["value"] = "semahash[mcp]==0.5.4"

    assert metadata_module.sync_server_json("0.5.4", 457) is True
    assert json.loads(metadata_module.SERVER_JSON.read_text()) == expected


def test_sync_repairs_stale_runtime_pin(metadata_module):
    expected = write_server_metadata(metadata_module, "semahash[mcp]==0.5.3")
    expected["packages"][0]["runtimeArguments"][1]["value"] = "semahash[mcp]==0.5.4"

    assert metadata_module.sync_server_json("0.5.4", 457) is True
    assert json.loads(metadata_module.SERVER_JSON.read_text()) == expected


def test_sync_updates_runtime_pin_with_future_release(metadata_module):
    expected = write_server_metadata(metadata_module, "semahash[mcp]==0.5.4")
    expected["version"] = "0.5.5"
    expected["packages"][0]["version"] = "0.5.5"
    expected["packages"][0]["runtimeArguments"][1]["value"] = "semahash[mcp]==0.5.5"

    assert metadata_module.sync_server_json("0.5.5", 457) is True
    assert json.loads(metadata_module.SERVER_JSON.read_text()) == expected
    assert metadata_module.sync_server_json("0.5.5", 457) is False


def test_synced_runtime_is_idempotent_without_writes(metadata_module, monkeypatch):
    write_server_metadata(metadata_module, "semahash[mcp]==0.5.4")
    before = metadata_module.SERVER_JSON.read_bytes()

    def unexpected_write(*args, **kwargs):
        pytest.fail("Already synchronized metadata must not be rewritten")

    monkeypatch.setattr(metadata_module, "_dump_json", unexpected_write)

    assert metadata_module.sync_server_json("0.5.4", 457) is False
    assert metadata_module.SERVER_JSON.read_bytes() == before
