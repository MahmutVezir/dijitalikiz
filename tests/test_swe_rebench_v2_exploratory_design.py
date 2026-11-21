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


def test_v02_registry_contains_dishka_and_inference_is_disabled():
    registry = load_json("SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json")
    assert registry["status"] == "contains_structurally_complete_candidates"
    assert registry["accepted_case_count"] == 3
    assert registry["accepted_project_count"] == 3
    assert len(registry["records"]) == 3
    assert [record["case_id"] for record in registry["records"]] == [
        "SRV2E-DISHKA_435", "SRV2E-EODAG_1530", "SRV2E-GEOFILEOPS_649"
    ]
    assert all(record["acceptance_decision"] == "accepted" for record in registry["records"])
    assert registry["inference_authorized"] is False


def test_single_human_output_scoring_is_the_active_v02_design():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    review = manifest["human_review"]
    assert review["human_participant_count"] == 1
    assert review["human_human_second_rater"] is False
    assert review["single_human_output_scoring"] is True
    assert review["single_human_scorer"] == "student_project_lead"
    assert review["single_human_scorer_count"] == 1
    assert review["output_scoring_raters"] == ["student_project_lead"]
    assert review["scoring_blinding_status"] == "condition_masked_not_blinded_to_case_source_gold_or_tier"
    assert review["full_researcher_source_exposure_disclosed"] is True
    assert review["human_human_interrater_reliability_claimed"] is False
    assert review["cohen_kappa_calculated"] is False
    assert review["agreement_statistics_planned"] == []
    assert review["ai_critique_is_human_rating"] is False
    assert review["independent_external_audit_claimed"] is False
    assert review["technical_review_panel"] == "not_applicable_no_additional_human_researchers_or_reviewers"
    assert review["prior_dual_human_documents"]["status"] == "superseded_historical_not_active"
    assert review["scoring_rubric_path"].endswith("SWE_REBENCH_V2_SINGLE_HUMAN_OUTPUT_SCORING_RUBRIC_V0_2_2026-11-21.md")
    assert review["amendment_path"].endswith("SINGLE_HUMAN_REVIEW_AMENDMENT_V0_2_2026-11-21.md")


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
    assert "The project has one human participant: the student project lead." in notes
    assert "second-human Rater_B proposal is superseded" in notes
    assert "No human-human agreement or Cohen kappa is claimed." in notes
    assert "scoring rules are specified in SWE_REBENCH_V2_OUTPUT_ADJUDICATION_RUBRIC_V0_1.md" not in notes
    assert "interval method must be selected, justified, and tested before outcome scoring is unblinded" in manifest["design"]["primary_analysis"]


def test_partial_support_is_separate_from_strict_primary_endpoint():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    design = manifest["design"]
    assert design["primary_endpoint"] == "E3 case-level strictly unsupported or contradicted asserted root-cause diagnosis; paired P1 versus P0"
    assert "partially_supported" in design["outcome_categories"]
    assert "excluded from the strict primary unsafe endpoint" in design["partial_support_handling"]


def test_single_human_scoring_rubric_preserves_evidence_support_and_limits():
    rubric = (ROOT / "research_candidates" / "evidence_abstention" / "SWE_REBENCH_V2_SINGLE_HUMAN_OUTPUT_SCORING_RUBRIC_V0_2_2026-11-21.md").read_text(encoding="utf-8")
    for category in ("partially_supported", "unsupported", "contradicted", "invalid_or_unscorable", "fully_supported", "valid_abstention"):
        assert category in rubric
    assert "excluded from the strict primary binary endpoint" in rubric
    assert "A correct guess is not automatically evidence-supported." in rubric
    assert "one human scorer" in rubric
    assert "condition-masked single-human scoring, not blinded scoring" in rubric
    assert "Do not calculate or claim" in rubric
    assert "not authorization for model inference" in rubric

def test_single_human_amendment_preserves_exposure_and_role_limits():
    amendment = (ROOT / "research_candidates" / "evidence_abstention" / "SINGLE_HUMAN_REVIEW_AMENDMENT_V0_2_2026-11-21.md").read_text(encoding="utf-8")
    assert "The project has one human participant" in amendment
    assert "There is no Rater B" in amendment
    assert "condition-masked single-human scoring, not blinded human scoring" in amendment
    assert "The AI critique cannot silently overwrite" not in amendment
    assert "full disclosed exposure" in amendment
    assert "inter-rater reliability or Cohen's kappa" in amendment
    assert "prior pipeline debugging, test-oracle troubleshooting or prompt calibration" in amendment
    assert "No case acceptance, model execution authorization" in amendment
