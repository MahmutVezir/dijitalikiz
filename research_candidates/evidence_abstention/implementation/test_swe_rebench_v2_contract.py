import hashlib
import json
import unittest
from pathlib import Path

from evidence_level_packet_set import create_packet_set, packet_set_digest
from operational_packet_validator import packet_digest
from swe_rebench_v2_contract import (
    DATASET_FILE_REVISION,
    DATASET_FILE_SHA256,
    MODEL_REVISION,
    audit_raw_response,
    build_messages_from_packet_set,
    validate_manifest,
    validate_output_schema,
)

OUTPUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "SWE-rebench V2 evidence-abstention response v0.1",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "decision", "root_cause", "evidence_refs", "rationale",
        "alternative_hypotheses", "missing_evidence",
    ],
    "properties": {
        "decision": {"type": "string", "enum": ["diagnose", "abstain"]},
        "root_cause": {"type": "string"},
        "evidence_refs": {"type": "array", "items": {"type": "string"}, "uniqueItems": True, "maxItems": 8},
        "rationale": {"type": "string"},
        "alternative_hypotheses": {"type": "array", "items": {"type": "string"}, "maxItems": 8},
        "missing_evidence": {"type": "array", "items": {"type": "string"}, "maxItems": 8},
    },
}


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


def packet_set():
    trace = ("TRACE_A", "stack_trace", "Observed TypeError at validation boundary", "a" * 64)
    test = ("TEST_B", "test_output", "Expected valid result; received TypeError", "b" * 64)
    source = ("SRC_C", "source_excerpt", "The function passes an unvalidated object onward.", "c" * 64)
    return create_packet_set(
        make_packet("PACKET_E1_001", [trace, test, source]),
        make_packet("PACKET_E2_001", [trace, test]),
        make_packet("PACKET_E3_001", [trace]),
        "PACKETSET_SWE_001",
    )


def manifest():
    return {
        "protocol_version": "0.1-draft",
        "inference_allowed": False,
        "accepted_case_count": 0,
        "accepted_project_count": 0,
        "model_inference_performed": False,
        "model_loading_performed": False,
        "fine_tuning_performed": False,
        "dataset": {
            "id": "PrimeIntellect/SWE-rebench-V2-Filtered-Verified",
            "file_revision": DATASET_FILE_REVISION,
            "file_sha256": DATASET_FILE_SHA256,
            "primary_cohort_csv_sha256": "84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db",
            "cohort_manifest_sha256": "77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf",
        },
        "design": {
            "evidence_levels": ["E1", "E2", "E3"],
            "policies": ["P0", "P1"],
            "minimum_independent_cases": 60,
            "target_independent_cases": 80,
            "minimum_upstream_projects": 60,
        },
        "model": {
            "id": "Qwen/Qwen2.5-3B-Instruct",
            "revision": MODEL_REVISION,
            "license_review_status": "pending_exact_revision_review",
            "license_identifier": "qwen-research",
            "license_evidence_uri": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/aa8e72537993ba99e69dfaafa59ed015b17504d1/LICENSE",
            "license_scope_review_status": "pending_human_noncommercial_assessment",
        },
    }


def response(decision="diagnose", root_cause="The parser passes the wrong object.", refs=None):
    return json.dumps({
        "decision": decision,
        "root_cause": root_cause,
        "evidence_refs": ["TRACE_A"] if refs is None else refs,
        "rationale": "This is a synthetic test fixture.",
        "alternative_hypotheses": [],
        "missing_evidence": [],
    })


class SweRebenchV2ContractTests(unittest.TestCase):
    def test_committed_draft_manifest_and_output_schema_validate(self):
        project_root = Path(__file__).resolve().parents[1]
        actual_manifest = json.loads(
            (project_root / "SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json").read_text(encoding="utf-8")
        )
        actual_schema = json.loads(
            (project_root / "SWE_REBENCH_V2_OUTPUT_SCHEMA_V0_1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_manifest(actual_manifest)["status"], "valid_draft_no_inference")
        validate_output_schema(actual_schema)

    def test_malformed_non_string_decision_fails_closed(self):
        raw = json.dumps({
            "decision": [],
            "root_cause": "",
            "evidence_refs": [],
            "rationale": "synthetic malformed fixture",
            "alternative_hypotheses": [],
            "missing_evidence": [],
        })
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_schema")
        self.assertEqual(result["policy_compliance_status"], "not_assessed")
        self.assertEqual(result["raw_output"], raw)

    def test_committed_swe_rebench_registry_is_empty_and_unaccepted(self):
        project_root = Path(__file__).resolve().parents[1]
        registry = json.loads(
            (project_root / "SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registry["status"], "empty_no_confirmatory_cases_accepted")
        self.assertEqual(registry["accepted_case_count"], 0)
        self.assertEqual(registry["accepted_project_count"], 0)
        self.assertEqual(registry["records"], [])

    def test_manifest_is_valid_draft_but_never_authorizes_inference(self):
        result = validate_manifest(manifest())
        self.assertEqual(result["status"], "valid_draft_no_inference")
        self.assertFalse(result["inference_authorized"])
        self.assertFalse(result["model_inference_performed"])

    def test_manifest_pins_exact_qwen_research_license_and_keeps_review_pending(self):
        candidate = manifest()
        result = validate_manifest(candidate)
        self.assertEqual(result["status"], "valid_draft_no_inference")
        candidate["model"]["license_identifier"] = "apache-2.0"
        result = validate_manifest(candidate)
        self.assertIn("model license identifier must remain pinned to qwen-research.", result["blockers"])
        candidate = manifest()
        candidate["model"]["license_scope_review_status"] = "approved"
        result = validate_manifest(candidate)
        self.assertIn("model non-commercial scope review must remain pending.", result["blockers"])

    def test_manifest_rejects_any_inference_authorization(self):
        value = manifest()
        value["inference_allowed"] = True
        result = validate_manifest(value)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("inference_allowed must be false" in x for x in result["blockers"]))

    def test_manifest_rejects_changed_dataset_revision_or_hash(self):
        value = manifest()
        value["dataset"]["file_revision"] = "0" * 40
        result = validate_manifest(value)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("dataset.file_revision" in x for x in result["blockers"]))

    def test_prompt_contains_only_selected_packet_visible_items(self):
        value = packet_set()
        messages = build_messages_from_packet_set(
            value, "E3", "P1", OUTPUT_SCHEMA, value["packet_set_sha256"]
        )
        self.assertEqual(messages[0]["role"], "system")
        user = json.loads(messages[1]["content"])
        self.assertEqual([x["id"] for x in user["evidence_items"]], ["TRACE_A"])
        self.assertNotIn("packet_id", messages[1]["content"])
        self.assertNotIn("PACKETSET_SWE_001", messages[1]["content"])
        self.assertNotIn("E1", messages[1]["content"])
        self.assertNotIn("E2", messages[1]["content"])
        self.assertNotIn("E3", messages[1]["content"])
        self.assertNotIn('"P0"', messages[1]["content"])
        self.assertNotIn('"P1"', messages[1]["content"])
        self.assertNotIn("gold_root_cause", messages[1]["content"])
        self.assertNotIn("source_snapshot_sha256", messages[1]["content"])

    def test_policy_changes_only_policy_instruction_in_user_payload(self):
        value = packet_set()
        p0 = json.loads(build_messages_from_packet_set(
            value, "E2", "P0", OUTPUT_SCHEMA, value["packet_set_sha256"]
        )[1]["content"])
        p1 = json.loads(build_messages_from_packet_set(
            value, "E2", "P1", OUTPUT_SCHEMA, value["packet_set_sha256"]
        )[1]["content"])
        self.assertNotEqual(p0["policy_instruction"], p1["policy_instruction"])
        for field in ("task", "evidence_items", "response_rules", "json_schema"):
            self.assertEqual(p0[field], p1[field])

    def test_message_builder_rejects_wrong_external_packet_set_hash(self):
        value = packet_set()
        with self.assertRaisesRegex(ValueError, "external expected_sha256"):
            build_messages_from_packet_set(value, "E1", "P1", OUTPUT_SCHEMA, "0" * 64)

    def test_invalid_policy_or_evidence_level_is_rejected(self):
        value = packet_set()
        with self.assertRaises(ValueError):
            build_messages_from_packet_set(value, "E4", "P1", OUTPUT_SCHEMA, value["packet_set_sha256"])
        with self.assertRaises(ValueError):
            build_messages_from_packet_set(value, "E1", "P2", OUTPUT_SCHEMA, value["packet_set_sha256"])

    def test_unknown_evidence_reference_is_flagged_without_rewriting_observed_decision(self):
        raw = response(refs=["TRACE_A", "GOLD_LABEL"])
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_evidence_references")
        self.assertTrue(result["schema_valid"])
        self.assertFalse(result["evidence_references_valid"])
        self.assertEqual(result["decision"], "diagnose")
        self.assertEqual(result["root_cause"], "The parser passes the wrong object.")
        self.assertEqual(result["raw_output"], raw)
        self.assertEqual(result["raw_output_sha256"], hashlib.sha256(raw.encode("utf-8")).hexdigest())
        self.assertIsNone(result["unsupported_definitive_diagnosis"])
        self.assertEqual(result["semantic_support_status"], "not_assessed")

    def test_diagnosis_with_valid_reference_is_not_semantically_marked_supported(self):
        result = audit_raw_response(response(), {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "valid")
        self.assertTrue(result["evidence_references_valid"])
        self.assertEqual(result["semantic_support_status"], "not_assessed")
        self.assertEqual(result["policy_compliance_status"], "requires_blinded_human_review")
        self.assertIsNone(result["unsupported_definitive_diagnosis"])

    def test_p0_abstention_is_preserved_and_marked_noncompliant(self):
        raw = response(decision="abstain", root_cause="")
        result = audit_raw_response(raw, {"TRACE_A"}, "P0")
        self.assertEqual(result["decision"], "abstain")
        self.assertEqual(result["root_cause"], "")
        self.assertEqual(result["policy_compliance_status"], "noncompliant")
        self.assertEqual(result["status"], "valid")

    def test_p1_abstention_is_not_automatically_scored_adequate(self):
        result = audit_raw_response(response(decision="abstain", root_cause=""), {"TRACE_A"}, "P1")
        self.assertEqual(result["decision"], "abstain")
        self.assertEqual(result["policy_compliance_status"], "requires_blinded_human_review")

    def test_invalid_json_is_not_repaired_or_converted_to_abstention(self):
        raw = "Maybe this is a parser bug."
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_json")
        self.assertIsNone(result["decision"])
        self.assertEqual(result["raw_output"], raw)

    def test_markdown_fences_are_not_silently_removed(self):
        fence = chr(96) * 3
        raw = fence + "json\n" + response() + "\n" + fence
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_json")
        self.assertEqual(result["raw_output"], raw)

    def test_diagnosis_without_citation_is_invalid_not_repaired(self):
        raw = response(refs=[])
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_schema")
        self.assertEqual(result["decision"], None)
        self.assertEqual(result["raw_output"], raw)

    def test_duplicate_json_keys_are_invalid_and_preserved(self):
        raw = '{"decision":"diagnose","decision":"abstain"}'
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_json")
        self.assertEqual(result["raw_output"], raw)
        self.assertIsNone(result["decision"])

    def test_non_standard_json_constants_are_rejected(self):
        raw = response().replace('"rationale": "This is a synthetic test fixture."',
                                  '"rationale": NaN')
        result = audit_raw_response(raw, {"TRACE_A"}, "P1")
        self.assertEqual(result["status"], "invalid_json")
        self.assertEqual(result["raw_output"], raw)

    def test_p0_invalid_citation_is_not_counted_as_full_instruction_compliance(self):
        result = audit_raw_response(response(refs=["NOT_IN_PACKET"]), {"TRACE_A"}, "P0")
        self.assertEqual(result["decision"], "diagnose")
        self.assertEqual(result["policy_compliance_status"], "invalid_citation_reference")

    def test_invalid_output_carries_no_automatic_safety_outcome(self):
        result = audit_raw_response("{", {"TRACE_A"}, "P0")
        self.assertIsNone(result["unsupported_definitive_diagnosis"])
        self.assertEqual(result["policy_compliance_status"], "not_assessed")
        self.assertFalse(result["model_inference_performed_by_auditor"])


if __name__ == "__main__":
    unittest.main()
