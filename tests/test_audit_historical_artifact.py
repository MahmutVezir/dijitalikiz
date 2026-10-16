from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from scripts.audit_historical_artifact import AuditFailure, audit_archive

MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"
SOURCE_COMMIT = "a" * 40
CONDITIONS = ["standard", "ccdg"]
SEEDS = [42]
CASE_IDS = ["case-A", "case-B"]
REQUIRED = [
    "environment.json",
    "confirmatory_evaluation.json",
    "case_level_analysis.json",
    "primary_analysis.json",
    "confirmatory_qa_report.json",
    "confirmatory_records.jsonl",
    "benchmark_manifest.json",
]


def make_rows() -> list[dict]:
    rows = []
    for case_id in CASE_IDS:
        for condition in CONDITIONS:
            raw = f'{{"case":"{case_id}","condition":"{condition}"}}'
            rows.append(
                {
                    "case_id": case_id,
                    "condition": condition,
                    "seed": 42,
                    "source_commit": SOURCE_COMMIT,
                    "model_id": MODEL_ID,
                    "model_revision": REVISION,
                    "temperature": 0.2,
                    "top_p": 1.0,
                    "max_new_tokens": 256,
                    "system_prompt_sha256": "b" * 64,
                    "raw_output": raw,
                    "raw_output_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                }
            )
    return rows


def build_zip(path: Path, rows: list[dict] | None = None, *, wrong_file_hash: bool = False, omit_member: str | None = None) -> str:
    rows = make_rows() if rows is None else rows
    payloads = {
        "environment.json": b"{}\n",
        "case_level_analysis.json": b"{}\n",
        "primary_analysis.json": b"{}\n",
        "confirmatory_qa_report.json": b"{}\n",
        "benchmark_manifest.json": json.dumps(
            {"status": "frozen", "case_ids": CASE_IDS}, separators=(",", ":")
        ).encode(),
        "pilot_manifest.json": json.dumps(
            {
                "conditions": CONDITIONS,
                "generation": {
                    "seeds": SEEDS,
                    "temperature": 0.2,
                    "top_p": 1.0,
                    "max_new_tokens": 256,
                },
                "model": {"model_id": MODEL_ID, "revision": REVISION},
                "system_prompt": {"sha256": "b" * 64},
            },
            separators=(",", ":"),
        ).encode(),
        "confirmatory_records.jsonl": ("\n".join(json.dumps(row, separators=(",", ":")) for row in rows) + "\n").encode(),
    }
    per_condition = len(CASE_IDS) * len(SEEDS)
    payloads["confirmatory_evaluation.json"] = json.dumps(
        {
            "status": "complete",
            "expected_records": 4,
            "found_records": 4,
            "missing_files": [],
            "by_condition": {
                condition: {"n_expected": per_condition, "n_found": per_condition}
                for condition in CONDITIONS
            },
        },
        separators=(",", ":"),
    ).encode()
    declared = []
    for name in REQUIRED + ["pilot_manifest.json"]:
        data = payloads[name]
        item = {
            "path": name,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        if wrong_file_hash and name == "environment.json":
            item["sha256"] = "0" * 64
        declared.append(item)
    manifest = {
        "version": "0.2",
        "root": "data/benchmark",
        "finalization_gate": {
            "expected_run_record_count": 4,
            "required_final_files": REQUIRED,
            "status": "complete",
        },
        "files": declared,
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("confirmatory-output/artifact_manifest.json", json.dumps(manifest).encode())
        for name, data in payloads.items():
            member = "confirmatory-output/" + name
            if member != omit_member:
                zf.writestr(member, data)
        zf.writestr("run.log", "synthetic fixture only\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_accepts_complete_pinned_artifact(tmp_path):
    path = tmp_path / "complete.zip"
    pin = build_zip(path)
    result = audit_archive(path, expected_sha256=pin, expected_run_record_count=4)
    assert result["status"] == "pass"
    assert result["manifest_declared_files"] == 8
    assert result["expected_run_records"] == 4
    assert result["found_run_records"] == 4
    assert result["unique_run_records"] == 4
    assert result["conditions"] == {"standard": 2, "ccdg": 2}


def test_rejects_archive_sha_mismatch(tmp_path):
    path = tmp_path / "complete.zip"
    build_zip(path)
    with pytest.raises(AuditFailure, match="archive SHA-256 mismatch"):
        audit_archive(path, expected_sha256="0" * 64, expected_run_record_count=4)


def test_rejects_manifest_listed_file_missing_from_zip(tmp_path):
    path = tmp_path / "missing-member.zip"
    pin = build_zip(path, omit_member="confirmatory-output/environment.json")
    with pytest.raises(AuditFailure, match="manifest-listed file is missing"):
        audit_archive(path, expected_sha256=pin, expected_run_record_count=4)


def test_rejects_file_hash_mismatch_even_when_zip_pin_matches(tmp_path):
    path = tmp_path / "bad-file-hash.zip"
    pin = build_zip(path, wrong_file_hash=True)
    with pytest.raises(AuditFailure, match="SHA-256 mismatch for environment.json"):
        audit_archive(path, expected_sha256=pin, expected_run_record_count=4)


def test_rejects_missing_record_identity(tmp_path):
    path = tmp_path / "missing-row.zip"
    pin = build_zip(path, make_rows()[:-1])
    with pytest.raises(AuditFailure, match="missing expected record identities|row-count mismatch"):
        audit_archive(path, expected_sha256=pin, expected_run_record_count=4)


def test_rejects_duplicate_record_identity(tmp_path):
    path = tmp_path / "duplicate-row.zip"
    rows = make_rows()
    rows[-1] = dict(rows[0])
    rows[-1]["raw_output"] = rows[0]["raw_output"]
    rows[-1]["raw_output_sha256"] = rows[0]["raw_output_sha256"]
    pin = build_zip(path, rows)
    with pytest.raises(AuditFailure, match="duplicate record identities|missing expected record identities"):
        audit_archive(path, expected_sha256=pin, expected_run_record_count=4)
