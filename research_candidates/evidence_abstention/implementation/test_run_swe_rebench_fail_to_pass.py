from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from run_swe_rebench_fail_to_pass import classify_result, read_selectors, run_one


class SelectorRunnerContractTests(unittest.TestCase):
    def test_selector_reader_preserves_spaces_and_brackets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "selectors.txt"
            selector = "tests/test_http.py::TestHTTPUtility::test_dict_header[=foo, =]"
            path.write_text(selector + "\n", encoding="utf-8")
            self.assertEqual(read_selectors(path), [selector])

    def test_runner_passes_selector_as_one_argv_item(self) -> None:
        selector = "tests/test_http.py::TestHTTPUtility::test_dict_header[=foo, =]"
        output = "F [100%]\nFAILED tests/test_http.py::TestHTTPUtility::test_dict_header[=foo, =] - AssertionError\n1 failed in 0.02s\n"
        completed = subprocess.CompletedProcess(args=["pytest"], returncode=1, stdout=output)
        with tempfile.TemporaryDirectory() as tmp:
            with patch("run_swe_rebench_fail_to_pass.subprocess.run", return_value=completed) as mocked:
                result = run_one(Path(tmp), selector, "base-fail")
            command = mocked.call_args.args[0]
            self.assertEqual(command[-1], selector)
            self.assertEqual(sum(arg == selector for arg in command), 1)
            self.assertTrue(result["ok"], result["reason"])

    def test_base_requires_executed_failure_not_collection_error(self) -> None:
        output = "F\nFAILED tests/test_x.py::test_bug\n1 failed in 0.02s\n"
        self.assertEqual(
            classify_result("base-fail", 1, output),
            (True, "selected test executed and failed on the buggy base"),
        )
        self.assertFalse(
            classify_result(
                "base-fail",
                1,
                "ERROR: not found: tests/test_x.py::test_bug\nno tests ran in 0.01s\n",
            )[0]
        )
        self.assertFalse(
            classify_result("base-fail", 0, "1 passed in 0.02s\n")[0]
        )

    def test_fixed_requires_pass_and_rejects_skipped_or_failed(self) -> None:
        self.assertTrue(classify_result("fixed-pass", 0, ".\n1 passed in 0.02s\n")[0])
        self.assertFalse(
            classify_result("fixed-pass", 0, "s\n1 skipped in 0.02s\n")[0]
        )
        self.assertFalse(
            classify_result("fixed-pass", 1, "F\n1 failed in 0.02s\n")[0]
        )


if __name__ == "__main__":
    unittest.main()
