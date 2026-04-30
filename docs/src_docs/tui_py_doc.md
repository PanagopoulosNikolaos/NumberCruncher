# tui.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [parseOutput](#parseOutput) | Function | Decodes raw terminal output into structured solver results. |
| [buildSolverPanel](#buildSolverPanel) | Function | Constructs a Rich Panel for graphical UI representation. |
| [buildBenchmarkTable](#buildBenchmarkTable) | Function | Formats historical performance data into a table. |
| [runSolvers](#runSolvers) | Function | Orchestrates sub-process execution of the `run_all.sh` script. |
| [main](#main) | Function | Application entry point and interactive loop control. |

## Overview
This file provides a terminal-based graphical interface (TUI) for the Countdown solver suite. It leverages the `rich` library to present results from the Python, Haskell, and Prolog solvers in a side-by-side comparison, including performance metrics and correctness verification.

## Detailed Breakdown

### runSolvers

**Primary Library:** `subprocess`  
**Purpose:** Triggers the synchronous execution of all language-specific solvers via a shell wrapper.

#### Overview
This function locates the `run_all.sh` orchestration script relative to its own file path and executes it using the `subprocess` module. It blocks execution while displaying a status indicator in the TUI until all background solvers complete their work.

#### Signature
```python
def runSolvers(target: int, numbers: list, console: Console) -> None
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| target | int | Yes | — | The target value for the game. |
| numbers | list | Yes | — | List of available integers. |
| console | Console | Yes | — | The Rich console framework instance. |

#### Returns
| Type | Description |
|------|-------------|
| None | Results are written to temporary files by the underlying script. |

#### Raise
| Exception | Condition |
|-----------|-----------|
| subprocess.SubprocessError | If the script execution fails or is not found. |

#### Dependencies
* **Required Libraries:** `os.path`, `subprocess`
* **External Tools:** `run_all.sh` (Shell orchestrator)

#### Workflow (Executable Logic Only)

**Phase 1: Path Resolution**
* **Operation 1:** Identify the absolute directory of `tui.py`.
* **Operation 2:** Construct the path to `run_all.sh` in the same directory.

**Phase 3: Execution Loop**
* **Operation 1:** Enter a `console.status` context to show a spinner.
* **Operation 2:** Run `subprocess.run` with the target and number list passed as arguments.

#### Source Code
```python
def runSolvers(target: int, numbers: list, console: Console) -> None:
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_all.sh")
    args = [script_path, str(target)] + [str(n) for n in numbers]
    with console.status("[bold green]Running all 3 solvers... This might take a while.[/bold green]") as status:
        subprocess.run(args, capture_output=True, text=True)
```

---

### parseOutput

**Signature:**
```python
def parseOutput(text: str) -> dict
```

**Purpose:** Extracts structured "Expression" and "Value" fields from raw solver output strings.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| text | str | Yes | — | Raw multi-line string text from a solver's stdout. |

**Returns:**
| Type | Description |
|------|-------------|
| dict | Structured keys `expression`, `value`, `success`, and `raw`. |

**Source Code:**
```python
def parseOutput(text: str) -> dict:
    result = {
        "expression": "N/A",
        "value": "N/A",
        "success": False,
        "raw": text or "No output captured.",
    }
    for line in text.splitlines():
        if line.startswith("Expression:"):
            result["expression"] = line.replace("Expression:", "").strip()
            result["success"] = True
        elif line.startswith("Value:"):
            result["value"] = line.replace("Value:", "").strip()
        elif "No solution" in line:
            result["success"] = False
    return result
```

**Implementation (Executable Logic Only):**
* **Line 0:** `initialization` — Creates a default failure result state.
* **Line 1:** `loop` — Iterates through every line in the raw input text.
* **Line 2:** `starts_with match` — Uses `str.startswith()` to identify relevant fields and `str.replace()`/`str.strip()` to extract sanitised data values.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| str.splitlines | Built-in | Line iteration | Python |
| str.strip | Built-in | Whitespace removal | Python |
| str.startswith | Built-in | Prefix identification | Python |
