from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_RUN_COUNT = 30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(artifact_root: Path, manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"manifest unreadable: {type(exc).__name__}: {exc}"]

    if manifest.get("finalization_gate", {}).get("status") != "complete":
        errors.append("manifest finalization_gate.status must be complete")
    if manifest.get("run_record_count") != EXPECTED_RUN_COUNT:
        errors.append(
            f"manifest run_record_count must be {EXPECTED_RUN_COUNT}, got {manifest.get('run_record_count')!r}"
        )

    entries = manifest.get("files", [])
    if not isinstance(entries, list):
        return errors + ["manifest files must be a list"]

    for entry in entries:
        rel = entry.get("path")
        if not isinstance(rel, str) or not rel:
            errors.append("manifest contains an invalid file path entry")
            continue
        path = artifact_root / rel
        if not path.is_file():
            errors.append(f"missing artifact file: {path}")
            continue
        expected_bytes = entry.get("bytes")
        if path.stat().st_size != expected_bytes:
            errors.append(f"byte-size mismatch: {rel}")
        expected_sha = entry.get("sha256")
        if path.stat().st_size == expected_bytes and sha256_file(path) != expected_sha:
            errors.append(f"sha256 mismatch: {rel}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify a completed frozen pilot artifact against its SHA-256 manifest."
    )
    parser.add_argument("--artifact-root", default="data/pilot")
    parser.add_argument("--manifest", default="data/pilot/artifact_manifest.json")
    args = parser.parse_args()

    errors = validate(Path(args.artifact_root), Path(args.manifest))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALID PILOT ARTIFACT: {args.artifact_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
