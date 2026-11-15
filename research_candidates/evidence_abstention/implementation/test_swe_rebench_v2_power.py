import unittest

from swe_rebench_v2_power import exact_mcnemar_pvalue, exact_paired_mcnemar_power


class SweRebenchV2PowerSensitivityTests(unittest.TestCase):
    def test_exact_mcnemar_known_values(self):
        self.assertEqual(exact_mcnemar_pvalue(0, 0), 1.0)
        self.assertAlmostEqual(exact_mcnemar_pvalue(5, 0), 0.0625)
        self.assertAlmostEqual(exact_mcnemar_pvalue(6, 0), 0.03125)

    def test_power_matches_documented_moderate_scenario(self):
        self.assertAlmostEqual(exact_paired_mcnemar_power(60, 0.30, 0.10), 0.635, delta=0.001)
        self.assertAlmostEqual(exact_paired_mcnemar_power(80, 0.30, 0.10), 0.779, delta=0.001)

    def test_power_matches_documented_weaker_scenario(self):
        self.assertAlmostEqual(exact_paired_mcnemar_power(60, 0.20, 0.12), 0.138, delta=0.001)
        self.assertAlmostEqual(exact_paired_mcnemar_power(80, 0.20, 0.12), 0.181, delta=0.001)

    def test_equal_discordance_probabilities_do_not_create_directional_power(self):
        power = exact_paired_mcnemar_power(60, 0.15, 0.15)
        self.assertLess(power, 0.05)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            exact_paired_mcnemar_power(0, 0.3, 0.1)
        with self.assertRaises(ValueError):
            exact_paired_mcnemar_power(60, 0.8, 0.3)
        with self.assertRaises(ValueError):
            exact_paired_mcnemar_power(60, 0.3, 0.1, alpha=1.0)
        with self.assertRaises(ValueError):
            exact_mcnemar_pvalue(-1, 0)


if __name__ == "__main__":
    unittest.main()
