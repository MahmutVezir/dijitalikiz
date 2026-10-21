#!/usr/bin/env python3
"""Audit independent blinded rater agreement; never adjudicates or accepts cases."""
import argparse
import csv
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

COLUMNS = {"task_id", "panel", "rater_id", "rating_dimension", "rating_value", "rating_status"}
PANEL_BY_DIMENSION = {
    "root_cause_accuracy": "ground_truth",
    "decision": "evidence_support",
    "evidence_support": "evidence_support",
    "missing_evidence_quality": "evidence_support",
    "unsupported_definitive_diagnosis": "evidence_support",
}
BOOTSTRAP_REPLICATES = 2000
BOOTSTRAP_SEED = 20261021


def cohen_kappa(left, right):
    if not left or len(left) != len(right):
        raise ValueError("paired ratings must be non-empty and equal length")
    n = len(left)
    observed = sum(a == b for a, b in zip(left, right)) / n
    p_left, p_right = Counter(left), Counter(right)
    categories = set(p_left) | set(p_right)
    expected = sum((p_left[c] / n) * (p_right[c] / n) for c in categories)
    if abs(1.0 - expected) < 1e-12:
        return None, observed, expected, "expected agreement is 1; kappa is undefined"
    return (observed - expected) / (1.0 - expected), observed, expected, None


def percentile(values, probability):
    vals = sorted(values)
    if not vals:
        return None
    position = (len(vals) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(vals) - 1)
    fraction = position - lower
    return vals[lower] * (1.0 - fraction) + vals[upper] * fraction


def bootstrap_kappa_ci(left, right, replicates=BOOTSTRAP_REPLICATES, seed=BOOTSTRAP_SEED):
    if len(left) != len(right) or not left:
        raise ValueError("paired ratings must be non-empty and equal length")
    rng = random.Random(seed)
    n = len(left)
    estimates = []
    for _ in range(replicates):
        ids = [rng.randrange(n) for _ in range(n)]
        estimate, _, _, _ = cohen_kappa([left[i] for i in ids], [right[i] for i in ids])
        if estimate is not None:
            estimates.append(estimate)
    # Do not present a misleading interval if too many resamples are undefined.
    if len(estimates) < int(0.95 * replicates):
        return None, len(estimates)
    return [percentile(estimates, 0.025), percentile(estimates, 0.975)], len(estimates)


def load_and_validate(path):
    with Path(path).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = sorted(COLUMNS - set(reader.fieldnames or []))
        if missing:
            raise ValueError("rater agreement CSV missing columns: " + ", ".join(missing))
        rows = list(reader)
    if not rows:
        raise ValueError("rater agreement CSV is empty")
    return rows


def analyze_rows(rows, minimum_tasks=360, bootstrap_replicates=BOOTSTRAP_REPLICATES, seed=BOOTSTRAP_SEED):
    ratings = defaultdict(dict)
    reviewers_by_panel = defaultdict(set)
    tasks_by_dimension = defaultdict(set)
    for row in rows:
        task = row["task_id"].strip()
        panel = row["panel"].strip()
        reviewer = row["rater_id"].strip()
        dimension = row["rating_dimension"].strip()
        value = row["rating_value"].strip()
        status = row["rating_status"].strip()
        if not task or not reviewer or not value:
            raise ValueError("task_id, rater_id and rating_value must be non-empty")
        if dimension not in PANEL_BY_DIMENSION:
            raise ValueError("unknown rating_dimension: " + dimension)
        if panel not in {"ground_truth", "evidence_support"}:
            raise ValueError("unknown panel label: " + panel)
        if panel != PANEL_BY_DIMENSION[dimension]:
            raise ValueError(f"rating dimension {dimension} must be assigned to panel {PANEL_BY_DIMENSION[dimension]}")
        if status != "locked_independent":
            raise ValueError("agreement input must contain only locked independent ratings; adjudicated rows are not substitutes")
        if (task, dimension) in ratings and reviewer in ratings[(task, dimension)]:
            raise ValueError(f"duplicate rating for task={task}, dimension={dimension}, reviewer={reviewer}")
        ratings[(task, dimension)][reviewer] = value
        reviewers_by_panel[panel].add(reviewer)
        tasks_by_dimension[dimension].add(task)

    if reviewers_by_panel["ground_truth"] & reviewers_by_panel["evidence_support"]:
        raise ValueError("ground-truth and evidence-support reviewer panels must be disjoint")
    if len(reviewers_by_panel["ground_truth"]) != 2:
        raise ValueError("exactly two independent ground-truth raters are required for this agreement pass")
    if len(reviewers_by_panel["evidence_support"]) != 2:
        raise ValueError("exactly two independent evidence-support raters are required for this agreement pass")

    task_count_by_dimension = {dim: len(tasks) for dim, tasks in tasks_by_dimension.items()}
    if not tasks_by_dimension:
        raise ValueError("no rated tasks found")
    minimum_observed_tasks = min(task_count_by_dimension.values())
    if minimum_observed_tasks < minimum_tasks:
        raise ValueError(f"agreement report blocked: minimum dimension has {minimum_observed_tasks} tasks; requires {minimum_tasks}")

    results = {}
    expected_reviewers = {}
    for dimension, tasks in sorted(tasks_by_dimension.items()):
        task_ids = sorted(tasks)
        paired = []
        reviewer_pair = None
        for task in task_ids:
            pair = ratings[(task, dimension)]
            if len(pair) != 2:
                raise ValueError(f"task {task} dimension {dimension} must have exactly two independent ratings")
            reviewers = tuple(sorted(pair))
            if reviewer_pair is None:
                reviewer_pair = reviewers
            elif reviewers != reviewer_pair:
                raise ValueError(f"reviewer pair changes within dimension {dimension}; use a predeclared panel for all tasks")
            paired.append((pair[reviewers[0]], pair[reviewers[1]]))
        left = [x[0] for x in paired]
        right = [x[1] for x in paired]
        kappa, agreement, expected, reason = cohen_kappa(left, right)
        ci, estimable = bootstrap_kappa_ci(left, right, bootstrap_replicates, seed)
        results[dimension] = {
            "n_tasks": len(task_ids),
            "panel": PANEL_BY_DIMENSION[dimension],
            "reviewer_ids": list(reviewer_pair),
            "raw_agreement": agreement,
            "expected_agreement": expected,
            "cohen_kappa": kappa,
            "cohen_kappa_bootstrap_95_ci": ci,
            "bootstrap_replicates_requested": bootstrap_replicates,
            "bootstrap_replicates_estimable": estimable,
            "kappa_undefined_reason": reason,
            "category_counts_rater_1": dict(sorted(Counter(left).items())),
            "category_counts_rater_2": dict(sorted(Counter(right).items())),
        }
        expected_reviewers[dimension] = list(reviewer_pair)

    return {
        "analysis_type": "locked_independent_blinded_rater_agreement",
        "status": "agreement_only_not_adjudicated",
        "n_rating_rows": len(rows),
        "n_dimensions": len(results),
        "n_tasks_by_dimension": task_count_by_dimension,
        "reviewers_by_panel": {k: sorted(v) for k, v in reviewers_by_panel.items()},
        "panel_overlap": False,
        "minimum_tasks_required": minimum_tasks,
        "bootstrap_seed": seed,
        "dimensions": results,
        "limitations": [
            "Cohen kappa is sensitive to category prevalence; raw agreement and category counts are shown alongside it.",
            "Bootstrap intervals resample task IDs and describe this reviewed task set; they do not cure non-representative sampling.",
            "Agreement is not correctness. Human adjudication, gold-ground-truth validation and case acceptance are separate gates.",
            "This tool does not reveal policy labels, adjudicate disagreements, accept cases, or run a model.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ratings", type=Path, required=True, help="Locked independent panel scores; no policy/gold fields")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-tasks", type=int, default=360, help="360 corresponds to 60 cases x 6 cells")
    parser.add_argument("--bootstrap-replicates", type=int, default=BOOTSTRAP_REPLICATES)
    parser.add_argument("--seed", type=int, default=BOOTSTRAP_SEED)
    args = parser.parse_args(argv)
    try:
        if args.minimum_tasks < 1 or args.bootstrap_replicates < 100:
            raise ValueError("minimum-tasks must be >=1 and bootstrap-replicates must be >=100")
        result = analyze_rows(load_and_validate(args.ratings), args.minimum_tasks, args.bootstrap_replicates, args.seed)
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        parser.exit(2, "BLOCKED: " + str(exc) + "\n")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
