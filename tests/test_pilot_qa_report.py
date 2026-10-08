from scripts.pilot_qa_report import build_report


def test_qa_report_makes_no_scientific_claims():
    report = build_report(
        {"status": "incomplete", "expected_records": 30, "found_records": 0, "by_condition": {}, "case_level": {}, "duplicate_output_groups": []},
        {"cases": ["case-a"]},
        {"case-a": {"contamination_risk": "unknown"}},
    )
    assert report["scientific_result_claims"] == "none"
    assert "pilot_contamination_risk_unresolved:case-a" in report["flags"]
