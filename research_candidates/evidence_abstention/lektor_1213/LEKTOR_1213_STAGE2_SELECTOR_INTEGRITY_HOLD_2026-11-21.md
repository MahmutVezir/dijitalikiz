# Lektor #1213 / PR #1214 — Stage 2 result and selector-integrity hold

**As of:** 2026-11-21  
**Research repository:** `MahmutVezir/dijitalikiz`  
**Research branch head at validation:** `52e29ee78765722abeed7195ea9fe933ae22825c`  
**Umbrella tracking PR:** [MahmutVezir/dijitalikiz#222](https://github.com/MahmutVezir/dijitalikiz/pull/222)  
**Upstream:** [lektor/lektor issue #1213](https://github.com/lektor/lektor/issues/1213), [PR #1214](https://github.com/lektor/lektor/pull/1214)

## Disposition

**Stage 2 is blocked/incomplete.** The independent issue-level reproducer detects the defect on the exact buggy base. However, the frozen SWE-rebench selector row fails its required base-side contract because its first selector unexpectedly passes. The workflow consequently skips the fixed-revision selector run. Do not count Lektor as a Stage 2 pass or accepted case.

## Pinned source and issue scope

- Buggy base: `c22e224ec56620c2a1d90016d74518970b1dd578`.
- Exact merged PR #1214 revision: `7d8bfed7ae0a2eb970acd5be824eeb380239e675`.
- Frozen dataset instance: `lektor__lektor-1214`, repository `lektor/lektor`.
- Canonical row SHA-256: `4e0b0674a9307164e9486009aa21690973135f599761a489d9a595c2ccea282d`.
- The frozen row contains **149 FAIL_TO_PASS selectors**: 24 from `tests/test_builder.py` and 125 from `tests/test_utils.py`.
- The issue reports build artifacts created with mode `0600`, while the reporter expects group-readable files, and asks about configurable umask behavior. PR #1214 says it fixes file modes of created files and also includes a related `atomic_open` correction.

## Confirmed independent reproduction on buggy base

Workflow [run 44917970732](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44917970732), job `136887636693`, executed the independent test in `research_candidates/evidence_abstention/reproduction/lektor_issue_1213/test_issue_1213.py`.

With umask `022`, the test creates a normal file and a Lektor build artifact, then compares their permission modes. On the exact buggy base it reports:

- normal file: `0644`
- build artifact: `0600`

The independent test therefore fails on the buggy base exactly as required. Source cloning and pinned source-file checks passed. The earlier environment-install problem was resolved by adding the Hatchling editable-build dependency and `wheel==0.45.1`; the latest run's installation step succeeded.

## Frozen-selector failure

The same run authenticated the Parquet file against the frozen dataset SHA-256 and extracted exactly one `lektor__lektor-1214` row. Its first selector was:

```text
tests/test_builder.py::test_basic_build
```

That selector **unexpectedly passed on the buggy base**, so the workflow stopped the base-side selector audit at the first entry. The fixed-revision reproducer/selector step was skipped. The PR-added `tests/test_builder.py::test_Artifact_file_mode` selector is present later in the 149-item row, but was not reached in this run. Outcomes for the remaining 148 selectors are unknown; no claims are made about them.

This is a dataset-selector integrity/scope problem, not an environment-install failure. The independent issue reproducer is valid evidence of the base defect, but it does not repair or override the immutable row's unexpected base pass.

## Artifact integrity

- Artifact: `lektor-issue-1213-reproduction`, ID `14712348769`.
- GitHub-reported SHA-256: `dc0345c2d3284f795721b10d226db6523db75c004e2823c525a0d943143bdb2c`.
- Independently downloaded archive SHA-256: identical.
- ZIP CRC: PASS.
- ZIP members: 13, including `SHA256SUMS.txt`.
- Internal manifest: 12 entries; **12/12 hashes PASS**.
- The archive includes the independent buggy-base test log, exact frozen row, selector list, problem statement, PR patch, source-provenance hashes, dependency freeze and license-metadata inventory. It does not contain a completed selector-results matrix because the workflow stopped at the first unexpected base pass.

## Required next gate

1. Preserve the exact frozen row and audit all 149 selectors without stopping at the first unexpected pass; retain per-selector base results.
2. Run the independent issue reproducer against the exact fixed PR revision and capture its result.
3. Reconcile the frozen selector row with the tests actually added/changed by PR #1214. Keep the issue-specific reproducer, related `atomic_open` tests and unrelated file-level selectors distinguishable.
4. Only after the row mismatch is resolved should the candidate advance to the Stage 2 pass decision and a separate Stage 3 E3/sample-suitability review.

**Current case status:** `blocked_dataset_selector_integrity`; Stage 3 not started; final case acceptance `not_accepted`; model inference remains unauthorized. No model weights were loaded and no inference, fine-tuning or training was performed.
