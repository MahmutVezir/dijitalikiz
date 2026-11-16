"""Integrity checks for the frozen 96-row static triage index."""
from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "SWE_REBENCH_V2_COHORT_96_STATIC_TRIAGE_LEDGER_V0_1_2026-11-16.json"


class CandidateTriageLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_all_96_cohort_ranks_appear_exactly_once(self):
        rows = self.data["rows"]
        ranks = [row["cohort_rank"] for row in rows]
        self.assertEqual(len(rows), 96)
        self.assertEqual(sorted(ranks), list(range(1, 97)))

    def test_screening_counts_match_rows(self):
        counts = {}
        for row in self.data["rows"]:
            key = row["screening_classification"]
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(counts, self.data["screening_counts"])
        self.assertEqual(sum(counts.values()), 96)

    def test_every_row_has_a_pinned_audit_source_and_pr(self):
        for row in self.data["rows"]:
            self.assertTrue(row["source_audit"])
            self.assertTrue(row["repository"])
            self.assertGreater(row["pull_request_number"], 0)
            self.assertTrue(row["pull_request_url"].startswith("https://github.com/"))

    def test_simpeg_second_pass_exclusion_is_explicit(self):
        adjustment = self.data["post_second_pass_adjustments"][0]
        self.assertEqual(adjustment["cohort_rank"], 63)
        self.assertEqual(adjustment["repository"], "simpeg/simpeg")
        self.assertEqual(adjustment["decision"], "excluded_from_strict_bug_shortlist")

    def test_triage_never_means_acceptance_or_inference_authorization(self):
        self.assertIn("not mean license clearance", self.data["interpretation"])
        self.assertNotIn("inference_authorized", self.data)
        self.assertEqual(self.data["row_count"], 96)


if __name__ == "__main__":
    unittest.main()
