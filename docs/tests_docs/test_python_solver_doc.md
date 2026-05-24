# test_python_solver.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [TestPythonSolver](#testpythonsolver) | Class | Tests the recursive tree-search solver implemented in Python. |
| [testDirectMatch](#testdirectmatch) | Function | Tests when the target is directly present in the input numbers. |
| [testVeryEasyCase](#testveryeasycase) | Function | Tests the solver with a very easy combination of numbers. |
| [testEasyCase](#testeasycase) | Function | Tests the solver with an easy combination of numbers. |
| [testMediumCase](#testmediumcase) | Function | Tests the solver with a medium difficulty game. |
| [testHardCase](#testhardcase) | Function | Tests the solver with a hard difficulty game. |
| [testVeryHardCase](#testveryhardcase) | Function | Tests the solver with a very hard difficulty game. |
| [testNoSolution](#testnosolution) | Function | Tests behavior when no valid solution can be constructed. |
| [testSingleElementPool](#testsingleelementpool) | Function | Tests behavior when the pool has only one element which is not the target. |
| [testEmptyPool](#testemptypool) | Function | Tests behavior when the input pool is empty. |
| [testSubtractionConstraint](#testsubtractionconstraint) | Function | Tests that subtraction only occurs if the result is strictly positive. |
| [testDivisionConstraint](#testdivisionconstraint) | Function | Tests that division only occurs if the result is an exact integer. |
| [testDuplicateNumbers](#testduplicatenumbers) | Function | Tests that duplicate input numbers are handled correctly. |

## Overview
This file contains unit tests for the Python implementation of the Countdown numbers game solver. It imports the solver module and tests its tree-search logic across varying difficulties and mathematical edge cases. The tests are executed using Python's standard `unittest` framework.

## TestPythonSolver

**Class Responsibility:** Verifies the correctness and logic constraints of the Python solver. It runs a series of unit tests with pre-defined number pools and target values, asserting expected returns.

### testDirectMatch

**Signature:**
```python
def testDirectMatch(self) -> None
```

**Purpose:** Tests when the target is directly present in the input numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testDirectMatch(self) -> None:
        target_val = 10
        numbers_pool = [(10, "10"), (2, "2"), (3, "3")]  # Simple pool with target present.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 10)  # Value matches target.
            self.assertEqual(expr_str, "10")  # Direct expression is the value.
```

**Implementation (Executable Logic Only):**
* **Line 24:** `def testDirectMatch(self) -> None:` — Method signature defining the test case.
* **Line 31:** `target_val = 10` — Defines the target value to solve for.
* **Line 32:** `numbers_pool = [(10, "10"), (2, "2"), (3, "3")]` — Defines the initial pool of number-expression tuples.
* **Line 33:** `result = countdown.solve(numbers_pool, target_val)` — Invokes the Python solver recursive search.
* **Line 34:** `self.assertIsNotNone(result)` — Asserts that a solution was found.
* **Line 35:** `if result is not None:` — Conditional check to prevent None type errors in static analysis.
* **Line 36:** `expr_str, val_str = result` — Unpacks the solution expression and evaluated value.
* **Line 37:** `self.assertEqual(val_str, 10)` — Asserts the returned value matches target.
* **Line 38:** `self.assertEqual(expr_str, "10")` — Asserts the returned expression string is correct.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testVeryEasyCase

**Signature:**
```python
def testVeryEasyCase(self) -> None
```

**Purpose:** Tests the solver with a very easy combination of numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testVeryEasyCase(self) -> None:
        target_val = 10
        numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4")]  # Sum equals 10.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 10)
            self.assertEqual(eval(expr_str), 10)  # Expression evaluates to 10.
```

**Implementation (Executable Logic Only):**
* **Line 40:** `def testVeryEasyCase(self) -> None:` — Method signature defining the test case.
* **Line 47:** `target_val = 10` — Target value setting.
* **Line 48:** `numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4")]` — Set pool that sums to 10.
* **Line 49:** `result = countdown.solve(numbers_pool, target_val)` — Invokes solver.
* **Line 50:** `self.assertIsNotNone(result)` — Asserts solution exists.
* **Line 51:** `if result is not None:` — Conditional check.
* **Line 52:** `expr_str, val_str = result` — Unpacks results.
* **Line 53:** `self.assertEqual(val_str, 10)` — Asserts target value matches.
* **Line 54:** `self.assertEqual(eval(expr_str), 10)` — Asserts math evaluation.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testEasyCase

**Signature:**
```python
def testEasyCase(self) -> None
```

**Purpose:** Tests the solver with an easy combination of numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testEasyCase(self) -> None:
        target_val = 50
        numbers_pool = [(2, "2"), (3, "3"), (5, "5"), (10, "10"), (25, "25")]  # Multiplication leads to target.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 50)
            self.assertEqual(eval(expr_str), 50)
```

**Implementation (Executable Logic Only):**
* **Line 56:** `def testEasyCase(self) -> None:` — Method signature.
* **Line 63:** `target_val = 50` — Target value setting.
* **Line 64:** `numbers_pool = [(2, "2"), (3, "3"), (5, "5"), (10, "10"), (25, "25")]` — Pool setup.
* **Line 65:** `result = countdown.solve(numbers_pool, target_val)` — Solver invocation.
* **Line 66:** `self.assertIsNotNone(result)` — Solution assertion.
* **Line 68:** `expr_str, val_str = result` — Unpacks values.
* **Line 69:** `self.assertEqual(val_str, 50)` — Asserts target match.
* **Line 70:** `self.assertEqual(eval(expr_str), 50)` — Asserts math correctness.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testMediumCase

**Signature:**
```python
def testMediumCase(self) -> None
```

**Purpose:** Tests the solver with a medium difficulty game.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testMediumCase(self) -> None:
        target_val = 123
        numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (25, "25")]  # Requires multiple operations.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 123)
            self.assertEqual(eval(expr_str), 123)
```

**Implementation (Executable Logic Only):**
* **Line 72:** `def testMediumCase(self) -> None:` — Method signature.
* **Line 79:** `target_val = 123` — Sets target value.
* **Line 80:** `numbers_pool = [...]` — Sets number pool.
* **Line 81:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 82:** `self.assertIsNotNone(result)` — Asserts result exists.
* **Line 84:** `expr_str, val_str = result` — Unpacks solution.
* **Line 85:** `self.assertEqual(val_str, 123)` — Validates output value.
* **Line 86:** `self.assertEqual(eval(expr_str), 123)` — Validates output expression.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testHardCase

**Signature:**
```python
def testHardCase(self) -> None
```

**Purpose:** Tests the solver with a hard difficulty game.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testHardCase(self) -> None:
        target_val = 456
        numbers_pool = [(1, "1"), (3, "3"), (5, "5"), (10, "10"), (25, "25"), (50, "50")]
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 456)
            self.assertEqual(eval(expr_str), 456)
```

**Implementation (Executable Logic Only):**
* **Line 88:** `def testHardCase(self) -> None:` — Method signature.
* **Line 95:** `target_val = 456` — Sets target value.
* **Line 96:** `numbers_pool = [...]` — Sets pool.
* **Line 97:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 98:** `self.assertIsNotNone(result)` — Validates solution existence.
* **Line 100:** `expr_str, val_str = result` — Unpacks variables.
* **Line 101:** `self.assertEqual(val_str, 456)` — Validates output value.
* **Line 102:** `self.assertEqual(eval(expr_str), 456)` — Validates arithmetic.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testVeryHardCase

**Signature:**
```python
def testVeryHardCase(self) -> None
```

**Purpose:** Tests the solver with a very hard difficulty game.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testVeryHardCase(self) -> None:
        target_val = 987
        numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (75, "75"), (100, "100")]
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 987)
            self.assertEqual(eval(expr_str), 987)
```

**Implementation (Executable Logic Only):**
* **Line 104:** `def testVeryHardCase(self) -> None:` — Method signature.
* **Line 111:** `target_val = 987` — Sets target value.
* **Line 112:** `numbers_pool = [...]` — Sets pool.
* **Line 113:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 114:** `self.assertIsNotNone(result)` — Asserts solution exists.
* **Line 116:** `expr_str, val_str = result` — Unpacks results.
* **Line 117:** `self.assertEqual(val_str, 987)` — Validates output value.
* **Line 118:** `self.assertEqual(eval(expr_str), 987)` — Validates arithmetic.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testNoSolution

**Signature:**
```python
def testNoSolution(self) -> None
```

**Purpose:** Tests behavior when no valid solution can be constructed.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testNoSolution(self) -> None:
        target_val = 999
        numbers_pool = [(2, "2"), (2, "2")]  # Impossible to reach 999.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)
```

**Implementation (Executable Logic Only):**
* **Line 120:** `def testNoSolution(self) -> None:` — Method signature.
* **Line 127:** `target_val = 999` — Sets target value.
* **Line 128:** `numbers_pool = [(2, "2"), (2, "2")]` — Sets impossible pool.
* **Line 129:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 130:** `self.assertIsNone(result)` — Asserts that no solution was found.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testSingleElementPool

**Signature:**
```python
def testSingleElementPool(self) -> None
```

**Purpose:** Tests behavior when the pool has only one element which is not the target.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testSingleElementPool(self) -> None:
        target_val = 10
        numbers_pool = [(5, "5")]  # Single element not matching target.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)
```

**Implementation (Executable Logic Only):**
* **Line 132:** `def testSingleElementPool(self) -> None:` — Method signature.
* **Line 139:** `target_val = 10` — Sets target.
* **Line 140:** `numbers_pool = [(5, "5")]` — Sets single element pool.
* **Line 141:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 142:** `self.assertIsNone(result)` — Asserts solver returns None.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testEmptyPool

**Signature:**
```python
def testEmptyPool(self) -> None
```

**Purpose:** Tests behavior when the input pool is empty.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testEmptyPool(self) -> None:
        target_val = 10
        numbers_pool = []  # Empty input pool.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)
```

**Implementation (Executable Logic Only):**
* **Line 144:** `def testEmptyPool(self) -> None:` — Method signature.
* **Line 151:** `target_val = 10` — Sets target.
* **Line 152:** `numbers_pool = []` — Sets empty pool.
* **Line 153:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 154:** `self.assertIsNone(result)` — Asserts solver returns None.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testSubtractionConstraint

**Signature:**
```python
def testSubtractionConstraint(self) -> None
```

**Purpose:** Tests that subtraction only occurs if the result is strictly positive.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testSubtractionConstraint(self) -> None:
        target_val = 1
        numbers_pool = [(2, "2"), (3, "3")]  # 3-2 = 1 (positive subtraction).
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 1)
            self.assertIn("-", expr_str)  # Subtraction must be utilized.
            self.assertNotIn("2 - 3", expr_str)  # Negative result subtraction is prohibited.
```

**Implementation (Executable Logic Only):**
* **Line 156:** `def testSubtractionConstraint(self) -> None:` — Method signature.
* **Line 163:** `target_val = 1` — Sets target value.
* **Line 164:** `numbers_pool = [(2, "2"), (3, "3")]` — Sets numbers pool.
* **Line 165:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 166:** `self.assertIsNotNone(result)` — Asserts solution exists.
* **Line 168:** `expr_str, val_str = result` — Unpacks results.
* **Line 169:** `self.assertEqual(val_str, 1)` — Validates output value.
* **Line 170:** `self.assertIn("-", expr_str)` — Asserts subtraction was used.
* **Line 171:** `self.assertNotIn("2 - 3", expr_str)` — Asserts negative subtraction was avoided.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testDivisionConstraint

**Signature:**
```python
def testDivisionConstraint(self) -> None
```

**Purpose:** Tests that division only occurs if the result is an exact integer.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testDivisionConstraint(self) -> None:
        target_val = 2
        numbers_pool = [(10, "10"), (4, "4")]  # 10/4 = 2.5 (non-integer division).
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)  # Non-integer division is prohibited, so no solution exists.
```

**Implementation (Executable Logic Only):**
* **Line 173:** `def testDivisionConstraint(self) -> None:` — Method signature.
* **Line 180:** `target_val = 2` — Sets target value.
* **Line 181:** `numbers_pool = [(10, "10"), (4, "4")]` — Sets non-divisible numbers.
* **Line 182:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 183:** `self.assertIsNone(result)` — Asserts no solution (since float division is prohibited).

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |

### testDuplicateNumbers

**Signature:**
```python
def testDuplicateNumbers(self) -> None
```

**Purpose:** Tests that duplicate input numbers are handled correctly.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| self | TestPythonSolver | Yes | — | Class instance reference |

**Returns:**
| Type | Description |
|------|-------------|
| None | Verified via assertion checks |

**Source Code:**
```python
    def testDuplicateNumbers(self) -> None:
        target_val = 10
        numbers_pool = [(5, "5"), (5, "5")]  # Two identical values.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 10)
            self.assertEqual(eval(expr_str), 10)
```

**Implementation (Executable Logic Only):**
* **Line 185:** `def testDuplicateNumbers(self) -> None:` — Method signature.
* **Line 192:** `target_val = 10` — Sets target value.
* **Line 193:** `numbers_pool = [(5, "5"), (5, "5")]` — Sets duplicate pool.
* **Line 194:** `result = countdown.solve(numbers_pool, target_val)` — Calls solver.
* **Line 195:** `self.assertIsNotNone(result)` — Asserts solution exists.
* **Line 197:** `expr_str, val_str = result` — Unpacks variables.
* **Line 198:** `self.assertEqual(val_str, 10)` — Validates output value.
* **Line 199:** `self.assertEqual(eval(expr_str), 10)` — Validates arithmetic.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| countdown.solve | External | Performs the recursive search | countdown |
