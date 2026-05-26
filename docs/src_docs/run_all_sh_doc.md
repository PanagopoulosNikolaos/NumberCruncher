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
    TIMEFORMAT="%R"
    { time python3 "$SOLVER_ROOT/python/countdown.py" "$TARGET" $NUMBERS > "$TEMP_DIR/python_output.txt" 2>&1 ; } 2> "$TEMP_DIR/python_time.txt"
) &
```

**Implementation (Executable Logic Only):**
* **Line 0:** `TIMEFORMAT="%R"` — Configures the bash built-in `time` command format to print only elapsed real seconds.
* **Line 1:** `time python3` — Runs the solver inside a timing block.
* **Line 2:** `2> redirect` — Redirects the printed execution time from standard error to the output time file.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| python3 | External | Python execution | python |
| ghc | External | Haskell compilation | ghc |
| swipl | External | Prolog execution | swipl |
| time | Built-in | Process timing | bash |
| sed | External | Text substitutions | sed |
