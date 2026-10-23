#!/usr/bin/env python3
"""Verify that V10 metadata intake can be reproduced exactly; runs no bug tests or model."""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(str(path) + " must contain a JSON object")
    return value


def read_csv(path):
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(str(path) + " has no CSV header")
        return list(reader)


def _require(condition, message, blockers):
    if not condition:
        blockers.append(message)


def verify_v10_intake(
    inventory_path,
    queue_path,
    generated_intake_path,
    frozen_intake_path,
    exposure_union_path,
    expected_inventory_rows=501,
    expected_queue_rows=407,
    expected_cohort_size=100,
    expected_project_count=14,
    expected_exclusion_count=93,
):
    blockers = []
    inventory_path = Path(inventory_path)
    queue_path = Path(queue_path)
    generated_intake_path = Path(generated_intake_path)
    frozen_intake_path = Path(frozen_intake_path)
    exposure_union_path = Path(exposure_union_path)

    try:
        inventory = read_csv(inventory_path)
        queue = read_csv(queue_path)
        generated = read_json(generated_intake_path)
        frozen = read_json(frozen_intake_path)
        exposure = read_json(exposure_union_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return {
            "status": "blocked",
            "ready": False,
            "blockers": ["Unable to load an input artifact: " + str(exc)],
            "bug_fix_tests_run_by_gate": 0,
            "model_inference_performed": False,
            "accepted_confirmatory_cases": 0,
        }

    inventory_ids = [row.get("case_id", "") for row in inventory]
    queue_ids = [row.get("case_id", "") for row in queue]
    if any(not isinstance(cid, str) or not cid.strip() for cid in inventory_ids + queue_ids):
        blockers.append("Inventory/queue contains an empty case ID.")
    if len(inventory_ids) != len(set(inventory_ids)):
        blockers.append("Inventory contains duplicate case IDs.")
    if len(queue_ids) != len(set(queue_ids)):
        blockers.append("Queue contains duplicate case IDs.")

    inventory_set = set(inventory_ids)
    queue_set = set(queue_ids)
    _require(queue_set.issubset(inventory_set), "Queue contains case IDs absent from the inventory.", blockers)
    _require(len(inventory) == expected_inventory_rows,
             f"Inventory row count is {len(inventory)}; expected {expected_inventory_rows}.", blockers)
    _require(len(queue) == expected_queue_rows,
             f"Queue row count is {len(queue)}; expected {expected_queue_rows}.", blockers)

    exclusion_ids = exposure.get("excluded_case_ids")
    if not isinstance(exclusion_ids, list) or any(not isinstance(cid, str) or not cid.strip() for cid in exclusion_ids):
        blockers.append("Exposure union does not contain a valid excluded_case_ids list.")
        exclusion_ids = []
    if len(exclusion_ids) != len(set(exclusion_ids)):
        blockers.append("Exposure union contains duplicate IDs.")
    recorded_exclusion_count = exposure.get("unique_exclusion_count")
    _require(recorded_exclusion_count == len(exclusion_ids),
             "Exposure union unique_exclusion_count disagrees with the ID list.", blockers)
    _require(len(exclusion_ids) == expected_exclusion_count,
             f"Exposure union has {len(exclusion_ids)} IDs; expected {expected_exclusion_count}.", blockers)
    exclusion_set = set(exclusion_ids)
    if queue_set & exclusion_set:
        blockers.append("Queue reintroduces previously exposed IDs: " + repr(sorted(queue_set & exclusion_set)))
    inventory_exclusion_set = inventory_set & exclusion_set

    selected_ids = generated.get("case_ids")
    frozen_ids = frozen.get("case_ids")
    if not isinstance(selected_ids, list) or any(not isinstance(cid, str) for cid in selected_ids):
        blockers.append("Generated intake case_ids is malformed.")
        selected_ids = []
    if not isinstance(frozen_ids, list) or any(not isinstance(cid, str) for cid in frozen_ids):
        blockers.append("Frozen V10 case_ids is malformed.")
        frozen_ids = []
    if len(selected_ids) != len(set(selected_ids)):
        blockers.append("Generated intake has duplicate selected IDs.")
    _require(len(selected_ids) == expected_cohort_size,
             f"Generated intake contains {len(selected_ids)} candidates; expected {expected_cohort_size}.", blockers)
    _require(selected_ids == frozen_ids, "Generated intake order differs from frozen V10 case order.", blockers)
    _require(selected_ids == queue_ids[:expected_cohort_size],
             "Frozen intake is not the exact prefix of the rebuilt eligible queue.", blockers)
    _require(set(selected_ids).issubset(queue_set),
             "Generated intake contains an ID outside the rebuilt queue.", blockers)
    _require(not (set(selected_ids) & exclusion_set),
             "Generated intake intersects the permanent-exposure set.", blockers)

    selected_rows = [row for row in queue if row.get("case_id") in set(selected_ids)]
    if len(selected_rows) != len(selected_ids):
        blockers.append("One or more selected case IDs cannot be resolved to exactly one queue row.")
    for row in selected_rows:
        cid = row.get("case_id", "<unknown>")
        if row.get("metadata_complete", "").lower() != "true":
            blockers.append(cid + ": metadata_complete is not true.")
        if row.get("accepted_for_confirmatory", "").lower() == "true":
            blockers.append(cid + ": a metadata-only row is incorrectly pre-accepted.")
        if row.get("acceptance_status") and row.get("acceptance_status") != "NOT_ACCEPTED":
            blockers.append(cid + ": acceptance_status must remain NOT_ACCEPTED.")

    actual_project_counts = dict(sorted(Counter(row.get("project", "") for row in selected_rows).items()))
    _require(len(actual_project_counts) == expected_project_count,
             f"Selected intake has {len(actual_project_counts)} projects; expected {expected_project_count}.", blockers)
    _require(actual_project_counts == generated.get("counts_by_project"),
             "Generated intake project counts do not match selected queue rows.", blockers)
    _require(actual_project_counts == frozen.get("counts_by_project"),
             "Frozen V10 project counts do not match selected queue rows.", blockers)

    actual_inventory_sha = sha256_file(inventory_path)
    actual_queue_sha = sha256_file(queue_path)
    _require(actual_inventory_sha == frozen.get("source_inventory_sha256"),
             "Inventory SHA-256 differs from the frozen V10 manifest.", blockers)
    _require(actual_queue_sha == frozen.get("source_queue_sha256"),
             "Queue SHA-256 differs from the frozen V10 manifest.", blockers)
    _require(actual_inventory_sha == generated.get("source_inventory_sha256"),
             "Generated intake inventory SHA-256 does not match the input file.", blockers)
    _require(actual_queue_sha == generated.get("source_queue_sha256"),
             "Generated intake queue SHA-256 does not match the input file.", blockers)

    generated_exclusions = generated.get("excluded_prior_exposure")
    frozen_exclusions = frozen.get("excluded_prior_exposure")
    if not isinstance(generated_exclusions, list) or not isinstance(frozen_exclusions, list):
        blockers.append("Generated or frozen exclusion list is missing.")
        generated_exclusions, frozen_exclusions = [], []
    _require(set(generated_exclusions) == set(frozen_exclusions),
             "Generated intake exposure exclusions differ from the frozen manifest.", blockers)
    _require(set(generated_exclusions) == inventory_exclusion_set,
             "Exclusion list does not match the exposure-union IDs present in the inventory.", blockers)
    _require(generated.get("accepted_confirmatory_cases") == 0,
             "Metadata intake must report zero accepted confirmatory cases.", blockers)
    _require(generated.get("llm_inference_performed") is False,
             "Metadata intake must report that no LLM inference was performed.", blockers)
    _require(frozen.get("accepted_confirmatory_cases") == 0,
             "Frozen V10 manifest must report zero accepted confirmatory cases.", blockers)
    _require(frozen.get("llm_inference_performed") is False,
             "Frozen V10 manifest must report that no LLM inference was performed.", blockers)

    return {
        "status": "passed" if not blockers else "blocked",
        "ready": not blockers,
        "mode": "metadata_reproducibility_only_no_bug_tests_no_model_inference",
        "inventory_rows": len(inventory),
        "inventory_projects": len({row.get("project", "") for row in inventory}),
        "queue_rows": len(queue),
        "queue_projects": len({row.get("project", "") for row in queue}),
        "selected_candidates": len(selected_ids),
        "selected_projects": len(actual_project_counts),
        "exposure_union_ids": len(exclusion_ids),
        "selected_exposure_intersection": len(set(selected_ids) & exclusion_set),
        "inventory_sha256": actual_inventory_sha,
        "queue_sha256": actual_queue_sha,
        "bug_fix_tests_run_by_gate": 0,
        "accepted_confirmatory_cases": 0,
        "model_inference_performed": False,
        "blocker_count": len(blockers),
        "blockers": blockers,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--generated-intake", type=Path, required=True)
    parser.add_argument("--frozen-intake", type=Path, required=True)
    parser.add_argument("--exposure-union", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)

    report = verify_v10_intake(
        args.inventory,
        args.queue,
        args.generated_intake,
        args.frozen_intake,
        args.exposure_union,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready"] else 2


if __name__ == "__main__":
    sys.exit(main())
