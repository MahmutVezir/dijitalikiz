# V9 offset-eight technical screen — human review handoff

**Status: completed technical triage; no accepted cases; no LLM inference.**  
**Workflow:** [39841744307](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307)  
**Selection-freeze artifact:** ID `12453223251`, SHA-256 `5a2b5c053b4a138cd31efc4771be2f438dee22cee461f98f091e31472a2c5dca` (inner checksums passed).  
**Pinned BugsInPy revision:** `11c5f1eea954a42132cfd06bf257766a7963e0fd`.

The batch was selected by the frozen cohort before target tests ran. The workflow concluded with a matrix failure because the Matplotlib-6 job failed before producing a case artifact. The other seven case jobs completed; six produced clean automated buggy-fail/fixed-pass signals, while Luigi-7's pinned pytest bootstrap failed on both sides. A technical signal is not proof of the root cause and is not case acceptance.

All eight cases are permanently excluded from the confirmatory sample because their metadata, patches or target outputs were inspected during this technical screen. This exclusion applies irrespective of each outcome.

## Technical signals requiring Panel A triage

| Candidate | Runtime / target | Raw buggy-side signal | Fixed-side signal | Artifact |
|---|---|---|---|---|
| **BugsInPy-tqdm-6** | Python 3.6.9; `python3 -m pytest tqdm/tests/tests_synchronisation.py::test_imap` | Fails with `AttributeError: 'tqdm' object has no attribute 'total'` | 1 passed | [Artifact 12454021042](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12454021042), ZIP SHA-256 `3db0c54a8d6060fb75be2945d0783a1352247b8061ae0d99b53b10a5909dac00` |
| **BugsInPy-youtube-dl-6** | Python 3.7.0; `python -m unittest -q test.test_utils.TestUtil.test_parse_dfxp_time_expr` | Returns `0.0` where the test expects `None` | Test passes | [Artifact 12453876171](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12453876171), ZIP SHA-256 `d4b85e44845b9157664783284bab490b4ebbe414ddb55eac7756e86d615c3f0a` |
| **BugsInPy-ansible-6** | Python 3.6.9; three targeted Galaxy collection-install tests | Failure signals include numeric values missing `split`, a `LooseVersion` attribute error and an “already installed at version unknown” error | All three target commands pass | [Artifact 12454255246](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12454255246), ZIP SHA-256 `5c7d43834ebd7b03c92acec7a3bd3e9b41014471455498f18bd3b826b13f9d9c` |
| **BugsInPy-black-8** | Python 3.8.3; `python -m unittest -q tests.test_black.BlackTestCase.test_comments7` | Formatting-output mismatch | Test passes | [Artifact 12453591492](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12453591492), ZIP SHA-256 `e20d36087a9acda02b4953da1404abf4d6d0ebb334af1f5da0d42b79c2b8d6ad` |
| **BugsInPy-fastapi-7** | Python 3.8.3; `pytest tests/test_multi_body_errors.py::test_jsonable_encoder_requiring_error` | `TypeError: Object of type Decimal is not JSON serializable` | Test passes | [Artifact 12454376785](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12454376785), ZIP SHA-256 `a6e50cc6a82d383cd1282b855870551a59317c9662811de604a71df5431dff57` |
| **BugsInPy-keras-6** | Python 3.7.3; `pytest tests/test_loss_masking.py::test_masking_is_all_zeros` | `assert nan == 0` fails | Test passes | [Artifact 12453811486](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12453811486), ZIP SHA-256 `6a7c74b4f8fc6d41477ec89aab72210f3092e460d1f5a6d08b1d058bb20ad4da` |

The per-case ZIP digests above match the downloaded artifacts; all listed inner `SHA256SUMS` checks passed. Full target log, summary, runtime fingerprint and audit-file hashes are recorded in the [dated exposure ledger](./EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json).

## Non-qualifying outcomes

| Candidate | What happened | Disposition |
|---|---|---|
| **BugsInPy-luigi-7** | Pinned pytest bootstrap failed with exit code 1 on both sides. The target test did not run; observed runtime Python was not captured. [Artifact 12454496788](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307/artifacts/12454496788), ZIP SHA-256 `065165fa1bdab07e5c4dd05050047414e4d91f2d18cdd13cf98bef8d37481a68`. | No buggy/fixed test pair; not a qualifying candidate. |
| **BugsInPy-matplotlib-6** | The matrix job failed without uploading a case artifact. Frozen metadata identifies the target as `pytest lib/matplotlib/tests/test_axes.py::TestScatter::test_scatter_single_color_c`, Python 3.8.1. | No raw case evidence is available from this run; do not classify its target outcome. |

## Required human review before this handoff can inform the research protocol

**Panel A — root-cause / provenance review.** Review source commits, patch and test diffs, the raw buggy and fixed logs, whether the tests directly establish the intended defect, source/license provenance, and whether a patch materially changes the test. For Ansible-6, specifically determine whether the “already installed at version unknown” failure is a genuine target defect or an environment/fixture interaction. For tqdm-6 and youtube-dl-6, assess potential overlap with earlier exposed cases from the same upstream projects.

**Panel B — independent evidence-sufficiency review.** Must be disjoint from Panel A and must not see case identity, buggy/fixed commit IDs, patch, fixed implementation, hidden E1/E2/E3 label, or root-cause answer. Use access-controlled blinded packets; a public repository is not an adequate blinding boundary.

No reviewer identities, licenses, root-cause judgments, E-level decisions, leakage clearance, or prior-exposure clearance are filled by automation. All are currently false/unreviewed. The cases remain excluded from confirmatory selection even if reviewers later judge their technical signals sound.

## Interpretation boundary

This batch helps rehearse and audit the data-validation pipeline only. It provides no evidence about Qwen abstention rate, hallucination rate, selective prediction, confidence calibration, or the P0/P1 hypothesis. No model was loaded and no response was generated.
