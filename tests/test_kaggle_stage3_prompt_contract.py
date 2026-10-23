import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "research_candidates" / "evidence_abstention" / "kaggle_stage3_p0_p1.py"
SOURCE = RUNNER.read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)


def function_node(name):
    matches = [
        node for node in TREE.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]
    if len(matches) != 1:
        raise AssertionError(f"Expected exactly one function named {name}, got {len(matches)}")
    return matches[0]


class Stage3PromptContractTests(unittest.TestCase):
    def test_prompt_builder_does_not_receive_hidden_evidence_level(self):
        node = function_node("make_prompt")
        self.assertEqual([arg.arg for arg in node.args.args], ["policy", "pack", "schema"])
        body = ast.get_source_segment(SOURCE, node).lower()
        self.assertNotIn("evidence_level", body)
        self.assertNotIn("evidence level", body)
        self.assertNotIn("kanıt seviyesi", body)

    def test_prompt_contains_policy_instruction_but_not_condition_label(self):
        body = ast.get_source_segment(SOURCE, function_node("make_prompt"))
        self.assertIn("POLICY_INSTRUCTIONS[policy]", body)
        self.assertNotIn('"P0"', body)
        self.assertNotIn('"P1"', body)

    def test_runner_uses_canonical_schema_and_strict_json(self):
        self.assertIn('read_json(project / "OUTPUT_SCHEMA.json")', SOURCE)
        self.assertIn("validate_schema_contract(schema)", SOURCE)
        parser_body = ast.get_source_segment(SOURCE, function_node("parse_response"))
        self.assertIn("json.loads(raw)", parser_body)
        self.assertNotIn("raw.find", parser_body)
        self.assertNotIn("raw.rfind", parser_body)
        self.assertNotIn("confidence", SOURCE.lower())

    def test_preflight_must_pass_before_study_execution(self):
        main_body = ast.get_source_segment(SOURCE, function_node("main"))
        self.assertLess(
            main_body.index("require_authorized_preflight(root)"),
            main_body.index("run_study(root, manifest)"),
        )
        self.assertIn("load_preflight_module(root).evaluate(root)", SOURCE)
        self.assertIn("EVIDENCE_ABSTENTION_INFERENCE_APPROVED", SOURCE)

    def test_runner_and_preflight_are_in_both_hash_contracts(self):
        preflight = (ROOT / "scripts" / "evidence_abstention_preflight.py").read_text(encoding="utf-8")
        analyzer = (ROOT / "scripts" / "analyze_evidence_abstention_results.py").read_text(encoding="utf-8")
        self.assertIn(
            '"inference_runner": "research_candidates/evidence_abstention/kaggle_stage3_p0_p1.py"',
            preflight,
        )
        self.assertIn('"preflight_code": "scripts/evidence_abstention_preflight.py"', preflight)
        self.assertIn('"research_candidates/evidence_abstention/kaggle_stage3_p0_p1.py"', analyzer)
        self.assertIn('"scripts/evidence_abstention_preflight.py"', analyzer)

    def test_run_output_identity_is_not_derived_from_hidden_condition(self):
        body = ast.get_source_segment(SOURCE, function_node("run_study"))
        self.assertIn("secrets.token_hex(10)", body)
        self.assertNotIn('str(output_index) + "|" + case["case_id"]', body)


if __name__ == "__main__":
    unittest.main()
