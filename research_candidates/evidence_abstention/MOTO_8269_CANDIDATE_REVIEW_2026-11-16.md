# getmoto/moto issue #8269 — candidate review

**Cohort rank:** 9 of 96 primary candidates  
**Dataset instance:** `getmoto__moto-8296` (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/getmoto/moto/issues/8269  
**Fix PR:** https://github.com/getmoto/moto/pull/8296  
**Review status:** static defect/patch and root-license screen passed; dataset resource identity is tied to PR #8296 creation time; candidate-specific CI job did not obtain a runner and executed zero steps. Exact base-fail/fix-pass reproduction and dependency-license inventory remain pending. Not an accepted case.

## 1. Defect contract

Issue #8269 reports that ECR `list_images()` returns only the latest tag when one image digest has multiple tags, while `describe_images()` exposes all tags. The expected API behavior is one image identifier per tag for the same image digest.

PR #8296 changes the response formatter from one `imageTag` per stored image object to iterating over `image.image_tags`. The exact base model stores all tags in `image.image_tags`, but the old `response_list_object` emits only `image.image_tag` (the current/latest tag). The fix iterates over the full tag list and emits one `imageDigest`/ `imageTag` object for each tag.

The independent reproducer creates one ECR repository, uploads the same manifest under `tag1` and `tag2`, calls `list_images()`, and asserts two identifiers with the same digest and both tags. This directly exercises the reported API behavior.

Static source trace: `ECRBackend.put_image()` finds an existing image with the same manifest on the second put and calls `image.update_tag(image_tag)`. `Image.update_tag()` appends the new tag to `image.image_tags` while retaining the latest value in `image.image_tag`. The buggy `response_list_object` serializes only `image.image_tag`; the fixed `ECRResponse.list_images()` loops over every entry in `image.image_tags` and emits one `{imageDigest, imageTag}` record per tag. The model source therefore stores both tags; the defect is in response projection, not tag persistence.

## 2. Pinned source identity

- Repository: `getmoto/moto`
- Buggy base: `bf49e22f41be7444dc20e05dfa5dd13f25672eba`
- Fixed PR head: `d46db48b4911d84235ef783ddab41b73882530f7`
- Merge commit: `60828f4befc1da863dc4ad630409f6443145fc71`
- Issue #8269 created: `2024-10-30T12:24:49Z`
- PR #8296 created: `2024-11-07T20:51:42Z`
- The SWE-rebench row is a PR-task instance (`getmoto__moto-8296`), so its `created_at` provenance is expected to match PR #8296, not issue #8269. The preflight now asserts the exact PR timestamp `2024-11-07 20:51:42` in addition to repository, base commit, language, and license.
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

## 6. Latest CI evidence and Stage 2 decision

The research workflow was run at `43898509334`; the Moto job was `133408468911`. Its GitHub job object reports `steps: null`, no log URL, and no runner assignment. A targeted rerun was requested for that one Moto job; attempt 2 produced job `133410279986`, which completed in approximately one second with `runner_id=0`, empty runner name, and `steps=[]`. The workflow run generated no artifacts. Other jobs in the same run also terminated without steps.

This is an execution-infrastructure failure before the candidate job began. It is **not** a failing base test, a failing fixed test, or a dependency/license failure. There is no raw reproduction evidence from these attempts.

| Gate | Evidence | Status |
|---|---|---|
| Defect report and PR linkage | Issue #8269 labelled bug; PR #8296 explicitly fixes it | Pass |
| Source mechanism | Image stores multiple tags; old response emits current tag only; fixed response expands image_tags | Strong static alignment |
| Dataset row identity | Instance ID, repo, base, Python, Apache-2.0 and PR creation timestamp assertions are frozen in workflow | Ready to verify; not executed |
| Defect-specific dataset test | PR adds same-manifest/multiple-tag test; base should return one item, fixed should return two | Strong oracle candidate; not executed |
| Independent reproducer | Local mock ECR, no AWS account or remote fixture | Prepared; not executed |
| Root source license | Apache-2.0; exact-base LICENSE blob recorded | Documentary screen passed |
| Minimal dependency license inventory | Workflow gate defined; no inventory artifact | Pending |
| Exact base-fail/fix-pass logs and artifact | Runner not allocated; no steps or artifact | **BLOCKED — no reproduction claim** |

**Stage 2 result:** technically promising and reproduction-ready on paper, but execution blocked by GitHub Actions runner allocation. Keep as provisional. Do not start Stage 3 gold/tier adjudication until the exact dataset selectors and independent reproducer both demonstrate the required base-fail/fixed-pass behavior with raw logs and hashes.

## 7. Independence, exposure, and acceptance

- The v0.2 primary cohort contains one candidate from getmoto/moto; this repository can contribute at most one accepted case.
- Issue #8269 (2024-10-30) and PR #8296 (2024-11-07) are later than the pinned Qwen2.5-3B-Instruct September 2024 public release. This ordering lowers the likelihood that this exact public issue/patch appears in those released weights, but does not prove training-data provenance or exclude general prior knowledge of ECR tag behavior.
- The student researcher has reviewed the issue and PR during screening; perfect blinding must not be claimed.
- Related issue-family and fork/lineage checks remain required before acceptance.
- Gold mechanism adjudication and E1/E2/E3 packet creation have not started.
- Final case acceptance: `not_accepted`.
- Model loading/inference authorization: `false`.
