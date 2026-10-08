from pathlib import Path
import json
import pytest

from scripts.analyze_case_level import (
    build_result,
    exact_mcnemar_pvalue,
    load_evaluation,
    paired_risk_difference_ci,
)


def _evaluation_payload(tmp_path: Path) -> Path:
    records = []
    for case_id in ("case-a", "case-b"):
        for condition in ("standard", "ccdg"):
            for seed in (42, 43, 44, 45, 46):
                passed = seed in (42, 43, 44) if condition == "ccdg" else seed in (42, 43)
                records.append({
                    "case_id": case_id,
                    "condition": condition,
                    "seed": seed,
                    "score": {"passed": passed},
                })
    path = tmp_path / "evaluation.json"
    path.write_text(json.dumps({"status": "complete", "records": records}), encoding="utf-8")
    return path


def test_case_level_analysis_reads_evaluation_output(tmp_path):
    path = _evaluation_payload(tmp_path)
    outcomes = load_evaluation(path, ["case-a", "case-b"])
    assert outcomes["case-a"]["standard"] is False
    assert outcomes["case-a"]["ccdg"] is True
    result = build_result(outcomes, ["case-a", "case-b"])
    assert result["n_cases"] == 2
    assert result["contingency_table"]["standard_fail_ccdg_pass"] == 2
    assert result["paired_effect_size"]["estimate"] == 1.0
    assert len(result["paired_effect_size"]["95_ci"]) == 2


def test_exact_mcnemar_is_two_sided():
    assert exact_mcnemar_pvalue(0, 0) == 1.0
    assert exact_mcnemar_pvalue(0, 2) == 0.5
    assert exact_mcnemar_pvalue(2, 0) == 0.5


def test_paired_ci_is_bounded():
    low, high = paired_risk_difference_ci(1, 3, 10)
    assert -1.0 <= low <= high <= 1.0


def test_incomplete_evaluation_is_blocked(tmp_path):
    path = tmp_path / "evaluation.json"
    path.write_text(json.dumps({"status": "incomplete", "records": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="incomplete"):
        load_evaluation(path, ["case-a"])


def test_duplicate_case_ids_are_blocked(tmp_path):
    path = _evaluation_payload(tmp_path)
    with pytest.raises(ValueError, match="case_ids must be unique"):
        load_evaluation(path, ["case-a", "case-a"])


def test_missing_seed_is_blocked(tmp_path):
    path = _evaluation_payload(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"] = [
        record for record in payload["records"]
        if not (
            record["case_id"] == "case-a"
            and record["condition"] == "ccdg"
            and record["seed"] == 46
        )
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="exactly one scored run for each seed"):
        load_evaluation(path, ["case-a", "case-b"])


def test_duplicate_seed_is_blocked(tmp_path):
    path = _evaluation_payload(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"] = [
        record for record in payload["records"]
        if not (
            record["case_id"] == "case-a"
            and record["condition"] == "standard"
            and record["seed"] == 46
        )
    ]
    payload["records"].append({
        "case_id": "case-a",
        "condition": "standard",
        "seed": 45,
        "score": {"passed": False},
    })
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="exactly one scored run for each seed"):
        load_evaluation(path, ["case-a", "case-b"])
