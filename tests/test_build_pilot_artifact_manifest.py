from pathlib import Path

from scripts import build_pilot_artifact_manifest


def test_manifest_module_exists():
    assert Path(build_pilot_artifact_manifest.__file__).is_file()
