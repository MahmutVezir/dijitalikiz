import json
from pathlib import Path

from scripts.validate_benchmark_manifest import validate_manifest


def test_draft_manifest_can_be_empty():
    assert validate_manifest({
        "status": "draft",
        "case_ids": [],
        "pilot_case_ids": ["pilot-a"],
    }) == []


def test_pilot_overlap_is_rejected():
    errors = validate_manifest({
        "status": "draft",
        "case_ids": ["pilot-a"],
        "pilot_case_ids": ["pilot-a"],
    })
    assert any("overlap" in error for error in errors)


def test_frozen_manifest_requires_power_assumption():
    errors = validate_manifest({
        "status": "frozen",
        "case_ids": ["main-a"],
        "pilot_case_ids": ["pilot-a"],
        "contamination_audit_completed": True,
    }, root=Path("/nonexistent"))
    assert any("power_assumption" in error for error in errors)


def test_frozen_manifest_rejects_missing_case_and_assessment():
    errors = validate_manifest({
        "status": "frozen",
        "case_ids": ["main-a"],
        "pilot_case_ids": ["pilot-a"],
        "contamination_audit_completed": True,
        "power_assumption": {
            "p_standard_only": 0.10,
            "p_ccdg_only": 0.30,
            "target_power": 0.80,
            "alpha": 0.05,
            "required_case_count": 2,
            "achieved_power": 0.8030,
        },
    }, root=Path("/nonexistent"))
    assert any("missing benchmark case file" in error for error in errors)
    assert any("missing assessment file" in error for error in errors)


def test_frozen_manifest_accepts_complete_case(tmp_path):
    (tmp_path / "data" / "benchmark" / "cases").mkdir(parents=True)
    (tmp_path / "data" / "assessments").mkdir(parents=True)

    case = {
        "case_id": "main-a",
        "source": "source",
        "source_url": "https://example.invalid/case",
        "publication_date": "2026-01-01",
        "technology": "Java",
        "error_description": "desc",
        "i_base": ["evidence"],
        "ccdg": [{"source": "A", "target": "B", "relation": "calls"}],
        "ground_truth": {
            "component": "A",
            "entity": "B",
            "operation": "call",
            "root_cause": "root",
            "required_relations": ["A", "B"],
        },
        "split": "confirmatory",
    }
    assessment = {
        "case_id": "main-a",
        "eligible_for_main": True,
        "contamination_risk": "medium",
    }
    (tmp_path / "data" / "benchmark" / "cases" / "main-a.json").write_text(
        json.dumps(case), encoding="utf-8"
    )
    (tmp_path / "data" / "assessments" / "main-a.json").write_text(
        json.dumps(assessment), encoding="utf-8"
    )

    errors = validate_manifest({
        "status": "frozen",
        "case_ids": ["main-a"],
        "pilot_case_ids": ["pilot-a"],
        "contamination_audit_completed": True,
        "power_assumption": {
            "p_standard_only": 0.10,
            "p_ccdg_only": 0.30,
            "target_power": 0.80,
            "alpha": 0.05,
            "required_case_count": 1,
            "achieved_power": 0.8030,
        },
    }, root=tmp_path)
    assert errors == []
