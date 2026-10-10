import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.validate_followup_v2_protocol import ROOT, validate_protocol


def load_manifest():
    return json.loads(
        (ROOT / "data" / "followup_v2" / "protocol_manifest.json").read_text(encoding="utf-8")
    )


def test_followup_v2_draft_manifest_matches_schema_but_stays_blocked():
    manifest = load_manifest()
    schema = json.loads(
        (ROOT / "schemas" / "followup_v2_protocol.schema.json").read_text(encoding="utf-8")
    )
    assert list(Draft202012Validator(schema).iter_errors(manifest)) == []
    report = validate_protocol(manifest, ROOT)
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert report["heldout_case_count"] == 0
    assert "heldout_case_pool_below_minimum" in report["issues"]
    assert "scoring_calibration_not_frozen_adjudicated" in report["issues"]
    assert "gate_pending:two_reviewer_ground_truth_adjudication" in report["issues"]


def test_followup_v2_manifest_keeps_primary_contrast_as_graph_vs_matched_prose():
    manifest = load_manifest()
    assert manifest["design"]["conditions"][0]["id"] == "A"
    assert manifest["design"]["conditions"][1]["id"] == "B"
    assert manifest["design"]["conditions"][2]["id"] == "C"
    assert manifest["design"]["primary_contrast"] == ["C", "B"]
    assert manifest["design"]["primary_unit"] == "independent software defect case"


def test_followup_v2_output_count_is_case_by_condition_by_seed_product():
    manifest = load_manifest()
    sample = manifest["sample_size"]
    assert sample["target_model_outputs"] == (
        sample["target_independent_case_count"]
        * sample["conditions"]
        * sample["replications_per_condition"]
    )
    assert sample["target_model_outputs"] == 915


def test_followup_v2_validator_blocks_historical_case_reuse():
    manifest = load_manifest()
    changed = copy.deepcopy(manifest)
    changed["case_pool"]["case_ids"] = ["commons-math-defects4j-MATH-305"]
    report = validate_protocol(changed, ROOT)
    assert any(
        issue.startswith("heldout_case_overlap:")
        for issue in report["issues"]
    )
    assert report["model_inference_permitted"] is False


def test_followup_v2_draft_does_not_authorize_inference_even_if_manifest_field_is_tampered():
    manifest = load_manifest()
    changed = copy.deepcopy(manifest)
    changed["model_inference_permitted"] = True
    report = validate_protocol(changed, ROOT)
    assert report["status"] == "blocked"
    assert report["model_inference_permitted"] is False
    assert "protocol_model_or_generation_not_frozen" in report["issues"]


def test_discovery_screening_audit_records_red_green_evidence_without_authorizing_inference():
    audit = json.loads(
        (ROOT / "data" / "followup_v2" / "discovery_screening_audit.json").read_text(encoding="utf-8")
    )
    assert audit["status"] == "technical_screening_pass"
    assert audit["policy"]["model_inference_performed"] is False
    assert audit["policy"]["independent_human_source_review_completed"] is False
    assert audit["policy"]["separate_adjudication_completed"] is False
    assert audit["policy"]["heldout_confirmatory_inclusion_authorized"] is False

    candidates = audit["candidates"]
    case_ids = [candidate["case_id"] for candidate in candidates]
    assert len(case_ids) == len(set(case_ids)) == 6
    summary = audit["screening_summary"]
    assert summary == {
        "total_leads": 6,
        "red_green_pass": 6,
        "failed_or_unresolved": 0,
        "independent_human_review_complete": 0,
        "adjudication_complete": 0,
        "heldout_eligible": 0,
        "target_heldout_independent_cases": 61,
    }

    for candidate in candidates:
        assert len(candidate["pre_fix_sha"]) == 40
        assert len(candidate["fixed_sha"]) == 40
        assert candidate["pre_fix_sha"] != candidate["fixed_sha"]
        assert candidate["reproduction_status"] == "independent_ci_red_green_pass"
        assert candidate["heldout_confirmatory_eligible"] is False
        assert candidate["human_review_status"] == "pending"
        assert len(candidate["artifact_sha256"]) == 64
        assert candidate["regression_tests"]
        for test in candidate["regression_tests"]:
            assert test["pre_fix"] == "failed_as_expected"
            assert test["fixed"] == "passed"
            assert test["failure_count"] >= 1


def test_discovery_leads_do_not_overlap_historical_or_calibration_cases():
    audit = json.loads(
        (ROOT / "data" / "followup_v2" / "discovery_screening_audit.json").read_text(encoding="utf-8")
    )
    lead_ids = {candidate["case_id"] for candidate in audit["candidates"]}
    pilot = json.loads((ROOT / "data" / "pilot" / "pilot_manifest.json").read_text(encoding="utf-8"))
    benchmark = json.loads((ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8"))
    calibration = json.loads((ROOT / "data" / "calibration" / "case_pool_manifest.json").read_text(encoding="utf-8"))

    excluded = set(pilot.get("cases", []))
    excluded |= set(benchmark.get("case_ids", []))
    excluded |= set(benchmark.get("pilot_case_ids", []))
    excluded |= {
        row["case_id"] for row in calibration.get("candidates", [])
        if isinstance(row, dict) and isinstance(row.get("case_id"), str)
    }
    assert lead_ids.isdisjoint(excluded)

