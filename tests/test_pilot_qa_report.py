from scripts.pilot_qa_report import build_report


def test_qa_report_makes_no_scientific_claims():
    report = build_report(
        {"status": "incomplete", "expected_records": 40, "found_records": 0, "by_condition": {}, "case_level": {}, "duplicate_output_groups": []},
        {"cases": ["case-a"]},
        {"case-a": {"contamination_risk": "unknown"}},
    )
    assert report["scientific_result_claims"] == "none"
    assert "pilot_contamination_risk_unresolved:case-a" in report["flags"]


def test_qa_report_uses_frozen_review_when_assessment_is_missing_or_unknown():
    report = build_report(
        {"status": "complete", "expected_records": 40, "found_records": 40,
         "by_condition": {}, "case_level": {}, "duplicate_output_groups": []},
        {"cases": ["case-a", "case-b"]},
        {"case-a": {"contamination_risk": "unknown"}},
        {"decisions": [
            {"case_id": "case-a", "decision": "include", "contamination_risk": "high"},
            {"case_id": "case-b", "decision": "include", "contamination_risk": "medium"},
        ]},
    )
    assert report["contamination_risk"] == {"case-a": "high", "case-b": "medium"}
    assert not any(flag.startswith("pilot_contamination_risk_unresolved") for flag in report["flags"])
