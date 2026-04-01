# countdown_pl.pl Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [evaluate](#evaluate) | Predicate | Core logic to calculate the result of an arithmetic tree structure. |
| [format_expr](#format_expr) | Predicate | Formats a complex tree into a nested parenthetical string. |
| [valid_state](#valid_state) | Predicate | Main backtracking search engine for the solver. |
| [combine](#combine) | Predicate | Logic for choosing and validating one binary arithmetic step. |
| [main](#main) | Predicate | Entry point for shell-based execution. |

## Overview
This file implements a goal-driven logic solver for the Countdown numbers game using SWI-Prolog. It utilizes Prolog's native backtracking and constraint-based logic to find a valid sequence of arithmetic operations (`add`, `sub`, `mul`, `div`) from a list of given integers to reach a target value.

## Detailed Breakdown

### evaluate

**Signature:**
```prolog
evaluate(Expr: term, Value: int) -> boolean
```

**Purpose:** Calculates the final integer value from an `Expr` tree.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Expr | term | Yes | — | An arithmetic tree using `add`, `sub`, etc. |
| Value | int | Yes | — | The resulting integer value. |

**Returns:**
| Type | Description |
|------|-------------|
| boolean | Succeeds if the calculation is valid. |

**Source Code:**
```prolog
evaluate(val(V), V).
evaluate(add(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    V is VL + VR.
evaluate(sub(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    VL > VR,
    V is VL - VR.
evaluate(mul(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    V is VL * VR.
evaluate(div(L, R), V) :-
    evaluate(L, VL),
    evaluate(R, VR),
    VR =\= 0,
    VL mod VR =:= 0,
    V is VL // VR.
```

**Implementation (Executable Logic Only):**
* **Line 0:** `val base case` — Unifies the integer value directly.
* **Line 1:** `add recursion` — Recursively evaluates both branches and sums.
* **Line 2:** `sub recursion` — Requires `VL > VR` to ensure a positive integer result.
* **Line 3:** `mul recursion` — Recursively evaluates both branches and multiplies.
* **Line 4:** `div recursion` — Requires `VR =\= 0` and `VL mod VR =:= 0` for exact integer division.

---

### valid_state

**Primary Library:** `library(lists)`  
**Purpose:** Backtracking engine that explores all possible states of the number pool.

#### Overview
This predicate uses backtracking to either identify the target in the current pool or generate a new pool by combining two numbers. It is the heart of the solver's non-deterministic search.

#### Signature
```prolog
valid_state(Pool: list, Target: int, Expr: term) -> boolean
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Pool | list | Yes | — | List of `node(Expr, Value)` terms. |
| Target | int | Yes | — | The integer to reach. |
| Expr | term | No | output | The resulting expression tree found. |

#### Returns
| Type | Description |
|------|-------------|
| boolean | Succeeds if a path to the target is found. |

#### Dependencies
* **Required Libraries:** `select/3` (Removing elements from the list)
* **Internal Modules:** `combine/6`, `valid_state/3` (Recursion)

#### Workflow (Executable Logic Only)

**Phase 1: Target Identification**
* **Operation 1:** Use `member/2` to check if any node in the `Pool` already matches the `Target`.
* **Operation 2:** If found, unify the output `Expr` and terminate successfully.

**Phase 3: Recursive Combination**
* **Operation 1:** Select two nodes `EA, EB` from the pool using `select/3`.
* **Operation 2:** Call `combine` to perform an arithmetic operation and get `CombinedExpr` and `CombinedValue`.
* **Operation 3:** Call `valid_state` recursively with a new pool containing the combined result and the remaining nodes.

#### Source Code
```prolog
valid_state(Pool, Target, Expr) :-
    member(node(Candidate, Value), Pool),
    Value =:= Target,
    Expr = Candidate.
valid_state(Pool, Target, Expr) :-
    length(Pool, Len),
    Len >= 2,
    select(node(EA, VA), Pool, Pool1),
    select(node(EB, VB), Pool1, Rest),
    combine(VA, VB, EA, EB, CombinedExpr, CombinedValue),
    valid_state([node(CombinedExpr, CombinedValue) | Rest], Target, Expr).
```
