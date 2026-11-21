# python-control #1144 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** python-control/python-control issue #1144 / fix PR #1145  
**Dataset row:** `python-control__python-control-1145`  
**Status:** **SOURCE- AND STAGE2-ARTIFACT-AUDITED MATRIX; STRENGTHENED E2 REPRODUCER COMMITTED BUT EXACT-PINNED-ENVIRONMENT CI RESULT PENDING; NOT PROJECT-LEAD APPROVED; CASE NOT ACCEPTED**

## 1. Purpose and current conclusion

This matrix applies the strengthened tier rule:

> E2 must eliminate at least one predeclared alternative while retaining at least two plausible mechanisms.

**Current result: E2 remains pending.** The original Stage 2 independent reproducer only asserted that the requested Axes had no lines; its failure did not independently record whether the lines appeared on the current/global Axes or whether they were absent entirely. A stronger assertion has been committed to the reproducer to record both axes' line counts, but the updated test has not yet been executed in the exact pinned environment. Therefore no E2 elimination claim is made until that result is available.

Conditional on the strengthened test observing lines on the current/global Axes and none on the explicitly supplied Axes, E2 would eliminate (A2) the hypothesis that no plot objects were generated and (A3) the hypothesis that only ControlPlot return metadata is incorrect, while leaving G1 and A1 plausible. E1 source evidence then distinguishes G1 from A1.

This matrix is a methodological audit and advisory proposal, not a project-lead gold/tier decision or case acceptance.

## 2. Frozen provenance

- Issue: https://github.com/python-control/python-control/issues/1144
- Fix PR: https://github.com/python-control/python-control/pull/1145
- Exact buggy base: `dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113`
- Exact fixed PR head: `21f4912c8b12216534b8d5b07c243c66675a8b83`
- Merge commit: `632391cae6d126ed5c632a01fe65be96dc28a344`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row: `python-control__python-control-1145`
- Dataset row SHA-256 (from Stage 2 workflow): `0dbc94f964604302bea3afc9322596577bab3bb990f2292a640c51d80e8099eb`
- Exact-base `control/freqplot.py` blob: `0489799602bde67ec88989b4cf18b3cfcd523ddb`
- Exact-base `control/ctrlplot.py` blob: `dbdb4e1ec239a0e56bb4384d5d713a395d9494ed`
- Exact-base `control/nichols.py` blob: `3c4edcdbda49b766d0987b4083b59c4f31e9e106`
- Exact-base `control/descfcn.py` blob: `bfe2d1a7ecc921cbcbaf8eef82c74942248796ac`
- Stage 2 workflow run/job/artifact: `44111403900 / 134137813952 / 14340013958`
- Artifact size: 44,667 bytes
- Artifact outer SHA-256: `5957e0de926f5242559fa955caa5a1e1a227309f919f3f1849fc35b072cd1824` (independently downloaded and recomputed; matches GitHub digest)
- ZIP CRC: PASS; internal SHA256SUMS: 14/14 PASS.
- Pinned environment: Python 3.11.9; `requirements.lock` includes NumPy 2.1.3, SciPy 1.14.1, Matplotlib 3.9.2, pytest 8.3.3 and pinned transitive packages.

## 3. Defect contract and scope

The issue's supplied example creates a 2×2 Matplotlib figure and passes `ax[1,0]` to `control.nyquist_plot`, but the curve appears in another subplot (reported as the bottom-right subplot). The same issue notes that `step_response(...).plot(ax=ax[1,0])` places its plot correctly.

PR #1145 explicitly states that it fixes #1144 and also addresses related axes-routing defects in `nichols_plot` and `describing_function_plot`. The frozen dataset row has three FAIL_TO_PASS selectors, one for each of these plot functions. They are related regression selectors within a single upstream project and one candidate; they are not three independent cases.

**Gold scope must remain explicit:** the primary issue symptom is the Nyquist explicit-Axes contract. The Nichols and describing-function selectors are related regressions fixed in the same PR. E1 may describe the shared pattern — some plotting operations use global pyplot state rather than the explicit Axes — but must not imply that the issue body itself separately reported all three APIs.

## 4. Predeclared alternative mechanisms

| ID | Alternative / candidate mechanism | Distinguishing prediction |
|---|---|---|
| G1 | Explicit Axes is accepted/parsed, but active drawing operations later call global pyplot functions such as `plt.plot` or `plt.text`, so the current/global Axes receives lines instead of the supplied Axes. | With current Axes deliberately set to a different subplot, actual Line2D objects appear on the current Axes while the explicitly supplied Axes remains empty. |
| A1 | Explicit-Axes normalization or selection is wrong in `_process_ax_keyword`; the plotting function resolves the supplied Axes to a different Axes before drawing. | The helper's returned Axes does not match the explicit Axes supplied by the caller. |
| A2 | No line objects are generated (or the data/response produces no drawable lines); the empty target Axes is not evidence of redirection. | Both the explicit and current/global Axes remain empty. |
| A3 | Only the `ControlPlot.axes` return metadata is wrong, while actual drawn lines are on the explicitly supplied Axes. | Direct inspection of each Axes' `lines` shows the target has the lines even if returned metadata says otherwise. |

These are competing explanations to test, not statements of equal prior probability.

## 5. E3 → E2 → E1 matrix

| Evidence / alternative | E3 — frozen issue narrative | E2 — strengthened public-API reproducer | E2 disposition | E1 — exact-base source evidence |
|---|---|---|---|---|
| G1: global pyplot drawing state | Possible, not established; symptoms show the requested Axes is not respected. | **Pending.** New test records actual line counts for explicit Axes and current Axes after deliberately setting them to different subplots. | Remains plausible if current Axes has lines and explicit Axes is empty. | `nyquist_plot` parses `ax` with `_process_ax_keyword`, but active drawing uses `plt.plot` and `plt.text`; line 1945 obtains `plt.gca()`. Nichols and describing-function paths also contain pyplot-global operations. |
| A1: explicit-Axes normalization/selection defect | Live. | Pending; direct line-count result alone does not yet show what `_process_ax_keyword` returned. | **Remains live at E2** if the updated observation confirms redirection. | `_process_ax_keyword` exact-base source reshapes and returns the supplied Axes object; the later plotting calls, not the resolver, disregard it. |
| A2: no plotting objects generated | Live. | **To be eliminated only if** the current/global Axes contains plotted lines in the exact pinned base run. | Conditional elimination. If both Axes are empty, not eliminated and E2 must be redesigned. | Active plotting statements produce lines using pyplot global state. |
| A3: return metadata only is wrong | Live. | **To be eliminated only if** direct inspection shows target empty and current Axes populated, independently of `ControlPlot.axes` metadata. | Conditional elimination. | Source shows actual draw calls routed through global pyplot; returned Axes processing is separate. |

### E2 diagnostic implementation

The current reproducer is:

`research_candidates/evidence_abstention/reproduction/python_control_issue_1144/test_issue_1144.py`

It creates a 2×2 figure, saves `axes[1,0]` as the explicit target, sets `axes[1,1]` as Matplotlib's current Axes via `plt.sca`, then calls `nyquist_plot(system, ax=explicit_axes)`. It records:

- `explicit_axes` line count;
- `current_global_axes` line count;
- upper-left line count;
- upper-right line count.

It asserts that the explicit Axes has one or more lines, the current Axes has zero, and the other checked Axes remain empty. On the buggy base, the expected G1 signature is explicit target = 0 lines and current/global Axes > 0 lines. On the fixed revision, expected explicit target > 0 and current/global Axes = 0.

The update commit is `15d39af8b4b662911c83da4bf796b2d4695ed9ee` (reproducer blob `aa93aee654f50592b7d99b270897072fbbf8a7ff`). **The updated reproducer's exact pinned-environment CI result is pending.** The Stage 2 archive only contains the earlier reproducer run, whose failure established an empty target Axes but did not separately capture current/global Axes line count. Do not transfer the historical result to the updated test.

## 6. Existing Stage 2 evidence and its limits

The previously executed Stage 2 run reports:
- independent reproducer: expected failure on the exact buggy base and pass on the exact fixed PR revision;
- all 3 frozen dataset selectors fail on the exact buggy base and pass on the exact fixed revision;
- pinned upstream conftest was enabled to restore the `mplcleanup` fixture; an earlier `--noconftest` setup-only failure was superseded;
- the three base selector failures are in the axis-placement assertions of the same parameterized `test_plot_ax_processing` test:
  - Nichols: unexpected 24 lines on the nominally empty lower-right Axes;
  - describing-function: expected top-middle Axes to have lines, but observed 0;
  - Nyquist: expected top-middle Axes to have lines, but observed 0.

These base outputs are consistent with the global-Axes defect, but the new independent reproducer is intended to give a cleaner issue-level direct observation with separate current/target line counts.

## 7. E1 exact-base source chain

Pinned source URLs:

- `control/ctrlplot.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/ctrlplot.py
- `control/freqplot.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/freqplot.py
- `control/nichols.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/nichols.py
- `control/descfcn.py`: https://github.com/python-control/python-control/blob/dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113/control/descfcn.py

The source audit establishes:

1. **Axes processing:** `_process_ax_keyword` in `control/ctrlplot.py:342–405` reshapes the supplied Axes array and returns it; it does not intentionally replace the explicitly supplied Axes with pyplot's current Axes.
2. **Nyquist:** `control/freqplot.py:1876–1877` assigns the result of `_process_ax_keyword` to local `ax`. However, active drawing calls `plt.plot` for the regular curve (line 1916), scaled curve (1931), invisible arrow curve (1942), mirrored curve (1952/1955/1966), start marker (1974), the -1 marker (1978), unit circle (1990), and sensitivity circles (1997 onward). At line 1945 it obtains `ax = plt.gca()` for arrow placement. Those operations follow Matplotlib's current pyplot Axes rather than consistently using the local explicit Axes.
3. **Nichols:** `control/nichols.py:108` obtains the explicit `ax_nichols`; the primary response curve uses `ax_nichols.plot` at line 132, but label, -180 marker and grid operations at lines 135–143 use `plt.xlabel`, `plt.ylabel`, `plt.plot` and `nichols_grid()` without `ax=ax_nichols`.
4. **Describing function:** `control/descfcn.py:523` calls `dfresp.response.plot(**kwargs)`, but the describing-function overlay at line 527 and annotations at line 533 use `plt.plot` and `plt.text` rather than the Axes from the returned `ControlPlot`.

The fixed PR diff changes these drawing calls to the corresponding Axes methods. The fixed source and patch are **not** model-visible evidence; they may be used only for hidden technical-gold validation.

## 8. Related issue family and counting limits

- Issue #1144 is the target explicit-Axes defect in `nyquist_plot`.
- PR #1145 reports it also fixes related defects in `nichols_plot` and `describing_function_plot`; the 3 frozen selectors are one project-level regression set, not 3 independent cases.
- Issue #1143 is a separate earlier Nyquist rescaling discussion. A later comment on #1143 also describes two `resp.plot(ax=...)` calls unexpectedly drawing to the same current Axes. This is related explicit-Axes API context, but not a duplicate of #1144 and not a second independent case.
- Maximum accepted cases per upstream repository remains one.
- Researcher source exposure is full after screening issue/PR/source/artifact. No blind gold adjudication or inter-rater reliability claim is made.
- Project-lead prior pipeline/debug exposure declaration for this candidate has not yet been collected; do not infer it from other candidates.

## 9. Proposed tier consequence and gates

- E3 = ABSTAIN is a plausible proposal: the issue narrative states the symptom and includes a contrast with another plotting API, but does not establish which internal component routes the lines.
- E2 = ABSTAIN remains **pending** until the strengthened exact-base reproducer is run and its outputs show the redirection signature. If it only reports target-empty, or current/global also empty, revise the tier construction or leave E2 unclassified.
- If the E2 signature is confirmed, it eliminates A2 and A3 while retaining G1 and A1; E2 then meets the strengthened alternative-elimination rule.
- E1 = ANSWER is an advisory proposal: the pinned source shows Axes normalization works but later draw operations call global pyplot state, supporting G1.
- Gold/tier status: **not project-lead approved**.
- Issue-family review: prepared in this matrix; project-lead review pending.
- Dependency/license and exact immutable dataset-card provenance review: separate gates, not cleared by this matrix.
- Final case acceptance: **not accepted**.
- Registry inclusion: **false**.
- Model loading, inference, fine-tuning and training: **not performed and not authorized**.
