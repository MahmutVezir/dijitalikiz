from scripts.validate_all_cases import validate_directory


def test_empty_case_directories_are_valid(tmp_path):
    assert validate_directory(tmp_path) == []


def test_pilot_control_files_are_not_treated_as_cases(tmp_path):
    pilot_dir = tmp_path / "pilot"
    pilot_dir.mkdir()
    (pilot_dir / "pilot_manifest.json").write_text("{}")
    assert validate_directory(pilot_dir, expected_split="pilot") == []


def test_missing_or_wrong_split_is_reported(tmp_path):
    case_path = tmp_path / "case.json"
    case_path.write_text('{"case_id": "case"}', encoding="utf-8")
    errors = validate_directory(tmp_path, expected_split="pilot")
    assert errors
    assert "source_url is empty" in " ".join(errors)
