import hashlib
import json

import pytest

from scripts import model_load_preflight


MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"
REVISION = "aa8e72537993ba99e69dfaafa59ed015b17504d1"


def write_json(path, value):
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")


def valid_manifest():
    return {
        "model": {"model_id": MODEL_ID, "revision": REVISION},
        "expected_records": 40,
    }


SOURCE_COMMIT = "d34db33fd34db33fd34db33fd34db33fd34db33f"


def valid_report(manifest, manifest_bytes):
    return {
        "schema_version": 1,
        "status": "pass",
        "pilot_authorized": True,
        "model_id": MODEL_ID,
        "model_revision": REVISION,
        "expected_records": manifest["expected_records"],
        "source_commit": SOURCE_COMMIT,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "checks": [
            {"name": name, "status": "pass", "detail": "unit-test receipt"}
            for name in sorted(model_load_preflight.REQUIRED_RECEIPT_CHECKS)
        ],
    }


def install_receipt_files(monkeypatch, tmp_path, report_overrides=None, manifest_overrides=None):
    # The report is tied to the original manifest; write any requested mutation
    # only to the on-disk manifest to exercise stale-receipt rejection.
    original_manifest = valid_manifest()
    original_manifest_bytes = json.dumps(original_manifest, sort_keys=True).encode("utf-8")
    report = valid_report(original_manifest, original_manifest_bytes)
    manifest_on_disk = dict(original_manifest)
    if manifest_overrides:
        manifest_on_disk.update(manifest_overrides)
    manifest_bytes = json.dumps(manifest_on_disk, sort_keys=True).encode("utf-8")
    if report_overrides:
        report.update(report_overrides)
    report_path = tmp_path / "compatibility_report.json"
    manifest_path = tmp_path / "pilot_manifest.json"
    source_commit_path = tmp_path / "kaggle_source_commit.txt"
    source_commit_path.write_text(SOURCE_COMMIT + "\n", encoding="utf-8")
    report_path.write_text(json.dumps(report), encoding="utf-8")
    manifest_path.write_bytes(manifest_bytes)
    monkeypatch.setattr(model_load_preflight, "REPORT", report_path)
    monkeypatch.setattr(model_load_preflight, "MANIFEST", manifest_path)
    monkeypatch.setattr(model_load_preflight, "SOURCE_COMMIT", source_commit_path)
    return report, manifest_on_disk


def test_valid_current_receipt_is_accepted(monkeypatch, tmp_path, capsys):
    install_receipt_files(monkeypatch, tmp_path)
    assert model_load_preflight.main() == 0
    assert "VERIFIED" in capsys.readouterr().out


@pytest.mark.parametrize(
    "report_overrides,manifest_overrides",
    [
        ({"status": "fail"}, None),
        ({"pilot_authorized": False}, None),
        ({"model_id": "different/model"}, None),
        ({"model_revision": "deadbeef"}, None),
        ({"expected_records": 999}, None),
        ({"source_commit": "unknown"}, None),
        ({"source_commit": "0" * 40}, None),
        ({"manifest_sha256": "0" * 64}, None),
        ({"schema_version": 99}, None),
        (None, {"expected_records": 41}),
    ],
)
def test_stale_or_mismatched_receipt_is_rejected(
    monkeypatch, tmp_path, capsys, report_overrides, manifest_overrides
):
    install_receipt_files(
        monkeypatch,
        tmp_path,
        report_overrides=report_overrides,
        manifest_overrides=manifest_overrides,
    )
    assert model_load_preflight.main() == 1
    assert "REJECTED" in capsys.readouterr().err


def test_receipt_with_a_missing_required_check_is_rejected(monkeypatch, tmp_path, capsys):
    report, _ = install_receipt_files(monkeypatch, tmp_path)
    report["checks"] = [
        row for row in report["checks"]
        if row["name"] != "pilot_sampling_smoke"
    ]
    model_load_preflight.REPORT.write_text(json.dumps(report), encoding="utf-8")
    assert model_load_preflight.main() == 1
    assert "required checks are missing" in capsys.readouterr().err


def test_receipt_with_nonpassing_or_malformed_check_is_rejected(monkeypatch, tmp_path, capsys):
    report, _ = install_receipt_files(monkeypatch, tmp_path)
    report["checks"][0]["status"] = "not_run"
    report["checks"].append(None)
    model_load_preflight.REPORT.write_text(json.dumps(report), encoding="utf-8")
    assert model_load_preflight.main() == 1
    assert "malformed check record" in capsys.readouterr().err


def test_missing_or_invalid_report_fails_closed(monkeypatch, tmp_path, capsys):
    manifest_path = tmp_path / "pilot_manifest.json"
    write_json(manifest_path, valid_manifest())
    monkeypatch.setattr(model_load_preflight, "MANIFEST", manifest_path)
    source_commit_path = tmp_path / "kaggle_source_commit.txt"
    source_commit_path.write_text(SOURCE_COMMIT + "\n", encoding="utf-8")
    monkeypatch.setattr(model_load_preflight, "SOURCE_COMMIT", source_commit_path)
    monkeypatch.setattr(model_load_preflight, "REPORT", tmp_path / "missing_report.json")
    assert model_load_preflight.main() == 1
    assert "MISSING/INVALID" in capsys.readouterr().err

    model_load_preflight.REPORT.write_text("{not json", encoding="utf-8")
    assert model_load_preflight.main() == 1
    assert "MISSING/INVALID" in capsys.readouterr().err
