"""Integration tests for the shell orchestration script and cross-solver consensus.

Executes the run_all.sh script and verifies that all three solvers output
consistent results for the preloaded benchmark problems.
"""

import os
import shutil
import subprocess
import unittest

# Check availability of GHC, make, and swipl to determine which solvers to test.
HAS_HASKELL = shutil.which("ghc") is not None and shutil.which("make") is not None
HAS_PROLOG = shutil.which("swipl") is not None


class TestOrchestration(unittest.TestCase):
    """
    Tests the orchestration shell script and solver consensus.

    Ensures that concurrent execution outputs are stored correctly and that all
    solvers agree on mathematical outcomes.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Builds the Haskell binary if Haskell is available on the system.

        Returns:
            None (None): The setup process does not return anything.
        """
        if HAS_HASKELL:
            haskell_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/haskell"))
            subprocess.run(
                ["make", "build"],
                cwd=haskell_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    def runOrchestrator(self, target: int, numbers: list) -> dict:
        """
        Runs the run_all.sh orchestration script and returns parsed outputs.

        Args:
            target (int): Target sum to reach.
            numbers (list): List of available integers.

        Returns:
            dict (dict): A dictionary mapping solver names to parsed output dicts.
        """
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/tui_wraper/run_all.sh"))
        cmd_args = [script_path, str(target)] + [str(n) for n in numbers]

        # Execute orchestrator concurrently.
        subprocess.run(cmd_args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        results = {}
        temp_dir = "/tmp/countdown_results"

        # Define solvers to parse based on system availability.
        solvers_to_parse = [("python", True)]
        if HAS_HASKELL:
            solvers_to_parse.append(("haskell", True))
        if HAS_PROLOG:
            solvers_to_parse.append(("prolog", True))

        for name, available in solvers_to_parse:
            output_file = os.path.join(temp_dir, f"{name}_output.txt")
            time_file = os.path.join(temp_dir, f"{name}_time.txt")

            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(os.path.exists(time_file))

            with open(output_file, "r") as f:
                output_content = f.read().strip()

            with open(time_file, "r") as f:
                time_val = f.read().strip()

            # Parse solver output lines.
            expr_str = ""
            val_str = ""
            success_status = False

            for line in output_content.splitlines():
                if line.startswith("Expression:"):
                    expr_str = line.replace("Expression:", "").strip()
                    success_status = True
                elif line.startswith("Value:"):
                    val_str = line.replace("Value:", "").strip()

            results[name] = {
                "success": success_status,
                "expression": expr_str,
                "value": val_str,
                "time": time_val
            }

        return results

    def testRunAllScript(self) -> None:
        """
        Tests basic execution of the run_all.sh script with simple arguments.

        Returns:
            None (None): Verified via assertion checks.
        """
        target_val = 10
        numbers_pool = [1, 2, 3, 4]
        results = self.runOrchestrator(target_val, numbers_pool)

        # Python is guaranteed to be tested.
        self.assertIn("python", results)
        self.assertTrue(results["python"]["success"])
        self.assertEqual(results["python"]["value"], "10")

        # Check Haskell consensus if available.
        if HAS_HASKELL:
            self.assertIn("haskell", results)
            self.assertTrue(results["haskell"]["success"])
            self.assertEqual(results["haskell"]["value"], "10")

        # Check Prolog consensus if available.
        if HAS_PROLOG:
            self.assertIn("prolog", results)
            self.assertTrue(results["prolog"]["success"])
            self.assertEqual(results["prolog"]["value"], "10")

    def testConsensusOnBenchmark(self) -> None:
        """
        Tests consensus among all available solvers on 5 default benchmark inputs.

        Returns:
            None (None): Verified via assertion checks.
        """
        benchmark_examples = [
            {"target": 10, "numbers": [1, 2, 3, 4]},
            {"target": 50, "numbers": [2, 3, 5, 10, 25]},
            {"target": 123, "numbers": [1, 2, 3, 4, 25]},
            {"target": 456, "numbers": [1, 3, 5, 10, 25, 50]},
            {"target": 987, "numbers": [1, 2, 3, 4, 75, 100]},
        ]

        for example in benchmark_examples:
            target = example["target"]
            numbers = example["numbers"]
            results = self.runOrchestrator(target, numbers)

            # Evaluate each solver's results to assert they are consistent.
            for name, data in results.items():
                self.assertTrue(
                    data["success"],
                    f"Solver {name} failed to solve target {target} with numbers {numbers}"
                )
                self.assertEqual(
                    int(data["value"]),
                    target,
                    f"Solver {name} target mismatch for target {target}: got {data['value']}"
                )
                self.assertEqual(
                    int(eval(data["expression"])),
                    target,
                    f"Solver {name} expression {data['expression']} does not evaluate to {target}"
                )


if __name__ == "__main__":
    unittest.main()
