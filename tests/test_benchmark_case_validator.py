import json
from pathlib import Path

from scripts.validate_benchmark_case import validate


ROOT = Path(__file__).resolve().parents[1]


def test_all_frozen_pilot_cases_pass_case_validator():
    case_paths = [
        ROOT / "data" / "pilot" / "commons-math-defects4j-MATH-927.json",
        ROOT / "data" / "pilot" / "commons-math-defects4j-MATH-950.json",
        ROOT / "data" / "pilot" / "commons-math-defects4j-MATH-988.json",
    ]
    for path in case_paths:
        assert validate(path) == [], json.dumps({"path": str(path), "errors": validate(path)})
