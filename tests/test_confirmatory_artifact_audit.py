from __future__ import annotations

import unittest

from scripts.audit_confirmatory_artifact import (
    exact_mcnemar_pvalue,
    normalize_phrase,
    paired_risk_difference_ci,
    root_cause_alias_match,
)


class ConfirmatoryAuditUnitTests(unittest.TestCase):
    def test_normalization_matches_punctuation_and_case(self):
        self.assertEqual(normalize_phrase("Exception_Path: ON_EX!"), "exception path on ex")

    def test_alias_match_uses_contiguous_normalized_phrase(self):
        output = {
            "root_cause_class": "Semantic Misclassification",
            "explanation": "The exception path is mislabeled as an unconditional edge.",
        }
        self.assertTrue(root_cause_alias_match(output, ["exception path mislabeled as unconditional edge"]))

    def test_alias_match_does_not_accept_unrelated_phrase(self):
        output = {"root_cause_class": "Type Error", "explanation": "A list was sorted incorrectly."}
        self.assertFalse(root_cause_alias_match(output, ["exception path mislabeled as unconditional edge"]))

    def test_mcnemar_no_discordant_pairs_returns_one(self):
        self.assertEqual(exact_mcnemar_pvalue(0, 0), 1.0)

    def test_mcnemar_one_discordant_pair_is_not_significant(self):
        self.assertEqual(exact_mcnemar_pvalue(1, 0), 1.0)

    def test_paired_ci_includes_zero_when_no_discordant_cases(self):
        low, high = paired_risk_difference_ci(0, 0, 16)
        self.assertAlmostEqual(low, -high, places=12)
        self.assertAlmostEqual(high, 0.1936076805344365, places=10)


if __name__ == "__main__":
    unittest.main()
