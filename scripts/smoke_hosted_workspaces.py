#!/usr/bin/env python3
"""Smoke-test tenant-scoped workspace reads on a deployed Sema server."""

from __future__ import annotations

import argparse
import json
import string
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


class SmokeFailure(RuntimeError):
    """A deployed workspace invariant did not hold."""


def get_json(base_url: str, path: str, *, expected_status: int = 200) -> Any:
    request = Request(f"{base_url.rstrip('/')}{path}", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
            body = response.read()
    except HTTPError as exc:
        status = exc.code
        body = exc.read()
    except URLError as exc:
        raise SmokeFailure(f"Could not reach {request.full_url}: {exc.reason}") from exc

    if status != expected_status:
        preview = body.decode("utf-8", errors="replace")[:500]
        raise SmokeFailure(
            f"GET {path} returned {status}, expected {expected_status}: {preview}"
        )

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise SmokeFailure(f"GET {path} did not return JSON") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


def run(base_url: str, workspace_id: str) -> None:
    encoded_workspace = quote(workspace_id, safe="")
    prefix = f"/api/workspaces/{encoded_workspace}"

    description = get_json(base_url, prefix)
    require(description.get("workspace_id") == workspace_id, "Workspace identity changed")
    require(description.get("read_only") is True, "Hosted workspace is not read-only")
    require(description.get("pattern_count", 0) > 0, "Hosted workspace has no patterns")
    for private_field in ("db_path", "vocab_dir", "metadata"):
        require(private_field not in description, f"Workspace leaked private field: {private_field}")

    root = get_json(base_url, f"{prefix}/root")
    root_hash = root.get("hash", "")
    require(
        len(root_hash) == 64 and all(character in string.hexdigits for character in root_hash),
        "Workspace root is not a SHA-256 hash",
    )
    require(root.get("pattern_count") == description["pattern_count"], "Pattern counts differ")
    require("db_path" not in root, "Workspace root leaked its database path")

    query = urlencode({"q": "coordination"})
    results = get_json(base_url, f"{prefix}/search?{query}")
    require(isinstance(results, list) and results, "Workspace search returned no results")

    first = results[0]
    handle = first.get("handle")
    require(isinstance(handle, str) and handle, "Search result has no handle")
    pattern_ref = first.get("sema_ref") or handle
    pattern = get_json(base_url, f"{prefix}/patterns/{quote(pattern_ref, safe='')}")
    require(pattern.get("handle"), "Pattern lookup returned no pattern")

    clean_handle = handle.split("#", 1)[0]
    resolved = get_json(base_url, f"{prefix}/resolve/{quote(clean_handle, safe='')}")
    require(resolved.get("count", 0) > 0, "Pattern resolution returned an empty graph")

    missing = quote("__staging_missing_workspace__", safe="")
    missing_prefix = f"/api/workspaces/{missing}"
    for path in (
        missing_prefix,
        f"{missing_prefix}/search?{query}",
        f"{missing_prefix}/patterns/{quote(pattern_ref, safe='')}",
        f"{missing_prefix}/resolve/{quote(clean_handle, safe='')}",
        f"{missing_prefix}/root",
    ):
        response = get_json(base_url, path, expected_status=404)
        require("not found" in response.get("detail", "").lower(), f"Unexpected 404 for {path}")

    print(
        f"PASS: {base_url.rstrip('/')} workspace={workspace_id} "
        f"patterns={description['pattern_count']} root={root_hash[:16]}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="Deployed server URL, such as the Railway staging URL")
    parser.add_argument("--workspace", default="local", help="Known workspace ID (default: local)")
    args = parser.parse_args()

    try:
        run(args.base_url, args.workspace)
    except SmokeFailure as exc:
        raise SystemExit(f"FAIL: {exc}") from exc


if __name__ == "__main__":
    main()
