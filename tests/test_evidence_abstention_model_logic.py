import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "prototype"))
from evidence_abstention_model import EvidencePacket, build_messages, validate_output

VALID = {
    "decision": "diagnose", "root_cause": "The cache is not invalidated.",
    "evidence_refs": ["TRACE_1", "CODE_1"], "rationale": "Trace and source hint at stale cache.",
    "alternative_hypotheses": ["A race condition"], "missing_evidence": [],
}


class ModelLogicTests(unittest.TestCase):
    def setUp(self):
        self.packet = EvidencePacket(code="cache.clear() is not called", traceback="KeyError: item")

    def test_prompt_exposes_only_present_evidence_ids(self):
        payload = json.loads(build_messages(self.packet, "P1")[1]["content"])
        self.assertEqual(payload["allowed_evidence_ids"], ["CODE_1", "TRACE_1"])
        self.assertIn("abstain", payload["policy"])

    def test_valid_citation_is_structural_not_semantic_proof(self):
        report = validate_output(json.dumps(VALID), self.packet, "P1")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["semantic_support"], "not_assessed")

    def test_unknown_evidence_id_becomes_abstention_under_p1(self):
        report = validate_output(json.dumps(dict(VALID, evidence_refs=["GOLD_LABEL"])), self.packet, "P1")
        self.assertEqual(report["status"], "guarded_abstention")
        self.assertEqual(report["decision"], "abstain")
        self.assertEqual(report["root_cause"], "")

    def test_diagnosis_without_citation_fails_closed_under_p1(self):
        report = validate_output(json.dumps(dict(VALID, evidence_refs=[])), self.packet, "P1")
        self.assertEqual(report["status"], "guarded_abstention")

    def test_non_json_is_not_guessed(self):
        report = validate_output("Maybe a cache bug.", self.packet, "P1")
        self.assertEqual(report["status"], "invalid_model_output")

    def test_abstention_requires_empty_root_cause(self):
        answer = {
            "decision": "abstain", "root_cause": "maybe cache", "evidence_refs": [],
            "rationale": "Insufficient evidence", "alternative_hypotheses": [],
            "missing_evidence": ["reproducer"],
        }
        self.assertEqual(validate_output(json.dumps(answer), self.packet, "P1")["status"], "invalid_model_output")

    def test_p0_abstention_is_recorded_as_policy_noncompliance(self):
        answer = {
            "decision": "abstain", "root_cause": "", "evidence_refs": [],
            "rationale": "Insufficient evidence", "alternative_hypotheses": [],
            "missing_evidence": ["reproducer"],
        }
        self.assertEqual(validate_output(json.dumps(answer), self.packet, "P0")["status"], "policy_noncompliance")

    def test_empty_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            build_messages(EvidencePacket(code="", traceback=""), "P1")


if __name__ == "__main__":
    unittest.main()
