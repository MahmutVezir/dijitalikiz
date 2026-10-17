from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest

from dijitalikiz.context import render_ccdg_context, render_standard_context
from dijitalikiz.models import ResearchCase
from scripts.audit_historical_artifact import (
    PINNED_MODEL_ID,
    PINNED_MODEL_REVISION,
    PINNED_SOURCE_COMMIT,
    AuditFailure,
    audit_archive,
    main,
)

CONDITIONS = ["standard", "ccdg"]
SEEDS = [42, 43, 44, 45, 46]
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
PROMPT = "Synthetic test-only prompt\n"
SYSTEM_PROMPT = "Return a JSON object.\n"


def case_payload(case_id: str) -> dict:
    return {
        "case_id": case_id,
        "source": "fixture-source",
        "source_url": "https://example.invalid/case",
        "publication_date": "2026-01-01",
        "technology": "synthetic fixture",
        "error_description": "test-only synthetic defect",
        "i_base": ["synthetic base fact"],
        "ccdg": [{"source": "A", "target": "B", "relation": "depends_on", "details": "fixture edge"}],
        "ground_truth": {"component": "A", "entity": "B", "operation": "test", "root_cause": "fixture", "required_relations": []},
    }


def make_rows(cases: dict[str, dict]) -> list[dict]:
    pilot = {
        "model": {"model_id": PINNED_MODEL_ID, "revision": PINNED_MODEL_REVISION, "precision": "float16", "quantization": "none"},
        "generation": {"temperature": 0.2, "top_p": 1.0, "max_new_tokens": 256},
        "prompt": {"sha256": hashlib.sha256(PROMPT.encode()).hexdigest()},
        "system_prompt": {"sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()},
    }
    rows = []
    for case_id, payload in cases.items():
        case = ResearchCase.from_dict(payload)
        for condition in CONDITIONS:
            context = render_standard_context(case) if condition == "standard" else render_ccdg_context(case)
            prompt_hash = hashlib.sha256((PROMPT + "\n\n" + context).encode()).hexdigest()
            context_hash = hashlib.sha256(context.encode()).hexdigest()
            for seed in SEEDS:
                raw = json.dumps({"diagnosis": case_id, "condition": condition}, separators=(",", ":"))
                rows.append({
                    "source_commit": PINNED_SOURCE_COMMIT,
                    "case_id": case_id,
                    "condition": condition,
                    "seed": seed,
                    "model_id": pilot["model"]["model_id"],
                    "model_revision": pilot["model"]["revision"],
                    "model_dtype": pilot["model"]["precision"],
                    "quantization": pilot["model"]["quantization"],
                    "temperature": pilot["generation"]["temperature"],
                    "top_p": pilot["generation"]["top_p"],
                    "max_new_tokens": pilot["generation"]["max_new_tokens"],
                    "prompt_sha256": prompt_hash,
                    "system_prompt_sha256": pilot["system_prompt"]["sha256"],
                    "context_sha256": context_hash,
                    "raw_output": raw,
                    "raw_output_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                })
    return rows


def build_zip(
    path: Path,
    *,
    rows: list[dict] | None = None,
    omit_member: str | None = None,
    wrong_file_hash: bool = False,
    wrong_file_size: bool = False,
    bad_jsonl: bool = False,
    bad_manifest: bool = False,
    omit_manifest: bool = False,
    pilot_overrides: dict | None = None,
    extra_member: str | None = None,
) -> str:
    cases = {case_id: case_payload(case_id) for case_id in CASE_IDS}
    payloads = {
        "environment.json": b"{}\n",
        "case_level_analysis.json": b"{}\n",
        "primary_analysis.json": b"{}\n",
        "confirmatory_qa_report.json": b"{}\n",
        "benchmark_manifest.json": json.dumps({"status": "frozen", "case_ids": CASE_IDS}, separators=(",", ":")).encode(),
        "PROMPT_TEMPLATE.txt": PROMPT.encode(),
        "SYSTEM_PROMPT.txt": SYSTEM_PROMPT.encode(),
    }
    for case_id, case in cases.items():
        payloads[f"cases/{case_id}.json"] = json.dumps(case, separators=(",", ":")).encode()
    pilot_payload = {
        "conditions": CONDITIONS,
        "generation": {"seeds": SEEDS, "temperature": 0.2, "top_p": 1.0, "do_sample": True, "max_new_tokens": 256},
        "model": {"model_id": PINNED_MODEL_ID, "revision": PINNED_MODEL_REVISION, "precision": "float16", "quantization": "none"},
        "prompt": {"path": "PROMPT_TEMPLATE.txt", "sha256": hashlib.sha256(PROMPT.encode()).hexdigest()},
        "system_prompt": {"path": "SYSTEM_PROMPT.txt", "sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()},
    }
    for section, overrides in (pilot_overrides or {}).items():
        if section in pilot_payload and isinstance(pilot_payload[section], dict) and isinstance(overrides, dict):
            pilot_payload[section].update(overrides)
        else:
            pilot_payload[section] = overrides
    payloads["pilot_manifest.json"] = json.dumps(pilot_payload, separators=(",", ":")).encode()
    if rows is None:
        rows = make_rows(cases)
    jsonl = "\n".join(json.dumps(row, separators=(",", ":")) for row in rows) + "\n"
    if bad_jsonl:
        jsonl = "not-valid-json\n"
    payloads["confirmatory_records.jsonl"] = jsonl.encode()
    n_records = len(CASE_IDS) * len(CONDITIONS) * len(SEEDS)
    per_condition = len(CASE_IDS) * len(SEEDS)
    payloads["confirmatory_evaluation.json"] = json.dumps({
        "status": "complete", "expected_records": n_records, "found_records": n_records, "missing_files": [],
        "by_condition": {condition: {"n_expected": per_condition, "n_found": per_condition} for condition in CONDITIONS},
    }, separators=(",", ":")).encode()

    declared = []
    for name, data in payloads.items():
        item = {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        if wrong_file_hash and name == "environment.json":
            item["sha256"] = "0" * 64
        if wrong_file_size and name == "environment.json":
            item["bytes"] += 1
        declared.append(item)
    manifest = {
        "version": "0.2", "root": "data/benchmark", "run_record_count": n_records,
        "file_count": len(declared),
        "finalization_gate": {"expected_run_record_count": n_records, "required_final_files": REQUIRED, "status": "complete"},
        "files": declared,
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        manifest_bytes = b"not-json" if bad_manifest else json.dumps(manifest, separators=(",", ":")).encode()
        if not omit_manifest:
            zf.writestr("confirmatory-output/artifact_manifest.json", manifest_bytes)
        for name, data in payloads.items():
            member = "confirmatory-output/" + name
            if member != omit_member:
                zf.writestr(member, data)
        if extra_member:
            zf.writestr("confirmatory-output/" + extra_member, b"unmanifested\n")
        zf.writestr("run.log", "synthetic fixture only\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(path: Path, digest: str):
    return audit_archive(path, expected_sha256=digest, expected_run_record_count=20)


def test_accepts_complete_pinned_artifact(tmp_path):
    path = tmp_path / "complete.zip"
    digest = build_zip(path)
    result = audit(path, digest)
    assert result["status"] == "pass"
    assert result["manifest_declared_files"] == result["files_checked"]
    assert result["expected_run_records"] == result["found_run_records"] == result["unique_run_records"] == 20
    assert result["conditions"] == {"standard": 10, "ccdg": 10}
    assert result["source_commits"] == [PINNED_SOURCE_COMMIT]


def test_rejects_archive_sha_mismatch(tmp_path):
    path = tmp_path / "archive.zip"
    build_zip(path)
    with pytest.raises(AuditFailure, match="archive SHA-256 mismatch"):
        audit(path, "0" * 64)


def test_rejects_missing_manifest_listed_file(tmp_path):
    path = tmp_path / "missing-member.zip"
    digest = build_zip(path, omit_member="confirmatory-output/environment.json")
    with pytest.raises(AuditFailure, match="manifest-listed file is missing"):
        audit(path, digest)


@pytest.mark.parametrize("kwargs,match", [
    ({"wrong_file_hash": True}, "SHA-256 mismatch for environment.json"),
    ({"wrong_file_size": True}, "byte-size mismatch for environment.json"),
])
def test_rejects_manifest_file_size_or_hash_mismatch(tmp_path, kwargs, match):
    path = tmp_path / "mismatch.zip"
    digest = build_zip(path, **kwargs)
    with pytest.raises(AuditFailure, match=match):
        audit(path, digest)


@pytest.mark.parametrize("row_mutation,match", [
    (lambda rows: rows[:-1], "missing expected record identities|JSONL row-count mismatch"),
    (lambda rows: rows[:-1] + [dict(rows[0])], "duplicate record identities|missing expected record identities"),
    (lambda rows: [dict(rows[0], condition="unexpected")]+rows[1:], "unexpected case/condition/seed identity|missing expected record identities"),
    (lambda rows: [dict(rows[0], raw_output_sha256="0"*64)]+rows[1:], "raw_output SHA-256 mismatch"),
    (lambda rows: [dict(rows[0], model_id="different/model")]+rows[1:], "model_id mismatch"),
    (lambda rows: [dict(rows[0], model_revision="0"*40)]+rows[1:], "model_revision mismatch"),
    (lambda rows: [dict(rows[0], temperature=0.7)]+rows[1:], "temperature mismatch"),
    (lambda rows: [dict(rows[0], top_p=0.5)]+rows[1:], "top_p mismatch"),
    (lambda rows: [dict(rows[0], max_new_tokens=128)]+rows[1:], "max_new_tokens mismatch"),
    (lambda rows: [dict(rows[0], prompt_sha256="0"*64)]+rows[1:], "prompt_sha256 mismatch"),
    (lambda rows: [dict(rows[0], context_sha256="0"*64)]+rows[1:], "context_sha256 mismatch"),
    (lambda rows: [dict(rows[0], system_prompt_sha256="0"*64)]+rows[1:], "system_prompt_sha256 mismatch"),
    (lambda rows: [dict(rows[0], model_dtype="bfloat16")]+rows[1:], "model_dtype mismatch"),
    (lambda rows: [dict(rows[0], quantization="gptq-int4")]+rows[1:], "quantization mismatch"),
    (lambda rows: [dict(rows[0], source_commit="0"*40)]+rows[1:], "source_commit mismatch"),
])
def test_rejects_bad_record_identity_or_frozen_fields(tmp_path, row_mutation, match):
    path = tmp_path / "bad-record.zip"
    rows = row_mutation(make_rows({case_id: case_payload(case_id) for case_id in CASE_IDS}))
    digest = build_zip(path, rows=rows)
    with pytest.raises(AuditFailure, match=match):
        audit(path, digest)


def test_rejects_broken_jsonl_and_manifest(tmp_path):
    bad_jsonl_path = tmp_path / "broken-jsonl.zip"
    digest = build_zip(bad_jsonl_path, bad_jsonl=True)
    with pytest.raises(AuditFailure, match="invalid JSONL record"):
        audit(bad_jsonl_path, digest)
    bad_manifest_path = tmp_path / "broken-manifest.zip"
    digest = build_zip(bad_manifest_path, bad_manifest=True)
    with pytest.raises(AuditFailure, match="cannot parse.*artifact_manifest"):
        audit(bad_manifest_path, digest)


def test_rejects_unmanifested_payload_and_missing_case_file(tmp_path):
    extra_path = tmp_path / "extra.zip"
    digest = build_zip(extra_path, extra_member="unexpected.json")
    with pytest.raises(AuditFailure, match="unmanifested file"):
        audit(extra_path, digest)
    missing_case_path = tmp_path / "missing-case.zip"
    digest = build_zip(missing_case_path, omit_member="confirmatory-output/cases/case-A.json")
    with pytest.raises(AuditFailure, match="manifest-listed file is missing"):
        audit(missing_case_path, digest)



@pytest.mark.parametrize("overrides,match", [
    ({"model": {"model_id": "different/model"}}, "model ID/revision"),
    ({"model": {"revision": "0" * 40}}, "model ID/revision"),
    ({"generation": {"temperature": 0.7}}, "temperature does not match"),
    ({"generation": {"top_p": 0.5}}, "top_p does not match"),
    ({"generation": {"do_sample": False}}, "do_sample=true"),
    ({"generation": {"max_new_tokens": 128}}, "max_new_tokens does not match"),
    ({"generation": {"seeds": [42]}}, "seeds do not match"),
])
def test_rejects_mismatched_frozen_manifest_settings(tmp_path, overrides, match):
    path = tmp_path / "bad-frozen-manifest.zip"
    digest = build_zip(path, pilot_overrides=overrides)
    with pytest.raises(AuditFailure, match=match):
        audit(path, digest)


def test_rejects_missing_artifact_manifest(tmp_path):
    path = tmp_path / "no-artifact-manifest.zip"
    digest = build_zip(path, omit_manifest=True)
    with pytest.raises(AuditFailure, match="missing historical artifact manifest"):
        audit(path, digest)

def test_cli_returns_nonzero_when_archive_is_missing(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(sys, "argv", ["audit_historical_artifact.py", "--archive", str(tmp_path / "absent.zip"), "--expected-sha256", "e" * 64, "--expected-run-record-count", "160"])
    assert main() == 1
    assert '"status": "fail"' in capsys.readouterr().err
