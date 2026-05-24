import sys
from itertools import combinations
import ast


def simplify_outer(expr):
    """Removes the outermost parentheses from an expression if they are matching.
    
    Args:
        expr (str): The expression string.
        
    Returns:
        str: The simplified expression string.
    """
    while expr.startswith("(") and expr.endswith(")"):
        try:
            # Check if the inner content is a valid standalone expression
            ast.parse(expr[1:-1])
            expr = expr[1:-1]
        except SyntaxError:
            break
    return expr

def solve(pool, target):
    """Solves the Countdown numbers game recursively using a tree search.

    Args:
        pool (list[tuple[int, str]]): A list of tuples containing current numbers and their expression strings.
        target (int): The target value to reach.

    Returns:
        tuple[str, int] | None: A tuple containing the valid expression string and its evaluated value,
            or None if no solution is found.
    """
    for val, expr in pool:
        if val == target:
            expr = simplify_outer(expr)
            return expr, val

    if len(pool) < 2:
        return None

    for (v1, e1), (v2, e2) in combinations(pool, 2):
        remaining = list(pool)
        remaining.remove((v1, e1))
        remaining.remove((v2, e2))

        ops = [
            (v1 + v2, f"({e1} + {e2})"),
            (v1 * v2, f"({e1} * {e2})"),
            (v1 - v2, f"({e1} - {e2})"),
            (v2 - v1, f"({e2} - {e1})"),
            (v1 // v2 if v2 and v1 % v2 == 0 else 0, f"({e1} / {e2})"),
            (v2 // v1 if v1 and v2 % v1 == 0 else 0, f"({e2} / {e1})"),
        ]

        for val, expr in ops:
            if val <= 0:
                continue
            res = solve(remaining + [(val, expr)], target)
            if res:
                return res
    return None


def main():
    """Parses command-line arguments and runs the solver.

    Returns:
        None: Prints the solver results to standard output.
    """
    if len(sys.argv) < 3:
        return print("Usage: python countdown.py <target> <n1> <n2> ... <nk>")

    target = int(sys.argv[1])
    numbers = [(int(x), x) for x in sys.argv[2:]]
    res = solve(numbers, target)

    print(
        f"Expression: {res[0]}\nValue: {res[1]}"
        if res
        else "No solution could be generated."
    )


if __name__ == "__main__":
    main()