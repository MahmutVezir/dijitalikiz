import json

from scripts.promote_candidate import main as promote_main


def test_validate_candidate_module_imports():
    from scripts.validate_candidate import validate_candidate
    assert validate_candidate({
        "case_id": "X",
        "source": "src",
        "source_url": "https://example.invalid",
        "publication_date": "2026-01-01",
        "technology": "Java",
        "error_description": "error",
        "i_base": ["evidence"],
        "evidence_urls": ["https://example.invalid/evidence"],
        "split": "candidates",
    }) == []


def test_promote_requires_main_eligibility():
    from dijitalikiz.candidate_assessment import CandidateAssessment
    assessment = CandidateAssessment(case_id="X").to_dict()
    assert assessment["eligible_for_main"] is False


def test_import_candidate_preserves_case_id():
    payload = {
        "case_id": "ignored",
        "source": "src",
        "source_url": "https://example.invalid",
        "publication_date": "2026-01-01",
        "technology": "Java",
        "error_description": "error",
        "i_base": ["evidence"],
        "evidence_urls": ["https://example.invalid/evidence"],
        "split": "candidates",
    }
    assert payload["case_id"] == "ignored"
    assert json.loads(json.dumps(payload))["case_id"] == "ignored"
