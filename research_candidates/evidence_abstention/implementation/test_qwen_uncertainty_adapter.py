import json
import unittest

from qwen_uncertainty_adapter import (
    EvidenceAudit,
    GenerationSample,
    assess_candidates,
    parse_structured_answer,
)
from uncertainty_policy import (
    CalibrationObservation,
    DecisionPolicy,
    EmpiricalConfidenceCalibrator,
)


def answer(decision="diagnose", root_cause=None, refs=None):
    if root_cause is None:
        root_cause = "Cache invalidation is inconsistent." if decision == "diagnose" else ""
    return json.dumps({
        "decision": decision,
        "root_cause": root_cause,
        "evidence_refs": ["E1"] if refs is None else refs,
        "rationale": "The supplied test evidence supports this assessment.",
        "alternative_hypotheses": [],
        "missing_evidence": [],
    })


class QwenAdapterTests(unittest.TestCase):
    def setUp(self):
        self.calibrator = EmpiricalConfidenceCalibrator(bin_count=5, min_samples_per_bin=2)
        self.calibrator.fit(
            [CalibrationObservation(0.1, True) for _ in range(10)]
            + [CalibrationObservation(0.9, False) for _ in range(10)]
        )
        self.policy = DecisionPolicy(0.8, 0.25, "sha256:" + "a" * 64, True)
        self.audit = EvidenceAudit("E1", frozenset({"E1", "E2"}), 1.0, False, False)
        self.samples = (
            GenerationSample(answer(), (0.05, 0.1), 10, "a" * 64),
            GenerationSample(answer(), (0.1, 0.1), 11, "b" * 64),
        )

    def test_parse_requires_exact_output_schema(self):
        parsed = parse_structured_answer(answer())
        self.assertEqual(parsed.decision, "diagnose")
        self.assertEqual(parsed.evidence_refs, ("E1",))

    def test_parse_rejects_extra_fields(self):
        value = json.loads(answer())
        value["confidence"] = 0.95
        with self.assertRaises(ValueError):
            parse_structured_answer(json.dumps(value))

    def test_parse_rejects_unknown_evidence_identifier_format(self):
        with self.assertRaises(ValueError):
            parse_structured_answer(answer(refs=["not a valid id"]))

    def test_parse_enforces_abstention_schema(self):
        with self.assertRaises(ValueError):
            parse_structured_answer(answer(decision="abstain", root_cause="a cause"))

    def test_identical_supported_candidates_can_diagnose(self):
        result = assess_candidates(self.samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "diagnose")
        self.assertAlmostEqual(result.uncertainty_index, 0.0875)

    def test_candidate_abstention_is_not_overridden(self):
        samples = (
            GenerationSample(answer("abstain", ""), (0.05,), 10, "a" * 64),
            self.samples[1],
        )
        result = assess_candidates(samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("model_requested_abstention", result.reasons)

    def test_missing_audit_fails_closed(self):
        audit = EvidenceAudit(None, frozenset({"E1"}), None, None, None)
        result = assess_candidates(self.samples, audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")

    def test_evidence_reference_not_in_packet_fails_closed(self):
        samples = (
            GenerationSample(answer(refs=["E99"]), (0.05,), 10, "a" * 64),
            self.samples[1],
        )
        result = assess_candidates(samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("unknown_evidence_reference", result.reasons)

    def test_invalid_candidate_fails_closed(self):
        samples = (
            GenerationSample("not JSON", (0.05,), 10, "a" * 64),
            self.samples[1],
        )
        result = assess_candidates(samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertEqual(result.reasons, ("invalid_candidate_output",))

    def test_only_one_candidate_fails_closed(self):
        result = assess_candidates(self.samples[:1], self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("uncertainty_samples_insufficient", result.reasons)


if __name__ == "__main__":
    unittest.main()
