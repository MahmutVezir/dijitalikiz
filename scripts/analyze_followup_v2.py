from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any

LABELS = {"correct", "partially_correct", "incorrect", "unscorable"}
CONDITIONS = ("A", "B", "C")
DEFAULT_SEEDS = (42, 43, 44, 45, 46)


def exact_mcnemar_pvalue(condition_x_only: int, condition_y_only: int) -> float:
    """Exact two-sided conditional binomial test for paired binary case outcomes."""
    if condition_x_only < 0 or condition_y_only < 0:
        raise ValueError("Discordant counts must be non-negative.")
    discordant = condition_x_only + condition_y_only
    if discordant == 0:
        return 1.0

    smaller = min(condition_x_only, condition_y_only)
    tail = sum(math.comb(discordant, k) for k in range(smaller + 1)) / (2 ** discordant)
    return min(1.0, 2.0 * tail)


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    """Holm step-down adjusted p-values, returned under each original comparison key."""
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    adjusted: dict[str, float] = {}
    running = 0.0
    count = len(ordered)
    for rank, (key, pvalue) in enumerate(ordered):
        candidate = min(1.0, (count - rank) * pvalue)
        running = max(running, candidate)
        adjusted[key] = running
    return adjusted


def _percentile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("Cannot calculate percentile from empty data.")
    position = (len(sorted_values) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return sorted_values[low]
    weight = position - low
    return sorted_values[low] * (1 - weight) + sorted_values[high] * weight


def paired_bootstrap_difference_ci(
    differences: list[int],
    *,
    resamples: int = 10000,
    seed: int = 20261010,
) -> list[float]:
    """Percentile CI for paired case-level risk difference, resampling cases as pairs."""
    if not differences:
        raise ValueError("Need paired case differences.")
    if resamples < 1000:
        raise ValueError("Use at least 1000 bootstrap resamples.")
    rng = random.Random(seed)
    n = len(differences)
    boot_means: list[float] = []
    for _ in range(resamples):
        boot_means.append(sum(differences[rng.randrange(n)] for _ in range(n)) / n)
    boot_means.sort()
    return [round(_percentile(boot_means, 0.025), 6), round(_percentile(boot_means, 0.975), 6)]


def analyze_adjudicated_ratings(
    rows: list[dict[str, Any]],
    case_ids: list[str],
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    *,
    bootstrap_resamples: int = 10000,
) -> dict[str, Any]:
    """Analyze only final human-adjudicated labels; does not score raw model text itself."""
    if not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("Expected a non-empty, unique, preregistered case ID list.")
    if len(seeds) != 5 or len(set(seeds)) != 5:
        raise ValueError("This v2 protocol requires five unique, predeclared seeds.")
    expected_cells = {
        (case_id, condition, seed)
        for case_id in case_ids
        for condition in CONDITIONS
        for seed in seeds
    }
    indexed: dict[tuple[str, str, int], dict[str, Any]] = {}
    issues: list[str] = []
    for index, row in enumerate(rows, start=1):
        case_id = row.get("case_id")
        condition = row.get("condition_id")
        seed = row.get("seed")
        label = row.get("final_label")
        if not isinstance(case_id, str) or condition not in CONDITIONS or not isinstance(seed, int) or isinstance(seed, bool):
            issues.append(f"row_{index}_has_invalid_cell_key")
            continue
        key = (case_id, condition, seed)
        if key in indexed:
            issues.append(f"duplicate_rating:{case_id}:{condition}:{seed}")
            continue
        if key not in expected_cells:
            issues.append(f"unexpected_rating_cell:{case_id}:{condition}:{seed}")
            continue
        if label not in LABELS:
            issues.append(f"invalid_final_label:{case_id}:{condition}:{seed}")
            continue
        if row.get("adjudicated") is not True or not isinstance(row.get("adjudicator_id"), str) or not row["adjudicator_id"].strip():
            issues.append(f"rating_not_adjudicated:{case_id}:{condition}:{seed}")
            continue
        indexed[key] = row

    missing = sorted(expected_cells - set(indexed))
    if missing:
        issues.append(f"missing_rating_cells:{len(missing)}")

    if issues:
        return {
            "status": "blocked",
            "input_rating_count": len(rows),
            "expected_rating_count": len(expected_cells),
            "observed_adjudicated_rating_count": len(indexed),
            "issue_count": len(issues),
            "issues": issues,
            "interpretation": "No hypothesis test is computed until every expected case-condition-seed output has one valid final adjudicated label."
        }

    pass_matrix: dict[str, dict[str, bool]] = {}
    seed_label_counts: dict[str, dict[str, int]] = {}
    for case_id in case_ids:
        pass_matrix[case_id] = {}
        for condition in CONDITIONS:
            labels = [
                indexed[(case_id, condition, seed)]["final_label"]
                for seed in seeds
            ]
            correct_count = sum(label == "correct" for label in labels)
            pass_matrix[case_id][condition] = correct_count >= 3
            seed_label_counts.setdefault(condition, {"correct": 0, "partially_correct": 0, "incorrect": 0, "unscorable": 0})
            for label in labels:
                seed_label_counts[condition][label] += 1

    case_pass_counts = {
        condition: sum(pass_matrix[case_id][condition] for case_id in case_ids)
        for condition in CONDITIONS
    }
    def compare(x: str, y: str) -> dict[str, Any]:
        x_only = sum(pass_matrix[case_id][x] and not pass_matrix[case_id][y] for case_id in case_ids)
        y_only = sum(pass_matrix[case_id][y] and not pass_matrix[case_id][x] for case_id in case_ids)
        both = sum(pass_matrix[case_id][x] and pass_matrix[case_id][y] for case_id in case_ids)
        neither = len(case_ids) - x_only - y_only - both
        return {
            "contrast": f"{x}_vs_{y}",
            "n_cases": len(case_ids),
            "x_pass_y_fail": x_only,
            "y_pass_x_fail": y_only,
            "both_pass": both,
            "both_fail": neither,
            "risk_difference_x_minus_y": round((case_pass_counts[x] - case_pass_counts[y]) / len(case_ids), 6),
            "exact_two_sided_mcnemar_p": exact_mcnemar_pvalue(x_only, y_only),
        }

    primary = compare("C", "B")
    secondary_raw = {
        "B_vs_A": compare("B", "A")["exact_two_sided_mcnemar_p"],
        "C_vs_A": compare("C", "A")["exact_two_sided_mcnemar_p"],
    }
    secondary_adjusted = holm_adjust(secondary_raw)
    primary_differences = [
        int(pass_matrix[case_id]["C"]) - int(pass_matrix[case_id]["B"])
        for case_id in case_ids
    ]
    primary_ci = paired_bootstrap_difference_ci(primary_differences, resamples=bootstrap_resamples)
    return {
        "status": "pass",
        "analysis_version": "followup-v2-case-level-analysis-1.0",
        "case_count": len(case_ids),
        "output_count": len(expected_cells),
        "replications_per_case_condition": len(seeds),
        "case_level_pass_threshold": "at least 3/5 final human-adjudicated labels are correct",
        "unscorable_handling": "counts as not-correct for the primary case-condition pass rule",
        "case_level_pass_counts": case_pass_counts,
        "per_condition_output_label_counts": seed_label_counts,
        "primary_contrast": {
            **primary,
            "paired_bootstrap_95_percentile_ci_for_risk_difference": primary_ci,
            "bootstrap_resamples": bootstrap_resamples,
            "bootstrap_random_seed": 20261010,
        },
        "secondary_contrasts": {
            key: {
                "raw_exact_two_sided_mcnemar_p": secondary_raw[key],
                "holm_adjusted_p": secondary_adjusted[key],
            }
            for key in ("B_vs_A", "C_vs_A")
        },
        "interpretation": "This analysis uses final adjudicated labels and independent cases as the unit. It does not infer a desired direction; report null, adverse, and inconclusive outcomes as observed."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze final human adjudications for the preregistered v2 design.")
    parser.add_argument("--manifest", type=Path, default=Path("data/followup_v2/protocol_manifest.json"))
    parser.add_argument("--ratings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-resamples", type=int, default=10000)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    ratings_path = args.ratings if args.ratings.is_absolute() else root / args.ratings
    output_path = args.output if args.output.is_absolute() else root / args.output
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "frozen":
        raise SystemExit("Refusing to analyze: follow-up v2 protocol is not frozen.")
    if manifest.get("model_inference_permitted") is not True:
        raise SystemExit("Refusing to analyze: follow-up v2 manifest is not inference-authorized.")
    rows = [
        json.loads(line)
        for line in ratings_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    report = analyze_adjudicated_ratings(
        rows,
        list(manifest["case_pool"]["case_ids"]),
        tuple(manifest["generation"]["seeds"]),
        bootstrap_resamples=args.bootstrap_resamples,
    )
    report["source_manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    report["source_ratings_sha256"] = hashlib.sha256(ratings_path.read_bytes()).hexdigest()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "case_count": report.get("case_count"), "issue_count": report.get("issue_count", 0), "output": str(output_path)}, indent=2))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
