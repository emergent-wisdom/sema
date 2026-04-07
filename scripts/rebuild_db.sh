#!/bin/bash
# Rebuild the taxonomy database from vocabulary files using sema apply
#
# Usage: ./rebuild_db.sh [--dry-run] [--check]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DB_PATH="$PROJECT_ROOT/data/taxonomy.db"
VOCAB_DIR="$PROJECT_ROOT/data/vocabulary"

cd "$PROJECT_ROOT"

# Use python module directly
SEMA_CMD="PYTHONPATH=src python3 -m sema.cli.main"

echo "=== Sema Database Rebuild ==="
echo "DB: $DB_PATH"
echo "Vocabulary: $VOCAB_DIR"
echo ""

# Count patterns
PATTERN_COUNT=$(ls -1 "$VOCAB_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')
echo "Found $PATTERN_COUNT patterns in vocabulary"

if [ "$1" == "--dry-run" ]; then
    echo ""
    echo "DRY RUN - would rebuild with:"
    echo "  1. Backup: $DB_PATH -> $DB_PATH.bak"
    echo "  2. Delete: $DB_PATH"
    echo "  3. Apply: sema apply --add $VOCAB_DIR"
    exit 0
fi

if [ "$1" == "--check" ]; then
    echo ""
    echo "Checking vocabulary validity..."
    eval "$SEMA_CMD apply --check --add $VOCAB_DIR"
    exit $?
fi

# Backup existing DB
if [ -f "$DB_PATH" ]; then
    echo ""
    echo "Backing up existing database..."
    cp "$DB_PATH" "$DB_PATH.bak"
    echo "  Backup: $DB_PATH.bak"

    echo "Removing old database..."
    rm "$DB_PATH"
fi

# Rebuild using sema apply
echo ""
echo "Rebuilding database with sema apply..."
echo ""

eval "$SEMA_CMD apply --add $VOCAB_DIR"

echo ""
echo "=== Rebuild Complete ==="
