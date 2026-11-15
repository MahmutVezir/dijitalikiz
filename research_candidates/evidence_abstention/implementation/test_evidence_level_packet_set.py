import copy
import hashlib
import unittest

from operational_packet_validator import packet_digest
from evidence_level_packet_set import (
    create_packet_set,
    packet_set_digest,
    validate_packet_set,
)


def make_packet(packet_id, items):
    packet = {
        "schema_version": "1.0",
        "packet_id": packet_id,
        "evidence_items": [],
    }
    for evidence_id, kind, content, source_hash in items:
        packet["evidence_items"].append({
            "id": evidence_id,
            "kind": kind,
            "content": content,
            "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "source_snapshot_sha256": source_hash,
        })
    packet["packet_sha256"] = packet_digest(packet)
    return packet


def valid_packet_set():
    common = ("TRACE_A", "stack_trace", "Traceback: ValueError", "a" * 64)
    extra_e2 = ("TEST_B", "test_output", "Expected 3, got 2", "b" * 64)
    extra_e1 = ("SRC_C", "source_excerpt", "return value is truncated", "c" * 64)
    return create_packet_set(
        make_packet("PACKET_E1_001", [common, extra_e2, extra_e1]),
        make_packet("PACKET_E2_001", [common, extra_e2]),
        make_packet("PACKET_E3_001", [common]),
        "PACKETSET_7F31A_001",
    )


class EvidenceLevelPacketSetTests(unittest.TestCase):
    def test_valid_strictly_nested_packet_set_passes(self):
        report = validate_packet_set(valid_packet_set())
        self.assertEqual(report["status"], "valid")
        self.assertTrue(report["strictly_nested"])
        self.assertEqual(report["additional_evidence_ids"]["E2_over_E3"], ["TEST_B"])
        self.assertEqual(report["additional_evidence_ids"]["E1_over_E2"], ["SRC_C"])

    def test_unknown_expected_packet_set_hash_fails_closed(self):
        report = validate_packet_set(valid_packet_set(), expected_sha256="0" * 64)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("external expected_sha256" in item for item in report["blockers"]))

    def test_e3_item_missing_from_e2_is_rejected(self):
        common = ("TRACE_A", "stack_trace", "Traceback: ValueError", "a" * 64)
        e2 = ("TEST_B", "test_output", "Expected 3, got 2", "b" * 64)
        e1 = ("SRC_C", "source_excerpt", "return value is truncated", "c" * 64)
        packet_set = {
            "schema_version": "1.0",
            "packet_set_id": "PACKETSET_7F31A_BAD",
            "packets": {
                "E1": make_packet("PACKET_E1_BAD", [common, e2, e1]),
                "E2": make_packet("PACKET_E2_BAD", [e2, e1]),
                "E3": make_packet("PACKET_E3_BAD", [common]),
            },
        }
        packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
        report = validate_packet_set(packet_set)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("E3 evidence items must be a subset of E2" in item for item in report["blockers"]))

    def test_same_evidence_id_cannot_change_content_between_levels(self):
        e1_a = ("TRACE_A", "stack_trace", "Traceback: ValueError", "a" * 64)
        e2_a = ("TRACE_A", "stack_trace", "Traceback: TypeError", "a" * 64)
        extra_e2 = ("TEST_B", "test_output", "Expected 3, got 2", "b" * 64)
        extra_e1 = ("SRC_C", "source_excerpt", "return value is truncated", "c" * 64)
        packet_set = {
            "schema_version": "1.0",
            "packet_set_id": "PACKETSET_7F31A_MUT",
            "packets": {
                "E1": make_packet("PACKET_E1_MUT", [e1_a, extra_e2, extra_e1]),
                "E2": make_packet("PACKET_E2_MUT", [e2_a, extra_e2]),
                "E3": make_packet("PACKET_E3_MUT", [e2_a]),
            },
        }
        packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
        report = validate_packet_set(packet_set)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("changes across levels" in item for item in report["blockers"]))

    def test_identical_adjacent_levels_are_rejected(self):
        common = ("TRACE_A", "stack_trace", "Traceback: ValueError", "a" * 64)
        e1_extra = ("SRC_C", "source_excerpt", "return value is truncated", "c" * 64)
        packet_set = {
            "schema_version": "1.0",
            "packet_set_id": "PACKETSET_7F31A_DUP",
            "packets": {
                "E1": make_packet("PACKET_E1_DUP", [common, e1_extra]),
                "E2": make_packet("PACKET_E2_DUP", [common]),
                "E3": make_packet("PACKET_E3_DUP", [common]),
            },
        }
        packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
        report = validate_packet_set(packet_set)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("E2 must add" in item for item in report["blockers"]))

    def test_duplicate_inner_packet_ids_are_rejected(self):
        common = ("TRACE_A", "stack_trace", "Traceback: ValueError", "a" * 64)
        packet = make_packet("PACKET_SAME", [common])
        packet_set = {
            "schema_version": "1.0",
            "packet_set_id": "PACKETSET_7F31A_DUPID",
            "packets": {
                "E1": packet,
                "E2": copy.deepcopy(packet),
                "E3": make_packet("PACKET_E3_DUPID", [common]),
            },
        }
        packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
        report = validate_packet_set(packet_set)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("distinct packet_id" in item for item in report["blockers"]))

    def test_hidden_fields_are_not_allowed_in_packet_set(self):
        packet_set = valid_packet_set()
        packet_set["gold_root_cause"] = "secret"
        packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
        report = validate_packet_set(packet_set)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("Unexpected packet-set fields" in item for item in report["blockers"]))

    def test_invalid_inner_packet_fails_closed(self):
        packet_set = valid_packet_set()
        packet_set["packets"]["E2"]["evidence_items"][0]["content"] = "altered"
        packet_set["packet_set_sha256"] = packet_set_digest(packet_set)
        report = validate_packet_set(packet_set)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("content SHA-256 mismatch" in item for item in report["blockers"]))

    def test_non_object_is_invalid_without_inference(self):
        report = validate_packet_set([])
        self.assertEqual(report["status"], "invalid")
        self.assertFalse(report["semantic_sufficiency_assessed"])
        self.assertFalse(report["gold_root_cause_read"])
        self.assertFalse(report["model_inference_performed"])


if __name__ == "__main__":
    unittest.main()
