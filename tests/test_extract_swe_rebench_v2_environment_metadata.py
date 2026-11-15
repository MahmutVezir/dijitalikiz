import unittest

import pyarrow as pa

from scripts.extract_swe_rebench_v2_environment_metadata import (
    EXPECTED_PARQUET_SHA256,
    build_output,
    extract_environment_record,
)


def row(instance_id, install_config=None):
    if install_config is None:
        install_config = {
            "pre_install": ["python -m pip install -e ."],
            "test_cmd": "pytest tests/test_dsp_normalize.py",
        }
    return {
        "instance_id": instance_id,
        "repo": "pyfar/pyfar",
        "base_commit": "a" * 40,
        "image_name": "prime/primeintellect/pyfar:fixture",
        "language": "python",
        "license": "MIT",
        "created_at": "2024-11-15T08:33:08Z",
        "install_config": install_config,
    }


class ExtractSweRebenchEnvironmentMetadataTests(unittest.TestCase):
    def test_extracts_only_environment_identity_fields_and_config(self):
        table = pa.Table.from_pylist([row("pyfar__pyfar-722")])
        record = extract_environment_record(table, "pyfar__pyfar-722")
        self.assertEqual(record["instance_id"], "pyfar__pyfar-722")
        self.assertEqual(record["repo"], "pyfar/pyfar")
        self.assertEqual(record["install_config"]["test_cmd"], "pytest tests/test_dsp_normalize.py")
        self.assertEqual(set(record), {
            "instance_id", "repo", "base_commit", "image_name",
            "language", "license", "created_at", "install_config"
        })

    def test_missing_target_row_fails_closed(self):
        table = pa.Table.from_pylist([row("other__repo-1")])
        with self.assertRaisesRegex(ValueError, "found 0"):
            extract_environment_record(table, "pyfar__pyfar-722")

    def test_duplicate_target_rows_fail_closed(self):
        table = pa.Table.from_pylist([
            row("pyfar__pyfar-722"),
            row("pyfar__pyfar-722"),
        ])
        with self.assertRaisesRegex(ValueError, "found 2"):
            extract_environment_record(table, "pyfar__pyfar-722")

    def test_empty_install_config_is_not_accepted(self):
        table = pa.Table.from_pylist([row("pyfar__pyfar-722", {})])
        with self.assertRaisesRegex(ValueError, "non-empty structured install_config"):
            extract_environment_record(table, "pyfar__pyfar-722")

    def test_non_struct_install_config_is_rejected(self):
        table = pa.table({
            "instance_id": ["pyfar__pyfar-722"],
            "repo": ["pyfar/pyfar"],
            "base_commit": ["a" * 40],
            "image_name": ["prime/primeintellect/pyfar:fixture"],
            "language": ["python"],
            "license": ["MIT"],
            "created_at": ["2024-11-15T08:33:08Z"],
            "install_config": ['{"test_cmd": "pytest"}'],
        })
        with self.assertRaisesRegex(ValueError, "must be a Parquet struct"):
            extract_environment_record(table, "pyfar__pyfar-722")

    def test_output_manifest_preserves_execution_boundary(self):
        record = row("pyfar__pyfar-722")
        output = build_output(record, EXPECTED_PARQUET_SHA256, 226272977, 6272)
        self.assertFalse(output["execution_boundary"]["upstream_test_or_build"])
        self.assertFalse(output["execution_boundary"]["model_inference"])
        self.assertEqual(len(output["environment_metadata_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
