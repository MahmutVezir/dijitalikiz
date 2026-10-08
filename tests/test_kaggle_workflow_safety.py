from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_kaggle_pilot_is_manual_only_and_opt_in():
    workflow = (ROOT / ".github" / "workflows" / "kaggle-pilot.yml").read_text(
        encoding="utf-8"
    )
    assert "workflow_dispatch:" in workflow
    assert "\n  push:" not in workflow
    assert 'description: "Run the frozen 30-inference pilot on Kaggle GPU"' in workflow
    assert "default: false" in workflow
    assert "if: inputs.execute_inference == true" in workflow


def test_kaggle_pilot_packages_exact_source_commit():
    workflow = (ROOT / ".github" / "workflows" / "kaggle-pilot.yml").read_text(
        encoding="utf-8"
    )
    assert "git archive --format=tar.gz --output=.kaggle-kernel/project.tar.gz HEAD" in workflow
    assert 'printf \'%s\\n\' "$GITHUB_SHA" > .kaggle-kernel/source_commit.txt' in workflow
