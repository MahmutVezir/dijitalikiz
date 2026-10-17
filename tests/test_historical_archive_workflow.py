from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "research-validation.yml"
ARCHIVE_PATH = "data/historical/confirmatory_artifact_2026-10-09.zip"
ARCHIVE_SHA256 = "e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd"


def test_workflow_pins_local_historical_archive_and_full_audit():
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert ARCHIVE_PATH in workflow
    assert ARCHIVE_SHA256 in workflow
    assert 'test "$(stat -c \'%s\' "$archive_path")" = "292742"' in workflow
    assert "python -m zipfile -t \"$archive_path\"" in workflow
    assert "scripts/audit_historical_artifact.py --archive \"$archive_path\"" in workflow
    assert "--expected-run-record-count 160" in workflow


def test_historical_archive_changes_trigger_both_ci_events():
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert workflow.count('"data/historical/**"') == 2


def test_workflow_does_not_depend_on_expiring_actions_artifact_or_actions_read():
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "11640450681" not in workflow
    assert "GH_TOKEN" not in workflow
    assert "/actions/artifacts/" not in workflow
    assert "actions: read" not in workflow
    assert ".github/workflows/stage-historical-archive.yml" not in workflow
    assert "contents: write" not in workflow


def test_workflow_keeps_execution_no_inference():
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "scripts/run_pilot.py" not in workflow
    assert "scripts/run_confirmatory.py" not in workflow
    assert "scripts/run_frozen_pilot.py" not in workflow
    assert "scripts/run_followup_v2.py" not in workflow
    assert "kaggle kernels push" not in workflow
    assert "kaggle kernels start" not in workflow
    assert "KAGGLE_API_TOKEN" not in workflow


PERSIST_WORKFLOW_PATH = (
    ROOT / ".github" / "workflows" / "persist-historical-archive.yml"
)


def test_archive_recovery_workflow_is_manual_only_and_requires_acknowledgement():
    workflow = PERSIST_WORKFLOW_PATH.read_text(encoding="utf-8")
    triggers = workflow.split("permissions:", maxsplit=1)[0]
    assert "workflow_dispatch:" in triggers
    assert "type: boolean" in triggers
    assert "\\n  schedule:" not in triggers
    assert "\\n  push:" not in triggers
    assert "ARCHIVE_ACK" in workflow
    assert 'test "$ARCHIVE_ACK" = "true"' in workflow
    assert 'test "$GITHUB_REF" = "refs/heads/main"' in workflow


def test_archive_recovery_pins_artifact_and_audits_before_git_write():
    workflow = PERSIST_WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "11640450681" in workflow
    assert "292742" in workflow
    assert ARCHIVE_SHA256 in workflow
    assert "actions: read" in workflow
    assert "contents: write" in workflow
    assert "pull-requests: write" in workflow
    assert "scripts/audit_historical_artifact.py" in workflow
    audit_position = workflow.index("python scripts/audit_historical_artifact.py")
    branch_position = workflow.index('git switch --create "$branch"')
    push_position = workflow.index('git push origin "$branch"')
    pr_position = workflow.index("gh pr create")
    assert audit_position < branch_position < push_position < pr_position
    assert 'git push origin main' not in workflow
    assert 'git push origin HEAD:main' not in workflow


def test_archive_recovery_workflow_cannot_execute_research_inference():
    workflow = PERSIST_WORKFLOW_PATH.read_text(encoding="utf-8")
    assert "scripts/run_pilot.py" not in workflow
    assert "scripts/run_confirmatory.py" not in workflow
    assert "scripts/run_frozen_pilot.py" not in workflow
    assert "scripts/run_followup_v2.py" not in workflow
    assert "kaggle kernels push" not in workflow
    assert "kaggle kernels start" not in workflow
    assert "KAGGLE_API_TOKEN" not in workflow
