import json
import os
from collections import defaultdict

VOCAB_DIR = "data/vocabulary"


def scan_stats():
    total_patterns = 0
    with_invariants = 0
    with_preconditions = 0
    with_postconditions = 0
    with_typed_io = 0
    with_parameters = 0
    total_parameters = 0
    that_compose = 0
    tier_counts = defaultdict(int)

    for filename in os.listdir(VOCAB_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(VOCAB_DIR, filename)) as f:
                try:
                    data = json.load(f)
                    total_patterns += 1

                    if data.get("invariants"):
                        with_invariants += 1

                    if data.get("preconditions"):
                        with_preconditions += 1

                    if data.get("postconditions"):
                        with_postconditions += 1

                    # Typed I/O: has accepts/yields keys in dependencies OR top level
                    deps = data.get("dependencies", {})
                    if (
                        data.get("accepts")
                        or data.get("yields")
                        or deps.get("accepts")
                        or deps.get("yields")
                    ):
                        with_typed_io += 1

                    params = data.get("parameters", [])
                    if params:
                        with_parameters += 1
                        total_parameters += len(params)

                    # Composes: has composes_with in dependencies
                    if deps.get("composes_with"):
                        that_compose += 1

                    # Tier counting
                    meta = data.get("_meta", {})
                    tier = meta.get("tier")
                    if tier is not None:
                        tier_counts[tier] += 1

                except json.JSONDecodeError:
                    pass

    print(f"Total patterns: {total_patterns}")
    print(
        f"Patterns with formal invariants: {with_invariants} "
        f"({with_invariants/total_patterns:.0%})"
    )
    print(
        f"Patterns with preconditions: {with_preconditions} "
        f"({with_preconditions/total_patterns:.0%})"
    )
    print(
        f"Patterns with postconditions: {with_postconditions} "
        f"({with_postconditions/total_patterns:.0%})"
    )
    print(f"Patterns with typed I/O: {with_typed_io} " f"({with_typed_io/total_patterns:.0%})")
    print(f"Patterns with parameters: {with_parameters} " f"({with_parameters/total_patterns:.0%})")
    print(f"Total parameters: {total_parameters}")
    print(f"Patterns that compose: {that_compose} " f"({that_compose/total_patterns:.0%})")

    print("\nTier Counts:")
    for t in sorted(tier_counts.keys()):
        print(f"Tier {t}: {tier_counts[t]}")


if __name__ == "__main__":
    scan_stats()
