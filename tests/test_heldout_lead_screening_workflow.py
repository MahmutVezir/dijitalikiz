from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "heldout-lead-red-green.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_heldout_lead_screening_is_scoped_and_read_only():
    workflow = workflow_text()
    assert "Held-out Lead Red-Green Screening" in workflow
    assert "pull_request:" in workflow
    assert "workflow_dispatch:" in workflow
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "KAGGLE_API_TOKEN" not in workflow
    assert "kaggle kernels push" not in workflow
    assert "enable_gpu" not in workflow
    assert "run-frozen-pilot:" not in workflow
    assert "run-confirmatory:" not in workflow
    assert "model.generate" not in workflow


def test_heldout_lead_screening_pins_exact_revisions_for_all_discovery_leads():
    workflow = workflow_text()
    expected = {
        "lang-1800-era-calendar": (
            "324d9fbd091749a9c70aed4b038fd0b4a520b3cf",
            "c7f1a6d27707e8cd8cbed94f83e0c58d2c480614",
        ),
        "lang-1807-wildcard-upper-bound": (
            "25c4bfcd6d9dc3a7333088bfc3031b05cd93837e",
            "43154e016ae213a0da5b727cd1aa18e6e0c56adb",
        ),
        "collections-728-ordered-next-key": (
            "a5248efd7f4f857f88770565414948e2d0524933",
            "04b30be69f4355f218d587703bc20b1a591c3e3c",
        ),
        "net-404-ftps-data-hostname-verifier": (
            "faa4edd7e287a3db465a32efd9c2d5faa15757fe",
            "a79729464f6e69b773171ff30e3d483cab7afd70",
        ),
        "net-403-ftp-parser-type-before-instantiation": (
            "a3d19751891edb9f7cb8c11bc344eaf1683b2b32",
            "6e38749760c0366aac1637c7dc15e4ccf76329c9",
        ),
        "text-768-stringmatcher-charsequence-window": (
            "a6cbba814422a06a0366468b2346f52aaacf8f3d",
            "81de4f7a7c7d3b13d89edd72d4c4b92aa33e6c81",
        ),
    }
    for case_id, (pre_fix, fixed) in expected.items():
        assert f"case_id: {case_id}" in workflow
        assert f"pre_fix: {pre_fix}" in workflow
        assert f"fix: {fixed}" in workflow
        assert re.fullmatch(r"[0-9a-f]{40}", pre_fix)
        assert re.fullmatch(r"[0-9a-f]{40}", fixed)


def test_heldout_lead_screening_fails_closed_on_red_and_requires_green():
    workflow = workflow_text()
    assert 'git -C "$SRC" checkout --detach "$PRE_FIX_SHA"' in workflow
    assert 'git -C "$SRC" reset --hard "$FIX_SHA"' in workflow
    assert "failed_as_expected" in workflow
    assert "passed" in workflow
    assert "BLOCKED: targeted regression test did not execute on pre-fix revision" in workflow
    assert "BLOCKED: targeted regression test did not execute on fixed revision" in workflow
    assert "Upload source-screening evidence" in workflow
    assert "retention-days: 90" in workflow
    assert 'name: "Screen candidate (no model inference)"' in workflow or "name: Screen candidate (no model inference)" in workflow
