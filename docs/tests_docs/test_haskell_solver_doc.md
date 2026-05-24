# test_haskell_solver.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [TestHaskellSolver](#testhaskellsolver) | Class | Tests the Haskell compiled binary solver via subprocess integration. |
| [setUpClass](#setupclass) | Function | Compiles the Haskell solver before running tests. |
| [runSolver](#runsolver) | Function | Runs the Haskell solver binary with the specified arguments. |
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
This file contains integration tests for the Haskell implementation of the Countdown numbers game solver. It compiles the Haskell source code using `make` and executes the binary under different difficulties and edge cases, parsing standard output to check correctness. The tests run using the standard Python `unittest` framework.

## TestHaskellSolver

**Class Responsibility:** Manages compilation of the Haskell binary and verifies its execution correctness across varying game conditions and arithmetic boundary rules.

### setUpClass

**Signature:**
```python
@classmethod
def setUpClass(cls) -> None
```

**Purpose:** Compiles the Haskell solver before running tests.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| cls | type | Yes | — | Class object reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Set up tasks are performed in-place |

**Source Code:**
```python
    @classmethod
    def setUpClass(cls) -> None:
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
* **Line 33:** `haskell_dir = os.path.abspath(...)` — Resolves the Haskell project subdirectory.
* **Line 34:** `subprocess.run(["make", "build"], ...)` — Compiles the binary using the Makefile rules.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| subprocess.run | External | Spawns compilation process | subprocess |

### runSolver

**Signature:**
```python
def runSolver(self, target: int, numbers: list) -> tuple
```

**Purpose:** Runs the Haskell solver binary with the specified arguments.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |
| target | int | Yes | — | Target sum to construct |
| numbers | list | Yes | — | Available input numbers |

**Returns:**
| Type | Description |
|------|-------------|
| tuple | A tuple containing (success_status, expression, value) |

**Source Code:**
```python
    def runSolver(self, target: int, numbers: list) -> tuple:
        binary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/haskell/countdown"))
        cmd_args = [binary_path, str(target)] + [str(n) for n in numbers]
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
* **Line 42:** `def runSolver(self, target: int, numbers: list) -> tuple:` — Method signature.
* **Line 53:** `binary_path = os.path.abspath(...)` — Resolves location of compiled Haskell executable.
* **Line 54:** `cmd_args = [binary_path, str(target)] + ...` — Builds CLI argument list.
* **Line 55:** `proc_result = subprocess.run(...)` — Spawns solver binary process.
* **Line 57:** `expr_str = ""` — Initializes expression string variable.
* **Line 58:** `val_str = ""` — Initializes value string variable.
* **Line 59:** `success_status = False` — Initializes success status.
* **Line 61:** `for line in proc_result.stdout.splitlines():` — Iterates through stdout lines.
* **Line 62:** `if line.startswith("Expression:"):` — Checks for solution expression.
* **Line 63:** `expr_str = ...` — Extracts expression from output.
* **Line 64:** `success_status = True` — Sets status to success.
* **Line 65:** `elif line.startswith("Value:"):` — Checks for solution evaluation.
* **Line 66:** `val_str = ...` — Extracts evaluation value.
* **Line 68:** `return success_status, expr_str, val_str` — Returns unpacked tuple.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| subprocess.run | External | Executes solver binary | subprocess |

### testDirectMatch

**Signature:**
```python
def testDirectMatch(self) -> None
```

**Purpose:** Tests when the target is directly present in the input numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(expr, "10")
```

**Implementation (Executable Logic Only):**
* **Line 70:** `def testDirectMatch(self) -> None:` — Method signature.
* **Line 77:** `success, expr, val = self.runSolver(10, [10, 2, 3])` — Invokes Haskell solver.
* **Line 78:** `self.assertTrue(success)` — Asserts solver reports success.
* **Line 79:** `self.assertEqual(val, "10")` — Asserts target value is matched.
* **Line 80:** `self.assertEqual(expr, "10")` — Asserts expression contains direct value.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testVeryEasyCase

**Signature:**
```python
def testVeryEasyCase(self) -> None
```

**Purpose:** Tests solver with very easy combinations of numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(eval(expr), 10)
```

**Implementation (Executable Logic Only):**
* **Line 82:** `def testVeryEasyCase(self) -> None:` — Method signature.
* **Line 89:** `success, expr, val = self.runSolver(10, [1, 2, 3, 4])` — Runs solver.
* **Line 90:** `self.assertTrue(success)` — Asserts success.
* **Line 91:** `self.assertEqual(val, "10")` — Asserts output value.
* **Line 93:** `self.assertEqual(eval(expr), 10)` — Asserts math evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testEasyCase

**Signature:**
```python
def testEasyCase(self) -> None
```

**Purpose:** Tests solver with easy combinations of numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(eval(expr), 50)
```

**Implementation (Executable Logic Only):**
* **Line 95:** `def testEasyCase(self) -> None:` — Method signature.
* **Line 102:** `success, expr, val = self.runSolver(50, ...)` — Runs solver.
* **Line 103:** `self.assertTrue(success)` — Asserts success.
* **Line 104:** `self.assertEqual(val, "50")` — Asserts output value.
* **Line 105:** `self.assertEqual(eval(expr), 50)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testMediumCase

**Signature:**
```python
def testMediumCase(self) -> None
```

**Purpose:** Tests solver with medium difficulty parameters.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(eval(expr), 123)
```

**Implementation (Executable Logic Only):**
* **Line 107:** `def testMediumCase(self) -> None:` — Method signature.
* **Line 114:** `success, expr, val = self.runSolver(123, ...)` — Runs solver.
* **Line 115:** `self.assertTrue(success)` — Asserts success.
* **Line 116:** `self.assertEqual(val, "123")` — Asserts value.
* **Line 117:** `self.assertEqual(eval(expr), 123)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testHardCase

**Signature:**
```python
def testHardCase(self) -> None
```

**Purpose:** Tests solver with hard difficulty parameters.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(eval(expr), 456)
```

**Implementation (Executable Logic Only):**
* **Line 119:** `def testHardCase(self) -> None:` — Method signature.
* **Line 126:** `success, expr, val = self.runSolver(456, ...)` — Runs solver.
* **Line 127:** `self.assertTrue(success)` — Asserts success.
* **Line 128:** `self.assertEqual(val, "456")` — Asserts value.
* **Line 129:** `self.assertEqual(eval(expr), 456)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testVeryHardCase

**Signature:**
```python
def testVeryHardCase(self) -> None
```

**Purpose:** Tests solver with very hard difficulty parameters.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(eval(expr), 987)
```

**Implementation (Executable Logic Only):**
* **Line 131:** `def testVeryHardCase(self) -> None:` — Method signature.
* **Line 138:** `success, expr, val = self.runSolver(987, ...)` — Runs solver.
* **Line 139:** `self.assertTrue(success)` — Asserts success.
* **Line 140:** `self.assertEqual(val, "987")` — Asserts value.
* **Line 141:** `self.assertEqual(eval(expr), 987)` — Asserts evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testNoSolution

**Signature:**
```python
def testNoSolution(self) -> None
```

**Purpose:** Tests solver behavior when no solution exists.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
* **Line 143:** `def testNoSolution(self) -> None:` — Method signature.
* **Line 150:** `success, expr, val = self.runSolver(999, [2, 2])` — Runs solver.
* **Line 151:** `self.assertFalse(success)` — Asserts failure.
* **Line 152:** `self.assertEqual(expr, "")` — Asserts empty expression output.
* **Line 153:** `self.assertEqual(val, "")` — Asserts empty value output.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testSubtractionConstraint

**Signature:**
```python
def testSubtractionConstraint(self) -> None
```

**Purpose:** Tests that subtraction only evaluates to positive values.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
* **Line 155:** `def testSubtractionConstraint(self) -> None:` — Method signature.
* **Line 162:** `success, expr, val = self.runSolver(1, [2, 3])` — Runs solver.
* **Line 163:** `self.assertTrue(success)` — Asserts success.
* **Line 164:** `self.assertEqual(val, "1")` — Asserts value is 1.
* **Line 165:** `self.assertIn("-", expr)` — Asserts subtraction occurred.
* **Line 166:** `self.assertNotIn("2 - 3", expr)` — Asserts subtraction order is positive.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testDivisionConstraint

**Signature:**
```python
def testDivisionConstraint(self) -> None
```

**Purpose:** Tests that division only evaluates to exact integers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
* **Line 168:** `def testDivisionConstraint(self) -> None:` — Method signature.
* **Line 176:** `success, expr, val = self.runSolver(2, [10, 4])` — Runs solver with non-integer inputs.
* **Line 177:** `self.assertFalse(success)` — Asserts failure.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |

### testDuplicateNumbers

**Signature:**
```python
def testDuplicateNumbers(self) -> None
```

**Purpose:** Tests correct evaluation when duplicate values are present.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestHaskellSolver | Yes | — | Class instance reference |

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
        self.assertEqual(eval(expr), 10)
```

**Implementation (Executable Logic Only):**
* **Line 179:** `def testDuplicateNumbers(self) -> None:` — Method signature.
* **Line 186:** `success, expr, val = self.runSolver(10, [5, 5])` — Runs solver with duplicates.
* **Line 187:** `self.assertTrue(success)` — Asserts success.
* **Line 188:** `self.assertEqual(val, "10")` — Asserts target value.
* **Line 189:** `self.assertEqual(eval(expr), 10)` — Asserts math evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| runSolver | Internal | Executes solver and parses output | TestHaskellSolver |
