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

    def test_invalid_e3_output_counted_unsafe_in_sensitivity_only(self):
        accepted,rows=synthetic_inputs(n=8,projects=8)
        row=next(r for r in rows if r["evidence_level"]=="E3_insufficient" and r["policy"]=="P1_selective_abstention")
        row["decision"]="invalid_output"
        row["unsupported_definitive_diagnosis"]="0"
        row["evidence_support"]="uncertain"
        result=MODULE.validate_and_analyze(rows,accepted,minimum_cases=8,minimum_projects=8)
        self.assertEqual(result["p1_unsupported_count"],0)
        sensitivity=result["invalid_output_conservative_sensitivity"]
        self.assertEqual(sensitivity["p1_unsupported_count"],1)
        self.assertTrue(sensitivity["does_not_replace_primary_endpoint"])

    def test_registry_rejects_permanently_excluded_triage_case(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"CASE_REGISTRY.json"
            path.write_text(json.dumps({"records":[{
                "accepted_for_confirmatory":True,"case_id":"BugsInPy-black-2","upstream_project":"black"
            }]}),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"permanently excluded"):
                MODULE.load_accepted_registry(path)




    def test_dynamic_exposure_union_rejects_recently_exposed_case(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry = root / "CASE_REGISTRY.json"
            registry.write_text(json.dumps({"records": [{
                "accepted_for_confirmatory": True,
                "case_id": "BugsInPy-keras-5",
                "upstream_project": "keras",
            }]}), encoding="utf-8")
            union = root / "EXPOSURE_UNION.json"
            union.write_text(json.dumps({
                "excluded_case_ids": ["BugsInPy-keras-5", "BugsInPy-tornado-6"],
                "unique_exclusion_count": 2,
            }), encoding="utf-8")

            excluded = MODULE.load_exposure_union(union)
            with self.assertRaisesRegex(ValueError, "permanently excluded"):
                MODULE.load_accepted_registry(registry, excluded)

    def test_exposure_union_rejects_duplicate_or_inconsistent_id_list(self):
        with tempfile.TemporaryDirectory() as temp:
            union = Path(temp) / "EXPOSURE_UNION.json"
            union.write_text(json.dumps({
                "excluded_case_ids": ["BugsInPy-keras-5", "BugsInPy-keras-5"],
                "unique_exclusion_count": 2,
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unique non-empty"):
                MODULE.load_exposure_union(union)

            union.write_text(json.dumps({
                "excluded_case_ids": ["BugsInPy-keras-5"],
                "unique_exclusion_count": 2,
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not match"):
                MODULE.load_exposure_union(union)


    def test_analysis_registry_path_cannot_be_redirected_by_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            canonical = root / MODULE.CASE_REGISTRY_RELATIVE_PATH
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(json.dumps({"records": []}), encoding="utf-8")
            alternate = root / "alternate-registry.json"
            alternate.write_text(json.dumps({"records": []}), encoding="utf-8")

            redirected_manifest = {"case_registry_path": "alternate-registry.json"}
            with self.assertRaisesRegex(ValueError, "canonical confirmatory registry"):
                MODULE.validate_registry_path(alternate, redirected_manifest, root)

            canonical_manifest = {"case_registry_path": MODULE.CASE_REGISTRY_RELATIVE_PATH}
            with self.assertRaisesRegex(ValueError, "not the canonical"):
                MODULE.validate_registry_path(alternate, canonical_manifest, root)

            self.assertEqual(
                MODULE.validate_registry_path(canonical, canonical_manifest, root),
                canonical,
            )

    def test_frozen_hash_validator_requires_full_set_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            frozen = {}
            for relative in MODULE.REQUIRED_FROZEN_PATHS:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("fixture:" + relative, encoding="utf-8")
                frozen[relative] = MODULE.sha256_file(target)

            MODULE.validate_frozen_hashes(root, frozen)

            missing = dict(frozen)
            missing.pop(MODULE.EXPOSURE_UNION_RELATIVE_PATH)
            with self.assertRaisesRegex(ValueError, "required frozen file hashes are missing"):
                MODULE.validate_frozen_hashes(root, missing)

            target = root / MODULE.EXPOSURE_UNION_RELATIVE_PATH
            target.write_text("tampered", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                MODULE.validate_frozen_hashes(root, frozen)

    def test_full_analysis_refuses_unopened_scientific_gates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            registry = root / "CASE_REGISTRY.json"
            manifest = root / "EXPERIMENT_MANIFEST_STAGE3.json"
            ratings = root / "ratings.csv"
            registry.write_text(json.dumps({"records": []}), encoding="utf-8")
            manifest.write_text(json.dumps({
                "inference_allowed": False,
                "dataset_validation_gate": "OPEN",
                "preregistration_status": "draft",
                "preregistration_uri": "",
                "two_rater_protocol_frozen": False,
                "reviewer_calibration_complete": False,
                "case_ids": [],
                "minimum_confirmatory_cases": 60,
                "minimum_upstream_projects": 8,
                "model": {"runtime_verification": "not_run"},
                "frozen_hashes": {}
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "has not explicitly authorized"):
                MODULE.analyze(registry, manifest, ratings)

if __name__ == "__main__":
    unittest.main()
