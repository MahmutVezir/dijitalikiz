# V11 Technical Screen Audit Note — 2026-11-11

## Scope and safeguards

This note records engineering evidence for the first eight preselected V11 candidates. It is not a confirmatory result and does not accept any case. The candidate order remains frozen; no candidate was replaced after observing test output.

- Metadata-only V11 intake: 100 candidates across 13 upstream projects.
- Confirmatory cases accepted: 0.
- Model inference/training performed: no.
- Human review, licensing review, ground-truth review, evidence-level review, leakage review and prior-exposure review remain open.
- First-batch matrix source queue SHA-256: `60be1b69ba912c43f11a9c7d2a902753685a2976ec159c2f3cae613b2bcdacb0`.
- First-batch cohort SHA-256: `f0cf46005c181eb63d04ec08fcaf7a48696ba84db938ba86c010f42e2703f325`.

The frozen batch contains:
1. BugsInPy-ansible-7
2. BugsInPy-black-9
3. BugsInPy-fastapi-9
4. BugsInPy-keras-8
5. BugsInPy-luigi-8
6. BugsInPy-matplotlib-7
7. BugsInPy-pandas-6
8. BugsInPy-scrapy-7

## Runner correction

The Ubuntu 24.04 runner branch is retained as a draft pull request; it has not been merged by this work.

Commit [4ecb179d877cc9914c43cec7621b083581994888](https://github.com/MahmutVezir/dijitalikiz/commit/4ecb179d877cc9914c43cec7621b083581994888) removes the `| head -n 1` pipelines from the GCC, G++ and Make version probes in the runner bootstrap step. The previous run showed `make: write error: stdout` at `make --version | head -n 1` under `set -o pipefail`; this was a runner-shell failure before the candidate's target tests. The corrected commands consume the full version output. This is a harness-only adjustment: it does not change cohort selection, upstream metadata, declared target commands or test assertions.

Commit [8020e89520ee34ef601d29dcb70703f60693fe9a](https://github.com/MahmutVezir/dijitalikiz/commit/8020e89520ee34ef601d29dcb70703f60693fe9a) adds the raw buggy and fixed worktree diff files to future case artifacts, alongside their SHA-256 records. This makes patch-level review possible rather than relying only on diff statistics and hashes.

## Matplotlib-7: environment blocker, not a bug result

The run-8 case artifact is [artifact 13872322800](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43058520834/artifacts/13872322800), created by workflow run [43058520834](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43058520834).

Observed evidence:

- Dataset-recorded Python: 3.8.1; the buggy and fixed environments both reported Python 3.8.1.
- Both target-test commands exited 1 before test collection because importing Matplotlib's test `conftest.py` raised `ModuleNotFoundError: No module named 'numpy'`.
- The artifact audit marks the pair as an environment/dependency error and reports no buggy-fail/fixed-pass signal.
- The ZIP contains 34 checksum entries; `sha256sum -c SHA256SUMS` was independently run and all 34 entries passed.
- BugsInPy's `projects/matplotlib/bugs/7/requirements.txt` is empty (SHA-256 `e69e29bb2d1d6434b8b29ae775ad8c2e48c5391`); no case-level `setup.sh` exists.
- Matplotlib's `setup.py` at buggy commit `969513e2a5227331a2eb9e4bc4ba8448a0f9831d` declares `numpy>=1.15` in both `setup_requires` and `install_requires`, plus other runtime dependencies.

Sources:
- [Pinned BugsInPy bug metadata](https://github.com/soarsmu/BugsInPy/blob/11c5f1eea954a42132cfd06bf257766a7963e0fd/projects/matplotlib/bugs/7/bug.info)
- [Pinned BugsInPy empty requirements file](https://github.com/soarsmu/BugsInPy/blob/11c5f1eea954a42132cfd06bf257766a7963e0fd/projects/matplotlib/bugs/7/requirements.txt)
- [Matplotlib setup.py at the buggy commit](https://github.com/matplotlib/matplotlib/blob/969513e2a5227331a2eb9e4bc4ba8448a0f9831d/setup.py)
- [BugsInPy compile script at the pinned dataset revision](https://github.com/soarsmu/BugsInPy/blob/11c5f1eea954a42132cfd06bf257766a7963e0fd/framework/bin/bugsinpy-compile)

Decision: do not classify Matplotlib-7 as a target-test failure, do not accept it, and do not install a guessed or unpinned NumPy version. Keep it blocked until a project-defined dependency installation strategy can be resolved into a frozen, auditable environment lock. The original frozen case stays in the record; no easier substitute is inserted into batch 0.

## Earlier technical signals

A previous run produced five raw buggy-fail/fixed-pass signals for Ansible-7, Black-9, FastAPI-9, Keras-8 and Scrapy-7. These are engineering triage signals only. They are not accepted cases, and they still require review of raw outputs and fixed-worktree patches by independent human reviewers. Scrapy's later run-8 retry was blocked in runner preparation by the version-output pipeline described above; it must be reassessed using the corrected workflow before relying on that case's technical pair.

## Current gate state

No candidate has been promoted to the confirmatory case registry. A job-level Actions success, artifact upload success, checksum pass, or technical signal is not equivalent to case acceptance. Acceptance requires independent review of the license, ground truth, evidence level, leakage/prior exposure, and the complete buggy-fail/fixed-pass evidence. The inference gate remains closed.

## Luigi-8: pytest plugin bootstrap blocker

The run-8 artifact is [artifact 13874255123](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43058520834/artifacts/13874255123).

Observed evidence:

- The pinned BugsInPy requirements specify `pytest==5.4.3`, `pytest-sanic==1.6.1`, and `sanic==20.3.0`.
- The environment build log shows that the `uvloop` wheel build failed. During the later pytest bootstrap, automatic loading of the `pytest-sanic` entry point failed with `ModuleNotFoundError: No module named 'sanic'`.
- The runner misinterpreted the failed `python -m pytest --version` probe as a missing test runner and installed `pytest==6.2.5`. That violates the pinned pytest-sanic constraint (`pytest<6.0,>=5.2`) and still does not repair the missing optional Sanic module.
- The selected target test is a `unittest.TestCase` method in `test/contrib/redshift_test.py`; its imports are Luigi and `mock`, not Sanic or pytest-sanic. Pytest's built-in unittest support is sufficient for this specific target.
- Neither buggy nor fixed target test was executed. The artifact checksum manifest contains 26 entries and all passed independent SHA-256 verification. No technical pair can be claimed.

The next consolidated workflow revision sets `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` only for the Luigi case, both during the pytest version probe and target invocation. This retains the declared pytest 5.4.3 and prevents an unrelated third-party entry-point plugin from aborting startup. The environment variable is present in the pinned pytest 5.4.3 source and disables setuptools entry-point autoload while preserving explicitly specified plugins. No target command, test source, candidate selection or expected outcome is changed.

Sources:
- [Pinned Luigi requirements](https://github.com/soarsmu/BugsInPy/blob/11c5f1eea954a42132cfd06bf257766a7963e0fd/projects/luigi/bugs/8/requirements.txt)
- [Pinned Luigi test command](https://github.com/soarsmu/BugsInPy/blob/11c5f1eea954a42132cfd06bf257766a7963e0fd/projects/luigi/bugs/8/run_test.sh)
- [Selected unittest-based target](https://github.com/spotify/luigi/blob/61ee32e9968978c32be12a6af0affa3a5750e87e/test/contrib/redshift_test.py)
- [pytest 5.4.3 plugin autoload implementation](https://github.com/pytest-dev/pytest/blob/5.4.3/src/_pytest/config/__init__.py)

Decision: keep Luigi-8 blocked until the corrected runner produces raw buggy-fail/fixed-pass results and both raw worktree patches are reviewed. Do not treat the bootstrap failure as a bug outcome or accept the case.
