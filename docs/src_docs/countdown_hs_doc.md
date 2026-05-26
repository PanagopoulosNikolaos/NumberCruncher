# countdown_hs.hs Documentation

## Navigation Table

| Name | Type | Description |
|------|------|-------------|
| [Op](#Op) | Data Type | Represents basic arithmetic operators. |
| [Expr](#Expr) | Data Type | Models an arithmetic calculation tree. |
| [eval](#eval) | Function | Evaluates an expression tree to its integer result. |
| [formatExpr](#formatExpr) | Function | Formats an expression tree as a human-readable string. |
| [candidates](#candidates) | Function | Generates valid operation results from two (value, expr) pairs. |
| [select2](#select2) | Function | Selects all pairs of elements from a list, returning them and remaining elements. |
| [select1](#select1) | Function | Selects one element from a list, returning it and remaining elements. |
| [solve](#solve) | Function | Recursive solver that tries all pair combinations to reach the target. |
| [main](#main) | Function | Main entry point. |

## Overview
This file implements a purely functional solver for the Countdown numbers game in Haskell. It uses an expression tree representation (`Expr`) and recursive search to explore the solution space, ensuring all arithmetic operations follow game restrictions (positive results, integer-only division).

## Detailed Breakdown

### Op

**Class Responsibility:** Algebraic data type representing arithmetic addition, subtraction, multiplication, and division operations.

### Expr

**Class Responsibility:** Algebraic data type modeling an expression tree, consisting of either literal leaf values (`Val Int`) or nested applications of operations (`App Op Expr Expr`).

---

### eval

**Signature:**
```haskell
eval :: Expr -> Int
```

**Purpose:** Evaluates an expression tree to its integer result.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| expr | Expr | Yes | — | The expression tree to evaluate. |

**Returns:**
| Type | Description |
|------|-------------|
| Int | The final integer value. |

**Source Code:**
```haskell
eval (Val n) = n
eval (App Add l r) = eval l + eval r
eval (App Sub l r) = eval l - eval r
eval (App Mul l r) = eval l * eval r
eval (App Div l r) = eval l `div` eval r
```

**Implementation (Executable Logic Only):**
* **Line 12:** `eval (Val n) = n` — Returns value of a leaf node.
* **Line 13:** `eval (App Add l r) = ...` — Recursively evaluates and adds.
* **Line 14:** `eval (App Sub l r) = ...` — Recursively evaluates and subtracts.
* **Line 15:** `eval (App Mul l r) = ...` — Recursively evaluates and multiplies.
* **Line 16:** `eval (App Div l r) = ...` — Recursively evaluates and divides.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| div | Built-in | Integer division | Haskell |

---

### formatExpr

**Signature:**
```haskell
formatExpr :: Expr -> String
```

**Purpose:** Formats an expression tree as a readable string with parentheses.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| expr | Expr | Yes | — | The expression tree to format. |

**Returns:**
| Type | Description |
|------|-------------|
| String | The formatted string representation. |

**Source Code:**
```haskell
formatExpr (Val n) = show n
formatExpr (App op l r) = "(" ++ formatExpr l ++ " " ++ sym op ++ " " ++ formatExpr r ++ ")"
  where sym Add = "+"; sym Sub = "-"; sym Mul = "*"; sym Div = "/"
```

**Implementation (Executable Logic Only):**
* **Line 20:** `formatExpr (Val n) = show n` — Show leaf value.
* **Line 21:** `formatExpr (App op l r) = ...` — Concatenates subexpressions within parentheses.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| show | Built-in | String conversion | Haskell |

---

### candidates

**Signature:**
```haskell
candidates :: (Int, Expr) -> (Int, Expr) -> [(Int, Expr)]
```

**Purpose:** Generates all valid operation results from two (value, expr) pairs.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| pair1 | (Int, Expr) | Yes | — | First operand pair. |
| pair2 | (Int, Expr) | Yes | — | Second operand pair. |

**Returns:**
| Type | Description |
|------|-------------|
| [(Int, Expr)] | List of all mathematically valid candidate results. |

**Source Code:**
```haskell
candidates (x, l) (y, r) = 
  [(x + y, App Add l r), (x * y, App Mul l r)] ++
  [(x - y, App Sub l r) | x > y] ++
  [(y - x, App Sub r l) | y > x] ++
  [(x `div` y, App Div l r) | y /= 0, x `mod` y == 0] ++
  [(y `div` x, App Div r l) | x /= 0, y `mod` x == 0]
```

**Implementation (Executable Logic Only):**
* **Line 27:** `Addition & Multiplication` — Unconditionally candidate.
* **Line 28:** `Subtraction (x - y)` — Guards that result must be positive (`x > y`).
* **Line 29:** `Subtraction (y - x)` — Guards that result must be positive (`y > x`).
* **Line 30:** `Division (x / y)` — Guards against division by zero and requires exact division (`mod == 0`).
* **Line 31:** `Division (y / x)` — Guards against division by zero and requires exact division (`mod == 0`).

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| div | Built-in | Integer division | Haskell |
| mod | Built-in | Modulo division | Haskell |

---

### select2

**Signature:**
```haskell
select2 :: [a] -> [(a, a, [a])]
```

**Purpose:** Selects all pairs of elements from a list, returning them and the remaining elements.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| list | [a] | Yes | — | Input list. |

**Returns:**
| Type | Description |
|------|-------------|
| [(a, a, [a])] | List of tuples with two selected items and the remaining list. |

**Source Code:**
```haskell
select2 [] = []
select2 (x:xs) = [(x, y, ys) | (y, ys) <- select1 xs] ++ [(y, z, x:ys) | (y, z, ys) <- select2 xs]
```

**Implementation (Executable Logic Only):**
* **Line 35:** `Base case` — Returns empty list for empty input.
* **Line 36:** `Recursive selection` — Selects `x` and pairs it with all selections from `xs` using `select1`, then recurses on `xs`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| select1 | Internal | Helper list selection | countdown.hs |

---

### select1

**Signature:**
```haskell
select1 :: [a] -> [(a, [a])]
```

**Purpose:** Selects one element from a list, returning it and the remaining elements.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| list | [a] | Yes | — | Input list. |

**Returns:**
| Type | Description |
|------|-------------|
| [(a, [a])] | List of tuples with one selected item and the rest of the list. |

**Source Code:**
```haskell
select1 [] = []
select1 (x:xs) = (x, xs) : [(y, x:ys) | (y, ys) <- select1 xs]
```

**Implementation (Executable Logic Only):**
* **Line 40:** `Base case` — Returns empty list for empty input.
* **Line 41:** `Recursive selection` — Pair `x` with `xs`, then recursively prepend `x` to remaining lists of subsequent elements.

---

### solve

**Signature:**
```haskell
solve :: Int -> [(Int, Expr)] -> Maybe Expr
```

**Purpose:** Recursive solver that tries all pair combinations to reach the target.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| target | Int | Yes | — | Target value. |
| pool | [(Int, Expr)] | Yes | — | Current pool of active expressions. |

**Returns:**
| Type | Description |
|------|-------------|
| Maybe Expr | `Just` the valid expression if found; otherwise, `Nothing`. |

**Source Code:**
```haskell
solve target pool 
  | not (null hits) = Just (head hits)
  | otherwise = listToMaybe $ mapMaybe (solve target) 
      [ (v, e) : rest | (a, b, rest) <- select2 pool, (v, e) <- candidates a b ]
  where hits = [e | (v, e) <- pool, v == target]
```

**Implementation (Executable Logic Only):**
* **Line 46:** `hits check` — Returns first hit if target is directly present in the pool.
* **Line 47:** `otherwise recursion` — Non-deterministically combines pairs using `select2` and `candidates`, then maps `solve` over resulting states, picking the first success via `listToMaybe`.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| listToMaybe | External | Gets first element of list as Maybe | Data.Maybe |
| mapMaybe | External | Maps a function returning Maybe over list | Data.Maybe |
| select2 | Internal | Select pairs from list | countdown.hs |
| candidates | Internal | Calculate pairs combinations | countdown.hs |

---

### main

**Signature:**
```haskell
main :: IO ()
```

**Purpose:** Main entry point.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| None | — | — | — | Reads program arguments. |

**Returns:**
| Type | Description |
|------|-------------|
| IO () | Outputs solved expression or failure. |

**Source Code:**
```haskell
main = do
  args <- getArgs
  case map read args of
    (target:nums) -> case solve target [(n, Val n) | n <- nums] of
      Just expr -> putStrLn $ "Expression: " ++ formatExpr expr ++ "\nValue: " ++ show (eval expr)
      Nothing   -> putStrLn "No solution could be generated."
    _ -> putStrLn "Usage: countdown <target> <n1> <n2> ..."
```

**Implementation (Executable Logic Only):**
* **Line 54:** `args <- getArgs` — Reads program arguments.
* **Line 55:** `map read args` — Parses target and input numbers list.
* **Line 56:** `solve target ...` — Invokes recursive search.
* **Line 57:** `putStrLn` — Outputs formatted expression and verified value.

**Dependencies:**
| Symbol | Kind | Purpose | Source |
|--------|------|---------|--------|
| getArgs | External | Get CLI arguments | System.Environment |
| putStrLn | Built-in | Print line to stdout | Haskell |
| show | Built-in | Format value to string | Haskell |
| solve | Internal | Recursive solver | countdown.hs |
| formatExpr | Internal | Expression formatter | countdown.hs |
| eval | Internal | Expression evaluator | countdown.hs |
