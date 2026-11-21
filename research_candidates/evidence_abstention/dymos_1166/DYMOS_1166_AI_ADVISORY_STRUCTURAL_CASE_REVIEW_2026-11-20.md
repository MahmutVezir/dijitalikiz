# AI advisory note — proposed Dymos #1166 case record

Date: 2026-11-20  
Role: technical and structural advisory only; not a human adjudication or case-acceptance decision.

## Evidence and proposed tier logic

- E3 contains only the frozen issue narrative. It describes the symptom but does not establish a reproduced observation or causal implementation path. The approved project-lead outcome is ABSTAIN.
- E2 adds the fresh public-API reproducer and its buggy-base output. The reproducer constructs a fresh model, makes no post-setup `set_val` override, and reads the promoted control input directly. This removes the stale-fixture/post-setup-override and downstream ODE-output explanations, but it does not expose the active component input-initialization line. Shape-normalization versus incorrect component-default initialization therefore remains unresolved. The approved outcome is ABSTAIN.
- E1 adds the four active pinned buggy-base source excerpts showing API forwarding, option storage, propagation into `ControlInterpComp`, and the polynomial-control input initialized with `np.ones(input_shape)`. The approved outcome is ANSWER, limited to this mechanism and the pinned path.

The survivor sets used in the proposed case record are therefore:
- E3: gold mechanism plus three declared alternatives.
- E2: gold mechanism plus the remaining shape-normalization alternative.
- E1: gold mechanism only.

This nested structure is a representation of the project lead's already recorded human decision, not a new assistant decision.

## Reproduction and provenance limits

The dataset selector and independent public-API reproducer are two routes for one Dymos defect. They must never be counted as two cases. Historical issue #531 is a related predecessor, not a separate case. The selected dataset timestamp maps to PR #1165 creation, not the later issue #1166 creation; the case record must preserve that distinction.

## Scope and human-review limits

The project lead approved the bounded documentary scope with an explicit scientific-independence condition. The acknowledgement is not legal advice, formal legal review, legal clearance, or general redistribution permission. Full researcher source/reproduction exposure is disclosed; prior pipeline/debug exposure is the project lead's direct self-report, not an independently witnessed audit. No blinded-review or inter-rater reliability claim is made.

## State of the proposed record

The case record is proposed and may be structurally validated. It must not be added to the accepted registry until a separate project-lead final YES is recorded after fail-closed registry validation. Structural validation does not authenticate external artifacts, rerun upstream tests, decide legal questions, or authorize model inference. No model weights, inference, training, or fine-tuning are included or authorized by this note.
