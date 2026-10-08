import json
from pathlib import Path

REVIEW = Path("data/pilot/final_candidate_review_2026-10-08.json")
MANIFEST = Path("data/pilot/pilot_manifest.json")


def test_final_candidate_review_is_deterministic_and_matches_manifest():
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    decisions = {row["case_id"]: row for row in review["decisions"]}
    assert len(decisions) == 5
    assert set(decisions) == {
        "commons-math-defects4j-MATH-927",
        "commons-math-defects4j-MATH-950",
        "commons-math-defects4j-MATH-938",
        "commons-math-defects4j-MATH-949",
        "commons-math-defects4j-MATH-988",
    }

    included = [case_id for case_id, row in decisions.items() if row["decision"] == "include"]
    excluded = [case_id for case_id, row in decisions.items() if row["decision"] == "exclude"]

    assert included == manifest["cases"] or set(included) == set(manifest["cases"])
    assert excluded == ["commons-math-defects4j-MATH-938"]
    assert review["expected_inference_records"] == 4 * 2 * 5 == manifest["expected_records"]

    assert decisions["commons-math-defects4j-MATH-949"]["dependency_strength"] == "strong"
    assert decisions["commons-math-defects4j-MATH-949"]["ccdg_suitability"] == "strong"
    assert decisions["commons-math-defects4j-MATH-949"]["eligibility"]["IC5"] == "pass"
    assert decisions["commons-math-defects4j-MATH-949"]["eligibility"]["IC6"] == "pass"
    assert decisions["commons-math-defects4j-MATH-938"]["eligibility"]["IC5"] == "fail"
    assert decisions["commons-math-defects4j-MATH-938"]["eligibility"]["IC6"] == "fail"
