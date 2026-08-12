#!/usr/bin/env bash
#
# Full release dance — run after pyproject.toml + CHANGELOG are merged to main.
#
# Phases (each gated by a confirmation prompt):
#   1. Pre-flight  — on main, clean tree, up-to-date, tests green, sync script
#                    reports no drift.
#   2. Tag + push  — git tag vX.Y.Z, push to origin.
#   3. GitHub release — publish a draft containing the verified bootstrap
#                      artifacts (triggers publish.yml → PyPI + MCP Registry).
#   4. Verify      — print the URLs to confirm everything landed.
#
# Version is read from pyproject.toml (single source of truth). Release notes
# body is auto-extracted from the matching CHANGELOG.md section.
#
# Usage:
#   scripts/release.sh            # interactive (prompts before each step)
#   scripts/release.sh --yes      # skip prompts (CI / trusted-caller mode)
#   scripts/release.sh --dry-run  # show what would happen, execute nothing

set -euo pipefail

# ── Args ──────────────────────────────────────────────────────────────────
YES=0
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        -y|--yes) YES=1 ;;
        -n|--dry-run) DRY_RUN=1 ;;
        -h|--help)
            sed -n '3,19p' "$0" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *)
            echo "Unknown arg: $arg" >&2
            exit 2 ;;
    esac
done

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# ── Helpers ───────────────────────────────────────────────────────────────
bold() { printf '\033[1m%s\033[0m\n' "$*"; }
fail() { printf '\033[31m❌ %s\033[0m\n' "$*" >&2; exit 1; }
ok()   { printf '\033[32m✓\033[0m %s\n' "$*"; }
run()  {
    if [[ $DRY_RUN -eq 1 ]]; then
        printf '  (dry-run) %s\n' "$*"
    else
        eval "$@"
    fi
}
confirm() {
    local prompt="$1"
    if [[ $YES -eq 1 || $DRY_RUN -eq 1 ]]; then
        return 0
    fi
    read -r -p "$prompt [y/N] " reply
    [[ "$reply" =~ ^[Yy]$ ]] || fail "Aborted."
}

# ── Phase 1: Pre-flight ───────────────────────────────────────────────────
bold "▸ Pre-flight checks"

branch="$(git rev-parse --abbrev-ref HEAD)"
[[ "$branch" == "main" ]] || fail "Not on main (on $branch). Merge to main first."
ok "on main"

if ! git diff --quiet || ! git diff --cached --quiet; then
    fail "Working tree is dirty. Commit or stash first."
fi
ok "clean working tree"

git fetch --quiet origin main
local_sha="$(git rev-parse HEAD)"
remote_sha="$(git rev-parse origin/main)"
[[ "$local_sha" == "$remote_sha" ]] || fail "Local main not up to date with origin/main."
ok "up to date with origin/main"

if ! python3 scripts/sync_release_metadata.py --check >/dev/null 2>&1; then
    fail "Release metadata out of sync. Run: python3 scripts/sync_release_metadata.py && git commit --amend --no-edit"
fi
ok "release metadata in sync"

bold "▸ Running tests"
if [[ $DRY_RUN -eq 1 ]]; then
    printf '  (dry-run) pytest\n'
else
    python3 -m pytest -q >/dev/null 2>&1 || fail "Tests failed. Fix before releasing."
fi
ok "tests green"

# ── Version + release-notes extraction ────────────────────────────────────
VERSION="$(awk -F'"' '/^version[[:space:]]*=/ { print $2; exit }' pyproject.toml)"
[[ -n "$VERSION" ]] || fail "Could not read version from pyproject.toml"
TAG="v$VERSION"
ok "version: $VERSION (tag: $TAG)"

if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
    fail "Tag $TAG already exists locally. Aborting to avoid clobber."
fi
if git ls-remote --exit-code --tags origin "$TAG" >/dev/null 2>&1; then
    fail "Tag $TAG already exists on origin. Aborting."
fi
ok "tag $TAG is unused"

# Extract the CHANGELOG section for this version. Match `## [X.Y.Z]` up to
# the next `## ` heading or `---` separator.
RELEASE_NOTES="$(
    awk -v ver="$VERSION" '
        $0 ~ "^## \\[" ver "\\]" { flag = 1; next }
        flag && /^## \[/         { exit }
        flag && /^---$/          { exit }
        flag                     { print }
    ' CHANGELOG.md
)"
if [[ -z "$(echo "$RELEASE_NOTES" | tr -d '[:space:]')" ]]; then
    fail "No CHANGELOG section found for $VERSION. Add one and retry."
fi
ok "release notes extracted from CHANGELOG.md"

# Build the public bootstrap-library assets before any tag or release is
# created. The builder verifies that the portable JSON release has exactly the
# same identities and roots as the bundled database.
RELEASE_DIR="$(mktemp -d)"
NOTES_FILE="$(mktemp)"
cleanup() {
    rm -rf "$RELEASE_DIR"
    rm -f "$NOTES_FILE"
}
trap cleanup EXIT
python3 scripts/build_bootstrap_release.py --version "$VERSION" --output-dir "$RELEASE_DIR"
BOOTSTRAP_ARCHIVE="$RELEASE_DIR/sema-bootstrap-$VERSION.zip"
[[ -f "$RELEASE_DIR/library.json" && -f "$BOOTSTRAP_ARCHIVE" ]] || \
    fail "Bootstrap release assets were not created"
ok "bootstrap library assets verified"

# ── Show plan ─────────────────────────────────────────────────────────────
echo
bold "▸ Release plan"
cat <<EOF
  Tag:           $TAG
  Remote:        origin
  PyPI:          semahash (auto via .github/workflows/publish.yml on release)
  MCP Registry:  io.github.emergent-wisdom/semahash
  Docs landing:  https://semahash.org
  Library index: library.json
  Pattern ZIP:   $(basename "$BOOTSTRAP_ARCHIVE")

  Release notes preview (first 20 lines):
$(echo "$RELEASE_NOTES" | head -20 | sed 's/^/    /')
EOF
echo

# ── Phase 2: Tag + push ───────────────────────────────────────────────────
bold "▸ Create + push tag"
confirm "Create tag $TAG and push to origin?"
run "git tag -a '$TAG' -m 'Release $TAG'"
run "git push origin '$TAG'"
ok "tag pushed"

# ── Phase 3: GitHub release ───────────────────────────────────────────────
bold "▸ Create GitHub release (triggers PyPI + MCP Registry publish)"
confirm "Create GitHub release for $TAG?"
# Use a temp file for notes so multi-line content survives shell quoting.
echo "$RELEASE_NOTES" > "$NOTES_FILE"
run "gh release create '$TAG' '$RELEASE_DIR/library.json' '$BOOTSTRAP_ARCHIVE' --draft --title '$TAG' --notes-file '$NOTES_FILE'"
run "gh release edit '$TAG' --draft=false --latest"
ok "GitHub release published with bootstrap assets — publish workflow should now be running"
echo "  Watch:  gh run list --workflow publish.yml --limit 3"

# Exercise the same stable manifest URL and version-pinned asset URL that consumers
# use. GitHub may take a few seconds to move the `latest` pointer after a draft
# is published, so retry briefly and require byte-for-byte equality with the
# artifacts verified before tagging.
bold "▸ Smoke-test public bootstrap assets"
PUBLIC_MANIFEST_URL="https://github.com/emergent-wisdom/sema/releases/latest/download/library.json"
PUBLIC_ARCHIVE_URL="https://github.com/emergent-wisdom/sema/releases/download/$TAG/$(basename "$BOOTSTRAP_ARCHIVE")"
if [[ $DRY_RUN -eq 1 ]]; then
    printf '  (dry-run) fetch and compare %s\n' "$PUBLIC_MANIFEST_URL"
    printf '  (dry-run) fetch and compare %s\n' "$PUBLIC_ARCHIVE_URL"
else
    public_manifest="$RELEASE_DIR/public-library.json"
    public_archive="$RELEASE_DIR/public-$(basename "$BOOTSTRAP_ARCHIVE")"
    public_ok=0
    for _attempt in {1..12}; do
        if curl -fsSL "$PUBLIC_MANIFEST_URL" -o "$public_manifest" \
            && curl -fsSL "$PUBLIC_ARCHIVE_URL" -o "$public_archive" \
            && cmp -s "$RELEASE_DIR/library.json" "$public_manifest" \
            && cmp -s "$BOOTSTRAP_ARCHIVE" "$public_archive"; then
            public_ok=1
            break
        fi
        sleep 5
    done
    [[ $public_ok -eq 1 ]] || fail "Published bootstrap assets failed the public URL smoke test."
fi
ok "public library.json and pattern ZIP match the verified release bytes"

# ── Phase 4: Verify ───────────────────────────────────────────────────────
echo
bold "▸ Verify (manual — give PyPI ~2 min, MCP Registry ~instant)"
cat <<EOF
  PyPI:         https://pypi.org/project/semahash/$VERSION/
  GitHub:       https://github.com/emergent-wisdom/sema/releases/tag/$TAG
  MCP Registry: https://registry.modelcontextprotocol.io/v0/servers?search=semahash
  Actions:      https://github.com/emergent-wisdom/sema/actions/workflows/publish.yml

Done — release $VERSION has left the building.
EOF
