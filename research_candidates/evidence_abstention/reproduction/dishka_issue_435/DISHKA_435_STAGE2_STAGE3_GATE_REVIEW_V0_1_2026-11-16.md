# Dishka #435 / dataset instance reagento__dishka-436 — Stage 2 and Stage 3 gate review

**Review date:** 2026-11-16  
**Cohort role:** primary, rank 2  
**Upstream repository:** `reagento/dishka` (repository ID `742987819`)  
**Defect report:** https://github.com/reagento/dishka/issues/435  
**Dataset-linked PR:** https://github.com/reagento/dishka/pull/436  
**Buggy base:** `8718d5af93f9e48bc2506c64827663fdccc5ad89`  
**Fixed revision:** `b1eae11734e64551d7b101195f27cb6870e1c364`

## Gate outcome

- **Stage 2 — exact reproduction:** PASS.
- **Stage 3 — technical gold, alternatives and E1/E2/E3:** PASS; explicit project-lead approval is recorded in the human adjudication decision.
- **Final case acceptance:** NOT YET ACCEPTED. The outstanding acknowledgement is limited to the researcher-exposure and single-human-adjudicator limitation statement, plus final registry-record validation. This does not reverse the Stage 2 or Stage 3 results.
- **Model inference authorization:** FALSE.

## Stage 2 — raw reproduction evidence

The later complete run is GitHub Actions run `43881610067`, job `133348644460`:

- Run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067
- Artifact ID: `14231689140`
- Artifact: [download from GitHub Actions](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067/artifacts/14231689140)
- Artifact ZIP SHA-256: `99c47e28c1707436d7dfa75dcb776f5a0865b2288f1ac16d1baee8d6684c7827`
- Python: 3.11.9
- Runner image: Ubuntu 22.04.5 LTS
- The archive was downloaded and independently checked locally: its ZIP SHA-256 matches the GitHub artifact digest, and every entry in its internal `SHA256SUMS.txt` verified successfully.

### Independent issue reproducer

Same test selector: `test_issue_435_override_lower_scope`.

- Buggy base: test fails with `AssertionError: 1 != 42`.
- Fixed revision: same test passes.
- No test collection/import error is reported in either run.

### Exact dataset FAIL_TO_PASS set

The exact Parquet row is `reagento__dishka-436`, repository `reagento/dishka`, base commit `8718d5af93f9e48bc2506c64827663fdccc5ad89`, language Python, dataset license Apache-2.0. The Parquet file SHA-256 is `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`; canonical row SHA-256 is `c548969ec886af21b56c93daae34db1a86b3a10c8dd1473d3d5c886549a9e86d`.

- Buggy base: **8/8 selectors failed**. The raw log shows actual assertion, alias-resolution, context, and factory-registration failures in cross-scope override paths; it does not show a collection failure.
- Fixed revision: **8/8 same selectors passed**.
- Base log ends: `8 failed in 0.21s`.
- Fixed log: `8 passed in 0.05s`.

The eight exact selectors are stored in the immutable run artifact at `dataset-fail-to-pass-selectors.txt`. They cover cross-scope overrides for aliases, context providers and ordinary providers. These are different manifestations of the same provider-processing / cross-scope registry consistency defect family, not eight independent cases.

### Environment and license scope

The exact issue reproducer imports the pinned source via `PYTHONPATH`; it has no third-party runtime dependencies and no pip installs. The dataset selector environment is isolated and version-pinned (`pytest==8.3.5`, `iniconfig==2.0.0`, `packaging==24.2`, `pluggy==1.5.0`). Parquet extraction uses a separate isolated environment with `pyarrow==19.0.1`.

The exact base root license and project metadata declare Apache-2.0. The changed-file manifest records the implementation file and four changed test files under the repository license. The documentary screen identifies no obvious prohibition for this minimal reproduction scope. It is not legal advice and is not blanket clearance for optional integrations, the full development toolchain, or redistribution.

## Stage 3 — human technical adjudication

The project lead explicitly approved these decisions in this conversation on 2026-11-16; the human record is `reproduction/dishka_issue_435/HUMAN_ADJUDICATION_DECISION_DISHKA_435_V0_1_DRAFT_2026-11-16.md`:

- Gold: `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`.
- Alternatives: `A1_SCOPE_CHAIN_PRECEDENCE`, `A2_CONSUMER_BINDING_OR_CACHE`.
- E3: G1, A1 and A2 remain possible.
- E2: A2 is eliminated; G1 and A1 remain.
- E1: G1 remains as the sole surviving mechanism.

The source-level chain is coherent with the exact reproducer: the buggy builder inserts factories into per-scope registries during provider processing; a later cross-scope override updates the final processed-factory mapping but does not remove the earlier per-scope entry. Request-local lookup can therefore return the stale factory. The fixed builder delays registry construction and populates it from the final processed-factory mapping.

## Independence and related-defect review

GitHub repository metadata for `reagento/dishka` reports repository ID `742987819`, `fork=false`, and `mirror_url=null`. This is the upstream project, not a fork or mirror.

The frozen primary cohort contains one row for this upstream repository (rank 2). The one-case-per-upstream-project rule remains in force; no second row from the same project may be counted as an independent case.

Related issues reviewed:

- #420 / PR #421 concerns PEP 695 generic inheritance and `WithParents` type-variable resolution in `entities/with_parents.py`; its mechanism is distinct from #435's cross-scope factory registry construction.
- #466 / PR #468 concerns implicit `from_context` registration and override validation; despite touching `registry_builder.py`, its changed path is context-provider validation/root-context construction, not the stale per-scope override mechanism in #435.
- #275 requests in-place container provider override as a feature; it is not a report of this defect.
- #16 is an enhancement about requiring explicit provider overrides.

These related project issues are retained in the review trail, not merged into #435's defect cluster. No other accepted case currently exists in the case registry, and no other primary cohort row for this repository is eligible to be counted.

## Exposure and limitations to preserve

- Researcher source exposure: **full**. The student researcher has reviewed the issue, patch, source code and tests during candidate selection and adjudication. Do not claim perfect blinding.
- Prior model-output/pipeline-debug exposure: **none**. No model inference, model-output scoring or model-guided debugging has been performed.
- The issue and PR dates are later than the pinned Qwen2.5-3B-Instruct public release period in September 2024. This lowers the likelihood that this exact later public issue/patch was in those released weights, but does not establish the model's complete training-data cutoff or prove absence of related knowledge in training.
- Human adjudication is single-rater: the student project lead is the one human adjudicator. ChatGPT's critique is advisory AI input, not a second human rating. No human-human inter-rater reliability or Cohen's kappa claim is allowed.

## Timestamp and post-run snapshot reconciliation

The dataset row is PR-derived:

- PR #436 created: `2025-04-15T22:52:26Z` — exact match to the dataset row's `created_at`.
- Defect issue #435 created: `2025-04-14T17:22:16Z` — separate source resource and different timestamp.

The run artifact's historical `issue-pr-snapshot-sha256.txt` recorded the pre-correction issue snapshot hash `62ee31658aca98a51d2ff1505b44f857294f431f169fba1fff2e2a849b96c49f`, whose `created_at` field incorrectly copied the PR timestamp. The source snapshot was subsequently corrected against the GitHub issue endpoint. The current corrected issue snapshot content SHA-256 is `086ee0aba856f76397da74a704d98cc8a82e40e165739d9cc352b202d103e8f3`; the current PR snapshot content SHA-256 remains `f87785a9189d468e4211ec60aeddf7fdaa1677915fce5dc2c7b3e7a658103d58`.

This is a source-snapshot metadata correction after the reproduction run, not a change to the code, environment, test selector, or raw test result. The raw artifact remains immutable and its original snapshot-hash file is preserved. The separate resource reconciliation record corrects the old CSV's `is_pull_request=false` field for PR #436. The phrase in that historical note saying the issue was “created at the same timestamp” is inaccurate; the present record supersedes it with the exact separate timestamps.

## Current decision

**Stage 2 PASS. Stage 3 PASS. Final case acceptance remains pending.** Before adding this record to the accepted registry, the project lead must acknowledge the disclosed full researcher-source exposure and the single-human-adjudicator limitation, and the complete acceptance record must pass the schema and registry validator. None of these remaining steps authorizes model inference.
