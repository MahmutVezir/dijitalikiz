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
    assert design["minimum_independent_cases"] == 15
    assert design["target_independent_cases"] == 20
    assert design["minimum_upstream_projects"] == 15
    assert design["target_upstream_projects"] == 20
    assert design["planned_outputs_at_minimum"] == 90
    assert design["planned_outputs_at_target"] == 120


def test_v02_registry_is_empty_and_inference_is_disabled():
    registry = load_json("SWE_REBENCH_V2_EXPLORATORY_CASE_REGISTRY_V0_2.json")
    assert registry["status"] == "empty_no_cases_accepted"
    assert registry["accepted_case_count"] == 0
    assert registry["accepted_project_count"] == 0
    assert registry["records"] == []
    assert registry["inference_authorized"] is False


def test_no_human_human_agreement_or_kappa_claim_is_encoded():
    manifest = load_json("SWE_REBENCH_V2_EXPLORATORY_MANIFEST_V0_2_2026-11-16.json")
    review = manifest["human_review"]
    assert review["human_human_second_rater"] is False
    assert review["human_human_interrater_reliability_claimed"] is False
    assert review["cohen_kappa_calculated"] is False
    assert review["ai_critique_is_human_rating"] is False
    assert review["independent_external_audit_claimed"] is False


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
    assert "No second human rater" in notes
    assert "v0.2 scoring rubric and case-acceptance schema/validator still require dedicated drafts" in notes
    assert "dedicated v0.2 single-researcher scoring rubric must be drafted and tested" in notes
    assert "scoring rules are specified in SWE_REBENCH_V2_OUTPUT_ADJUDICATION_RUBRIC_V0_1.md" not in notes
    assert "interval method must be selected, justified, and tested before outcome scoring is unblinded" in manifest["design"]["primary_analysis"]
