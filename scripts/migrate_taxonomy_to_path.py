#!/usr/bin/env python3
"""One-shot migration: _meta.layer + _meta.category → _meta.path.

Rewrites every pattern JSON under data/vocabulary/ and data/staging/ (if
present). Idempotent: skips files that already carry `_meta.path`.

Also removes the top-level `sema_layer` and `sema_category` fields,
which were computed/derived and are now reconstructible from
`_meta.path[0]` and `_meta.path[1]`. Export keeps them if needed but the
source of truth is `_meta.path`.

Does NOT touch `sema_id` or any hashed field — path lives in `_meta`,
which is excluded from `SEMANTIC_FIELDS`.
"""

import json
import sys
from pathlib import Path


def migrate_pattern(p: dict) -> tuple[dict, bool]:
    """Returns (mutated_pattern, was_changed)."""
    meta = p.get("_meta")
    if not isinstance(meta, dict):
        return p, False
    changed = False

    if "path" not in meta:
        layer = meta.pop("layer", None)
        category = meta.pop("category", None)
        if layer is None:
            # No layer means we can't migrate; skip quietly.
            return p, False
        segments = [layer]
        if category:
            segments.append(category)
        meta["path"] = segments
        changed = True
    else:
        # Already has path — ensure layer/category don't linger as stale.
        for stale_key in ("layer", "category"):
            if stale_key in meta:
                meta.pop(stale_key)
                changed = True

    # Drop top-level sema_layer / sema_category (derived, redundant).
    for stale_key in ("sema_layer", "sema_category"):
        if stale_key in p:
            p.pop(stale_key)
            changed = True

    return p, changed


def main():
    repo_root = Path(__file__).resolve().parent.parent
    targets = []
    for sub in ("data/vocabulary", "data/staging"):
        d = repo_root / sub
        if d.is_dir():
            targets.extend(sorted(d.glob("*.json")))

    if not targets:
        print("No pattern JSONs found under data/vocabulary/ or data/staging/")
        return 1

    migrated = 0
    already = 0
    skipped = 0
    for f in targets:
        try:
            raw = f.read_text()
            data = json.loads(raw)
        except Exception as e:
            print(f"  SKIP {f.name} (parse error: {e})")
            skipped += 1
            continue
        if not isinstance(data, dict) or "_meta" not in data:
            skipped += 1
            continue

        before = json.dumps(data, sort_keys=True)
        data, changed = migrate_pattern(data)
        after = json.dumps(data, sort_keys=True)

        if not changed and before == after:
            already += 1
            continue

        # Preserve the exact output shape export produces: indent=2,
        # non-ASCII preserved, trailing newline.
        f.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        migrated += 1

    print(f"Migrated:       {migrated}")
    print(f"Already done:   {already}")
    print(f"Skipped:        {skipped}")
    print(f"Total examined: {migrated + already + skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
