#!/bin/bash
# Orchestrates all three Countdown solvers (Python, Haskell, Prolog) concurrently.
# Usage: ./run_all.sh <target> <n1> <n2> ... <nk>
#
# Produces separate output files for each solver that runner.py reads.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMP_DIR="/tmp/countdown_results"

rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <target> <n1> <n2> ... <nk>"
    exit 1
fi

TARGET="$1"
shift
NUMBERS="$*"

# Build the Prolog argument string
PROLOG_LIST="[$(echo "$NUMBERS" | sed 's/ /,/g')]"

# Launch all three solvers concurrently, timing each one
(
    START=$(date +%s%N)
    python3 "$PROJECT_ROOT/src/python/countdown.py" "$TARGET" $NUMBERS > "$TEMP_DIR/python_output.txt" 2>&1
    END=$(date +%s%N)
    ELAPSED=$(echo "scale=3; ($END - $START) / 1000000000" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/python_time.txt"
) &

# Compiles Haskell if needed
HS_BIN="$PROJECT_ROOT/src/haskell/countdown"
if [ ! -f "$HS_BIN" ] || [ "$PROJECT_ROOT/src/haskell/countdown.hs" -nt "$HS_BIN" ]; then
    ghc -o "$HS_BIN" "$PROJECT_ROOT/src/haskell/countdown.hs" -O2 2>/dev/null
fi

(
    START=$(date +%s%N)
    "$HS_BIN" "$TARGET" $NUMBERS > "$TEMP_DIR/haskell_output.txt" 2>&1
    END=$(date +%s%N)
    ELAPSED=$(echo "scale=3; ($END - $START) / 1000000000" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/haskell_time.txt"
) &

(
    START=$(date +%s%N)
    swipl -s "$PROJECT_ROOT/src/prolog/countdown.pl" -g "main($TARGET, $PROLOG_LIST), halt." > "$TEMP_DIR/prolog_output.txt" 2>&1
    END=$(date +%s%N)
    ELAPSED=$(echo "scale=3; ($END - $START) / 1000000000" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/prolog_time.txt"
) &

# Wait for all solvers to finish
wait
