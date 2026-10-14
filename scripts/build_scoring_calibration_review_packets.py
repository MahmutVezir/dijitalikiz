from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES = ROOT / "data" / "calibration" / "examples.jsonl"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Calibration examples file not found: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{line_number}: each JSONL row must be an object")
        rows.append(row)
    if not rows:
        raise ValueError(f"No calibration examples found in {path}")
    return rows


def build_packets(
    examples: list[dict[str, Any]],
    *,
    reviewer_a_seed: int = 1701,
    reviewer_b_seed: int = 2903,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    seen_ids: set[str] = set()
    packet_by_example: dict[str, dict[str, Any]] = {}
    key_rows: list[dict[str, Any]] = []

    for row in examples:
        example_id = row.get("example_id")
        if not isinstance(example_id, str) or not example_id.strip():
            raise ValueError("Every example requires a non-empty example_id.")
        if example_id in seen_ids:
            raise ValueError(f"Duplicate example_id: {example_id}")
        seen_ids.add(example_id)

        required = (
            "case_summary",
            "source_url",
            "evidence_urls",
            "ground_truth_root_cause",
            "ground_truth_rationale",
            "response_text",
            "matcher_text",
            "root_cause_aliases",
            "response_origin",
            "generation_metadata",
            "challenge_class",
            "legacy_matcher_accepts",
            "source_case_id",
            "is_from_frozen_study_output",
        )
        missing = [field for field in required if field not in row]
        if missing:
            raise ValueError(f"{example_id}: missing fields: {', '.join(missing)}")
        if row["is_from_frozen_study_output"] is not False:
            raise ValueError(f"{example_id}: calibration examples cannot come from frozen study outputs.")
        if not isinstance(row["response_text"], str) or not row["response_text"].strip():
            raise ValueError(f"{example_id}: response_text must be non-empty.")
        if not isinstance(row["matcher_text"], str) or not row["matcher_text"].strip():
            raise ValueError(f"{example_id}: matcher_text must be the exact historical matcher surface")
        if not isinstance(row["evidence_urls"], list) or not row["evidence_urls"]:
            raise ValueError(f"{example_id}: at least one source evidence URL is required.")
        aliases = row["root_cause_aliases"]
        if not isinstance(aliases, list) or not aliases or not all(
            isinstance(alias, str) and alias.strip() for alias in aliases
        ):
            raise ValueError(f"{example_id}: root_cause_aliases must be a non-empty string list")
        if len(set(alias.strip().lower() for alias in aliases)) != len(aliases):
            raise ValueError(f"{example_id}: root_cause_aliases must not contain duplicates")
        origin = row["response_origin"]
        if origin not in {"independent_model_output", "human_authored_control", "synthetic_adversarial_control"}:
            raise ValueError(f"{example_id}: unsupported response_origin: {origin!r}")
        metadata = row["generation_metadata"]
        if origin == "independent_model_output":
            required_metadata = {"model_id", "model_revision", "seed", "prompt_sha256", "raw_output_sha256"}
            if not isinstance(metadata, dict) or not required_metadata.issubset(metadata):
                raise ValueError(f"{example_id}: independent model outputs require complete generation_metadata")
        elif metadata is not None:
            raise ValueError(f"{example_id}: human-authored/synthetic controls must set generation_metadata to null")

        # The reviewer receives source evidence and the response, but not the
        # case identifier, gold label, challenge class, or matcher decision.
        review_id = "REV-" + hashlib.sha256(f"scoring-calibration-v1:{example_id}".encode("utf-8")).hexdigest()[:12]
        packet_by_example[example_id] = {
            "review_id": review_id,
            "case_summary": row["case_summary"],
            "source_url": row["source_url"],
            "evidence_urls": row["evidence_urls"],
            "response_text": row["response_text"],
            "instruction": (
                "Independently classify the root-cause diagnosis using the cited case evidence. "
                "Do not infer correctness from the presence of a familiar phrase. Explain the "
                "causal mechanism and cite evidence in your review."
            ),
        }
        key_rows.append({
            "review_id": review_id,
            "example_id": example_id,
            "source_case_id": row["source_case_id"],
            "response_origin": row["response_origin"],
            "ground_truth_root_cause": row["ground_truth_root_cause"],
            "ground_truth_rationale": row["ground_truth_rationale"],
            "challenge_class": row["challenge_class"],
            "legacy_matcher_accepts": row["legacy_matcher_accepts"],
            "root_cause_aliases": row["root_cause_aliases"],
        })

    def shuffled_packet(seed: int) -> list[dict[str, Any]]:
        rows = list(packet_by_example.values())
        random.Random(seed).shuffle(rows)
        return rows

    key_rows.sort(key=lambda row: row["review_id"])
    key = {
        "key_status": "PRIVATE_DO_NOT_SHARE_BEFORE_REVIEWS_LOCKED",
        "protocol_version": "scoring-calibration-v1",
        "items": key_rows,
    }
    return shuffled_packet(reviewer_a_seed), shuffled_packet(reviewer_b_seed), key


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build separate blinded scoring-calibration packets and a private unblinding key."
    )
    parser.add_argument("--examples", type=Path, default=DEFAULT_EXAMPLES)
    parser.add_argument("--reviewer-a-output", type=Path, required=True)
    parser.add_argument("--reviewer-b-output", type=Path, required=True)
    parser.add_argument("--key-output", type=Path, required=True)
    parser.add_argument("--reviewer-a-seed", type=int, default=1701)
    parser.add_argument("--reviewer-b-seed", type=int, default=2903)
    args = parser.parse_args()

    examples = read_jsonl(args.examples)
    packet_a, packet_b, key = build_packets(
        examples,
        reviewer_a_seed=args.reviewer_a_seed,
        reviewer_b_seed=args.reviewer_b_seed,
    )
    write_jsonl(args.reviewer_a_output, packet_a)
    write_jsonl(args.reviewer_b_output, packet_b)
    args.key_output.parent.mkdir(parents=True, exist_ok=True)
    args.key_output.write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "packets_built",
        "example_count": len(examples),
        "reviewer_a_packet": str(args.reviewer_a_output),
        "reviewer_b_packet": str(args.reviewer_b_output),
        "private_key": str(args.key_output),
        "warning": "Keep the private key outside version control and do not share it until both independent reviews are locked.",
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
