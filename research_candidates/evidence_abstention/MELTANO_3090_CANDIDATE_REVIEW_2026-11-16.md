# meltano/sdk issue #3090 — candidate review

**Cohort rank:** 26 of 96 primary candidates  
**Dataset instance:** meltano__sdk-3091 (exact row identity to be authenticated by the workflow)  
**Issue:** https://github.com/meltano/sdk/issues/3090  
**Fix PR:** https://github.com/meltano/sdk/pull/3091  
**Review status:** issue/patch/source contract and minimal direct reproducer prepared; exact dataset row and selector execution pending. Not an accepted case.

## 1. Defect contract

Issue #3090 demonstrates that two sibling properties in one JSON Schema both reference the same component. The first property resolves correctly, but the second becomes an empty object. The exact base implementation carries a mutable visited_refs set through sibling recursion. Once the first property resolves the component, the second sibling is incorrectly treated as a circular reference even though it is not on the current recursion path.

PR #3091 changes the state from a shared mutable set to an immutable tuple representing the current recursion stack. This prevents repeated sibling references from being mistaken for cycles while preserving protection against genuine recursive references.

The independent reproducer loads the exact upstream schema.py source by file path (without importing the full SDK package), calls resolve_schema_references with two sibling references to the same component, and requires both properties to resolve to {type: number}.

## 2. Pinned source identity

- Repository: meltano/sdk
- Buggy base: ae326fe394ec15d528ec2f1e396b8bb3dd5e99a2
- Fixed PR head: 9505ff1989b9be4d53b5bc9664b3fe3885879cb1
- Merge commit: 948bcec790bafebbb571cf3c0d58116a49d6f6aa
- Issue #3090 created: 2025-06-12T01:45:49Z
- PR #3091 created: 2025-06-12T01:47:30Z
- Exact-base root LICENSE Git blob: 564273905d22b60a0deb1155ece4281c0b855cbc
- Exact-base pyproject.toml Git blob: baae3360646db13ca761362cd99724176016031d
- Exact-base schema.py Git blob: 035851fe4c3cb574b8015cf7f44da278cb4f1767
- Fixed schema.py Git blob: 7754f835e4b11d13a4778669fb94a68c461b9f40
- Exact-base license declaration: Apache-2.0.

## 3. Reproduction and dependency scope

The independent reproducer imports only the exact schema.py file via importlib and requires referencing. The dataset regression selector imports the SDK package through the existing deprecated _singerlib shim, so the workflow uses a pinned subset of the exact base package's declared runtime dependencies plus pytest. All installed distribution license metadata is recorded before upstream source tests.

No external services, remote fixtures, or private data are used. This is a narrow test-environment license screen, not blanket legal clearance for every optional Singer SDK extra or redistribution.

## 4. Dataset selector requirement

The workflow authenticates the exact Parquet row meltano__sdk-3091, records its canonical row hash and FAIL_TO_PASS selectors, and applies the exact PR diff to the buggy base. Every selector must fail on the buggy base for the repeated-reference defect and pass on the fixed PR head. A collection/import/dependency failure is not counted as a reproduction.

## 5. Independence and exposure

- The frozen primary cohort contains one meltano/sdk candidate; this repository can contribute at most one accepted case.
- Issue and PR were created on 2025-06-12, after the September 2024 public release of the pinned Qwen2.5-3B-Instruct family. This temporal ordering lowers the likelihood that the exact public issue/patch was present in the released weights, but does not prove the model's full training-data cutoff.
- The student researcher has reviewed the issue and PR during candidate screening; perfect blinding must not be claimed.
- Related issue-family and repository-lineage review remains required.

## 6. Current decision

Issue/patch alignment: strong.  
Independent source reproducer: prepared; workflow pending.  
Dataset FAIL_TO_PASS selectors: pending exact-row authentication and execution.  
Minimal dependency/license inventory: pending workflow evidence and human review.  
Gold mechanism and E1/E2/E3 packet: pending human adjudication.  
Final case acceptance: not accepted.  
Model loading/inference authorization: false.

## Superseding Stage 2 addendum — 20 November 2026

The Meltano #3090 reproduction job completed successfully in two recorded candidate-matrix runs. The latest branch repeat is:
- Workflow run: 44331092872; job: 134895968235 — success.
- Artifact: 14440520435; GitHub-reported SHA-256: b1336169d7b6d8e4e47edbcd920d842ad525c7a4e2df841b998182099bed1bd3.
- The independent source reproducer executed against the exact buggy base and failed on the second sibling reference as expected; the same reproducer passed on the exact fixed revision.
- The exact frozen dataset selector was authenticated and failed on the test-only patched buggy base, then passed on the fixed revision.
- The row timestamp was authenticated against the linked PR resource.

The issue and reproducer agree on one mechanism: a mutable visited_refs set is shared between sibling schema-property branches. After resolving the first property's $ref, the second identical $ref is incorrectly treated as a cycle and left as an empty object. PR #3091 changes this to recursion-path state, preserving cycle protection without treating sibling reuse as recursion.

PR #3091 identifies #3009 as the introduction history. Record that relationship in the issue-family/lineage review; it does not create a second sample case. Meltano contributes at most one upstream-project case.

**Current disposition:** Stage 2 technical reproduction PASS; candidate remains not accepted. Project-lead source-aware gold/E1-E2-E3 decision, candidate-specific prior pipeline/debug exposure declaration, bounded source/dependency/dataset license-scope acknowledgement, related-issue/lineage review, complete proposed case record and fail-closed registry validation remain open. The earlier sections saying the exact row/selectors/reproducer were pending are historical and superseded by this addendum.

## Project-lead selection decision

## Project-lead first-batch selection — 20 November 2026

The student project lead explicitly accepted Meltano SDK #3090 as one of the strong first-batch candidates to continue through v0.2 Stage 3 case evaluation, applying the unchanged Dishka-equivalent criteria.

This is candidate-selection approval only. It does **not** approve the proposed Meltano gold mechanism or E1/E2/E3 tier membership; those remain for a separate source-aware project-lead decision. The bounded source/dependency/dataset scope acknowledgement, candidate-specific prior pipeline/debug exposure declaration, related issue/lineage review, complete case record, fail-closed registry validation and separate final case YES/NO remain pending.

PR #3091's link to #3009 remains introduction history for the same Meltano repository and does not create another independent case. This candidate remains not accepted as a final case. No model load, inference, fine-tuning or training is authorized.


## Stage 3 advisory and integrity addendum — 21 November 2026

The Stage 2 artifact was independently downloaded and locally rechecked:
- Run 44331092872; artifact 14440520435.
- Recomputed ZIP SHA-256: b1336169d7b6d8e4e47edbcd920d842ad525c7a4e2df841b998182099bed1bd3, matching GitHub's digest.
- ZIP CRC test passed.
- Internal SHA256SUMS manifest verified 14/14 files.

Prepared the following Stage 3 documents. They are proposals/reviews, not project-lead approvals or case acceptance:
- Gold and tier proposal: research_candidates/evidence_abstention/meltano_3090/MELTANO_3090_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_2026-11-21.md
- Issue-family/repository independence review: research_candidates/evidence_abstention/meltano_3090/MELTANO_3090_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-21.json
- Bounded license-scope review: research_candidates/evidence_abstention/meltano_3090/MELTANO_3090_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-21.json
- Local artifact integrity record: research_candidates/evidence_abstention/meltano_3090/MELTANO_3090_STAGE2_ARTIFACT_INTEGRITY_REVIEW_2026-11-21.md

The source-aware gold proposal is G1: one mutable visited_refs set is shared across sibling property branches. After the first sibling resolves a component reference, the second sibling is incorrectly treated as a recursive cycle and returns after its $ref is removed. The proposed tiers are E3 ABSTAIN, E2 ABSTAIN, E1 ANSWER. E3 and E2 intentionally retain the same causal hypotheses: reproduction confirms the symptom but does not expose internal state ownership. Only the exact base/fixed source snapshots in E1 distinguish G1 from the alternatives.

The issue-family review treats PR #3009 as the prior introduction of circular-reference tracking in the same resolver path, not as another independent case. The one-case-per-upstream-project rule is preserved.

The license-scope review is deliberately not closed:
- The exact-base root repository license is recorded as Apache-2.0.
- The dataset row's upstream repository license field is Apache-2.0, while the current dataset card identifies its distribution license as CC-BY-4.0. These are distinct layers.
- Hugging Face's README history shows the data upload at fb9aa22 and a separate README/card upload at 6fe2932 on the same date. The full immutable README commit SHA and exact card bytes have not yet been captured in the case evidence bundle; exact pinned-card review remains pending.
- The installed package inventory has 32 distribution entries; eight have a null raw license field, two lack license classifiers, and some entries have multiple license classifiers. Canonical license text/notices and full transitive dependency scope remain human-review items.

The candidate review already records that the researcher reviewed the issue and PR during screening. The source-aware analysis has now also been discussed in this workflow; do not claim blinding. Candidate-specific prior pipeline/debug exposure is still awaiting the project lead's explicit declaration. No “none” value is inferred.

**Current disposition remains:** Stage 2 technical pass; Stage 3 technical gold/tier proposal prepared but not approved; license scope not acknowledged; exposure declaration pending; no final proposed case record; not in the registry; no model execution authorization.


## Project-lead technical gold and evidence-tier decision — 21 November 2026

The project lead explicitly approved the source-aware technical gold and evidence tiers for Meltano SDK #3090:
- **G1:** shared mutable `visited_refs` state leaks across sibling JSON Schema property branches; after the first sibling resolves a reference, the second sibling is incorrectly stopped by the visited-reference guard and returns without resolving the target.
- **E3 — ABSTAIN:** the issue narrative contains the tentative “presumably already visited” clue, but this is a hypothesis rather than proof of sibling-shared traversal state.
- **E2 — ABSTAIN:** the frozen dataset selector and independent public-API reproducer confirm exact buggy-base failure and fixed-revision success, but do not expose the internal causal mechanism.
- **E1 — ANSWER:** the pinned buggy/fixed source snapshots show the mutable set, sibling propagation, early guard, and immutable recursion-path tuple fix.

The decision is source-aware and single-adjudicator; the researcher had already reviewed the issue and PR, so no blinding or independent second-rater claim is made. The reporter's tentative clue remains visible in E3 rather than being erased or overstated.

This closes only Stage 3 technical gold/tier adjudication. Candidate-specific prior pipeline/debug exposure remains pending; the bounded source/dependency/dataset license scope remains open; no final case record or separate final YES/NO acceptance has been made. Meltano remains outside the v0.2 registry, accepted counts remain 2 cases from 2 projects, and model loading/inference/fine-tuning/training remain unauthorized. PR #3009 remains repository lineage, not a second case.

Decision record: `research_candidates/evidence_abstention/meltano_3090/PROJECT_LEAD_GOLD_AND_EVIDENCE_TIER_DECISION_MELTANO_3090_2026-11-21.md`.


## Post-approval validation addendum — 21 November 2026

The decision-record assertion was aligned with the exact wording in the project-lead decision file. The corrected branch head `864896d4cfb12cbe68c76eab2abd3edf0929f21c` passed:
- Evidence Abstention Preflight run 44899668556: success; v0.2 acceptance/readiness tests 27 passed; design/scoring tests 10 passed. The readiness report retains 13 blockers, 2 accepted cases from 2 projects, `ready_for_inference=false`, and `inference_authorized=false`.
- Research Validation run 44899668507: 479 passed, 6 skipped, 56 subtests passed.
- Uncertainty unit tests run 44899668509: 171 tests passed.
- Qwen adapter CPU tests run 44899668410: success.
- Dymos repeat run 44899668525: success.

The Meltano approval and fail-closed status regression test is included in the 27-test v0.2 acceptance/readiness suite. This is validation of repository records and no-inference gates only; no model weights were loaded and no inference, fine-tuning or training was performed. The candidate remains outside the registry and its prior exposure and bounded license-scope acknowledgements remain open.
