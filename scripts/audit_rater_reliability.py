from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Sequence

LABELS = ("correct", "partially_correct", "incorrect", "unscorable")
REQUIRED_COLUMNS = ("item_id", "rater_a", "rater_b")
DEFAULT_MIN_EXACT_AGREEMENT = 0.80
DEFAULT_MIN_KAPPA = 0.70


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


def _validate_item_ids(rows: Sequence[dict[str, str]], expected_item_ids: Sequence[str]) -> None:
    if not expected_item_ids:
        raise ValueError("The calibration item list must be non-empty and preregistered.")
    if any(not isinstance(item_id, str) or not item_id.strip() for item_id in expected_item_ids):
        raise ValueError("Expected item IDs must be non-empty strings.")
    if len(expected_item_ids) != len(set(expected_item_ids)):
        raise ValueError("The preregistered calibration item list contains duplicate IDs.")
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
            f"Ratings do not match the preregistered item list; "
            f"missing={missing}, unexpected={unexpected}."
        )


def compute_rater_reliability(
    rows: Sequence[dict[str, str]],
    expected_item_ids: Sequence[str],
) -> dict[str, object]:
    """Compute agreement using fixed preregistered minima; never substitutes for human ratings."""
    if not rows:
        raise ValueError("No real paired ratings were supplied.")
    _validate_item_ids(rows, expected_item_ids)

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
    parser.add_argument("--expected-item-ids", required=True, type=Path,
                        help="JSON array containing the preregistered opaque calibration item IDs.")
    parser.add_argument("--output-json", type=Path,
                        help="Optional aggregate report path; raw ratings and answers are never copied to it.")
    args = parser.parse_args(argv)

    try:
        expected_item_ids = json.loads(args.expected_item_ids.read_text(encoding="utf-8"))
        if not isinstance(expected_item_ids, list) or not all(
            isinstance(item_id, str) for item_id in expected_item_ids
        ):
            raise ValueError("Expected item ID file must be a JSON array of strings.")
        rows = load_ratings_csv(args.ratings_csv)
        report = compute_rater_reliability(
            rows,
            expected_item_ids,
        )
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
