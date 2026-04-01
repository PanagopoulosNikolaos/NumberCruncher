# run_all.sh Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [PROJECT_ROOT](#PROJECT_ROOT) | Variable | Absolute path to the main project directory. |
| [TEMP_DIR](#TEMP_DIR) | Variable | Directory for storing intermediate output files. |
| [PROLOG_LIST](#PROLOG_LIST) | Variable | Formatted comma-separated list of inputs for SWI-Prolog. |
| [main_process](#main_process) | Workflow | Launches 3 solvers concurrently and captures output/timing. |

## Overview
This shell script acts as the primary orchestration layer for the multi-language Countdown solver. It calculates the project's root directory, manages temporary result files, prepares arguments for Prolog's syntax, and concurrently executes the Python, Haskell, and Prolog components while capturing their respective outcomes and individual execution times.

## Detailed Breakdown

### main_process

**Signature:**
```bash
./run_all.sh <target> <n1> <n2> ... <nk>
```

**Purpose:** Orchestrates concurrent multi-language solver execution.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| target | int | Yes | — | The integer to reach. |
| numbers | vargs | Yes | — | All subsequent numeric arguments for the pool. |

**Returns:**
| Type | Description |
|------|-------------|
| None | Writes `*_output.txt` and `*_time.txt` to `/tmp/countdown_results`. |

**Source Code:**
```bash
(
    START=$(date +%s%N)
    python3 "$PROJECT_ROOT/src/python/countdown.py" "$TARGET" $NUMBERS > "$TEMP_DIR/python_output.txt" 2>&1
    END=$(date +%s%N)
    ELAPSED=$(echo "scale=3; ($END - $START) / 1000000000" | bc)
    echo "$ELAPSED" > "$TEMP_DIR/python_time.txt"
) &
```

**Implementation (Executable Logic Only):**
* **Line 0:** `date +%s%N` — Captures the start time in nanoseconds.
* **Line 1:** `python3 call` — Executes the solver in the background using the `&` operator.
* **Line 2:** `echo / bc` — Calculates the elapsed time in seconds with 3 decimal places using the `bc` command.
* **Line 3:** `redirect >` — Forwards standard output and error to a temporary text file.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| python3 | External | Python execution | python |
| ghc | External | Haskell compilation | ghc |
| swipl | External | Prolog execution | swipl |
| bc | External | Floating point arithmetic | bc |
| sed | External | Text substitutions | sed |
| date | External | Time measurement | bash |
