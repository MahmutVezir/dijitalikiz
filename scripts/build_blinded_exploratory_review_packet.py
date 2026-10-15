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


def build_packet(
    artifact_root: Path,
    artifact_sha256: str = EXPECTED_ARCHIVE_SHA256,
    reviewer_label: str = "A",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if reviewer_label not in {"A", "B"}:
        raise ValueError("reviewer_label must be A or B.")
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
        raise ValueError(
            f"Expected {expected_count} run records for 2 conditions × 5 seeds; found {len(run_files)}."
        )

    run_records = [_read_json(path) for path in run_files]
    observed_keys = set()
    allowed_conditions = {"standard", "ccdg"}
    allowed_seeds = {42, 43, 44, 45, 46}
    for record in run_records:
        source_key = (record.get("case_id"), record.get("condition"), record.get("seed"))
        if source_key in observed_keys:
            raise ValueError(f"Duplicate run identity in source artifact: {source_key}")
        observed_keys.add(source_key)
        if record.get("case_id") not in source_cases:
            raise ValueError(f"Run references unknown case: {source_key}")
        if record.get("condition") not in allowed_conditions or record.get("seed") not in allowed_seeds:
            raise ValueError(f"Unexpected condition or seed in frozen artifact: {source_key}")
        if record.get("parsed_output") is None:
            raise ValueError(f"Output cannot be reviewed as a parsed diagnosis: {source_key}")
    if len(observed_keys) != expected_count:
        raise ValueError("Source artifact is missing one or more case-condition-seed combinations.")

    # Keep anonymous case references stable across reviewers so their ratings can be
    # aligned after both reviews are locked. Randomize each reviewer's row order
    # using a separate deterministic seed.
    case_seed = int(
        hashlib.sha256(f"{artifact_sha256}:case-reference-map".encode("ascii")).hexdigest()[:16], 16
    )
    case_rng = random.Random(case_seed)
    shuffled_case_ids = list(case_ids)
    case_rng.shuffle(shuffled_case_ids)
    case_refs = {
        case_id: f"CASE-{index + 1:02d}"
        for index, case_id in enumerate(shuffled_case_ids)
    }
    order_seed = int(
        hashlib.sha256(f"{artifact_sha256}:reviewer-order:{reviewer_label}".encode("ascii")).hexdigest()[:16], 16
    )
    rng = random.Random(order_seed)

    rows: list[dict[str, Any]] = []
    key_by_hidden_key: dict[str, dict[str, Any]] = {}
    for record in run_records:
        case_id = record["case_id"]
        case = source_cases[case_id]
        output = record["parsed_output"]
        hidden_key = f"{case_id}|{record['condition']}|{record['seed']}"

        rows.append({
            "_hidden_key": hidden_key,
            "review_id": "",
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
        key_by_hidden_key[hidden_key] = {
            "reviewer_code": reviewer_label,
            "review_id": "",
            "case_ref": case_refs[case_id],
            "source_case_id": case_id,
            "condition": record["condition"],
            "seed": record["seed"],
            "source_commit": record.get("source_commit"),
            "prompt_sha256": record.get("prompt_sha256"),
            "context_sha256": record.get("context_sha256"),
        }

    rng.shuffle(rows)
    for index, row in enumerate(rows, start=1):
        row["review_id"] = f"REVIEW-{reviewer_label}-{index:03d}"
        hidden_key = row.pop("_hidden_key")
        key_by_hidden_key[hidden_key]["review_id"] = row["review_id"]

    key_rows = sorted(key_by_hidden_key.values(), key=lambda item: item["review_id"])
    if len(key_rows) != len(rows) or len({item["review_id"] for item in key_rows}) != len(rows):
        raise ValueError("Blinding key mapping failed integrity checks.")

    packet_metadata = {
        "record_type": "metadata",
        "packet_version": "1.1",
        "packet_kind": "post_hoc_exploratory_semantic_review",
        "reviewer_code": reviewer_label,
        "source_artifact_archive_sha256": artifact_sha256,
        "n_records": len(rows),
        "condition_labels_and_seeds_in_reviewer_rows": False,
        "original_case_ids_in_reviewer_rows": False,
        "frozen_primary_results_modified": False,
        "new_inference_performed": False,
        "review_status": "unreviewed_packet",
        "warning": (
            "This packet supports exploratory post-hoc review only. It cannot replace "
            "or amend the frozen confirmatory endpoint."
        ),
    }
    return [packet_metadata, *rows], key_rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a condition- and seed-masked exploratory review packet from the frozen artifact."
    )
    parser.add_argument("--artifact-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--key-output",
        required=True,
        type=Path,
        help="Keep this key separate; do not share it with reviewers.",
    )
    parser.add_argument("--artifact-sha256", default=EXPECTED_ARCHIVE_SHA256)
    parser.add_argument(
        "--reviewer-label",
        choices=("A", "B"),
        required=True,
        help="Build this reviewer's independently randomized packet and separate mapping key.",
    )
    args = parser.parse_args()

    packet, key_rows = build_packet(args.artifact_root, args.artifact_sha256, args.reviewer_label)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.key_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in packet) + "\n",
        encoding="utf-8",
    )
    args.key_output.write_text(
        json.dumps(
            {"warning": "KEEP PRIVATE FROM REVIEWERS", "records": key_rows},
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "packet_built",
        "reviewer_code": args.reviewer_label,
        "review_records": len(packet) - 1,
        "packet_path": str(args.output),
        "key_path": str(args.key_output),
        "reviewer_rows_include_condition_or_seed": False,
        "frozen_results_modified": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
