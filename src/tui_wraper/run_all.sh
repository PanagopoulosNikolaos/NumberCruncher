#!/bin/bash
# Orchestrates all three Countdown solvers (Python, Haskell, Prolog) concurrently.
# Usage: ./run_all.sh <target> <n1> <n2> ... <nk>
#
# Produces separate output files for each solver that runner.py reads.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Resolve the solver source directory relative to the script location.
SOLVER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

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

# Compiles Haskell if needed in a user-writable cache directory to avoid permission issues.
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/numbercruncher"
mkdir -p "$CACHE_DIR"
HS_BIN="$CACHE_DIR/countdown"
if [ ! -f "$HS_BIN" ] || [ "$SOLVER_ROOT/haskell/countdown.hs" -nt "$HS_BIN" ]; then
    ghc -o "$HS_BIN" -odir "$CACHE_DIR" -hidir "$CACHE_DIR" "$SOLVER_ROOT/haskell/countdown.hs" -O2 2>/dev/null
fi

# Launch all three solvers concurrently, timing each one using high-precision EPOCHREALTIME.
(
    START=$EPOCHREALTIME
    python3 "$SOLVER_ROOT/python/countdown.py" "$TARGET" $NUMBERS > "$TEMP_DIR/python_output.txt" 2>&1
    END=$EPOCHREALTIME
    ELAPSED=$(echo "scale=3; $END - $START" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/python_time.txt"
) &

(
    START=$EPOCHREALTIME
    "$HS_BIN" "$TARGET" $NUMBERS > "$TEMP_DIR/haskell_output.txt" 2>&1
    END=$EPOCHREALTIME
    ELAPSED=$(echo "scale=3; $END - $START" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/haskell_time.txt"
) &

(
    START=$EPOCHREALTIME
    swipl -s "$SOLVER_ROOT/prolog/countdown.pl" -g "main($TARGET, $PROLOG_LIST), halt." > "$TEMP_DIR/prolog_output.txt" 2>&1
    END=$EPOCHREALTIME
    ELAPSED=$(echo "scale=3; $END - $START" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/prolog_time.txt"
) &

# Wait for all solvers to finish
wait
