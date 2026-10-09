from pathlib import Path
import hashlib
import json
import py_compile
import sys

from scripts.power_mcnemar import exact_mcnemar_power
from scripts.validate_benchmark_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_preselected_confirmatory_manifest_is_frozen_and_complete():
    manifest = json.loads(
        (ROOT / "data" / "benchmark" / "benchmark_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "frozen"
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
    metadata = manifest["freeze_metadata"]
    assert metadata["pilot_completion_verified"] is True
    assert metadata["case_selection_preselected_before_inference"] is True
    assert metadata["scoring_protocol_amendment_recorded"] is True
    assert metadata["pilot_outputs_consulted_for_scoring_protocol_diagnostics"] is True
    assert metadata["confirmatory_outputs_consulted"] is False
    assert metadata["verified_pilot_record_count"] == 40
    assert len(metadata["pilot_artifact_sha256"]) == 64


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
        ROOT / "scripts" / "build_confirmatory_launcher.py",
    ):
        py_compile.compile(str(path), doraise=True)


def test_kaggle_automation_is_single_canonical_workflow():
    workflow_dir = ROOT / ".github" / "workflows"
    workflow_names = sorted(path.name for path in workflow_dir.glob("*.yml"))
    assert workflow_names == ["kaggle-pilot.yml"]

def test_confirmatory_kaggle_kernel_isolated_from_exported_artifacts():
    kernel_path = ROOT / "kaggle" / "confirmatory_kernel.py"
    source = kernel_path.read_text(encoding="utf-8")
    py_compile.compile(str(kernel_path), doraise=True)
    assert 'RUNTIME_ROOT = Path("/tmp/dijitalikiz-confirmatory-runtime")' in source
    assert 'WORKDIR = RUNTIME_ROOT / "dijitalikiz"' in source
    assert 'PYTHON_ENV = RUNTIME_ROOT / "dijitalikiz-py311"' in source
    assert 'OUTPUT_DIR = KERNEL_ROOT / "confirmatory-output"' in source
    assert 'BUNDLE_SOURCE.unlink()' in source
    assert 'SOURCE_COMMIT_FILE.unlink()' in source
    assert "source_bundle_sha256" in source
    assert 'run(str(python), "-m", "pip", "check", cwd=WORKDIR)' in source
    assert source.index('"scripts/validate_confirmatory_artifact_manifest.py"') < source.index('for item in benchmark.iterdir()')
    assert 'run(str(python), "scripts/run_confirmatory.py"' in source
    assert '"/kaggle/working/dijitalikiz"' not in source


def test_frozen_manifest_passes_full_gate_without_mutating_repository_file():
    manifest_path = ROOT / "data" / "benchmark" / "benchmark_manifest.json"
    original_bytes = manifest_path.read_bytes()
    manifest = json.loads(original_bytes.decode("utf-8"))
    assert manifest["status"] == "frozen"
    assert not validate_manifest(manifest, ROOT)
    assert manifest_path.read_bytes() == original_bytes



def test_confirmatory_launcher_builder_emits_checksum_bound_kernel(tmp_path):
    import subprocess
    import tarfile

    source_file = tmp_path / "README.txt"
    source_file.write_text("frozen source fixture", encoding="utf-8")
    bundle = tmp_path / "source.tar.gz"
    with tarfile.open(bundle, "w:gz") as archive:
        archive.add(source_file, arcname="data/README.txt")

    output_dir = tmp_path / "kernel"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_confirmatory_launcher.py"),
            "--bundle",
            str(bundle),
            "--source-commit",
            "a" * 40,
            "--output-dir",
            str(output_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    generated = output_dir / "kernel.py"
    py_compile.compile(str(generated), doraise=True)
    source = generated.read_text(encoding="utf-8")
    assert "EXPECTED_BUNDLE_SHA256" in source
    assert "RUNNER_SOURCE_B64" in source
    assert "FROZEN_SOURCE_COMMIT = " in source
    assert "a" * 40 in source
