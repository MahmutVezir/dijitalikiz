from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_benchmark_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]


def draft_manifest() -> dict:
    return json.loads(
        (ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(
            encoding="utf-8"
        )
    )


def test_draft_manifest_is_valid_without_power_metadata():
    assert validate_manifest(draft_manifest(), ROOT) == []


def test_frozen_manifest_requires_power_metadata():
    manifest = draft_manifest()
    manifest.update(
        status="frozen",
        case_ids=["dummy"],
        contamination_audit_completed=True,
    )
    manifest.pop("power_assumption", None)
    errors = validate_manifest(manifest, ROOT)
    assert any("power_assumption" in error for error in errors)


def test_frozen_manifest_rejects_case_count_below_required():
    manifest = draft_manifest()
    manifest.update(
        status="frozen",
        case_ids=["dummy"],
        pilot_case_ids=[],
        contamination_audit_completed=True,
        power_assumption={
            "p_standard_only": 0.50,
            "p_ccdg_only": 0.10,
            "target_power": 0.80,
            "alpha": 0.05,
            "required_case_count": 2,
            "achieved_power": 0.8085,
        },
    )
    errors = validate_manifest(manifest, ROOT)
    assert "confirmatory case count is below the predeclared required_case_count" in errors


def test_frozen_manifest_accepts_complete_power_metadata(tmp_path):
    manifest = draft_manifest()
    manifest.update(
        status="frozen",
        case_ids=["case-a", "case-b"],
        pilot_case_ids=[],
        contamination_audit_completed=True,
        power_assumption={
            "p_standard_only": 0.50,
            "p_ccdg_only": 0.10,
            "target_power": 0.80,
            "alpha": 0.05,
            "required_case_count": 2,
            "achieved_power": 0.8085,
        },
    )

    for case_id in manifest["case_ids"]:
        case_path = tmp_path / "data" / "benchmark" / "cases" / f"{case_id}.json"
        case_path.parent.mkdir(parents=True, exist_ok=True)
        case_path.write_text(json.dumps({
            "case_id": case_id,
            "source": "test",
            "source_url": "https://example.com/case",
            "publication_date": "2026-01-01",
            "technology": "test",
            "error_description": "independent defect",
            "i_base": ["A calls B"],
            "ccdg": [{"source": "A", "target": "B", "relation": "calls", "details": "dependency"}],
            "ground_truth": {
                "component": "B",
                "entity": "B",
                "operation": "operation",
                "root_cause": "root_cause_class",
                "required_relations": ["A", "B"],
            },
            "split": "confirmatory",
        }, indent=2), encoding="utf-8")

        assessment_path = tmp_path / "data" / "assessments" / f"{case_id}.json"
        assessment_path.parent.mkdir(parents=True, exist_ok=True)
        assessment_path.write_text(json.dumps({
            "case_id": case_id,
            "eligible_for_main": True,
            "contamination_risk": "low",
        }), encoding="utf-8")

    assert validate_manifest(manifest, tmp_path) == []
