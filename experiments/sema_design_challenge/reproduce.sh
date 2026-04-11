#!/bin/bash
set -e

# Change to script directory
cd "$(dirname "$0")"

# ---- CONFIGURATION ----
SWARM_DIR="$(cd "$(dirname "$0")/../orchestrator" && pwd)"

if [ ! -d "$SWARM_DIR/src/swarm" ]; then
    echo "ERROR: orchestrator not found at $SWARM_DIR"
    exit 1
fi

# Setup Environment
export PYTHONPATH=$PYTHONPATH:$SWARM_DIR/src
export PYTHONUNBUFFERED=1
# Load .env if present
if [ -f "$(dirname "$0")/.env" ]; then
    set -a; source "$(dirname "$0")/.env"; set +a
elif [ -f "$(dirname "$0")/../../.env" ]; then
    set -a; source "$(dirname "$0")/../../.env"; set +a
fi

export MODEL="${MODEL:-gemini-3.1-flash-lite-preview}"

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "ERROR: GOOGLE_API_KEY not set (set it or add to .env)"
    exit 1
fi

PY="${PYTHON:-python3}"

# --- BATCH SETUP ---
# Create a single timestamped folder for this entire batch run
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BATCH_DIR="traces/run_${TIMESTAMP}"
mkdir -p "$BATCH_DIR"

# --- TRAP SETUP ---
# Function to kill child processes on exit/interrupt
cleanup() {
    echo ""
    echo "🛑 INTERRUPT RECEIVED! Killing all background experiments..."
    kill 0
    wait
    exit 1
}

trap cleanup SIGINT SIGTERM
# ------------------

echo "========================================================"
echo "🧪 SEMA DESIGN CHALLENGE (PARALLEL)"
echo "========================================================"
echo "Starting all 3 conditions in parallel..."
echo "Batch Directory: $BATCH_DIR"
echo "--------------------------------------------------------"

# Run Condition A
# Logs go to the batch dir immediately
echo ">>> [A] Started: Natural Language"
$PY "$SWARM_DIR/run_experiment.py" \
    --scenario natural_language.yaml \
    --turns 100 \
    --output-dir "$BATCH_DIR" \
    --subdir-name "A_Natural_Language" \
    > "$BATCH_DIR/A.log" 2>&1 &
PID_A=$!

# Run Condition B
echo ">>> [B] Started: Sema Only"
$PY "$SWARM_DIR/run_experiment.py" \
    --scenario design_challenge.yaml \
    --turns 100 \
    --output-dir "$BATCH_DIR" \
    --subdir-name "B_Sema_Only" \
    > "$BATCH_DIR/B.log" 2>&1 &
PID_B=$!

# Run Condition C
echo ">>> [C] Started: Optimistic"
$PY "$SWARM_DIR/run_experiment.py" \
    --scenario optimistic.yaml \
    --turns 100 \
    --output-dir "$BATCH_DIR" \
    --subdir-name "C_Optimistic" \
    > "$BATCH_DIR/C.log" 2>&1 &
PID_C=$!

# Wait for all
echo ">>> Running... Logs are in $BATCH_DIR/"
echo "    (e.g., tail -f $BATCH_DIR/A.log)"
wait $PID_A $PID_B $PID_C

echo "========================================================"
echo "✅ EXPERIMENTS COMPLETE. CLEANING UP..."

# Move the logs INTO their respective subfolders for perfect containment
mv "$BATCH_DIR/A.log" "$BATCH_DIR/A_Natural_Language/console.log"
mv "$BATCH_DIR/B.log" "$BATCH_DIR/B_Sema_Only/console.log"
mv "$BATCH_DIR/C.log" "$BATCH_DIR/C_Optimistic/console.log"

echo "Results archived in: $BATCH_DIR"
echo "========================================================"
