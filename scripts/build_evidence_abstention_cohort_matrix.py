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
    if cohort.get("record_type") != "metadata_only_predeclared_case_screening_order_not_confirmatory_dataset":
        raise ValueError("Cohort is not declared as a metadata-only predeclared screening order")
    if cohort.get("accepted_confirmatory_cases") != 0 or cohort.get("llm_inference_performed") is not False:
        raise ValueError("Cohort acceptance/inference flags are not fail-closed")
    actual_queue_sha=sha256_file(queue_path)
    if actual_queue_sha != cohort.get("source_queue_csv_sha256"):
        raise ValueError("Queue CSV hash does not match the frozen cohort provenance")
    ids=cohort.get("case_ids")
    if not isinstance(ids,list) or len(ids) < batch_size or len(ids) != len(set(ids)):
        raise ValueError("Frozen cohort IDs are missing, duplicated, or smaller than requested batch")
    if cohort.get("cohort_size") != len(ids):
        raise ValueError("Frozen cohort_size does not match case_ids length")

    # Ensure the cohort order is exactly the prefix of the deterministic queue.
    queue_ids=[r["case_id"] for r in queue]
    if queue_ids[:len(ids)] != ids:
        raise ValueError("Frozen cohort IDs do not match the top of the verified queue in order")
    selected=queue[:batch_size]
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
