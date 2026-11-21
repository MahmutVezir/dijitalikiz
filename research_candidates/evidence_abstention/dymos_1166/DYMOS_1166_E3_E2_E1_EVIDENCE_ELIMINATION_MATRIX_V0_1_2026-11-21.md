# Dymos #1166 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** OpenMDAO/dymos issue #1166 / fix PR #1165  
**Dataset row:** `openmdao__dymos-1165`  
**Status:** **SOURCE- AND PACKET-AUDITED MATRIX — EXISTING PROJECT-LEAD GOLD/TIER APPROVAL RETAINED; FINAL CASE ACCEPTANCE PENDING**

## 1. Purpose and decision

This audit applies the strengthened evidence-tier criterion:

> E2 must eliminate at least one predeclared plausible alternative while leaving at least two plausible mechanisms unresolved.

**Finding: the approved Dymos tier construction satisfies the criterion.** The E2 packet rules out two specific alternatives using the design of the independent reproducer and where it reads the output. It still leaves the main implementation defect (G1) and a value-shape normalization explanation (A1) plausible. E1's exact buggy-base source chain distinguishes G1 from A1.

The project lead already approved G1 and E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER on 20 November 2026. This matrix substantiates that existing decision; it does not change or replace the decision record.

## 2. Frozen provenance

- Issue: https://github.com/OpenMDAO/dymos/issues/1166
- Fix PR: https://github.com/OpenMDAO/dymos/pull/1165
- Exact buggy base: `3efd1035c3bf62890034eb9e07de543f3d117867`
- Exact fixed PR head: `0ffc82225d6125dcb5c5b5acfb9be9fd712ef949`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row: `openmdao__dymos-1165`
- Independent reproducer:
  `research_candidates/evidence_abstention/reproduction/dymos_issue_1166/test_issue_1166.py`
- Frozen selector:
  `dymos/examples/balanced_field/test/test_balanced_field_length.py::TestBalancedFieldLengthDefaultValues::test_default_vals_stick`
- Operational packet set:
  `research_candidates/evidence_abstention/dymos_1166/OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_1_2026-11-20.json`
- E3 packet SHA-256: `3aa2320ac5fc464108e3a4e79a6a062c80708caec0bc9e332fe6cd742a6bfb53`
- E2 packet SHA-256: `7c16c6c61dadb5217493946b42b2b02a9dbdc63a0500b2e51b66982f4439385b`
- E1 packet SHA-256: `8d78d4ac4828276485b73bb01f5411be42feec328418cd575aa828ddae0faaa5`
- Project-lead decision:
  `research_candidates/evidence_abstention/dymos_1166/PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_DYMOS_1166_2026-11-20.md`
- Latest repeated exact-base/fixed-revision issue-level reproducer: workflow `44904689950`, job `136847632352`, artifact `14706839946`; base output `[[1.0], [1.0]]` instead of `[[5.0], [15.0]]`; identical fixed-revision reproducer passed (1 test). The artifact was independently downloaded and checked: SHA-256 matched, ZIP CRC passed, internal hashes 15/15.

## 3. Predeclared alternative mechanisms

| ID | Alternative mechanism | Distinguishing prediction |
|---|---|---|
| G1 | The caller-provided polynomial-control `val` is forwarded and stored, but the active polynomial-control input initialization discards it and initializes the input to ones. | A fresh model reads all ones at the promoted control input on the buggy base; the exact source path shows the stored value is not used by the active `add_input` statement. |
| A1 | Polynomial value shape normalization/broadcasting prevents the supplied default from being represented correctly. | Without the active source path, a correctly shaped list may still be transformed or rejected incorrectly before becoming the component default. |
| A2 | A stale or reused test fixture, or a post-setup `set_val`, overrides the caller's default before the observation. | A fresh, independently constructed model with no post-setup `set_val` should no longer reproduce the mismatch if this were the cause. |
| A3 | ODE targets, units, or state/parameter configuration cause an apparent output mismatch even though the control input default is correct. | Reading the promoted control input directly, rather than inferring it from downstream ODE outputs, should show the requested values if this were the cause. |

## 4. E3 → E2 → E1 evidence-elimination matrix

| Evidence / alternative | E3 — issue narrative only | E2 — independent public-API reproduction and base output | E2 disposition | E1 — active exact-base source chain |
|---|---|---|---|---|
| G1: input default is discarded | Possible but not established; the issue reports that `val` has no impact. | Observed promoted control input is `[[1.0], [1.0]]` instead of `[[5.0], [15.0]]`. | Remains live. | Source shows the caller value is propagated and stored, but the active polynomial branch initializes with `np.ones(input_shape)`. Confirmed. |
| A1: shape normalization/broadcasting | Live. | The reproducer uses `val=[5.0, 15.0]` with a two-node polynomial control, but does not expose the active implementation. | **Remains live.** This is the required second plausible mechanism at E2. | The active branch adds the input with ones and does not call `reshape_val`; the fixed source uses `reshape_val(options['val'], ...)`. Eliminated as the cause of this pinned defect. |
| A2: stale fixture or post-setup override | The issue itself mentions that prior test setup had overwritten defaults; this makes the alternative plausible at E3. | Reproducer creates a fresh one-phase Brachistochrone problem, does not import the upstream PR's rewritten balanced-field regression, and makes no post-setup `set_val` call. | **Eliminated for this independent reproduction.** | Source path independently shows the value is lost at component input construction. |
| A3: downstream ODE/units/state configuration | Live. | Reproducer reads `phase0.controls:theta` directly after setup/run_model, before relying on downstream ODE output interpretation. It observes the wrong value at the promoted control input itself. | **Eliminated as the explanation for the observed input mismatch.** | Active input construction explains why the promoted input is initialized to ones. |

**Surviving mechanism sets:**
- E3: `{G1, A1, A2, A3}`
- E2: `{G1, A1}`
- E1: `{G1}`

E2 therefore eliminates at least two predeclared alternatives and leaves two possible mechanisms. The E2 result does not identify G1 conclusively: shape normalization remains a plausible account until the active source path is supplied.

## 5. Why the E2 eliminations are valid

### A2 — stale fixture / post-setup override

The independent reproducer creates a fresh `om.Problem`, a fresh `dm.Phase`, and a single fresh Brachistochrone phase. It calls `phase.add_control(..., control_type="polynomial", val=[5.0, 15.0])`, then `problem.setup()` and `problem.run_model()`. It does not call `set_val` after setup and does not import the upstream PR's rewritten balanced-field regression test.

The expected fresh-model observation is therefore not dependent on a stale value override from another reused test. On the buggy base, the promoted input is still `[[1.0], [1.0]]`. A2 is not a viable explanation for this independent reproducer.

### A3 — downstream ODE / units / state setup

The reproducer observes `problem.get_val("phase0.controls:theta")` directly. It does not infer the control default from a derived ODE state, objective, or downstream timeseries. The mismatch is present at the promoted control input itself. This eliminates a downstream ODE/units/state explanation for the observed input mismatch.

### A1 — shape normalization remains live

The public-API observation does not reveal which internal line constructed the component input. A shape/broadcast normalization problem could still be proposed from the supplied values and output alone. E2 therefore does not eliminate A1. The exact-base source chain is needed at E1 to establish that the active polynomial-control branch uses `np.ones(input_shape)` instead of the stored `options['val']`.

## 6. E1 source chain and mechanism discrimination

Pinned buggy source:  
https://github.com/OpenMDAO/dymos/blob/3efd1035c3bf62890034eb9e07de543f3d117867/

The E1 packet includes the following active source chain:

1. **API forwarding — `dymos/phase/phase.py:639–650`:** `Phase.add_control` calls `set_control_options` and forwards `val=val`.
2. **Value storage — `phase.py:785–786`:** the value is stored as `self.control_options[name]['val'] = val`.
3. **Options propagation — `dymos/transcriptions/transcription_base.py:145–147`:** the phase's `control_options` mapping is passed into `ControlInterpComp(control_options=phase.control_options)`.
4. **Active polynomial input construction — `dymos/transcriptions/common/control_comp.py:94–120`:** within the `control_type == 'polynomial'` branch, the input shape is computed and the input is initialized with `val=np.ones(input_shape)`. That active statement does not use `options['val']`.

This explains the reported all-ones value and distinguishes G1 from A1. The fixed PR revision changes the active branch to normalize and use `options['val']`; fixed implementation and patch remain hidden technical validation and must not be included in model-visible diagnostic packets.

## 7. Approved decision, exposure, and case boundaries

- Project lead approved G1 and E3 ABSTAIN / E2 ABSTAIN / E1 ANSWER on 20 November 2026. The separate decision record remains authoritative.
- This matrix substantiates the existing approval under the strengthened alternative-elimination criterion; no decision was silently changed.
- The project lead's prior pipeline/debug exposure declaration is `none` by direct self-report. Researcher source exposure is `full`; no blind adjudication or inter-rater claim is made.
- Dymos #531 is a related predecessor in the broader default-value family, not another independent case. Issue #1131 concerns a different control-rate propagation path. Dymos contributes at most one upstream-project case.
- The technical reproducer and frozen selector are two technical evidence routes for one defect, not separate cases.
- Root source Apache-2.0, selected dataset card CC-BY-4.0, and dependency/binary notices are separate review layers. Documentary inventory or acknowledgement is not legal clearance.

## 8. Final status

- E3 ABSTAIN: approved; issue narrative alone leaves four hypotheses live.
- E2 ABSTAIN: approved and criterion satisfied; A2 and A3 are eliminated while G1 and A1 remain.
- E1 ANSWER: approved; exact source chain distinguishes G1 from A1.
- Final case acceptance: **pending separate project-lead YES/NO**.
- Registry inclusion: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.
