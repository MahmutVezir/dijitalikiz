from __future__ import annotations
import argparse, json
from pathlib import Path

def main()->int:
    p=argparse.ArgumentParser(description="Export frozen confirmatory run records to deterministic JSONL.")
    p.add_argument("--runs-dir",default="data/benchmark/runs")
    p.add_argument("--output",default="data/benchmark/confirmatory_records.jsonl")
    a=p.parse_args()
    manifest=json.loads(Path("data/benchmark/benchmark_manifest.json").read_text(encoding="utf-8"))
    expected=len(manifest["case_ids"])*2*5
    runs=Path(a.runs_dir)
    records=[json.loads(x.read_text(encoding="utf-8")) for x in sorted(runs.glob("*.json"))]
    if len(records)!=expected:
        raise RuntimeError(f"Expected {expected} confirmatory records; found {len(records)}.")
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8",newline="\n") as f:
        for r in records: f.write(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n")
    print(f"EXPORTED CONFIRMATORY JSONL: {len(records)} records -> {out}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
