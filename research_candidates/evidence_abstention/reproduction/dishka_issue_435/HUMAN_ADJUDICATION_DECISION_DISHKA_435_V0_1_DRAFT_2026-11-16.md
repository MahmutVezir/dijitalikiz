# Dishka #435 — human adjudication decision record

**Record version:** 0.1 draft  
**Date prepared:** 2026-11-16  
**Status:** DRAFT — awaiting student project lead's explicit adjudication  
**Candidate:** `reagento__dishka-436`  
**Upstream project:** `reagento/dishka`  
**Issue / fix:** [Issue #435](https://github.com/reagento/dishka/issues/435) / [PR #436](https://github.com/reagento/dishka/pull/436)  
**Technical reproduction:** passed in GitHub Actions run [43881610067](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067)  
**Case acceptance:** NOT ACCEPTED  
**Model loading/inference authorization:** FALSE

## 1. Purpose and decision boundary

This record separates the technical recommendation from the student's human adjudication. The AI research assistant may propose a mechanism and critique the evidence tiers, but it is not a human co-investigator, independent human rater, or the decision-maker.

The student project lead must confirm, amend, or reject each proposed decision below. No field in this draft is evidence of human approval. Even after the proposed gold mechanism and evidence tiers are approved, the case remains unaccepted until every other case-acceptance gate is complete.

## 2. Technical reproduction already established

The pinned issue reproducer fails on the buggy base with `AssertionError: 1 != 42` and passes on the fixed revision. The same workflow applied the exact dataset test patch and reported all eight SWE-rebench FAIL_TO_PASS selectors failing on the buggy base and passing on the fixed revision.

- Workflow run: [43881610067](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067)
- Artifact: `dishka-issue-435-reproduction-43881610067-1`
- Artifact SHA-256: `99c47e28c1707436d7dfa75dcb776f5a0865b2288f1ac16d1baee8d6684c7827`
- Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
- Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`
- Python: 3.11.9; Ubuntu 22.04.5 LTS

This is technical reproduction evidence, not semantic adjudication or case acceptance.

## 3. Proposed gold mechanism

**Proposed mechanism ID:** `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`

The buggy `RegistryBuilder._process_factory` inserts provider factories into their declared scope registry while providers are processed. When a later provider overrides the same dependency in another scope, the global `processed_factories[provides]` entry is updated, but the earlier per-scope entry remains. During resolution, the request-scoped registry is checked before falling back to its parent APP container. The stale request-scoped factory therefore returns `1`, shadowing the later APP-scoped override `42`.

The fixed revision defers registry construction until provider processing is complete and populates the scope registries from the final `processed_factories` mapping. The request then resolves to `42`.

**AI-assisted technical recommendation:** G1 is the strongest explanation and is supported by the pinned base/fixed implementation diff and cross-scope regression tests. It is suitable to be submitted to the project lead as the proposed gold mechanism.

## 4. Alternative mechanisms to adjudicate

- **A1_SCOPE_CHAIN_PRECEDENCE:** the observed value is due to ordinary local-scope-before-parent lookup semantics, rather than a stale registration. Prediction: a current-scope registration should shadow a parent registration whenever it exists; absent a stale local entry, the APP value should be returned.
- **A2_CONSUMER_BINDING_OR_CACHE:** the consumer factory or container cache captured an earlier value independently of registry population. Prediction: the wrong value would remain explainable without a stale request-scope factory entry, potentially differing between direct `get(int)` and resolving the `Interactor`.

The proposed G1 should be accepted as gold only if the evidence supports the predicted mechanism and excludes the alternatives at the appropriate evidence levels.

## 5. Proposed nested evidence tiers

### E3 — insufficient evidence

Visible material: issue snapshot, independent issue reproducer, and base/fixed reproduction logs.

Proposed surviving mechanisms: `G1`, `A1`, `A2`.

Rationale: the issue and output establish the cross-scope override failure and expected value, but do not reveal the internal resolution path. A model seeing only E3 should not be expected to distinguish the three mechanisms.

### E2 — partial evidence

E3 material is retained unchanged, with the exact buggy-base container lookup and registry lookup source snapshots added.

Proposed surviving mechanisms: `G1`, `A1`.

Rationale: the fresh-container reproducer and lookup path make a prior cached value or captured consumer value an inadequate explanation. However, E2 does not yet explain why the request-scope registry contains the earlier factory.

### E1 — sufficient evidence

E2 material is retained unchanged, with the exact buggy-base and fixed registry-builder source, their diff, and the upstream cross-scope regression test added.

Proposed surviving mechanism: `G1` only.

Rationale: the base implementation shows the per-scope insertion during provider processing; the fixed implementation defers insertion and builds from the final winning factory map. The upstream cross-scope test distinguishes this stale-entry mechanism from ordinary scope-chain precedence.

**AI-assisted tier recommendation:** the E3 → E2 → E1 progression is logically coherent: each stronger tier adds source-level evidence that removes at least one alternative, while preserving the lower-tier evidence unchanged. The proposed evidence sets must still pass file/hash, provenance, and nested-set validation. Structural validation alone cannot prove that an evidence tier is semantically sufficient.

## 6. Exposure and limitations to preserve

- The student researcher has reviewed the issue and fix during candidate screening. Do not claim perfect blinding.
- The pinned model family was publicly released before the issue/PR dates, which lowers the likelihood of exact post-release issue exposure but does not establish the model's complete training-data cutoff or prove absence from training.
- The proposed documentary license screen is limited to the minimal Python 3.11.9 reproducer environment; it is not legal advice or blanket clearance for optional dependencies or redistribution.
- The working design has one human adjudicator. ChatGPT's critique is advisory AI input, not a second human rating. Do not claim human-human inter-rater reliability or Cohen's kappa.

## 7. Student project lead decision — pending

The project lead should explicitly confirm or amend each item:

- [ ] I accept `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION` as the technical gold mechanism.
- [ ] I accept A1 and A2 as the predeclared alternatives used in the adjudication.
- [ ] I accept the proposed E3, E2, and E1 evidence memberships and rationales.
- [ ] I confirm that the researcher exposure and single-adjudicator limitations above are accurately recorded.

**Human decision:** PENDING — no decision has been recorded by this draft.  
**Decision date (UTC):** PENDING  
**Amendments / rationale:** PENDING

## 8. Remaining case-acceptance gates

Even after the project lead signs off on the technical gold and evidence tiers, separately verify:

1. exact dataset-row identity, timestamp/resource-type provenance, and row hash;
2. one-case-per-upstream-project independence and related-defect/fork lineage;
3. exposure classification and the model-training contamination limitation;
4. exact-base license and changed-file/dependency scope, with documentary evidence;
5. immutable evidence packet files, packet hashes, and provenance;
6. the case-acceptance schema and validator against the actual record.

Until all gates pass and the case record is accepted, the registry count remains zero and model inference remains unauthorized.
