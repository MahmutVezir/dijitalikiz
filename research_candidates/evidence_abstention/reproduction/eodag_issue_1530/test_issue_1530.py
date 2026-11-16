"""Minimal YAML-level regression reproducer for CS-SI/eodag#1530."""
from __future__ import annotations

import os
from pathlib import Path
import unittest

import yaml


class EodagIssue1530Regression(unittest.TestCase):
    def test_geodes_and_geodes_s3_have_distinct_configuration_keys(self) -> None:
        source_root = Path(os.environ["EODAG_SOURCE_ROOT"])
        template = source_root / "eodag" / "resources" / "user_conf_template.yml"
        with template.open(encoding="utf-8") as stream:
            providers = yaml.safe_load(stream)

        self.assertIn("geodes", providers)
        self.assertIn("geodes_s3", providers)
        self.assertEqual(
            set(providers["geodes"]["auth"]["credentials"]),
            {"apikey"},
        )
        self.assertEqual(
            set(providers["geodes_s3"]["auth"]["credentials"]),
            {"aws_access_key_id", "aws_secret_access_key", "aws_session_token"},
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
