import hashlib
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


def test_frozen_manifest_accepts_complete_cases(tmp_path):
    case_dir = tmp_path / "data" / "benchmark" / "cases"
    assessment_dir = tmp_path / "data" / "assessments"
    case_dir.mkdir(parents=True)
    assessment_dir.mkdir(parents=True)

    for case_id in ("main-a", "main-b"):
        case = {
            "case_id": case_id,
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
            "case_id": case_id,
            "eligible_for_main": True,
            "contamination_risk": "medium",
        }
        (case_dir / f"{case_id}.json").write_text(
            json.dumps(case), encoding="utf-8"
        )
        (assessment_dir / f"{case_id}.json").write_text(
            json.dumps(assessment), encoding="utf-8"
        )

    rubric_path = tmp_path / "data" / "benchmark" / "evaluation_rubric.json"
    rubric_path.parent.mkdir(parents=True, exist_ok=True)
    rubric_bytes = json.dumps({
        "primary_endpoint": "root_cause_correctness_with_predeclared_aliases",
        "cases": [
            {"case_id": "main-a", "root_cause_aliases": ["root cause A"]},
            {"case_id": "main-b", "root_cause_aliases": ["root cause B"]},
        ],
    }).encode("utf-8")
    rubric_path.write_bytes(rubric_bytes)

    errors = validate_manifest({
        "status": "frozen",
        "scoring_rubric": {
            "path": "data/benchmark/evaluation_rubric.json",
            "sha256": hashlib.sha256(rubric_bytes).hexdigest(),
            "primary_endpoint": "root_cause_correctness_with_predeclared_aliases",
        },
        "case_ids": ["main-a", "main-b"],
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
    }, root=tmp_path)
    assert errors == []
