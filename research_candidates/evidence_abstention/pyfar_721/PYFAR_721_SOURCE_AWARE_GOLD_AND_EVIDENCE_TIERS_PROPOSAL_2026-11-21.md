# PyFar #721 — source-aware gold and evidence-tier proposal

Date: 2026-11-21  
Project: TÜBİTAK 2204-A — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
Candidate: pyfar/pyfar issue #721 / fix PR #722  
Dataset instance: `pyfar__pyfar-722`  
Status: **ADVISORY PROPOSAL ONLY — NOT PROJECT-LEAD APPROVED**

## 1. Candidate contract and exact source identity

- Upstream repository: `pyfar/pyfar`
- Issue: https://github.com/pyfar/pyfar/issues/721
- Fix PR: https://github.com/pyfar/pyfar/pull/722
- Buggy base: `648dda4c60c5a6f74acf335f7808c590c9d23929`
- Fixed commit: `a4d72d380bb8ddb0950d334eb1b0793ee6d86e0e`
- Merge commit: `ecd0589a3fef83ec17e8d72a4bd5a3c64ef7c445`
- Changed paths: `pyfar/dsp/dsp.py`; `tests/test_dsp_normalize.py`
- Exact-base source blob for `pyfar/dsp/dsp.py`: `b44dbac7817be97126bd3bbac88add4b6a1ebd54`
- Exact-base source blob for `tests/test_dsp_normalize.py`: `224e8c501db5b763374ae74f9d9d40fc0205e0a4`
- Fixed source blob for `pyfar/dsp/dsp.py`: `c032e89e156921d990b4d6b5977fe39229fb66ff`
- Fixed source blob for `tests/test_dsp_normalize.py`: `69fde6699c70a8ce42cf18e2b4c04a81a1a8f643`

Issue #721 says that `normalize(..., reference_method="energy", target=1)` does not produce the requested signal energy. The reporter gives examples including input energy 20 yielding output energy 0.05, and input energy 5 yielding output energy 0.2. The issue also describes 2,000- and 4,000-sample noise signals with output energies 0.05 and 0.025 rather than a common target of 1.

PR #722 states that it applies the square-root relationship to energy and power references, applies the square root to the target as well, and updates documentation/tests. The maintainer follow-up explicitly says the first draft was only correct for `target=1`; the final change corrects the target scaling and clarifies that the mean-channel energy aggregation happens before square-rooting.

## 2. Proposed gold mechanism

**Proposed G1 — `ENERGY_POWER_TARGET_AND_REFERENCE_NOT_SQUARE_ROOTED`**

In the exact buggy implementation, `normalize` obtains the energy or power reference, applies the selected channel reduction, and then scales the signal linearly as:

`normalized_signal = signal.copy() * target / reference_norm`

But energy and power are quadratic in signal amplitude:

- energy: `sum(abs(x)**2)`
- power: `sum(abs(x)**2) / N`

If the input energetic reference is (R) and the requested target is (T), the buggy amplitude factor (T/R) produces an output energetic metric (R(T/R)^2=T^2/R), not (T). For the requested metric to equal (T), the amplitude factor must be (sqrt{T/R}).

The fixed PR therefore square-roots both the channel-reduced reference and the target for `energy` and `power`. It does not apply this transformation to `rms`, which is already amplitude-linear. This proposal is specifically about the energy/power branch; it does not claim the RMS branch has the same defect.

### Competing explanations to preserve

- **A1 — Energetic metric implementation or domain mismatch:** the reported difference could arise because the energy/power measurements themselves, rather than normalization scaling, are inconsistent with their documented definitions.
- **A2 — Target semantic ambiguity:** `target` could be interpreted as an amplitude target rather than the requested energy/power value. The issue wording and maintainer discussion support the latter, but this alternative must remain visible in lower-evidence packets.
- **A3 — Channel-reduction semantics:** the order of `channel_handling` aggregation and square-rooting might be the causal issue, particularly for `mean`. The fix's maintainer discussion says the intended semantics are aggregate the channel energies/powers first, then take the square root. The Stage 2 selectors cover multiple channel modes, not only `mean`.

These are live alternatives for evidence-tier construction, not claims that the alternatives are equally likely.

## 3. Proposed E1/E2/E3 decisions

The proposed decisions are **E3 ABSTAIN, E2 ABSTAIN, E1 ANSWER**. This is not yet a project-lead decision.

### E3 — ABSTAIN

Evidence: the issue narrative and its reported numerical counterexamples only.

The issue establishes a normalization symptom and the expected energetic target but does not expose the implementation path or prove whether the measurement functions, target semantics, or normalization formula are responsible. Proposed surviving mechanisms: `G1, A1, A2, A3`.

### E2 — ABSTAIN

Evidence: E3 plus the frozen Stage 2 base-only test outputs from the exact pinned buggy source. The workflow authenticated one exact dataset row and ran 23 frozen FAIL_TO_PASS selectors. All 23 executed and failed on the exact buggy base with the energy/power target assertions; the same 23 selectors passed on the exact fixed commit.

E2 must contain only the issue narrative and the buggy-base symptom/output evidence. Do not include the fixed-source patch or the internal implementation explanation in the model-visible E2 packet. This evidence verifies the symptom on the pinned source and reduces the chance of an unrelated collection/runtime failure, but it does not establish the causal source-level mechanism. Proposed surviving mechanisms: `G1, A1, A2`. A3 is substantially weakened because the reproduced failures span individual, max, min, and mean channel handling, rather than only the mean aggregation path.

**Independence limitation:** the 23 selectors are drawn from the upstream PR's added regression-test suite. They are not 23 independent cases, and they are not a separately authored issue-level reproducer. The study must not describe them as independent reproductions or independent test oracles. No standalone public-API reproducer has been run for this candidate.

### E1 — ANSWER

Evidence: E2 plus exact immutable buggy-base source excerpts from `pyfar/dsp/dsp.py`:

- `energy` returns `np.sum(np.abs(signal.time)**2, axis=-1)` (base source line 2156).
- `power` returns `np.sum(np.abs(signal.time)**2, axis=-1)/signal.n_samples` (line 2200).
- `rms` returns `np.sqrt(power(signal))` (line 2242), establishing that RMS is already amplitude-linear.
- `normalize` selects energy/power as the reference (lines 2630–2633), applies `channel_handling` to `reference_norm` (lines 2645–2654), and then applies the unrooted ratio `signal.copy() * target / reference_norm` (line 2665).

This source chain distinguishes G1 from A1–A3: the energy and power metrics are explicitly quadratic; the target and reference remain unrooted in the buggy path; the channel reducer is applied before the scaling step; and RMS follows a different path. Proposed surviving mechanism: `G1`.

The fixed source and full PR patch must remain withheld from E1's model-visible evidence packet if the task is diagnosis from evidence rather than recognition of the patch.

## 4. Stage 2 reproduction evidence and limitations

Latest Stage 2 branch repeat:
- Workflow run: `44331092872`
- Job: `134895967816`
- Artifact: `14440390942`
- Artifact SHA-256: `17e80ba9a81153ea833ce0cee05271f1815c6c6d597653c12f9bbe11f0f95bf8`
- Independently downloaded/recomputed outer ZIP SHA-256 matches the recorded GitHub digest.
- ZIP CRC check passed; internal SHA256SUMS verified **14/14** files.
- Dataset row: `pyfar__pyfar-722`; row SHA-256: `82444bd1dcaa0c52bcac4a5c0b76efc20ed0ad26606de1edc338265843aca6bd`.
- Frozen FAIL_TO_PASS selectors: **23/23 expected failures** on exact buggy base and **23/23 passes** on exact fixed commit.

The first PyFar environment attempt failed at test collection because `netCDF4` was missing. That historical attempt is not counted as a defect reproduction. The corrected lock added `netCDF4==1.7.2`, `cftime==1.6.4.post1`, and `certifi==2024.8.30`; only the corrected 23/23 result is the Stage 2 pass.

Remaining supplementary test questions: the original 2,000-/4,000-sample noise example has not been separately recreated in an independent public-API script; array-valued energetic targets and `return_reference=True` behavior are not explicitly covered by the 23 frozen selectors. These are additional coverage questions, not claims of a failed reproduction.

## 5. Methodological and decision boundaries

- One upstream project can contribute at most one accepted case. The 23 test selectors remain one PyFar case.
- The researcher has reviewed the issue, PR, exact-base source, and Stage 2 outputs. No blinding claim is permissible.
- Candidate-specific prior pipeline/debug exposure was declared **`none`** by the project lead on 2026-11-21 (direct self-report; not independently witnessed or externally audited). Researcher source exposure remains **`full`**; no blind adjudication or inter-rater reliability claim is made. See Section 7.
- This is a single source-aware adjudication proposal for the project lead. No independent second-rater or inter-rater reliability claim is made.
- Dataset-card and dependency/notice review remain open; the license-scope acknowledgement is pending. No legal clearance is asserted.
- No final case record has been accepted; PyFar remains outside the v0.2 registry.
- No model weights were loaded, and no inference, fine-tuning, or training is authorized or performed.

## 6. Proposed project-lead decision

The project lead should separately approve or revise G1 and the proposed E3/E2/E1 outcomes after reviewing this proposal. This document is advisory only; it does not record a human decision or accept PyFar into the registry.


## 7. Project-lead prior pipeline/debug exposure declaration — 21 November 2026

The project lead directly declared **`prior_pipeline_debug_exposure = none`** for PyFar #721. The declaration covers prior use of its issue, PR, source code, dataset selector, or reproducer to debug/develop the shared pipeline or tune prompts/tests before prospective candidate validation.

Decision record: `research_candidates/evidence_abstention/pyfar_721/PROJECT_LEAD_EXPOSURE_DECISION_PYFAR_721_2026-11-21.md`.

This closes only the candidate-specific prior pipeline/debug exposure gate, on a direct self-report that was not independently witnessed or externally audited. **Researcher source exposure remains `full`** because the issue, PR, exact-base source, and Stage 2 outputs were reviewed. No blindness or inter-rater claim is made.

This does not approve the proposed gold or E3/E2/E1 tiers, the issue-family independence assessment, license/data-use scope, dependency/native notices, proposed case record, or final case acceptance. PyFar remains outside the accepted registry and inference remains unauthorized.
