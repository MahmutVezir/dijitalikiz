# Project-lead technical gold and evidence-tier decision — Meltano SDK #3090

**Decision:** APPROVED  
**Decision maker:** Student project lead  
**Decision timestamp:** 2026-11-21T11:27:00Z  
**Candidate:** meltano/sdk issue #3090 / fix PR #3091  
**Proposed case ID:** SRV2E-MELTANO_3090  
**Scope:** Stage 3 technical gold mechanism and E1/E2/E3 evidence-tier adjudication only

## 1. Explicit decision

The project lead approves the following source-aware technical gold and evidence-tier outcomes:

- **G1:** A shared mutable `visited_refs` set leaks traversal state across sibling JSON Schema property branches. After the first sibling resolves a component reference and adds its path to the shared set, the second sibling is incorrectly treated as a recursive cycle. Its `$ref` is removed and it returns without resolving the referenced schema.
- **E3 — ABSTAIN:** The issue narrative reports the symptom and includes the tentative phrase “presumably already visited.” That phrase is a hypothesis, not proof that mutable traversal state is shared across sibling branches.
- **E2 — ABSTAIN:** The frozen selector and independent public-API reproducer establish the failure on the exact buggy base and its correction on the exact fixed revision. They establish reproducibility, not the internal causal mechanism.
- **E1 — ANSWER:** The exact buggy and fixed source snapshots expose the shared mutable set, sibling call propagation, early visited-reference guard, and the fix's immutable recursion-path tuple. This source evidence supports G1 and discriminates it from the retained alternatives.

The surviving mechanism sets remain:
- E3: `{G1, A1, A2, A3}`
- E2: `{G1, A1, A2, A3}`
- E1: `{G1}`

## 2. Scientific rationale and limits

A correct guess at G1 from E3 or E2 is not an evidence-supported diagnosis. The E3 wording must preserve the reporter's tentative clue as a clue; it must not be rewritten as if no causal hint existed. E2 increases confidence that the reported behavior is real and fixed by the patch, but does not by itself identify whether traversal-state leakage, resolver behavior, aliasing, or schema merge behavior caused it. E1 contains the source-level evidence needed to support the mechanism.

This is a single source-aware project-lead adjudication. The researcher had previously reviewed the issue and PR, and the source-aware analysis has been discussed; no blinded adjudication, independent second-rater review, or inter-rater reliability claim is made. ChatGPT's prior recommendation is advisory input, not an independent human vote.

## 3. Explicitly out of scope

This decision:
- closes only the technical gold and evidence-tier decision within Stage 3;
- does **not** accept Meltano into the v0.2 exploratory registry;
- does **not** change the accepted case/project count (remains 2 cases from 2 upstream projects);
- does **not** resolve the candidate-specific prior pipeline/debug exposure declaration;
- does **not** acknowledge or clear the bounded source/dependency/dataset license scope;
- does **not** create a final case-acceptance record or constitute the separate final YES/NO acceptance decision;
- does **not** add related PR #3009 as another case;
- does **not** authorize model loading, inference, fine-tuning, or training.

## 4. Remaining gates

Before a final case decision, the project lead must separately provide the candidate-specific prior pipeline/debug exposure declaration and review/acknowledge or reject the bounded documentary-use scope after the outstanding dependency and immutable dataset-card evidence is reconciled. The proposed case record must then pass fail-closed structural validation, followed by a separate explicit final YES/NO case-acceptance decision.
