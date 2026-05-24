# test_orchestration.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [TestOrchestration](#testorchestration) | Class | Tests the orchestration shell script and solver consensus. |
| [setUpClass](#setupclass) | Function | Builds the Haskell binary if Haskell is available on the system. |
| [runOrchestrator](#runorchestrator) | Function | Runs the run_all.sh orchestration script and returns parsed outputs. |
| [testRunAllScript](#testrunallscript) | Function | Tests basic execution of the run_all.sh script with simple arguments. |
| [testConsensusOnBenchmark](#testconsensusonbenchmark) | Function | Tests consensus among all available solvers on 5 default benchmark inputs. |

## Overview
This file contains integration and consensus tests for the Countdown numbers game solvers. It executes the concurrent shell orchestration script `run_all.sh` via a subprocess and validates that the temporary outputs written by each language's solver (Python, Haskell, Prolog) match the target and evaluation goals. The tests run using the standard Python `unittest` framework.

## TestOrchestration

**Class Responsibility:** Manages concurrent execution of all solvers, verifies output file generation, and validates result consensus across the benchmark examples.

### setUpClass

**Signature:**
```python
@classmethod
def setUpClass(cls) -> None
```

**Purpose:** Builds the Haskell binary if Haskell is available on the system.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| cls | type | Yes | — | Class object reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Compilation is run in-place |

**Source Code:**
```python
    @classmethod
    def setUpClass(cls) -> None:
        if HAS_HASKELL:
            haskell_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/haskell"))
            subprocess.run(
                ["make", "build"],
                cwd=haskell_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
```

**Implementation (Executable Logic Only):**
* **Line 26:** `@classmethod def setUpClass(cls) -> None:` — Method signature.
* **Line 33:** `if HAS_HASKELL:` — Check if GHC and make compile tools are available.
* **Line 34:** `haskell_dir = os.path.abspath(...)` — Resolves path to Haskell source.
* **Line 35:** `subprocess.run(["make", "build"], ...)` — Compiles Haskell solver if possible.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| subprocess.run | External | Compiles Haskell binary | subprocess |

---

### runOrchestrator

**Primary Library:** `subprocess`  
**Purpose:** Runs the `run_all.sh` orchestration script and returns parsed outputs.

#### Overview
This method invokes the orchestration script via a subprocess to run all three solvers concurrently. Once execution finishes, it reads and parses the generated output files (standard output and execution time metrics) stored in the temporary results directory. It dynamically detects available languages to handle compile-time or runtime exclusions gracefully.

#### Signature
```python
def runOrchestrator(self, target: int, numbers: list) -> dict
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestOrchestration | Yes | — | Class instance reference |
| target | int | Yes | — | Target sum to reach |
| numbers | list | Yes | — | List of available integers |

#### Returns
| Type | Description |
|------|-------------|
| dict | A dictionary mapping solver names to parsed output dicts containing 'success', 'expression', 'value', and 'time' |

#### Raises
| Exception | Condition |
|-----------|-----------|
| CalledProcessError | If the execution of the subprocess fails or returns non-zero status |

#### Dependencies
* **Required Libraries:** `subprocess` (Spawns shell script execution)
* **External Tools:** `run_all.sh` (Executes the concurrent solver suite)
* **Internal Modules:** None

#### Workflow (Executable Logic Only)

**Phase 1: Subprocess Invocation**
Resolves paths and executes the orchestrator script, capturing execution states.
* **Operation 1:** Formulates the absolute path to `run_all.sh`.
* **Operation 2:** Executes the script with the target and number parameters.

*Code Context:*
```python
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/tui_wraper/run_all.sh"))
        cmd_args = [script_path, str(target)] + [str(n) for n in numbers]

        # Execute orchestrator concurrently.
        subprocess.run(cmd_args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

**Phase 2: Result Processing and File Reading**
Iterates through output files from `/tmp/countdown_results`, extracts solver attributes, and updates the return dictionary.
* **Operation 1:** Generates the list of active solvers to parse based on compiler availability.
* **Operation 2:** Verifies existence of output and timing files.
* **Operation 3:** Extracts and parses expressions, values, and elapsed execution times.

*Code Context:*
```python
        results = {}
        temp_dir = "/tmp/countdown_results"

        # Define solvers to parse based on system availability.
        solvers_to_parse = [("python", True)]
        if HAS_HASKELL:
            solvers_to_parse.append(("haskell", True))
        if HAS_PROLOG:
            solvers_to_parse.append(("prolog", True))

        for name, available in solvers_to_parse:
            output_file = os.path.join(temp_dir, f"{name}_output.txt")
            time_file = os.path.join(temp_dir, f"{name}_time.txt")

            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(os.path.exists(time_file))

            with open(output_file, "r") as f:
                output_content = f.read().strip()

            with open(time_file, "r") as f:
                time_val = f.read().strip()

            # Parse solver output lines.
            expr_str = ""
            val_str = ""
            success_status = False

            for line in output_content.splitlines():
                if line.startswith("Expression:"):
                    expr_str = line.replace("Expression:", "").strip()
                    success_status = True
                elif line.startswith("Value:"):
                    val_str = line.replace("Value:", "").strip()

            results[name] = {
                "success": success_status,
                "expression": expr_str,
                "value": val_str,
                "time": time_val
            }

        return results
```

#### Source Code
```python
    def runOrchestrator(self, target: int, numbers: list) -> dict:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/tui_wraper/run_all.sh"))
        cmd_args = [script_path, str(target)] + [str(n) for n in numbers]

        # Execute orchestrator concurrently.
        subprocess.run(cmd_args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        results = {}
        temp_dir = "/tmp/countdown_results"

        # Define solvers to parse based on system availability.
        solvers_to_parse = [("python", True)]
        if HAS_HASKELL:
            solvers_to_parse.append(("haskell", True))
        if HAS_PROLOG:
            solvers_to_parse.append(("prolog", True))

        for name, available in solvers_to_parse:
            output_file = os.path.join(temp_dir, f"{name}_output.txt")
            time_file = os.path.join(temp_dir, f"{name}_time.txt")

            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(os.path.exists(time_file))

            with open(output_file, "r") as f:
                output_content = f.read().strip()

            with open(time_file, "r") as f:
                time_val = f.read().strip()

            # Parse solver output lines.
            expr_str = ""
            val_str = ""
            success_status = False

            for line in output_content.splitlines():
                if line.startswith("Expression:"):
                    expr_str = line.replace("Expression:", "").strip()
                    success_status = True
                elif line.startswith("Value:"):
                    val_str = line.replace("Value:", "").strip()

            results[name] = {
                "success": success_status,
                "expression": expr_str,
                "value": val_str,
                "time": time_val
            }

        return results
```

#### Usage Example
```python
results = self.runOrchestrator(10, [1, 2, 3, 4])
```

#### Common Issues & Related Functions
* **Issue:** Missing compilers. The method delegates skipped state detection using global `HAS_HASKELL` and `HAS_PROLOG` flags.
* **`setUpClass()`:** Compiles the Haskell target binary prior to orchestrating solver comparisons.

---

### testRunAllScript

**Signature:**
```python
def testRunAllScript(self) -> None
```

**Purpose:** Tests basic execution of the run_all.sh script with simple arguments.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestOrchestration | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testRunAllScript(self) -> None:
        target_val = 10
        numbers_pool = [1, 2, 3, 4]
        results = self.runOrchestrator(target_val, numbers_pool)

        # Python is guaranteed to be tested.
        self.assertIn("python", results)
        self.assertTrue(results["python"]["success"])
        self.assertEqual(results["python"]["value"], "10")

        # Check Haskell consensus if available.
        if HAS_HASKELL:
            self.assertIn("haskell", results)
            self.assertTrue(results["haskell"]["success"])
            self.assertEqual(results["haskell"]["value"], "10")

        # Check Prolog consensus if available.
        if HAS_PROLOG:
            self.assertIn("prolog", results)
            self.assertTrue(results["prolog"]["success"])
            self.assertEqual(results["prolog"]["value"], "10")
```

**Implementation (Executable Logic Only):**
* **Line 104:** `def testRunAllScript(self) -> None:` — Method signature.
* **Line 111:** `target_val = 10` — Sets target.
* **Line 112:** `numbers_pool = [1, 2, 3, 4]` — Sets pool.
* **Line 113:** `results = self.runOrchestrator(target_val, numbers_pool)` — Calls orchestrator.
* **Line 116:** `self.assertIn("python", results)` — Asserts Python output exists.
* **Line 117:** `self.assertTrue(results["python"]["success"])` — Asserts Python solved correctly.
* **Line 118:** `self.assertEqual(results["python"]["value"], "10")` — Validates value.
* **Line 121:** `if HAS_HASKELL:` — Conditional check.
* **Line 122:** `self.assertIn("haskell", results)` — Asserts Haskell output.
* **Line 123:** `self.assertTrue(...)` — Asserts Haskell success.
* **Line 127:** `if HAS_PROLOG:` — Conditional check.
* **Line 128:** `self.assertIn("prolog", results)` — Asserts Prolog output.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runOrchestrator | Internal | Runs concurrent suite | TestOrchestration |

---

### testConsensusOnBenchmark

**Signature:**
```python
def testConsensusOnBenchmark(self) -> None
```

**Purpose:** Tests consensus among all available solvers on 5 default benchmark inputs.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestOrchestration | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testConsensusOnBenchmark(self) -> None:
        benchmark_examples = [
            {"target": 10, "numbers": [1, 2, 3, 4]},
            {"target": 50, "numbers": [2, 3, 5, 10, 25]},
            {"target": 123, "numbers": [1, 2, 3, 4, 25]},
            {"target": 456, "numbers": [1, 3, 5, 10, 25, 50]},
            {"target": 987, "numbers": [1, 2, 3, 4, 75, 100]},
        ]

        for example in benchmark_examples:
            target = example["target"]
            numbers = example["numbers"]
            results = self.runOrchestrator(target, numbers)

            # Evaluate each solver's results to assert they are consistent.
            for name, data in results.items():
                self.assertTrue(
                    data["success"],
                    f"Solver {name} failed to solve target {target} with numbers {numbers}"
                )
                self.assertEqual(
                    int(data["value"]),
                    target,
                    f"Solver {name} target mismatch for target {target}: got {data['value']}"
                )
                self.assertEqual(
                    int(eval(data["expression"])),
                    target,
                    f"Solver {name} expression {data['expression']} does not evaluate to {target}"
                )
```

**Implementation (Executable Logic Only):**
* **Line 132:** `def testConsensusOnBenchmark(self) -> None:` — Method signature.
* **Line 139:** `benchmark_examples = [...]` — Hardcodes preloaded benchmark examples list.
* **Line 147:** `for example in benchmark_examples:` — Iterates benchmark list.
* **Line 148:** `target = example["target"]` — Retrieves target value.
* **Line 149:** `numbers = example["numbers"]` — Retrieves numbers pool.
* **Line 150:** `results = self.runOrchestrator(target, numbers)` — Evaluates orchestrator execution.
* **Line 153:** `for name, data in results.items():` — Iterates solver results.
* **Line 154:** `self.assertTrue(data["success"], ...)` — Validates success report.
* **Line 158:** `self.assertEqual(int(data["value"]), target, ...)` — Validates matched value.
* **Line 163:** `self.assertEqual(int(eval(data["expression"])), target, ...)` — Validates expression evaluation matches target.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runOrchestrator | Internal | Runs concurrent suite | TestOrchestration |
