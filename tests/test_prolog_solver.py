"""Integration tests for the Prolog implementation of the Countdown game solver.

Executes subprocess integration tests using SWI-Prolog ('swipl') for various
difficulties and edge cases.
"""

import os
import shutil
import subprocess
import unittest

# Check if swipl is available in system PATH.
HAS_PROLOG = shutil.which("swipl") is not None


@unittest.skipIf(not HAS_PROLOG, "SWI-Prolog (swipl) is not installed.")
class TestPrologSolver(unittest.TestCase):
    """
    Tests the SWI-Prolog solver implementation.

    Verifies solution correctness, logic constraints, and edge case responses
    via swipl subprocess execution.
    """

    def runSolver(self, target: int, numbers: list) -> tuple:
        """
        Runs the Prolog solver with the given target and numbers.

        Args:
            target (int): Target sum to construct.
            numbers (list): Available input numbers.

        Returns:
            tuple (tuple): (success_status, expression, value) representing solver results.
        """
        prolog_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/prolog/countdown.pl"))
        prolog_list = "[" + ",".join(map(str, numbers)) + "]"

        cmd_args = [
            "swipl",
            "-s", prolog_file,
            "-g", f"main({target}, {prolog_list}), halt."
        ]

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

    def testDirectMatch(self) -> None:
        """
        Tests when the target is directly present in the input numbers.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(10, [10, 2, 3])
        self.assertTrue(success)
        self.assertEqual(val, "10")
        self.assertIn("10", expr)

    def testVeryEasyCase(self) -> None:
        """
        Tests solver with very easy combinations of numbers.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(10, [1, 2, 3, 4])
        self.assertTrue(success)
        self.assertEqual(val, "10")
        # Parse the Prolog expression tree and evaluate in Python context.
        self.assertEqual(int(eval(expr)), 10)

    def testEasyCase(self) -> None:
        """
        Tests solver with easy combinations of numbers.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(50, [2, 3, 5, 10, 25])
        self.assertTrue(success)
        self.assertEqual(val, "50")
        self.assertEqual(int(eval(expr)), 50)

    def testMediumCase(self) -> None:
        """
        Tests solver with medium difficulty parameters.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(123, [1, 2, 3, 4, 25])
        self.assertTrue(success)
        self.assertEqual(val, "123")
        self.assertEqual(int(eval(expr)), 123)

    def testHardCase(self) -> None:
        """
        Tests solver with hard difficulty parameters.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(456, [1, 3, 5, 10, 25, 50])
        self.assertTrue(success)
        self.assertEqual(val, "456")
        self.assertEqual(int(eval(expr)), 456)

    def testVeryHardCase(self) -> None:
        """
        Tests solver with very hard difficulty parameters.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(987, [1, 2, 3, 4, 75, 100])
        self.assertTrue(success)
        self.assertEqual(val, "987")
        self.assertEqual(int(eval(expr)), 987)

    def testNoSolution(self) -> None:
        """
        Tests solver behavior when no solution exists.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(999, [2, 2])
        self.assertFalse(success)
        self.assertEqual(expr, "")
        self.assertEqual(val, "")

    def testSubtractionConstraint(self) -> None:
        """
        Tests that subtraction only evaluates to positive values.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(1, [2, 3])
        self.assertTrue(success)
        self.assertEqual(val, "1")
        self.assertIn("-", expr)
        self.assertNotIn("2 - 3", expr)

    def testDivisionConstraint(self) -> None:
        """
        Tests that division only evaluates to exact integers.

        Returns:
            None (None): Verified via assertion checks.
        """
        # 10 / 4 is non-integer, so no solution should be possible.
        success, expr, val = self.runSolver(2, [10, 4])
        self.assertFalse(success)

    def testDuplicateNumbers(self) -> None:
        """
        Tests correct evaluation when duplicate values are present.

        Returns:
            None (None): Verified via assertion checks.
        """
        success, expr, val = self.runSolver(10, [5, 5])
        self.assertTrue(success)
        self.assertEqual(val, "10")
        self.assertEqual(int(eval(expr)), 10)


if __name__ == "__main__":
    unittest.main()
