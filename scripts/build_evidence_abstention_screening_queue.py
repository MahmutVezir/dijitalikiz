#!/usr/bin/env python3
"""Build a deterministic, project-balanced BugsInPy validation queue.

This is metadata triage only. It does not run buggy/fixed tests, review code or
licenses, assign ground truth/evidence levels, clear prior exposure, or accept
cases for confirmatory analysis.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPOSURE_ADDENDUM = ROOT / "research_candidates" / "evidence_abstention" / "EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json"

# Any candidate used to test the validation workflow or inspect raw test results
# is kept out of the confirmatory queue to prevent researcher/pipeline-debug exposure.
EXCLUDED_CASES = {
    "BugsInPy-black-1",
    "BugsInPy-tqdm-1",
    "BugsInPy-httpie-1",
    "BugsInPy-youtube-dl-1",
    "BugsInPy-PySnooper-1",
    "BugsInPy-black-2",
    "BugsInPy-cookiecutter-1",
    "BugsInPy-fastapi-1",
    "BugsInPy-luigi-1",
    "BugsInPy-sanic-1",
    "BugsInPy-scrapy-1",
    "BugsInPy-thefuck-1",
    "BugsInPy-tornado-1",
}
REQUIRED_COLUMNS = {
    "case_id", "project", "bug_id", "source_repository", "python_version",
    "buggy_commit_id", "fixed_commit_id", "test_file", "run_test_command",
    "metadata_complete", "permanently_excluded_feasibility_case",
}
QUEUE_COLUMNS = [
    "queue_rank", "project_round", "screening_batch", "queue_status",
    "acceptance_status",
]
HEX_COMMIT = re.compile(r"^[0-9a-fA-F]{7,64}$")


def sort_bug_id(row):
    value = str(row.get("bug_id", "")).strip()
    return (0, int(value)) if value.isdigit() else (1, value.casefold())


def load_exposure_exclusions(path):
    path = Path(path)
    try:
        raw = path.read_bytes()
        document = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Exposure exclusion addendum is missing or invalid: " + str(exc)) from exc
    if not isinstance(document, dict):
        raise ValueError("Exposure exclusion addendum must contain a JSON object")

    case_ids = document.get("excluded_case_ids")
    if not isinstance(case_ids, list) or any(not isinstance(item, str) or not item.strip() for item in case_ids):
        raise ValueError("Exposure exclusion addendum must provide non-empty excluded_case_ids")
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("Exposure exclusion addendum contains duplicate excluded_case_ids")

    recorded_ids = set()
    records = document.get("additional_batch_records", [])
    if not isinstance(records, list):
        raise ValueError("Exposure addendum additional_batch_records must be a list")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Exposure addendum batch records must be objects")
        cases = record.get("cases", [])
        if not isinstance(cases, list):
            raise ValueError("Exposure addendum batch record cases must be a list")
        for case in cases:
            case_id = case if isinstance(case, str) else case.get("case_id") if isinstance(case, dict) else None
            if not isinstance(case_id, str) or not case_id.strip():
                raise ValueError("Exposure addendum contains a malformed case record")
            recorded_ids.add(case_id)
    missing_from_index = recorded_ids - set(case_ids)
    if missing_from_index:
        raise ValueError("Exposure addendum batch records missing from excluded_case_ids: " + ", ".join(sorted(missing_from_index)))

    return set(case_ids), hashlib.sha256(raw).hexdigest()


def build_queue(input_path, output_path, summary_path, first_batch_per_project=5, exposure_addendum_path=None):
    input_path = Path(input_path)
    output_path = Path(output_path)
    summary_path = Path(summary_path)
    exposure_path = Path(exposure_addendum_path) if exposure_addendum_path else DEFAULT_EXPOSURE_ADDENDUM
    dynamic_exclusions, exposure_sha256 = load_exposure_exclusions(exposure_path)
    excluded_cases = EXCLUDED_CASES | dynamic_exclusions
    with input_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        missing = sorted(REQUIRED_COLUMNS - set(fields))
        if missing:
            raise ValueError("Inventory is missing required columns: " + ", ".join(missing))
        rows = list(reader)

    exclusions = Counter()
    by_project = defaultdict(list)
    for row in rows:
        case_id = row.get("case_id", "").strip()
        if case_id in excluded_cases or row.get("permanently_excluded_feasibility_case", "").lower() == "true":
            exclusions["previously_exposed_permanent_exclusion"] += 1
            continue
        if row.get("metadata_complete", "").lower() != "true":
            exclusions["incomplete_metadata"] += 1
            continue
        buggy, fixed = row.get("buggy_commit_id", "").strip(), row.get("fixed_commit_id", "").strip()
        if not buggy or not fixed or buggy == fixed or not HEX_COMMIT.fullmatch(buggy) or not HEX_COMMIT.fullmatch(fixed):
            exclusions["invalid_or_identical_commit_ids"] += 1
            continue
        required_values = ("project", "source_repository", "python_version", "test_file", "run_test_command")
        if any(not row.get(name, "").strip() for name in required_values):
            exclusions["missing_minimum_queue_fields"] += 1
            continue
        by_project[row["project"].strip()].append(row)

    for project in by_project:
        by_project[project].sort(key=sort_bug_id)

    # Interleave projects by per-project ordinal to avoid using one project's
    # cases as the entire first screen. This is a screening order, not sampling
    # for inference, and it does not make any case eligible.
    queue = []
    project_round = 1
    while True:
        added = False
        for project in sorted(by_project, key=str.casefold):
            cases = by_project[project]
            if project_round <= len(cases):
                row = dict(cases[project_round - 1])
                row["queue_rank"] = len(queue) + 1
                row["project_round"] = project_round
                row["screening_batch"] = "B1" if project_round <= first_batch_per_project else "B2_PLUS"
                row["queue_status"] = "queued_for_manual_validation_only"
                row["acceptance_status"] = "NOT_ACCEPTED"
                # Keep these gates explicitly closed even if an input inventory
                # later changes its default values.
                row["test_pair_verified"] = "false"
                row["license_reviewed"] = "false"
                row["ground_truth_reviewed"] = "false"
                row["evidence_levels_reviewed"] = "false"
                row["leakage_reviewed"] = "false"
                row["prior_exposure_clear"] = "unknown"
                row["accepted_for_confirmatory"] = "false"
                queue.append(row)
                added = True
        if not added:
            break
        project_round += 1

    if not queue:
        raise ValueError("No metadata candidates passed the queue's minimum fields.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_fields = QUEUE_COLUMNS + [name for name in fields if name not in QUEUE_COLUMNS]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(queue)

    project_counts = Counter(row["project"] for row in queue)
    batch_counts = Counter(row["screening_batch"] for row in queue)
    summary = {
        "purpose": "Metadata-only, project-balanced manual validation queue; not an accepted dataset.",
        "input_rows": len(rows),
        "queue_rows": len(queue),
        "projects_in_queue": len(project_counts),
        "queue_rows_by_project": dict(sorted(project_counts.items())),
        "queue_rows_by_batch": dict(sorted(batch_counts.items())),
        "first_batch_per_project_ordinal": first_batch_per_project,
        "exposure_addendum_sha256": exposure_sha256,
        "documented_exposure_exclusion_count": len(dynamic_exclusions),
        "documented_exposure_exclusion_ids": sorted(dynamic_exclusions),
        "exclusions_by_reason": dict(sorted(exclusions.items())),
        "test_pairs_run_by_this_script": 0,
        "licenses_reviewed_by_this_script": 0,
        "ground_truth_or_evidence_levels_reviewed": 0,
        "prior_exposure_cleared": 0,
        "accepted_confirmatory_cases": 0,
        "llm_inference_performed": False,
        "notes": [
            "The queue order interleaves projects and sorts case IDs within each project.",
            "Queued cases must not be treated as eligible or confirmatory before all case-level gates pass.",
            "The first batch is a triage convenience only; it is not a statistical sample or a promise that 60 cases will pass.",
        ],
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="metadata inventory CSV")
    parser.add_argument("--output", type=Path, required=True, help="screening queue CSV")
    parser.add_argument("--summary", type=Path, required=True, help="JSON queue summary")
    parser.add_argument("--first-batch-per-project", type=int, default=5)
    parser.add_argument("--exposure-addendum", type=Path, default=DEFAULT_EXPOSURE_ADDENDUM)
    args = parser.parse_args(argv)
    if args.first_batch_per_project < 1:
        parser.error("--first-batch-per-project must be at least 1")
    summary = build_queue(args.input, args.output, args.summary, args.first_batch_per_project, args.exposure_addendum)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
