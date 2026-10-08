from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def workflow_text() -> str:
    return (ROOT / ".github" / "workflows" / "kaggle-pilot.yml").read_text(
        encoding="utf-8"
    )


def test_kaggle_pilot_is_manual_only_and_opt_in():
    workflow = workflow_text()
    assert "workflow_dispatch:" in workflow
    assert "\n  push:" not in workflow
    assert 'description: "Run the frozen 40-inference pilot on Kaggle GPU"' in workflow
    assert "default: false" in workflow
    assert "if: github.event_name == 'workflow_dispatch' && inputs.execute_inference == true" in workflow


def test_kaggle_pilot_is_read_only_against_github_repository():
    workflow = workflow_text()
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "git push origin" not in workflow
    assert "git commit" not in workflow


def test_kaggle_pilot_packages_exact_source_commit():
    workflow = workflow_text()
    assert "git archive --format=tar.gz --output=.kaggle-kernel/project.tar.gz HEAD" in workflow
    assert 'printf \'%s\\n\' "$GITHUB_SHA" > .kaggle-kernel/source_commit.txt' in workflow


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
