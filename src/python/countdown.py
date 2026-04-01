
"""Countdown numbers game solver.

Finds an arithmetic expression using given numbers to reach a target value.
Uses a recursive tree-based search exploring all valid combinations.
"""

import sys
from itertools import combinations


def solve(pool, target):
    """Search for an expression evaluating to target.

    Args:
        pool (list): List of (value, expression_string) tuples.
        target (int): The target number to reach.

    Returns:
        tuple: (expression_string, value) if found, else None.
    """
    # Check if any single number matches the target
    for val, expr in pool:
        if val == target:
            return expr, val

    # Need at least 2 numbers to combine
    if len(pool) < 2:
        return None

    # Try all pairs with all operations
    for i, j in combinations(range(len(pool)), 2):
        v1, e1 = pool[i]
        v2, e2 = pool[j]

        # Build remaining pool (excluding the two picked numbers)
        remaining = [pool[k] for k in range(len(pool)) if k != i and k != j]

        # Define all valid operations
        candidates = [
            (v1 + v2, f"({e1} + {e2})"),
            (v1 * v2, f"({e1} * {e2})"),
        ]

        # Subtraction: only if result is positive
        if v1 - v2 > 0:
            candidates.append((v1 - v2, f"({e1} - {e2})"))
        if v2 - v1 > 0:
            candidates.append((v2 - v1, f"({e2} - {e1})"))

        # Division: only if exact integer result
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


def main():
    """Parse CLI arguments and run the solver."""
    if len(sys.argv) < 3:
        print("Usage: python countdown.py <target> <n1> <n2> ... <nk>")
        sys.exit(1)

    target = int(sys.argv[1])
    numbers = [(int(x), str(x)) for x in sys.argv[2:]]

    result = solve(numbers, target)

    if result is not None:
        expr, value = result
        # Strip outermost parentheses for cleaner display
        if expr.startswith("(") and expr.endswith(")"):
            expr = expr[1:-1]
        print(f"Expression: {expr}")
        print(f"Value: {value}")
    else:
        print("No solution could be generated.")


if __name__ == "__main__":
    main()