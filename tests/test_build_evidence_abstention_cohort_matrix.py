import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"build_evidence_abstention_cohort_matrix.py"
SPEC=importlib.util.spec_from_file_location("cohort_matrix",SCRIPT)
MODULE=importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

FIELDS=[
"queue_rank","project_round","screening_batch","case_id","project","bug_id",
"source_repository","python_version","buggy_commit_id","fixed_commit_id",
"run_test_sha256","bug_info_sha256","project_info_sha256","test_file","run_test_command",
"metadata_complete","accepted_for_confirmatory","permanently_excluded_feasibility_case","setup_sha256"
]


def row(rank,project,cmd=None,**overrides):
    x={k:"" for k in FIELDS}
    x.update({
      "queue_rank":str(rank),"project_round":str(rank),"screening_batch":"B1",
      "case_id":f"BugsInPy-{project}-{rank}","project":project,"bug_id":str(rank),
      "source_repository":f"https://example.invalid/{project}","python_version":"3.8.3",
      "buggy_commit_id":"a"*40,"fixed_commit_id":"b"*40,"run_test_sha256":"c"*64,
      "bug_info_sha256":"d"*64,"project_info_sha256":"e"*64,"test_file":"tests/test_x.py",
      "run_test_command":cmd or "pytest tests/test_x.py::test_x","metadata_complete":"true",
      "accepted_for_confirmatory":"false","permanently_excluded_feasibility_case":"false"
    })
    x.update(overrides)
    return x


class CohortMatrixTests(unittest.TestCase):
    def setup_files(self,root,rows):
        q=root/"queue.csv"
        with q.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
        ids=[x["case_id"] for x in rows]
        cohort={
          "record_type":"metadata_only_predeclared_case_screening_order_not_confirmatory_dataset",
          "cohort_size":len(ids),"case_ids":ids,
          "source_queue_csv_sha256":hashlib.sha256(q.read_bytes()).hexdigest(),
          "accepted_confirmatory_cases":0,"llm_inference_performed":False
        }
        c=root/"cohort.json";c.write_text(json.dumps(cohort),encoding="utf-8")
        return q,c

    def test_selects_exact_prefix_and_keeps_acceptance_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(i,p) for i,p in enumerate(["a","b","c","d","e"],1)]
            q,c=self.setup_files(root,rows)
            out=MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",3)
            inc=out["matrix"]["include"]
            self.assertEqual([x["case_id"] for x in inc],["BugsInPy-a-1","BugsInPy-b-2","BugsInPy-c-3"])
            self.assertEqual(out["summary"]["distinct_upstream_projects"],3)
            self.assertTrue(all(x["install_worktree_package"] is False for x in inc))
            self.assertEqual(out["summary"]["accepted_confirmatory_cases"],0)
            self.assertFalse(out["summary"]["llm_inference_performed"])

    def test_converts_tox_to_metadata_python_environment(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(1,"cookiecutter","tox tests/test_hooks.py::test_hook"),row(2,"other")]
            q,c=self.setup_files(root,rows)
            out=MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",2)
            self.assertEqual(out["matrix"]["include"][0]["raw_test_commands"],["tox tests/test_hooks.py::test_hook"])
            self.assertEqual(out["matrix"]["include"][0]["execution_test_commands"],["tox -e py38 -- tests/test_hooks.py::test_hook"])

    def test_fails_closed_if_queue_sha_or_order_changes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(1,"a"),row(2,"b")]
            q,c=self.setup_files(root,rows)
            # mutate queue after freezing the cohort hash
            with q.open("a",encoding="utf-8") as f:f.write("\n")
            with self.assertRaisesRegex(ValueError,"Queue CSV hash"):
                MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",2)

    def test_fails_if_selected_cases_repeat_a_project(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(1,"same"),row(2,"same")]
            q,c=self.setup_files(root,rows)
            with self.assertRaisesRegex(ValueError,"distinct upstream project"):
                MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",2)


    def test_v2_skips_only_documented_prior_exposure_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(i,p) for i,p in enumerate(["a","b","c","d","e"],1)]
            q=root/"queue.csv"
            with q.open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
            excluded=["BugsInPy-a-1","BugsInPy-b-2"]
            ids=[x["case_id"] for x in rows if x["case_id"] not in excluded]
            cohort={
                "record_type":"metadata_only_screening_intake_not_confirmatory_dataset",
                "cohort_size":len(ids),
                "case_ids":ids,
                "excluded_prior_exposure":excluded,
                "source_queue_sha256":hashlib.sha256(q.read_bytes()).hexdigest(),
                "accepted_confirmatory_cases":0,
                "llm_inference_performed":False
            }
            c=root/"cohort.json";c.write_text(json.dumps(cohort),encoding="utf-8")
            out=MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",2)
            self.assertEqual([x["case_id"] for x in out["matrix"]["include"]],
                             ["BugsInPy-c-3","BugsInPy-d-4"])
            self.assertEqual(out["summary"]["accepted_confirmatory_cases"],0)
            self.assertFalse(out["summary"]["llm_inference_performed"])

    def test_v2_fails_if_excluded_id_is_reintroduced(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(i,p) for i,p in enumerate(["a","b","c","d"],1)]
            q=root/"queue.csv"
            with q.open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
            excluded=["BugsInPy-a-1"]
            ids=[x["case_id"] for x in rows]
            cohort={
                "record_type":"metadata_only_screening_intake_not_confirmatory_dataset",
                "cohort_size":len(ids),
                "case_ids":ids,
                "excluded_prior_exposure":excluded,
                "source_queue_sha256":hashlib.sha256(q.read_bytes()).hexdigest(),
                "accepted_confirmatory_cases":0,
                "llm_inference_performed":False
            }
            c=root/"cohort.json";c.write_text(json.dumps(cohort),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"prior-exposed ID appears"):
                MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",2)


    def test_historical_cohort_fails_closed_when_it_contains_later_exposed_case(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            rows=[row(1,"ansible"),row(2,"other")]
            q,c=self.setup_files(root,rows)
            cohort=json.loads(c.read_text(encoding="utf-8"))
            cohort["case_ids"][0]="BugsInPy-ansible-1"
            # Keep queue hash intact; this test is specifically about the known
            # exposure guard, not a hash mismatch.
            c.write_text(json.dumps(cohort),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"permanently excluded after workflow debugging"):
                MODULE.prepare(q,c,root/"matrix.json",root/"summary.json",1)


if __name__=="__main__":
    unittest.main()
