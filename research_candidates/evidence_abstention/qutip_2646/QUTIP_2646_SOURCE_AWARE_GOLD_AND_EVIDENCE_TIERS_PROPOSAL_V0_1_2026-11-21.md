# QuTiP #2646 — source-aware gold and E1/E2/E3 proposal

**Date:** 21 November 2026  
**Candidate:** qutip/qutip issue #2646 / fix PR #2694  
**Dataset row:** qutip__qutip-2694  
**Status:** ADVISORY PROPOSAL ONLY — NOT PROJECT-LEAD APPROVED; PROMPT/SELECTOR SCOPE CAVEAT; CASE NOT ACCEPTED

## 1. Candidate contract

Issue #2646 reports that passing an existing QuTiP `Coefficient` into `QobjEvo` with an updated `args` mapping does not change the coefficient's evaluated arguments. The issue asks whether this is an API misuse or a defect.

PR #2694 fixes the public `coefficient()` factory's handling of an existing `Coefficient`: when a new args mapping is supplied, the factory's builder path must apply `replace_arguments(args)` rather than return the original coefficient unchanged. The PR also changes mutable defaults to `None` and normalizes absent mappings to empty dictionaries. The core gold is the existing-Coefficient re-wrapping path, not a general claim that all QobjEvo argument updates are defective.

**Scope discrepancy:** the issue body demonstrates the symptom through QobjEvo, but the issue code has `args={"g:2"}`, a set literal, not the intended mapping `{"g": 2}`. The frozen dataset selector and the Stage 2 reproducer instead exercise `coefficient(existing_coefficient, args={...})` directly. The issue comments explicitly connect that narrower factory defect back to the reported QobjEvo behavior. Preserve this gap; do not claim the Stage 2 reproducer is a verbatim executable replay of the issue snippet.

## 2. Proposed gold mechanism

**G1 — `COEFFICIENT_BUILDER_PASSTHROUGH_DISCARDS_UPDATED_ARGS`.**

In the exact buggy base, the public `coefficient()` factory registers the `Coefficient` type to a builder helper named `_return`. The factory constructs a kwargs mapping containing `args`, selects the builder with `isinstance(base, type_)`, and calls that builder with `**kwargs`. The buggy `_return(base, **kwargs)` immediately returns `base` without consuming `args` and without calling `base.replace_arguments(args)`. Therefore, wrapping an existing FunctionCoefficient with a new args mapping returns the unchanged original coefficient and it continues to evaluate using the old values.

The defect is specific to the builder path for an already-created `Coefficient`. It does not mean that `FunctionCoefficient.replace_arguments` is generally broken; exact-base source shows that method merges the replacement mapping and constructs a new FunctionCoefficient.

## 3. Predeclared alternative explanations

- **A1 — QobjEvo-only argument handling defect:** the QobjEvo constructor may fail to apply its `args` mapping, while direct use of `coefficient(existing_coefficient, args=...)` may work.
- **A2 — coefficient-factory dispatch/kwargs forwarding defect:** the public factory may select the wrong builder or fail to pass the `args` mapping to the selected builder.
- **A3 — FunctionCoefficient replacement implementation defect:** `replace_arguments` may itself fail to construct a new coefficient with updated values.
- **G1 — passthrough builder discards args:** the factory passes `args` into `_return`, but `_return` returns the original object without applying the replacement.

These are competing mechanisms. They are not claims of equal likelihood.

## 4. Proposed E3/E2/E1 tiers

### E3 — proposed ABSTAIN

Evidence is limited to the frozen dataset `problem_statement`: the issue title and body, including the QobjEvo symptom, the reporter's question about bug versus incorrect usage, and the exact sample code as written.

E3 establishes an externally visible mismatch but does not identify whether the problem lies in QobjEvo argument parsing, the coefficient factory, builder dispatch, or replacement behavior. The code literal `args={"g:2"}` is a set rather than the described dictionary and prevents the sample from serving as a clean executable reproduction without correction.

E3 ABSTAIN is a plausible proposal under a rubric requiring source-backed causal diagnosis. The malformed code sample is a sample-quality risk and should be explicitly reviewed by the project lead. Do not repair the text in the model-visible E3 packet.

### E2 — proposed ABSTAIN

Evidence:
- E3 unchanged;
- the independent public-API reproducer calls `qt.coefficient(original, args={"a": 2})` directly, without constructing a QobjEvo;
- the exact buggy-base output remains `1` instead of requested `2`;
- the exact frozen dataset selector `qutip/tests/core/test_coefficient.py::test_coefficient_update_args` exhibits the same base failure and fixed-revision pass.

This eliminates A1 as the sole explanation: the stale-argument behavior also occurs outside QobjEvo when the public coefficient factory is used directly. However, E2 does not show whether the args mapping is dropped by the factory dispatch, ignored by the selected `_return` builder, or passed to a replacement method that fails. A2, A3, and G1 remain plausible. E2 therefore meets the strengthened criterion of eliminating at least one alternative while retaining at least two.

### E1 — proposed ANSWER

Evidence:
- E2 unchanged;
- exact-base `QobjEvo.__init__` and `_read_element` source showing the QobjEvo `args` mapping is passed to `coefficient(op[1], args=args, ...)`;
- exact-base `coefficient()` source showing `args` is included in kwargs and the existing `Coefficient` is dispatched to the registered `_return` builder;
- exact-base `_return` body showing that it returns `base` unchanged and ignores the kwargs;
- exact-base `FunctionCoefficient.replace_arguments` implementation showing that it merges the new args and constructs a new coefficient.

These excerpts distinguish G1 from A2 and A3. The exact bug is the `_return` passthrough that discards the supplied `args` mapping. The fixed PR and post-fix source remain hidden technical-gold validation and must not be included in model-visible E1 evidence.

## 5. Evidence-elimination matrix

Full row-by-row source and artifact audit:

research_candidates/evidence_abstention/qutip_2646/QUTIP_2646_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md

Surviving mechanisms:
- E3: G1, A1, A2, A3.
- E2: G1, A2, A3.
- E1: G1.

## 6. Researcher exposure and issue comments

The public issue comments include a maintainer response that the `args` behavior is a bug and a later comment that directly identifies the coefficient factory as failing to update arguments, together with a minimal coefficient re-wrapping example. Those comments were reviewed during this audit.

The model-visible E3 packet is defined by the authenticated dataset `problem_statement`, which does not include issue comments. Do not add comments, PR discussion, or patch text to E3. Researcher source exposure is therefore full; perfect blinding must not be claimed.

## 7. Temporal exposure

The pinned study model is Qwen/Qwen2.5-3B-Instruct at revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`. Qwen announced Qwen2.5 on 19 September 2024. The QuTiP issue was opened on 5 March 2025 and PR #2694 on 15 May 2025. The candidate-specific issue and patch therefore postdate the public model release and pinned repository revision. This makes exposure to the exact issue/PR less likely for the pinned checkpoint, but does not prove the model's complete training-data cutoff or rule out pre-existing QuTiP source-code exposure.

Sources:
- Qwen Team, Qwen2.5 announcement, 19 September 2024: https://qwenlm.github.io/blog/qwen2.5/
- Qwen2.5-3B-Instruct model card: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- Pinned model revision: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/tree/aa8e72537993ba99e69dfaafa59ed015b17504d1

## 8. Methodological and acceptance boundaries

- Stage 2 exact-base/fixed reproduction and artifact integrity: passed for the one-test reproducer snapshot actually run.
- Expanded three-test follow-up reproducer: committed but not yet backed by a verified CI result; do not count its results.
- Prompt/selector scope discrepancy and malformed `args` literal: explicit project-lead sample-suitability review required.
- Project-lead gold/tier approval: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Researcher source exposure: full; no blind adjudication or inter-rater reliability claim.
- Temporal assessment: issue/PR-specific exposure less likely by chronology; pre-existing source exposure and exact model training-data cutoff remain unverified.
- Root BSD-3-Clause license and dependency/bundled notices: human review pending; no legal clearance claim.
- Bounded research-scope acknowledgement, schema-conformant case record and fail-closed validation: pending.
- Final case acceptance: not accepted; registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.