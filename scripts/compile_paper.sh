#!/bin/bash
set +e  # Don't exit on error — pdflatex/bibtex return non-zero on warnings

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Using project root: $PROJECT_ROOT"

# Ensure we are in the project root for python imports to work if needed
cd "$PROJECT_ROOT"

# 1. Generate Tables (outputs .tex files for \input)
echo "Generating tables..."
python3 scripts/generate_paper_tables.py

# 2. Generate Pattern Cards (outputs pattern_cards.tex for appendix)
echo "Generating pattern cards..."
python3 scripts/generate_pattern_cards.py

# 3. Update Paper Hashes
echo "Updating paper hashes..."
python3 scripts/update_paper_hashes.py

# 4. Calculate Stats (Optional)
echo "Calculating stats..."
python3 scripts/calculate_graph_stats.py

# 5. Compile Paper (pdflatex -> bibtex -> pdflatex x2)
# Clean stale aux to force fresh resolution after hash updates
echo "Compiling PDF..."
cd paper
rm -f sema.aux sema.bbl sema.blg sema.log 2>/dev/null
pdflatex -interaction=nonstopmode sema.tex > /dev/null
bibtex sema
pdflatex -interaction=nonstopmode sema.tex > /dev/null
pdflatex -interaction=nonstopmode sema.tex > /dev/null

# Verify
UNDEFINED=$(grep -c "LaTeX Warning.*undefined" sema.log 2>/dev/null || true)
if [ "$UNDEFINED" -gt 0 ] 2>/dev/null; then
    echo "WARNING: $UNDEFINED undefined references remain"
    grep "LaTeX Warning.*undefined" sema.log | head -5
else
    PAGES=$(grep 'Output written' sema.log | tail -1 | grep -o '[0-9]* pages')
    echo "Done. PDF is at paper/sema.pdf ($PAGES, 0 undefined)"
fi
