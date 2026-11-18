# CTAPIpe #2730 — project independence and exposure screen (draft)

**Candidate:** cta-observatory__ctapipe-2732 (primary cohort rank 31)  
**Status:** preliminary documentary screen; formal human decision pending.

## 1. Upstream project identity

- Canonical upstream repository: `cta-observatory/ctapipe`
- GitHub repository metadata reports `fork=false`.
- Upstream repository URL: https://github.com/cta-observatory/ctapipe
- Frozen candidate row: `cta-observatory__ctapipe-2732`
- Dataset base commit: `287e7685e0e963f3fb44d92832ca97ac8c265c40`
- PR #2732 fixed commit: `5007b6ab61887d7555155edb4d1d296603a9735e`

The primary-cohort candidate intake queue lists CTAPIpe once at rank 31. The row is not a fork/mirror candidate according to repository metadata. A new read-only workflow has been added to scan the complete frozen Parquet file for every row whose `repo` field equals `cta-observatory/ctapipe`. Its run and artifact result are pending at the time this draft is written.

The repository's dataset-wide count is required before signing the one-upstream-project rule. Even if more than one frozen task row exists for the repository, at most one accepted case from this project may be counted. A repository-level uniqueness check does not by itself establish that two defects are semantically independent.

## 2. Related issue-family screen

GitHub issue searches in the canonical repository used the following focused terms:
- `muonparameters_skewness`
- `radial_light_distribution skewness`
- `MuonParametersContainer HDF5`
- `to_value muon`

The only direct result with the muon skewness/HDF5 symptom was Issue #2730 itself. The broader `to_value`/muon search also returned Issue #1139 (CHEC camera geometry converter classes broken for Prod4), which appears unrelated by title and symptom. This is a search-based preliminary screen, not an exhaustive issue/PR history or semantic graph. It cannot prove the absence of related defects outside the searched terms or across forks.

## 3. Researcher and AI exposure

- The student researcher has reviewed the frozen issue body, reporter traceback, base/fixed source, PR discussion, dataset row, test selector, and reproduction output. Record **full researcher source exposure**.
- ChatGPT has also seen the full case source and reproduction. It is an AI research assistant, not an independent human reviewer.
- No Qwen model was loaded; no prompt calibration or model generation was performed; no model output was scored; no training or fine-tuning occurred.
- The CTAPIpe-specific Stage 2 workflow and test harness were refined against this case. This is candidate-specific technical reproduction-workflow exposure. Whether that meets the v0.2 protocol's "prior pipeline-debug exposure" exclusion is not silently classified as none; the project lead must decide the appropriate exploratory-sample treatment.
- The public Qwen2.5-3B-Instruct release date predates the issue/PR dates. This makes exact post-release issue/PR exposure in the published model less likely, but the model's full training-data cutoff and absence of related code from training cannot be independently established.

## 4. Provisional status

- Canonical repository / fork status: documented (`fork=false`).
- Primary queue contains one CTAPIpe row: documented.
- Full frozen Parquet repository-row count: pending workflow artifact.
- Semantic related-issue-family review: preliminary search only; human sign-off pending.
- Researcher source exposure: full.
- Candidate-specific technical reproduction-workflow exposure: disclosed; protocol classification pending.
- Model exposure/training-data contamination: not proven either way.
- One-case-per-upstream-project acceptance: pending.
- Confirmatory use: not eligible without a separate exposure decision and all remaining gates.
- Exploratory feasibility use: only if the student project lead explicitly accepts the disclosed limitations and the other case gates pass.

No model load, inference, training, or fine-tuning has occurred or been authorized.
