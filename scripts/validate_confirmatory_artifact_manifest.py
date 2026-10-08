from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def main()->int:
    p=argparse.ArgumentParser(description="Verify confirmatory artifact checksums.")
    p.add_argument("--artifact-root",default="data/benchmark")
    p.add_argument("--manifest",default="data/benchmark/artifact_manifest.json")
    a=p.parse_args()
    root=Path(a.artifact_root); m=json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    for item in m["files"]:
        path=root/item["path"]
        if not path.is_file(): raise RuntimeError(f"Missing artifact: {path}")
        if path.stat().st_size!=item["bytes"]: raise RuntimeError(f"Size mismatch: {path}")
        if sha256_file(path)!=item["sha256"]: raise RuntimeError(f"Checksum mismatch: {path}")
    expected=m["run_record_count"]
    runs=sorted((root/"runs").glob("*.json"))
    if len(runs)!=expected: raise RuntimeError(f"Run-count mismatch: {len(runs)} != {expected}")
    print(json.dumps({"status":"pass","run_record_count":len(runs),"file_count":m["file_count"]},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
