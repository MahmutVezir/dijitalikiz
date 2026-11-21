# PyFar #721 — project-lead gold and evidence-tier decision

Date: 2026-11-21  
Project: TÜBİTAK 2204-A — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
Candidate: pyfar/pyfar issue #721 / fix PR #722  
Dataset instance: `pyfar__pyfar-722`  
Decision-maker: Student project lead  
Decision basis: Explicit approval in the project lead's conversation on 2026-11-21  
Status: **GOLD MECHANISM AND EVIDENCE-TIER DECISIONS APPROVED; CASE NOT ACCEPTED**

## 1. Decision

The project lead approves the following source-aware gold mechanism:

**G1 — `ENERGY_POWER_TARGET_AND_REFERENCE_NOT_SQUARE_ROOTED`**

In the exact buggy implementation, the energy/power normalization path scales signal amplitude using the unrooted ratio `target / reference_norm`. Since energy and power are quadratic in signal amplitude, this does not generally produce the requested energetic target. The corresponding amplitude factor is `sqrt(target / reference_norm)`.

The approval is specifically limited to the defective `energy` and `power` normalization branches. It does **not** claim that the RMS branch has the same defect; RMS is already amplitude-linear.

The project lead also approves the following evidence-tier decisions:

| Tier | Approved outcome |
|---|---|
| E3 — issue narrative and reported symptom | **ABSTAIN** |
| E2 — E3 plus frozen exact-buggy-base selector outputs | **ABSTAIN** |
| E1 — E2 plus immutable exact-base source evidence | **ANSWER** |

## 2. Rationale and evidence boundaries

- **E3 — ABSTAIN:** the issue narrative establishes the symptom and expected energetic target but does not identify the implementation mechanism. Measurement semantics, target interpretation, and normalization scaling remain plausible explanations.
- **E2 — ABSTAIN:** the exact pinned buggy base reproduces the reported class of failure, while the same frozen selectors pass on the fixed revision. This strengthens symptom attribution but does not, by itself, establish the causal source-level mechanism.
- **E2 selector limitation:** the 23 selectors originate from the upstream PR-added regression-test suite. They are one selector set, not 23 independent cases, and not a separately authored issue-level reproducer. No claim of independent reproductions or independent test oracles is made.
- **E1 — ANSWER:** immutable exact-base source excerpts show that energy and power are quadratic in amplitude while the buggy normalization path applies the unrooted target/reference ratio. The source chain distinguishes the proposed G1 mechanism from the lower-tier alternatives.
- The fixed patch is not to be exposed in the model-visible diagnostic evidence packet when evaluating diagnosis from evidence rather than patch recognition.

## 3. Scope explicitly not approved by this decision

This decision does **not**:

1. approve the prepared issue-family independence review;
2. grant legal clearance or authorize redistribution/use beyond a separately documented bounded research-scope acknowledgement;
3. close dataset-card README pinning/provenance, dependency-license, bundled/native-component, or notice reviews;
4. accept PyFar #721 as a final case or add it to the v0.2 accepted registry;
5. authorize model loading, inference, fine-tuning, or training.

The prior pipeline/debug exposure declaration remains `none` by direct project-lead self-report, not independently witnessed or externally audited. Researcher source exposure remains `full`; no blinded adjudication or inter-rater reliability claim is made.

## 4. Required next gates

1. Project-lead review of the prepared issue-family independence disposition.
2. Complete pinned dataset-card README/bytes provenance, canonical dependency-license, bundled/native-component and notice checks.
3. Obtain bounded research-scope acknowledgement only after those reviews are complete; do not describe it as legal clearance.
4. Complete the proposed case record and fail-closed validation.
5. Obtain a separate final project-lead YES/NO case-acceptance decision.

Until those gates and the separate final acceptance are completed, PyFar remains outside the accepted registry and inference remains unauthorized.
