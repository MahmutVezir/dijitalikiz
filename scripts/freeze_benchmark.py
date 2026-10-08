from __future__ import annotations
import argparse,json
from pathlib import Path

from scripts.validate_benchmark_manifest import validate_manifest

ROOT=Path(".")
REQUIRED_PILOT_FILES=("pilot_records.jsonl","pilot_evaluation.json","case_level_analysis.json","pilot_qa_report.json","artifact_manifest.json")

def main()->int:
    p=argparse.ArgumentParser(description="Freeze the preselected confirmatory benchmark after pilot completion.")
    p.add_argument("--pilot-artifact-root",required=True,help="Directory containing finalized pilot artifacts.")
    p.add_argument("--manifest",default="data/benchmark/benchmark_manifest.json")
    a=p.parse_args()
    pilot_root=Path(a.pilot_artifact_root)
    missing=[str(pilot_root/x) for x in REQUIRED_PILOT_FILES if not (pilot_root/x).is_file()]
    if missing: raise SystemExit("Pilot finalization artifacts missing: "+", ".join(missing))
    pilot_eval=json.loads((pilot_root/"pilot_evaluation.json").read_text(encoding="utf-8"))
    if pilot_eval.get("status")!="complete" or pilot_eval.get("found_records")!=pilot_eval.get("expected_records") or pilot_eval.get("expected_records")!=30:
        raise SystemExit("Pilot artifact is not complete; confirmatory benchmark cannot freeze.")
    path=Path(a.manifest); manifest=json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("status")!="draft": raise SystemExit("Benchmark manifest is already frozen or invalid.")
    errors=validate_manifest(manifest,ROOT)
    if errors: raise SystemExit("Benchmark draft validation failed: "+" | ".join(errors))
    if len(manifest.get("case_ids",[]))!=manifest["power_assumption"]["required_case_count"]:
        raise SystemExit("Confirmatory case count does not match predeclared power requirement.")
    frozen_candidate=dict(manifest)
    frozen_candidate["status"]="frozen"
    frozen_errors=validate_manifest(frozen_candidate,ROOT)
    if frozen_errors:
        raise SystemExit("Frozen benchmark validation failed: "+" | ".join(frozen_errors))
    manifest["status"]="frozen"
    manifest["freeze_metadata"]={
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "pilot_completion_verified":True,
        "case_selection_model_outputs_consulted":False,
        "freeze_is_non_post_hoc":"true"
    }
    path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":"frozen","case_count":len(manifest["case_ids"])},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
