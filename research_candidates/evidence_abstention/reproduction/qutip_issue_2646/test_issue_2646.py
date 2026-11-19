"""Independent coefficient-argument update reproducer for QuTiP issue #2646."""
from __future__ import annotations

import unittest

import numpy as np
import qutip as qt


class QuTiPIssue2646Regression(unittest.TestCase):
    def test_direct_replace_arguments_control(self) -> None:
        def coefficient_function(t, args):
            return args["a"]

        original = qt.coefficient(coefficient_function, args={"a": 1})
        replaced = original.replace_arguments({"a": 2})

        self.assertEqual(original(0), 1)
        self.assertEqual(replaced(0), 2)

    def test_rewrapping_a_coefficient_updates_its_arguments(self) -> None:
        def coefficient_function(t, args):
            return args["a"]

        original = qt.coefficient(coefficient_function, args={"a": 1})
        updated = qt.coefficient(original, args={"a": 2})
        self.assertEqual(updated(0), 2)

    def test_qobjevo_constructor_updates_embedded_coefficient_arguments(self) -> None:
        operator = qt.sigmaz()

        def coefficient_function(t, args):
            return t + args["g"]

        original = qt.coefficient(coefficient_function, args={"g": 1})
        original_evo = qt.QobjEvo([operator, original])
        updated_evo = qt.QobjEvo([operator, original], args={"g": 2})

        np.testing.assert_allclose(original_evo(1).full(), (2 * operator).full())
        np.testing.assert_allclose(updated_evo(1).full(), (3 * operator).full())


if __name__ == "__main__":
    unittest.main(verbosity=2)
