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
