import glob
import json
import os
import re

# Repository-relative path to the canonical vocabulary.
VOCAB_DIR = "data/vocabulary"


def audit_references():
    print(f"🔍 Scanning {VOCAB_DIR} for missing links...")

    # 1. Load Registry
    registry = {}
    files = sorted(glob.glob(os.path.join(VOCAB_DIR, "*.json")))
    for fpath in files:
        with open(fpath) as f:
            data = json.load(f)
            handle = data.get("handle")
            if handle:
                registry[handle] = data

    print(f"Loaded {len(registry)} patterns.")

    # 2. Build Link Map (Who links to whom?)
    # Map: Source -> Set(Targets)
    link_map = {}

    for handle, data in registry.items():
        linked = set()

        # Check 'links'
        if "links" in data:
            for _rel, targets in data["links"].items():
                for t in targets:
                    # t is "Handle#Hash" or just "Handle"
                    t_handle = t.split("#")[0]
                    linked.add(t_handle)

        # Check 'interface'
        if "interface" in data:
            for _k, v in data["interface"].items():
                v_handle = v.split("#")[0]
                linked.add(v_handle)

        link_map[handle] = linked

    # 3. Scan Text for References
    missing_links = []

    # Common words that are also handles (False Positive Prone)
    # We will ignore these unless they appear with a #hash or specific context,
    # but for this broad sweep, we might just list them and filter output.
    # Actually, let's keep them but be skeptical.
    COMMON_WORDS = {
        "Task",
        "Vote",
        "Trace",
        "Signal",
        "Context",
        "Break",
        "Card",
        "Probe",
        "Rank",
        "Select",
        "Yield",
        "Compose",
        "Decay",
        "Rally",
        "Retry",
        "Route",
        "Warmup",
    }

    for handle, data in registry.items():
        # Aggregate all text
        text_content = (
            f"{data.get('mechanism', '')} {data.get('gloss', '')} {data.get('failure_modes', '')}"
        )
        for inv in data.get("invariants", []):
            text_content += " " + inv
        for pre in data.get("preconditions", []):
            text_content += " " + pre
        for post in data.get("postconditions", []):
            text_content += " " + post

        # Check against all other handles
        for target_handle in registry:
            if target_handle == handle:
                continue  # Self-reference is fine (or irrelevant for links)

            # Simple substring check (Case Sensitive)
            # We enforce word boundary to avoid finding "Ask" in "Task" (though Task is handle)
            # regex: \bHandle\b
            if re.search(r"\b" + re.escape(target_handle) + r"\b", text_content):
                # Check if already linked
                if target_handle not in link_map[handle]:
                    # Filter: If common word, check if it looks like a proper noun usage?
                    # Hard to do without NLP. We'll mark as "High" or "Low" confidence.
                    confidence = "High"
                    if target_handle in COMMON_WORDS:
                        confidence = "Low (Common Word)"

                    missing_links.append(
                        {
                            "source": handle,
                            "target": target_handle,
                            "confidence": confidence,
                            "snippet": "...",  # could extract context
                        }
                    )

    # 4. Report
    print(f"\nFound {len(missing_links)} potential missing links.\n")

    # Sort by Source
    missing_links.sort(key=lambda x: (x["source"], x["target"]))

    current_source = None
    for m in missing_links:
        if m["confidence"].startswith("Low"):
            continue  # Skip low confidence for the main report to reduce noise

        if m["source"] != current_source:
            print(f"🔹 {m['source']}")
            current_source = m["source"]

        print(f"   ❓ Mentions '{m['target']}' but not linked.")


if __name__ == "__main__":
    audit_references()
