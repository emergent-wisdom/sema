#!/usr/bin/env bash
# Pre-commit gate: fail if pyproject.toml `version = ...` changed
# but CHANGELOG.md is not also staged in the same commit.
#
# Wired into .pre-commit-config.yaml as the "changelog-gate" hook
# (fires only when pyproject.toml is staged).

set -euo pipefail

# Does the staged diff on pyproject.toml touch the version line?
if ! git diff --cached --unified=0 pyproject.toml 2>/dev/null \
    | grep -qE '^[-+]version[[:space:]]*='; then
    # No version change; nothing to gate.
    exit 0
fi

# Version changed — CHANGELOG.md must also be staged.
if git diff --cached --name-only | grep -qx 'CHANGELOG.md'; then
    exit 0
fi

cat <<'EOF'

❌ changelog-gate: pyproject.toml version changed but CHANGELOG.md was
   NOT updated in the same commit.

   Add an entry under ## [Unreleased] describing the changes, then:
     git add CHANGELOG.md
   and retry the commit.

EOF
exit 1
