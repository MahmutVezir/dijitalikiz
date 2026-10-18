from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "heldout-lead-red-green.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def active_case_ids(workflow: str) -> list[str]:
    marker = "      matrix:\n        include:\n"
    start = workflow.find(marker)
    assert start >= 0, "screening matrix is missing"
    start += len(marker)
    end = workflow.find("\n\n\n    env:", start)
    assert end >= 0, "screening matrix boundary is missing"
    return re.findall(r"^\s*- case_id: ([^\r\n]+)$", workflow[start:end], re.MULTILINE)


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
    assert "MAVEN_MODULE" in workflow
    assert '-pl "$MAVEN_MODULE" -am' in workflow
    assert "surefire.failIfNoSpecifiedTests=false" in workflow


def test_heldout_lead_screening_runs_only_the_six_pending_candidates():
    workflow = workflow_text()
    expected = {
        "netty-17623-negative-search-domain-cache": (
            "de7fa8997db278b83f56b22f89b691be58ae88ba",
            "1addbf90c4fd35713c61e5c54ad4d21c14d7df1d",
        ),
        "netty-17764-tls13-signature-algorithm-key-selection": (
            "3eaff63caf06a582cc3df72422aa1124734b46c6",
            "84c167ea85e0d7f5b40caec6cab859018f9490bd",
        ),
        "collections-724-indexed-collection-iterator-index-drift": (
            "3ff49116a265817f7546f72052e3d0478c159e62",
            "651a6218910a906dc50415c145d63ba06c07a659",
        ),
        "collections-720-synchronized-collection-foreach-lock": (
            "d58a5e3a1258877bd94ba79db9f8a5f90892624b",
            "6ee9dd78c79f367dd8e3e1655e4664bcec960ad6",
        ),
        "lang-1795-fastdateformat-mutable-timezone-cache-leak": (
            "d235f1e997523d7a3d9d1c63e9a1853c2ab728fd",
            "117a9ea791b87af1b90413fa8290891ca3106cfd",
        ),
        "compress-797-lz77-back-reference-window-bound": (
            "4a17b64939b782a5e95c5aecfd583b631cb58522",
            "cebee156fe66578b5142b4176e6c408a76d65c0c",
        ),
    }
    ids = active_case_ids(workflow)
    assert len(ids) == len(set(ids)) == 6
    assert set(ids) == set(expected)
    assert "matrix.screen_pending" not in workflow
    assert not re.search(r"^\s*screen_pending:", workflow, re.MULTILINE)
    assert not re.search(r"^\s{4}if:.*matrix\.", workflow, re.MULTILINE)
    assert "max-parallel: 2" in workflow
    assert '.github/workflows/heldout-lead-red-green.yml' not in workflow.split("pull_request:", 1)[1].split("workflow_dispatch:", 1)[0]
    for case_id, (pre_fix, fixed) in expected.items():
        assert f"case_id: {case_id}" in workflow
        assert f"pre_fix: {pre_fix}" in workflow
        assert f"fix: {fixed}" in workflow
        assert re.fullmatch(r"[0-9a-f]{40}", pre_fix)
        assert re.fullmatch(r"[0-9a-f]{40}", fixed)
        assert pre_fix != fixed


def test_tls13_candidate_explicitly_enables_boringssl_and_records_profile():
    workflow = workflow_text()
    marker = "          - case_id: netty-17764-tls13-signature-algorithm-key-selection\n"
    start = workflow.find(marker)
    assert start >= 0, "TLS 1.3 candidate is missing"
    end = workflow.find("\n          - case_id:", start + len(marker))
    block = workflow[start:end if end >= 0 else len(workflow)]

    # The regression concerns Netty's native OpenSSL/BoringSSL key-selection path.
    # JDK-only success cannot be accepted as evidence that this defect is reproduced.
    assert "maven_profiles: boringssl" in block
    assert "MAVEN_PROFILES: ${{ matrix.maven_profiles || '' }}" in workflow
    assert 'mvn -B -ntp -P"$MAVEN_PROFILES" -pl "$MAVEN_MODULE" -am clean' in workflow
    assert 'echo "maven_profiles=$MAVEN_PROFILES"' in workflow


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
