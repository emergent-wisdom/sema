#!/bin/bash
# Install Git Hooks for Sema

HOOK_DIR=$(git rev-parse --git-path hooks)
PRE_COMMIT="$HOOK_DIR/pre-commit"

echo "Installing pre-commit hook to $PRE_COMMIT..."

cat > "$PRE_COMMIT" << 'EOF'
#!/bin/bash
# Sema Pre-Commit Hook
# Calculates Merkle Root and updates docs

echo "🔄 Running Sema Merkle Root Calculator..."

# Navigate to repo root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Run the script
python3 scripts/vocabulary_merkle_root.py
python3 scripts/export/export_short_hand.py

# Add the updated docs to the commit
git add docs/information/vocabulary_information.md
git add data/shorthand/all_patterns_short.md

echo "✅ Merkle Root & Reference updated."
EOF

chmod +x "$PRE_COMMIT"
echo "✅ Hook installed."
