from pathlib import Path
import hashlib
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
    rubric_path = ROOT / manifest["scoring_rubric"]["path"]
    rubric_bytes = rubric_path.read_bytes()
    assert hashlib.sha256(rubric_bytes).hexdigest() == manifest["scoring_rubric"]["sha256"]
    rubric = json.loads(rubric_bytes.decode("utf-8"))
    assert [item["case_id"] for item in rubric["cases"]] == manifest["case_ids"]
    assert all(item["root_cause_aliases"] for item in rubric["cases"])


def test_predeclared_power_matches_exact_utility():
    power = json.loads(
        (ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8")
    )["power_assumption"]
    assert power["alternative"] == "ccdg_better_than_standard"
    observed = exact_mcnemar_power(
        16, power["p_standard_only"], power["p_ccdg_only"], alpha=0.05
    )
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


def test_preselected_manifest_passes_full_frozen_gate_without_changing_repo_status():
    draft = json.loads(
        (ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8")
    )
    frozen_candidate = {**draft, "status": "frozen"}
    assert draft["status"] == "draft"
    assert not validate_manifest(frozen_candidate, ROOT)
