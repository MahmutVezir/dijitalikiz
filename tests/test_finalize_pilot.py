from pathlib import Path

from scripts import finalize_pilot


def test_finalize_module_exists():
    assert Path(finalize_pilot.__file__).is_file()
