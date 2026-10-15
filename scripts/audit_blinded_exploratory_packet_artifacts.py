#!/usr/bin/env python3
"""Fail-closed integrity audit for the frozen 2026-10-15 v1.2 review packets.

Reads the archived historical outputs, two reviewer ZIPs, and two private
coordinator keys. Never prints the keys, case identifiers, conditions, seeds,
source revisions, prompt hashes, or individual model outputs.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

EXPECTED = {
    "archive": "e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd",
    "A": "0604919587fe8063b294c9ca5848d6a5843b683df68de8b66cbb9894ff61fdb0",
    "B": "c247950cdf55be67da4adce934397fc558e168c9f74781b550cc56bb1ced81fb",
}
FORBIDDEN_REVIEW_FIELDS = {
    "case_id", "condition", "seed", "source_commit", "source_url",
    "prompt_sha256", "context_sha256", "raw_output_sha256", "ground_truth",
    "answer_key", "expected_root_cause", "canonical_root_cause",
}
REVIEW_FIELDS = {
    "root_cause_correctness", "component_localization", "evidence_consistency",
    "dependency_reasoning", "overall_diagnostic_status", "reviewer_notes_with_evidence",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json_lines(data: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]


def walk_keys(value: Any):
    if isinstance(value, dict):
        for key, sub in value.items():
            yield key
            yield from walk_keys(sub)
    elif isinstance(value, list):
        for sub in value:
            yield from walk_keys(sub)


def walk_strings(value: Any):
    if isinstance(value, dict):
        for sub in value.values():
            yield from walk_strings(sub)
    elif isinstance(value, list):
        for sub in value:
            yield from walk_strings(sub)
    elif isinstance(value, str):
        yield value


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def audit(archive_path: Path, packet_a_path: Path, packet_b_path: Path,
          key_a_path: Path, key_b_path: Path) -> dict[str, Any]:
    paths = [archive_path, packet_a_path, packet_b_path, key_a_path, key_b_path]
    for p in paths:
        require(p.is_file(), f"Required input missing: {p.name}")

    archive_bytes = archive_path.read_bytes()
    actual_hashes = {
        "archive": sha256(archive_bytes),
        "A": sha256(packet_a_path.read_bytes()),
        "B": sha256(packet_b_path.read_bytes()),
    }
    for label, digest in actual_hashes.items():
        require(digest == EXPECTED[label], f"{label} SHA-256 does not match frozen v1.2 value")

    with zipfile.ZipFile(archive_path) as z:
        require(z.testzip() is None, "Historical archive CRC/integrity check failed")
        members = set(z.namelist())
        root = "confirmatory-output/"
        manifest = json.loads(z.read(root + "artifact_manifest.json"))
        declared = manifest.get("files", [])
        require(len(declared) == 212 and manifest.get("file_count") == 212,
                "Historical artifact manifest no longer declares 212 files")
        bad_manifest_entries = 0
        for entry in declared:
            rel = entry["path"]
            full = rel if rel.startswith(root) else root + rel
            if full not in members:
                bad_manifest_entries += 1
                continue
            body = z.read(full)
            if len(body) != entry["bytes"] or sha256(body) != entry["sha256"]:
                bad_manifest_entries += 1
        require(bad_manifest_entries == 0, "Historical archive manifest integrity failure")

        run_names = [name for name in members if name.startswith(root + "runs/") and name.endswith(".json")]
        archive_runs = [json.loads(z.read(name)) for name in run_names]
        identities = {(r["case_id"], r["condition"], r["seed"]) for r in archive_runs}
        require(len(archive_runs) == 160 and len(identities) == 160,
                "Historical archive must contain 160 unique case-condition-seed records")
        require(len({r["case_id"] for r in archive_runs}) == 16,
                "Historical archive must contain 16 independent defect cases")
        archive_by_id = {(r["case_id"], r["condition"], r["seed"]): r for r in archive_runs}

    key_a = json.loads(key_a_path.read_text(encoding="utf-8"))
    key_b = json.loads(key_b_path.read_text(encoding="utf-8"))
    require(key_a.get("reviewer_code") == "A" and key_b.get("reviewer_code") == "B",
            "Reviewer-specific private-key pairing is inconsistent")
    require(key_a.get("source_artifact_sha256") == actual_hashes["archive"] == key_b.get("source_artifact_sha256"),
            "Private key references a different source archive")
    key_maps = {}
    for label, key in (("A", key_a), ("B", key_b)):
        recs = key.get("records", [])
        require(len(recs) == 160, f"Private key {label} must contain 160 mappings")
        mapping = {item["review_id"]: item for item in recs}
        require(len(mapping) == 160, f"Private key {label} contains duplicate review IDs")
        key_maps[label] = mapping

    packet_rows = {}
    per_reviewer = {}
    for label, packet_path in (("A", packet_a_path), ("B", packet_b_path)):
        with zipfile.ZipFile(packet_path) as z:
            require(z.testzip() is None, f"Reviewer {label} ZIP integrity check failed")
            names = {n for n in z.namelist() if not n.endswith("/")}
            require(names == {"README_REVIEWER.md", "review_packet.jsonl"},
                    f"Reviewer {label} ZIP has unexpected members")
            rows = read_json_lines(z.read("review_packet.jsonl"))
        require(len(rows) == 161, f"Reviewer {label} packet must contain one header and 160 rows")
        header, response_rows = rows[0], rows[1:]
        require(header.get("reviewer_code") == label and header.get("n_records") == 160,
                f"Reviewer {label} header is inconsistent")
        require(header.get("review_status") == "unreviewed_packet",
                f"Reviewer {label} packet is not marked unreviewed")
        require(len({r.get("review_id") for r in response_rows}) == 160,
                f"Reviewer {label} packet has duplicate/missing review IDs")
        require(len({r.get("case_ref") for r in response_rows}) == 16,
                f"Reviewer {label} packet must contain 16 anonymized case references")

        forbidden_hits = []
        url_rows = 0
        blank_rows = 0
        mapping_checks = collections.Counter()
        for row in response_rows:
            keys = set(walk_keys(row))
            forbidden_hits.extend(sorted(keys & FORBIDDEN_REVIEW_FIELDS))
            if any(re.search(r"https?://", s) for s in walk_strings(row)):
                url_rows += 1
            review = row.get("review")
            require(isinstance(review, dict) and set(review) == REVIEW_FIELDS,
                    f"Reviewer {label} review schema does not match the frozen rubric")
            if all(v in ("", None, []) for v in review.values()):
                blank_rows += 1

            mapping = key_maps[label].get(row["review_id"])
            require(mapping is not None, f"Reviewer {label} row has no private mapping")
            ident = (mapping["source_case_id"], mapping["condition"], mapping["seed"])
            source = archive_by_id.get(ident)
            require(source is not None, f"Reviewer {label} mapping has no archive run")
            raw_hash = sha256(row["response"]["raw_output"].encode("utf-8"))
            require(raw_hash == mapping["raw_output_sha256"] == source["raw_output_sha256"],
                    f"Reviewer {label} raw output does not match the frozen archive")
            mapping_checks["raw_output_hash"] += 1
            require(mapping["prompt_sha256"] == source["prompt_sha256"] and
                    mapping["context_sha256"] == source["context_sha256"],
                    f"Reviewer {label} prompt/context mapping mismatch")
            mapping_checks["prompt_context_hashes"] += 1
            require(mapping["source_commit"] == source["source_commit"],
                    f"Reviewer {label} source commit mapping mismatch")
            mapping_checks["source_commit"] += 1
            require(mapping["case_ref"] == row["case_ref"],
                    f"Reviewer {label} anonymous case reference mismatch")
            mapping_checks["case_reference"] += 1

        require(not forbidden_hits, f"Reviewer {label} has prohibited metadata keys")
        require(url_rows == 0, f"Reviewer {label} has direct URL(s) in response rows")
        require(blank_rows == 160, f"Reviewer {label} packet has pre-filled ratings")
        packet_rows[label] = response_rows
        per_reviewer[label] = {
            "zip_sha256": actual_hashes[label],
            "zip_bytes": packet_path.stat().st_size,
            "zip_members": 2,
            "review_rows": len(response_rows),
            "unique_case_refs": 16,
            "unique_review_ids": 160,
            "all_ratings_blank": True,
            "prohibited_metadata_field_hits": 0,
            "rows_with_direct_urls": 0,
            "archive_linkage_checks": dict(mapping_checks),
            "archive_linkage_records_per_check": 160,
        }

    def comparable(row: dict[str, Any]) -> tuple[str, str]:
        return row["case_ref"], sha256(row["response"]["raw_output"].encode("utf-8"))

    a_sequence = [comparable(r) for r in packet_rows["A"]]
    b_sequence = [comparable(r) for r in packet_rows["B"]]
    require(collections.Counter(a_sequence) == collections.Counter(b_sequence),
            "Reviewer A/B packet response multisets differ")
    identical_positions = sum(a == b for a, b in zip(a_sequence, b_sequence))

    return {
        "status": "PASS",
        "audit_scope": "file integrity and blinded-packet mapping only; not human semantic scoring",
        "historical_archive": {
            "sha256": actual_hashes["archive"],
            "bytes": archive_path.stat().st_size,
            "manifest_entries_verified": 212,
            "manifest_size_hash_mismatches": 0,
            "archive_run_records": 160,
            "unique_case_condition_seed_identities": 160,
            "independent_cases": 16,
        },
        "reviewers": per_reviewer,
        "A_B_same_response_multiset": True,
        "A_B_same_row_positions": identical_positions,
        "A_B_total_row_positions": 160,
        "human_ratings_received": False,
        "semantic_correctness_established": False,
        "historical_frozen_endpoint_modified": False,
        "new_inference_performed": False,
        "coordinator_private_keys_written_to_report": False,
    }


def main() -> int:
    if len(sys.argv) != 6:
        print("Usage: audit_blinded_exploratory_packet_artifacts.py ARCHIVE.zip REVIEWER_A.zip REVIEWER_B.zip PRIVATE_KEY_A.json PRIVATE_KEY_B.json", file=sys.stderr)
        return 2
    try:
        result = audit(*(Path(p) for p in sys.argv[1:]))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
