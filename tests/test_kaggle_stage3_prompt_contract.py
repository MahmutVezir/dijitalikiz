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
    def test_system_prompt_uses_the_frozen_common_text(self):
        node = next(
            node for node in TREE.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "SYSTEM_PROMPT" for target in node.targets)
        )
        prompt = ast.literal_eval(node.value)
        self.assertIn("user message.\\nBase factual claims only", prompt)

    def test_prompt_spec_documents_the_output_schema_placeholder(self):
        prompt_spec = (ROOT / "research_candidates" / "evidence_abstention" / "PROMPT_CONDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("JSON schema:", prompt_spec)
        self.assertIn("{OUTPUT_SCHEMA_JSON}", prompt_spec)
        self.assertIn('json.dumps(schema, ensure_ascii=False)', SOURCE)

    def test_runtime_preflight_checks_package_and_resolved_revision_pins(self):
        self.assertIn("validate_runtime_environment(root)", SOURCE)
        self.assertIn("validate_loaded_model(tokenizer, model)", SOURCE)
        self.assertIn('expected.get(name) != actual.get(name)', SOURCE)
        self.assertIn('model_revision != MODEL_REVISION', SOURCE)
        self.assertIn('tokenizer_revision != MODEL_REVISION', SOURCE)
        self.assertIn('"resolved_tokenizer_revision_observable"', SOURCE)
        self.assertIn('"immutable_full_commit_sha_passed_to_from_pretrained; exposed resolved revisions are checked when available"', SOURCE)

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

    def test_gold_root_cause_is_bound_to_canonical_registry_hash(self):
        self.assertIn('record.get("reference_root_cause_sha256")', SOURCE)
        self.assertIn('sha256_text(case["reference_root_cause"])', SOURCE)
        self.assertIn("Restricted gold root-cause SHA-256 mismatch", SOURCE)

    def test_run_output_identity_is_not_derived_from_hidden_condition(self):
        body = ast.get_source_segment(SOURCE, function_node("run_study"))
        self.assertIn("secrets.token_hex(10)", body)
        self.assertNotIn('str(output_index) + "|" + case["case_id"]', body)


if __name__ == "__main__":
    unittest.main()
