#!/usr/bin/env python3
"""Generate a frozen, cross-project metadata-only technical screening matrix.

The matrix is derived from the first N rows of the already-frozen 120-case
cohort. It never accepts a case, executes tests, or authorizes model inference.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-f]{64}$")
KNOWN_PRIOR_EXPOSURE_IDS = {
    # First historical cohort used during workflow debugging.
    "BugsInPy-ansible-1", "BugsInPy-black-3", "BugsInPy-cookiecutter-2",
    "BugsInPy-fastapi-2", "BugsInPy-httpie-2", "BugsInPy-keras-1",
    "BugsInPy-luigi-2", "BugsInPy-matplotlib-1",
    # V2 batch used to diagnose missing pytest / setup-state issues.
    "BugsInPy-pandas-1", "BugsInPy-PySnooper-2", "BugsInPy-sanic-2",
    "BugsInPy-scrapy-2", "BugsInPy-spacy-1", "BugsInPy-thefuck-2",
    "BugsInPy-tornado-2", "BugsInPy-tqdm-2",
    # V3 batch used to diagnose metadata parsing and runner bootstrap.
    "BugsInPy-youtube-dl-2", "BugsInPy-ansible-2", "BugsInPy-black-4",
    "BugsInPy-cookiecutter-3", "BugsInPy-fastapi-3", "BugsInPy-httpie-3",
    "BugsInPy-keras-2", "BugsInPy-luigi-3",
    # V4 batch used to inspect test dependency / runner behavior.
    "BugsInPy-matplotlib-2", "BugsInPy-pandas-2", "BugsInPy-PySnooper-3",
    "BugsInPy-sanic-3", "BugsInPy-scrapy-3", "BugsInPy-spacy-2",
    "BugsInPy-thefuck-3", "BugsInPy-tornado-3",
    # V5 first-eight batch used to validate the technical screening workflow.
    "BugsInPy-tqdm-3", "BugsInPy-youtube-dl-3", "BugsInPy-ansible-3",
    "BugsInPy-black-5", "BugsInPy-cookiecutter-4", "BugsInPy-fastapi-4",
    "BugsInPy-httpie-4", "BugsInPy-keras-3",
}
COMMIT = re.compile(r"^[0-9a-fA-F]{7,64}$")
REQUIRED = {
    "queue_rank", "project_round", "screening_batch", "case_id", "project",
    "bug_id", "source_repository", "python_version", "buggy_commit_id",
    "fixed_commit_id", "run_test_sha256", "bug_info_sha256", "project_info_sha256",
    "test_file", "run_test_command", "metadata_complete", "accepted_for_confirmatory",
    "permanently_excluded_feasibility_case",
}


def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()


def prepare(queue_path, cohort_path, matrix_path, summary_path, batch_size=8):
    queue_path=Path(queue_path)
    cohort_path=Path(cohort_path)
    with queue_path.open("r",newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames or []
        missing=sorted(REQUIRED-set(fields))
        if missing:
            raise ValueError("Queue missing required columns: "+", ".join(missing))
        queue=list(reader)
    cohort=json.loads(cohort_path.read_text(encoding="utf-8"))
    allowed_record_types = {
        "metadata_only_predeclared_case_screening_order_not_confirmatory_dataset",
        "metadata_only_screening_intake_not_confirmatory_dataset",
    }
    if cohort.get("record_type") not in allowed_record_types:
        raise ValueError("Cohort is not declared as a metadata-only screening order")
    if cohort.get("accepted_confirmatory_cases") != 0 or cohort.get("llm_inference_performed") is not False:
        raise ValueError("Cohort acceptance/inference flags are not fail-closed")
    actual_queue_sha=sha256_file(queue_path)
    # Cohort v1 and v2 used different field names. Support both while always
    # checking the actual file digest against the recorded value.
    expected_queue_sha = cohort.get("source_queue_csv_sha256") or cohort.get("source_queue_sha256")
    if actual_queue_sha != expected_queue_sha:
        raise ValueError("Queue CSV hash does not match the frozen cohort provenance")
    ids=cohort.get("case_ids")
    if not isinstance(ids,list) or len(ids) < batch_size or len(ids) != len(set(ids)):
        raise ValueError("Frozen cohort IDs are missing, duplicated, or smaller than requested batch")
    if cohort.get("cohort_size") != len(ids):
        raise ValueError("Frozen cohort_size does not match case_ids length")

    if cohort.get("record_type") == "metadata_only_predeclared_case_screening_order_not_confirmatory_dataset":
        exposed_in_historical = sorted(set(ids) & KNOWN_PRIOR_EXPOSURE_IDS)
        if exposed_in_historical:
            raise ValueError("Historical cohort contains cases permanently excluded after workflow debugging; use the exposure-clean v2 cohort: " + ", ".join(exposed_in_historical))

    # Cohort v1 is the exact queue prefix. Cohort v2 may skip only IDs
    # explicitly documented as permanently exposed before model inference.
    queue_ids=[r["case_id"] for r in queue]
    excluded=cohort.get("excluded_prior_exposure", [])
    if not isinstance(excluded, list) or len(excluded) != len(set(excluded)):
        raise ValueError("Prior-exposure exclusion list is malformed or duplicated")
    if set(ids) & set(excluded):
        raise ValueError("A prior-exposed ID appears in the active screening cohort")
    missing_excluded=set(excluded)-set(queue_ids)
    if missing_excluded:
        raise ValueError("Excluded prior-exposure IDs are absent from the source queue: "+", ".join(sorted(missing_excluded)))
    eligible_queue=[r for r in queue if r["case_id"] not in set(excluded)]
    eligible_ids=[r["case_id"] for r in eligible_queue]
    if eligible_ids[:len(ids)] != ids:
        raise ValueError("Frozen cohort IDs do not match the deterministic queue after documented exposure exclusions")
    selected=eligible_queue[:batch_size]
    if len({r["project"] for r in selected}) != batch_size:
        raise ValueError("The initial screening batch must cover one distinct upstream project per case")

    matrix=[]
    for row in selected:
        if row.get("metadata_complete","").lower() != "true":
            raise ValueError("Selected queue row is not metadata complete: "+row["case_id"])
        if row.get("permanently_excluded_feasibility_case","").lower() == "true":
            raise ValueError("A permanently excluded case appears in the queue: "+row["case_id"])
        if row.get("accepted_for_confirmatory","").lower() == "true":
            raise ValueError("Queue cannot pre-accept a case: "+row["case_id"])
        py=row.get("python_version","").strip()
        buggy=row.get("buggy_commit_id","").strip()
        fixed=row.get("fixed_commit_id","").strip()
        run_hash=row.get("run_test_sha256","").strip().lower()
        if not py or not buggy or not fixed or buggy==fixed or not COMMIT.fullmatch(buggy) or not COMMIT.fullmatch(fixed):
            raise ValueError("Invalid runtime/commit metadata: "+row["case_id"])
        if not HEX64.fullmatch(run_hash):
            raise ValueError("Invalid run_test SHA-256: "+row["case_id"])
        raw_commands=[s.strip() for s in row.get("run_test_command","").split(";") if s.strip()]
        if not raw_commands:
            raise ValueError("No declared test command for "+row["case_id"])
        execution_commands=[]
        for command in raw_commands:
            # BugsInPy records tox invocations without limiting tox's env matrix.
            # Constrain only these to the metadata Python major/minor so that
            # unrelated unavailable interpreters do not become case outcomes.
            if command.startswith("tox "):
                minor="py"+ "".join(py.split(".")[:2])
                execution_commands.append("tox -e "+minor+" -- "+command[len("tox "):].strip())
            else:
                execution_commands.append(command)
        matrix.append({
            "queue_rank": int(row["queue_rank"]),
            "case_id": row["case_id"],
            "project": row["project"],
            "bug_id": row["bug_id"],
            "source_repository": row["source_repository"],
            "python_version": py,
            "buggy_commit": buggy,
            "fixed_commit": fixed,
            "run_test_sha256": run_hash,
            "bug_info_sha256": row["bug_info_sha256"],
            "project_info_sha256": row["project_info_sha256"],
            "test_file": row["test_file"],
            "raw_test_commands": raw_commands,
            "execution_test_commands": execution_commands,
            "install_worktree_package": row["project"].lower()=="black",
            "expected_setup_sha256": row.get("setup_sha256",""),
        })

    summary={
        "purpose":"first fixed technical-screening batch from a predeclared 120-case queue; metadata only",
        "source_queue_sha256":actual_queue_sha,
        "source_cohort_sha256":sha256_file(cohort_path),
        "cohort_size":len(ids),
        "batch_size":batch_size,
        "case_ids":[x["case_id"] for x in matrix],
        "upstream_projects":[x["project"] for x in matrix],
        "distinct_upstream_projects":len({x["project"] for x in matrix}),
        "test_pairs_executed_by_matrix_builder":0,
        "accepted_confirmatory_cases":0,
        "llm_inference_performed":False,
        "notes":[
            "The selection order is frozen before test results are observed.",
            "This batch is not a random sample and not a confirmatory dataset.",
            "If a case fails setup or target-test validation, record the reason; do not silently replace it with an easier case.",
            "Any candidate whose metadata/test/patch is opened for workflow debugging is permanently excluded from the confirmatory sample.",
        ],
    }
    Path(matrix_path).write_text(json.dumps({"include":matrix},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    Path(summary_path).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"matrix":{"include":matrix},"summary":summary}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--queue",required=True,type=Path)
    p.add_argument("--cohort",required=True,type=Path)
    p.add_argument("--matrix-output",required=True,type=Path)
    p.add_argument("--summary-output",required=True,type=Path)
    p.add_argument("--batch-size",type=int,default=8)
    a=p.parse_args(argv)
    if a.batch_size < 1:
        p.error("--batch-size must be at least one")
    result=prepare(a.queue,a.cohort,a.matrix_output,a.summary_output,a.batch_size)
    print(json.dumps(result["summary"],ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
