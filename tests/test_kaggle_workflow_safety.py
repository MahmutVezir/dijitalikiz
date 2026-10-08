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


def test_kaggle_pilot_builds_exact_source_dataset_and_safe_launcher():
    workflow = workflow_text()
    assert "git archive --format=tar.gz --output=/tmp/dijitalikiz-source.tar.gz HEAD" in workflow
    assert "base64 -w 0 /tmp/dijitalikiz-source.tar.gz" in workflow
    assert "mahmutvezir/dijitalikiz-frozen-source-v2" in workflow
    assert "source_bundle_sha256.txt" in workflow
    assert 'kaggle datasets download -d "$DATASET_ID"' in workflow
    assert 'KERNEL_SLUG="dijitalikiz-frozen-pilot-${GITHUB_SHA:0:12}"' in workflow
    assert 'sed -i "s/__EXPECTED_SOURCE_COMMIT__/$GITHUB_SHA/g"' in workflow
    assert "python -m py_compile .kaggle-kernel/kernel.py" in workflow
    assert "PROJECT_B64_PLACEHOLDER" not in workflow
    

def test_kaggle_launcher_contains_no_stale_bundle_reference():
    kernel = (ROOT / "kaggle" / "kernel.py").read_text(encoding="utf-8")
    assert "bundle_source" not in kernel
    assert 'SOURCE_DATASET = "mahmutvezir/dijitalikiz-frozen-source-v2"' in kernel
    assert "source_bundle_sha256.txt" in kernel
    assert "__EXPECTED_SOURCE_COMMIT__" in kernel


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
