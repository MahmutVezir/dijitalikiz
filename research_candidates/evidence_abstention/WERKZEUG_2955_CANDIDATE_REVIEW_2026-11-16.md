# pallets/werkzeug #2955 — candidate review

**Cohort rank:** 32 of 96 primary candidates  
**Dataset instance:** pallets__werkzeug-2956  
**Issue:** https://github.com/pallets/werkzeug/issues/2955  
**Fix PR:** https://github.com/pallets/werkzeug/pull/2956  
**Review status:** strong static bug candidate; exact dataset reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #2955 reports an IndexError when Authorization.from_header receives an invalid authorization parameter such as "Digest =foo". The parser splits the item into an empty key and a value, then indexes key[-1] while checking for the RFC 2231 "*" suffix.

PR #2956 adds an early guard in parse_dict_header: if the parsed key is empty, skip the invalid parameter. The PR adds parameterized parser tests and an Authorization-level regression test. This directly matches the reported failure mechanism.

## 2. Pinned source identity

- Repository: pallets/werkzeug
- Buggy base: 40319f91dbbae0a780526eab037a009b1a7e4d36
- Fixed PR head: 1688968101c3341136bd8420ac7b77b6286c7409
- PR merge commit: 6732b579eeaaa2cfb562e57bed55994e4f93ccfb
- Issue #2955 created: 2024-10-09T18:42:44Z
- PR #2956 created: 2024-10-10T21:07:05Z
- PR body explicitly says it fixes issue #2955.

## 3. Source and dependency license screen

- Exact-base pyproject.toml declares LICENSE.txt and the BSD License classifier.
- Exact-base LICENSE.txt is BSD 3-Clause.
- Changed source and test files are covered by the repository license.
- The targeted test imports the source tree directly and requires only MarkupSafe plus pytest and its pinned transitive dependencies. No external fixture, network service, or optional integration is required.
- The workflow records installed distribution license metadata before importing Werkzeug source and stops if metadata is missing.
- This is a narrow documentary screen, not legal advice or blanket clearance for optional extras or redistribution.

## 4. Test adequacy

The issue's exact invalid-input shape is represented by the PR's new Authorization regression test. The dataset FAIL_TO_PASS selectors are extracted from the exact pinned Parquet row, not manually guessed.

Required result: all selected tests fail on the exact buggy base with the empty-key IndexError and pass on the exact fixed revision. Collection errors, dependency failures, or unrelated failures do not count as reproduction.

## 5. Independence and exposure

- The cohort contains one primary candidate for pallets/werkzeug; this project can contribute at most one accepted case.
- The issue and PR were created after the September 2024 public release of Qwen2.5-3B-Instruct. This reduces the likelihood that this exact issue/patch was in the released weights but does not establish complete training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family and fork/lineage checks remain part of final acceptance.

## 6. Current decision

Issue/patch alignment: strong.  
Root source license: BSD 3-Clause.  
Dependency license inventory: pending workflow evidence and review.  
Exact base-fail/fix-pass reproduction: pending.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading and inference authorization: false.
