import hashlib
import json
from pathlib import Path

from scripts.validate_pilot_artifact_manifest import (
    EXPECTED_RUN_COUNT,
    REQUIRED_FINAL_FILES,
    sha256_file,
    validate,
)


def _write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _build_valid_artifact(root: Path) -> Path:
    runs = root / "runs"
    runs.mkdir(parents=True)
    for index in range(EXPECTED_RUN_COUNT):
        _write(runs / f"run-{index:02d}.json", f'{{"run":{index}}}\n'.encode())

    for name in REQUIRED_FINAL_FILES:
        _write(root / name, f"{name}\n".encode())

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

    manifest = {
        "version": "1.2",
        "root": "data/pilot",
        "finalization_gate": {
            "expected_run_record_count": EXPECTED_RUN_COUNT,
            "required_final_files": sorted(REQUIRED_FINAL_FILES),
            "status": "complete",
        },
        "files": entries,
        "file_count": len(entries),
        "run_record_count": EXPECTED_RUN_COUNT,
    }
    manifest_path = root / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def test_artifact_manifest_verification_requires_all_30_runs_and_final_files(tmp_path: Path):
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
    payload["files"] = [entry for entry in payload["files"] if not entry["path"].startswith("runs/run-29")]
    payload["file_count"] = len(payload["files"])
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate(tmp_path, manifest_path)
    assert any("exactly 30 run JSON files" in error for error in errors)


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
