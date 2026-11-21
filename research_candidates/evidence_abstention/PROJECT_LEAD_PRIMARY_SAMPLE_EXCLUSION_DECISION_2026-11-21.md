# Project-lead decision: primary abstention sample exclusions

**Decision date:** 21 November 2026  
**Active study:** SWE-rebench V2 evidence-abstention, v0.2 exploratory/feasibility  
**Decision authority:** Student project lead  
**Source:** Explicit project-lead approval in the ChatGPT conversation on 21 November 2026  
**Public-record limitation:** This is a dated decision record, not a cryptographic signature. A more precise approval timestamp is not asserted.

## 1. Decision

The project lead **approves exclusion of the following six candidates from the current primary abstention sample** because their frozen issue-visible E3 material already gives away the core causal diagnosis or the intended repair direction to a degree that undermines a defensible E3 insufficient-evidence condition:

1. **msgspec #769 / PR #772** — the issue explicitly identifies the non-iterable `types.UnionType.__parameters__` descriptor, its TypeError, and a workaround that avoids the special case.
2. **Jinja #2032 / PR #2033** — the issue explicitly identifies missing `clear` and `pop` mutation guards for `MutableSequence` and supplies a `[].pop()` example.
3. **jsonpickle #564 / PR #565** — the issue supplies a minimal keyword-only constructor example, serialized `py/reduce` state, and a traceback at the constructor call.
4. **scikit-activeml #503 / PR #504** — the issue explicitly says that strategy-level `random_state` is not propagated to the cluster algorithm, shows the workaround, and demonstrates nondeterminism.
5. **Babel #1129 / PR #1141** — the issue explicitly states that seconds must be optional and default to zero when the locale format is `H:mm`.
6. **Gammapy #5524 / PR #5525** — the issue title and body explicitly say the phase-curve template is not normalized at initialization; the PR also changes a separate short-interval integral behavior not described in the issue.

The exact candidate review notes and frozen upstream references are maintained separately in the progress ledger.

## 2. Scope of the decision

For each of these six candidates:

- Primary abstention sample eligibility: **excluded**.
- Stage 2 / Stage 3 technical work already performed: preserve as evidence; do not erase or rewrite prior results.
- Further Stage 2 execution for primary-sample acceptance: **not authorized or required** under this decision.
- Accepted v0.2 case registry inclusion: **no**.
- Separate easy-answer / evidence-sufficient control-group assignment: **none**.
- Model loading, inference, fine-tuning or training: **not authorized**.

This is a sample-suitability decision. It is not a claim that the upstream defects are false, that the fixes are invalid, or that technical reproductions (where performed) did not happen.

## 3. Why no easy-answer control group is created

The current v0.2 exploratory design defines E1/E2/E3 evidence conditions and P0/P1 policies for the primary experiment. It does **not** define a separate easy-answer/evidence-sufficient control group, its allocation, scoring, sample-size treatment or analysis.

The six excluded candidates therefore remain screening/exclusion records. They are not silently repurposed as controls. Any future control group would require a prospective protocol amendment, explicit decision rules, and a separate versioned design before any such cases are used.

## 4. Registry and frozen-cohort invariants

- The frozen 96-row cohort source and its hashes remain unchanged.
- The v0.2 accepted-case registry is not modified by this exclusion decision.
- Existing accepted Dishka and EODAG case records remain unchanged.
- No rejected or excluded candidate is inserted into the accepted registry.
- The exclusion overlay is recorded in the Stage 2/Stage 3 progress ledger, with per-candidate reasons and links to the static review notes.
- The six candidates remain visible in the candidate ledger so the research audit trail is preserved.

## 5. Next sequential work

Continue candidate review in frozen cohort order, without lowering acceptance criteria. Do not skip unresolved earlier-ranked candidates solely to reach later rows. The next open gates are:

1. **GeoFileOps #649 (rank 49):** finish the Stage 3 sample-suitability review and the remaining project-lead evidence/exposure/license decisions.
2. **Lektor #1214 (rank 50):** retain the completed Stage 2 selector-integrity exclusion; do not rerun or trim the frozen row.
3. **music21 #1736 (rank 51):** authenticate its exact frozen row and resolve E3 suitability / mixed patch-scope questions.
4. **GeoPandas #3591 (rank 52):** authenticate its exact frozen row and obtain the project-lead E3 and exposure decisions.
5. Continue to rank 55 onward only after earlier open gates are resolved or formally excluded.

This decision does not authorize model execution. All existing no-inference restrictions remain in force.
