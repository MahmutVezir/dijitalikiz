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


## 5. Completed frozen dataset family scan (2026-11-18)

The full Parquet row extraction has now completed successfully.

- Workflow: [44313191520](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44313191520)
- Job: `134832360579`
- Artifact: `14430704023`
- Artifact ZIP SHA-256: `7da5213baffb781389e44b8d26afa543a5f18b1f0b8609eeb6928f052da99650`
- All `10/10` internal checksum entries independently verified; artifact includes 11 members, including five complete frozen row JSON files and the project inventory.
- All five full rows were read from the pinned Parquet and independently hashed.

| Frozen row | Bug category / PR | Dataset base commit | F2P count | Full-row SHA-256 |
|---|---|---|---:|---|
| `cta-observatory__ctapipe-1872` | PR #1872 / issue #1621: simulation_config always maps observation IDs to configurations | `65a3dfe7442f40e14025ddd6dac97427af9f357f` | 2 | `59d1aeb7e62bd9f53e560f0522fefd7541b5f2681a4a549b59a6dba26659631b` |
| `cta-observatory__ctapipe-1883` | PR #1883 / issue #1882: Component/Tool logger hierarchy | `0612a333c87cbb7c39b3a82c4663082e77eceb72` | 1 | `04e0fc47b2c83c8b55d1e3dce73191478a9f56c6a7bac4d5153be77156f76329` |
| `cta-observatory__ctapipe-2320` | PR #2320 / issue #2321: SoftwareTrigger list versus NumPy array | `4cea6a81c42d2ef9f2a768ed1121ca6ca1790f36` | 3 | `29aa95ca29633ca6cae342f83a5240fddc26a847781587ff71df919aeef294ec` |
| `cta-observatory__ctapipe-2732` | PR #2732 / issue #2730: muon skewness/excess-kurtosis HDF5 mixed Quantity/float serialization | `287e7685e0e963f3fb44d92832ca97ac8c265c40` | 1 | `e7d40ebfdfa47f6d2b92940d83d4e1c74afea6a096e9dca0d682ebb0854e7006` |
| `cta-observatory__ctapipe-2738` | PR #2738 / issue #2737: DispReconstructor sign probability column | `ba264d9685e58b748c65d1d89c66ae0365588103` | 1 | `db357eac53cf7fb6675b16b0ad56af595eba2edb357dab35f50808c092bb8a3b` |

The row inventory stores a hash for the problem statement, production patch, test patch, and complete canonical row for each task. All five tasks share the same canonical upstream repository identity; they are not five independent projects.

The PR patches confirm different defect mechanisms:
- #1872 changes the shape of simulation configuration values and corresponding metadata-writing logic. It touches `ctapipe/io/datawriter.py`, but does not change the muon table writer, unit conversion, or `QuantityColumnTransform` mechanism.
- #1883 changes logging hierarchy initialization in `Component` and `Tool`.
- #2320 changes `SoftwareTrigger` handling of NumPy arrays of telescope IDs.
- #2738 changes the probability class index used for `DispReconstructor` sign inference.
- #2732 changes the unit representation returned for radial muon skewness and excess kurtosis.

**Within-repository family decision proposed:** #2732 is the only one of the five frozen rows in the selected muon Quantity/float HDF5 defect family. The other four rows are distinct task families and are not alternatives for this specific defect.

**Counting rule:** one upstream project can contribute at most one accepted case. If #2732 is eventually accepted, CTAPIpe contributes exactly one case, not five. The other four rows remain documented sibling tasks but cannot be added as separately accepted independent cases from this upstream project.

The full five-row inventory is in the successful row-audit artifact. The artifact's row paths are relative to the ZIP root as `project_rows/<instance_id>.json`; the machine-readable inventory records each full-row hash and original F2P selectors.
