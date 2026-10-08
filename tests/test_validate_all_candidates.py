from pathlib import Path

from scripts.validate_all_candidates import validate_all


def test_candidate_pool_script_exists():
    assert Path(__file__).resolve().parents[1].joinpath(
        "scripts", "validate_all_candidates.py"
    ).is_file()


def test_empty_candidate_pool_is_valid(tmp_path):
    errors = validate_all(
        tmp_path / "candidates",
        tmp_path / "assessments",
    )
    assert errors == []
