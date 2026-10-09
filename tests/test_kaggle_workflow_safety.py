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
    assert (
        "if: github.event_name == 'push' || "
        "(github.event_name == 'workflow_dispatch' && inputs.execute_inference == true)"
    ) in workflow


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
