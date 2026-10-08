import hashlib
import json

from scripts.validate_pilot_artifact_manifest import validate


def _write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _manifest(root):
    data = json.loads((root / "artifact_manifest.json").read_text(encoding="utf-8"))
    return data


def test_artifact_manifest_verification_passes(tmp_path):
    artifact = tmp_path / "artifact"
    artifact.mkdir()
    raw = b'{"x":1}\n'
    _write(artifact / "runs" / "case.json", raw)

    manifest = {
        "version": "1.2",
        "root": "data/pilot",
        "run_record_count": 30,
        "finalization_gate": {"status": "complete"},
        "files": [{
            "path": "runs/case.json",
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }],
    }
    manifest_path = artifact / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    assert validate(artifact, manifest_path) == []


def test_artifact_manifest_detects_tampering(tmp_path):
    artifact = tmp_path / "artifact"
    artifact.mkdir()
    _write(artifact / "runs" / "case.json", b"original")
    manifest = {
        "run_record_count": 30,
        "finalization_gate": {"status": "complete"},
        "files": [{
            "path": "runs/case.json",
            "bytes": 8,
            "sha256": hashlib.sha256(b"original").hexdigest(),
        }],
    }
    manifest_path = artifact / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _write(artifact / "runs" / "case.json", b"tampered")

    errors = validate(artifact, manifest_path)
    assert any("byte-size mismatch" in error for error in errors)
