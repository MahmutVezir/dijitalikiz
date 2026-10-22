#!/usr/bin/env python3
"""Run one pinned BugsInPy buggy/fixed pair and archive raw evidence; never auto-accept."""
import argparse, hashlib, json, os, platform, re, shlex, shutil, subprocess, sys
from pathlib import Path

DATASET_SHA = "11c5f1eea954a42132cfd06bf257766a7963e0fd"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FAIL = (r"=+ FAILURES =+", r"\b[1-9][0-9]* failed\b", r"\bFAILED\b", r"^FAIL:", r"^ERROR:", r"AssertionError", r"assert .* == .*", r"Traceback \(most recent call last\):")
ENVERR = (r"ModuleNotFoundError", r"No module named", r"ImportError while loading conftest", r"Error loading plugin", r"pytest: command not found", r"command not found", r"No matching distribution found", r"Could not find a version that satisfies", r"Could not build wheels?", r"subprocess-exited-with-error", r"fatal error:", r"gcc: command not found", r"No such file or directory:.*(?:test|fixture)", r"collected 0 items", r"ERROR: file or directory not found")
PASS = (r"\b[1-9][0-9]* passed\b", r"^OK$", r"Ran [1-9][0-9]* tests? in")

def digest(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as f:
        for part in iter(lambda: f.read(1048576), b""): h.update(part)
    return h.hexdigest()

def read(path):
    p = Path(path)
    if not p.is_file(): return ""
    with p.open("r", encoding="utf-8", errors="replace") as f: return f.read()

def info(path):
    out = {}
    for line in read(path).splitlines():
        m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[\"'](.*?)[\"']\s*$", line)
        if m: out[m.group(1)] = m.group(2)
    return out

def run(cmd, cwd, logfile, env=None):
    Path(logfile).parent.mkdir(parents=True, exist_ok=True)
    with open(str(logfile), "wb") as out:
        try: p = subprocess.Popen(cmd, cwd=str(cwd) if cwd else None, env=env, stdout=out, stderr=subprocess.STDOUT); return p.wait()
        except OSError as e: out.write(("PROCESS_START_ERROR: " + repr(e) + "\n").encode("utf-8", "replace")); return 127

def git(cwd, *args):
    try: p = subprocess.run(["git", "-C", str(cwd)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except OSError: return None
    return p.stdout.strip() if p.returncode == 0 else None

def any_match(s, patterns): return any(re.search(p, s, re.I | re.M) for p in patterns)

def freeze_normalized(path, root):
    lines=[]
    for line in read(path).splitlines():
        line=line.replace(str(root), "<WORK_ROOT>")
        line=re.sub(r"file://[^ ]+", "file://<LOCAL_PATH>", line)
        line=re.sub(r"(?i)(-e\s+)(?:[^ ]+)", r"\1<EDITABLE_PROJECT>", line)
        if line.strip(): lines.append(line.strip())
    return "\n".join(sorted(lines))+"\n"

def finish(root, rec):
    (root/"summary.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    rows=[]
    for side in ("buggy","fixed"):
        x=rec.get(side,{})
        rows.append("| %s | %s | %s | %s | %s | %s |" % (side, x.get("setup_completed",False), x.get("actual_head",""), x.get("target_test_exit_code","not run"), x.get("test_failure_signature_present",False), x.get("pass_marker_present",False)))
    lines=["# Minimum Technical Validation Report","","- Case: %s" % rec.get("case_id"),"- Pair status: %s" % rec.get("technical_pair_status"),"- Confirmatory acceptance: NO; manual review only.","- Model inference performed: false","","## Gate checks","","- Source hashes verified: %s" % rec.get("source_hashes_verified"),"- Both environments setup completed: %s" % rec.get("both_setup_completed"),"- Both Python runtimes match metadata: %s" % rec.get("both_runtimes_match_metadata"),"- Dependency snapshots match: %s" % rec.get("dependency_fingerprints_match"),"- Fixed tree intersects patch paths: %s" % rec.get("fixed_tree_matches_patch_paths"),"- Buggy-fail/fixed-pass raw markers: %s" % rec.get("raw_buggy_fail_fixed_pass_signals_present"),"- Environment/harness error marker: %s" % rec.get("environment_or_harness_error_present"),"","## Raw results","","| Side | Setup complete | HEAD | Test exit | Failure marker | Pass marker |","|---|---:|---|---:|---:|---:|"]+rows+["","## Blockers",""]
    lines += ["- "+b for b in rec.get("blockers",[])] if rec.get("blockers") else ["- No automated blockers detected. Manual root-cause, source-diff, license, independence, and evidence-sufficiency review remains mandatory."]
    lines += ["","Automated exit codes and output markers alone do not prove that the code defect caused the failure. Inspect raw logs, test assertion/traceback, patch diff, runtime/dependency snapshots and license before any research use.",""]
    (root/"minimum-validation-report.md").write_text("\n".join(lines), encoding="utf-8")
    (root/"preflight-blockers.txt").write_text("\n".join(rec.get("blockers",[]))+"\n", encoding="utf-8")
    def sums(): return [digest(p)+"  ./"+p.name for p in sorted(root.iterdir()) if p.is_file() and p.name not in ("SHA256SUMS","checksum-audit.json")]
    (root/"SHA256SUMS").write_text("\n".join(sums())+"\n", encoding="utf-8")
    audit=[]
    for line in read(root/"SHA256SUMS").splitlines():
        expected,name=line.split("  ",1); p=root/name[2:]; actual=digest(p)
        audit.append({"file":name[2:],"expected_sha256":expected,"observed_sha256":actual,"matches":expected==actual})
    (root/"checksum-audit.json").write_text(json.dumps({"all_match":all(x["matches"] for x in audit),"files":audit,"accepted_for_confirmatory":False},indent=2)+"\n",encoding="utf-8")
    lines=[digest(p)+"  ./"+p.name for p in sorted(root.iterdir()) if p.is_file() and p.name!="SHA256SUMS"]
    (root/"SHA256SUMS").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return 0

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--dataset-root",required=True,type=Path); ap.add_argument("--artifact-dir",required=True,type=Path); ap.add_argument("--work-root",required=True,type=Path); a=ap.parse_args()
    ds=a.dataset_root.resolve(); out=a.artifact_dir.resolve(); root=a.work_root.resolve(); out.mkdir(parents=True,exist_ok=True); root.mkdir(parents=True,exist_ok=True)
    envvars={"case_id":"CASE_ID","project":"PROJECT","bug_id":"BUG_ID","python":"EXPECTED_PYTHON","buggy":"EXPECTED_BUGGY","fixed":"EXPECTED_FIXED","bug_info_sha256":"BUG_INFO_SHA256","project_info_sha256":"PROJECT_INFO_SHA256","run_test_sha256":"RUN_TEST_SHA256","patch_sha256":"PATCH_SHA256"}
    c={k:os.environ.get(v,"") for k,v in envvars.items()}; blockers=[]
    rec={"case_id":c["case_id"],"dataset":"BugsInPy","dataset_revision_expected":DATASET_SHA,"dataset_revision_observed":git(ds,"rev-parse","HEAD"),"technical_triage_only":True,"accepted_for_confirmatory":False,"confirmatory_eligible":False,"llm_inference_performed":False,"manual_review_required":True,"blockers":blockers,"warnings":["Hand-targeted candidates are technical triage only, not a confirmatory sample.","Output signatures require human root-cause review.","Absence of public training-data contamination cannot be proven."]}
    if rec["dataset_revision_observed"]!=DATASET_SHA: blockers.append("Pinned BugsInPy revision mismatch")
    pd=ds/"projects"/c["project"]; bd=pd/"bugs"/c["bug_id"]
    src={"bug.info":bd/"bug.info","project.info":pd/"project.info","run_test.sh":bd/"run_test.sh","bug_patch.txt":bd/"bug_patch.txt"}
    expected={"bug.info":c["bug_info_sha256"],"project.info":c["project_info_sha256"],"run_test.sh":c["run_test_sha256"],"bug_patch.txt":c["patch_sha256"]}
    hashes={}; meta={}
    for name,p in src.items():
        if not p.is_file(): blockers.append("Missing raw source: "+name); continue
        observed=digest(p); ok=bool(HEX64.fullmatch(expected[name])) and observed==expected[name]; hashes[name]={"sha256":observed,"expected_sha256":expected[name],"matches":ok}
        if not ok: blockers.append("Raw source SHA-256 mismatch: "+name)
        shutil.copy2(str(p),str(out/name))
        if name in ("bug.info","project.info"): meta[name]=info(p)
    rec["source_hashes"]=hashes; rec["source_hashes_verified"]=len(hashes)==4 and all(x["matches"] for x in hashes.values())
    bi=meta.get("bug.info",{}); pi=meta.get("project.info",{}); py=bi.get("python_version",""); bug=bi.get("buggy_commit_id",""); fixed=bi.get("fixed_commit_id",""); pp=bi.get("pythonpath",pi.get("pythonpath",""))
    rec.update({"source_repository":pi.get("github_url",""),"dataset_recorded_python":py,"buggy_commit_from_metadata":bug,"fixed_commit_from_metadata":fixed,"pythonpath_metadata":pp})
    if py!=c["python"] or bug!=c["buggy"] or fixed!=c["fixed"]: blockers.append("Raw bug.info metadata mismatch")
    cmds=[x.strip() for x in read(src["run_test.sh"]).splitlines() if x.strip() and not x.lstrip().startswith("#")]
    cmd=cmds[0] if len(cmds)==1 else None; rec["target_test_command"]=cmd
    if cmd is None: blockers.append("run_test.sh must contain one command")
    if rec["dataset_revision_observed"]!=DATASET_SHA or blockers or cmd is None:
        rec.update({"technical_pair_status":"NOT_VALIDATED","technical_pair_signal_present":False,"blockers":sorted(set(blockers))}); return finish(out,rec)
    rec["controller_python_observed"]=platform.python_version()
    if platform.python_version()!=py: blockers.append("Active Python version differs from pinned metadata")
    patch_paths=sorted(set(re.findall(r"^diff --git a/(.*?) b/",read(src["bug_patch.txt"]),re.M))); rec["patch_paths"]=patch_paths
    (out/"patch-paths.txt").write_text("\n".join(patch_paths)+"\n",encoding="utf-8")
    framework=ds/"framework"/"bin"; base=os.environ.copy(); base["PATH"]=str(framework)+os.pathsep+base.get("PATH",""); sides={}
    for side,version in (("buggy","0"),("fixed","1")):
        side_root=root/side; side_root.mkdir(parents=True,exist_ok=True)
        cr=run(["bugsinpy-checkout","-p",c["project"],"-i",c["bug_id"],"-v",version,"-w",str(side_root)],ds,out/(side+"-checkout.log"),base); tree=side_root/c["project"]
        s={"checkout_exit_code":cr,"setup_completed":False}; sides[side]=s
        if cr or not tree.is_dir(): blockers.append(side+" checkout failed; target test not run"); (out/(side+"-status.txt")).write_text("checkout failed; no test result\n",encoding="utf-8"); continue
        head=git(tree,"rev-parse","HEAD"); changed=git(tree,"diff","--name-only") or ""; df=subprocess.run(["git","-C",str(tree),"diff","--binary"],stdout=subprocess.PIPE,stderr=subprocess.PIPE); diff=df.stdout if df.returncode==0 else b""
        if side=="fixed" and head==c["fixed"]:
            changed=git(tree,"diff","--name-only",c["buggy"]+".."+c["fixed"]) or ""; df=subprocess.run(["git","-C",str(tree),"diff","--binary",c["buggy"]+".."+c["fixed"]],stdout=subprocess.PIPE,stderr=subprocess.PIPE); diff=df.stdout if df.returncode==0 else b""
        paths=sorted(x for x in changed.splitlines() if x); s.update({"actual_head":head,"changed_paths":paths,"diff_sha256":hashlib.sha256(diff).hexdigest()})
        (out/(side+"-actual-head.txt")).write_text((head or "")+"\n",encoding="utf-8"); (out/(side+"-changed-paths.txt")).write_text("\n".join(paths)+"\n",encoding="utf-8"); (out/(side+"-diff.sha256")).write_text(s["diff_sha256"]+"\n",encoding="utf-8")
        if side=="buggy" and head!=c["buggy"]: blockers.append("Buggy HEAD does not equal recorded buggy commit")
        if side=="fixed":
            intersects=bool(set(paths).intersection(patch_paths)); s["fixed_tree_valid"]=head==c["fixed"] or (head==c["buggy"] and intersects and bool(diff)); s["fixed_tree_matches_patch_paths"]=intersects
            if not s["fixed_tree_valid"]: blockers.append("Fixed tree is not pinned fixed commit or patched buggy base")
            if not intersects: blockers.append("Fixed diff does not touch bug_patch.txt paths")
        compile_rc=run(["env","-u","SHELLOPTS","-u","BASH_ENV","bash","--noprofile","--norc",str(framework/"bugsinpy-compile")],tree,out/(side+"-compile.log"),base)
        s["compile_exit_code"]=compile_rc; s["setup_completed"]=compile_rc==0 and (tree/"bugsinpy_compile_flag").is_file() and (tree/"env"/"bin"/"activate").is_file()
        if not s["setup_completed"]: blockers.append(side+" compile/setup failed; test not counted"); (out/(side+"-status.txt")).write_text("setup failed; target test not counted\n",encoding="utf-8"); continue
        activation="set +u; source env/bin/activate nondestructive; "
        s["runtime_fingerprint_exit_code"]=run(["bash","-c",activation+"python --version; python -c 'import platform,sys; print(\"executable=\"+sys.executable); print(\"platform=\"+platform.platform())'"],tree,out/(side+"-runtime-fingerprint.txt"),base)
        m=re.search(r"^Python (\d+\.\d+\.\d+)$",read(out/(side+"-runtime-fingerprint.txt")),re.M); s["runtime_python_observed"]=m.group(1) if m else None
        if s["runtime_fingerprint_exit_code"] or s["runtime_python_observed"]!=py: blockers.append(side+" virtualenv Python does not match metadata")
        pypaths=[str(tree)]
        if pp:
            q=Path(pp); q=q if q.is_absolute() else tree/q; pypaths.insert(0,str(q))
        if base.get("PYTHONPATH"): pypaths.append(base["PYTHONPATH"])
        if "pytest" in cmd and not re.search(r"python(?:3)?\s+-m\s+pytest",cmd):
            pre=run(["bash","-c",activation+"python -m pytest --version"],tree,out/(side+"-pytest-preflight.log"),base)
            if pre:
                pr=run(["bash","-c",activation+"python -m pip install --disable-pip-version-check pytest==6.2.5 && python -m pytest --version"],tree,out/(side+"-pytest-bootstrap.log"),base); s["pytest_bootstrap_exit_code"]=pr
                if pr: blockers.append(side+" pytest install failed; target test not counted"); continue
        fr=run(["bash","-c",activation+"python -m pip freeze"],tree,out/(side+"-pip-freeze.txt"),base); s["pip_freeze_exit_code"]=fr
        norm=freeze_normalized(out/(side+"-pip-freeze.txt"),root); (out/(side+"-pip-freeze-normalized.txt")).write_text(norm,encoding="utf-8"); s["pip_freeze_sha256"]=digest(out/(side+"-pip-freeze.txt")); s["normalized_pip_freeze_sha256"]=digest(out/(side+"-pip-freeze-normalized.txt"))
        if fr: blockers.append(side+" pip freeze failed")
        env=base.copy(); env["PYTHONPATH"]=os.pathsep.join(pypaths)
        tr=run(["bash","-c",activation+"export PYTHONPATH="+shlex.quote(env["PYTHONPATH"])+"; exec bash -c "+shlex.quote(cmd)],tree,out/(side+"-test.log"),env); log=read(out/(side+"-test.log"))
        s.update({"target_test_exit_code":tr,"test_failure_signature_present":tr!=0 and any_match(log,FAIL),"pass_marker_present":tr==0 and any_match(log,PASS),"environment_or_harness_error_present":any_match(log,ENVERR)})
        (out/(side+"-status.txt")).write_text("checkout_exit="+str(cr)+"\ncompile_exit="+str(compile_rc)+"\ntarget_test_exit="+str(tr)+"\ntest_failure_signature="+str(s["test_failure_signature_present"]).lower()+"\npass_marker="+str(s["pass_marker_present"]).lower()+"\nenvironment_or_harness_error="+str(s["environment_or_harness_error_present"]).lower()+"\n",encoding="utf-8")
    b=sides.get("buggy",{}); f=sides.get("fixed",{}); both=b.get("setup_completed") is True and f.get("setup_completed") is True
    runtimes=b.get("runtime_python_observed")==py and f.get("runtime_python_observed")==py
    dep=(out/"buggy-pip-freeze-normalized.txt").is_file() and (out/"fixed-pip-freeze-normalized.txt").is_file() and read(out/"buggy-pip-freeze-normalized.txt")==read(out/"fixed-pip-freeze-normalized.txt")
    raw=b.get("target_test_exit_code") not in (None,0) and b.get("test_failure_signature_present") is True and f.get("target_test_exit_code")==0 and f.get("pass_marker_present") is True
    env_error=b.get("environment_or_harness_error_present") is True or f.get("environment_or_harness_error_present") is True
    patch_match=f.get("fixed_tree_matches_patch_paths") is True
    signal=rec["source_hashes_verified"] and not blockers and both and runtimes and dep and raw and not env_error and f.get("fixed_tree_valid") is True and patch_match and b.get("pip_freeze_exit_code")==0 and f.get("pip_freeze_exit_code")==0
    rec.update({"buggy":b,"fixed":f,"both_setup_completed":both,"both_runtimes_match_metadata":runtimes,"dependency_fingerprints_match":dep,"raw_buggy_fail_fixed_pass_signals_present":raw,"environment_or_harness_error_present":env_error,"fixed_tree_matches_patch_paths":patch_match,"technical_pair_signal_present":signal,"technical_pair_status":"TECHNICAL_SIGNAL_PRESENT_MANUAL_REVIEW_REQUIRED" if signal else "NOT_VALIDATED","accepted_for_confirmatory":False,"confirmatory_eligible":False,"llm_inference_performed":False,"blockers":sorted(set(blockers))})
    return finish(out,rec)

if __name__=="__main__": sys.exit(main())
