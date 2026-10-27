import ast
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype"))
from evidence_abstention_model import (
    EvidencePacket, POLICY_INSTRUCTIONS, SYSTEM_PROMPT,
    build_messages, validate_output,
)

VALID = {
    "decision": "diagnose",
    "root_cause": "The cache is not invalidated.",
    "evidence_refs": ["TRACE_1", "CODE_1"],
    "rationale": "The supplied trace and source suggest a stale-cache path.",
    "alternative_hypotheses": ["A race condition"],
    "missing_evidence": [],
}


class ModelLogicTests(unittest.TestCase):
    def setUp(self):
        self.packet = EvidencePacket(code="cache.clear() is not called", traceback="KeyError: item")

    def test_prompt_constants_match_the_frozen_stage3_runner(self):
        runner = (ROOT / "research_candidates" / "evidence_abstention" / "kaggle_stage3_p0_p1.py").read_text(encoding="utf-8")
        tree = ast.parse(runner)
        values = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in {"SYSTEM_PROMPT", "POLICY_INSTRUCTIONS"}:
                        values[target.id] = ast.literal_eval(node.value)
        self.assertEqual(SYSTEM_PROMPT, values["SYSTEM_PROMPT"])
        self.assertEqual(POLICY_INSTRUCTIONS, values["POLICY_INSTRUCTIONS"])

    def test_user_prompt_uses_canonical_task_and_schema_not_hidden_evidence_label(self):
        messages = build_messages(self.packet, "P1")
        self.assertEqual(messages[0]["content"], SYSTEM_PROMPT)
        self.assertIn("Task: Assess the likely root cause of the reported software defect.", messages[1]["content"])
        self.assertIn("JSON schema:", messages[1]["content"])
        self.assertNotIn("E1", messages[1]["content"])
        self.assertNotIn("E2", messages[1]["content"])
        self.assertNotIn("E3", messages[1]["content"])
        self.assertNotIn("gold_root_cause", messages[1]["content"])

    def test_valid_citation_is_structural_not_semantic_proof(self):
        report = validate_output(json.dumps(VALID), self.packet, "P1")
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["semantic_support"], "not_assessed")

    def test_unknown_evidence_id_is_flagged_without_rewriting_observed_decision(self):
        report = validate_output(json.dumps(dict(VALID, evidence_refs=["GOLD_LABEL"])), self.packet, "P1")
        self.assertEqual(report["status"], "invalid_evidence_references")
        self.assertEqual(report["decision"], "diagnose")
        self.assertEqual(report["root_cause"], VALID["root_cause"])

    def test_diagnosis_without_citation_is_flagged_not_rewritten(self):
        report = validate_output(json.dumps(dict(VALID, evidence_refs=[])), self.packet, "P1")
        self.assertEqual(report["status"], "invalid_evidence_references")
        self.assertEqual(report["decision"], "diagnose")

    def test_non_json_is_not_repaired_or_guessed(self):
        report = validate_output("Maybe a cache bug.", self.packet, "P1")
        self.assertEqual(report["status"], "invalid_model_output")

    def test_markdown_fence_is_not_silently_stripped(self):
        fence = chr(96) * 3
        raw = fence + "json\n" + json.dumps(VALID) + "\n" + fence
        self.assertEqual(validate_output(raw, self.packet, "P1")["status"], "invalid_model_output")

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

    def test_empty_required_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            build_messages(EvidencePacket(code="", traceback=""), "P1")

    def test_non_string_input_is_rejected_cleanly(self):
        with self.assertRaises(TypeError):
            EvidencePacket(code=None, traceback="an error").validate()


if __name__ == "__main__":
    unittest.main()
