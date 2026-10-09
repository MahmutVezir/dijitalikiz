import hashlib
import json
from pathlib import Path

from dijitalikiz.pilot_config import (
    expected_pilot_record_count,
    expected_pilot_run_filenames,
)
from scripts.validate_pilot_artifact_manifest import (
    REQUIRED_FINAL_FILES,
    sha256_file,
    validate,
)


def _frozen_manifest() -> dict:
    return {
        "version": "0.7",
        "status": "model_frozen",
        "cases": ["case-a", "case-b", "case-c", "case-d"],
        "conditions": ["standard", "ccdg"],
        "replications": 5,
        "generation": {"seeds": [42, 43, 44, 45, 46]},
        "expected_records": 40,
    }


def _write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _build_valid_artifact(root: Path) -> Path:
    pilot_manifest = _frozen_manifest()
    (root / "pilot_manifest.json").write_text(
        json.dumps(pilot_manifest, indent=2), encoding="utf-8"
    )

    for name in REQUIRED_FINAL_FILES - {"pilot_manifest.json"}:
        _write(root / name, f"{name}\n".encode())

    for case_id in pilot_manifest["cases"]:
        _write(root / f"{case_id}.json", json.dumps({"case_id": case_id}).encode())

    for index, name in enumerate(
        sorted(expected_pilot_run_filenames(pilot_manifest, require_declared=True))
    ):
        _write(root / "runs" / name, json.dumps({"index": index}).encode())

    entries = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "artifact_manifest.json":
            entries.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )

    expected_count = expected_pilot_record_count(pilot_manifest, require_declared=True)
    manifest = {
        "version": "1.3",
        "root": "data/pilot",
        "finalization_gate": {
            "expected_run_record_count": expected_count,
            "required_final_files": sorted(REQUIRED_FINAL_FILES),
            "status": "complete",
        },
        "files": entries,
        "file_count": len(entries),
        "run_record_count": expected_count,
    }
    manifest_path = root / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def test_artifact_manifest_verification_requires_all_frozen_runs_and_inputs(tmp_path: Path):
    manifest_path = _build_valid_artifact(tmp_path)
    assert validate(tmp_path, manifest_path) == []


def test_artifact_manifest_detects_same_size_tampering(tmp_path: Path):
    manifest_path = _build_valid_artifact(tmp_path)
    target = tmp_path / "pilot_evaluation.json"
    original = target.read_bytes()
    target.write_bytes(b"!" * len(original))
    assert target.stat().st_size == len(original)

    errors = validate(tmp_path, manifest_path)
    assert any("sha256 mismatch" in error for error in errors)


def test_artifact_manifest_rejects_incomplete_run_list(tmp_path: Path):
    manifest_path = _build_valid_artifact(tmp_path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_entry = next(
        entry for entry in payload["files"] if entry["path"].startswith("runs/")
    )
    payload["files"] = [
        entry for entry in payload["files"] if entry is not run_entry
    ]
    payload["file_count"] = len(payload["files"])
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate(tmp_path, manifest_path)
    assert any("run record path set mismatch" in error for error in errors)
    assert any("unlisted artifact file" in error for error in errors)


def test_artifact_manifest_rejects_path_traversal(tmp_path: Path):
    manifest_path = _build_valid_artifact(tmp_path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["files"].append(
        {
            "path": "../escape.txt",
            "bytes": 0,
            "sha256": hashlib.sha256(b"").hexdigest(),
        }
    )
    payload["file_count"] = len(payload["files"])
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate(tmp_path, manifest_path)
    assert any("unsafe manifest path" in error for error in errors)
