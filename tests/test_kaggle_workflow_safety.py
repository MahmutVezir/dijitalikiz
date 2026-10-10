from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def workflow_text() -> str:
    return (ROOT / ".github" / "workflows" / "kaggle-pilot.yml").read_text(
        encoding="utf-8"
    )


def test_kaggle_pilot_is_manual_or_scoped_trigger_and_opt_in():
    workflow = workflow_text()
    assert "workflow_dispatch:" in workflow
    assert 'paths:\n      - ".github/kaggle-pilot-trigger"' in workflow
    assert 'description: "Run the frozen 40-inference pilot on Kaggle GPU"' in workflow
    assert "default: false" in workflow
    assert "execute_confirmatory:" in workflow
    assert 'description: "Run the frozen 160-inference confirmatory benchmark on Kaggle GPU"' in workflow
    pilot_job = workflow.split("  run-frozen-pilot:", 1)[1].split("  reject-ambiguous-selection:", 1)[0]
    confirmatory_job = workflow.split("  run-confirmatory:", 1)[1]

    # Frozen inference may only launch from main; branch-local trigger writes
    # must never start Kaggle model runs.
    assert "if: github.ref == 'refs/heads/main' && (" in pilot_job
    assert "if: github.ref == 'refs/heads/main' && (" in confirmatory_job
    assert "!contains(github.event.head_commit.message, '[validate-only]')" in pilot_job
    assert "!contains(github.event.head_commit.message, '[confirmatory]')" in pilot_job
    assert "inputs.execute_inference == true && inputs.execute_confirmatory == false" in pilot_job
    assert "inputs.execute_confirmatory == true && inputs.execute_inference == false" in confirmatory_job
    assert "validate-only:" in workflow
    assert "pytest -q" in workflow
    assert "kaggle kernels push" in workflow


def test_kaggle_pilot_is_read_only_against_github_repository():
    workflow = workflow_text()
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "git push origin" not in workflow
    assert "git commit" not in workflow


def test_kaggle_pilot_builds_self_contained_launcher():
    workflow = workflow_text()
    assert "git archive" in workflow
    assert "--output=/tmp/dijitalikiz-source.tar.gz" in workflow
    assert "base64 -w 0" in workflow
    assert "FROZEN_SOURCE_COMMIT" in workflow
    assert "EXPECTED_BUNDLE_SHA256" in workflow
    assert "PROJECT_BUNDLE_B64" in workflow
    assert 'dataset_sources": []' in workflow
    assert "python -m py_compile .kaggle-kernel/kernel.py" in workflow
    assert "__COMMIT__" in workflow
    assert "__BUNDLE_SHA256__" in workflow
    assert "__BUNDLE_B64__" in workflow


def test_kaggle_pilot_binds_launcher_to_current_commit():
    workflow = workflow_text()
    assert 'KERNEL_SLUG="dijitalikiz-frozen-pilot-' in workflow
    assert "GITHUB_SHA:0:8" in workflow
    assert "GITHUB_RUN_ID" in workflow
    assert "GITHUB_RUN_ATTEMPT" in workflow
    assert "GITHUB_SHA:0:12" not in workflow
    assert 'launcher = (' in workflow
    assert '.replace("__COMMIT__", commit)' in workflow
    assert 'echo "Embedded source commit: $GITHUB_SHA"' in workflow


def test_kaggle_pilot_has_no_dataset_transfer_dependency():
    workflow = workflow_text()
    assert "kaggle datasets create" not in workflow
    assert "kaggle datasets version" not in workflow
    assert "kaggle datasets download" not in workflow
    assert "kagglehub" not in workflow


def test_kaggle_pilot_checks_canonical_final_artifacts():
    workflow = workflow_text()
    for name in (
        "pilot_records.jsonl",
        "pilot_evaluation.json",
        "case_level_analysis.json",
        "pilot_qa_report.json",
        "artifact_manifest.json",
    ):
        assert name in workflow
    assert "validate_pilot_artifact_manifest.py" in workflow


def test_kaggle_pilot_uses_node24_compatible_python_action_and_checks_dependencies():
    workflow = workflow_text()
    assert "uses: actions/setup-python@v6" in workflow
    assert "uses: actions/setup-python@v5" not in workflow
    assert 'run(str(target_python), "-m", "pip", "check", cwd=WORKDIR)' in workflow

def test_kaggle_artifact_validation_loop_has_single_do():
    workflow = workflow_text()
    assert "\n          do\n          do\n" not in workflow
    assert "for required in" in workflow
    assert 'test -n "$(find kaggle-output -name "$required" -type f -print -quit)"' in workflow


def test_kaggle_runtime_and_installed_packages_are_not_exported_as_artifacts():
    workflow = workflow_text()
    assert 'RUNTIME_ROOT = Path("/tmp/dijitalikiz-frozen-pilot-runtime")' in workflow
    assert 'BUNDLE = RUNTIME_ROOT / "project.tar.gz"' in workflow
    assert 'WORKDIR = RUNTIME_ROOT / "dijitalikiz"' in workflow
    assert 'PYTHON_ENV = RUNTIME_ROOT / "dijitalikiz-py311"' in workflow
    assert "RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)" in workflow
    assert 'output_dir = KERNEL_ROOT / "pilot-output"' in workflow
    assert "group: dijitalikiz-frozen-pilot-output-v2" in workflow


def test_validate_only_path_never_runs_inference():
    workflow = workflow_text()
    assert "contains(github.event.head_commit.message, '[validate-only]')" in workflow
    assert "github.event_name == 'workflow_dispatch' && inputs.execute_inference == false" in workflow
    validate_job = workflow.split("  validate-only:", 1)[1].split("  run-frozen-pilot:", 1)[0]
    assert "kaggle kernels push" not in validate_job
    assert "run_confirmatory.py" not in validate_job
    assert "validate_benchmark_manifest.py" in validate_job
    assert "audit_confirmatory_integrity.py" in validate_job
    assert "scripts/build_confirmatory_launcher.py" in validate_job
    assert "py_compile /tmp/dijitalikiz-confirmatory-launcher-check/kernel.py" in validate_job


def test_confirmatory_run_is_separately_opt_in_and_fails_closed():
    workflow = workflow_text()
    assert "run-confirmatory:" in workflow
    assert "reject-ambiguous-selection:" in workflow
    assert "inputs.execute_confirmatory == true && inputs.execute_inference == false" in workflow
    assert "contains(github.event.head_commit.message, '[confirmatory]')" in workflow
    confirmatory_job = workflow.split("  run-confirmatory:", 1)[1]
    for required in (
        "data/benchmark",
        "data/pilot",
        "data/assessments",
        "scripts/build_confirmatory_launcher.py",
        "scripts/audit_confirmatory_integrity.py",
        "scripts/validate_benchmark_manifest.py",
        "scripts/validate_confirmatory_artifact_manifest.py",
        "confirmatory_evaluation.json",
        "primary_analysis.json",
        "dijitalikiz-confirmatory-",
    ):
        assert required in confirmatory_job
    assert "execute_inference == true && inputs.execute_confirmatory == true" in workflow


def test_confirmatory_push_does_not_also_launch_the_pilot():
    workflow = workflow_text()
    pilot_job = workflow.split("  run-frozen-pilot:", 1)[1].split("  reject-ambiguous-selection:", 1)[0]
    assert "!contains(github.event.head_commit.message, '[confirmatory]')" in pilot_job
