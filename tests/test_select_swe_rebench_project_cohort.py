import unittest

from scripts.select_swe_rebench_project_cohort import (
    build_cohort,
    hamilton_quotas,
)


def row(instance, repo, license_name="MIT", status="metadata_candidate_unreviewed"):
    return {
        "instance_id": instance,
        "repo": repo,
        "base_commit": "a" * 40,
        "created_at_utc": "2025-01-01T00:00:00Z",
        "language": "python",
        "license": license_name,
        "fail_to_pass_count": "1",
        "screen_status": status,
    }


class CohortTests(unittest.TestCase):
    def fixture(self):
        rows = []
        strata = [("MIT", 8), ("Apache-2.0", 4), ("BSD-3-Clause", 4)]
        for lic, count in strata:
            for i in range(count):
                repo = f"org{i}-{lic.split('-')[0].lower()}/project{i}"
                rows.append(row(f"{repo}-case-a", repo, lic))
                if i % 2 == 0:
                    rows.append(row(f"{repo}-case-b", repo, lic))
        return rows

    def test_hamilton_quotas_sum_to_target(self):
        result = hamilton_quotas(
            {"MIT": 47, "Apache-2.0": 33, "BSD-3-Clause": 29, "MIT-0": 2, "BSD-2-Clause": 2},
            96,
        )
        self.assertEqual(sum(result.values()), 96)
        self.assertEqual(
            result,
            {"Apache-2.0": 28, "BSD-2-Clause": 2, "BSD-3-Clause": 24, "MIT": 40, "MIT-0": 2},
        )

    def test_one_primary_per_project_and_project_reserves_do_not_overlap(self):
        primary, reserves, alternates, summary = build_cohort(
            self.fixture(), target=12, seed="test-seed"
        )
        self.assertEqual(len(primary), 12)
        self.assertEqual(len({r["repo"] for r in primary}), 12)
        self.assertEqual(len(reserves), 4)
        self.assertFalse({r["repo"] for r in primary} & {r["repo"] for r in reserves})
        self.assertEqual(len(alternates), 8)
        self.assertEqual(summary["accepted_confirmatory_cases"], 0)
        self.assertFalse(summary["model_inference_performed"])

    def test_selection_is_independent_of_input_order(self):
        rows = self.fixture()
        first = build_cohort(rows, target=12, seed="fixed")
        second = build_cohort(list(reversed(rows)), target=12, seed="fixed")
        self.assertEqual([x["instance_id"] for x in first[0]], [x["instance_id"] for x in second[0]])
        self.assertEqual([x["repo"] for x in first[1]], [x["repo"] for x in second[1]])

    def test_previous_exposure_projects_are_excluded(self):
        rows = self.fixture() + [row("keras-case", "keras-team/keras")]
        primary, reserves, alternates, _ = build_cohort(rows, target=12, seed="test")
        all_rows = primary + reserves + alternates
        self.assertNotIn("keras-team/keras", {x["repo"] for x in all_rows})

    def test_unapproved_license_and_non_python_are_not_selected(self):
        rows = self.fixture() + [
            row("custom-case", "custom/project", "custom-check-github"),
            row("js-case", "js/project", "MIT"),
        ]
        rows[-1]["language"] = "javascript"
        primary, reserves, alternates, _ = build_cohort(rows, target=12, seed="test")
        selected = primary + reserves + alternates
        self.assertNotIn("custom/project", {x["repo"] for x in selected})
        self.assertNotIn("js/project", {x["repo"] for x in selected})

    def test_duplicate_instance_ids_fail_closed(self):
        rows = self.fixture()
        rows.append(dict(rows[0]))
        with self.assertRaisesRegex(ValueError, "Duplicate instance_id"):
            build_cohort(rows, target=12, seed="test")


if __name__ == "__main__":
    unittest.main()
