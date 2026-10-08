import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


def validate(schema_path: Path, payload: dict):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)


def test_research_case_schema_accepts_real_pilot_case():
    case_path = ROOT / "data" / "pilot" / "commons-math-defects4j-MATH-927.json"
    validate(
        ROOT / "schemas" / "research_case.schema.json",
        json.loads(case_path.read_text(encoding="utf-8")),
    )


def test_diagnostic_output_schema_accepts_frozen_shape():
    validate(
        ROOT / "schemas" / "diagnostic_output.schema.json",
        {
            "diagnosed_component": "C",
            "root_cause_class": "R",
            "affected_entity": "E",
            "explanation": "operation",
        },
    )


def test_benchmark_manifest_schema_accepts_draft_manifest():
    validate(
        ROOT / "schemas" / "benchmark_manifest.schema.json",
        json.loads(
            (ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(
                encoding="utf-8"
            )
        ),
    )


def test_all_schema_files_are_valid_json():
    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
