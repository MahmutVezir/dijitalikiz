from __future__ import annotations
import json, os, shutil, subprocess, sys, tarfile
from pathlib import Path

ROOT=Path("/kaggle/working")
BUNDLE=ROOT/"project.tar.gz"
SOURCE_COMMIT_FILE=ROOT/"source_commit.txt"
WORKDIR=ROOT/"dijitalikiz"

def run(*args:str,cwd:Path|None=None,env:dict[str,str]|None=None)->None:
    print("$"," ".join(args),flush=True)
    subprocess.run(args,cwd=str(cwd) if cwd else None,env=env,check=True)

if not BUNDLE.is_file():
    raise RuntimeError("Exact-source confirmatory project bundle is missing.")
if WORKDIR.exists(): shutil.rmtree(WORKDIR)
WORKDIR.mkdir(parents=True,exist_ok=True)
with tarfile.open(BUNDLE,"r:gz") as archive:
    archive.extractall(WORKDIR)

source_commit=SOURCE_COMMIT_FILE.read_text(encoding="utf-8").strip() if SOURCE_COMMIT_FILE.exists() else "unknown"
bench=WORKDIR/"data"/"benchmark"
bench.mkdir(parents=True,exist_ok=True)
(bench/"kaggle_source_commit.txt").write_text(source_commit+"\n",encoding="utf-8")

run(sys.executable,"-m","pip","install","-r","requirements-pilot.txt",cwd=WORKDIR)
env=dict(os.environ); env["PYTHONPATH"]=str(WORKDIR)
run(sys.executable,"scripts/capture_environment.py","--output","data/benchmark/environment.json",cwd=WORKDIR,env=env)
env_path=bench/"environment.json"
environment=json.loads(env_path.read_text(encoding="utf-8"))
environment["source_commit"]=source_commit
environment["source_commit_verified_from_bundle"]=True
environment_path=bench/"environment.json"
environment_path.write_text(json.dumps(environment,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

run(sys.executable,"scripts/pilot_preflight.py","--require-cuda",cwd=WORKDIR,env=env)
run(sys.executable,"scripts/model_load_preflight.py",cwd=WORKDIR,env=env)
run(sys.executable,"scripts/audit_confirmatory_integrity.py",cwd=WORKDIR,env=env)
run(sys.executable,"scripts/run_confirmatory.py",cwd=WORKDIR,env=env)
manifest=json.loads((bench/"benchmark_manifest.json").read_text(encoding="utf-8"))
run(sys.executable,"scripts/finalize_confirmatory.py","--runs-dir","data/benchmark/runs","--case-ids",*manifest["case_ids"],cwd=WORKDIR,env=env)

output=ROOT/"confirmatory-output"
if output.exists(): shutil.rmtree(output)
output.mkdir(parents=True,exist_ok=True)
for item in bench.iterdir():
    dest=output/item.name
    if item.is_dir(): shutil.copytree(item,dest)
    else: shutil.copy2(item,dest)

required=("environment.json","confirmatory_evaluation.json","case_level_analysis.json","primary_analysis.json","confirmatory_qa_report.json","confirmatory_records.jsonl","artifact_manifest.json","benchmark_manifest.json")
missing=[str(output/x) for x in required if not (output/x).is_file()]
if missing: raise RuntimeError("Confirmatory finalized but artifacts are missing: "+", ".join(missing))
print(f"Confirmatory experiment completed for source commit {source_commit}.",flush=True)
print(f"Artifacts staged at {output}.",flush=True)
