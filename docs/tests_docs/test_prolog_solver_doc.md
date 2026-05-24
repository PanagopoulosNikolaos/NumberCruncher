# test_prolog_solver.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [TestPrologSolver](#testprologsolver) | Class | Tests the SWI-Prolog logic solver via subprocess integration. |
| [runSolver](#runsolver) | Function | Runs the Prolog solver with the given target and numbers. |
| [testDirectMatch](#testdirectmatch) | Function | Tests when the target is directly present in the input numbers. |
| [testVeryEasyCase](#testveryeasycase) | Function | Tests solver with very easy combinations of numbers. |
| [testEasyCase](#testeasycase) | Function | Tests solver with easy combinations of numbers. |
| [testMediumCase](#testmediumcase) | Function | Tests solver with medium difficulty parameters. |
| [testHardCase](#testhardcase) | Function | Tests solver with hard difficulty parameters. |
| [testVeryHardCase](#testveryhardcase) | Function | Tests solver with very hard difficulty parameters. |
| [testNoSolution](#testnosolution) | Function | Tests solver behavior when no solution exists. |
| [testSubtractionConstraint](#testsubtractionconstraint) | Function | Tests that subtraction only evaluates to positive values. |
| [testDivisionConstraint](#testdivisionconstraint) | Function | Tests that division only evaluates to exact integers. |
| [testDuplicateNumbers](#testduplicatenumbers) | Function | Tests correct evaluation when duplicate values are present. |

## Overview
This file contains integration tests for the Prolog implementation of the Countdown numbers game solver. It executes SWI-Prolog (`swipl`) using Python subprocess, passing the target and available numbers list to evaluate logic outcomes. The tests run using the standard Python `unittest` framework.

## TestPrologSolver

**Class Responsibility:** Manages SWI-Prolog solver executions and verifies outputs against math constraints (such as positive subtraction and exact integer divisions) and distinct game difficulties.

### runSolver

**Signature:**
```python
def runSolver(self, target: int, numbers: list) -> tuple
```

**Purpose:** Runs the Prolog solver with the given target and numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |
| target | int | Yes | — | Target sum to construct |
| numbers | list | Yes | — | Available input numbers |

**Returns:**
| Type | Description |
|------|-------------|
| tuple | A tuple containing (success_status, expression, value) |

**Source Code:**
```python
    def runSolver(self, target: int, numbers: list) -> tuple:
        prolog_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/prolog/countdown.pl"))
        prolog_list = "[" + ",".join(map(str, numbers)) + "]"

        cmd_args = [
            "swipl",
            "-s", prolog_file,
            "-g", f"main({target}, {prolog_list}), halt."
        ]

        proc_result = subprocess.run(cmd_args, capture_output=True, text=True, check=True)

        expr_str = ""
        val_str = ""
        success_status = False

        for line in proc_result.stdout.splitlines():
            if line.startswith("Expression:"):
                expr_str = line.replace("Expression:", "").strip()
                success_status = True
            elif line.startswith("Value:"):
                val_str = line.replace("Value:", "").strip()

        return success_status, expr_str, val_str
```

**Implementation (Executable Logic Only):**
* **Line 25:** `def runSolver(self, target: int, numbers: list) -> tuple:` — Method signature.
* **Line 36:** `prolog_file = os.path.abspath(...)` — Resolves the Prolog source file location.
* **Line 37:** `prolog_list = ...` — Formats python list as a Prolog list string representation.
* **Line 39:** `cmd_args = ["swipl", ...]` — Generates command parameters for SWI-Prolog.
* **Line 45:** `proc_result = subprocess.run(...)` — Spawns `swipl` process and retrieves outputs.
* **Line 47:** `expr_str = ""` — Initializes output expression string.
* **Line 48:** `val_str = ""` — Initializes output value string.
* **Line 49:** `success_status = False` — Initializes status flags.
* **Line 51:** `for line in proc_result.stdout.splitlines():` — Iterates through stdout lines.
* **Line 52:** `if line.startswith("Expression:"):` — Identifies generated solution.
* **Line 53:** `expr_str = ...` — Extracts expression string.
* **Line 54:** `success_status = True` — Sets status to success.
* **Line 55:** `elif line.startswith("Value:"):` — Identifies target matches.
* **Line 56:** `val_str = ...` — Extracts value.
* **Line 58:** `return success_status, expr_str, val_str` — Returns outcomes.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| subprocess.run | External | Executes swipl engine | subprocess |

### testDirectMatch

**Signature:**
```python
def testDirectMatch(self) -> None
```

**Purpose:** Tests when the target is directly present in the input numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testDirectMatch(self) -> None:
        success, expr, val = self.runSolver(10, [10, 2, 3])
        self.assertTrue(success)
        self.assertEqual(val, "10")
        self.assertIn("10", expr)
```

**Implementation (Executable Logic Only):**
* **Line 60:** `def testDirectMatch(self) -> None:` — Method signature.
* **Line 67:** `success, expr, val = self.runSolver(10, [10, 2, 3])` — Runs Prolog solver.
* **Line 68:** `self.assertTrue(success)` — Asserts solution success.
* **Line 69:** `self.assertEqual(val, "10")` — Asserts target match.
* **Line 70:** `self.assertIn("10", expr)` — Asserts direct expression contains target.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testVeryEasyCase

**Signature:**
```python
def testVeryEasyCase(self) -> None
```

**Purpose:** Tests solver with very easy combinations of numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testVeryEasyCase(self) -> None:
        success, expr, val = self.runSolver(10, [1, 2, 3, 4])
        self.assertTrue(success)
        self.assertEqual(val, "10")
        self.assertEqual(int(eval(expr)), 10)
```

**Implementation (Executable Logic Only):**
* **Line 72:** `def testVeryEasyCase(self) -> None:` — Method signature.
* **Line 79:** `success, expr, val = self.runSolver(10, [1, 2, 3, 4])` — Runs Prolog solver.
* **Line 80:** `self.assertTrue(success)` — Asserts success.
* **Line 81:** `self.assertEqual(val, "10")` — Asserts output value.
* **Line 83:** `self.assertEqual(int(eval(expr)), 10)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testEasyCase

**Signature:**
```python
def testEasyCase(self) -> None
```

**Purpose:** Tests solver with easy combinations of numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testEasyCase(self) -> None:
        success, expr, val = self.runSolver(50, [2, 3, 5, 10, 25])
        self.assertTrue(success)
        self.assertEqual(val, "50")
        self.assertEqual(int(eval(expr)), 50)
```

**Implementation (Executable Logic Only):**
* **Line 85:** `def testEasyCase(self) -> None:` — Method signature.
* **Line 92:** `success, expr, val = self.runSolver(50, ...)` — Runs solver.
* **Line 93:** `self.assertTrue(success)` — Asserts success.
* **Line 94:** `self.assertEqual(val, "50")` — Asserts value.
* **Line 95:** `self.assertEqual(int(eval(expr)), 50)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testMediumCase

**Signature:**
```python
def testMediumCase(self) -> None
```

**Purpose:** Tests solver with medium difficulty parameters.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testMediumCase(self) -> None:
        success, expr, val = self.runSolver(123, [1, 2, 3, 4, 25])
        self.assertTrue(success)
        self.assertEqual(val, "123")
        self.assertEqual(int(eval(expr)), 123)
```

**Implementation (Executable Logic Only):**
* **Line 97:** `def testMediumCase(self) -> None:` — Method signature.
* **Line 104:** `success, expr, val = self.runSolver(123, ...)` — Runs solver.
* **Line 105:** `self.assertTrue(success)` — Asserts success.
* **Line 106:** `self.assertEqual(val, "123")` — Asserts value.
* **Line 107:** `self.assertEqual(int(eval(expr)), 123)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testHardCase

**Signature:**
```python
def testHardCase(self) -> None
```

**Purpose:** Tests solver with hard difficulty parameters.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testHardCase(self) -> None:
        success, expr, val = self.runSolver(456, [1, 3, 5, 10, 25, 50])
        self.assertTrue(success)
        self.assertEqual(val, "456")
        self.assertEqual(int(eval(expr)), 456)
```

**Implementation (Executable Logic Only):**
* **Line 109:** `def testHardCase(self) -> None:` — Method signature.
* **Line 116:** `success, expr, val = self.runSolver(456, ...)` — Runs solver.
* **Line 117:** `self.assertTrue(success)` — Asserts success.
* **Line 118:** `self.assertEqual(val, "456")` — Asserts value.
* **Line 119:** `self.assertEqual(int(eval(expr)), 456)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testVeryHardCase

**Signature:**
```python
def testVeryHardCase(self) -> None
```

**Purpose:** Tests solver with very hard difficulty parameters.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testVeryHardCase(self) -> None:
        success, expr, val = self.runSolver(987, [1, 2, 3, 4, 75, 100])
        self.assertTrue(success)
        self.assertEqual(val, "987")
        self.assertEqual(int(eval(expr)), 987)
```

**Implementation (Executable Logic Only):**
* **Line 121:** `def testVeryHardCase(self) -> None:` — Method signature.
* **Line 128:** `success, expr, val = self.runSolver(987, ...)` — Runs solver.
* **Line 129:** `self.assertTrue(success)` — Asserts success.
* **Line 130:** `self.assertEqual(val, "987")` — Asserts value.
* **Line 131:** `self.assertEqual(int(eval(expr)), 987)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testNoSolution

**Signature:**
```python
def testNoSolution(self) -> None
```

**Purpose:** Tests solver behavior when no solution exists.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testNoSolution(self) -> None:
        success, expr, val = self.runSolver(999, [2, 2])
        self.assertFalse(success)
        self.assertEqual(expr, "")
        self.assertEqual(val, "")
```

**Implementation (Executable Logic Only):**
* **Line 133:** `def testNoSolution(self) -> None:` — Method signature.
* **Line 140:** `success, expr, val = self.runSolver(999, [2, 2])` — Runs solver.
* **Line 141:** `self.assertFalse(success)` — Asserts failure.
* **Line 142:** `self.assertEqual(expr, "")` — Asserts empty expression.
* **Line 143:** `self.assertEqual(val, "")` — Asserts empty value.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testSubtractionConstraint

**Signature:**
```python
def testSubtractionConstraint(self) -> None
```

**Purpose:** Tests that subtraction only evaluates to positive values.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testSubtractionConstraint(self) -> None:
        success, expr, val = self.runSolver(1, [2, 3])
        self.assertTrue(success)
        self.assertEqual(val, "1")
        self.assertIn("-", expr)
        self.assertNotIn("2 - 3", expr)
```

**Implementation (Executable Logic Only):**
* **Line 145:** `def testSubtractionConstraint(self) -> None:` — Method signature.
* **Line 152:** `success, expr, val = self.runSolver(1, [2, 3])` — Runs solver.
* **Line 153:** `self.assertTrue(success)` — Asserts success.
* **Line 154:** `self.assertEqual(val, "1")` — Asserts target value.
* **Line 155:** `self.assertIn("-", expr)` — Asserts subtraction occurs.
* **Line 156:** `self.assertNotIn("2 - 3", expr)` — Asserts negative subtraction was avoided.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testDivisionConstraint

**Signature:**
```python
def testDivisionConstraint(self) -> None
```

**Purpose:** Tests that division only evaluates to exact integers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testDivisionConstraint(self) -> None:
        # 10 / 4 is non-integer, so no solution should be possible.
        success, expr, val = self.runSolver(2, [10, 4])
        self.assertFalse(success)
```

**Implementation (Executable Logic Only):**
* **Line 158:** `def testDivisionConstraint(self) -> None:` — Method signature.
* **Line 166:** `success, expr, val = self.runSolver(2, [10, 4])` — Runs solver.
* **Line 167:** `self.assertFalse(success)` — Asserts failure.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |

### testDuplicateNumbers

**Signature:**
```python
def testDuplicateNumbers(self) -> None
```

**Purpose:** Tests correct evaluation when duplicate values are present.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPrologSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testDuplicateNumbers(self) -> None:
        success, expr, val = self.runSolver(10, [5, 5])
        self.assertTrue(success)
        self.assertEqual(val, "10")
        self.assertEqual(int(eval(expr)), 10)
```

**Implementation (Executable Logic Only):**
* **Line 169:** `def testDuplicateNumbers(self) -> None:` — Method signature.
* **Line 176:** `success, expr, val = self.runSolver(10, [5, 5])` — Runs solver.
* **Line 177:** `self.assertTrue(success)` — Asserts success.
* **Line 178:** `self.assertEqual(val, "10")` — Asserts target value.
* **Line 179:** `self.assertEqual(int(eval(expr)), 10)` — Asserts math evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestPrologSolver |
