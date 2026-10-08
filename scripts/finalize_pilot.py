from __future__ import annotations

import argparse
import subprocess
import sys


DEFAULT_CASES = (
    "commons-math-defects4j-MATH-927",
    "commons-math-defects4j-MATH-950",
    "commons-math-defects4j-MATH-988",
)


def run(command: list[str]) -> None:
    print("$", " ".join(command), flush=True)
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Finalize a completed frozen pilot without invoking the model."
    )
    parser.add_argument("--runs-dir", default="data/pilot/runs")
    parser.add_argument("--case-ids", nargs="+", default=list(DEFAULT_CASES))
    args = parser.parse_args()

    run([sys.executable, "scripts/audit_pilot_integrity.py",
         "--runs-dir", args.runs_dir, "--require-complete"])
    run([sys.executable, "scripts/evaluate_pilot.py",
         "--runs-dir", args.runs_dir])
    run([
        sys.executable, "scripts/analyze_case_level.py",
        "--evaluation", "data/pilot/pilot_evaluation.json",
        "--case-ids", *args.case_ids,
        "--output", "data/pilot/case_level_analysis.json",
    ])
    run([sys.executable, "scripts/pilot_qa_report.py"])
    run([sys.executable, "scripts/build_pilot_artifact_manifest.py",
         "--runs-dir", args.runs_dir])

    print("PILOT FINALIZATION COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
