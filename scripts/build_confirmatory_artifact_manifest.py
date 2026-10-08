from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def main()->int:
    parser=argparse.ArgumentParser(description="Build immutable confirmatory artifact checksums.")
    parser.add_argument("--runs-dir",default="data/benchmark/runs")
    parser.add_argument("--output",default="data/benchmark/artifact_manifest.json")
    args=parser.parse_args()

    root=Path("data/benchmark"); runs=Path(args.runs_dir)
    manifest=json.loads((root/"benchmark_manifest.json").read_text(encoding="utf-8"))
    cases=manifest["case_ids"]
    expected=len(cases)*2*5
    records=sorted(runs.glob("*.json")) if runs.is_dir() else []
    if len(records)!=expected:
        raise RuntimeError(f"Expected {expected} confirmatory run records; found {len(records)}.")
    required=[Path("environment.json"),Path("confirmatory_evaluation.json"),Path("case_level_analysis.json"),Path("primary_analysis.json"),Path("confirmatory_qa_report.json")]
    missing=[str(root/p) for p in required if not (root/p).is_file()]
    if missing: raise RuntimeError(f"Missing finalized confirmatory artifacts: {missing}")
    files=records+[root/p for p in required]+[root/"benchmark_manifest.json"]
    rel=[p.relative_to(root) for p in files]
    payload={
      "version":"0.1","root":"data/benchmark",
      "finalization_gate":{"expected_run_record_count":expected,"required_final_files":[str(p) for p in required],"status":"complete"},
      "files":[{"path":str(r),"bytes":p.stat().st_size,"sha256":sha256_file(p)} for p,r in zip(files,rel)],
      "run_record_count":len(records)
    }
    payload["file_count"]=len(payload["files"])
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":"pass","run_record_count":len(records),"file_count":len(files),"output":str(out)},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
