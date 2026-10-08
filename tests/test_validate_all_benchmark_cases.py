from pathlib import Path
import json

from scripts.validate_all_benchmark_cases import main as validate_main

ROOT = Path(__file__).resolve().parents[1]

def test_preselected_confirmatory_cases_are_valid():
    manifest = json.loads((ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["case_ids"]) == 16
    assert validate_main([]) == 0
