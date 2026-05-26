# tui.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [readFile](#readFile) | Function | Reads a file and returns its contents safely. |
| [parseOutput](#parseOutput) | Function | Parses solver output into structured result data. |
| [buildSolverPanel](#buildSolverPanel) | Function | Constructs a Rich Panel for displaying a single solver's result. |
| [buildBenchmarkTable](#buildBenchmarkTable) | Function | Generates a comparison table summarizing execution data for all solvers. |
| [findFastest](#findFastest) | Function | Identifies the solver demonstrating the lowest execution time. |
| [runSolvers](#runSolvers) | Function | Invokes the shell script to run all solvers simultaneously. |
| [displayResults](#displayResults) | Function | Collects outputs from individual runner components and manages TUI drawing. |
| [main](#main) | Function | Initializes application loop, handles menus, and triggers solver flows. |

## Overview
This file provides an interactive Text User Interface (TUI) to compare and benchmark the Python, Haskell, and Prolog solver components. It uses the `rich` framework to render side-by-side results, elapsed times, and a comparison table checking for numerical consensus among the solvers.

## Detailed Breakdown

### readFile

**Signature:**
```python
def readFile(path: str) -> str
```

**Purpose:** Safely reads a file and returns its contents, stripping trailing whitespace.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| path | str | Yes | — | The absolute or relative file path to read. |

**Returns:**
| Type | Description |
|------|-------------|
| str | The stripped text content of the file, or an empty string on error. |

**Source Code:**
```python
def readFile(path: str) -> str:
    try:
        with open(path) as f:
            return f.read().strip()
    except (FileNotFoundError, PermissionError):
        return ""
```

---

### parseOutput

**Signature:**
```python
def parseOutput(text: str) -> dict
```

**Purpose:** Parses solver output into structured result data.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| text | str | Yes | — | Raw multi-line output text from a solver's stdout. |

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

---

### buildSolverPanel

**Signature:**
```python
def buildSolverPanel(name: str, output: dict, time_str: str, color: str) -> Panel
```

**Purpose:** Constructs a Rich Panel for displaying a single solver's result.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| name | str | Yes | — | Display name of the solver. |
| output | dict | Yes | — | Parsed output dictionary. |
| time_str | str | Yes | — | Recorded execution time string. |
| color | str | Yes | — | Theme color used for indicators. |

**Returns:**
| Type | Description |
|------|-------------|
| Panel | A Rich framework Panel configured with solver results. |

**Source Code:**
```python
def buildSolverPanel(name: str, output: dict, time_str: str, color: str) -> Panel:
    if output["success"]:
        status = Text("SOLVED", style=f"bold {color}")
    else:
        status = Text("NO SOLUTION", style="bold red")

    content = Text.assemble(
        ("Expression: ", "bold"),
        (output["expression"], "cyan" if output["success"] else "dim"),
        "\n",
        ("Value: ", "bold"),
        (output["value"], "cyan" if output["success"] else "dim"),
        "\n\n",
        ("Time: ", "bold"),
        (f"{time_str}s", "yellow"),
        "\n",
        ("Status: ", "bold"),
        status,
    )

    return Panel(content, title=f"[bold]{name}[/bold]", border_style=color)
```

---

### buildBenchmarkTable

**Primary Library:** `rich.table`  
**Purpose:** Generates a comparison table summarizing execution data for all solvers.

#### Overview
This function creates a `Table` comparing execution time, success status, and result consensus. It finds the first successful solver value to use as a reference point, and then lists each solver's results alongside a indicator showing whether they match the reference.

#### Signature
```python
def buildBenchmarkTable(solver_data: list) -> Table
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| solver_data | list | Yes | — | List of tuples containing (name, output_dict, time_str, color). |

#### Returns
| Type | Description |
|------|-------------|
| Table | A Rich framework Table object. |

#### Workflow (Executable Logic Only)

**Phase 1: Table Initialization & Reference Finding**
* **Operation 1:** Initialize a `Table` with columns: Solver, Time, Result, and Match.
* **Operation 2:** Traverse `solver_data` to locate the first successful value to use as `reference_value`.

*Code Context:*
```python
    table = Table(
        title="Benchmark Comparison",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )
    table.add_column("Solver", justify="center", style="bold cyan")
    table.add_column("Time", justify="center", style="yellow")
    table.add_column("Result", justify="center")
    table.add_column("Match", justify="center")

    reference_value = None
    for name, output, time_str, color in solver_data:
        if output["success"]:
            reference_value = output["value"]
            break
```

**Phase 2: Row Generation & Match Verification**
* **Operation 1:** Iterate through solvers, defining colors based on success.
* **Operation 2:** Perform string comparisons against `reference_value` to determine consensus.
* **Operation 3:** Format text string indicators (e.g. checkmark and cross mark Unicode code points) and add the row to the table.

*Code Context:*
```python
    for name, output, time_str, color in solver_data:
        result = "PASS" if output["success"] else "FAIL"
        style = "green" if output["success"] else "red"

        if output["success"] and reference_value:
            matches = output["value"] == reference_value
            match_str = "\u2714 YES" if matches else "\u2718 DIFFERS" 
            match_style = "green" if matches else "red"
        else:
            match_str = "N/A"
            match_style = "dim"

        table.add_row(
            name,
            f"{time_str}s",
            f"[{style}]{result}[/{style}]",
            f"[{match_style}]{match_str}[/{match_style}]",
        )
```

#### Source Code
```python
def buildBenchmarkTable(solver_data: list) -> Table:
    table = Table(
        title="Benchmark Comparison",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )
    table.add_column("Solver", justify="center", style="bold cyan")
    table.add_column("Time", justify="center", style="yellow")
    table.add_column("Result", justify="center")
    table.add_column("Match", justify="center")

    reference_value = None
    for name, output, time_str, color in solver_data:
        if output["success"]:
            reference_value = output["value"]
            break

    for name, output, time_str, color in solver_data:
        result = "PASS" if output["success"] else "FAIL"
        style = "green" if output["success"] else "red"

        if output["success"] and reference_value:
            matches = output["value"] == reference_value
            match_str = "\u2714 YES" if matches else "\u2718 DIFFERS" 
            match_style = "green" if matches else "red"
        else:
            match_str = "N/A"
            match_style = "dim"

        table.add_row(
            name,
            f"{time_str}s",
            f"[{style}]{result}[/{style}]",
            f"[{match_style}]{match_str}[/{match_style}]",
        )

    return table
```

---

### findFastest

**Signature:**
```python
def findFastest(solver_data: list) -> str
```

**Purpose:** Identifies the solver demonstrating the lowest execution time.

**Source Code:**
```python
def findFastest(solver_data: list) -> str:
    times = []
    for name, _, time_str, _ in solver_data:
        try:
            t = float(time_str)
            times.append((name, t))
        except ValueError:
            pass

    if times:
        return min(times, key=lambda x: x[1])[0]
    return "N/A"
```

---

### runSolvers

**Signature:**
```python
def runSolvers(target: int, numbers: list, console: Console) -> None
```

**Purpose:** Invokes the shell script to run all solvers simultaneously.

**Source Code:**
```python
def runSolvers(target: int, numbers: list, console: Console) -> None:
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_all.sh")
    args = [script_path, str(target)] + [str(n) for n in numbers]
    
    with console.status("[bold green]Running all 3 solvers... This might take a while.[/bold green]") as status:
        subprocess.run(args, capture_output=True, text=True)  
```

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| subprocess.run | External | Runs the shell script | subprocess |
| os.path.join | External | Resolves file paths | os |

---

### displayResults

**Primary Library:** `rich`  
**Purpose:** Collects outputs from individual runner components and manages TUI drawing.

#### Overview
This function handles reading the temporary solver outputs from `/tmp/countdown_results`, parsing them, laying out side-by-side Result Panels using `Columns`, and displaying the benchmark table. It also performs consensus evaluation and outputs a banner summarizing if all solvers matched.

#### Signature
```python
def displayResults(console: Console) -> None
```

#### Workflow (Executable Logic Only)

**Phase 1: Read and Parse Outputs**
* **Operation 1:** Iterate through `SOLVERS` constants.
* **Operation 2:** Read stdout output files and execution time files from `TEMP_DIR`.
* **Operation 3:** Call `parseOutput` and structure the parsed data into `solver_data`.

**Phase 2: Renders Interface Elements**
* **Operation 1:** Build list of `Panel` objects using `buildSolverPanel`.
* **Operation 2:** Output panels arranged horizontally using `Columns`.
* **Operation 3:** Render the benchmark table via `buildBenchmarkTable` and print the fastest solver.
* **Operation 4:** Assert agreement of winning values and print a color-coded "PASS" or "FAIL" statement.

#### Source Code
```python
def displayResults(console: Console) -> None:
    solver_data = []
    for name, lang_hint, emoji, color in SOLVERS:
        output_text = readFile(os.path.join(TEMP_DIR, f"{lang_hint}_output.txt"))
        time_str = readFile(os.path.join(TEMP_DIR, f"{lang_hint}_time.txt"))
        time_str = time_str if time_str else "N/A"

        output = parseOutput(output_text)
        solver_data.append((name, output, time_str, color))

    panels = [
        buildSolverPanel(name, output, time_str, color)
        for name, output, time_str, color in solver_data
    ]

    console.print()
    console.rule("[bold green]Solver Results[/bold green]")
    console.print()

    columns = Columns(panels, equal=True, expand=True)
    console.print(columns)
    console.print()

    console.print(buildBenchmarkTable(solver_data))
    console.print()

    fastest = findFastest(solver_data)
    console.print(
        f"[bold]Fastest Solver:[/bold] [green]{fastest}[/green] "
        if fastest != "N/A"
        else "[bold]Fastest Solver:[/bold] [yellow]Unable to determine[/yellow]"
    )

    values = [
        output["value"]
        for _, output, _, _ in solver_data
        if output["success"]
    ]
    if len(set(values)) <= 1 and len(values) > 0:
        console.print("[bold green]All solutions match: PASS[/bold green]")
    elif len(values) > 1:
        console.print("[bold red]Solution values differ: FAIL[/bold red]")
    else:
        console.print("[bold yellow]No successful solutions to compare[/bold yellow]")
```

---

### main

**Primary Library:** `rich`  
**Purpose:** Initialises application loop, handles menus, and triggers solver flows.

#### Overview
This function is the main interactive loop of the TUI. It displays a table of five preloaded puzzles of increasing difficulty, prompting the user to select one, run a custom puzzle, or exit. It handles input validation and starts the execution flows.

#### Signature
```python
def main() -> None
```

#### Workflow (Executable Logic Only)

**Phase 1: Render Interactive Menu**
* **Operation 1:** Start infinite loop, clearing console on each iteration.
* **Operation 2:** Construct and print a menu Table representing preloaded puzzle difficulties.
* **Operation 3:** Call `Prompt.ask` to receive a selection.

**Phase 2: Input Handling & Execution**
* **Operation 1:** If choice is '0', break the loop.
* **Operation 2:** If choice is '6' (Custom), prompt for target and pool numbers, catching `ValueError` on bad inputs.
* **Operation 3:** For valid inputs, invoke `runSolvers` and print parsed details via `displayResults`, prompting to return.

#### Source Code
```python
def main() -> None:
    console = Console()
    
    while True:
        console.clear()
        console.rule("[bold green]Countdown Numbers Game - TUI[/bold green]")
        
        table = Table(title="Preloaded Examples", show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", justify="right")
        table.add_column("Difficulty", style="green")
        table.add_column("Target", style="bold yellow")
        table.add_column("Numbers")
        
        for i, ex in enumerate(EXAMPLES):
            num_str = ", ".join(map(str, ex["numbers"]))
            table.add_row(str(i+1), ex["name"], str(ex["target"]), num_str)
            
        console.print(table)
        console.print("6. [bold cyan]Custom[/bold cyan] - Enter your own target and numbers")
        console.print("0. [bold red]Exit[/bold red]")
        
        console.print()
        choice = Prompt.ask("Select an option", choices=["0", "1", "2", "3", "4", "5", "6"])
        
        if choice == "0":
            break
        
        if choice == "6":
            target_str = Prompt.ask("Enter the target number")
            numbers_str = Prompt.ask("Enter the available numbers separated by spaces")
            try:
                target = int(target_str)
                numbers = [int(n) for n in numbers_str.split()]
            except ValueError:
                console.print("[bold red]Invalid input![/bold red]")
                Prompt.ask("Press Enter to continue")
                continue
        else:
            idx = int(choice) - 1
            target = EXAMPLES[idx]["target"]
            numbers = EXAMPLES[idx]["numbers"]
            
        runSolvers(target, numbers, console)
        displayResults(console)
        
        console.print()
        Prompt.ask("Press Enter to return to the menu")
```
