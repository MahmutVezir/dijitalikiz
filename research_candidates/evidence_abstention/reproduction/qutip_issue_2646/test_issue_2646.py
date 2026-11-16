"""Independent coefficient-argument update reproducer for QuTiP issue #2646."""
from __future__ import annotations

import unittest

import qutip as qt


class QuTiPIssue2646Regression(unittest.TestCase):
    def test_rewrapping_a_coefficient_updates_its_arguments(self) -> None:
        def coefficient_function(t, args):
            return args["a"]

        original = qt.coefficient(coefficient_function, args={"a": 1})
        updated = qt.coefficient(original, args={"a": 2})
        self.assertEqual(updated(0), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
