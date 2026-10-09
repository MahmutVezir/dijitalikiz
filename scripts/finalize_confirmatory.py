from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

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

    benchmark = Path("data/benchmark")
    manifest = json.loads((benchmark / "benchmark_manifest.json").read_text(encoding="utf-8"))
    evidence_dir = benchmark / "assessments"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for case_id in manifest["case_ids"]:
        source = Path("data/assessments") / f"{case_id}.json"
        if not source.is_file():
            raise RuntimeError(f"Missing frozen candidate assessment: {source}")
        shutil.copy2(source, evidence_dir / source.name)

    supporting_files = [
        (Path("data/pilot/pilot_manifest.json"), benchmark / "pilot_manifest.json"),
        (Path("data/pilot/PROMPT_TEMPLATE.txt"), benchmark / "PROMPT_TEMPLATE.txt"),
        (Path("data/pilot/SYSTEM_PROMPT.txt"), benchmark / "SYSTEM_PROMPT.txt"),
        (Path("data/pilot/model_load_preflight.json"), benchmark / "model_load_preflight.json"),
        (Path("data/pilot/final_candidate_review_2026-10-08.json"), benchmark / "final_pilot_candidate_review.json"),
        (Path("docs/CONTAMINATION_AUDIT.md"), benchmark / "contamination_audit.md"),
        (Path("docs/CONFIRMATORY_SCORING_PROTOCOL.md"), benchmark / "scoring_protocol.md"),
        (Path("docs/PILOT_QA_REVIEW_2026-10-09.md"), benchmark / "pilot_qa_review.md"),
    ]
    for source, destination in supporting_files:
        if not source.is_file():
            raise RuntimeError(f"Missing supporting artifact source: {source}")
        shutil.copy2(source, destination)

    run([sys.executable,"scripts/build_confirmatory_records_jsonl.py","--runs-dir",a.runs_dir])
    run([sys.executable,"scripts/build_confirmatory_artifact_manifest.py","--runs-dir",a.runs_dir])
    print("CONFIRMATORY FINALIZATION COMPLETE",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
