# Lektor #1213 / PR #1214 — complete Stage 2 matrix and selector-integrity hold

**Updated:** 2026-11-21  
**Research repository:** `MahmutVezir/dijitalikiz`  
**Workflow implementation commit:** `cc06457bef0b219106087e2421dd5607f21f4d87`  
**Upstream issue:** https://github.com/lektor/lektor/issues/1213  
**Upstream fix PR:** https://github.com/lektor/lektor/pull/1214  
**Research tracking PR:** https://github.com/MahmutVezir/dijitalikiz/pull/222

## 1. Final disposition

**Stage 2 contract: FAILED — do not accept Lektor as a validated SWE-rebench case.**

The independent issue reproducer and the exact issue-specific regression selector both demonstrate the intended base-fail/fixed-pass behavior. However, the immutable dataset row contains a broad and partly malformed 149-selector set. The complete two-sided matrix was collected; it does not satisfy the frozen `FAIL_TO_PASS` contract. No selector was removed or rewritten to force a pass.

The case remains **not accepted**, and Stage 3 was not started.

## 2. Exact source and dataset identity

- Buggy base: `c22e224ec56620c2a1d90016d74518970b1dd578`.
- Exact fixed PR head: `7d8bfed7ae0a2eb970acd5be824eeb380239e675`.
- Dataset instance: `lektor__lektor-1214`, repository `lektor/lektor`.
- Frozen dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`.
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.
- Canonical row SHA-256: `4e0b0674a9307164e9486009aa21690973135f599761a489d9a595c2ccea282d`.
- Frozen row has **149 FAIL_TO_PASS selectors**: 24 from `tests/test_builder.py` and 125 from `tests/test_utils.py`.

The dataset problem statement describes build artifacts created with mode `0600`, asks for group-readable permissions, and suggests an umask configuration. It does not itself identify the internal `mkstemp`/temporary-file implementation path.

## 3. Independent issue reproducer — verified base fail / fixed pass

Workflow run [44919553942](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44919553942), job `136892468466`, ran the independent test `test_new_artifact_mode_matches_normally_created_file`.

With umask `022`:
- ordinary file mode: `0644`;
- Lektor build artifact on buggy base: `0600`;
- the reproducer failed on the buggy base for that exact mismatch, as required;
- the same reproducer passed on fixed PR revision `7d8bfed7ae0a2eb970acd5be824eeb380239e675`.

This is direct evidence that PR #1214 fixes the reported file-permission behavior.

## 4. Exact issue-specific frozen selector — verified base fail / fixed pass

The frozen row contains:

```text
tests/test_builder.py::test_Artifact_file_mode
```

- On the buggy base it failed on the actual permission assertion: `0o100600` versus `0o100644`.
- On the exact fixed PR revision it passed.

This one selector is the direct issue-aligned regression test. It is valid evidence for the narrow technical correction, but it does not override the other 148 entries in the frozen row.

## 5. Complete frozen selector matrices

The revised workflow collected every selector in row order on both revisions. Both result files contain 149 entries, and both selector sequences match the frozen row exactly.

### Buggy base: 149 results

| Outcome | Count | Interpretation |
|---|---:|---|
| Unexpected pass | 23 | Existing Builder selectors passed before the fix |
| Target permission assertion failure | 1 | `test_Artifact_file_mode` fails with the reported `0600` vs `0644` mismatch |
| Test-module import/collection error | 125 | `tests/test_utils.py` cannot import the PR-added `create_temp` symbol on the buggy base |

The 125 Utils selectors do **not** represent 125 independently observed functional regressions. The PR's test patch adds `from lektor.utils import create_temp`, while `create_temp` is introduced by the PR in `lektor/utils.py`. On the buggy base the entire test module fails during import, before those individual tests can execute. Their failures are therefore collection/import failures, not per-test evidence of the artifact-permission defect.

The 23 unexpected passes are broad file-level selectors from `tests/test_builder.py`; they are not failures on the buggy revision and should not appear in an unchanged `FAIL_TO_PASS` contract.

### Fixed revision: 149 results

| Outcome | Count |
|---|---:|
| Passed | 145 |
| Invalid/unresolved selector IDs | 4 |

The four unresolved IDs are malformed `test_deprecated_function` node IDs in the frozen row:

- `tests/test_utils.py::test_deprecated_function[kwargs0-^'f'`
- `tests/test_utils.py::test_deprecated_function[kwargs1-^'f'`
- `tests/test_utils.py::test_deprecated_function[kwargs2-^'f'`
- `tests/test_utils.py::test_deprecated_function[kwargs3-^'oldfunc'`

Pytest reports that these node IDs are not found in the collected module and runs no tests for them. The row strings have an unmatched opening parameter bracket, so these are not successful fixed-side selector executions.

### Contract audit

The workflow's `stage2-contract-audit.json` records:

- dataset selector count: 149;
- base results: 149, complete and in order;
- fixed results: 149, complete and in order;
- independent issue reproducer: base failure and fixed pass;
- unexpected base passes: 23;
- fixed selector failures: 4;
- `stage2_contract_passed: false`.

The exact frozen row therefore fails the required complete base-fail/fixed-pass contract despite the genuine issue-specific reproducer and regression test.

## 6. Why the dataset row is not salvageable in this study

The failure is not an environment setup problem. The environment now installs and builds successfully, and the complete selector matrices were produced.

The frozen row combines:
1. broad selectors from a changed test file, including 23 tests that pass on the buggy base;
2. 125 selectors whose module cannot be imported on the buggy base because the PR adds a new helper imported by the modified test file;
3. four fixed-side node IDs that do not resolve to tests.

The research protocol does not authorize silently trimming `FAIL_TO_PASS`, rewriting malformed selectors, or substituting a hand-selected one-test subset after inspecting outcomes. The one valid issue-aligned selector and independent reproducer are retained as engineering evidence only. The dataset case remains blocked.

## 7. Artifact and provenance integrity

- Artifact name: `lektor-issue-1213-reproduction`.
- Artifact ID: `14712694556`.
- GitHub artifact SHA-256: `25d0e9565cc267cc73a3e46c89978880ace5ad4716e2e0023513bc48811c0d91`.
- Independently downloaded ZIP SHA-256: identical.
- ZIP CRC check: PASS.
- Archive members: 20.
- `SHA256SUMS.txt`: 19 entries, **19/19 internal file hashes PASS**.
- `python-license-inventory.json`: valid JSON in this artifact.
- Raw archive includes `base-selector-results.json`, `fixed-selector-results.json`, `stage2-contract-audit.json`, the issue reproducer logs, frozen row, selector list, PR patches, source provenance hashes and pinned environment inventory.
- The full matrix has not been reduced to a summary-only artifact.

## 8. Required disposition

- `stage2_status`: `blocked_dataset_selector_integrity`.
- `stage3_status`: `not_started_stage2_not_passed`.
- `final_case_acceptance`: `not_accepted`.
- Registry inclusion: `false`.
- Model inference authorization: `false`.
- Model loading, inference, fine-tuning and training: not performed.

No further attempt should rerun or alter this frozen row to obtain a pass. Reconsideration would require a separately versioned and justified dataset correction or a new, predeclared study protocol; neither is authorized by this result.
