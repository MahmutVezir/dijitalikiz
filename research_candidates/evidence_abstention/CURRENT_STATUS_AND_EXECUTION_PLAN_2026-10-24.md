# Current status and next actions — 24 October 2026

## Status boundary

- Project: Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ.
- The confirmatory registry remains empty; model inference remains prohibited.
- The pinned BugsInPy revision remains `11c5f1eea954a42132cfd06bf257766a7963e0fd`.
- Four candidates used or inspected during session runner calibration are permanently excluded: `BugsInPy-ansible-4`, `BugsInPy-fastapi-8`, `BugsInPy-httpie-5`, and `BugsInPy-keras-7`. This decision is outcome-independent.
- The model candidate remains the pinned `Qwen/Qwen2.5-3B-Instruct` revision recorded in the project plan. This phase screens benchmark cases and runtime infrastructure; it is not a comparison among base models and not model training.

## Keras-7 screen outcome

The Keras-7 technical preflight verified the pinned dataset revision, candidate inventory/static-audit/queue hashes, case metadata and patch hashes, upstream commit availability, the common fixed-test overlay, and intersection with the then-current 93-ID exposure union. The target test itself was not executed.

The screen stopped before environment creation because a pre-existing Python 3.7.3 virtual environment reported a null `sys._base_executable`. No package installation, environment modification, candidate test, or model inference took place. Since the source/test patch was inspected while diagnosing the runner, Keras-7 is permanently excluded from confirmatory analysis.

The fixed commit changes `np.squeeze(self.model.predict(x, **kwargs))` to `np.squeeze(self.model.predict(x, **kwargs), axis=-1)` and adds the single-example regression test. This explains the candidate's upstream bug, but is not a test-pair reproduction result for this session.

## Python runtime discovery and disposable venv smoke

The no-install/no-mutation discovery step identified executable Python 3.7.3 paths:
- `/kaggle/working/stage3_conda_python373_env/bin/python`
- `/kaggle/working/stage3_conda_python373_env/bin/python3`
- `/kaggle/working/stage3_conda_python373_env/bin/python3.7`
- `/kaggle/working/stage3_conda_python373_env/bin/python3.7m`

The main path ran and reported Python 3.7.3, with its `sys.base_prefix` pointing at the existing environment. Thus the earlier blocker is best classified as a discovery/preflight design defect, not absence of Python 3.7.3.

The case-independent disposable venv smoke passed on 2026-10-24 at 15:58:24 UTC. It created and launched a separate Python 3.7.3 environment, verified that `sys.prefix` matched the disposable path and differed from `sys.base_prefix`, and intentionally confirmed `pip` was not importable because the test used `--without-pip`. All three subprocesses returned code 0. No installation, target test, model inference, or existing-environment modification occurred. Evidence: [PYTHON373_VENV_CREATION_SMOKE_2026-10-24.json](PYTHON373_VENV_CREATION_SMOKE_2026-10-24.json).

This result validates only venv creation and interpreter isolation. Pip/toolchain bootstrap and project dependency installation remain unverified.

## Pinned toolchain smoke — first attempt blocked

The 24 October disposable toolchain smoke successfully created a fresh Python 3.7.3 venv and installed the expected wheels `pip==23.3.2`, `setuptools==67.8.0`, and `wheel==0.41.3`. `pip check` returned code 0 with “No broken requirements found.” However, the exact-version probe failed while importing `setuptools`, with an assertion pointing to the base environment's `distutils/core.py`. The first report is recorded in [PYTHON373_PIP_TOOLCHAIN_SMOKE_2026-10-24.json](PYTHON373_PIP_TOOLCHAIN_SMOKE_2026-10-24.json).

The probe used `import json, pip, setuptools, wheel`, which imports `pip` before `setuptools`. Upstream Setuptools reports document this import-order pattern as a cause of the same assertion (see https://github.com/pypa/setuptools/issues/3044). Treat this as a likely test-harness defect, not a confirmed project-runtime failure, until a corrected probe passes. The original output is preserved; no candidate source or test was executed.

Next smoke uses an import-order-safe check: import `setuptools` and `wheel` without first importing `pip`, query pip's version through the CLI separately, and verify the three exact entries using `pip freeze --all`. A successful rerun is required before candidate execution.

## Pinned toolchain smoke v2 — passed

The import-order-safe rerun passed on 2026-10-24 at 16:07:33 UTC. A fresh disposable Python 3.7.3 venv installed and verified `pip==23.3.2`, `setuptools==67.8.0`, and `wheel==0.41.3`. The exact `pip freeze --all` lines matched the three pins, and `pip check` returned code 0 with no broken requirements. All recorded commands in this smoke completed without error. Evidence: [PYTHON373_PIP_TOOLCHAIN_SMOKE_V2_2026-10-24.json](PYTHON373_PIP_TOOLCHAIN_SMOKE_V2_2026-10-24.json).

This closes the disposable Python 3.7.3 toolchain-bootstrap smoke only. It does not authorize running a benchmark candidate under a mismatched interpreter. The next queued candidate is `BugsInPy-ansible-7`, whose pinned metadata requires Python 3.6.9, so Python 3.7.3 cannot be used to run it unless an explicit protocol amendment is justified and frozen beforehand. Current next step is a case-independent, read-only search for Python 3.6.9 and environment managers; no candidate source download or test is allowed during this discovery.

## Exposure decision and rebuilt queue provenance

The dated addendum `EXPOSURE_EXCLUSION_ADDENDUM_2026-10-24.json` records the four session exclusions. The derived `EXPOSURE_UNION_2026-10-24.json` contains 97 unique IDs (the previous 93-ID union plus four cases); the original 21–23 October records remain unchanged.

The metadata-only queue rebuild completed successfully from the pinned 501-row / 17-project inventory:
- Inventory SHA-256: `069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb`
- Exposure-union raw SHA-256: `887ece481244b432e6f2a89ae7fbbd1c032a71569171a5b714a3a73c66c570f1`
- Exposure-union Git blob SHA: `c94b7606f5d3a347a2b06e789ba0d7acef5e2855`
- Queue: 403 rows across 13 projects; SHA-256 `bac3d90f5d4e473645583aa9585a38f6fa44153ac739cacf4e2e7b16600f8e49`
- Static audit SHA-256: `e23090ec74ce2d1f9fd7feafa69b2d779a1a38e5482b7e18654cacd72fd7245d`
- Static prescreen readiness: 45 candidates across 7 projects.
- Excluded-ID reintroduction: none; queue/exposure intersection is 0.
- One incomplete metadata record was excluded from the queue.

The minimum diversity gate is at least 8 upstream projects; the currently static-ready set covers only 7. Static readiness is a screening priority, not acceptance. The first queue candidate is `BugsInPy-ansible-7` (Python 3.6.9 metadata; 12 direct pins; static risk flags none). It has not been run and must not be run until the next infrastructure smoke passes. The four permanent exclusions remain unavailable for confirmatory analysis.

The V10 100-candidate files are historical provenance and must not be reused directly as the new execution order. The rebuilt queue is the active metadata-screening list.

## Immediate next actions

1. Run case-independent read-only discovery for Python 3.6.9 and available environment managers. Do not download candidate source, install project dependencies, or run tests during this step.
2. If Python 3.6.9 is absent, assess a reproducible isolated environment creation plan and its availability before choosing a candidate; preserve the exact Python version metadata gate.
3. Only after the runtime matches the first queued candidate, screen it with the rebuilt queue and permanent exclusion union. Buggy-fail/fixed-pass must both be reproduced in the recorded runtime. If a candidate is used to debug or modify the runner, permanently exclude it before modifying the runner.
4. Continue licensing, root-cause, leakage, prior-exposure, evidence-sufficiency, and independent-rater gates. A static-ready candidate is not an accepted case.

## Inference gate

Inference remains closed. The study still requires at least 60 independently accepted cases across at least 8 upstream projects (target 80), reproducible buggy-fail/fixed-pass results with runtime Python matching dataset metadata, license and ground-truth review, evidence-sufficiency review by a disjoint blinded panel, leakage/prior-exposure clearance, frozen reviewer calibration, immutable model/tokenizer/runtime verification, frozen hashes, and separately reviewed preregistration/authorization.

No confirmatory model outputs or hypothesis results exist for this study.
