import json
import unittest

from semantic_evidence_auditor import (
    build_semantic_audit_messages,
    parse_semantic_audit,
)


def claim(claim_id="C1", status="supported", refs=None):
    return {
        "claim_id": claim_id,
        "claim": "The cache path ignores the configured directory.",
        "status": status,
        "evidence_refs": ["TRACE_A"] if refs is None else refs,
        "rationale": "The supplied trace supports this classification.",
    }


def audit(claims=None, self_check_conflict=False, explicit_contradiction=False):
    return json.dumps({
        "claims": [claim()] if claims is None else claims,
        "self_check_conflict": self_check_conflict,
        "explicit_contradiction": explicit_contradiction,
    })


class SemanticEvidenceAuditorTests(unittest.TestCase):
    def setUp(self):
        self.answer = {
            "decision": "diagnose",
            "root_cause": "The cache path ignores the configured directory.",
            "evidence_refs": ["TRACE_A"],
            "rationale": "The trace shows the unexpected default path.",
            "alternative_hypotheses": [],
            "missing_evidence": [],
        }
        self.evidence = [{"id": "TRACE_A", "content": "Observed path=/home/user/.cache"}]

    def test_builds_audit_request_from_visible_answer_and_evidence_only(self):
        system, user = build_semantic_audit_messages(self.answer, self.evidence)
        self.assertEqual(system["role"], "system")
        payload = json.loads(user["content"])
        self.assertEqual(payload["available_evidence_ids"], ["TRACE_A"])
        self.assertEqual(payload["evidence_items"], self.evidence)
        self.assertNotIn("gold_root_cause", payload)
        self.assertNotIn("evidence_level", payload)

    def test_rejects_extra_answer_fields_that_could_leak_labels(self):
        answer = dict(self.answer, gold_root_cause="hidden")
        with self.assertRaises(ValueError):
            build_semantic_audit_messages(answer, self.evidence)

    def test_rejects_duplicate_or_malformed_evidence_ids(self):
        with self.assertRaises(ValueError):
            build_semantic_audit_messages(self.answer, self.evidence * 2)
        with self.assertRaises(ValueError):
            build_semantic_audit_messages(self.answer, [{"id": "trace a", "content": "trace"}])

    def test_parses_full_support(self):
        result = parse_semantic_audit(audit(), frozenset({"TRACE_A"}))
        self.assertEqual(result.supported_claim_coverage, 1.0)
        self.assertFalse(result.explicit_contradiction)

    def test_computes_partial_and_unsupported_claim_coverage(self):
        result = parse_semantic_audit(
            audit([
                claim("C1", "supported"),
                claim("C2", "partial"),
                claim("C3", "unsupported", []),
            ]),
            frozenset({"TRACE_A"}),
        )
        self.assertAlmostEqual(result.supported_claim_coverage, 0.5)

    def test_rejects_unknown_evidence_references(self):
        with self.assertRaisesRegex(ValueError, "not present in the packet"):
            parse_semantic_audit(audit([claim(refs=["TRACE_MISSING"])]), frozenset({"TRACE_A"}))

    def test_contradiction_flag_must_match_claim_label(self):
        with self.assertRaisesRegex(ValueError, "disagrees"):
            parse_semantic_audit(
                audit([claim(status="contradicted")], explicit_contradiction=False),
                frozenset({"TRACE_A"}),
            )

    def test_rejects_malformed_schema_and_empty_claims(self):
        with self.assertRaises(ValueError):
            parse_semantic_audit('{"claims":[],"self_check_conflict":false,"explicit_contradiction":false}', frozenset({"TRACE_A"}))
        with self.assertRaises(ValueError):
            parse_semantic_audit('{"claims":[],"extra":true}', frozenset({"TRACE_A"}))

    def test_detects_explicit_contradiction_for_fail_closed_use(self):
        result = parse_semantic_audit(
            audit([claim(status="contradicted")], explicit_contradiction=True),
            frozenset({"TRACE_A"}),
        )
        self.assertTrue(result.explicit_contradiction)
        self.assertEqual(result.supported_claim_coverage, 0.0)


if __name__ == "__main__":
    unittest.main()
