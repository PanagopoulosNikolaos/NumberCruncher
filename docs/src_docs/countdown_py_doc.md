# countdown.py Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [solve](#solve) | Function | Recursively searches for an arithmetic expression evaluating to the target. |
| [main](#main) | Function | Orchestrates CLI argument parsing and solver execution. |

## Overview
This file implements a recursive, tree-based solver for the Countdown numbers game. It explores all valid arithmetic combinations of a pool of integers to find an expression that evaluates to a specific target value, adhering to game rules such as positive results for subtraction and integer results for division.

## Detailed Breakdown

### solve

**Primary Library:** `itertools` (for combinations)  
**Purpose:** Recursively searches for an expression evaluating to the target value.

#### Overview
The function employs a depth-first search strategy. It first checks if the target is already present in the current pool. If not, it iteratively selects pairs of numbers, applies all possible arithmetic operations, and adds the resulting expression back into the pool for the next recursive step.

#### Signature
```python
def solve(pool: list, target: int) -> tuple
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| pool | list | Yes | — | List of (value, expression_string) tuples representing current available numbers. |
| target | int | Yes | — | The integer target value to be achieved. |

#### Returns
| Type | Description |
|------|-------------|
| tuple | A tuple containing (expression_string, value) if a solution is found; otherwise, `None`. |

#### Raise
| Exception | Condition |
|-----------|-----------|
| None | Handled via return values. |

#### Dependencies
* **Required Libraries:** `itertools.combinations` (Generating unique pairs from the number pool)
* **Internal Modules:** `solve` (Recursive calls)

#### Workflow (Executable Logic Only)

**Phase 1: Base Case & Validation**
Checks if the target is already achieved or if the pool is exhausted.
* **Operation 1:** Iterate through `pool` to find any `val == target`.
* **Operation 2:** Verify `len(pool) >= 2` to ensure further operations are possible.

*Code Context:*
```python
    for val, expr in pool:
        if val == target:
            return expr, val
    if len(pool) < 2:
        return None
```

**Phase 2: Pair Selection & Combination**
Generates all possible arithmetic results from every pair in the pool.
* **Operation 1:** Select indices `i, j` using `combinations`.
* **Operation 2:** Calculate `v1 + v2` and `v1 * v2`.
* **Operation 3:** Calculate `v1 - v2` or `v2 - v1` if results are positive.
* **Operation 4:** Calculate `v1 // v2` or `v2 // v1` if division is exact.

**Phase 3: Recursive Search**
Recurses with the new number pool.
* **Operation 1:** For each candidate result, create a `new_pool` and call `solve`.
* **Operation 2:** Return the first valid result found.

#### Source Code
```python
def solve(pool, target):
    for val, expr in pool:
        if val == target:
            return expr, val
    if len(pool) < 2:
        return None
    for i, j in combinations(range(len(pool)), 2):
        v1, e1 = pool[i]
        v2, e2 = pool[j]
        remaining = [pool[k] for k in range(len(pool)) if k != i and k != j]
        candidates = [
            (v1 + v2, f"({e1} + {e2})"),
            (v1 * v2, f"({e1} * {e2})"),
        ]
        if v1 - v2 > 0:
            candidates.append((v1 - v2, f"({e1} - {e2})"))
        if v2 - v1 > 0:
            candidates.append((v2 - v1, f"({e2} - {e1})"))
        if v2 != 0 and v1 % v2 == 0:
            candidates.append((v1 // v2, f"({e1} / {e2})"))
        if v1 != 0 and v2 % v1 == 0:
            candidates.append((v2 // v1, f"({e2} / {e1})"))
        for new_val, new_expr in candidates:
            new_pool = remaining + [(new_val, new_expr)]
            result = solve(new_pool, target)
            if result is not None:
                return result
    return None
```

#### Usage Example
```python
result = solve([(1, "1"), (2, "2"), (4, "4")], 7)
# Returns ("(1 + (2 * 4))", 7) or similar
```

---

### main

**Signature:**
```python
def main() -> None
```

**Purpose:** Parses command-line arguments and initiates the solver.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | Reads directly from `sys.argv`. |

**Returns:**
| Type | Description |
|------|-------------|
| None | Outputs results directly to standard output. |

**Source Code:**
```python
def main():
    if len(sys.argv) < 3:
        print("Usage: python countdown.py <target> <n1> <n2> ... <nk>")
        sys.exit(1)
    target = int(sys.argv[1])
    numbers = [(int(x), str(x)) for x in sys.argv[2:]]
    result = solve(numbers, target)
    if result is not None:
        expr, value = result
        if expr.startswith("(") and expr.endswith(")"):
            expr = expr[1:-1]
        print(f"Expression: {expr}")
        print(f"Value: {value}")
    else:
        print("No solution could be generated.")
```

**Implementation (Executable Logic Only):**
* **Line 0:** `sys.argv check` — Validates that a target and at least one number are provided.
* **Line 1:** `target/numbers parsing` — Converts string arguments into a usable pool of tuples.
* **Line 2:** `solve() call` — Initiates the recursive search.
* **Line 3:** `result formatting` — Cleans up the expression string (stripping outer parentheses) and prints the outcome.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| sys.argv | External | CLI Argument access | sys |
| sys.exit | External | Error termination | sys |
| int | Built-in | String to Integer conversion | Python |
| solve | Internal | Solver logic | countdown.py |
