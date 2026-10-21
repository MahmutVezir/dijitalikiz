import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "analyze_evidence_abstention_rater_agreement.py"
SPEC = importlib.util.spec_from_file_location("evidence_abstention_rater_agreement", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def make_rows(n=360):
    rows=[]
    for i in range(n):
        task=f"opaque-{i:04d}"
        gt_a = "correct" if i % 4 else "partially_correct"
        gt_b = gt_a if i % 5 else ("incorrect" if gt_a != "incorrect" else "correct")
        for reviewer,value in [("gt-a",gt_a),("gt-b",gt_b)]:
            rows.append({"task_id":task,"panel":"ground_truth","rater_id":reviewer,
                         "rating_dimension":"root_cause_accuracy","rating_value":value,
                         "rating_status":"locked_independent"})
        dims={
            "decision":("diagnose" if i%7 else "abstain","diagnose" if i%9 else "invalid_output"),
            "evidence_support":("supported" if i%3 else "unsupported","supported" if i%4 else "partially_supported"),
            "missing_evidence_quality":("not_applicable" if i%5 else "discriminative","not_applicable" if i%6 else "partially_relevant"),
            "unsupported_definitive_diagnosis":("1" if i%11==0 else "0","1" if i%13==0 else "0"),
        }
        for dim,(a,b) in dims.items():
            for reviewer,value in [("ev-a",a),("ev-b",b)]:
                rows.append({"task_id":task,"panel":"evidence_support","rater_id":reviewer,
                             "rating_dimension":dim,"rating_value":value,"rating_status":"locked_independent"})
    return rows


class RaterAgreementTests(unittest.TestCase):
    def test_kappa_known_perfect_and_independent_marginals(self):
        self.assertEqual(MODULE.cohen_kappa(["A","B","A","B"],["A","B","A","B"])[0],1.0)
        self.assertLess(MODULE.cohen_kappa(["A","A","B","B"],["A","B","A","B"])[0],1.0)

    def test_bootstrap_interval_is_deterministic(self):
        rows=make_rows(360)
        result1=MODULE.analyze_rows(rows,minimum_tasks=360,bootstrap_replicates=100,seed=7)
        result2=MODULE.analyze_rows(rows,minimum_tasks=360,bootstrap_replicates=100,seed=7)
        self.assertEqual(result1["dimensions"],result2["dimensions"])
        self.assertTrue(result1["panel_overlap"] is False)
        self.assertEqual(result1["n_tasks_by_dimension"]["root_cause_accuracy"],360)

    def test_rejects_panel_overlap(self):
        rows=make_rows(4)
        for row in rows:
            if row["rater_id"]=="ev-a":
                row["rater_id"]="gt-a"
        with self.assertRaisesRegex(ValueError,"panels must be disjoint"):
            MODULE.analyze_rows(rows,minimum_tasks=4,bootstrap_replicates=100)

    def test_rejects_insufficient_tasks(self):
        with self.assertRaisesRegex(ValueError,"requires 360"):
            MODULE.analyze_rows(make_rows(20),minimum_tasks=360,bootstrap_replicates=100)

    def test_rejects_wrong_panel_for_dimension(self):
        rows=make_rows(4)
        rows[0]["panel"]="evidence_support"
        with self.assertRaisesRegex(ValueError,"must be assigned to panel"):
            MODULE.analyze_rows(rows,minimum_tasks=4,bootstrap_replicates=100)

    def test_requires_locked_independent_scores(self):
        rows=make_rows(4)
        rows[0]["rating_status"]="adjudicated"
        with self.assertRaisesRegex(ValueError,"locked independent ratings"):
            MODULE.analyze_rows(rows,minimum_tasks=4,bootstrap_replicates=100)

    def test_rejects_inconsistent_panel_pairing(self):
        rows=make_rows(4)
        for row in rows:
            if row["task_id"]=="opaque-0003" and row["rating_dimension"]=="root_cause_accuracy" and row["rater_id"]=="gt-a":
                row["rater_id"]="gt-c"
        with self.assertRaisesRegex(ValueError,"reviewer pair changes"):
            MODULE.analyze_rows(rows,minimum_tasks=4,bootstrap_replicates=100)


if __name__ == "__main__":
    unittest.main()
