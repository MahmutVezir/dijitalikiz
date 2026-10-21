# Cohort v2 exposure audit — 2026-10-21

The original `SCREENING_COHORT_120_2026-10-21.json` remains preserved as a historical record. It contains eight cases later used in runtime/workflow debugging and therefore permanently excluded from confirmatory use:

- BugsInPy-ansible-1
- BugsInPy-black-3
- BugsInPy-cookiecutter-2
- BugsInPy-fastapi-2
- BugsInPy-httpie-2
- BugsInPy-keras-1
- BugsInPy-luigi-2
- BugsInPy-matplotlib-1

The verified screening queue has 487 unique metadata candidates across 17 projects (queue CSV SHA-256: `d03d2331a902f32cbb1f11922f9dda69fa51d2070b8a3cb07f1a9a689529cd1c`). A deterministic intake v2 must be formed by traversing that queue in ascending rank, skipping only these eight prior-exposure IDs, and taking the first 120 remaining IDs. This is an outcome-independent exposure exclusion, not replacement based on whether tests pass.

This file records the audit decision only. It does not mark any candidate accepted, does not authorize inference, and does not change the preregistered confirmatory sample. The original cohort file must not be overwritten.


## CI enforcement added

The cohort matrix builder now accepts both the historical v1 schema and the exposure-clean v2 schema, validates that v2 is exactly the deterministic queue order after the explicit prior-exposure exclusions, and fails closed if a historical cohort includes any of the eight exposed IDs. New tests cover the v2 skip rule, reintroduction rejection, and historical-cohort rejection.

[CI run 39658791623](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39658791623) ran the metadata inventory tests (3/3), queue tests (2/2), and cohort-matrix tests (7/7) successfully. The subsequent cohort-freeze step intentionally stopped because the existing workflow still points to the historical v1 file, which contains the eight exposed IDs. No new candidate test pairs or model inference were run in that workflow. Before starting the next technical batch, the workflow's cohort input and path trigger must be switched to `SCREENING_COHORT_120_V2_2026-10-21.json`; this is a configuration blocker, not a scientific result.


## V2 batch follow-up — technical bootstrap issue (2026-10-21)

The first technical batch selected from the exposure-clean V2 intake is recorded in workflow run [39659544932](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39659544932). The freeze step succeeded, but the run is not valid evidence that cases passed the test-pair gate. The completed `BugsInPy-PySnooper-2` artifact has matching Python 3.8.1 on both sides, while both test commands exited 1 with `pytest: command not found`; the audit therefore correctly records no buggy-fail/fixed-pass pair. The `BugsInPy-spacy-1` artifact did not start the case setup and has no observed runtime or target test results. Those are runner/setup failures, not bug outcomes.

To keep the exposure rule outcome-independent, the eight candidates in this batch are recorded as technical-debug exposures and are skipped by the V3 intake. The original V1 and V2 manifests remain unchanged as historical records. V3 retains 120 distinct candidate IDs across 17 projects and skips sixteen IDs total. This exclusion does not say the upstream bugs are invalid; it says these candidate IDs were used while diagnosing the technical screening harness.

The cohort workflow now points to V3 and installs pinned `pytest==6.2.5` in each case's isolated BugsInPy environment when the target command begins with `pytest`; the selected package set is captured by the per-side runtime fingerprint and the bootstrap log is checksummed. This change still requires a completed CI run and raw artifact inspection before considering the technical screen functional. All acceptance flags remain false and inference remains off.


## V3 runner-debug follow-up — metadata parsing issue (2026-10-21)

Workflow run [39660745325](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39660745325) passed the V3 queue freeze but did not produce an accepted case. The first inspected candidate, `BugsInPy-youtube-dl-2`, was stopped by the metadata consistency step before checkout/test because the workflow's strict regular expression expected `fixed_commit_id="..."` while the pinned upstream `bug.info` stores `fixed_commit_id ="..."`. This is a workflow parser defect, not a mismatch in the frozen queue metadata; the inventory contains the expected commit ID. The parser now tolerates whitespace around assignment operators.

V3 is preserved as the runner-debug intake and its first eight selected candidates are treated as permanently exposed for confirmatory purposes. The next frozen intake is [V4](SCREENING_COHORT_120_V4_2026-10-21.json), which skips 24 debug-exposed IDs total, preserves the upstream queue digest, and still has 120 candidates across 17 upstream projects. It accepts zero cases. The workflow now targets V4 and has the whitespace-tolerant parser; completion of CI and raw artifact inspection are still required.
