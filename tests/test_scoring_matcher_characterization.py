import json
from pathlib import Path

from scripts.audit_scoring_matcher_characterization import characterize


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "scoring_matcher_characterization_v1.json"


def test_characterization_fixtures_are_explicitly_non_empirical():
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert fixture["status"] == "synthetic_software_test_fixtures_only"
    assert fixture["not_for_scientific_performance_claims"] is True
    assert fixture["not_model_generated"] is True
    assert fixture["not_independent_adjudication"] is True


def test_frozen_alias_matcher_matches_characterization_expectations():
    report = characterize()
    assert report["status"] == "characterization_passed"
    assert report["scientific_performance_estimate"] is False
    assert report["model_outputs_evaluated"] == 0
    assert report["frozen_confirmatory_records_modified"] == 0
    assert report["matcher_behavior_matches_fixture_expectations"] is True


def test_characterization_exposes_false_rejection_and_false_acceptance_modes():
    report = characterize()
    assert "synthetic_correct_paraphrase" in report["synthetic_correct_examples_rejected_by_matcher"]
    assert "synthetic_negated_alias" in report["synthetic_incorrect_examples_accepted_by_matcher"]


def test_unresolved_hypotheses_are_not_treated_as_empirical_success():
    report = characterize()
    assert "synthetic_multiple_guesses" in report["ambiguous_examples_with_alias_hits"]
    assert "synthetic_alias_as_unselected_quote" in report["ambiguous_examples_with_alias_hits"]
