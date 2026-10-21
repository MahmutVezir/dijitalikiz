import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evidence_abstention_requires_pytest.py"
SPEC = importlib.util.spec_from_file_location("requires_pytest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class RequiresPytestTests(unittest.TestCase):
    def test_detects_pytest_with_arguments(self):
        self.assertTrue(MODULE.requires_pytest(["pytest lib/matplotlib/tests/test_marker.py::test_marker_fillstyle"]))

    def test_detects_pytest_notation_with_whitespace(self):
        self.assertTrue(MODULE.requires_pytest(["  pytest  tests/test_x.py::test_x"]))

    def test_does_not_flag_unittest(self):
        self.assertFalse(MODULE.requires_pytest(["python -m unittest -q tests.test_x.TestCase.test_y"]))

    def test_rejects_malformed_command_list(self):
        with self.assertRaisesRegex(ValueError, "JSON list of strings"):
            MODULE.requires_pytest("pytest tests/test_x.py")


if __name__ == "__main__":
    unittest.main()
