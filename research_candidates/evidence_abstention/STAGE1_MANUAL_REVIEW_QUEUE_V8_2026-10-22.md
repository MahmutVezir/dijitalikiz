# V8 technical screen — independent human-review queue

**Status:** 22 October 2026. Technical test-pair signals only. None of the cases is accepted into the confirmatory registry.

Four completed candidates from the frozen V8 screening queue have the following signals: the observed Python version matches the dataset metadata; the same target test fails on the buggy revision and passes on the fixed revision; artifact checksums validate; and the automated audit reports no fixture or environment warning.

| Candidate | Python | Target test | Technical status |
|---|---:|---|---|
| FastAPI-5 | 3.8.3 | test_filter_sub_model | Buggy fail / fixed pass signal |
| Keras-4 | 3.7.3 | test_tfoptimizer_pass_correct_named_params_to_native_tensorflow_optimizer | Buggy fail / fixed pass signal |
| Scrapy-5 | 3.8.3 | test_follow_None_url | Buggy fail / fixed pass signal |
| Sanic-5 | 3.8.3 | test_logging_modified_root_logger_config | Buggy fail / fixed pass signal |

The raw artifacts contain test logs, observed runtime fingerprints, source metadata hashes, worktree diff hashes, and checksum manifests. This technical check does not approve licenses, root-cause ground truth, or evidence sufficiency.

## Required human-review sequence

1. **Ground-truth panel:** At least two independent reviewers inspect the pinned Bug.info, patch, and source test; independently record the root cause and source evidence; resolve disagreements under a predefined adjudication procedure.
2. **Evidence-sufficiency panel:** Two separate reviewers prepare and assess E1/E2/E3 packets without seeing the patch, fixed commit, issue/PR identifiers, or the root-cause answer key. Their IDs must not overlap with the ground-truth panel.
3. **License, provenance, leakage, and independence:** Review full license terms and attribution requirements; audit the prior-exposure history; exclude duplicate bugs, pull requests, or dependent cases.
4. **Acceptance:** Only after every case-level and global gate passes may an accepted record be added to the case registry. This handoff file accepts no cases.

Patch links in the JSON are for the ground-truth panel only. Do not provide this file or those links to the evidence-sufficiency panel or to the model as an answer key.

Full commit identifiers, SHA-256 values, artifact IDs, and source references are in STAGE1_MANUAL_REVIEW_QUEUE_V8_2026-10-22.json. All four cases retain accepted_for_confirmatory=false; licensing, root-cause review, E1/E2/E3 review, leakage review, and the evidence packets remain open.


## Completed V8 batch disposition

The V8 selection-freeze job and all eight case jobs have now returned. Four cases are handed off above for independent ground-truth review. Four others are not review candidates from this run:

| Case | Why it is not a technical candidate |
|---|---|
| Black-6 | The buggy log indicates a missing test fixture or harness-file issue. |
| Matplotlib-4 | Environment/dependency/plugin failure signatures; the fixed test also failed. |
| Luigi-5 | Runtime Python was not recorded consistently and did not establish a metadata-matched test pair. |
| Pandas-4 | Pinned pytest installation failed before either target test ran. |

The raw artifacts for these four cases are retained in the same workflow run and their IDs/SHA-256 values are recorded in the JSON handoff. Do not reinterpret these failures as target bugs. This V8 batch did not result in a case being accepted; the case registry remains unchanged and model inference remains disabled.
