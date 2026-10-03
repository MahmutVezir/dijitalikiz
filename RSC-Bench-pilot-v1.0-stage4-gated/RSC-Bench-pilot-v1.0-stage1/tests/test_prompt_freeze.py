from pathlib import Path
import json
import pytest

from rscbench.freeze import freeze, verify_frozen
from rscbench.prompts import PromptBuilder

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "prompts/manifests/prompt_freeze.json"


def reset_manifest() -> None:
    MANIFEST.write_text(json.dumps({
        "status": "UNFROZEN",
        "protocol_version": "1.0",
        "standard_system_sha256": None,
        "standard_user_sha256": None,
        "ccdg_system_sha256": None,
        "ccdg_user_sha256": None,
        "frozen_at": None
    }, indent=2) + "\n", encoding="utf-8")


def test_freeze_and_verify():
    reset_manifest()
    freeze(ROOT)
    verify_frozen(ROOT)
    reset_manifest()


def test_frozen_change_blocks_execution():
    reset_manifest()
    freeze(ROOT)
    path = ROOT / "prompts/standard_context/system.txt"
    original = path.read_text(encoding="utf-8")
    try:
        path.write_text(original + "\nChanged.\n", encoding="utf-8")
        with pytest.raises(RuntimeError):
            verify_frozen(ROOT)
    finally:
        path.write_text(original, encoding="utf-8")
        reset_manifest()
