# countdown.pl Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [combine](#combine) | Predicate | Generates a valid arithmetic operation result. |
| [solve](#solve) | Predicate | Succeeds when an expression evaluating to Target is found. |
| [fmt](#fmt) | Predicate | Formats an expression tree into a human-readable string. |
| [op_char](#op_char) | Predicate | Maps operators to their character representations. |
| [num_to_node](#num_to_node) | Predicate | Helper to convert a number to a node. |
| [main](#main) | Predicate | Entry point called by run_all.sh to solve and display. |
| [run](#run) | Predicate | Entry point for the SWI-Prolog interpreter. |

## Overview
This file implements a goal-driven logic solver for the Countdown numbers game using SWI-Prolog. It utilizes Prolog's native backtracking and constraint-based logic to find a valid sequence of arithmetic operations (`add`, `sub`, `mul`, `div`) from a list of given integers to reach a target value.

## Detailed Breakdown

### combine

**Signature:**
```prolog
combine(EA: term, VA: int, EB: term, VB: int, OpExpr: term, OpVal: int) -> boolean
```

**Purpose:** Generates a valid arithmetic operation result and enforces game rules.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| EA | term | Yes | — | First expression tree. |
| VA | int | Yes | — | First value. |
| EB | term | Yes | — | Second expression tree. |
| VB | int | Yes | — | Second value. |
| OpExpr | term | No | output | Output combined expression tree. |
| OpVal | int | No | output | Output evaluated integer value. |

**Returns:**
| Type | Description |
|------|-------------|
| boolean | Succeeds if the combination is mathematically valid. |

**Source Code:**
```prolog
combine(EA, VA, EB, VB, add(EA, EB), V) :- VA =< VB, V is VA + VB.
combine(EA, VA, EB, VB, sub(EA, EB), V) :- VA > VB, V is VA - VB.
combine(EA, VA, EB, VB, mul(EA, EB), V) :- VA =< VB, V is VA * VB, V > 1.
combine(EA, VA, EB, VB, div(EA, EB), V) :- VB > 1, 0 is VA mod VB, V is VA // VB.
```

**Implementation (Executable Logic Only):**
* **Line 7:** `add` — Commutative constraint (`VA =< VB`).
* **Line 8:** `sub` — Requires strictly positive result (`VA > VB`).
* **Line 9:** `mul` — Commutative constraint (`VA =< VB`) and excludes multiplying by 1 (`V > 1`).
* **Line 10:** `div` — Excludes dividing by 1 (`VB > 1`), check for no modulo remainder, and performs integer division.

---

### solve

**Signature:**
```prolog
solve(Pool: list, Target: int, Expr: term) -> boolean
```

**Purpose:** Succeeds when an expression evaluating to Target is found.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Pool | list | Yes | — | List of node(Expr, Value) structures. |
| Target | int | Yes | — | Target value to search for. |
| Expr | term | No | output | Output winning expression tree. |

**Returns:**
| Type | Description |
|------|-------------|
| boolean | Succeeds if the target is reachable. |

**Source Code:**
```prolog
solve(Pool, Target, Expr) :-
    member(node(Expr, Target), Pool).
solve(Pool, Target, Expr) :-
    select(node(EA, VA), Pool, P1),
    select(node(EB, VB), P1, Rest),
    combine(EA, VA, EB, VB, NewExpr, NewVal),
    solve([node(NewExpr, NewVal) | Rest], Target, Expr).
```

**Implementation (Executable Logic Only):**
* **Line 13:** `Base case` — Succeeds if any node in `Pool` matches `Target`.
* **Line 15:** `Recursive step` — Non-deterministically selects two elements, combines them using `combine`, inserts new node, and recurses.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| member/2 | External | Check list membership | library(lists) |
| select/3 | External | Select elements from list | library(lists) |
| combine | Internal | Form candidate operations | countdown.pl |

---

### fmt

**Signature:**
```prolog
fmt(Expr: term, Formatted: string) -> boolean
```

**Purpose:** Formats an expression tree into a human-readable parenthesized string.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Expr | term | Yes | — | Expression tree node. |
| Formatted | string | No | output | Output formatted string. |

**Returns:**
| Type | Description |
|------|-------------|
| boolean | Succeeds if formatting is successful. |

**Source Code:**
```prolog
fmt(val(V), S) :- !, number_string(V, S).
fmt(Expr, S) :-
    Expr =.. [Op, L, R],
    op_char(Op, C),
    fmt(L, LS),
    fmt(R, RS),
    atomic_list_concat(['(', LS, ' ', C, ' ', RS, ')'], S).
```

**Implementation (Executable Logic Only):**
* **Line 22:** `val(V)` — Base case conversion using `number_string`. Cut `!` prevents backtracking.
* **Line 23:** `Expr =.. [Op, L, R]` — Univ operator unpacks term.
* **Line 28:** `atomic_list_concat` — Concatenates formatted sub-expressions with operator char.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| number_string/2 | Built-in | Convert number to string | SWI-Prolog |
| atomic_list_concat/2 | Built-in | Concatenate atomic terms | SWI-Prolog |
| op_char | Internal | Get operator character representation | countdown.pl |

---

### op_char

**Signature:**
```prolog
op_char(OpName: atom, Char: atom) -> boolean
```

**Purpose:** Maps operator names to their character representations.

**Source Code:**
```prolog
op_char(add, +).
op_char(sub, -).
op_char(mul, *).
op_char(div, /).
```

---

### num_to_node

**Signature:**
```prolog
num_to_node(N: int, Node: term) -> boolean
```

**Purpose:** Helper to convert a number to a node.

**Source Code:**
```prolog
num_to_node(N, node(val(N), N)).
```

---

### main

**Signature:**
```prolog
main(Target: int, Numbers: list) -> boolean
```

**Purpose:** Entry point called by run_all.sh to solve and display the result.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Target | int | Yes | — | Target value. |
| Numbers | list | Yes | — | Pool of available numbers. |

**Source Code:**
```prolog
main(Target, Numbers) :-
    run([Target | Numbers]).
```

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| run | Internal | Runs solver and prints outputs | countdown.pl |

---

### run

**Signature:**
```prolog
run(Args: list) -> boolean
```

**Purpose:** Entry point for the SWI-Prolog interpreter.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Args | list | Yes | — | Argument list where first element is target. |

**Source Code:**
```prolog
run(Args) :-
    Args = [Target | Numbers],
    maplist(num_to_node, Numbers, Pool),
    (   solve(Pool, Target, Expr)
    ->  fmt(Expr, S),
        format('Expression: ~s~n', [S]),
        format('Value: ~d~n', [Target])
    ;   format('No solution could be generated.~n', [])
    ).
```

**Implementation (Executable Logic Only):**
* **Line 44:** `Args unpacking` — Splitting list to Target and Numbers.
* **Line 45:** `maplist` — Generates initial `Pool` of nodes.
* **Line 46:** `solve` — Attempts to find target in pool.
* **Line 47:** `fmt` — Formats winning expression string if found.
* **Line 48:** `format` — Prints solution expression and value, or failure.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| maplist/3 | External | Map list using predicate | SWI-Prolog |
| format/2 | Built-in | Print formatted outputs | SWI-Prolog |
| solve | Internal | Recursive solver | countdown.pl |
| fmt | Internal | Formatter | countdown.pl |
