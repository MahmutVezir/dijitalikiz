from pathlib import Path

from scripts import model_load_preflight


def test_smoke_test_parser_defaults():
    assert Path(model_load_preflight.__file__).is_file()
