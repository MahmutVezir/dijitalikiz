import json
from pathlib import Path

from scripts.audit_context_v2_parity import audit_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_context_v2_parity_audit_passes_for_frozen_case_definitions():
    report = audit_manifest(
        ROOT / "data" / "benchmark" / "benchmark_manifest.json",
        ROOT / "data" / "benchmark" / "cases",
    )
    assert report["status"] == "pass"
    assert report["protocol_version"] == "context-v2"
    assert report["case_count"] == 16
    assert report["condition_count"] == 3
    assert len(report["cases"]) == report["case_count"]
    assert all(item["edge_count"] > 0 for item in report["cases"])
    assert all(item["base_context_sha256"] for item in report["cases"])
