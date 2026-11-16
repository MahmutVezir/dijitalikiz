# getmoto/moto issue #8269 — candidate review

**Cohort rank:** 9 of 96 primary candidates  
**Dataset instance:** `getmoto__moto-8296` (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/getmoto/moto/issues/8269  
**Fix PR:** https://github.com/getmoto/moto/pull/8296  
**Review status:** static defect/patch and root-license screen passed; exact base-fail/fix-pass reproduction and dataset selector audit pending. Not an accepted case.

## 1. Defect contract

Issue #8269 reports that ECR `list_images()` returns only the latest tag when one image digest has multiple tags, while `describe_images()` exposes all tags. The expected API behavior is one image identifier per tag for the same image digest.

PR #8296 changes the response formatter from one `imageTag` per stored image object to iterating over `image.image_tags`. The exact base model stores all tags in `image.image_tags`, but the old `response_list_object` emits only `image.image_tag` (the current/latest tag). The fix iterates over the full tag list and emits one `imageDigest`/ `imageTag` object for each tag.

The independent reproducer creates one ECR repository, uploads the same manifest under `tag1` and `tag2`, calls `list_images()`, and asserts two identifiers with the same digest and both tags. This directly exercises the reported API behavior.

## 2. Pinned source identity

- Repository: `getmoto/moto`
- Buggy base: `bf49e22f41be7444dc20e05dfa5dd13f25672eba`
- Fixed PR head: `d46db48b4911d84235ef783ddab41b73882530f7`
- Merge commit: `60828f4befc1da863dc4ad630409f6443145fc71`
- Issue #8269 created: `2024-10-30T12:24:49Z`
- PR #8296 created: `2024-11-07T20:51:42Z`
- Exact-base root LICENSE Git blob: `90a85e7149454f173dd595bdeb884340cc01e6f6`
- Exact-base setup.cfg Git blob: `fb1c7ead5806c611cf184980e8b54e4932079758`
- Changed source files: `moto/ecr/models.py`, `moto/ecr/responses.py`; changed test: `tests/test_ecr/test_ecr_boto3.py`.

## 3. License and runtime scope

- Exact-base root license: Apache-2.0.
- Exact-base `setup.cfg` declares base runtime dependencies: boto3, botocore, cryptography, requests, xmltodict, Werkzeug, python-dateutil, responses, and Jinja2.
- The reproducer uses the minimal pinned versions in `reproduction/moto_issue_8269/requirements.lock`; no Docker, AWS account, external service, or remote fixture is required.
- The workflow records installed distribution license metadata before executing Moto source. Any missing or conflicting license metadata is a hard stop until source-level evidence is recorded.
- This is a documentary screen for the pinned minimal reproduction environment, not legal advice or blanket clearance for Moto's optional extras, all services, or redistribution.

## 4. Dataset selector requirement

The workflow authenticates the exact Parquet row for `getmoto__moto-8296`, records its canonical row hash and `FAIL_TO_PASS` selectors, and applies the PR diff to the exact buggy base so that the added tests can be executed there. The same dataset selectors must fail on the buggy base for the expected missing-tag behavior and pass on the fixed revision. The independent issue reproducer is additional evidence, not a substitute for the dataset selectors.

## 5. Independence and exposure

- The v0.2 primary cohort contains one candidate from getmoto/moto; this repository can contribute at most one accepted case.
- Issue #8269 was created on 2024-10-30, after the September 2024 public release of the pinned Qwen2.5-3B-Instruct family. This temporal ordering lowers the plausibility that the exact public issue/patch was in the released weights, but does not establish full training-data provenance or exclude prior knowledge of the general ECR behavior.
- The student researcher has reviewed the issue and PR during candidate screening; perfect blinding must not be claimed.
- Related issue-family and fork/lineage checks remain required before acceptance.

## 6. Current decision

Issue/patch alignment: strong.  
Independent issue reproducer: prepared; workflow pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Minimal runtime license inventory: pending workflow evidence and review.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.
