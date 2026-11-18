import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research_candidates" / "evidence_abstention"


def load_json(name):
    return json.loads((RESEARCH / name).read_text(encoding="utf-8"))


def test_v02_manifest_is_exploratory_and_not_confirmatory():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    design = manifest["design"]
    assert manifest["protocol_version"] == "0.2-exploratory-draft"
    assert design["study_type"] == "exploratory_feasibility"
    assert design["minimum_independent_cases"] == 1
    assert design["target_independent_cases"] == 20
    assert design["minimum_upstream_projects"] == 1
    assert design["target_upstream_projects"] == 20
    assert design["planned_outputs_at_15_cases"] == 90
    assert design["planned_outputs_at_stretch_target"] == 120


def test_v02_registry_is_empty_and_inference_is_disabled():
    registry = load_json("SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json")
    assert registry["status"] == "empty_no_cases_accepted"
    assert registry["accepted_case_count"] == 0
    assert registry["accepted_project_count"] == 0
    assert registry["records"] == []
    assert registry["inference_authorized"] is False


def test_second_human_output_rater_is_identified_but_not_yet_approved():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    review = manifest["human_review"]
    rater_b = review["second_human_rater"]
    assert review["human_human_second_rater"] is True
    assert rater_b["public_pseudonym"] == "Rater_B"
    assert rater_b["status"] == "identified_pending_explicit_consent_and_case_specific_independence_screen"
    assert rater_b["consent_confirmed"] is False
    assert rater_b["independence_screen_complete"] is False
    assert rater_b["is_external_auditor"] is False
    assert rater_b["is_gold_or_tier_adjudicator"] is False
    assert review["human_human_interrater_reliability_claimed"] is False
    assert review["cohen_kappa_calculated"] is False
    assert review["ai_critique_is_human_rating"] is False
    assert review["independent_external_audit_claimed"] is False
    assert review["second_human_tier_review"] is False


def test_qwen_remains_candidate_only_and_not_loaded():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    assert manifest["model"]["id"] == "Qwen/Qwen2.5-3B-Instruct"
    assert manifest["model"]["revision"] == "aa8e72537993ba99e69dfaafa59ed015b17504d1"
    assert manifest["model"]["license_identifier"] == "qwen-research"
    assert manifest["model"]["license_review_status"] == "pending_exact_revision_review"
    assert manifest["model_loading_performed"] is False
    assert manifest["model_inference_performed"] is False
    assert manifest["inference_allowed"] is False


def test_pinned_dataset_identity_is_preserved():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    dataset = manifest["dataset"]
    assert dataset["file_revision"] == "fb9aa226b2ce37c708ea7732e7b980abacdadb67"
    assert dataset["file_sha256"] == "7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9"
    assert dataset["train_rows"] == 6272


def test_v02_manifest_does_not_apply_legacy_confirmatory_gates():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    notes = "\n".join(manifest["notes"])
    assert "v0.1 confirmatory manifest, case schema/validator" in notes
    assert "do not use them to claim v0.2 readiness" in notes
    assert "A second human output rater (public pseudonym Rater_B) has been identified" in notes
    assert "The v0.2 dual-human model-output scoring rubric" in notes
    assert "no human-human ratings or Cohen kappa have yet been produced" in notes
    assert "scoring rules are specified in SWE_REBENCH_V2_OUTPUT_ADJUDICATION_RUBRIC_V0_1.md" not in notes
    assert "interval method must be selected, justified, and tested before outcome scoring is unblinded" in manifest["design"]["primary_analysis"]


def test_partial_support_is_separate_from_strict_primary_endpoint():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    design = manifest["design"]
    assert design["primary_endpoint"] == "E3 case-level strictly unsupported or contradicted asserted root-cause diagnosis; paired P1 versus P0"
    assert "partially_supported" in design["outcome_categories"]
    assert "excluded from the strict primary unsafe endpoint" in design["partial_support_handling"]


def test_dual_human_scoring_rubric_preserves_blinding_and_original_ratings():
    rubric = (ROOT / "research_candidates" / "evidence_abstention" / "SWE_REBENCH_V2_DUAL_HUMAN_OUTPUT_SCORING_RUBRIC_V0_1_DRAFT_2026-11-18.md").read_text(encoding="utf-8")
    assert "partially_supported" in rubric
    assert "unsupported" in rubric
    assert "contradicted" in rubric
    assert "invalid_or_unscorable" in rubric
    assert "excluded from the strict primary binary endpoint" in rubric
    assert "A correct but unsupported guess remains unsupported" in rubric
    assert "ChatGPT is never counted as a human rater" in rubric
    assert "Both original ratings are locked before discussion" in rubric
    assert "hidden E1/E2/E3 label" in rubric
    assert "case-cluster" in rubric
    assert "Rater B" in rubric
    assert "not authorization for model inference" in rubric

def test_human_evaluator_amendment_preserves_exposure_exclusion_and_roles():
    amendment = (ROOT / "research_candidates" / "evidence_abstention" / "HUMAN_EVALUATOR_AMENDMENT_V0_1_2026-11-18.md").read_text(encoding="utf-8")
    assert "The existing v0.2 candidate rule excluding cases used for earlier pipeline debugging" in amendment
    assert "does not erase the project lead's prior source exposure" in amendment
    assert "Rater B's proposed role is an independent human scorer" in amendment
    assert "not an authorization for model loading, inference, scoring, or case acceptance" in amendment
