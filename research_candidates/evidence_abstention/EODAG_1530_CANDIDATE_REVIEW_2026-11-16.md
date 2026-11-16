# CS-SI/eodag issue #1530 — candidate review

**Cohort rank:** 16 of 96 primary candidates  
**Dataset instance:** `CS-SI__eodag-1536` (row identity to be authenticated in the reproduction workflow)  
**Issue:** https://github.com/CS-SI/eodag/issues/1530  
**Fix PR:** https://github.com/CS-SI/eodag/pull/1536  
**Review status:** source/issue/patch and narrow minimal-reproducer license screen passed; dataset selector audit and exact workflow reproduction pending. Not an accepted case.

## 1. Defect contract

Issue #1530 reports that the default user configuration template contains two top-level YAML mapping entries both named `geodes`. The first block is the public Geodes provider and contains an `apikey` credential. The second is the Geodes S3 provider and contains AWS credentials. With ordinary YAML mapping semantics, the later duplicate key replaces the earlier mapping. The resulting configuration no longer contains the public Geodes credential shape and can make the public provider request AWS credentials.

PR #1536 renames the second key to `geodes_s3`. The issue-specific contract is therefore: parsing the template must preserve both provider configurations under distinct keys, with `geodes.auth.credentials.apikey` and `geodes_s3.auth.credentials.aws_access_key_id/aws_secret_access_key/aws_session_token`.

The PR also changes provider initialization to include `StacListAssets` and modifies several provider tests for that additional feature. This is mixed scope. The minimal reproducer isolates only the duplicate-key defect; the dataset FAIL_TO_PASS selectors must still be inspected to determine whether they isolate #1530 or combine the unrelated #1517 feature.

## 2. Pinned source identity

- Repository: `CS-SI/eodag`
- Buggy base: `b7cc06e19025e5bbf14e28a0975f1749e21e9be3`
- Fixed PR head: `312966a46513a082333d46cd7212bdce36aaf769`
- Merge commit: `697b5c851f7f15ccb48c9e749061314118f26e3b`
- Issue #1530 created: `2025-02-20T11:38:36Z`
- PR #1536 created: `2025-02-21T10:04:30Z`
- PR #1536 merged: `2025-02-21T12:28:31Z`
- Exact-base YAML template Git blob: `0d6c9e24a3294dd12c2b09e844ef3990b01a0a5b`
- Fixed YAML template Git blob: `5221bd2d052bdd60363367d3be51044e1cc95c76`
- Exact-base root LICENSE Git blob: `1a9893b43e8e6d46ff5cda60ab6562850b7f78ff`
- Exact-base NOTICE Git blob: `9f763bc3c2f90854b8209ce60e23c8fc03c6ec7e`
- Exact-base setup.cfg Git blob: `fdf8cc087fe720c835e0bfceeeabd1c66aed47a4`

The workflow will authenticate the dataset row timestamp against the exact PR resource before any claim is made about timestamp agreement.

## 3. Narrow source and dependency license screen

- Exact-base root license: Apache-2.0.
- Exact-base NOTICE identifies PyYAML as MIT.
- Exact-base setup.cfg declares PyYAML as a runtime dependency.
- The minimal reproducer reads the exact upstream YAML resource and imports only PyYAML; it does not import EODAG, install the full geospatial stack, call external services, or use remote test fixtures.
- Pinned minimal test dependency: PyYAML 6.0.2. The package's release page identifies MIT licensing; the upstream NOTICE independently records PyYAML under MIT.
- The workflow will record installed distribution metadata and verify the exact version before executing the source reproducer.

This is a documentary screen for the minimal YAML reproducer only. It is not legal advice or blanket clearance for the full EODAG dependency graph, optional providers, external data, or redistribution.

## 4. Independent reproducer

Path: `research_candidates/evidence_abstention/reproduction/eodag_issue_1530/test_issue_1530.py`

The same test loads `eodag/resources/user_conf_template.yml` at the exact buggy base and fixed revision. It requires:
- both `geodes` and `geodes_s3` keys to exist;
- public `geodes` to contain only the `apikey` credential field;
- `geodes_s3` to contain the three AWS credential fields.

Expected base failure: missing `geodes_s3` because the second duplicate `geodes` mapping overwrites the first. Expected fixed pass: both distinct mappings are preserved.

This is an issue-specific source reproducer, not a substitute for the dataset FAIL_TO_PASS selectors.

## 5. Independence and exposure

- The v0.2 primary cohort contains one row for CS-SI/eodag; this repository can contribute at most one accepted case.
- Issue #1530 and PR #1536 were created after the September 2024 public release of the pinned Qwen2.5-3B-Instruct model. This reduces the likelihood that this exact public issue/patch was present in the released weights, but does not establish complete training-data provenance.
- The student researcher has reviewed the issue and patch during candidate screening. This exposure must be recorded; perfect blinding must not be claimed.
- Related issue-family review remains required before final acceptance.

## 6. Current decision

Issue/patch alignment for duplicate YAML keys: strong.  
Minimal YAML reproducer: prepared; workflow result pending.  
Dataset FAIL_TO_PASS row and selector scope: pending; must isolate #1530 from PR #1536's separate StacListAssets changes.  
Minimal-environment license screen: documented, narrow pass.  
Gold mechanism and E1/E2/E3 evidence adjudication: pending human decision.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.
