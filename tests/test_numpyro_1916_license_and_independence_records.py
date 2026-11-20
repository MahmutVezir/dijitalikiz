import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMPYRO = ROOT / "research_candidates" / "evidence_abstention" / "numpyro_1916"
LICENSE_PATH = NUMPYRO / "NUMPYRO_1916_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-20.json"
INDEPENDENCE_PATH = NUMPYRO / "NUMPYRO_1916_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json"


class Numpyro1916LicenseAndIndependenceRecordTests(unittest.TestCase):
    def test_dependency_inventory_is_locally_integrity_verified_but_not_legally_approved(self):
        record = json.loads(LICENSE_PATH.read_text(encoding="utf-8"))
        env = record["reproduction_environment"]
        self.assertEqual(env["artifact_id"], 14536697284)
        self.assertEqual(env["artifact_reported_sha256"], env["locally_downloaded_archive_sha256"])
        self.assertTrue(env["outer_sha256_matches_reported_digest"])
        self.assertEqual(env["zip_crc"], "PASS")
        self.assertEqual(env["sha256sums_payload_verified_count"], 15)
        self.assertEqual(len(env["source_test_runtime_packages"]), 17)
        self.assertTrue(all(
            item.get("license") or item.get("license_classifiers")
            for item in env["source_test_runtime_packages"]
        ))
        self.assertFalse(record["human_review"]["accepted_as_legal_clearance"])
        self.assertEqual(record["human_review"]["project_lead_scope_acknowledgement"], "pending")
        self.assertFalse(record["dataset"]["exact_pinned_dataset_card_license_verified"])
        self.assertFalse(record["inference_authorized"])

    def test_upstream_license_and_changed_files_are_explicitly_scoped(self):
        record = json.loads(LICENSE_PATH.read_text(encoding="utf-8"))
        source = record["upstream_source"]
        self.assertEqual(source["root_license_spdx"], "Apache-2.0")
        self.assertEqual(len(source["changed_files"]), 2)
        self.assertTrue(all(item["spdx_header"] == "Apache-2.0" for item in source["changed_files"]))
        self.assertEqual(record["dataset"]["row_license_field"], "Apache-2.0")
        self.assertEqual(record["dataset"]["dataset_hub_card_current_license"], "CC-BY-4.0")

    def test_numpyro_is_distinct_from_dishka_but_related_issues_are_clustered(self):
        record = json.loads(INDEPENDENCE_PATH.read_text(encoding="utf-8"))
        self.assertFalse(record["candidate"]["upstream_repository_is_fork"])
        self.assertTrue(record["candidate"]["fix_pr_head_is_fork"])
        self.assertTrue(record["distinct_from_first_accepted_project"]["independent_upstream_project"])
        self.assertEqual(record["counting_rule"]["issue_count"], 1)
        self.assertEqual(record["counting_rule"]["dataset_row_count"], 1)
        self.assertEqual(record["counting_rule"]["frozen_selector_count"], 2)
        self.assertTrue(record["counting_rule"]["selectors_are_two_test_variants_of_one_defect"])
        self.assertFalse(record["issue_family_disposition"]["exact_duplicate_found"])
        timestamp = record["timestamp_reconciliation"]
        self.assertEqual(timestamp["dataset_row_created_at_raw"], "2024-11-28 00:54:29")
        self.assertEqual(timestamp["upstream_pr_created_at_utc"], "2024-11-28T00:54:29Z")
        self.assertTrue(timestamp["equality_after_utc_normalization"])
        self.assertNotEqual(timestamp["dataset_row_created_at_raw"], timestamp["upstream_issue_created_at_utc"])
        self.assertEqual(timestamp["case_level_timestamp_reconciliation"], "verified")
        self.assertEqual(timestamp["cohort_wide_timestamp_gate"], "remains_open")
        self.assertEqual(
            set(record["issue_family_disposition"]["duplicate_candidates_excluded_from_independent_case_count"]),
            {2132, 2338, 2359, 2392},
        )
        self.assertEqual(record["exposure_and_roles"]["panel_b_independent_source_unexposed_reviewers_confirmed"], 0)
        self.assertEqual(record["independence_status"]["final_case_acceptance"], "not_accepted")
        self.assertFalse(record["independence_status"]["inference_authorized"])


if __name__ == "__main__":
    unittest.main()
