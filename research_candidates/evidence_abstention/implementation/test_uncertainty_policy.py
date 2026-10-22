import unittest

from uncertainty_policy import (
    CalibrationObservation,
    DecisionPolicy,
    DecisionRequest,
    EmpiricalConfidenceCalibrator,
    brier_score,
    decide,
    expected_calibration_error,
    lexical_disagreement,
    mean_normalized_token_entropy,
    normalized_entropy_from_logits,
)


class UncertaintyPolicyTests(unittest.TestCase):
    def setUp(self):
        self.calibrator = EmpiricalConfidenceCalibrator(bin_count=5, min_samples_per_bin=8)
        self.calibrator.fit(
            [CalibrationObservation(0.1, True) for _ in range(10)]
            + [CalibrationObservation(0.9, False) for _ in range(10)]
        )
        self.policy = DecisionPolicy(0.8, 0.25, "sha256:" + "a" * 64, True)

    def request(self, **overrides):
        values = {
            "evidence_level": "E1",
            "answer": "Cache invalidation caused the defect.",
            "available_evidence_ids": frozenset({"E1", "E2"}),
            "cited_evidence_ids": ("E1",),
            "supported_claim_coverage": 1.0,
            "normalized_token_entropy": 0.1,
            "candidate_answers": ("Cache invalidation caused the defect.", "Cache invalidation caused the defect."),
            "self_check_conflict": False,
            "explicit_contradiction": False,
            "model_requested_abstention": False,
        }
        values.update(overrides)
        return DecisionRequest(**values)

    def decide(self, request=None, policy=None, calibrator=None):
        return decide(request or self.request(), calibrator or self.calibrator, policy or self.policy)

    def test_normalized_entropy_extremes(self):
        self.assertAlmostEqual(normalized_entropy_from_logits([10.0, -10.0]), 0.0, places=6)
        self.assertAlmostEqual(normalized_entropy_from_logits([0.0, 0.0]), 1.0, places=6)

    def test_entropy_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            normalized_entropy_from_logits([1.0])
        with self.assertRaises(ValueError):
            normalized_entropy_from_logits([float("nan"), 0.0])

    def test_mean_token_entropy_requires_generated_tokens(self):
        with self.assertRaises(ValueError):
            mean_normalized_token_entropy([])
        self.assertAlmostEqual(mean_normalized_token_entropy([[0.0, 0.0], [10.0, -10.0]]), 0.5, places=5)

    def test_lexical_disagreement_is_none_for_one_sample(self):
        self.assertIsNone(lexical_disagreement(["one answer"]))

    def test_lexical_disagreement_is_zero_for_identical_samples(self):
        self.assertEqual(lexical_disagreement(["same answer", "same answer"]), 0.0)

    def test_accepts_only_when_all_gates_pass(self):
        result = self.decide()
        self.assertEqual(result.decision, "diagnose")
        self.assertEqual(result.confidence_probability, 11 / 12)

    def test_unknown_evidence_level_abstains(self):
        result = self.decide(self.request(evidence_level=None))
        self.assertEqual(result.decision, "abstain")
        self.assertIn("evidence_level_unknown", result.reasons)

    def test_insufficient_evidence_abstains(self):
        result = self.decide(self.request(evidence_level="E3"))
        self.assertEqual(result.decision, "abstain")
        self.assertIn("evidence_insufficient", result.reasons)

    def test_model_requested_abstention_is_never_overridden(self):
        result = self.decide(self.request(model_requested_abstention=True))
        self.assertEqual(result.decision, "abstain")
        self.assertIn("model_requested_abstention", result.reasons)

    def test_contradiction_abstains(self):
        result = self.decide(self.request(explicit_contradiction=True))
        self.assertIn("evidence_contradiction", result.reasons)

    def test_unknown_contradiction_status_abstains(self):
        result = self.decide(self.request(explicit_contradiction=None))
        self.assertIn("contradiction_status_unknown", result.reasons)

    def test_unverified_calibration_abstains(self):
        result = self.decide(policy=DecisionPolicy(0.8, 0.25, "sha256:" + "a" * 64, False))
        self.assertIn("calibration_not_frozen", result.reasons)

    def test_unknown_citation_abstains(self):
        result = self.decide(self.request(cited_evidence_ids=("E99",)))
        self.assertIn("unknown_evidence_reference", result.reasons)

    def test_missing_calibration_abstains(self):
        result = self.decide(policy=DecisionPolicy(None, 0.25, None, False))
        self.assertIn("calibration_not_frozen", result.reasons)

    def test_missing_signal_abstains(self):
        result = self.decide(self.request(candidate_answers=("single sample",)))
        self.assertIn("uncertainty_signals_incomplete", result.reasons)

    def test_high_disagreement_abstains(self):
        result = self.decide(self.request(candidate_answers=("cache corruption", "database migration")))
        self.assertIn("uncertainty_threshold_exceeded", result.reasons)
        self.assertIn("confidence_below_threshold", result.reasons)

    def test_self_check_conflict_abstains(self):
        result = self.decide(self.request(self_check_conflict=True))
        self.assertIn("uncertainty_threshold_exceeded", result.reasons)

    def test_calibrator_requires_minimum_bin_samples(self):
        calibrator = EmpiricalConfidenceCalibrator(bin_count=5, min_samples_per_bin=2)
        calibrator.fit([CalibrationObservation(0.1, True)])
        self.assertIsNone(calibrator.predict(0.1))

    def test_calibrator_returns_smoothed_supported_accuracy(self):
        calibrator = EmpiricalConfidenceCalibrator(bin_count=5, min_samples_per_bin=2)
        calibrator.fit([
            CalibrationObservation(0.1, True),
            CalibrationObservation(0.1, False),
        ])
        self.assertEqual(calibrator.predict(0.1), 0.5)

    def test_missing_calibration_bin_abstains(self):
        calibrator = EmpiricalConfidenceCalibrator(bin_count=5, min_samples_per_bin=8)
        calibrator.fit([CalibrationObservation(0.1, True) for _ in range(10)])
        result = self.decide(self.request(normalized_token_entropy=0.6), calibrator=calibrator)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("calibration_bin_insufficient", result.reasons)

    def test_brier_and_ece(self):
        self.assertAlmostEqual(brier_score([0.9, 0.1], [True, False]), 0.01, places=6)
        self.assertAlmostEqual(expected_calibration_error([0.9, 0.1], [True, False]), 0.1, places=6)

    def test_metrics_reject_mismatched_lengths(self):
        with self.assertRaises(ValueError):
            brier_score([0.7], [True, False])
        with self.assertRaises(ValueError):
            expected_calibration_error([0.7], [True, False])


if __name__ == "__main__":
    unittest.main()
