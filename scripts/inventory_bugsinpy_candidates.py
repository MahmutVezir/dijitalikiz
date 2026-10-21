#!/usr/bin/env python3
"""Build a metadata-only inventory of BugsInPy cases. Never runs tests or an LLM."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

DATASET_COMMIT = "11c5f1eea954a42132cfd06bf257766a7963e0fd"
EXCLUDED_CASES = {
    "BugsInPy-black-1",
    "BugsInPy-tqdm-1",
    "BugsInPy-httpie-1",
    "BugsInPy-youtube-dl-1",
    "BugsInPy-PySnooper-1",
}
FIELDS = [
    "source_dataset", "dataset_revision", "project", "bug_id", "case_id",
    "source_repository", "project_info_sha256", "bug_info_sha256",
    "patch_sha256", "run_test_sha256", "setup_sha256",
    "python_version", "pythonpath", "buggy_commit_id", "fixed_commit_id",
    "test_file", "run_test_command", "metadata_complete",
    "permanently_excluded_feasibility_case", "test_pair_verified",
    "license_reviewed", "ground_truth_reviewed", "evidence_levels_reviewed",
    "leakage_reviewed", "prior_exposure_clear", "accepted_for_confirmatory",
    "screening_status",
]


def sha256_file(path):
    if not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_key_values(path):
    values = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"^\s*([A-Za-z0-9_]+)\s*=\s*(.*?)\s*$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value.strip()
    return values


def inventory_rows(root, revision=DATASET_COMMIT):
    projects_root = root / "projects"
    if not projects_root.is_dir():
        raise ValueError("Expected BugsInPy checkout with a projects/ directory")
    rows = []
    metadata_files = sorted(projects_root.glob("*/bugs/*/bug.info"))
    for bug_info in metadata_files:
        bug_dir = bug_info.parent
        project_dir = bug_dir.parent.parent
        project = project_dir.name
        bug_id = bug_dir.name
        case_id = f"BugsInPy-{project}-{bug_id}"
        info = parse_key_values(bug_info)
        project_info = project_dir / "project.info"
        project_meta = parse_key_values(project_info)
        patch = bug_dir / "bug_patch.txt"
        run_test = bug_dir / "run_test.sh"
        setup = bug_dir / "setup.sh"
        run_test_command = " ; ".join(
            line.strip() for line in run_test.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip()
        ) if run_test.is_file() else ""
        required_present = all(info.get(key) for key in (
            "python_version", "buggy_commit_id", "fixed_commit_id", "test_file"
        )) and bool(run_test_command)
        commits_differ = (
            bool(info.get("buggy_commit_id")) and bool(info.get("fixed_commit_id"))
            and info.get("buggy_commit_id") != info.get("fixed_commit_id")
        )
        complete = required_present and commits_differ
        excluded = case_id in EXCLUDED_CASES
        rows.append({
            "source_dataset": "BugsInPy",
            "dataset_revision": revision,
            "project": project,
            "bug_id": bug_id,
            "case_id": case_id,
            "source_repository": project_meta.get("github_url", ""),
            "project_info_sha256": sha256_file(project_info),
            "bug_info_sha256": sha256_file(bug_info),
            "patch_sha256": sha256_file(patch),
            "run_test_sha256": sha256_file(run_test),
            "setup_sha256": sha256_file(setup),
            "python_version": info.get("python_version", ""),
            "pythonpath": info.get("pythonpath", ""),
            "buggy_commit_id": info.get("buggy_commit_id", ""),
            "fixed_commit_id": info.get("fixed_commit_id", ""),
            "test_file": info.get("test_file", ""),
            "run_test_command": run_test_command,
            "metadata_complete": str(bool(complete)).lower(),
            "permanently_excluded_feasibility_case": str(excluded).lower(),
            "test_pair_verified": "false",
            "license_reviewed": "false",
            "ground_truth_reviewed": "false",
            "evidence_levels_reviewed": "false",
            "leakage_reviewed": "false",
            "prior_exposure_clear": "false" if excluded else "unknown",
            "accepted_for_confirmatory": "false",
            "screening_status": "excluded_prior_exposure" if excluded else (
                "metadata_incomplete" if not complete else "unreviewed_metadata_only"
            ),
        })
    rows.sort(key=lambda row: (row["project"].casefold(), int(row["bug_id"]) if row["bug_id"].isdigit() else 10**9, row["bug_id"]))
    return rows


def verify_commit(root, expected):
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    )
    actual = result.stdout.strip()
    if actual.lower() != expected.lower():
        raise ValueError(f"Dataset commit mismatch: expected {expected}, got {actual}")
    return actual


def write_inventory(rows, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(rows, revision):
    counts = Counter(row["project"] for row in rows)
    return {
        "source_dataset": "BugsInPy",
        "dataset_revision": revision,
        "raw_metadata_cases_in_inventory": len(rows),
        "projects_in_inventory": len(counts),
        "raw_cases_by_project": dict(sorted(counts.items())),
        "metadata_complete_count": sum(row["metadata_complete"] == "true" for row in rows),
        "prior_exposure_excluded_count": sum(row["permanently_excluded_feasibility_case"] == "true" for row in rows),
        "accepted_confirmatory_cases": 0,
        "test_pairs_verified_by_this_script": 0,
        "licenses_reviewed_by_this_script": 0,
        "llm_inference_performed": False,
        "purpose": "Metadata-only inventory; it does not run tests, read ground-truth labels, adjudicate causes, review licenses, or authorize inference.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Local BugsInPy repository checkout")
    parser.add_argument("--output", type=Path, required=True, help="Destination CSV path")
    parser.add_argument("--summary", type=Path, required=True, help="Destination JSON summary path")
    parser.add_argument("--expected-commit", default=DATASET_COMMIT)
    parser.add_argument("--expected-count", type=int, default=None)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        revision = verify_commit(root, args.expected_commit)
        rows = inventory_rows(root, revision)
        if args.expected_count is not None and len(rows) != args.expected_count:
            raise ValueError(f"Inventory count mismatch: expected {args.expected_count}, got {len(rows)}")
        write_inventory(rows, args.output)
        summary = build_summary(rows, revision)
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
