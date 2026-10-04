from pathlib import Path
import json

from scripts.analyze_case_level import build_result, load_evaluation


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


def test_incomplete_evaluation_is_blocked(tmp_path):
    path = tmp_path / "evaluation.json"
    path.write_text(json.dumps({"status": "incomplete", "records": []}), encoding="utf-8")
    try:
        load_evaluation(path, ["case-a"])
    except ValueError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("Incomplete evaluation must be rejected")
