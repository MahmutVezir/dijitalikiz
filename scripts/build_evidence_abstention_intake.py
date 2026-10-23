#!/usr/bin/env python3
"""Create a deterministic metadata-only intake from an exposure-filtered BugsInPy queue."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from build_evidence_abstention_screening_queue import EXCLUDED_CASES, load_exposure_exclusions


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path, required):
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        missing = sorted(set(required) - set(fields))
        if missing:
            raise ValueError("CSV is missing required fields: " + ", ".join(missing))
        return list(reader)


def build_intake(inventory_path, queue_path, output_path, cohort_size=100, exposure_addendum_path=None, minimum_projects=8):
    inventory_path = Path(inventory_path)
    queue_path = Path(queue_path)
    output_path = Path(output_path)
    if cohort_size < 1:
        raise ValueError("cohort_size must be positive")
    if minimum_projects < 1:
        raise ValueError("minimum_projects must be positive")

    inventory = read_csv(
        inventory_path,
        {"case_id", "project", "permanently_excluded_feasibility_case"},
    )
    queue = read_csv(
        queue_path,
        {"case_id", "project", "metadata_complete", "accepted_for_confirmatory"},
    )

    inventory_ids = [row["case_id"] for row in inventory]
    queue_ids = [row["case_id"] for row in queue]
    if any(not isinstance(item, str) or not item.strip() for item in inventory_ids + queue_ids):
        raise ValueError("Inventory and queue case IDs must be non-empty strings")
    if len(inventory_ids) != len(set(inventory_ids)):
        raise ValueError("Inventory contains duplicate case IDs")
    if len(queue_ids) != len(set(queue_ids)):
        raise ValueError("Queue contains duplicate case IDs")
    inventory_id_set = set(inventory_ids)
    queue_id_set = set(queue_ids)
    if not queue_id_set.issubset(inventory_id_set):
        raise ValueError("Queue contains IDs absent from the source inventory")

    if cohort_size > len(queue):
        raise ValueError("Requested intake size exceeds the eligible screening queue")
    selected = queue[:cohort_size]
    selected_ids = [row["case_id"] for row in selected]
    if any(row.get("metadata_complete", "").lower() != "true" for row in selected):
        raise ValueError("Intake prefix contains metadata-incomplete candidate rows")
    if any(row.get("accepted_for_confirmatory", "").lower() == "true" for row in selected):
        raise ValueError("Metadata-only intake must not pre-accept cases")

    exposure_path = (
        Path(exposure_addendum_path)
        if exposure_addendum_path is not None
        else Path(__file__).resolve().parents[1]
        / "research_candidates"
        / "evidence_abstention"
        / "EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json"
    )
    dynamic_exclusions, exposure_sha = load_exposure_exclusions(exposure_path)
    permanently_excluded = {
        row["case_id"]
        for row in inventory
        if row.get("permanently_excluded_feasibility_case", "").lower() == "true"
    }
    documented_exclusions = (EXCLUDED_CASES | dynamic_exclusions | permanently_excluded) & inventory_id_set
    if documented_exclusions & queue_id_set:
        raise ValueError("Exposure-filtered queue contains documented prior-exposure IDs")
    if documented_exclusions & set(selected_ids):
        raise ValueError("Selected intake reintroduces a documented prior-exposure case")

    counts = Counter(row["project"] for row in selected)
    if any(not project for project in counts):
        raise ValueError("Selected queue rows must identify their upstream project")
    if len(counts) < minimum_projects:
        raise ValueError(
            "Intake contains only "
            + str(len(counts))
            + " upstream projects; required minimum is "
            + str(minimum_projects)
        )

    output = {
        "record_type": "metadata_only_screening_intake_not_confirmatory_dataset",
        "created_on": "2026-10-23",
        "selection_rule": (
            "First N rows of the deterministic, interleaved queue rebuilt from the pinned BugsInPy inventory "
            "after applying the recorded permanent-exposure and metadata validity exclusions."
        ),
        "cohort_size": len(selected_ids),
        "upstream_project_count": len(counts),
        "counts_by_project": dict(sorted(counts.items())),
        "source_inventory_sha256": sha256_file(inventory_path),
        "source_queue_sha256": sha256_file(queue_path),
        "exposure_addendum_sha256": exposure_sha,
        "accepted_confirmatory_cases": 0,
        "llm_inference_performed": False,
        "excluded_prior_exposure": sorted(documented_exclusions),
        "case_ids": selected_ids,
        "notes": [
            "This file freezes a metadata-only screening order, not an accepted or labeled experiment dataset.",
            "No buggy/fixed test pair has been run by this builder.",
            "No license, root-cause, evidence sufficiency, leakage or independent-review gate is passed by this builder.",
            "Candidates used to debug the validation pipeline remain excluded irrespective of their technical outcome.",
            "Every subsequent eight-case screen must record raw artifacts; an automated technical signal never auto-accepts a case.",
            "No model inference is performed or authorized by this file.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--minimum-projects", type=int, default=8)
    parser.add_argument("--exposure-addendum", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        result = build_intake(
            args.inventory,
            args.queue,
            args.output,
            args.size,
            args.exposure_addendum,
            args.minimum_projects,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, "ERROR: " + str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
