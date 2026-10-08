from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

KERNEL_ROOT = Path("/kaggle/working")
SOURCE_DATASET = "mahmutvezir/dijitalikiz-frozen-source-v2"
EXPECTED_SOURCE_COMMIT = "__EXPECTED_SOURCE_COMMIT__"
BUNDLE = KERNEL_ROOT / "project.tar.gz"
WORKDIR = KERNEL_ROOT / "dijitalikiz"
PYTHON_ENV = KERNEL_ROOT / "dijitalikiz-py311"
TARGET_PYTHON = PYTHON_ENV / "bin" / "python"


def run(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=str(cwd) if cwd else None, env=env, check=True)


def output(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def locate_frozen_dataset() -> Path:
    roots = (
        Path("/kaggle/input"),
        Path("/kaggle/working"),
    )
    matches: list[Path] = []

    for root in roots:
        if not root.exists():
            continue
        for bundle_marker in root.rglob("project.tar.gz.b64"):
            candidate = bundle_marker.parent
            if all(
                (candidate / filename).is_file()
                for filename in (
                    "project.tar.gz.b64",
                    "source_bundle_sha256.txt",
                    "source_commit.txt",
                )
            ):
                matches.append(candidate)

    unique_matches = []
    seen = set()
    for candidate in matches:
        resolved = candidate.resolve()
        if resolved not in seen:
            unique_matches.append(resolved)
            seen.add(resolved)

    if len(unique_matches) == 1:
        return unique_matches[0]

    if not unique_matches:
        raise RuntimeError(
            "Frozen source dataset is not mounted with the complete "
            "project.tar.gz.b64 + source_bundle_sha256.txt + source_commit.txt set."
        )

    raise RuntimeError(
        "Multiple complete frozen source dataset payloads were found: "
        + ", ".join(str(path) for path in unique_matches)
    )


dataset_dir = locate_frozen_dataset()

bundle_b64 = dataset_dir / "project.tar.gz.b64"
bundle_sha = dataset_dir / "source_bundle_sha256.txt"
commit_source = dataset_dir / "source_commit.txt"

for required in (bundle_b64, bundle_sha, commit_source):
    if not required.is_file():
        raise RuntimeError(f"Frozen source dataset file is missing: {required}")

payload_b64 = bundle_b64.read_text(encoding="ascii").strip()
try:
    decoded_bundle = base64.b64decode(payload_b64, validate=True)
except Exception as exc:
    raise RuntimeError("Frozen source base64 payload is invalid.") from exc

BUNDLE.write_bytes(decoded_bundle)
expected_bundle_sha = bundle_sha.read_text(encoding="ascii").strip()
actual_bundle_sha = hashlib.sha256(decoded_bundle).hexdigest()
if expected_bundle_sha != actual_bundle_sha:
    raise RuntimeError(
        "Frozen source bundle checksum mismatch: "
        f"expected {expected_bundle_sha}, got {actual_bundle_sha}"
    )

source_commit = commit_source.read_text(encoding="utf-8").strip()
if len(source_commit) != 40 or any(ch not in "0123456789abcdef" for ch in source_commit.lower()):
    raise RuntimeError(f"Invalid frozen source commit marker: {source_commit!r}")

if EXPECTED_SOURCE_COMMIT == "__EXPECTED_SOURCE_COMMIT__":
    raise RuntimeError("Kaggle launcher was not bound to a concrete Git source commit.")
if source_commit != EXPECTED_SOURCE_COMMIT:
    raise RuntimeError(
        "Frozen source commit mismatch: "
        f"launcher expects {EXPECTED_SOURCE_COMMIT}, dataset provides {source_commit}"
    )

print(
    f"Using versioned Kaggle source bundle for commit {source_commit} "
    f"(sha256={actual_bundle_sha})",
    flush=True,
)

if WORKDIR.exists():
    shutil.rmtree(WORKDIR)
WORKDIR.mkdir(parents=True, exist_ok=True)

with tarfile.open(BUNDLE, "r:gz") as archive:
    archive.extractall(WORKDIR)

pilot_dir = WORKDIR / "data" / "pilot"
pilot_dir.mkdir(parents=True, exist_ok=True)
(pilot_dir / "kaggle_source_commit.txt").write_text(
    source_commit + "\n", encoding="utf-8"
)

target_python = ensure_python311()
target_version = output(
    str(target_python),
    "-c",
    "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
)
if target_version != "3.11":
    raise RuntimeError(f"Frozen pilot requires Python 3.11, got {target_version}")

run(
    str(target_python),
    "-m",
    "pip",
    "install",
    "-r",
    "requirements-pilot.txt",
    cwd=WORKDIR,
)

env = dict(os.environ)
env["PYTHONPATH"] = str(WORKDIR)

run(str(target_python), "scripts/capture_environment.py", cwd=WORKDIR, env=env)
environment_path = pilot_dir / "environment.json"
environment = json.loads(environment_path.read_text(encoding="utf-8"))
environment["source_commit"] = source_commit
environment["source_commit_verified_from_kaggle_dataset"] = True
environment_path.write_text(
    json.dumps(environment, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

run(str(target_python), "scripts/pilot_preflight.py", "--require-cuda", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/model_load_preflight.py", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/audit_pilot_integrity.py", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/run_pilot.py", cwd=WORKDIR, env=env)
run(str(target_python), "scripts/finalize_pilot.py", cwd=WORKDIR, env=env)

output_dir = KERNEL_ROOT / "pilot-output"
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

for item in pilot_dir.iterdir():
    destination = output_dir / item.name
    if item.is_dir():
        shutil.copytree(item, destination)
    else:
        shutil.copy2(item, destination)

required = (
    output_dir / "pilot_records.jsonl",
    output_dir / "pilot_evaluation.json",
    output_dir / "case_level_analysis.json",
    output_dir / "pilot_qa_report.json",
    output_dir / "artifact_manifest.json",
)
missing = [str(path) for path in required if not path.is_file()]
if missing:
    raise RuntimeError(
        "Pilot finalized but required artifacts are missing: " + ", ".join(missing)
    )

print(f"Kaggle pilot completed for source commit {source_commit}.", flush=True)
print(f"Pilot artifacts staged at {output_dir}.", flush=True)
