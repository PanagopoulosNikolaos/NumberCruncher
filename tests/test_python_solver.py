"""Unit tests for the Python solver implementation of the Countdown game.

Verifies the recursive search logic against various difficulty levels and
boundary conditions.
"""

import sys
import os
import unittest

# Insert Python source directory to the beginning of import path to prevent naming collisions.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/python")))
import countdown


class TestPythonSolver(unittest.TestCase):
    """
    Tests the recursive tree-search solver implemented in Python.

    Evaluates the correctness of the solver's output, verification of math rules,
    and handling of edge cases.
    """

    def testDirectMatch(self) -> None:
        """
        Tests when the target is directly present in the input numbers.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 10
        numbers_pool = [(10, "10"), (2, "2"), (3, "3")]  # Simple pool with target present.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 10)  # Value matches target.
            self.assertEqual(expr_str, "10")  # Direct expression is the value.

    def testVeryEasyCase(self) -> None:
        """
        Tests the solver with a very easy combination of numbers.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 10
        numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4")]  # Sum equals 10.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 10)
            self.assertEqual(eval(expr_str), 10)  # Expression evaluates to 10.

    def testEasyCase(self) -> None:
        """
        Tests the solver with an easy combination of numbers.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 50
        numbers_pool = [(2, "2"), (3, "3"), (5, "5"), (10, "10"), (25, "25")]  # Multiplication leads to target.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 50)
            self.assertEqual(eval(expr_str), 50)

    def testMediumCase(self) -> None:
        """
        Tests the solver with a medium difficulty game.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 123
        numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (25, "25")]  # Requires multiple operations.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 123)
            self.assertEqual(eval(expr_str), 123)

    def testHardCase(self) -> None:
        """
        Tests the solver with a hard difficulty game.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 456
        numbers_pool = [(1, "1"), (3, "3"), (5, "5"), (10, "10"), (25, "25"), (50, "50")]
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 456)
            self.assertEqual(eval(expr_str), 456)

    def testVeryHardCase(self) -> None:
        """
        Tests the solver with a very hard difficulty game.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 987
        numbers_pool = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (75, "75"), (100, "100")]
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 987)
            self.assertEqual(eval(expr_str), 987)

    def testNoSolution(self) -> None:
        """
        Tests behavior when no valid solution can be constructed.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 999
        numbers_pool = [(2, "2"), (2, "2")]  # Impossible to reach 999.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)

    def testSingleElementPool(self) -> None:
        """
        Tests behavior when the pool has only one element which is not the target.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 10
        numbers_pool = [(5, "5")]  # Single element not matching target.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)

    def testEmptyPool(self) -> None:
        """
        Tests behavior when the input pool is empty.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 10
        numbers_pool = []  # Empty input pool.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)

    def testSubtractionConstraint(self) -> None:
        """
        Tests that subtraction only occurs if the result is strictly positive.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 1
        numbers_pool = [(2, "2"), (3, "3")]  # 3-2 = 1 (positive subtraction).
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 1)
            self.assertIn("-", expr_str)  # Subtraction must be utilized.
            self.assertNotIn("2 - 3", expr_str)  # Negative result subtraction is prohibited.

    def testDivisionConstraint(self) -> None:
        """
        Tests that division only occurs if the result is an exact integer.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 2
        numbers_pool = [(10, "10"), (4, "4")]  # 10/4 = 2.5 (non-integer division).
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNone(result)  # Non-integer division is prohibited, so no solution exists.

    def testDuplicateNumbers(self) -> None:
        """
        Tests that duplicate input numbers are handled correctly.

        Returns:
            None (None): The output is validated via assertions.
        """
        target_val = 10
        numbers_pool = [(5, "5"), (5, "5")]  # Two identical values.
        result = countdown.solve(numbers_pool, target_val)
        self.assertIsNotNone(result)
        if result is not None:
            expr_str, val_str = result
            self.assertEqual(val_str, 10)
            self.assertEqual(eval(expr_str), 10)


if __name__ == "__main__":
    unittest.main()
