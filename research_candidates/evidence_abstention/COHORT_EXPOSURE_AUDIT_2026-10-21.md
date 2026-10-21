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
