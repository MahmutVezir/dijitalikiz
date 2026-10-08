from __future__ import annotations

import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

KERNEL_ROOT = Path("/kaggle/working")
BUNDLE = KERNEL_ROOT / "project.tar.gz"
SOURCE_COMMIT_FILE = KERNEL_ROOT / "source_commit.txt"
WORKDIR = KERNEL_ROOT / "dijitalikiz"


def run(*args: str, cwd: Path | None = None) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=str(cwd) if cwd else None, check=True)


if not BUNDLE.is_file():
    raise RuntimeError("Exact-source project bundle is missing from the Kaggle kernel package.")

if WORKDIR.exists():
    shutil.rmtree(WORKDIR)
WORKDIR.mkdir(parents=True, exist_ok=True)

with tarfile.open(BUNDLE, "r:gz") as archive:
    archive.extractall(WORKDIR)

source_commit = SOURCE_COMMIT_FILE.read_text(encoding="utf-8").strip() if SOURCE_COMMIT_FILE.exists() else "unknown"
(WORKDIR / "data/pilot/kaggle_source_commit.txt").write_text(source_commit + "\n", encoding="utf-8")
(WORKDIR / "data/pilot").mkdir(parents=True, exist_ok=True)

run(sys.executable, "-m", "pip", "install", "-r", "requirements-pilot.txt", cwd=WORKDIR)
run(sys.executable, "scripts/capture_environment.py", cwd=WORKDIR)
# The bundle is not a Git checkout, so restore the exact source commit into environment metadata.
environment_path = WORKDIR / "data/pilot/environment.json"
environment = __import__("json").loads(environment_path.read_text(encoding="utf-8"))
environment["source_commit"] = source_commit
environment["source_commit_verified_from_bundle"] = True
environment_path.write_text(__import__("json").dumps(environment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
run(sys.executable, "scripts/pilot_preflight.py", "--require-cuda", cwd=WORKDIR)
run(sys.executable, "scripts/model_load_preflight.py", cwd=WORKDIR)
run(sys.executable, "scripts/audit_pilot_integrity.py", cwd=WORKDIR)
run(sys.executable, "scripts/run_pilot.py", cwd=WORKDIR)
run(sys.executable, "scripts/run_pilot.py", cwd=WORKDIR)
run(sys.executable, "scripts/finalize_pilot.py", cwd=WORKDIR)

output_dir = KERNEL_ROOT / "pilot-output"
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)
source_pilot_dir = WORKDIR / "data" / "pilot"
for item in source_pilot_dir.iterdir():
    destination = output_dir / item.name
    if item.is_dir():
        shutil.copytree(item, destination)
    else:
        shutil.copy2(item, destination)

print(f"Kaggle pilot completed for source commit {source_commit}.", flush=True)
print(f"Pilot artifacts staged at {output_dir}.", flush=True)
