from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from dijitalikiz.models import DiagnosticOutput
from scripts.evaluate_confirmatory import root_cause_alias_match

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "scoring_matcher_characterization_v1.json"
RUBRIC_PATH = ROOT / "data" / "benchmark" / "evaluation_rubric.json"
ALLOWED_LABELS = {"correct", "partially_correct", "incorrect", "unscorable"}


def characterize() -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))

    if fixture.get("status") != "synthetic_software_test_fixtures_only":
        raise ValueError("Fixture status must explicitly identify this as synthetic test data.")
    if fixture.get("not_for_scientific_performance_claims") is not True:
        raise ValueError("Fixture must prohibit scientific performance claims.")
    if fixture.get("not_model_generated") is not True or fixture.get("not_independent_adjudication") is not True:
        raise ValueError("Fixture provenance flags are missing or invalid.")

    case_id = fixture["case_id_for_alias_reference"]
    rubric_cases = {item["case_id"]: item["root_cause_aliases"] for item in rubric["cases"]}
    if case_id not in rubric_cases:
        raise ValueError(f"Alias reference case {case_id!r} is absent from the frozen rubric.")
    aliases = fixture["aliases_copied_from_frozen_rubric_without_modification"]
    if aliases != rubric_cases[case_id]:
        raise ValueError("Synthetic fixture aliases differ from the frozen rubric; do not silently drift.")

    examples = fixture.get("examples")
    if not isinstance(examples, list) or not examples:
        raise ValueError("Fixture set must contain examples.")
    observed: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for example in examples:
        example_id = example.get("example_id")
        if not isinstance(example_id, str) or not example_id or example_id in seen_ids:
            raise ValueError(f"Missing or duplicate example_id: {example_id!r}")
        seen_ids.add(example_id)
        label = example.get("expected_semantic_label_for_synthetic_test")
        if label not in ALLOWED_LABELS:
            raise ValueError(f"Unknown synthetic label {label!r} for {example_id}")
        output = DiagnosticOutput.from_dict(example["output"])
        actual = root_cause_alias_match(output, aliases)
        expected = example.get("expected_matcher_result")
        if not isinstance(expected, bool):
            raise ValueError(f"expected_matcher_result must be boolean for {example_id}")
        if actual is not expected:
            raise AssertionError(
                f"Matcher behavior changed for {example_id}: expected {expected}, got {actual}"
            )
        observed.append({
            "example_id": example_id,
            "kind": example["kind"],
            "synthetic_label": label,
            "matcher_match": actual,
            "matches_expected_characterization": actual is expected,
        })

    # This is deliberately a characterization, not a representative accuracy estimate.
    decisive = [item for item in observed if item["synthetic_label"] in {"correct", "incorrect"}]
    false_rejections = [
        item["example_id"] for item in decisive
        if item["synthetic_label"] == "correct" and not item["matcher_match"]
    ]
    false_acceptances = [
        item["example_id"] for item in decisive
        if item["synthetic_label"] == "incorrect" and item["matcher_match"]
    ]
    ambiguous_alias_hits = [
        item["example_id"] for item in observed
        if item["synthetic_label"] in {"partially_correct", "unscorable"} and item["matcher_match"]
    ]

    return {
        "status": "characterization_passed",
        "fixture_set_id": fixture["fixture_set_id"],
        "purpose": "synthetic software behavior characterization only",
        "scientific_performance_estimate": False,
        "model_outputs_evaluated": 0,
        "frozen_confirmatory_records_modified": 0,
        "example_count": len(observed),
        "matcher_behavior_matches_fixture_expectations": all(
            item["matches_expected_characterization"] for item in observed
        ),
        "synthetic_correct_examples_rejected_by_matcher": false_rejections,
        "synthetic_incorrect_examples_accepted_by_matcher": false_acceptances,
        "ambiguous_examples_with_alias_hits": ambiguous_alias_hits,
        "examples": observed,
        "interpretation": (
            "The fixture demonstrates known limitations of contiguous phrase matching. "
            "Counts are constructed examples and must not be reported as empirical model accuracy."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Characterize the frozen alias matcher on synthetic fixtures only.")
    parser.add_argument("--output", help="Optional path for a JSON characterization report.")
    args = parser.parse_args()
    report = characterize()
    serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
