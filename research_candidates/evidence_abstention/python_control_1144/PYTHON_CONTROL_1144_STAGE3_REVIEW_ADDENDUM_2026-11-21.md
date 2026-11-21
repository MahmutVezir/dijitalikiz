# python-control #1144 — Stage 3 review addendum

**Date:** 21 November 2026  
**Candidate:** python-control/python-control issue #1144 / fix PR #1145  
**Dataset row:** `python-control__python-control-1145`  
**Disposition:** Stage 2 reproduction and archive integrity passed; source-aware Stage 3 proposal/matrix prepared; strengthened E2 diagnostic run pending; not accepted.

## 1. Stage 2 evidence and exact identity

- Exact buggy base: `dc7d71bd1a2d143f10fa8fe91d31292bdf8f5113`
- Exact fixed PR head: `21f4912c8b12216534b8d5b07c243c66675a8b83`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row SHA-256: `0dbc94f964604302bea3afc9322596577bab3bb990f2292a640c51d80e8099eb`
- Stage 2 run/job/artifact: `44111403900 / 134137813952 / 14340013958`
- Artifact size: 44,667 bytes
- Artifact SHA-256: `5957e0de926f5242559fa955caa5a1e1a227309f919f3f1849fc35b072cd1824` (independently downloaded and recomputed; exact match to GitHub digest)
- ZIP CRC: PASS; internal SHA256SUMS: 14/14 PASS.

The pinned exact environment used Python 3.11.9 with the committed `requirements.lock`, including NumPy 2.1.3, SciPy 1.14.1, Matplotlib 3.9.2 and pytest 8.3.3.

Stage 2 ran the following frozen selectors on the buggy base and fixed revision:

1. `control/tests/ctrlplot_test.py::test_plot_ax_processing[frequency_response-nichols_plot]`
2. `control/tests/ctrlplot_test.py::test_plot_ax_processing[describing_function_response-describing_function_plot]`
3. `control/tests/ctrlplot_test.py::test_plot_ax_processing[nyquist_response-nyquist_plot]`

All three failed on the exact buggy base and passed on the exact fixed PR revision. The workflow restored the upstream conftest (including `mplcleanup`); the earlier `--noconftest` setup-only failure is superseded and is not counted as reproduction evidence.

The Stage 2 logs show:
- Nichols selector: lower-right Axes unexpectedly received 24 lines where it should have remained empty.
- Describing-function selector: the intended top-middle Axes had 0 lines.
- Nyquist selector: the intended top-middle Axes had 0 lines.

These are three parameterizations of one upstream test family and one candidate, not three independent cases.

## 2. Independent reproducer and E2 diagnostic correction

Original independent reproducer:
`research_candidates/evidence_abstention/reproduction/python_control_issue_1144/test_issue_1144.py`

The original test deliberately set a 2×2 figure's current Axes to the lower-right subplot, passed the lower-left subplot as `ax=`, and asserted that the supplied Axes contained lines while the other Axes remained empty. It failed on the buggy base and passed on the fixed revision. However, the original failure only established that the requested Axes was empty; it did not record whether the current/global Axes had received the lines.

To close that diagnostic gap, the reproducer was strengthened on 21 November 2026:
- it now records actual Line2D counts for the explicit Axes, current/global Axes, upper-left and upper-right Axes;
- it asserts that the supplied Axes receives lines and the current/global Axes remains empty;
- the failure message includes all observed line counts.

Updated test commit: `15d39af8b4b662911c83da4bf796b2d4695ed9ee`  
Updated test blob: `aa93aee654f50592b7d99b270897072fbbf8a7ff`

**The updated test has not yet produced an exact pinned-environment CI result.** The GitHub Actions workflow-run lookup for this commit returned no run; the only combined status reported by the connector was the unrelated Vercel build-rate-limit failure. Therefore the intended E2 line-count signature remains pending and must not be reported as observed.

## 3. Source audit

Pinned source blobs at exact buggy base:

- `control/freqplot.py`: `0489799602bde67ec88989b4cf18b3cfcd523ddb`
- `control/ctrlplot.py`: `dbdb4e1ec239a0e56bb4384d5d713a395d9494ed`
- `control/nichols.py`: `3c4edcdbda49b766d0987b4083b59c4f31e9e106`
- `control/descfcn.py`: `bfe2d1a7ecc921cbcbaf8eef82c74942248796ac`

Key observations:
- `_process_ax_keyword` in `control/ctrlplot.py:342–405` reshapes and returns the explicitly supplied Axes array.
- `nyquist_plot` obtains the processed Axes at `control/freqplot.py:1876–1877`, but active drawing calls global `plt.plot`/`plt.text` in later lines (including 1916, 1931, 1942, 1952, 1955, 1966, 1974, 1978, 1990, 1997 onward); it also uses `plt.gca()` at line 1945.
- `nichols_plot` obtains `ax_nichols` at line 108 and uses it for the principal curve at line 132, but labels, marker and grid are still sent through pyplot-global calls at lines 135–143.
- `describing_function_plot` delegates the Nyquist response at line 523, but adds the describing-function curve at line 527 and annotations at line 533 using `plt.plot` and `plt.text`.

This source-level evidence supports the proposed shared pattern: explicit Axes are accepted but not consistently threaded through all subsequent drawing operations.

## 4. Stage 3 proposal and issue family

- Matrix: `PYTHON_CONTROL_1144_E3_E2_E1_EVIDENCE_ELIMINATION_MATRIX_V0_1_2026-11-21.md`
- Gold/tier proposal: `PYTHON_CONTROL_1144_SOURCE_AWARE_GOLD_AND_EVIDENCE_TIERS_PROPOSAL_V0_1_2026-11-21.md`
- Proposed G1: `EXPLICIT_AXES_PASSED_BUT_GLOBAL_PYPLOT_STATE_USED_FOR_DRAWING`.
- Proposed tiers: E3 ABSTAIN; E2 ABSTAIN only if the strengthened diagnostic shows the current/global Axes has lines while the explicit target Axes is empty; E1 ANSWER after the exact-base source chain is shown.
- If updated E2 diagnostic does not show redirection, or cannot be run, revise the tier or leave E2 unclassified. Do not force the ABSTAIN label.
- Related issue #1143 is earlier Nyquist rescaling context with a later comment reporting another explicit-Axes plotting issue. It is related API-family context, not a duplicate of #1144 and not another independent case.
- PR #1145 contains adjacent fixes for Nyquist, Nichols and describing-function plotting. The three dataset selectors are one Python-Control candidate and one upstream project.
- Researcher source exposure: full. Project-lead prior pipeline/debug exposure declaration: pending. No blind adjudication or inter-rater claim is made.

## 5. Remaining gates

- Exact pinned dataset-card bytes/license provenance and canonical dependency license/notices: pending human review.
- Bounded documentary research-scope acknowledgement: pending.
- Project-lead review of issue-family disposition, source-aware gold and E3/E2/E1 proposal: pending.
- Project-lead prior pipeline/debug exposure declaration: pending.
- Schema-conformant case record and fail-closed validation: pending.
- Separate final project-lead YES/NO case acceptance: pending.
- Registry inclusion: false.
- No model loading, inference, fine-tuning or training performed or authorized.
