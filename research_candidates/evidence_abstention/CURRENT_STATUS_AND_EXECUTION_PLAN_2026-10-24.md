# Current status and next actions — 24 October 2026

## Status boundary

- Project: Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ.
- The confirmatory registry remains empty; model inference remains prohibited.
- The pinned BugsInPy revision remains `11c5f1eea954a42132cfd06bf257766a7963e0fd`.
- Four candidates used or inspected during session runner calibration are permanently excluded: `BugsInPy-ansible-4`, `BugsInPy-fastapi-8`, `BugsInPy-httpie-5`, and `BugsInPy-keras-7`. This decision is outcome-independent.

## Keras-7 screen outcome

The Keras-7 technical preflight verified the pinned dataset revision, the candidate inventory/static-audit/queue hashes, case metadata and patch hashes, upstream commit availability, the common fixed-test overlay, and intersection with the then-current 93-ID exposure union. The target test itself was not executed.

The screen stopped before environment creation because a pre-existing Python 3.7.3 virtual environment reported a null `sys._base_executable`. No package installation, environment modification, candidate test, or model inference took place. Since the source/test patch was inspected while diagnosing the runner, Keras-7 is permanently excluded from confirmatory analysis.

The fixed commit changes `np.squeeze(self.model.predict(x, **kwargs))` to `np.squeeze(self.model.predict(x, **kwargs), axis=-1)` and adds the single-example regression test. This explains the candidate's upstream bug, but is not a test-pair reproduction result for this session.

## Python runtime discovery — case-independent diagnostic

The no-install/no-mutation discovery step identified executable Python 3.7.3 paths:
- `/kaggle/working/stage3_conda_python373_env/bin/python`
- `/kaggle/working/stage3_conda_python373_env/bin/python3`
- `/kaggle/working/stage3_conda_python373_env/bin/python3.7`
- `/kaggle/working/stage3_conda_python373_env/bin/python3.7m`

The main path ran and reported Python 3.7.3, with its `sys.base_prefix` pointing at the existing environment. Thus the earlier blocker is best classified as a discovery/preflight design defect, not absence of Python 3.7.3. A disposable venv-creation smoke check has **not** yet been performed, so successful creation of isolated per-candidate environments remains unverified. See [RUNNER_PYTHON373_DISCOVERY_2026-10-24.json](RUNNER_PYTHON373_DISCOVERY_2026-10-24.json).

## Exposure decision and queue provenance

The dated addendum `EXPOSURE_EXCLUSION_ADDENDUM_2026-10-24.json` records the four session exclusions. The derived `EXPOSURE_UNION_2026-10-24.json` contains 97 unique IDs (the previous 93-ID union plus four cases); the original 21–23 October records remain unchanged.

The V10 100-candidate files are historical provenance and must not be reused directly as the new execution order. Rebuild the deterministic full metadata queue from the pinned 501-row BugsInPy inventory using the extended 97-ID union. Expected metadata-only queue size is 403 rows across 14 upstream projects, assuming all 4 new exclusions were previously eligible and no other source metadata changed. The rebuild must fail closed if any recorded input hash, dataset revision, or exposure-union Git blob hash disagrees.

## Immediate next actions

1. Rebuild the full inventory and queue from the pinned BugsInPy checkout, verifying the expected 501-row inventory hash and 97-ID union. This is metadata-only; no target tests or inference.
2. Review the first statically ready candidate in the rebuilt queue, in the predeclared project-interleaved order. Static readiness is only a screening priority, not acceptance.
3. Run a separate infrastructure-only disposable venv creation check with the discovered Python 3.7.3 executable. Do not install project dependencies during this smoke check.
4. Only after both queue and disposable-venv smoke checks pass, choose the next unexposed candidate for a test-pair screen. If a candidate is used to debug or modify the runner, add it to the permanent exclusion record before modifying the runner.

## Inference gate

Inference remains closed. The study still requires at least 60 independently accepted cases across at least 8 upstream projects (target 80), reproducible buggy-fail/fixed-pass results with runtime Python matching dataset metadata, license and ground-truth review, evidence-sufficiency review by a disjoint blinded panel, leakage/prior-exposure clearance, frozen reviewer calibration, immutable model/tokenizer/runtime verification, frozen hashes, and separately reviewed preregistration/authorization.

No confirmatory model outputs or hypothesis results exist for this study.
