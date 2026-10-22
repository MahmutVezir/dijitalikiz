import json
import sys
import unittest
from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import patch

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
        "evidence_refs": ["TRACE_A"] if refs is None else refs,
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
        self.audit = EvidenceAudit(packet_validation_status="valid", available_evidence_ids=frozenset({"TRACE_A", "TEST_B"}), supported_claim_coverage=1.0, self_check_conflict=False, explicit_contradiction=False)
        self.samples = (
            GenerationSample(answer(), (0.05, 0.1), 10, "a" * 64),
            GenerationSample(answer(), (0.1, 0.1), 11, "a" * 64),
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

    def test_parse_rejects_non_string_evidence_ids_without_type_error(self):
        with self.assertRaises(ValueError):
            parse_structured_answer(answer(refs=[{"unexpected": "object"}]))

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
        audit = EvidenceAudit(packet_validation_status=None, available_evidence_ids=frozenset({"TRACE_A"}), supported_claim_coverage=None, self_check_conflict=None, explicit_contradiction=None)
        result = assess_candidates(self.samples, audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")

    def test_gold_evidence_level_label_cannot_be_used_as_packet_status(self):
        from dataclasses import replace

        audit = replace(self.audit, packet_validation_status="E1")
        result = assess_candidates(self.samples, audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("packet_validation_unknown", result.reasons)

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

    def test_candidate_prompt_hash_mismatch_fails_closed(self):
        samples = (self.samples[0], GenerationSample(answer(), (0.1,), 11, "b" * 64))
        result = assess_candidates(samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("candidate_prompt_hash_mismatch", result.reasons)

    def test_duplicate_candidate_seed_fails_closed(self):
        samples = (self.samples[0], GenerationSample(answer(), (0.1,), 10, "a" * 64))
        result = assess_candidates(samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("candidate_seeds_not_unique", result.reasons)

    def test_malformed_candidate_prompt_hash_fails_closed(self):
        samples = (self.samples[0], GenerationSample(answer(), (0.1,), 11, "not-a-hash"))
        result = assess_candidates(samples, self.audit, self.calibrator, self.policy)
        self.assertEqual(result.decision, "abstain")
        self.assertIn("invalid_candidate_prompt_hash", result.reasons)

    def test_generation_requests_and_passes_attention_mask(self):
        class FakeIds:
            ndim = 2
            shape = (1, 3)

            def to(self, device):
                return self

            def __getitem__(self, key):
                return FakeGeneratedIds()

        class FakeGeneratedIds:
            def numel(self):
                return 2

        class FakeMask:
            shape = (1, 3)

            def to(self, device):
                return self

        class FakeSequences:
            def __getitem__(self, key):
                return FakeGeneratedIds()

        class FakeScore:
            def __getitem__(self, index):
                return self

        class FakeTokenizer:
            eos_token_id = 2

            def __init__(self):
                self.template_kwargs = None

            def apply_chat_template(self, messages, **kwargs):
                self.template_kwargs = kwargs
                return {"input_ids": FakeIds(), "attention_mask": mask}

            def decode(self, generated_ids, skip_special_tokens=True):
                return answer()

        class FakeModel:
            device = SimpleNamespace(type="cpu", index=None)

            def __init__(self):
                self.calls = []

            def generate(self, input_ids, **kwargs):
                self.calls.append((input_ids, kwargs))
                return SimpleNamespace(sequences=FakeSequences(), scores=[FakeScore(), FakeScore()])

        fake_torch = SimpleNamespace(
            device=lambda name: SimpleNamespace(type=name, index=None),
            random=SimpleNamespace(fork_rng=lambda devices: nullcontext()),
            manual_seed=lambda seed: None,
            cuda=SimpleNamespace(current_device=lambda: 0, manual_seed_all=lambda seed: None),
        )
        mask = FakeMask()
        tokenizer = FakeTokenizer()
        model = FakeModel()
        with patch.dict(sys.modules, {"torch": fake_torch}), patch(
            "qwen_uncertainty_adapter._normalized_entropy_from_tensor", return_value=0.2
        ):
            from qwen_uncertainty_adapter import generate_candidates
            samples = generate_candidates(
                tokenizer,
                model,
                [{"role": "user", "content": "test"}],
                candidate_count=2,
                base_seed=90,
            )

        self.assertTrue(tokenizer.template_kwargs["return_dict"])
        self.assertEqual(len(samples), 2)
        self.assertIs(model.calls[0][1]["attention_mask"], mask)
        self.assertIs(model.calls[1][1]["attention_mask"], mask)
        self.assertEqual([sample.seed for sample in samples], [90, 91])
        self.assertEqual(samples[0].prompt_sha256, samples[1].prompt_sha256)


if __name__ == "__main__":
    unittest.main()
