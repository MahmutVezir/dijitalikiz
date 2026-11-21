# PyFar #721 — E3/E2/E1 evidence-elimination matrix

**Date:** 21 November 2026  
**Candidate:** pyfar/pyfar issue #721 / fix PR #722  
**Dataset instance:** `pyfar__pyfar-722`  
**Status:** **SOURCE- AND ARTIFACT-AUDITED MATRIX; PRIOR GOLD/TIER APPROVAL RETAINED; FINAL CASE NOT ACCEPTED**

## 1. Purpose and decision boundary

This matrix audits whether the previously approved tiers — E3 ABSTAIN, E2 ABSTAIN, E1 ANSWER — are supported by a defensible evidence progression. It does not silently modify the project lead's 21 November 2026 decision.

The proposed gold mechanism remains:

**G1 — `ENERGY_POWER_TARGET_AND_REFERENCE_NOT_SQUARE_ROOTED`**

In the pinned buggy base, `normalize` scales amplitude by the unrooted ratio `target / reference_norm` for energy/power. Since energy and power are quadratic in amplitude, the energetic target is not generally attained. The amplitude scale consistent with target energetic value T and reference R is `sqrt(T / R)`.

## 2. Frozen provenance and integrity

- Issue: https://github.com/pyfar/pyfar/issues/721
- Fix PR: https://github.com/pyfar/pyfar/pull/722
- Exact buggy base: `648dda4c60c5a6f74acf335f7808c590c9d23929`
- Exact fixed revision: `a4d72d380bb8ddb0950d334eb1b0793ee6d86e0e`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset row: `pyfar__pyfar-722`
- Dataset row SHA-256: `82444bd1dcaa0c52bcac4a5c0b76efc20ed0ad26606de1edc338265843aca6bd`
- Exact buggy-base `pyfar/dsp/dsp.py` blob: `b44dbac7817be97126bd3bbac88add4b6a1ebd54`
- Stage 2 workflow run/job/artifact: `44331092872 / 134895967816 / 14440390942`
- Artifact SHA-256, independently recomputed from downloaded ZIP: `17e80ba9a81153ea833ce0cee05271f1815c6c6d597653c12f9bbe11f0f95bf8`
- ZIP CRC: PASS; internal SHA256SUMS: 14/14 PASS.

The archived Stage 2 results contain 23 frozen FAIL_TO_PASS selectors: 23/23 expected failures on exact buggy base and 23/23 passes on exact fixed revision. This is one candidate and one upstream project, not 23 independent cases.

## 3. Predeclared alternatives

| ID | Alternative | What remains possible without source-level evidence |
|---|---|---|
| A1 | Energy/power measurement-definition or reference-computation mismatch | The metric functions or the way their returned reference is interpreted may be inconsistent with the caller's intended energetic target. |
| A2 | Target semantics / amplitude-versus-energetic-target mismatch | The observed mismatch may arise from how the API maps an energetic target into an amplitude multiplier; output symptoms alone do not establish the exact internal formula. |
| A3 | Channel-reduction-only defect | The primary issue may be caused solely by multi-channel aggregation order, especially mean-channel handling. |
| A4 | Target=1/default-only behavior | The defect may be limited to the issue's default/unit target rather than applying to other explicit target values. |
| G1 | Unrooted energy/power reference and target in the amplitude scale | The pinned source computes energy/power quadratically but scales amplitude by `target / reference_norm` without square-rooting either term. |

A1 and A2 deliberately remain separate from G1: observed output values alone do not prove whether the problem originates in the metric/reference calculation, the API meaning of `target`, or the final amplitude-scaling expression.

## 4. E3 → E2 → E1 evidence-elimination matrix

| Evidence / hypothesis | E3 — issue narrative | E2 — add exact-base frozen outputs | E2 disposition | E1 — add exact-base source |
|---|---|---|---|---|
| A1: metric/reference computation mismatch | Live. Issue gives energy measurements and wrong normalized energies, but no pinned implementation chain. | Still live: failing outputs establish the behavior but do not show whether the reference measurement or its use is the internal source. | **Not eliminated.** | Source definitions show energy and power are computed as sums of squared magnitudes (power divided by N); normalization reuses those methods as reference metrics. |
| A2: target semantics / amplitude mapping | Live, although the issue reporter explicitly proposes dividing by the square root of the calculated reference for the target=1 example. This is a hypothesis, not an independently verified implementation trace. | Outputs across targets 0.5, 1, and 2 strengthen a quadratic-target pattern but do not expose the exact code path. | **Not eliminated as a source-level alternative.** | Source shows target and reference both enter an amplitude multiplier unrooted; the energy/power target requires square-root conversion. |
| A3: channel-reduction-only defect | The issue's single-channel noise examples already do not point to a mean-only aggregation defect. | Failures occur under `individual`, `max`, `min`, and `mean` modes. | **Eliminated as the sole explanation.** The bug is present even when no multi-channel aggregation is performed (`individual`) and is not confined to `mean`. | Source shows channel reduction is applied to the reference before the unrooted amplitude scaling. |
| A4: target=1/default-only behavior | Issue narrative demonstrates target=1 only; it cannot establish behavior for other targets. | Failures cover target 0.5 and target 2 as well as target 1. | **Eliminated as a scope limitation.** The bug is not restricted to the unit/default target. | Source formula explains why non-unit targets also require square-rooting the target itself, not just the reference. |
| G1 | Reporter suggests a square-rooted reference for target=1, but does not prove the pinned implementation uses an unrooted target/reference amplitude ratio. | Numerical output patterns are consistent with the quadratic scaling defect; exact source-level cause remains unproven. | Strongly supported as a hypothesis; source-level mechanism is not yet established. | Exact-base energy/power definitions and the normalization expression directly establish G1. |
| RMS as a competing defective branch | Issue does not report an RMS failure. | The 23 frozen selectors are energy/power cases; they do not independently establish an RMS defect. | No RMS defect claim is supported by E2. | Exact base defines RMS as `sqrt(power)`, so RMS is already amplitude-linear; the approved gold remains restricted to energy/power. |

## 5. E3 disclosure risk — reporter's hypothesis must remain visible

The issue body explicitly says:

> “the signal should be divided by the root of the calculated reference value, not the value itself.”

It also gives target=1 examples: an input energy of 20 leads to output energy 0.05; input energy 5 leads to output energy 0.2; and the sample code reports input/output energy pairs of 20/0.05 and 40/0.025.

This is a strong and highly relevant clue. It must not be removed, paraphrased away, or withheld from E3 merely to manufacture uncertainty.

**E3 ABSTAIN is defensible only under the project's strict evidence-supported-diagnosis criterion:** the reporter's proposed correction is treated as an unverified hypothesis, not as proof that the pinned implementation actually contains the alleged scaling expression. The model may identify the hypothesis, but it should not claim the implementation-level root cause as established from the issue narrative alone. If the task instead asks for the most likely repair or accepts the reporter's theory as sufficient evidence, E3 may be answerable and this case may be less suitable for a primary abstention tier. This is an explicit sample-suitability risk for project-lead review.

## 6. E2 artifact-level selector audit

The 23 selectors comprise the following parameter coverage:

- `reference_method`: energy and power (2 methods).
- `target`: 0.5, 1, and 2.
- `channel_handling`: individual, max, min, and mean.
- All 23 selected cases fail on the exact buggy base and pass on the exact fixed revision.

The relevant underlying parameter grid has 24 energy/power combinations (2 methods × 3 targets × 4 channel modes). One combination — `energy / min / target=1` — is absent from FAIL_TO_PASS because it is non-discriminating for this input: the minimum channel energy is already 1, so the buggy amplitude multiplier is 1 and the resulting energy happens to equal the target. This is a legitimate non-failing control, not a missing failed test. The artifact therefore supports 23/23 FAIL_TO_PASS selectors, not 24/24.

Representative exact-base observations from the archived log include:

| Channel handling | Target | Energy output observed | Power output observed |
|---|---:|---:|---:|
| max | 0.5 | 0.01 | 0.03 |
| max | 1 | 0.04 | 0.12 |
| max | 2 | 0.16 | 0.48 |
| min | 0.5 | 0.25 | 0.75 |
| min | 1 | Non-discriminating energy selector; power 3.0 | 3.0 |
| min | 2 | 4.0 | 12.0 |
| mean | 0.5 | 0.0192307692 | 0.0576923077 |
| mean | 1 | 0.0769230769 | 0.2307692308 |
| mean | 2 | 0.3076923077 | 0.9230769231 |

The `individual` cases also fail for both energetic methods; for example, target 0.5 produces the energy array `[0.25, 0.01]` rather than `[0.5, 0.5]`. The logs therefore show that the failure is not confined to the `mean` reduction path.

**Important source-independence boundary:** the 23 selectors were derived from the upstream PR-added regression parameterization. They are one selector set, not independent cases or separately authored issue-level reproductions. Do not call them 23 independent experiments. No standalone public-API reproducer is claimed in this record.

## 7. E1 exact-base source chain

Pinned buggy source:  
https://github.com/pyfar/pyfar/blob/648dda4c60c5a6f74acf335f7808c590c9d23929/pyfar/dsp/dsp.py

The relevant source lines are:

- **Energy, line 2156:** `np.sum(np.abs(signal.time)**2, axis=-1)`.
- **Power, line 2200:** `np.sum(np.abs(signal.time)**2, axis=-1)/signal.n_samples`.
- **RMS, line 2242:** `np.sqrt(power(signal))`.
- **Reference selection, lines 2628–2634:** `normalize` selects the energy, power, or RMS measurement method.
- **Channel reduction, lines 2652–2663:** `individual`, `max`, `min`, or `mean` is applied to the reference.
- **Buggy scaling, line 2665:** `normalized_signal = signal.copy() * target / reference_norm`.

For energy/power, let the original energetic reference be R and the requested target be T. Multiplying signal amplitude by T/R yields an energetic output:

`R × (T/R)^2 = T^2/R`

rather than T. To achieve T, the amplitude multiplier must be:

`sqrt(T/R)`

The source chain establishes G1 without relying on the fixed patch. RMS is excluded from the gold because its returned metric is already the square root of power.

**Model-visible leakage control:** E1 can contain the pinned buggy-base metric definitions and unrooted normalization expression. Do not include the fixed implementation, PR patch, or post-fix source in any diagnosis packet. Use those only for hidden technical validation.

## 8. Tier conclusion and remaining project-lead review

- **E3 ABSTAIN — previously approved.** Keep the reporter's square-root hypothesis visible. The label relies on treating that proposal as unverified rather than accepting it as source-level proof. Review sample suitability if the intended answer rubric permits a likely-repair answer.
- **E2 ABSTAIN — previously approved.** E2 eliminates A3 (mean-only channel aggregation) and A4 (unit-target-only scope), but A1 and A2 remain possible because output evidence does not show the exact implementation chain. The 23 selectors provide strong numerical support for G1 but are not independent cases.
- **E1 ANSWER — previously approved.** Exact-base source establishes the quadratic metrics and unrooted amplitude-scaling expression, supporting G1.

No change is made to the prior project-lead gold/tier decision in this matrix. If the E3 disclosure risk changes the agreed answerability rubric, record a new explicit project-lead decision rather than silently changing the existing decision record.

## 9. Status boundaries

- Stage 2 exact-base/fixed reproduction and artifact integrity: passed.
- Project-lead G1 and E3/E2/E1 decision: approved on 2026-11-21.
- This matrix: source/artifact audit; not final case acceptance.
- Issue-family review: prepared, project-lead review pending.
- Dataset-card exact README pin/bytes, canonical dependency licenses, bundled/native component notices, and bounded research-scope acknowledgement: open.
- Case record and fail-closed validation: open.
- Separate final project-lead YES/NO case acceptance: open.
- Registry inclusion: false.
- Model loading, inference, fine-tuning and training: not performed and not authorized.
