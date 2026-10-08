from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

KERNEL_ROOT = Path("/kaggle/working")
SOURCE_COMMIT = "SOURCE_COMMIT_PLACEHOLDER"
EMBEDDED_PROJECT_B64 = "PROJECT_B64_PLACEHOLDER"
BUNDLE = KERNEL_ROOT / "project.tar.gz"
WORKDIR = KERNEL_ROOT / "dijitalikiz"


def run(*args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=str(cwd) if cwd else None, env=env, check=True)


# Kaggle's kernel package does not reliably expose arbitrary sidecar files.
# The GitHub Action therefore embeds the exact source archive into this
# launcher. Kaggle never needs credentials for the private GitHub repository.
if SOURCE_COMMIT == "SOURCE_COMMIT_PLACEHOLDER":
    raise RuntimeError("Frozen source commit was not embedded into the Kaggle launcher.")
if EMBEDDED_PROJECT_B64 == "PROJECT_B64_PLACEHOLDER":
    raise RuntimeError("Exact project source was not embedded into the Kaggle launcher.")

try:
    BUNDLE.write_bytes(
        base64.b64decode(EMBEDDED_PROJECT_B64.encode("ascii"), validate=True)
    )
except Exception as exc:
    raise RuntimeError("Embedded exact-source project archive is invalid.") from exc

print(f"Using embedded exact project source: {SOURCE_COMMIT}", flush=True)

if WORKDIR.exists():
    shutil.rmtree(WORKDIR)
WORKDIR.mkdir(parents=True, exist_ok=True)

with tarfile.open(BUNDLE, "r:gz") as archive:
    archive.extractall(WORKDIR)

source_commit = SOURCE_COMMIT
pilot_dir = WORKDIR / "data" / "pilot"
pilot_dir.mkdir(parents=True, exist_ok=True)
(pilot_dir / "kaggle_source_commit.txt").write_text(
    source_commit + "\n", encoding="utf-8"
)

run(sys.executable, "-m", "pip", "install", "-r", "requirements-pilot.txt", cwd=WORKDIR)

env = dict(os.environ)
env["PYTHONPATH"] = str(WORKDIR)

run(sys.executable, "scripts/capture_environment.py", cwd=WORKDIR, env=env)
environment_path = pilot_dir / "environment.json"
environment = json.loads(environment_path.read_text(encoding="utf-8"))
environment["source_commit"] = source_commit
environment["source_commit_verified_from_embedded_bundle"] = True
environment_path.write_text(
    json.dumps(environment, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

run(sys.executable, "scripts/pilot_preflight.py", "--require-cuda", cwd=WORKDIR, env=env)
run(sys.executable, "scripts/model_load_preflight.py", cwd=WORKDIR, env=env)
run(sys.executable, "scripts/audit_pilot_integrity.py", cwd=WORKDIR, env=env)
run(sys.executable, "scripts/run_pilot.py", cwd=WORKDIR, env=env)
run(sys.executable, "scripts/finalize_pilot.py", cwd=WORKDIR, env=env)

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
