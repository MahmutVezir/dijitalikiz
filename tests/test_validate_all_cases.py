from scripts.validate_all_cases import validate_directory


def test_empty_case_directories_are_valid(tmp_path):
    assert validate_directory(tmp_path) == []
