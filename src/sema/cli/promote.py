"""
Pattern Promotion with System 2 Validation.

Before moving from staging/ to vocabulary/, patterns must pass:
1. Cycle detection - No circular SIMULATES chains
2. Tier consistency - EdgeSimulates targets must be higher tier
3. Link integrity - All referenced patterns exist in vocabulary
4. Invariant check - Pattern's invariants are internally consistent
5. Manifest match - Declared interface matches actual structure

Only patterns that pass ALL checks can be promoted.
"""

import json
import os
import shutil
import sys
from dataclasses import dataclass, field

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.taxonomy_graph.graph_store import GraphStore


@dataclass
class ValidationResult:
    """Result of validation checks."""

    passed: bool
    checks: dict[str, bool] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class PromoteResult:
    """Result of a promotion attempt."""

    success: bool
    handle: str | None = None
    destination: str | None = None
    validation: ValidationResult | None = None
    errors: list[str] = field(default_factory=list)


class PatternPromoter:
    """
    Promotes patterns from staging to vocabulary after System 2 validation.

    The Gatekeeper: No pattern enters production vocabulary without passing
    all validation checks. This prevents graph corruption and maintains
    semantic integrity.
    """

    def __init__(
        self,
        store: GraphStore,
        staging_dir: str,
        vocab_dir: str,
        verbose: bool = False,
        force: bool = False,
    ):
        self.store = store
        self.staging_dir = staging_dir
        self.vocab_dir = vocab_dir
        self.verbose = verbose
        self.force = force  # Skip validation (dangerous!)

    def promote(self, handle: str) -> PromoteResult:
        """
        Promote a pattern from staging to vocabulary.

        Returns PromoteResult with success/failure details.
        """
        filename = f"{handle}.json"
        src_path = os.path.join(self.staging_dir, filename)
        dst_path = os.path.join(self.vocab_dir, filename)

        # Check source exists
        if not os.path.exists(src_path):
            return PromoteResult(
                success=False,
                handle=handle,
                errors=[f"Pattern '{handle}' not found in staging ({self.staging_dir})"],
            )

        # Load pattern
        try:
            with open(src_path, encoding="utf-8") as f:
                pattern = json.load(f)
        except json.JSONDecodeError as e:
            return PromoteResult(
                success=False, handle=handle, errors=[f"Invalid JSON in staging file: {e}"]
            )

        # Run validation (unless --force)
        if not self.force:
            validation = self.validate(pattern)

            if not validation.passed:
                return PromoteResult(
                    success=False, handle=handle, validation=validation, errors=validation.errors
                )
        else:
            validation = ValidationResult(passed=True)
            validation.warnings.append("Validation skipped (--force)")

        # Move to production vocabulary
        os.makedirs(self.vocab_dir, exist_ok=True)
        shutil.move(src_path, dst_path)

        return PromoteResult(
            success=True, handle=handle, destination=dst_path, validation=validation
        )

    def validate(self, pattern: dict) -> ValidationResult:
        """
        Run all System 2 validation checks.

        All checks must pass for validation to succeed.
        """
        result = ValidationResult(passed=True)
        handle = pattern.get("handle", "Unknown")

        if self.verbose:
            print(f"Running System 2 checks for '{handle}'...")

        # Check 1: Tier Consistency
        tier_ok, tier_errors = self._check_tier_consistency(pattern)
        result.checks["tier_consistency"] = tier_ok
        if not tier_ok:
            result.passed = False
            result.errors.extend(tier_errors)
        elif self.verbose:
            print("  [1/5] Tier consistency: PASSED")

        # Check 2: Cycle Detection
        cycle_ok, cycle_errors = self._check_no_cycles(pattern)
        result.checks["no_cycles"] = cycle_ok
        if not cycle_ok:
            result.passed = False
            result.errors.extend(cycle_errors)
        elif self.verbose:
            print("  [2/5] Cycle detection: PASSED")

        # Check 3: Link Integrity
        links_ok, link_errors = self._check_link_integrity(pattern)
        result.checks["link_integrity"] = links_ok
        if not links_ok:
            result.passed = False
            result.errors.extend(link_errors)
        elif self.verbose:
            print("  [3/5] Link integrity: PASSED")

        # Check 4: Invariant Consistency
        inv_ok, inv_errors = self._check_invariants(pattern)
        result.checks["invariant_consistency"] = inv_ok
        if not inv_ok:
            result.passed = False
            result.errors.extend(inv_errors)
        elif self.verbose:
            print("  [4/5] Invariant consistency: PASSED")

        # Check 5: Manifest Match (interface declaration)
        manifest_ok, manifest_errors = self._check_manifest(pattern)
        result.checks["manifest_match"] = manifest_ok
        if not manifest_ok:
            result.passed = False
            result.errors.extend(manifest_errors)
        elif self.verbose:
            print("  [5/5] Manifest match: PASSED")

        return result

    def _check_tier_consistency(self, pattern: dict) -> tuple[bool, list[str]]:
        """
        EdgeSimulates targets must be higher tier than source.

        Tier ordering: 1 (Ironclad) < 2 (Stable) < 3 (Experimental)
        A Tier 2 pattern can SIMULATES a Tier 3, but not vice versa.
        """
        errors = []
        my_tier = pattern.get("tier") or 1  # Default to Tier 1 if not specified

        links = pattern.get("links", {})
        simulates_targets = links.get("SIMULATES", [])

        for target in simulates_targets:
            target_handle = target.split("#")[0]
            target_pattern = self._load_vocab_pattern(target_handle)

            if target_pattern:
                target_tier = target_pattern.get("tier") or 1

                # SIMULATES must go UP in tier (more rigorous)
                if target_tier <= my_tier:
                    errors.append(
                        f"Tier violation: '{pattern['handle']}' (Tier {my_tier}) "
                        f"SIMULATES '{target_handle}' (Tier {target_tier}). "
                        f"Target must be higher tier for increased rigor."
                    )

        return len(errors) == 0, errors

    def _check_no_cycles(self, pattern: dict) -> tuple[bool, list[str]]:
        """
        Detect circular dependencies in SIMULATES chains.

        A pattern cannot transitively SIMULATES itself.
        """
        errors = []
        handle = pattern.get("handle")

        visited: set[str] = set()
        stack: list[str] = [handle]

        while stack:
            current = stack.pop()

            if current in visited:
                if current == handle:
                    errors.append(f"Cycle detected: '{handle}' transitively SIMULATES itself")
                    break
                continue

            visited.add(current)

            # Get SIMULATES targets for current node
            current_pattern = self._load_vocab_pattern(current)
            if current_pattern:
                targets = current_pattern.get("links", {}).get("SIMULATES", [])
                for target in targets:
                    target_handle = target.split("#")[0]
                    if target_handle == handle:
                        errors.append(
                            f"Cycle detected: '{current}' SIMULATES '{handle}' "
                            f"which creates a circular dependency"
                        )
                    else:
                        stack.append(target_handle)

        return len(errors) == 0, errors

    def _check_link_integrity(self, pattern: dict) -> tuple[bool, list[str]]:
        """
        All referenced patterns must exist in vocabulary (not just staging).
        """
        errors = []

        for _rel_type, targets in pattern.get("links", {}).items():
            for target in targets:
                target_handle = target.split("#")[0]

                # Must exist in vocabulary (production)
                vocab_path = os.path.join(self.vocab_dir, f"{target_handle}.json")
                if not os.path.exists(vocab_path):
                    errors.append(
                        f"Link target '{target_handle}' not found in vocabulary. "
                        f"Promote it first, or remove the link."
                    )

        return len(errors) == 0, errors

    def _check_invariants(self, pattern: dict) -> tuple[bool, list[str]]:
        """
        Basic invariant consistency check.

        Currently checks:
        - Invariants are non-empty strings
        - No duplicate invariants
        """
        errors = []
        invariants = pattern.get("invariants", [])

        seen = set()
        for i, inv in enumerate(invariants):
            if not inv or not inv.strip():
                errors.append(f"Invariant {i + 1} is empty")
            elif inv in seen:
                errors.append(f"Duplicate invariant: '{inv[:50]}...'")
            else:
                seen.add(inv)

        return len(errors) == 0, errors

    def _check_manifest(self, pattern: dict) -> tuple[bool, list[str]]:
        """
        Check that declared interface matches actual structure.

        If pattern declares an interface (subject, payload, output),
        verify those patterns exist.
        """
        errors = []
        interface = pattern.get("interface", {})

        for role, target_handle in interface.items():
            if target_handle:
                vocab_path = os.path.join(self.vocab_dir, f"{target_handle}.json")
                if not os.path.exists(vocab_path):
                    errors.append(f"Interface {role}='{target_handle}' not found in vocabulary")

        return len(errors) == 0, errors

    def _load_vocab_pattern(self, handle: str) -> dict | None:
        """Load a pattern from vocabulary directory."""
        path = os.path.join(self.vocab_dir, f"{handle}.json")
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None


def promote_pattern(
    handle: str,
    store: GraphStore,
    staging_dir: str,
    vocab_dir: str,
    verbose: bool = False,
    force: bool = False,
) -> PromoteResult:
    """Convenience function to promote a pattern."""
    promoter = PatternPromoter(
        store=store, staging_dir=staging_dir, vocab_dir=vocab_dir, verbose=verbose, force=force
    )
    return promoter.promote(handle)


def list_staged(staging_dir: str) -> list[str]:
    """List all patterns in staging directory."""
    if not os.path.exists(staging_dir):
        return []

    patterns = []
    for f in os.listdir(staging_dir):
        if f.endswith(".json"):
            patterns.append(f[:-5])  # Remove .json extension

    return sorted(patterns)
