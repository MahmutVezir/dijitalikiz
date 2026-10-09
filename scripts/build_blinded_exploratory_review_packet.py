from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any

EXPECTED_ARCHIVE_SHA256 = "e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_packet(artifact_root: Path, artifact_sha256: str = EXPECTED_ARCHIVE_SHA256) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_root = artifact_root.resolve()
    manifest_path = artifact_root / "benchmark_manifest.json"
    case_dir = artifact_root / "cases"
    runs_dir = artifact_root / "runs"
    if not manifest_path.exists() or not case_dir.is_dir() or not runs_dir.is_dir():
        raise FileNotFoundError(
            "artifact_root must contain benchmark_manifest.json and cases/ and runs/ directories"
        )

    manifest = _read_json(manifest_path)
    case_ids = list(manifest.get("case_ids", []))
    if len(case_ids) != len(set(case_ids)) or not case_ids:
        raise ValueError("Benchmark manifest case_ids must be non-empty and unique.")

    source_cases = {case_id: _read_json(case_dir / f"{case_id}.json") for case_id in case_ids}
    run_files = sorted(runs_dir.glob("*.json"))
    expected_count = len(case_ids) * 2 * 5
    if len(run_files) != expected_count:
        raise ValueError(f"Expected {expected_count} run records for 2 conditions × 5 seeds; found {len(run_files)}.")

    run_records = [_read_json(path) for path in run_files]
    observed_keys = set()
    allowed_conditions = {"standard", "ccdg"}
    allowed_seeds = {42, 43, 44, 45, 46}
    for record in run_records:
        key = (record.get("case_id"), record.get("condition"), record.get("seed"))
        if key in observed_keys:
            raise ValueError(f"Duplicate run identity in source artifact: {key}")
        observed_keys.add(key)
        if record.get("case_id") not in source_cases:
            raise ValueError(f"Run references unknown case: {key}")
        if record.get("condition") not in allowed_conditions or record.get("seed") not in allowed_seeds:
            raise ValueError(f"Unexpected condition or seed in frozen artifact: {key}")
        if record.get("parsed_output") is None:
            raise ValueError(f"Output cannot be reviewed as a parsed diagnosis: {key}")
    if len(observed_keys) != expected_count:
        raise ValueError("Source artifact is missing one or more case-condition-seed combinations.")

    # This seeded permutation is reproducible from the archive digest while removing
    # case IDs, condition names, and seeds from the reviewer-facing rows.
    seed_int = int(hashlib.sha256(artifact_sha256.encode("ascii")).hexdigest()[:16], 16)
    rng = random.Random(seed_int)
    shuffled_case_ids = list(case_ids)
    rng.shuffle(shuffled_case_ids)
    case_refs = {case_id: f"CASE-{index + 1:02d}" for index, case_id in enumerate(shuffled_case_ids)}

    rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    for record in run_records:
        case_id = record["case_id"]
        case = source_cases[case_id]
        output = record["parsed_output"]
        review_id = ""  # assigned after a deterministic shuffle
        rows.append({
            "review_id": review_id,
            "case_ref": case_refs[case_id],
            "source_evidence": {
                "source": case.get("source", ""),
                "source_url": case.get("source_url", ""),
                "publication_date": case.get("publication_date", ""),
                "technology": case.get("technology", ""),
                "error_description": case.get("error_description", ""),
                "i_base": case.get("i_base", []),
            },
            "reference": {
                "component": case["ground_truth"].get("component", ""),
                "entity": case["ground_truth"].get("entity", ""),
                "operation": case["ground_truth"].get("operation", ""),
                "root_cause": case["ground_truth"].get("root_cause", ""),
                "required_relations": case["ground_truth"].get("required_relations", []),
            },
            "response": {
                "diagnosed_component": output.get("diagnosed_component", ""),
                "root_cause_class": output.get("root_cause_class", ""),
                "affected_entity": output.get("affected_entity", ""),
                "explanation": output.get("explanation", ""),
                "raw_output": record.get("raw_output", ""),
            },
            "review": {
                "root_cause_correctness": "",
                "component_localization": "",
                "evidence_consistency": "",
                "dependency_reasoning": "",
                "overall_diagnostic_status": "",
                "reviewer_notes": "",
            },
        })
        key_rows.append({
            "review_id": review_id,
            "case_ref": case_refs[case_id],
            "source_case_id": case_id,
            "condition": record["condition"],
            "seed": record["seed"],
            "source_commit": record.get("source_commit"),
            "prompt_sha256": record.get("prompt_sha256"),
            "context_sha256": record.get("context_sha256"),
        })

    rng.shuffle(rows)
    key_by_signature = {
        (item["case_ref"], item["response"]["raw_output"]): item
        for item in rows
    }
    # The exact raw response is unique within this frozen artifact; detect otherwise.
    if len(key_by_signature) != len(rows):
        raise ValueError("Non-unique case/response pair prevents deterministic review-key mapping.")
    # Map the shuffled packet back to frozen metadata without writing conditions to packet rows.
    metadata_by_pair = {}
    for record in run_records:
        case_id = record["case_id"]
        pair = (case_refs[case_id], record.get("raw_output", ""))
        metadata_by_pair[pair] = {
            "case_ref": case_refs[case_id],
            "source_case_id": case_id,
            "condition": record["condition"],
            "seed": record["seed"],
            "source_commit": record.get("source_commit"),
            "prompt_sha256": record.get("prompt_sha256"),
            "context_sha256": record.get("context_sha256"),
        }

    for index, row in enumerate(rows, start=1):
        row["review_id"] = f"REVIEW-{index:03d}"
        row.pop("condition", None)
        row.pop("seed", None)
        metadata_by_pair[(row["case_ref"], row["response"]["raw_output"])]["review_id"] = row["review_id"]
    key_rows = sorted(metadata_by_pair.values(), key=lambda item: item["review_id"])

    packet_metadata = {
        "record_type": "metadata",
        "packet_version": "1.0",
        "packet_kind": "post_hoc_exploratory_semantic_review",
        "source_artifact_archive_sha256": artifact_sha256,
        "n_records": len(rows),
        "condition_labels_and_seeds_in_reviewer_rows": False,
        "original_case_ids_in_reviewer_rows": False,
        "frozen_primary_results_modified": False,
        "new_inference_performed": False,
        "review_status": "unreviewed_packet",
        "warning": "This packet supports exploratory post-hoc review only. It cannot replace or amend the frozen confirmatory endpoint."
    }
    return [packet_metadata, *rows], key_rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a condition- and seed-masked exploratory review packet from the frozen artifact.")
    parser.add_argument("--artifact-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--key-output", required=True, type=Path, help="Keep this key separate; do not share it with reviewers.")
    parser.add_argument("--artifact-sha256", default=EXPECTED_ARCHIVE_SHA256)
    args = parser.parse_args()

    packet, key_rows = build_packet(args.artifact_root, args.artifact_sha256)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.key_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in packet) + "\n",
        encoding="utf-8",
    )
    args.key_output.write_text(
        json.dumps({"warning": "KEEP PRIVATE FROM REVIEWERS", "records": key_rows}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "packet_built",
        "review_records": len(packet) - 1,
        "packet_path": str(args.output),
        "key_path": str(args.key_output),
        "reviewer_rows_include_condition_or_seed": False,
        "frozen_results_modified": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
