# SkyPilot #5981 / PR #5985 — Stage 2 teknik sonuç kaydı

**Durum:** Stage 2 teknik doğrulama geçti; Stage 3 ve nihai vaka kabulü bekliyor.  
**Upstream:** `skypilot-org/skypilot`  
**Cohort instance:** `skypilot-org__skypilot-5985` (rank 17/96)  
**Issue:** https://github.com/skypilot-org/skypilot/issues/5981  
**Fix PR:** https://github.com/skypilot-org/skypilot/pull/5985

## 1. Sabit kaynak kimlikleri

- Buggy base: `60a6c930feeb8c48511f74c25bc2d7e12b290dd6`
- Fixed PR revision: `c8154ff3a4875cbb1bac8f29bb45254f264d72ba`
- Exact-base root license: Apache-2.0
- Exact-base LICENSE Git blob: `aad27dddb0055248d9ceb93ac287898fc1d25b29`
- Exact-base `sky/utils/common_utils.py` Git blob: `a0ca0e97a4360019af0c5ec17381a2a3c753a094`
- Fixed `sky/utils/common_utils.py` Git blob: `5745c98b0ddd233625a3f49da20a032833cd95ff`
- Issue created: `2025-06-12T17:18:04Z`
- PR created: `2025-06-12T21:52:38Z`

## 2. Exact dataset row

- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Instance ID: `skypilot-org__skypilot-5985`
- Repository: `skypilot-org/skypilot`
- Base commit: `60a6c930feeb8c48511f74c25bc2d7e12b290dd6`
- Dataset `created_at`: `2025-06-12 21:52:38`, matching the PR resource creation timestamp.
- Canonical row SHA-256: `a846e85ec5452d8100659e5c6c8cbecc3401dae16b8830eed77543172ef9bbbe`
- Exact FAIL_TO_PASS selector count: 1.
- Exact selector:
  `tests/unit_tests/test_sky/clouds/test_ssh.py::TestSSHExistingAllowedContexts::test_complex_scenario_with_mixed_filtering`

The row was read from the pinned Parquet file. No alternate row or reconstructed selector was substituted.

## 3. Defect and observed result

Issue #5981 concerns the use of Python `str.lstrip("ssh-")`. Its argument is a set of removable leading characters, not an exact prefix. Therefore `"ssh-staging".lstrip("ssh-")` becomes `"taging"`, not `"staging"`.

The exact upstream regression test configures allowed pools `["prod", "staging", "nonexistent"]`, available contexts including `ssh-staging`, and node-pool contexts including `ssh-staging`. It expects both `ssh-prod` and `ssh-staging`.

**Buggy base result:** the test executed and failed. Actual result was `["ssh-prod"]`; expected result was `["ssh-prod", "ssh-staging"]`. Pytest reported a real assertion failure, not a collection/setup error.

**Fixed revision result:** the same exact selector passed.

Strict runner contracts:
- Buggy base: `1/1` selector executed and failed.
- Fixed revision: `1/1` identical selector passed.

This exact upstream regression test is the issue-specific reproduction. No separate independent standalone reproducer was added; the candidate is not being credited with an additional second test.

## 4. Test-only patch isolation

The PR's full source diff was retained separately for provenance. Only the PR test-file diff was applied to the buggy base before testing.

Verified test-only patch scope:
- `tests/unit_tests/test_sky/clouds/test_ssh.py`
- `production_code_changed = false`

The production changes introducing `common_utils.removeprefix` were not applied to the buggy base. The fixed-side run checked out the exact fixed revision and ran the identical selector.

## 5. Focused environment and license metadata

- Python: 3.11.9
- Exact lock path: `research_candidates/evidence_abstention/reproduction/skypilot_issue_5981/requirements.lock`
- Locked external distributions: 85
- Pinned lock SHA-256 recorded by the pinned workflow: `a5f56951e68d90cc7d78136d94420c7081a475343846c1f1e7df662d6fcbab94`
- Installed distribution inventory: 86 records, including the editable SkyPilot source distribution.
- License metadata: present for all 86 inventory records; the pinned workflow fails before test execution if any installed distribution lacks license metadata.
- Exact dependency-version comparison against `requirements.lock`: passed.
- `pip check`: passed.
- No Kubernetes cluster, SSH endpoint, cloud account, or external service was used.

The inventory provides package metadata for human review; it is not legal advice or blanket legal clearance. Project-lead review of the dependency and bundled-license scope remains open.

## 6. Workflow and artifact integrity

Environment discovery:
- Workflow run: [44120296410](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44120296410)
- Job: `134169504792`
- Artifact ID: `14344533255`
- Artifact ZIP SHA-256: `b0df249916eaaf25cb3d8fad4c9a0b29df6dd91490bcf03300ed068d398c39f1`
- Internal SHA256SUMS: 17 entries, 0 mismatches.

Pinned repeat:
- Workflow run: [44120296408](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44120296408)
- Job: `134169504759`
- Artifact ID: `14345590500`
- Artifact ZIP SHA-256: `c9b41b7fa3ce284a322e59bee360cc3504a27f2608212ea84cfb1bed38cded3e`
- Internal SHA256SUMS: 18 entries, 0 mismatches.
- Pinned repeat reran the same selector against the same base and fixed commits in the exact 85-package lock environment; all install, version, license-metadata, and test steps passed.

The artifact ZIPs were downloaded and independently checked: ZIP CRC tests passed, every listed inner file was present, and all SHA-256 values matched.

## 7. Decision and remaining gates

**Stage 2 technical reproduction: PASS.**  
**Stage 3 human gold/alternative-hypothesis adjudication: not started.**  
**Final case acceptance: not accepted.**  
**Model loading, inference, or training: not authorized and not performed.**

Remaining gates:
1. Project-lead review of the 86-entry dependency/license inventory and any bundled notices.
2. Repository lineage, related-issue-family and independent-project review.
3. Human gold root-cause and alternative-hypothesis adjudication.
4. Preparation and human approval of nested E1/E2/E3 evidence packets.
5. Complete schema-conformant case-acceptance record and fail-closed registry validation.
6. Separate project-lead final case-acceptance decision.

Researcher source exposure during candidate screening is recorded as partial; no blinding claim is made. The issue and PR post-date the September 2024 public release window of the pinned Qwen model family, but the exact training-data cutoff is not independently established. No no-contamination guarantee is claimed.

## 8. Excluded auxiliary run

A third redundant workflow was accidentally created while the existing discovery and pinned workflows were already present. Its patch-scope step failed before dependency installation or upstream test execution; it is not evidence for or against the candidate. The duplicate workflow file was removed and will not be used. The two pre-existing workflows above are the authoritative discovery and pinned-repeat evidence.
