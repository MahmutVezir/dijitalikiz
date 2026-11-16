from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_WORKFLOW = ROOT / ".github" / "workflows" / "research-validation.yml"
ARCHIVE_WORKFLOW = ROOT / ".github" / "workflows" / "persist-historical-archive.yml"
SAFETY_WORKFLOW = ROOT / ".github" / "workflows" / "persist-historical-archive-safety.yml"
ARCHIVE_SHA256 = "e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd"


def test_research_validation_does_not_gate_on_unrelated_historical_ccdg_zip():
    workflow = RESEARCH_WORKFLOW.read_text(encoding="utf-8")
    assert "validate-repository:" in workflow
    assert "validate-historical-archive:" not in workflow
    assert "data/historical/confirmatory_artifact_2026-10-09.zip" not in workflow
    assert "scripts/audit_historical_artifact.py" not in workflow
    assert "repository_validation_status=PASS" in workflow
    assert "repository_validation_status=FAIL" in workflow
    assert "This job checks repository code/configuration only" in workflow




def test_historical_archive_changes_still_trigger_repository_ci():
    workflow = RESEARCH_WORKFLOW.read_text(encoding="utf-8")
    assert workflow.count('"data/historical/**"') == 0


def test_research_validation_uses_read_only_permissions_and_no_upload():
    workflow = RESEARCH_WORKFLOW.read_text(encoding="utf-8")
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "actions: write" not in workflow
    assert "pull-requests: write" not in workflow
    assert "permissions: write-all" not in workflow
    assert "actions/upload-artifact@" not in workflow
    for command in ("git push", "git commit", "git add", "git branch", "gh pr create", "gh release upload"):
        assert command not in workflow


def test_manual_archive_verifier_is_read_only_and_fail_closed():
    workflow = ARCHIVE_WORKFLOW.read_text(encoding="utf-8")
    triggers = workflow.split("permissions:", maxsplit=1)[0]
    assert "workflow_dispatch:" in triggers
    assert "push:" not in triggers
    assert "pull_request:" not in triggers
    assert "actions: read" in workflow
    assert "contents: read" in workflow
    assert "actions: write" not in workflow
    assert "contents: write" not in workflow
    assert "pull-requests: write" not in workflow
    assert "permissions: write-all" not in workflow
    assert "11640450681" in workflow
    assert ARCHIVE_SHA256 in workflow
    assert "BLOCKED/UNAVAILABLE" in workflow
    assert "python -m zipfile -t" in workflow
    assert "python scripts/audit_historical_artifact.py" in workflow
    for command in ("git push", "git commit", "git add", "git branch", "git switch --create", "gh pr create", "gh release upload", "actions/upload-artifact@"):
        assert command not in workflow


def test_static_safety_contract_scans_all_runtime_write_surfaces():
    safety = SAFETY_WORKFLOW.read_text(encoding="utf-8")
    assert 'runtime_sources = (("archive", archive), ("research", research))' in safety
    assert "forbidden_write_command" in safety
    assert "forbidden_api_write" in safety
    assert "forbidden_model_execution" in safety
    assert "actions/upload-artifact@" in safety
    assert "BLOCKED/UNAVAILABLE" in safety
    assert "Historical archive record audit: FAIL (diagnostic log kept out of public workflow output)." in safety
    assert "Read-only historical archive workflow static safety checks: PASS" in safety
    # A static source check is not a substitute for the runtime artifact integrity job.
    assert "runtime verification is a separate gate" in safety


def test_workflow_keeps_execution_no_inference():
    workflow = RESEARCH_WORKFLOW.read_text(encoding="utf-8")
    archive_workflow = ARCHIVE_WORKFLOW.read_text(encoding="utf-8")
    combined = workflow + "\n" + archive_workflow
    assert "scripts/run_pilot.py" not in combined
    assert "scripts/run_confirmatory.py" not in combined
    assert "scripts/run_frozen_pilot.py" not in combined
    assert "scripts/run_followup_v2.py" not in combined
    assert "kaggle kernels push" not in combined
    assert "kaggle kernels start" not in combined
    assert "KAGGLE_API_TOKEN" not in combined
