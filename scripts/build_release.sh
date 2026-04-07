#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=== Sema Release Build ==="
echo ""

# 1. Build web frontend
echo "Building web frontend..."
cd web
npm install --silent
npm run build
echo "Copying frontend to server static..."
rm -rf ../src/sema/server/static/assets ../src/sema/server/static/index.html ../src/sema/server/static/favicon.svg
cp -r dist/* ../src/sema/server/static/
cd "$PROJECT_ROOT"
echo "  ✓ Frontend built"
echo ""

# 2. Regenerate paper
echo "Regenerating paper assets..."
python3 scripts/generate_paper_tables.py
python3 scripts/generate_pattern_cards.py
python3 scripts/update_paper_hashes.py
python3 scripts/calculate_graph_stats.py
echo "  ✓ Paper assets regenerated"
echo ""

# 3. Compile paper
echo "Compiling PDF..."
cd paper
pdflatex -interaction=nonstopmode sema.tex > /dev/null 2>&1 || true
bibtex sema > /dev/null 2>&1 || true
pdflatex -interaction=nonstopmode sema.tex > /dev/null 2>&1 || true
pdflatex -interaction=nonstopmode sema.tex > /dev/null 2>&1 || true
cd "$PROJECT_ROOT"
echo "  ✓ PDF compiled"
echo ""

# 4. Build Python package
echo "Building Python package..."
python3 -m build
echo "  ✓ Package built"
echo ""

echo "=== Build Complete ==="
echo ""
echo "Artifacts:"
echo "  Frontend:  src/sema/server/static/"
echo "  Paper:     paper/sema.pdf"
echo "  Package:   dist/"
echo ""
echo "To publish to PyPI:"
echo "  twine upload dist/*"
