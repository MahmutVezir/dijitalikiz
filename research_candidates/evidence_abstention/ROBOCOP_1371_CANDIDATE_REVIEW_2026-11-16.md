# MarketSquare/robotframework-robocop #1371 — candidate review

**Cohort rank:** 24 of 96 primary candidates  
**Dataset instance:** marketsquare__robotframework-robocop-1374  
**Issue:** https://github.com/MarketSquare/robotframework-robocop/issues/1371  
**Fix PR:** https://github.com/MarketSquare/robotframework-robocop/pull/1374  
**Review status:** strong static bug candidate; the first Parquet extraction attempt used an incorrectly cased instance ID and returned zero rows. The frozen cohort scope audit records the lowercase instance ID; the current workflow now resolves by normalized repository name plus exact base SHA and requires exactly one match. Post-correction extraction and reproduction are pending. Not an accepted case.

## 1. Defect contract

Issue #1371 reports that robocop format --check prints that files would be reformatted but exits with status 0. For a check-only formatter, modified files should cause exit status 1; no changes should return 0.

PR #1374 identifies the control-flow problem: formatting_result returned an integer, but the caller did not propagate that value as the CLI process exit status. The fix raises typer.Exit with the appropriate code. The PR adds four explicit CLI cases covering check on/off and files that would/would not be formatted.

This is a direct observable CLI failure, with a clear expected outcome and a focused regression test.

## 2. Pinned source identity

- Repository: MarketSquare/robotframework-robocop
- Buggy base: 271e73253a70710cc80374128efa9eabb549b5f2
- Fixed PR head: ceb6824fb4d80442937497a740edf60a5b6382e0
- PR merge commit: 6ed3c579e5d14fae89471be29503f73a051105af
- Issue #1371 created: 2025-04-02T08:09:21Z
- PR #1374 created: 2025-04-02T13:39:40Z
- PR body explicitly says it fixes issue #1371.

## 3. Source and dependency license screen

- Exact-base LICENSE is Apache-2.0.
- Exact-base pyproject.toml declares Apache Software License.
- The targeted test uses only the repository's included Robot Framework fixture files; no external service or external dataset is needed.
- The minimal runtime/test dependency lock pins Robocop's declared runtime dependencies, pytest, and the relevant transitive dependencies.
- Before importing Robocop source, the workflow records license metadata for each installed distribution and stops if a package has neither a license field nor a license classifier.
- This is a narrow documentary screen, not legal advice or blanket clearance for optional extras or redistribution.

## 4. Test adequacy

The exact dataset FAIL_TO_PASS selectors are extracted from the pinned Parquet row. The workflow applies the PR diff to the exact buggy base and runs those selectors, then runs the same selectors against the exact fixed PR head.

Required result: the base fails because a formatting check with changed files exits 0 instead of 1; the fixed revision passes. Collection errors, dependency failures, or unrelated failures do not count as a reproduction.

## 5. Independence and exposure

- The cohort contains one primary candidate for this upstream project; it can contribute at most one accepted case.
- Issue and PR dates are after the September 2024 public release of Qwen2.5-3B-Instruct. This reduces the likelihood that this exact issue/patch was in the released weights but does not establish complete training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family and fork/lineage checks remain part of final acceptance.

## 6. Prior workflow attempt and current decision

The first reproduction run was `43881610067`, job `133348643973`. Package installation and dependency-license inventory passed. Parquet SHA-256 matched the pinned value `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`, but row extraction searched the case-sensitive instance ID `MarketSquare__robotframework-robocop-1374` and returned zero rows (`AssertionError: 0`). The frozen 17–24 scope audit records the normalized ID as `marketsquare__robotframework-robocop-1374`.

The current workflow no longer relies on the fragile full instance ID. It scans for rows whose normalized `repo` contains `robotframework-robocop` and whose `base_commit` equals `271e73253a70710cc80374128efa9eabb549b5f2`; it requires exactly one row, validates repo/base/language/license and prints the resolved instance ID. This is a correction to the row selector, not proof that the row has now been found. The corrected extraction and test pair have not yet run; the later preflight run `43898509334` ended with the Robocop job having zero steps/no runner assignment.

Issue/patch alignment: strong.  
Root source license: Apache-2.0.  
Dependency inventory: passed in the first run.  
Dataset row: initial lookup failed because of case-sensitive instance-id mismatch; corrected repo/base resolver pending execution.  
Exact base-fail/fix-pass reproduction: not run.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading and inference authorization: false.
