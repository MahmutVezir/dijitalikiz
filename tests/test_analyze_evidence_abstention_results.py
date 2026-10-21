import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "analyze_evidence_abstention_results.py"
SPEC = importlib.util.spec_from_file_location("evidence_abstention_analysis", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def synthetic_inputs(n=8, projects=8):
    accepted = {f"BugsInPy-proj{i % projects}-{i+1}": f"proj{i % projects}" for i in range(n)}
    rows=[]
    for case_index, (cid, project) in enumerate(accepted.items()):
        for level in MODULE.LEVELS:
            for policy in MODULE.POLICIES:
                outcome=""
                evidence="supported"
                if level=="E3_insufficient":
                    outcome="1" if (policy==MODULE.POLICIES[0] and case_index % 3 == 0) else "0"
                    if outcome=="1": evidence="unsupported"
                rows.append({
                    "case_id":cid,"upstream_project":project,"evidence_level":level,
                    "policy":policy,"decision":"diagnose","unsupported_definitive_diagnosis":outcome,
                    "root_cause_accuracy":"correct","evidence_support":evidence,
                    "missing_evidence_quality":"not_applicable","adjudication_status":"final"
                })
    return accepted, rows


class ExactMcNemarTests(unittest.TestCase):
    def test_exact_mcnemar_known_examples(self):
        got=MODULE.exact_mcnemar_pvalue([1,1,1,0],[0,0,0,0])
        self.assertAlmostEqual(got["p_value"],0.25)
        self.assertEqual(got["p0_only_unsupported"],3)
        self.assertEqual(got["p1_only_unsupported"],0)
        self.assertEqual(MODULE.exact_mcnemar_pvalue([0,1],[0,1])["p_value"],1.0)
        self.assertEqual(MODULE.exact_mcnemar_pvalue([0,0],[0,0])["p_value"],1.0)

    def test_clopper_pearson_boundaries_and_order(self):
        self.assertEqual(MODULE.clopper_pearson_interval(0,10,0.05)[0],0.0)
        self.assertEqual(MODULE.clopper_pearson_interval(10,10,0.05)[1],1.0)
        lo,hi=MODULE.clopper_pearson_interval(3,10,0.05)
        self.assertLess(lo,0.3)
        self.assertGreater(hi,0.3)
        self.assertLess(lo,hi)

    def test_conservative_risk_difference_interval_contains_point_estimate(self):
        p0=[1,1,0,0,1,0,0,0]; p1=[0,0,0,0,1,0,0,0]; n=len(p0)
        ci0=MODULE.clopper_pearson_interval(sum(p0),n,0.025)
        ci1=MODULE.clopper_pearson_interval(sum(p1),n,0.025)
        rd=sum(p1)/n-sum(p0)/n
        ci=[max(-1.0,ci1[0]-ci0[1]),min(1.0,ci1[1]-ci0[0])]
        self.assertLessEqual(ci[0],rd); self.assertGreaterEqual(ci[1],rd)

    def test_rejects_below_threshold(self):
        accepted,rows=synthetic_inputs(n=8,projects=8)
        with self.assertRaisesRegex(ValueError,"requires 60"):
            MODULE.validate_and_analyze(rows,accepted,minimum_cases=60,minimum_projects=8)

    def test_validates_synthetic_complete_pairs_and_reports_sensitivity(self):
        accepted,rows=synthetic_inputs(n=16,projects=8)
        result=MODULE.validate_and_analyze(rows,accepted,minimum_cases=16,minimum_projects=8)
        self.assertEqual(result["n_independent_accepted_cases"],16)
        self.assertEqual(result["n_upstream_projects"],8)
        self.assertEqual(result["exact_two_sided_mcnemar"]["p0_only_unsupported"],6)
        self.assertEqual(result["p1_unsupported_count"],0)
        self.assertEqual(len(result["leave_one_upstream_project_out_sensitivity"]),8)

    def test_rejects_duplicate_cell(self):
        accepted,rows=synthetic_inputs(n=8,projects=8); rows.append(dict(rows[0]))
        with self.assertRaisesRegex(ValueError,"duplicate case/evidence/policy"):
            MODULE.validate_and_analyze(rows,accepted,minimum_cases=8,minimum_projects=8)

    def test_rejects_nonfinal_human_adjudication(self):
        accepted,rows=synthetic_inputs(n=8,projects=8); rows[0]["adjudication_status"]="pending"
        with self.assertRaisesRegex(ValueError,"non-final"):
            MODULE.validate_and_analyze(rows,accepted,minimum_cases=8,minimum_projects=8)

    def test_rejects_bad_primary_outcome_locations(self):
        accepted,rows=synthetic_inputs(n=8,projects=8)
        next(r for r in rows if r["evidence_level"]=="E3_insufficient")["unsupported_definitive_diagnosis"]=""
        with self.assertRaisesRegex(ValueError,"E3 outcome"):
            MODULE.validate_and_analyze(rows,accepted,minimum_cases=8,minimum_projects=8)
        accepted,rows=synthetic_inputs(n=8,projects=8)
        next(r for r in rows if r["evidence_level"]=="E1_sufficient")["unsupported_definitive_diagnosis"]="0"
        with self.assertRaisesRegex(ValueError,"blank outside E3"):
            MODULE.validate_and_analyze(rows,accepted,minimum_cases=8,minimum_projects=8)

    def test_registry_rejects_permanently_excluded_triage_case(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"CASE_REGISTRY.json"
            path.write_text(json.dumps({"records":[{
                "accepted_for_confirmatory":True,"case_id":"BugsInPy-black-2","upstream_project":"black"
            }]}),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"permanently excluded"):
                MODULE.load_accepted_registry(path)


if __name__ == "__main__":
    unittest.main()
