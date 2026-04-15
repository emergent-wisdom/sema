#!/usr/bin/env bash
# Integration test: multi-DB system in a clean venv
# Run from repo root: bash tests/integration/test_multi_db.sh
set -e

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="/tmp/sema-integration-test"
PROJECT_DB="/tmp/sema-test-project.db"
CUSTOM_DB="/tmp/sema-test-custom.db"
EMPTY_DB="/tmp/sema-test-empty.db"
PATTERNS_FILE="/tmp/sema-test-patterns.txt"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

pass() { echo -e "${GREEN}PASS${NC}: $1"; }
fail() { echo -e "${RED}FAIL${NC}: $1"; exit 1; }

# Cleanup
cleanup() {
    rm -rf "$VENV" "$PROJECT_DB" "$CUSTOM_DB" "$EMPTY_DB" "$PATTERNS_FILE"
}
trap cleanup EXIT
cleanup

echo "Building wheel..."
cd "$REPO_ROOT"
rm -f dist/*.whl
uv build --wheel 2>&1 | tail -1

WHEEL=$(ls dist/semahash-*.whl | head -1)
echo "Wheel: $WHEEL"
echo ""

echo "Creating fresh venv..."
python3.12 -m venv "$VENV"
SEMA="$VENV/bin/sema"
PY="$VENV/bin/python3.12"
"$VENV/bin/pip" install "${WHEEL}[mcp]" -q 2>&1 | tail -1

echo ""
echo "=== TEST 1: Version ==="
V=$($SEMA --version 2>&1)
echo "$V"
[[ "$V" == *"semahash"* ]] && pass "Version works" || fail "Version broken"

echo ""
echo "=== TEST 2: Bundled DB works ==="
OUT=$($SEMA search "consensus" 2>&1 | head -1)
echo "$OUT"
[[ "$OUT" == *"Search"* ]] && pass "Search works" || fail "Search broken"

echo ""
echo "=== TEST 3: Caution flags present ==="
CAUTION=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager()
c = sum(1 for d in r.registry.values() if d.get('_meta', {}).get('caution'))
print(c)
")
echo "Caution flags: $CAUTION"
[[ "$CAUTION" -ge 28 ]] && pass "Caution flags present" || fail "Caution flags missing"

echo ""
echo "=== TEST 4: Build full preset ==="
$SEMA build "$PROJECT_DB" --preset full 2>&1
[[ -f "$PROJECT_DB" ]] && pass "Full DB created" || fail "Full DB not created"

echo ""
echo "=== TEST 5: Project DB works ==="
OUT=$(SEMA_DB_PATH="$PROJECT_DB" $SEMA search "consensus" 2>&1 | head -1)
echo "$OUT"
[[ "$OUT" == *"Search"* ]] && pass "Project DB search works" || fail "Project DB broken"

echo ""
echo "=== TEST 6: Build standard preset ==="
rm "$PROJECT_DB"
$SEMA build "$PROJECT_DB" --preset standard 2>&1
COUNT=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager(db_path='$PROJECT_DB')
print(r.count())
")
echo "Standard patterns: $COUNT"
[[ "$COUNT" -gt 300 && "$COUNT" -lt 453 ]] && pass "Standard is subset" || fail "Standard count wrong: $COUNT"

echo ""
echo "=== TEST 7: Build from custom file ==="
printf "ChainOfThought\nVote\nConsensus\n" > "$PATTERNS_FILE"
$SEMA build "$CUSTOM_DB" --from "$PATTERNS_FILE" 2>&1
COUNT=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager(db_path='$CUSTOM_DB')
print(r.count())
")
echo "Custom patterns: $COUNT (3 requested + deps)"
[[ "$COUNT" -gt 3 ]] && pass "Dependencies resolved" || fail "No deps resolved"

echo ""
echo "=== TEST 8: Build with SEMA_DB_PATH pointing to empty DB ==="
$SEMA build "$EMPTY_DB" --preset empty 2>&1
rm "$CUSTOM_DB"
SEMA_DB_PATH="$EMPTY_DB" $SEMA build "$CUSTOM_DB" --preset standard 2>&1
COUNT=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager(db_path='$CUSTOM_DB')
print(r.count())
")
echo "Built from empty env: $COUNT patterns"
[[ "$COUNT" -gt 300 ]] && pass "Build ignores SEMA_DB_PATH" || fail "Build read from SEMA_DB_PATH"

echo ""
echo "=== TEST 9: Mint into project DB ==="
SEMA_DB_PATH="$PROJECT_DB" $PY -c "
import os; os.environ['SEMA_DB_PATH'] = '$PROJECT_DB'
import json
from importlib import reload
import sema.mcp.server as s; reload(s)
r = json.loads(s._sema_mint(json.dumps({
    'handle': 'TestMintedPattern',
    'mechanism': 'A test pattern.',
    'gloss': 'Test',
    '_meta': {'layer': 'Mind', 'category': 'Reasoning', 'ring': 2, 'tier': 3}
})))
print('Minted:', r.get('success'))
"
FOUND=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager(db_path='$PROJECT_DB')
print('TestMintedPattern' in r.registry)
")
[[ "$FOUND" == "True" ]] && pass "Mint into project DB works" || fail "Mint failed"

echo ""
echo "=== TEST 10: Pip upgrade does NOT affect project DB ==="
"$VENV/bin/pip" install "${WHEEL}[mcp]" --force-reinstall -q 2>&1 | tail -1
FOUND=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager(db_path='$PROJECT_DB')
print('TestMintedPattern' in r.registry)
")
[[ "$FOUND" == "True" ]] && pass "Project DB survives upgrade" || fail "Project DB lost data"

echo ""
echo "=== TEST 11: MCP tools work with project DB ==="
SEMA_DB_PATH="$PROJECT_DB" $PY -c "
import os, json; os.environ['SEMA_DB_PATH'] = '$PROJECT_DB'
from importlib import reload
import sema.mcp.server as s; reload(s)
stats = json.loads(s.sema_stats())
print(f'MCP stats: {stats[\"total_patterns\"]} patterns')
results = json.loads(s.sema_search('consensus'))
print(f'MCP search: {len(results)} results')
"
pass "MCP tools work with project DB"

echo ""
echo "=== TEST 12: sema use switches DB ==="
$SEMA use "$PROJECT_DB" 2>&1
ACTIVE=$($SEMA use 2>&1)
echo "$ACTIVE"
[[ "$ACTIVE" == *"$PROJECT_DB"* ]] && pass "sema use switches DB" || fail "sema use broken"

echo ""
echo "=== TEST 13: Commands use the switched DB ==="
COUNT=$($PY -c "
from sema.core.registry import RegistryManager, get_default_db_path
r = RegistryManager(db_path=get_default_db_path())
print(r.count())
")
echo "Patterns via switched DB: $COUNT"
[[ "$COUNT" -gt 390 ]] && pass "Switched DB is active" || fail "Switched DB not active"

echo ""
echo "=== TEST 14: sema use --default resets ==="
$SEMA use --default 2>&1
ACTIVE=$($SEMA use 2>&1)
echo "$ACTIVE"
[[ "$ACTIVE" == *"bundled"* || "$ACTIVE" == *"site-packages"* || "$ACTIVE" == *"data/taxonomy"* ]] && pass "Reset to default" || fail "Reset broken: $ACTIVE"

echo ""
echo "=== TEST 15: Mint blocked on bundled DB ==="
MINT_RESULT=$($PY -c "
import json
from sema.mcp.server import _sema_mint
r = json.loads(_sema_mint(json.dumps({
    'handle': 'ShouldFail',
    'mechanism': 'test',
    'gloss': 'test',
    '_meta': {'layer': 'Mind', 'category': 'Reasoning', 'ring': 2, 'tier': 3}
})))
print(r.get('success', 'error'))
")
echo "Mint on bundled: $MINT_RESULT"
[[ "$MINT_RESULT" == "False" ]] && pass "Mint blocked on bundled DB" || fail "Mint should be blocked"

echo ""
echo "=== TEST 16: sema use rejects nonexistent path ==="
OUT=$($SEMA use /tmp/does_not_exist.db 2>&1)
echo "$OUT"
[[ "$OUT" == *"not found"* ]] && pass "Rejects nonexistent path" || fail "Accepted nonexistent path"

echo ""
echo "=== TEST 17: sema use rejects bundled DB ==="
BUNDLED=$($PY -c "from sema.core.registry import get_bundled_db_path; print(get_bundled_db_path())")
OUT=$($SEMA use "$BUNDLED" 2>&1)
echo "$OUT"
[[ "$OUT" == *"Cannot"* || "$OUT" == *"overwritten"* ]] && pass "Rejects bundled DB" || fail "Accepted bundled DB"

echo ""
echo "=== TEST 18: Build refuses existing file ==="
OUT=$($SEMA build "$PROJECT_DB" --preset full 2>&1)
echo "$OUT"
[[ "$OUT" == *"already exists"* ]] && pass "Refuses existing file" || fail "Overwrote existing file"

echo ""
echo "=== TEST 19: Default user reads bundled without sema use ==="
# Clear any active_db config
rm -f ~/.config/sema/active_db
COUNT=$($PY -c "
from sema.core.registry import RegistryManager, get_default_db_path, is_bundled_db
path = get_default_db_path()
print(f'{is_bundled_db(path)}|{RegistryManager(db_path=path).count()}')
")
IS_BUNDLED=$(echo "$COUNT" | cut -d'|' -f1)
PCOUNT=$(echo "$COUNT" | cut -d'|' -f2)
echo "Bundled: $IS_BUNDLED, Patterns: $PCOUNT"
[[ "$IS_BUNDLED" == "True" && "$PCOUNT" -ge 453 ]] && pass "Default is bundled DB" || fail "Default not bundled"

echo ""
echo "=== TEST 20: Mint blocked on bundled, works on project ==="
# Block on bundled
$SEMA use --default 2>&1 > /dev/null
BLOCKED=$($PY -c "
import json
from sema.mcp.server import _sema_mint
r = json.loads(_sema_mint(json.dumps({
    'handle': 'BlockTest', 'mechanism': 'test', 'gloss': 'test',
    '_meta': {'layer': 'Mind', 'category': 'Reasoning', 'ring': 2, 'tier': 3}
})))
print(r.get('success'))
")
# Allow on project
$SEMA use "$PROJECT_DB" 2>&1 > /dev/null
ALLOWED=$($PY -c "
import os, json; os.environ['SEMA_DB_PATH'] = '$PROJECT_DB'
from importlib import reload
import sema.mcp.server as s; reload(s)
r = json.loads(s._sema_mint(json.dumps({
    'handle': 'AllowTest', 'mechanism': 'test', 'gloss': 'test',
    '_meta': {'layer': 'Mind', 'category': 'Reasoning', 'ring': 2, 'tier': 3}
})))
print(r.get('success'))
")
echo "Bundled mint: $BLOCKED, Project mint: $ALLOWED"
[[ "$BLOCKED" == "False" && "$ALLOWED" == "True" ]] && pass "Mint correctly gated" || fail "Mint gating broken"

echo ""
echo "=== TEST 21: sema list shows known DBs ==="
OUT=$($SEMA list 2>&1)
echo "$OUT"
[[ "$OUT" == *"default"* ]] && pass "sema list shows default" || fail "sema list broken"
[[ "$OUT" == *"sema-test-project"* || "$OUT" == *"project"* ]] && pass "sema list shows built DB" || fail "Built DB not in list"
[[ "$OUT" == *"453 patterns"* ]] && pass "sema list shows correct default count" || fail "Default count wrong"
[[ "$OUT" == *"0 patterns"* ]] && pass "sema list shows correct empty count" || fail "Empty count wrong"

echo ""
echo "=== TEST 22: sema list marks active DB ==="
$SEMA use "$PROJECT_DB" 2>&1 > /dev/null
OUT=$($SEMA list 2>&1)
echo "$OUT"
# Active DB should have the arrow marker
[[ "$OUT" == *"→"*"$PROJECT_DB"* || "$OUT" == *"→"*"project"* ]] && pass "Active DB marked" || fail "Active not marked"
$SEMA use --default 2>&1 > /dev/null

echo ""
echo "=== TEST 23: Full workflow — build, use, mint, switch, verify ==="
# Build a fresh DB
rm -f /tmp/sema-workflow-test.db
$SEMA build /tmp/sema-workflow-test.db --preset full 2>&1
# Switch to it
$SEMA use /tmp/sema-workflow-test.db 2>&1
# Mint into it
SEMA_DB_PATH=/tmp/sema-workflow-test.db $PY -c "
import os, json; os.environ['SEMA_DB_PATH'] = '/tmp/sema-workflow-test.db'
from importlib import reload
import sema.mcp.server as s; reload(s)
r = json.loads(s._sema_mint(json.dumps({
    'handle': 'WorkflowTest',
    'mechanism': 'Full workflow test pattern.',
    'gloss': 'Workflow test',
    '_meta': {'layer': 'Mind', 'category': 'Reasoning', 'ring': 2, 'tier': 3}
})))
print('Mint:', r.get('success'))
"
# Switch to default
$SEMA use --default 2>&1
# Verify minted pattern NOT in default
DEFAULT_HAS=$($PY -c "
from sema.core.registry import RegistryManager, get_default_db_path
r = RegistryManager(db_path=get_default_db_path())
print('WorkflowTest' in r.registry)
")
# Switch back — verify minted pattern IS there
$SEMA use /tmp/sema-workflow-test.db 2>&1
PROJECT_HAS=$($PY -c "
from sema.core.registry import RegistryManager
r = RegistryManager(db_path='/tmp/sema-workflow-test.db')
print('WorkflowTest' in r.registry)
")
echo "Default has WorkflowTest: $DEFAULT_HAS"
echo "Project has WorkflowTest: $PROJECT_HAS"
[[ "$DEFAULT_HAS" == "False" && "$PROJECT_HAS" == "True" ]] && pass "Full workflow correct" || fail "Workflow broken"
rm -f /tmp/sema-workflow-test.db
$SEMA use --default 2>&1 > /dev/null

echo ""
echo "==========================================="
echo -e "${GREEN}All tests passed!${NC}"
echo "==========================================="
