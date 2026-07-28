#!/bin/bash
# Install Git Hooks for Sema

HOOK_DIR=$(git rev-parse --git-path hooks)
PRE_COMMIT="$HOOK_DIR/pre-commit"

echo "Installing pre-commit hook to $PRE_COMMIT..."

cat > "$PRE_COMMIT" << 'EOF'
#!/bin/bash
# Sema Pre-Commit Hook
# Calculates aggregate roots and updates docs

echo "🔄 Running Sema aggregate-root calculator..."

# Navigate to repo root
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

# Run the script
python3 scripts/vocabulary_merkle_root.py

# Add the updated docs to the commit
git add docs/information/vocabulary_information.md

echo "✅ Aggregate roots updated."
EOF

chmod +x "$PRE_COMMIT"
echo "✅ Hook installed."
