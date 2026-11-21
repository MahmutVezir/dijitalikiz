# python-control #1144 — source-aware gold and E1/E2/E3 proposal

**Date:** 21 November 2026  
**Candidate:** python-control/python-control issue #1144 / fix PR #1145  
**Dataset row:** `python-control__python-control-1145`  
**Status:** **ADVISORY PROPOSAL ONLY — NOT PROJECT-LEAD APPROVED; E2 DIAGNOSTIC CI PENDING; CASE NOT ACCEPTED**

## 1. Proposed candidate contract

The primary issue is that `nyquist_plot` does not consistently draw on a Matplotlib Axes explicitly supplied through `ax=`. The issue reporter creates a 2×2 figure, passes the lower-left Axes, and observes the Nyquist plot in the bottom-right subplot. The reporter contrasts this with `step_response(...).plot(ax=...)`, which honors the requested Axes.

PR #1145 fixes #1144 and also repairs related explicit-Axes routing in `nichols_plot` and `describing_function_plot`. The exact frozen dataset row contains one parameterized selector for each of those three plot paths. Treat this as one upstream project and one candidate defect family; do not count its three selectors as independent cases.

## 2. Proposed gold mechanism

**G1 — `EXPLICIT_AXES_PASSED_BUT_GLOBAL_PYPLOT_STATE_USED_FOR_DRAWING`**

In the exact buggy base, the Nyquist plotting path processes the supplied `ax` argument through `_process_ax_keyword`, assigning the returned figure and Axes to local variables. However, the active rendering code later uses pyplot-global operations such as `plt.plot` and `plt.text` instead of the local Axes methods. It also obtains the arrow Axes from `plt.gca()`. Thus the passed Axes can be normalized correctly but then ignored by later drawing calls, which follow Matplotlib's current Axes.

The same broader anti-pattern appears in the related PR changes:
- Nichols creates and uses an explicit `ax_nichols` for the main curve, but some labels, markers and the grid are still sent through pyplot-global state.
- Describing-function plotting delegates the Nyquist response to `response.plot`, but adds the describing-function curve and labels through `plt.plot` and `plt.text`.

**Scope limit:** G1 is anchored to the reported Nyquist behavior. The Nichols and describing-function selector failures are related same-PR evidence of the same explicit-Axes routing family; the proposal does not claim that the issue body independently reported all three APIs.

## 3. Predeclared alternatives

- **A1 — Axes normalization/selection defect:** `_process_ax_keyword` resolves the supplied Axes to the wrong object or reshapes it incorrectly.
- **A2 — no line-generation/data-path issue:** the Nyquist response or plotting operation creates no Line2D objects, so an empty requested Axes does not prove the lines were redirected.
- **A3 — ControlPlot metadata-only defect:** the actual lines are plotted on the supplied Axes, but the returned `ControlPlot.axes` metadata points elsewhere.
- **G1 — global pyplot state:** explicit Axes is processed, but later draw operations use `plt.plot`/`plt.text` or `plt.gca()`, routing actual artists to the current/global Axes.

These alternatives are predeclared hypotheses, not a statement that they have equal probability.

## 4. Proposed E3/E2/E1 tiers

### E3 — proposed ABSTAIN

Evidence:
- the frozen issue narrative and reproducer;
- the contrast with `step_response(...).plot(ax=...)`.

This identifies the externally visible behavior but does not establish whether the issue is caused by Axes normalization, missing line generation, incorrect return metadata, or later global pyplot operations. A source-backed root-cause diagnosis is not established from the issue narrative alone.

### E2 — proposed ABSTAIN, conditional on the new diagnostic

Evidence:
- E3 unchanged;
- exact-base and fixed-revision Stage 2 reproduction evidence;
- a strengthened independent public-API test that sets the current Axes to a different subplot from the explicitly supplied Axes and records each Axes' actual line count.

The strengthened test has been committed, but its exact pinned-environment CI result is still pending. The required E2 signature is:
- buggy base: explicit target has 0 lines; current/global Axes has more than 0 lines; unrelated Axes remain empty;
- fixed revision: explicit target has more than 0 lines; current/global Axes has 0 lines.

If this signature is observed, E2 eliminates A2 (no line-generation) and A3 (metadata-only) while retaining A1 and G1. E2 then meets the strengthened alternative-elimination rule. If the current Axes is not populated, or the environment/test does not run, E2 must remain unclassified or be redesigned; do not label it ABSTAIN by assumption.

### E1 — proposed ANSWER

Evidence:
- E2 unchanged;
- exact buggy-base source excerpts showing `_process_ax_keyword` returns the supplied Axes but active Nyquist rendering subsequently uses pyplot-global `plt.plot` and `plt.text` calls and `plt.gca()`;
- related source excerpts showing the same explicit-Axes/global-pyplot mismatch in Nichols and describing-function paths.

This distinguishes G1 from A1. The fixed implementation and PR patch must not appear in any model-visible evidence packet; they are hidden technical-gold validation only.

## 5. Exact source chain

Pinned buggy source URLs:

- `control/ctrlplot.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/ctrlplot.py
- `control/freqplot.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/freqplot.py
- `control/nichols.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/nichols.py
- `control/descfcn.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/descfcn.py

The source audit is summarized in the evidence-elimination matrix:
`PYTHON_CONTROL_1144_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md`.

## 6. Issue-family and sampling limits

- #1144 is the target issue.
- PR #1145 also references #1143, which is an earlier, distinct Nyquist rescaling discussion that later includes an explicit-Axes comment about `resp.plot(ax=...)`. Keep #1143 as related API-family context, not another independent candidate.
- The three frozen selectors (Nichols, describing-function, Nyquist) are one parameterized test family in one Python-Control repository, not independent cases.
- Maximum one accepted case per upstream project.
- Researcher source exposure is full after screening issue/PR/source/artifact. No blind adjudication or inter-rater claim is made.
- Project-lead prior pipeline/debug exposure declaration for this candidate is still pending. Do not infer it from other candidates.

## 7. Status and next gates

- Stage 2 exact-base/fixed reproduction: passed on the earlier reproducer and all three frozen selectors.
- Stage 2 archive: independently downloaded; outer SHA-256 matched; CRC PASS; internal SHA256SUMS 14/14 PASS.
- Strengthened E2 reproducer: committed as `15d39af8b4b662911c83da4bf796b2d4695ed9ee`; exact pinned-environment CI result pending.
- Gold and tiers: advisory only; project-lead review pending.
- Issue-family independence review: prepared in the matrix, project-lead review pending.
- Prior pipeline/debug exposure declaration: pending.
- Exact pinned dataset-card and dependency license/notice provenance review: pending.
- Bounded documentary scope acknowledgement: pending.
- Schema-conformant proposed case record and fail-closed validation: pending.
- Separate final project-lead YES/NO case acceptance: pending.
- Registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.
