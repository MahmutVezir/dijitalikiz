"""Independent axis-placement reproducer for python-control issue #1144."""
from __future__ import annotations

import unittest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import control as ct


class PythonControlIssue1144Regression(unittest.TestCase):
    def test_nyquist_plot_uses_the_explicitly_supplied_axes(self) -> None:
        figure, axes = plt.subplots(2, 2)
        try:
            system = ct.tf([1], [2, 1])
            plt.sca(axes[1, 1])
            ct.nyquist_plot(system, ax=axes[1, 0])
            self.assertGreater(len(axes[1, 0].lines), 0)
            self.assertEqual(len(axes[0, 0].lines), 0)
            self.assertEqual(len(axes[0, 1].lines), 0)
            self.assertEqual(len(axes[1, 1].lines), 0)
        finally:
            plt.close(figure)


if __name__ == "__main__":
    unittest.main(verbosity=2)
