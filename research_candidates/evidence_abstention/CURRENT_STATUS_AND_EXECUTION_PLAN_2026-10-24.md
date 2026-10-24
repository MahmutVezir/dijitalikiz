# Current status and next actions — 24 October 2026

## Status boundary

- Project: Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ.
- Main study design is unchanged. The confirmatory registry remains empty; model inference remains prohibited.
- The pinned BugsInPy revision remains `11c5f1eea954a42132cfd06bf257766a7963e0fd`.
- The latest Keras-7 technical screen did **not** run its target test, create a new isolated environment, install packages, modify an existing environment, or run model inference.

## Keras-7 screen outcome

Candidate: `BugsInPy-keras-7`.

The report verified the pinned dataset revision, the candidate inventory/static-audit/queue hashes, its four source metadata hashes and bug-patch hash, the 93-ID prior exposure union, and the expected upstream commits. The fixed commit's patch changes `np.squeeze(self.model.predict(x, **kwargs))` to `np.squeeze(self.model.predict(x, **kwargs), axis=-1)`; the target regression test is supplied by the fixed commit and overlaid on the buggy source, consistent with the BugsInPy checkout protocol.

The screen then stopped before environment creation. The prior HTTPie-5 virtual environment reports Python 3.7.3, but `sys._base_executable` is null. The screen treated that field as the only possible base-interpreter path and did not check the reported `sys.base_prefix/bin/python` path or discover other installed interpreters. Therefore this is an **incomplete runtime-discovery check**, not a Keras target-test result. No test or scientific outcome can be inferred.

## Exposure decision

Before changing or debugging the runner, the following cases are permanently excluded from confirmatory analysis regardless of technical outcome:

- `BugsInPy-ansible-4`
- `BugsInPy-fastapi-8`
- `BugsInPy-httpie-5`
- `BugsInPy-keras-7`

The 24 October addendum and extended screening union record these exclusions. The original 21–23 October logs and the 23 October 93-ID union remain unchanged. The extended union contains 97 unique exclusions and is the required filter when rebuilding the next metadata queue. The existing V10 cohort remains provenance only; it must not be used directly as a new execution order.

## Immediate next actions

1. Run the case-independent `stage3_runner_python373_discovery.py` diagnostic. It only probes known interpreter paths and reads environment metadata; it performs no installation, environment mutation, candidate test, or model inference.
2. Use its report to determine whether an exact Python 3.7.3 interpreter is already available. If not, provision and validate a pinned interpreter in a separate infrastructure step before running any candidate.
3. Rebuild the deterministic metadata queue using the extended 97-ID union, preserving all existing hashes and the original V10 files.
4. Select the next not-yet-exposed candidate from the rebuilt queue. Any candidate used for subsequent runner debugging must be added to the permanent exclusion log before the runner is changed.

## Inference gate

Inference remains closed. The study still requires at least 60 independently accepted cases across at least 8 upstream projects (target 80), reproducible buggy-fail/fixed-pass results with matching recorded/runtime Python versions, license and ground-truth reviews, evidence-sufficiency review by a disjoint blinded panel, leakage/prior-exposure clearance, frozen reviewer calibration, immutable model/tokenizer/runtime verification, frozen hashes, and a separately reviewed preregistration/authorization step.

No confirmatory model outputs or results exist for this study.
