# countdown_hs.hs Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [Expr](#Expr) | Data Type | Recursive data structure representing an arithmetic expression. |
| [eval](#eval) | Function | Evaluates an `Expr` tree to its integer result. |
| [formatExpr](#formatExpr) | Function | Formats an `Expr` tree into a human-readable string. |
| [candidates](#candidates) | Function | Generates valid results from a pair of arithmetic operands. |
| [solve](#solve) | Function | Entry point for the recursive solver logic. |
| [findInPairs](#findInPairs) | Function | Orchestration function for pair selection and recursive calls. |
| [main](#main) | Function | CLI handler for Haskell binary execution. |

## Overview
This file implements a purely functional solver for the Countdown numbers game in Haskell. It uses an expression tree representation (`Expr`) and recursive search to explore the solution space, ensuring all arithmetic operations follow game restrictions (positive results, integer-only division).

## Detailed Breakdown

### Expr

**Class Responsibility:** A recursive algebraic data type that models an arithmetic calculation. It supports integer values and basic binary operators (Add, Sub, Mul, Div), which together construct the tree structure used during search.

### Constructor
* **Val (Int):** Represents a literal integer value.
* **Add (Expr, Expr):** Represents an addition operator.
* **Sub (Expr, Expr):** Represents a subtraction operator.
* **Mul (Expr, Expr):** Represents a multiplication operator.
* **Div (Expr, Expr):** Represents a division operator.

---

### eval

**Signature:**
```haskell
eval :: Expr -> Int
```

**Purpose:** Recursively calculates the integer result of an expression tree.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| expr | Expr | Yes | — | The tree to evaluate. |

**Returns:**
| Type | Description |
|------|-------------|
| Int | The final integer value. |

**Source Code:**
```haskell
eval (Val n)    = n
eval (Add l r)  = eval l + eval r
eval (Sub l r)  = eval l - eval r
eval (Mul l r)  = eval l * eval r
eval (Div l r)  = eval l `div` eval r
```

**Implementation (Executable Logic Only):**
* **Line 0:** `base case` — Returns the integer value if the node is `Val`.
* **Line 1:** `recursion` — Recursively evaluates left and right branches and applies the corresponding infix operator.

---

### candidates

**Signature:**
```haskell
candidates :: (Int, Expr) -> (Int, Expr) -> [(Int, Expr)]
```

**Purpose:** Generates all valid results (value and tree) from two source numbers.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| operand1 | (Int, Expr) | Yes | — | Value and expression tree for the first operand. |
| operand2 | (Int, Expr) | Yes | — | Value and expression tree for the second operand. |

**Returns:**
| Type | Description |
|------|-------------|
| [(Int, Expr)] | A list of all valid combinations. |

**Source Code:**
```haskell
candidates (v1, e1) (v2, e2) =
    [ (v1 + v2, Add e1 e2)
    , (v1 * v2, Mul e1 e2)
    ]
    ++ [ (v1 - v2, Sub e1 e2) | v1 > v2 ]
    ++ [ (v2 - v1, Sub e2 e1) | v2 > v1 ]
    ++ [ (v1 `div` v2, Div e1 e2) | v2 /= 0, v1 `mod` v2 == 0 ]
    ++ [ (v2 `div` v1, Div e2 e1) | v1 /= 0, v2 `mod` v1 == 0 ]
```

**Implementation (Executable Logic Only):**
* **Line 0:** `list comprehension` — Produces results while filtering for positive subtraction results and integer division results using guard conditions.

---

### findInPairs

**Primary Library:** Standard Library  
**Purpose:** Iterates through every possible pair in the pool and recurses down the search tree.

#### Overview
This function uses list comprehensions to select pairs of elements by their indices. For each pair, it uses the `candidates` function to generate new possible branches and then calls `solve` to see if those branches reach the target. It leverages a helper `firstJust` to stop at the first solution found.

#### Signature
```haskell
findInPairs :: Int -> [(Int, Expr)] -> Maybe Expr
```

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| target | Int | Yes | — | The value to find. |
| pool | [(Int, Expr)] | Yes | — | The list of current number/expression pairs. |

#### Returns
| Type | Description |
|------|-------------|
| Maybe Expr | `Just` the result tree if successful, otherwise `Nothing`. |

#### Raise
| Exception | Condition |
|-----------|-----------|
| None | Handled via `Maybe` type. |

#### Dependencies
* **Required Libraries:** `removeAt` (List manipulation)
* **Internal Modules:** `solve`, `candidates`

#### Workflow (Executable Logic Only)

**Phase 1: Index-based Pair Selection**
* **Operation 1:** Select `i` from `[0 .. length pool - 1]`.
* **Operation 2:** Select `j` from `[i + 1 .. length pool - 1]` to avoid reversing pairs.
* **Operation 3:** Remove elements at `i` and `j` to form the `rest` list.

**Phase 2: Combination Generation**
* **Operation 1:** Call `candidates (v1, e1) (v2, e2)` for the selected pair.

**Phase 3: Deep Recursion**
* **Operation 1:** For each candidate `(v, e)`, call `solve target ((v, e) : rest)`.
* **Operation 2:** Use `firstJust` to traverse the list of results and return the first non-`Nothing` value.

#### Source Code
```haskell
findInPairs target pool = firstJust $ do
    i <- [0 .. length pool - 1]
    j <- [i + 1 .. length pool - 1]
    let (v1, e1) = pool !! i
        (v2, e2) = pool !! j
        rest = removeAt (removeAt pool i) $ if j > i then j - 1 else j
    (v, e) <- candidates (v1, e1) (v2, e2)
    return $ solve target ((v, e) : rest)
  where
    firstJust [] = Nothing
    firstJust (Nothing:xs) = firstJust xs
    firstJust (Just x:_) = Just x
```
