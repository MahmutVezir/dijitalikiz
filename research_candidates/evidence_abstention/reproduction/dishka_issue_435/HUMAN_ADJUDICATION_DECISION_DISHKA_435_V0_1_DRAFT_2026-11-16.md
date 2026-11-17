# Dishka #435 — human adjudication decision record

**Record version:** 0.1 draft  
**Date prepared:** 2026-11-16; limitation acknowledgement added 2026-11-17  
**Status:** TECHNICAL GOLD / EVIDENCE-TIER ADJUDICATION AND LIMITATION ACKNOWLEDGEMENT APPROVED; FINAL CASE ACCEPTANCE GATES OPEN  
**Candidate:** `reagento__dishka-436`  
**Upstream project:** `reagento/dishka`  
**Issue / fix:** [Issue #435](https://github.com/reagento/dishka/issues/435) / [PR #436](https://github.com/reagento/dishka/pull/436)  
**Technical reproduction:** passed in GitHub Actions run [43881610067](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067)  
**Case acceptance:** NOT ACCEPTED  
**Model loading/inference authorization:** FALSE

## 1. Purpose and decision boundary

This record separates the technical recommendation from the student's human adjudication. The AI research assistant may propose a mechanism and critique the evidence tiers, but it is not a human co-investigator, independent human rater, or the decision-maker.

The project lead's explicit approvals were communicated in this conversation on 2026-11-16 and 2026-11-17. The first approval covers the proposed technical gold mechanism, the A1/A2 alternative set, and the E3/E2/E1 evidence-tier memberships and rationales. The second approval acknowledges the researcher-exposure and single-adjudicator limitations and accepts use of this case only within the exploratory feasibility design. These are human project-lead decisions, not AI-generated decisions. Neither approval closes the remaining case-acceptance gates or authorizes model loading or inference.

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

**Project-lead adjudication:** APPROVED on 2026-11-16. The student project lead accepts G1 as the technical gold mechanism, subject to the limitations and remaining gates recorded below.

## 4. Alternative mechanisms to adjudicate

- **A1_SCOPE_CHAIN_PRECEDENCE:** the observed value is due to ordinary local-scope-before-parent lookup semantics, rather than a stale registration. Prediction: a current-scope registration should shadow a parent registration whenever it exists; absent a stale local entry, the APP value should be returned.
- **A2_CONSUMER_BINDING_OR_CACHE:** the consumer factory or container cache captured an earlier value independently of registry population. Prediction: the wrong value would remain explainable without a stale request-scope factory entry, potentially differing between direct `get(int)` and resolving the `Interactor`.

**Project-lead adjudication:** A1 and A2 are accepted as the predeclared alternative mechanisms for this case's evidence-tier exercise. Their role is to define what evidence must distinguish; they are not asserted to be equally likely explanations.

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

**Project-lead adjudication:** APPROVED on 2026-11-16. The project lead accepts the proposed E3 → E2 → E1 hierarchy and its stated mechanism-survival rationale. This semantic approval does not replace the pending file/hash, provenance, and nested-set validation. Structural validation alone cannot prove that an evidence tier is semantically sufficient.

## 6. Exposure and limitations to preserve

- The student researcher has reviewed the issue and fix during candidate screening. The researcher therefore acknowledges **full source-level exposure to the case materials already reviewed**. Do not claim perfect blinding or a blinded human adjudication.
- This acknowledgement concerns the researcher's exposure. It does **not** establish whether the model encountered this issue, PR, or code during training. The pinned model family was publicly released before the issue/PR dates, which lowers the likelihood of exact post-release issue exposure but does not establish the model's complete training-data cutoff or prove absence from training.
- The proposed documentary license screen is limited to the minimal Python 3.11.9 reproducer environment; it is not legal advice or blanket clearance for optional dependencies or redistribution.
- The working design has **one human adjudicator: the student project lead**. ChatGPT's critique is advisory AI input, not a second human rating.
- Consequently, do not claim human-human inter-rater reliability, inter-rater agreement, or Cohen's kappa. No second-human-rater statistic will be manufactured or inferred from AI critique.

## 7. Student project lead decisions — recorded

### 7.1 Technical adjudication approval — 2026-11-16

The student project lead explicitly approved:

- [x] Accept `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION` as the technical gold mechanism.
- [x] Accept A1 and A2 as the predeclared alternatives used in the adjudication.
- [x] Accept the proposed E3, E2, and E1 evidence memberships and rationales.

**Human decision:** APPROVED — technical gold, alternatives, and evidence-tier design only.  
**Decision date:** 2026-11-16.  
**Amendments / rationale:** No amendments requested in the approval. The decision does not waive any remaining acceptance gate.

### 7.2 Researcher-exposure and single-adjudicator limitation acknowledgement — 2026-11-17

The student project lead explicitly confirmed in this conversation:

> “Bu dört sınırlamayı kabul ediyor ve Dishka vaka kaydına bu şekilde işlenmesini onaylıyorum eğer doğru bir onaylamaysa.”

The approval was given after the four limitations were clarified as follows:

- [x] **Researcher exposure:** acknowledge that the student has full source-level exposure to the Dishka issue/fix materials already reviewed; do not claim researcher blinding.
- [x] **Single human adjudicator:** acknowledge that the student project lead is the only human adjudicator; ChatGPT is not a second human rater.
- [x] **No inter-rater reliability claim:** do not claim human-human inter-rater agreement or Cohen's kappa.
- [x] **Exploratory use only:** use Dishka, if it passes all remaining gates, as a case in the exploratory feasibility study under these limitations; do not present it as confirmatory evidence or as an unrestricted demonstration of general performance.

**Human decision:** APPROVED — the four methodological limitations and exploratory-use boundary above.  
**Decision date:** 2026-11-17 (communicated in this conversation).  
**Scope:** This approval records acceptance of the limitations. It does not certify that the exposure audit, training-data contamination assessment, licensing review, independence check, evidence packet, or acceptance validator has passed.

## 8. Remaining case-acceptance gates

Even after the project lead signs off on the technical gold, evidence tiers, and limitations, separately verify:

1. exact dataset-row identity, timestamp/resource-type provenance, and row hash;
2. one-case-per-upstream-project independence and related-defect/fork lineage;
3. exposure classification and the model-training contamination limitation;
4. exact-base license and changed-file/dependency scope, with documentary evidence;
5. immutable evidence packet files, packet hashes, and provenance;
6. the case-acceptance schema and validator against the actual record.

Until all gates pass and the case record is formally accepted, the registry count remains zero and model inference remains unauthorized.
