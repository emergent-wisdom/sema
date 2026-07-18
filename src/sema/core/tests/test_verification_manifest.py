"""Keep the machine-readable proof manifest connected to checked artifacts."""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
MANIFEST_PATH = REPO_ROOT / "verification" / "proof-manifest.json"
LEAN_ROOT = REPO_ROOT / "verification" / "lean"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_uses_pinned_project_toolchain():
    manifest = load_manifest()
    pinned_toolchain = (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()

    assert manifest["format"] == "sema-proof-manifest/v1"
    assert manifest["verifier"]["toolchain"] == pinned_toolchain


def test_manifest_references_existing_artifacts_and_theorems():
    manifest = load_manifest()

    for proof in manifest["proofs"]:
        model = REPO_ROOT / proof["model"]
        implementation = REPO_ROOT / proof["implementation"]
        conformance_file = proof["conformance_test"].split("::", 1)[0]
        conformance_test = REPO_ROOT / conformance_file

        assert model.is_file(), proof["id"]
        assert implementation.is_file(), proof["id"]
        assert conformance_test.is_file(), proof["id"]

        model_source = model.read_text(encoding="utf-8")
        for theorem in proof["theorems"]:
            assert re.search(rf"\btheorem\s+{re.escape(theorem)}\b", model_source), (
                proof["id"],
                theorem,
            )


def test_lean_proofs_contain_no_placeholders_or_custom_axioms():
    forbidden = re.compile(r"\b(sorry|admit|axiom)\b")

    for lean_file in LEAN_ROOT.rglob("*.lean"):
        assert not forbidden.search(lean_file.read_text(encoding="utf-8")), lean_file
