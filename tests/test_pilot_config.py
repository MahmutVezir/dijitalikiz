import pytest

from dijitalikiz.pilot_config import (
    expected_pilot_record_count,
    expected_pilot_run_filenames,
)


def frozen_manifest():
    return {
        "status": "model_frozen",
        "cases": ["case-a", "case-b", "case-c", "case-d"],
        "conditions": ["standard", "ccdg"],
        "replications": 5,
        "generation": {"seeds": [42, 43, 44, 45, 46]},
        "expected_records": 40,
    }


def test_frozen_manifest_defines_exact_40_run_cross_product():
    manifest = frozen_manifest()
    assert expected_pilot_record_count(manifest, require_declared=True) == 40
    assert len(expected_pilot_run_filenames(manifest, require_declared=True)) == 40


def test_expected_count_rejects_declared_count_drift():
    manifest = frozen_manifest()
    manifest["expected_records"] = 30
    with pytest.raises(ValueError, match="expected_records mismatch"):
        expected_pilot_record_count(manifest, require_declared=True)


def test_expected_count_rejects_duplicate_case_ids():
    manifest = frozen_manifest()
    manifest["cases"].append("case-a")
    with pytest.raises(ValueError, match="duplicate case IDs"):
        expected_pilot_record_count(manifest, require_declared=True)


def test_expected_count_rejects_unsafe_case_ids():
    manifest = frozen_manifest()
    manifest["cases"][0] = "../case-a"
    with pytest.raises(ValueError, match="safe"):
        expected_pilot_record_count(manifest, require_declared=True)
