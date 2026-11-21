# Project-lead technical gold and E1/E2/E3 decision — Dymos #1166

**Decision date:** 20 November 2026  
**Candidate:** OpenMDAO/dymos issue #1166; fix PR #1165  
**Decision owner:** Student project lead  
**Disposition:** APPROVED — source-aware exploratory technical gold and evidence-tier adjudication only

## Project-lead decision

The project lead explicitly approved the proposed technical gold mechanism and the proposed E3/E2/E1 evidence-tier decisions in the conversation on 20 November 2026, stating: **“Onaylıyorum ama projenin ilerleyişini bozmazsa.”**

This is interpreted as approval provided that the decision does not bypass or weaken the previously agreed project gates. Recording the decision does not disrupt the project sequence: it closes the source-aware gold/tier adjudication step within Stage 3 and leaves the license, dataset-card, case-record, registry, and final-acceptance gates in their existing order. No inference or model execution is enabled by this approval.

## Approved technical gold mechanism

On the exact buggy base `3efd1035c3bf62890034eb9e07de543f3d117867`:

1. `Phase.add_control` forwards the caller's `val` argument to `set_control_options` (`dymos/phase/phase.py:638–640`).
2. `set_control_options` stores it in `phase.control_options[name]['val']` (`phase.py:785–786`).
3. `TranscriptionBase` passes the same control-options mapping to `ControlInterpComp` (`dymos/transcriptions/transcription_base.py:145–147`).
4. In the active polynomial-control branch, `ControlInterpComp._configure_controls` initializes the component input using `val=np.ones(input_shape)` rather than the stored `options['val']` (`dymos/transcriptions/common/control_comp.py:95–120`).

**Approved gold:** the caller-provided polynomial-control default is stored and propagated to the interpolation component, but the buggy polynomial-control input initialization discards it by initializing the input to ones. This explains the observed `[[1.0], [1.0]]` values instead of the requested `[[5.0], [15.0]]`. The fixed PR head normalizes and uses `options['val']` for the input default.

The decision is limited to this issue-specific polynomial-control default-initialization mechanism. It does not claim exhaustive coverage of every Dymos transcription or control mode.

## Approved evidence-tier decisions

| Evidence tier | Evidence available to the model | Project-lead decision |
|---|---|---|
| E3 | Frozen issue narrative only | **ABSTAIN** — the symptom is described, but there is no reproducible observation or implementation-path evidence establishing the cause. |
| E2 | E3 plus independent public-API reproducer and observed buggy-base assertion output | **ABSTAIN** — the failure is observable and reproducible, but the implementation mechanism is not evidenced. A correct guess is not an evidence-supported diagnosis. |
| E1 | E2 plus the active pinned source chain from API forwarding and value storage through component configuration to the all-ones input default | **ANSWER** — the causal implementation path is sufficiently evidenced to state the approved gold mechanism. |

These decisions define the project's operational evidence threshold for this candidate. “ANSWER” means the response is supported by the supplied source evidence, not merely that the model happens to name the correct cause.

## Adjudication method and exposure

- This is the Dishka-equivalent v0.2 exploratory, source-aware, single-human-adjudicator route.
- The student project lead is the human adjudicator and has full source/reproduction exposure; no blinded adjudication is claimed.
- ChatGPT provided technical analysis and recommendations only; the project lead made the approval decision.
- Hasan's previously described contribution remains supplementary project-lead-reported technical concurrence only; no signed independent review or second gold adjudicator is claimed.
- This is not an inter-rater reliability result. The separate two-human-rater requirement for later blinded scoring of raw model outputs remains unchanged.

## Evidence and counting limits

- The frozen dataset selector and independent public-API reproducer are two reproduction routes for one Dymos defect, not two independent cases.
- Historical issue #531 remains a related predecessor in the same broad default-value family and is not counted as another case.
- The source-aware E1 packet is pinned to the exact buggy base; its packet-set SHA-256 is `7ca1e50290bc037e9147dc30eff10152cecc506e0cb1ac70de5c420cbf939474`.
- The project lead's prior pipeline/debug exposure declaration remains `none`; researcher source/reproduction exposure remains `full`.

## Explicitly not approved by this decision

This decision does **not** constitute:

- acknowledgement or approval of any source, dependency, binary-notice, dataset, or redistribution license scope;
- legal clearance;
- verification of the exact pinned dataset-card license;
- final acceptance of Dymos #1166 into the accepted case registry;
- authorization to load model weights, perform inference, fine-tuning, training, or any other model execution.

The bounded documentary license-scope acknowledgement, authentication of the exact pinned dataset-card license, schema-conformant case record, fail-closed registry validation, and separate final case YES/NO remain required. Until those gates are closed, Dymos remains a Stage 3 candidate and the existing readiness gate remains authoritative.
