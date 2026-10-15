import json
from pathlib import Path

import pytest

from scripts.audit_historical_design import analyze_case, audit_project


def _case(case_id="case-a"):
    return {
        "case_id": case_id,
        "source": "Synthetic issue tracker",
        "source_url": "https://example.invalid/issues/1",
        "publication_date": "2026-01-01",
        "technology": "SyntheticProject / Python / data flow",
        "error_description": "The parser returns the wrong result after a stale mapping is retained.",
        "i_base": [
            "Parser invokes MappingStore.",
            "The fix changes how stale mapping entries are removed.",
        ],
        "ccdg": [
            {
                "source": "Parser",
                "target": "MappingStore",
                "relation": "calls",
                "details": "parser requests a mapping",
            }
        ],
        "ground_truth": {
            "component": "MappingStore",
            "entity": "stale mapping",
            "operation": "removeEntry()",
            "root_cause": "stale_mapping_not_removed",
            "required_relations": ["Parser", "MappingStore"],
        },
        "split": "confirmatory",
    }


def test_analyze_case_flags_historical_renderer_information_mismatch():
    result = analyze_case(
        _case(),
        ["stale mapping entry is not removed"],
    )

    assert result["standard_context_has_explicit_error_description"] is True
    assert result["ccdg_context_has_explicit_error_description"] is False
    assert result["standard_context_has_dependency_section"] is False
    assert result["ccdg_context_has_dependency_section"] is True
    assert result["source_and_technology_shared"] is True
    assert result["all_i_base_facts_shared_verbatim"] is True
    assert result["explicit_fix_cue_facts_in_shared_i_base"][0]["fact_id"] == "B2"
    assert result["case_alias_literal_hits_standard"] == []
    assert result["case_alias_literal_hits_ccdg"] == []


def _write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def _minimal_project(root: Path):
    benchmark = root / "data" / "benchmark"
    case = _case()
    _write(
        benchmark / "benchmark_manifest.json",
        {"status": "frozen", "case_ids": ["case-a"]},
    )
    _write(
        benchmark / "evaluation_rubric.json",
        {
            "cases": [
                {"case_id": "case-a", "root_cause_aliases": ["stale mapping entry is not removed"]}
            ]
        },
    )
    _write(benchmark / "cases" / "case-a.json", case)
    _write(benchmark / "cases" / "orphan.json", _case("orphan"))


def test_audit_uses_frozen_manifest_and_reports_unlisted_case_files(tmp_path):
    _minimal_project(tmp_path)

    result = audit_project(tmp_path)

    assert result["model_inference_performed"] is False
    assert result["historical_results_modified"] is False
    assert result["active_case_count"] == 1
    assert result["case_json_files_not_in_active_manifest"] == ["orphan"]
    assert result["legacy_context_parity"]["standard_explicit_error_description_count"] == 1
    assert result["legacy_context_parity"]["ccdg_explicit_error_description_count"] == 0
    assert result["input_cue_screen"]["case_count_with_explicit_fix_or_corrected_cue_in_I_base"] == 1


def test_audit_fails_closed_when_rubric_order_diverges_from_manifest(tmp_path):
    _minimal_project(tmp_path)
    rubric_path = tmp_path / "data" / "benchmark" / "evaluation_rubric.json"
    _write(
        rubric_path,
        {"cases": [{"case_id": "orphan", "root_cause_aliases": []}]},
    )

    with pytest.raises(ValueError, match="Rubric case IDs/order differ"):
        audit_project(tmp_path)


def test_audit_fails_closed_when_a_manifest_case_is_missing(tmp_path):
    _minimal_project(tmp_path)
    case_file = tmp_path / "data" / "benchmark" / "cases" / "case-a.json"
    case_file.unlink()

    with pytest.raises(ValueError, match="Manifest-listed cases missing"):
        audit_project(tmp_path)
