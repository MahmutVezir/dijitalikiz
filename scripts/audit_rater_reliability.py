from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

LABELS = ("correct", "partially_correct", "incorrect", "unscorable")
CHALLENGE_CLASSES = (
    "canonical_correct",
    "correct_paraphrase",
    "wrong_mechanism",
    "negated_correct_phrase",
    "multiple_hypotheses",
    "partial_diagnosis",
    "unscorable_output",
)
RESPONSE_ORIGINS = (
    "independent_model_output",
    "human_authored_control",
    "synthetic_adversarial_control",
)
EXPECTED_ITEM_FIELDS = {"item_id", "challenge_class", "source_case_id", "response_origin"}
REQUIRED_COLUMNS = ("item_id", "rater_a", "rater_b")
DEFAULT_MIN_EXACT_AGREEMENT = 0.80
DEFAULT_MIN_KAPPA = 0.70
MIN_EXAMPLES_PER_CHALLENGE_CLASS = 4
MIN_INDEPENDENT_MODEL_OUTPUTS = 7
MIN_DISTINCT_MODEL_CASES = 7
MIN_CONTROL_EXAMPLES = 7


def load_ratings_csv(path: Path) -> list[dict[str, str]]:
    """Load paired, anonymized calibration labels; answer text and identities are not accepted."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or tuple(reader.fieldnames) != REQUIRED_COLUMNS:
            raise ValueError(
                "CSV header must be exactly: " + ",".join(REQUIRED_COLUMNS)
            )
        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, start=2):
            if None in row or any(row.get(column) is None for column in REQUIRED_COLUMNS):
                raise ValueError(f"Malformed CSV row at line {row_number}.")
            rows.append({column: str(row[column]).strip() for column in REQUIRED_COLUMNS})
    return rows


def validate_expected_item_metadata(
    expected_items: Sequence[dict[str, str]],
) -> list[str]:
    """Enforce the preregistered calibration-size, class-diversity and origin requirements."""
    if len(expected_items) < MIN_EXAMPLES_PER_CHALLENGE_CLASS * len(CHALLENGE_CLASSES):
        raise ValueError(
            "Calibration metadata must contain at least 28 items "
            "(four per each of the seven challenge classes)."
        )

    ids: list[str] = []
    class_counts: Counter[str] = Counter()
    origin_counts: Counter[str] = Counter()
    model_case_ids: set[str] = set()

    for row_number, item in enumerate(expected_items, start=1):
        if not isinstance(item, dict) or set(item) != EXPECTED_ITEM_FIELDS:
            raise ValueError(
                f"Expected-item metadata row {row_number} must contain exactly "
                "item_id, challenge_class, source_case_id, response_origin."
            )

        item_id = item.get("item_id")
        challenge_class = item.get("challenge_class")
        source_case_id = item.get("source_case_id")
        origin = item.get("response_origin")
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError(f"Expected-item metadata row {row_number} has an empty item_id.")
        if challenge_class not in CHALLENGE_CLASSES:
            raise ValueError(
                f"Expected-item metadata row {row_number} has an invalid challenge_class."
            )
        if not isinstance(source_case_id, str) or not source_case_id.strip():
            raise ValueError(
                f"Expected-item metadata row {row_number} has an empty source_case_id."
            )
        if origin not in RESPONSE_ORIGINS:
            raise ValueError(
                f"Expected-item metadata row {row_number} has an invalid response_origin."
            )

        ids.append(item_id)
        class_counts[challenge_class] += 1
        origin_counts[origin] += 1
        if origin == "independent_model_output":
            model_case_ids.add(source_case_id)

    if len(ids) != len(set(ids)):
        raise ValueError("Expected-item metadata contains duplicate item_id values.")

    missing_classes = [
        challenge_class for challenge_class in CHALLENGE_CLASSES
        if class_counts[challenge_class] < MIN_EXAMPLES_PER_CHALLENGE_CLASS
    ]
    if missing_classes:
        raise ValueError(
            "Calibration challenge-class composition is below the preregistered minimum: "
            + ", ".join(missing_classes)
        )

    if origin_counts["independent_model_output"] < MIN_INDEPENDENT_MODEL_OUTPUTS:
        raise ValueError(
            "Calibration requires at least seven independent model-output examples."
        )
    if len(model_case_ids) < MIN_DISTINCT_MODEL_CASES:
        raise ValueError(
            "Independent model-output examples must come from at least seven distinct defect cases."
        )
    control_count = (
        origin_counts["human_authored_control"]
        + origin_counts["synthetic_adversarial_control"]
    )
    if control_count < MIN_CONTROL_EXAMPLES:
        raise ValueError("Calibration requires at least seven control examples.")

    return ids


def _validate_rating_rows(
    rows: Sequence[dict[str, str]],
    expected_item_ids: Sequence[str],
) -> None:
    if not expected_item_ids:
        raise ValueError("The preregistered calibration item list must be non-empty.")
    observed_ids: list[str] = []
    for index, row in enumerate(rows, start=1):
        item_id = row.get("item_id", "").strip()
        if not item_id:
            raise ValueError(f"Rating row {index} has an empty item_id.")
        observed_ids.append(item_id)
        for rater_key in ("rater_a", "rater_b"):
            label = row.get(rater_key, "").strip()
            if label not in LABELS:
                raise ValueError(
                    f"Rating row {index} has an invalid {rater_key} label: {label!r}."
                )
    if len(observed_ids) != len(set(observed_ids)):
        raise ValueError("Ratings contain duplicate item IDs.")
    expected = set(expected_item_ids)
    observed = set(observed_ids)
    if observed != expected:
        missing = sorted(expected - observed)
        unexpected = sorted(observed - expected)
        raise ValueError(
            "Ratings do not match the preregistered item list; "
            f"missing={missing}, unexpected={unexpected}."
        )


def compute_rater_reliability(
    rows: Sequence[dict[str, str]],
    expected_items: Sequence[dict[str, str]],
) -> dict[str, object]:
    """Compute agreement under the full preregistered calibration composition."""
    if not rows:
        raise ValueError("No real paired ratings were supplied.")
    expected_item_ids = validate_expected_item_metadata(expected_items)
    _validate_rating_rows(rows, expected_item_ids)

    table = {left: {right: 0 for right in LABELS} for left in LABELS}
    row_totals = {label: 0 for label in LABELS}
    column_totals = {label: 0 for label in LABELS}
    agree_count = 0

    for row in rows:
        left = row["rater_a"].strip()
        right = row["rater_b"].strip()
        table[left][right] += 1
        row_totals[left] += 1
        column_totals[right] += 1
        if left == right:
            agree_count += 1

    total = len(rows)
    exact_agreement = agree_count / total
    expected_agreement = sum(
        row_totals[label] * column_totals[label] for label in LABELS
    ) / (total * total)
    if expected_agreement == 1.0:
        kappa: float | None = None
    else:
        kappa = (exact_agreement - expected_agreement) / (1.0 - expected_agreement)

    gate_reasons: list[str] = []
    if exact_agreement < DEFAULT_MIN_EXACT_AGREEMENT:
        gate_reasons.append("exact_agreement_below_threshold")
    if kappa is None:
        gate_reasons.append("cohen_kappa_undefined")
    elif kappa < DEFAULT_MIN_KAPPA:
        gate_reasons.append("cohen_kappa_below_threshold")
    gate_passed = not gate_reasons

    challenge_counts = Counter(item["challenge_class"] for item in expected_items)
    origin_counts = Counter(item["response_origin"] for item in expected_items)
    model_case_count = len({
        item["source_case_id"] for item in expected_items
        if item["response_origin"] == "independent_model_output"
    })
    control_count = (
        origin_counts["human_authored_control"]
        + origin_counts["synthetic_adversarial_control"]
    )

    return {
        "status": "pass" if gate_passed else "blocked",
        "gate_passed": gate_passed,
        "calibration_only": True,
        "model_inference_permitted": False,
        "rating_count": total,
        "labels": list(LABELS),
        "exact_agreement": round(exact_agreement, 6),
        "cohen_kappa": None if kappa is None else round(kappa, 6),
        "expected_agreement": round(expected_agreement, 6),
        "thresholds": {
            "min_exact_agreement": DEFAULT_MIN_EXACT_AGREEMENT,
            "min_cohen_kappa": DEFAULT_MIN_KAPPA,
        },
        "calibration_composition": {
            "challenge_class_counts": {
                challenge_class: challenge_counts[challenge_class]
                for challenge_class in CHALLENGE_CLASSES
            },
            "response_origin_counts": {
                origin: origin_counts[origin] for origin in RESPONSE_ORIGINS
            },
            "distinct_model_output_cases": model_case_count,
            "control_example_count": control_count,
        },
        "contingency_table": table,
        "rater_a_marginals": row_totals,
        "rater_b_marginals": column_totals,
        "gate_reasons": gate_reasons,
        "interpretation": (
            "Reliability gate passed for the declared calibration items only."
            if gate_passed
            else "Reliability gate remains blocked; do not relax thresholds after confirmatory outcomes."
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit agreement between two independent raters on a preregistered calibration set."
    )
    parser.add_argument("--ratings-csv", required=True, type=Path)
    parser.add_argument(
        "--expected-item-metadata",
        required=True,
        type=Path,
        help="JSON array with item_id, challenge_class, source_case_id and response_origin.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional aggregate report path; raw ratings and answers are never copied to it.",
    )
    args = parser.parse_args(argv)

    try:
        expected_items = json.loads(
            args.expected_item_metadata.read_text(encoding="utf-8")
        )
        if not isinstance(expected_items, list) or not all(
            isinstance(item, dict) for item in expected_items
        ):
            raise ValueError("Expected-item metadata file must be a JSON array of objects.")
        rows = load_ratings_csv(args.ratings_csv)
        report = compute_rater_reliability(rows, expected_items)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    print(serialized, end="")
    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(serialized, encoding="utf-8")
    return 0 if report["gate_passed"] is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
