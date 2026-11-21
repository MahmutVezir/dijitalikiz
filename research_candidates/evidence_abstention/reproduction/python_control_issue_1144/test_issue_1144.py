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
            explicit_axes = axes[1, 0]
            current_axes = axes[1, 1]
            plt.sca(current_axes)
            ct.nyquist_plot(system, ax=explicit_axes)

            actual_line_counts = {
                "explicit_axes": len(explicit_axes.lines),
                "current_global_axes": len(current_axes.lines),
                "upper_left": len(axes[0, 0].lines),
                "upper_right": len(axes[0, 1].lines),
            }
            self.assertTrue(
                actual_line_counts["explicit_axes"] > 0
                and actual_line_counts["current_global_axes"] == 0,
                msg=f"Expected all Nyquist lines on explicit Axes only; observed {actual_line_counts}",
            )
            self.assertEqual(actual_line_counts["upper_left"], 0)
            self.assertEqual(actual_line_counts["upper_right"], 0)
        finally:
            plt.close(figure)


if __name__ == "__main__":
    unittest.main(verbosity=2)
