import unittest

from swe_rebench_v2_e1_guardrail import analyze_e1_coverage


class E1CoverageGuardrailTests(unittest.TestCase):
    def test_identical_coverage_passes(self):
        result = analyze_e1_coverage([True] * 60, [True] * 60, replicates=1000)
        self.assertEqual(result["delta_p1_minus_p0"], 0.0)
        self.assertTrue(result["non_inferiority_demonstrated"])
        self.assertEqual(result["paired_counts"]["both_covered"], 60)

    def test_large_coverage_loss_fails_guardrail(self):
        p0 = [True] * 60
        p1 = [False] * 18 + [True] * 42
        result = analyze_e1_coverage(p0, p1, replicates=5000)
        self.assertAlmostEqual(result["delta_p1_minus_p0"], -0.30)
        self.assertFalse(result["non_inferiority_demonstrated"])
        self.assertEqual(result["paired_counts"]["p0_only_covered"], 18)

    def test_preserves_pairing_and_counts(self):
        result = analyze_e1_coverage(
            [True, True, False, False],
            [True, False, True, False],
            replicates=1000,
        )
        self.assertEqual(result["paired_counts"], {
            "both_covered": 1,
            "p0_only_covered": 1,
            "p1_only_covered": 1,
            "neither_covered": 1,
        })
        self.assertEqual(result["delta_p1_minus_p0"], 0.0)

    def test_deterministic(self):
        args = ([True, True, False], [True, False, True])
        self.assertEqual(
            analyze_e1_coverage(*args, replicates=1000),
            analyze_e1_coverage(*args, replicates=1000),
        )

    def test_rejects_unpaired_lengths(self):
        with self.assertRaises(ValueError):
            analyze_e1_coverage([True], [True, False])

    def test_rejects_non_boolean_values(self):
        with self.assertRaises(TypeError):
            analyze_e1_coverage([1, True], [True, False])

    def test_rejects_too_few_bootstrap_replicates(self):
        with self.assertRaises(ValueError):
            analyze_e1_coverage([True, False], [True, False], replicates=999)


if __name__ == "__main__":
    unittest.main()
