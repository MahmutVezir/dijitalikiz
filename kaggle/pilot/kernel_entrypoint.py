"""Headless Kaggle entrypoint for the frozen 30-run pilot."""
from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path

REPO = "https://github.com/MahmutVezir/dijitalikiz.git"
REF = os.environ.get("DIJITALIKIZ_REF", "main")
WORK = Path("/kaggle/working")
CHECKOUT = WORK / "dijitalikiz"
OUTPUT = WORK / "dijitalikiz-pilot-output"

def run(*args: str, cwd: Path | None = None) -> None:
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=cwd, check=True)

def main() -> None:
    if CHECKOUT.exists():
        shutil.rmtree(CHECKOUT)
    run("git", "clone", "--depth", "1", REPO, str(CHECKOUT))
    run("git", "fetch", "--depth", "1", "origin", REF, cwd=CHECKOUT)
    run("git", "checkout", "--detach", REF, cwd=CHECKOUT)
    run("python", "-m", "pip", "install", "--upgrade", "pip")
    run("python", "-m", "pip", "install", "-r", "requirements-pilot.txt", cwd=CHECKOUT)
    run("python", "scripts/pilot_preflight.py", cwd=CHECKOUT)
    run("python", "scripts/capture_environment.py", cwd=CHECKOUT)
    run("python", "scripts/audit_pilot_integrity.py", cwd=CHECKOUT)
    run("python", "scripts/run_pilot.py", cwd=CHECKOUT)
    run("python", "scripts/audit_pilot_integrity.py", "--require-complete", cwd=CHECKOUT)
    run("python", "scripts/evaluate_pilot.py", cwd=CHECKOUT)
    run(
        "python", "scripts/analyze_case_level.py",
        "--evaluation", "data/pilot/pilot_evaluation.json",
        "--case-ids",
        "commons-math-defects4j-MATH-927",
        "commons-math-defects4j-MATH-950",
        "commons-math-defects4j-MATH-988",
        "--output", "data/pilot/case_level_analysis.json",
        cwd=CHECKOUT,
    )
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    for name in (
        "pilot_records.jsonl",
        "pilot_evaluation.json",
        "case_level_analysis.json",
        "environment.json",
    ):
        source = CHECKOUT / "data" / "pilot" / name
        if source.exists():
            shutil.copy2(source, OUTPUT / name)
    if not any(OUTPUT.iterdir()):
        raise RuntimeError("Pilot completed but no expected output artifacts were produced.")
    print("KAGGLE_PILOT_OUTPUT_READY", flush=True)

if __name__ == "__main__":
    main()
