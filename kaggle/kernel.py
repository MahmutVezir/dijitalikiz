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
(WORKDIR / "data/pilot").mkdir(parents=True, exist_ok=True)
(WORKDIR / "data/pilot/kaggle_source_commit.txt").write_text(source_commit + "\n", encoding="utf-8")

run(sys.executable, "-m", "pip", "install", "-r", "requirements-pilot.txt", cwd=WORKDIR)
run(sys.executable, "scripts/capture_environment.py", cwd=WORKDIR)
run(sys.executable, "scripts/pilot_preflight.py", "--require-cuda", cwd=WORKDIR)
run(sys.executable, "scripts/audit_pilot_integrity.py", cwd=WORKDIR)
run(sys.executable, "scripts/run_pilot.py", cwd=WORKDIR)
run(sys.executable, "scripts/audit_pilot_integrity.py", cwd=WORKDIR)
run(sys.executable, "scripts/evaluate_pilot.py", cwd=WORKDIR)
run(
    sys.executable,
    "scripts/analyze_case_level.py",
    "--evaluation",
    "data/pilot/pilot_evaluation.json",
    "--case-ids",
    "commons-math-defects4j-MATH-927",
    "commons-math-defects4j-MATH-950",
    "commons-math-defects4j-MATH-988",
    "--output",
    "data/pilot/case_level_analysis.json",
    cwd=WORKDIR,
)

print(f"Kaggle pilot completed for source commit {source_commit}.", flush=True)
