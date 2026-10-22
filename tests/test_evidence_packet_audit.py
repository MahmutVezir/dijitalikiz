import importlib.util
import json
import sys
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "research_candidates"
    / "evidence_abstention"
    / "implementation"
    / "evidence_packet_audit.py"
)
SPEC = importlib.util.spec_from_file_location("evidence_packet_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def packet():
    return MODULE.create_packet([
        {
            "id": "TRACE_A",
            "kind": "test_log",
            "content": "FAILED test_cache_invalidation",
            "source_uri": "artifact://test-log",
        },
        {
            "id": "SRC_B",
            "kind": "source_excerpt",
            "content": "cache.clear()",
            "source_uri": "artifact://source-excerpt",
        },
    ])


class EvidencePacketAuditTests(unittest.TestCase):
    def test_canonical_packet_and_content_hashes_pass(self):
        value = packet()
        result = MODULE.audit_packet(value)
        self.assertEqual(result.status, "valid")
        self.assertEqual(set(result.available_evidence_ids), {"TRACE_A", "SRC_B"})
        self.assertEqual(result.semantic_support_status, "not_assessed")

    def test_external_hash_mismatch_fails_closed(self):
        result = MODULE.audit_packet(packet(), expected_sha256="0" * 64)
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("expected_sha256" in error for error in result.errors))

    def test_changed_content_without_hash_update_fails(self):
        value = packet()
        value["items"][0]["content"] += " altered"
        result = MODULE.audit_packet(value)
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("content_sha256" in error for error in result.errors))
        self.assertTrue(any("packet_sha256" in error for error in result.errors))

    def test_duplicate_evidence_ids_fail(self):
        value = packet()
        value["items"][1]["id"] = value["items"][0]["id"]
        value["items"][1]["content_sha256"] = MODULE.sha256_bytes(
            value["items"][1]["content"].encode("utf-8")
        )
        value["packet_sha256"] = MODULE.sha256_bytes(MODULE.canonical_packet_payload(value))
        result = MODULE.audit_packet(value)
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("duplicates evidence ID" in error for error in result.errors))

    def test_gold_label_fields_are_rejected(self):
        value = packet()
        value["gold_root_cause"] = "secret label"
        value["packet_sha256"] = MODULE.sha256_bytes(MODULE.canonical_packet_payload(value))
        result = MODULE.audit_packet(value)
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("forbidden gold/answerability fields" in error for error in result.errors))

    def test_response_cannot_cite_unknown_evidence(self):
        result = MODULE.audit_response(
            MODULE.audit_packet(packet()),
            {"decision": "diagnose", "root_cause": "a cause", "evidence_refs": ["HIDDEN_9"]},
        )
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("unknown evidence references" in error for error in result.errors))

    def test_diagnosis_requires_traceable_evidence(self):
        result = MODULE.audit_response(
            MODULE.audit_packet(packet()),
            {"decision": "diagnose", "root_cause": "a cause", "evidence_refs": []},
        )
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("must cite" in error for error in result.errors))

    def test_abstention_can_have_no_citations_but_semantics_remain_unassessed(self):
        result = MODULE.audit_response(
            MODULE.audit_packet(packet()),
            {"decision": "abstain", "root_cause": "", "evidence_refs": []},
        )
        self.assertEqual(result.status, "valid")
        self.assertEqual(result.semantic_support_status, "not_assessed")

    def test_response_rejects_duplicate_citations(self):
        result = MODULE.audit_response(
            MODULE.audit_packet(packet()),
            {"decision": "diagnose", "root_cause": "a cause", "evidence_refs": ["TRACE_A", "TRACE_A"]},
        )
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("unique" in error for error in result.errors))

    def test_invalid_packet_causes_response_audit_failure(self):
        invalid = MODULE.audit_packet({"schema_version": "1.0", "items": []})
        result = MODULE.audit_response(
            invalid,
            {"decision": "abstain", "root_cause": "", "evidence_refs": []},
        )
        self.assertEqual(result.status, "invalid")
        self.assertTrue(any("not structurally valid" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
