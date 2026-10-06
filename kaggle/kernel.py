import os
import subprocess
import sys

REPO = "https://github.com/MahmutVezir/dijitalikiz.git"
REF = os.environ.get("GITHUB_SHA", "main")
WORKDIR = "/kaggle/working/dijitalikiz"

def run(*args, cwd=None):
    print("$", " ".join(args), flush=True)
    subprocess.run(args, cwd=cwd, check=True)

run("git", "clone", "--depth", "1", REPO, WORKDIR)
# The workflow's pushed kernel is generated from a GitHub commit. The clone
# intentionally follows the repository default branch so the Kaggle runner
# remains usable independently of GitHub Actions environment variables.
run(sys.executable, "-m", "pip", "install", "-r", "requirements-pilot.txt", cwd=WORKDIR)

run(sys.executable, "scripts/capture_environment.py", cwd=WORKDIR)
run(sys.executable, "scripts/audit_pilot_integrity.py", cwd=WORKDIR)
run(sys.executable, "scripts/run_pilot.py", cwd=WORKDIR)
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

print("Kaggle pilot completed.", flush=True)
