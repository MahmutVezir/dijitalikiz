from pathlib import Path
import json
import py_compile

from scripts.power_mcnemar import exact_mcnemar_power
from scripts.validate_benchmark_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_preselected_confirmatory_manifest_is_complete_draft():
    manifest = json.loads(
        (ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "draft"
    assert len(manifest["case_ids"]) == 16
    assert len(set(manifest["case_ids"])) == 16
    assert manifest["contamination_audit_completed"] is True
    assert manifest["power_assumption"]["required_case_count"] == 16
    assert manifest["power_assumption"]["achieved_power"] >= manifest["power_assumption"]["target_power"]
    assert not validate_manifest(manifest, ROOT)


def test_predeclared_power_matches_exact_utility():
    observed = exact_mcnemar_power(16, 0.60, 0.05, alpha=0.05)
    assert observed >= 0.80
    assert round(observed, 4) == 0.8070


def test_confirmatory_scripts_compile():
    for path in (
        ROOT / "scripts" / "run_confirmatory.py",
        ROOT / "scripts" / "audit_confirmatory_integrity.py",
        ROOT / "scripts" / "evaluate_confirmatory.py",
        ROOT / "scripts" / "primary_confirmatory_analysis.py",
        ROOT / "scripts" / "finalize_confirmatory.py",
        ROOT / "scripts" / "confirmatory_qa_report.py",
        ROOT / "scripts" / "build_confirmatory_records_jsonl.py",
        ROOT / "scripts" / "build_confirmatory_artifact_manifest.py",
        ROOT / "scripts" / "validate_confirmatory_artifact_manifest.py",
        ROOT / "scripts" / "freeze_benchmark.py",
    ):
        py_compile.compile(str(path), doraise=True)


def test_kaggle_automation_is_single_canonical_workflow():
    workflow_dir = ROOT / ".github" / "workflows"
    workflow_names = sorted(path.name for path in workflow_dir.glob("*.yml"))
    assert workflow_names == ["kaggle-pilot.yml"]
