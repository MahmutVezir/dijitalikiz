# Reagento/Dishka issue #435 — pre-reproduction review

**Cohort rank:** 2 of 96 primary candidates  
**Dataset instance:** `reagento__dishka-436`  
**Issue:** https://github.com/reagento/dishka/issues/435  
**Fix PR:** https://github.com/reagento/dishka/pull/436  
**Review status:** static scope, provenance, and minimal-environment license screen completed; exact reproduction pending. **Not an accepted case.**

## 1. Issue/patch alignment

Issue #435 is labelled `bug` and supplies a minimal reproducer. A REQUEST-scoped provider registers `int=1`; a later APP-scoped fake provider registers `int=42`; a REQUEST-scoped interactor resolves the dependency. The expected result is 42, but the reporter observed 1.

PR #436 explicitly closes issue #435. Its implementation changes registry construction so provider factories are collected and later inserted into registries after provider processing. It adds cross-scope override tests for provided factories, aliases, and context variables. The changed production file is `src/dishka/registry_builder.py`; four changed test files cover the same override behavior.

The issue and PR have a coherent defect-specific contract: later provider override should determine the resolved dependency despite the provider scopes. The PR's tests exercise the same semantic area. The independent reproducer added to this repository uses the exact issue example and will be run unchanged at the pinned base and fix revisions.

## 2. Pinned source identity and dataset timestamp

- Repository: `reagento/dishka`
- Repository API reports `fork=false`, `archived=false`, created 2024-01-14.
- Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
- Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`
- Dataset row timestamp: `2025-04-15T22:52:26Z`
- GitHub PR #436 `created_at`: `2025-04-15T22:52:26Z`
- GitHub issue #435 `created_at`: `2025-04-15T22:52:26Z`
- Timestamp reconciliation register: exact match.

PR #436 changes five files:
1. `src/dishka/registry_builder.py` (31 additions, 37 deletions)
2. `tests/unit/container/override/test_alias.py` (+52)
3. `tests/unit/container/override/test_context_var.py` (+44)
4. `tests/unit/container/override/test_provide.py` (+23)
5. `tests/unit/container/test_context_vars.py` (+5)

The base blob for `src/dishka/registry_builder.py` is `9a7f2ece6065f357a1806075c5b19af46d15c43d`. The exact-base test-file blobs and the PR's changed-file patch are recorded in the GitHub PR API response; the exact reproducer and raw test logs will be hash-recorded by the reproduction workflow.

## 3. License and dependency screen for the planned reproducer

- Exact-base root `LICENSE`: Apache-2.0; Git blob `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`.
- Exact-base `pyproject.toml`: Git blob `aac556bc080e4c7ce0defc77dd171b3324f742a8`; declares Apache-2.0.
- The exact-base tree contains one license/notice-like file: root `LICENSE`; no nested LICENSE, NOTICE, COPYING, or COPYRIGHT file was found.
- Runtime dependency declaration: `exceptiongroup>=1.1.3; python_version<"3.11"`; therefore no declared third-party runtime dependency is selected under Python 3.11.9.
- Build-system dependency: `setuptools>=66.0`; the reproducer does not build or install a wheel.
- Development/test requirements (pytest and tooling) are not installed or used by the reproducer.
- The reproducer uses Python's standard-library `unittest` and imports source directly through `PYTHONPATH=src`.

This is a narrow documentary screen for the minimal reproduction environment, not legal advice or blanket clearance for every optional integration, development environment, redistribution, or later experiment.

## 4. Independence and exposure

- The canonical repository is not marked as a fork by GitHub.
- The primary cohort selects one candidate project per repository; this candidate is one of the 96 unique primary repositories.
- The candidate has no evidence of being one of the four previously exposed repositories explicitly excluded in the v0.2 manifest.
- The pinned Qwen2.5-3B-Instruct family was publicly released in September 2024; issue #435 and PR #436 were created on 2025-04-15. This temporal ordering reduces the plausibility that this exact public issue/patch was present in the already released model weights. It does not prove the model's complete training-data provenance or exclude prior knowledge of similar patterns.
- The student researcher is now exposed to the issue and patch through candidate review. ChatGPT's review is advisory AI exposure, not a second human rating. Any later semantic scoring must record this exposure and must not claim perfect blinding.

## 5. Exact reproduction plan

A standard-library regression test was added at:
`research_candidates/evidence_abstention/reproduction/dishka_issue_435/test_issue_435.py`

It reproduces the exact issue example and asserts that the REQUEST-scoped interactor resolves 42 from the later APP-scoped fake provider.

Workflow:
`.github/workflows/evidence-abstention-preflight.yml (job: `dishka-issue-435-reproduction`)`

The workflow uses:
- Ubuntu 22.04 GitHub-hosted runner;
- Python 3.11.9;
- no pip installs and no third-party test framework;
- the same test file, test name, and command selector at both exact commits;
- required base failure with `AssertionError: 1 != 42`;
- required fixed-revision pass;
- raw logs, runtime details, commit IDs, and SHA-256 artifact.

A workflow pass is evidence of the specified reproducer behavior only. It does not by itself establish full case acceptance, semantic gold correctness, E1/E2/E3 adequacy, or independence from all related defect families.

## 6. Current decision

Static issue/patch alignment: **promising; retain for technical reproduction**.  
Minimal reproduction environment license/provenance screen: **documented, narrow pass**.  
Exact base-fail/fix-pass reproduction: **pending**.  
Full dependency/legal clearance beyond this minimal environment: **not claimed**.  
Gold standard, alternative mechanisms, evidence packets, E1/E2/E3: **not yet adjudicated**.  
Final case acceptance: **not accepted**.  
Model loading/inference authorization: **false**.
