import hashlib
import unittest

from operational_packet_validator import packet_digest, validate_packet


def valid_packet():
    content = "The target test raises a TypeError at the validation boundary."
    packet = {
        "schema_version": "1.0",
        "packet_id": "PACKET_DEMO_001",
        "evidence_items": [
            {
                "id": "TEST_A",
                "kind": "test_output",
                "content": content,
                "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                "source_snapshot_sha256": "a" * 64,
            },
            {
                "id": "TRACE_B",
                "kind": "stack_trace",
                "content": "TypeError: invalid arguments",
                "content_sha256": hashlib.sha256(b"TypeError: invalid arguments").hexdigest(),
                "source_snapshot_sha256": "b" * 64,
            },
        ],
    }
    packet["packet_sha256"] = packet_digest(packet)
    return packet


class OperationalPacketValidatorTests(unittest.TestCase):
    def test_valid_packet_checks_content_and_manifest_hashes(self):
        result = validate_packet(valid_packet())
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["available_evidence_ids"], ["TEST_A", "TRACE_B"])
        self.assertFalse(result["semantic_support_audit_performed"])
        self.assertFalse(result["contradiction_audit_performed"])
        self.assertFalse(result["model_inference_performed"])

    def test_content_mutation_fails_hash_validation(self):
        packet = valid_packet()
        packet["evidence_items"][0]["content"] += " hidden change"
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("content SHA-256 mismatch" in item for item in result["blockers"]))

    def test_packet_hash_mismatch_fails(self):
        packet = valid_packet()
        packet["packet_sha256"] = "c" * 64
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("packet SHA-256 mismatch.", result["blockers"])

    def test_duplicate_evidence_ids_fail(self):
        packet = valid_packet()
        packet["evidence_items"][1]["id"] = "TEST_A"
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("Evidence item IDs must be unique.", result["blockers"])

    def test_gold_condition_fields_are_rejected(self):
        packet = valid_packet()
        packet["gold_evidence_level"] = "E3_insufficient"
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("Unexpected top-level fields" in item for item in result["blockers"]))

    def test_case_identity_is_not_allowed_as_packet_id(self):
        packet = valid_packet()
        packet["packet_id"] = "BugsInPy-fastapi-6"
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("pseudonymous PACKET_" in item for item in result["blockers"]))

    def test_source_hash_must_be_valid_sha256(self):
        packet = valid_packet()
        packet["evidence_items"][0]["source_snapshot_sha256"] = "not-a-hash"
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("source_snapshot_sha256" in item for item in result["blockers"]))

    def test_unknown_evidence_kind_fails_closed(self):
        packet = valid_packet()
        packet["evidence_items"][0]["kind"] = "gold_root_cause"
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("unsupported evidence kind" in item for item in result["blockers"]))

    def test_invalid_packet_never_exports_ids_as_available(self):
        packet = valid_packet()
        packet["evidence_items"][0]["content_sha256"] = "0" * 64
        packet["packet_sha256"] = packet_digest(packet)
        result = validate_packet(packet)
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["available_evidence_ids"], [])

    def test_non_object_is_invalid(self):
        result = validate_packet([])
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["available_evidence_ids"], [])


if __name__ == "__main__":
    unittest.main()

