import json
import unittest

from evidence_packet_audit import create_packet
from semantic_evidence_auditor import (
    build_semantic_audit_messages,
    build_semantic_audit_messages_from_packet,
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
        self.packet = create_packet([{
            "id": "TRACE_A",
            "kind": "test_trace",
            "content": "Observed path=/home/user/.cache",
            "source_uri": "https://example.org/trace",
        }])

    def test_builds_audit_request_from_visible_answer_and_evidence_only(self):
        system, user = build_semantic_audit_messages(self.answer, self.evidence)
        self.assertEqual(system["role"], "system")
        payload = json.loads(user["content"])
        self.assertEqual(payload["available_evidence_ids"], ["TRACE_A"])
        self.assertEqual(payload["evidence_items"], self.evidence)
        self.assertNotIn("gold_root_cause", payload)
        self.assertNotIn("evidence_level", payload)

    def test_frozen_packet_builder_uses_only_hash_verified_packet_content(self):
        system, user = build_semantic_audit_messages_from_packet(
            self.answer,
            self.packet,
            self.packet["packet_sha256"],
        )
        payload = json.loads(user["content"])
        self.assertEqual(system["role"], "system")
        self.assertEqual(payload["evidence_items"], self.evidence)
        self.assertEqual(payload["available_evidence_ids"], ["TRACE_A"])

    def test_frozen_packet_builder_rejects_content_changed_after_freeze(self):
        changed_packet = create_packet([{
            "id": "TRACE_A",
            "kind": "test_trace",
            "content": "Observed path=/tmp/altered-cache",
            "source_uri": "https://example.org/trace",
        }])
        with self.assertRaisesRegex(ValueError, "external expected_sha256"):
            build_semantic_audit_messages_from_packet(
                self.answer,
                changed_packet,
                self.packet["packet_sha256"],
            )

    def test_frozen_packet_builder_rejects_tampered_content_hashes(self):
        tampered_packet = json.loads(json.dumps(self.packet))
        tampered_packet["items"][0]["content"] = "tampered after packet creation"
        with self.assertRaisesRegex(ValueError, "content_sha256 does not match content"):
            build_semantic_audit_messages_from_packet(
                self.answer,
                tampered_packet,
                self.packet["packet_sha256"],
            )

    def test_frozen_packet_builder_requires_a_valid_external_hash(self):
        for invalid_hash in ("", "sha256:" + "a" * 64, "not-a-hash"):
            with self.subTest(invalid_hash=invalid_hash):
                with self.assertRaisesRegex(ValueError, "frozen external packet SHA-256"):
                    build_semantic_audit_messages_from_packet(
                        self.answer,
                        self.packet,
                        invalid_hash,
                    )

    def test_frozen_packet_builder_rejects_extra_hidden_label_fields(self):
        hidden_packet = dict(self.packet, gold_root_cause="hidden answer")
        with self.assertRaisesRegex(ValueError, "structural/hash validation"):
            build_semantic_audit_messages_from_packet(
                self.answer,
                hidden_packet,
                self.packet["packet_sha256"],
            )

    def test_frozen_packet_builder_rejects_unknown_answer_references(self):
        answer = dict(self.answer, evidence_refs=["TRACE_MISSING"])
        with self.assertRaisesRegex(ValueError, "not present in the packet"):
            build_semantic_audit_messages_from_packet(
                answer,
                self.packet,
                self.packet["packet_sha256"],
            )

    def test_rejects_extra_answer_fields_that_could_leak_labels(self):
        answer = dict(self.answer, gold_root_cause="hidden")
        with self.assertRaises(ValueError):
            build_semantic_audit_messages(answer, self.evidence)

    def test_rejects_duplicate_or_malformed_evidence_ids(self):
        with self.assertRaises(ValueError):
            build_semantic_audit_messages(self.answer, self.evidence * 2)
        with self.assertRaises(ValueError):
            build_semantic_audit_messages(self.answer, [{"id": "trace a", "content": "trace"}])

    def test_rejects_candidate_references_missing_from_packet(self):
        answer = dict(self.answer, evidence_refs=["TRACE_MISSING"])
        with self.assertRaisesRegex(ValueError, "not present in the packet"):
            build_semantic_audit_messages(answer, self.evidence)

    def test_rejects_malformed_candidate_field_types(self):
        with self.assertRaisesRegex(ValueError, "must be strings"):
            build_semantic_audit_messages(dict(self.answer, root_cause=123), self.evidence)
        with self.assertRaisesRegex(ValueError, "must contain at most eight strings"):
            build_semantic_audit_messages(
                dict(self.answer, alternative_hypotheses=[{"hidden": "value"}]),
                self.evidence,
            )

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
            parse_semantic_audit(
                '{"claims":[],"self_check_conflict":false,"explicit_contradiction":false}',
                frozenset({"TRACE_A"}),
            )
        with self.assertRaises(ValueError):
            parse_semantic_audit('{"claims":[],"extra":true}', frozenset({"TRACE_A"}))

    def test_rejects_non_string_claim_status_without_crashing(self):
        invalid = claim()
        invalid["status"] = ["supported"]
        with self.assertRaisesRegex(ValueError, "unknown support status"):
            parse_semantic_audit(audit([invalid]), frozenset({"TRACE_A"}))

    def test_detects_explicit_contradiction_for_fail_closed_use(self):
        result = parse_semantic_audit(
            audit([claim(status="contradicted")], explicit_contradiction=True),
            frozenset({"TRACE_A"}),
        )
        self.assertTrue(result.explicit_contradiction)
        self.assertEqual(result.supported_claim_coverage, 0.0)


if __name__ == "__main__":
    unittest.main()
