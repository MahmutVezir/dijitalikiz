from __future__ import annotations
import argparse, subprocess, sys

def run(cmd:list[str])->None:
    print("$"," ".join(cmd),flush=True)
    subprocess.run(cmd,check=True)

def main()->int:
    p=argparse.ArgumentParser(description="Finalize frozen confirmatory inference.")
    p.add_argument("--runs-dir",default="data/benchmark/runs")
    p.add_argument("--case-ids",nargs="+",required=True)
    a=p.parse_args()
    run([sys.executable,"scripts/audit_confirmatory_integrity.py","--runs-dir",a.runs_dir,"--require-complete"])
    run([sys.executable,"scripts/evaluate_confirmatory.py","--runs-dir",a.runs_dir])
    run([sys.executable,"scripts/analyze_case_level.py","--evaluation","data/benchmark/confirmatory_evaluation.json","--case-ids",*a.case_ids,"--output","data/benchmark/case_level_analysis.json"])
    run([sys.executable,"scripts/primary_confirmatory_analysis.py"])
    run([sys.executable,"scripts/confirmatory_qa_report.py"])
    run([sys.executable,"scripts/build_confirmatory_records_jsonl.py","--runs-dir",a.runs_dir])
    run([sys.executable,"scripts/build_confirmatory_artifact_manifest.py","--runs-dir",a.runs_dir])
    print("CONFIRMATORY FINALIZATION COMPLETE",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
