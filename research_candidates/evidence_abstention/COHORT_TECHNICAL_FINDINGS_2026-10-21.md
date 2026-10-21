# İlk dondurulmuş kohortun teknik bulguları — 21 Ekim 2026

**Durum:** Ön değerlendirme notu. Bu bir vaka kabul kararı, model çıktısı veya doğrulayıcı analiz değildir.

## 1. `BugsInPy-black-3`: hedef test çifti ham teknik sinyali mevcut

- Cohort batch workflow: [run 39648272888](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39648272888)
- Dataset repository: `https://github.com/soarsmu/BugsInPy`
- BugsInPy revision: `11c5f1eea954a42132cfd06bf257766a7963e0fd`
- Metadata path: `projects/black/bugs/3/bug.info`; metadata SHA-256: `09ac24b9d2f0224396efec8d9ef288d4d4605acda48494400b908dfb8c4790cc`
- Recorded/runtime Python: `3.8.3` / `3.8.3` (match)
- Buggy base commit: `8126b4f6a9342290de4655e6a8a78cd288ce7daa`
- Fixed reference: `7a14a37981862ef418f3cdb4a7e2375856f97529`
- Target command: `python -m unittest -q tests.test_black.BlackTestCase.test_invalid_config_return_code`
- BugsInPy `run_test.sh` SHA-256: `41745e9452aa678f675d1f6c66d963586276803f86ada6a9daffe7a8e5adae90`
- Artifact ID: `12369255542`; artifact ZIP SHA-256: `46751205664c0060e712e8278dae96dd27addb40e3551dae17ba999c251affa8`
- Raw buggy log SHA-256: `b5d54b0ee35aa9aecf2b493fecd6546849ce2eec8782989084ca6538580141a0`
- Raw fixed log SHA-256: `11b870b56982a54cd1a0293015807cf6435177ae40d74d4f189bf1818ab6ce78`
- Runtime fingerprint hashes: buggy `d1430cf15702c47640f910ac307b86634e989ddcd277505db0e5c939ac2f7a21`; fixed `4644a53e519611d47a35468e1da4522218d9e2a73bb928f9a26675f1d043d36d`
- Worktree diff hashes: buggy `49e4141003256bbad51ea6d67be6984740c96da77764f86bb3564af37326c1ac`; fixed `9041e7106e96e47f0b966c753ee5e81fdb7b80a187431b82824f15b8967ed09f`
- Automated target exit codes: buggy `1`; fixed `0`. The artifact integrity audit passed.

### One-reviewer technical interpretation (not an independent panel decision)

The pinned BugsInPy patch changes Click's `--config` path option from `exists=False` to `exists=True`. The fixed-commit test `test_invalid_config_return_code` creates a temporary config path, deletes it, then expects Black to return CLI code 2 rather than treating the missing path as a configuration-file read error. The buggy worktree returns code 1 with a “Could not open file … Error reading configuration file: No such file or directory” diagnostic; the fixed worktree passes the same target test.

This log is consistent with the metadata patch and the test's stated expectation. It is a credible **technical failure/fix pair signal**; final ground truth must still be checked and signed off independently by the project’s human review process. The fixed worktree has the buggy base as `HEAD` because the dataset harness applies fixed-commit changes as a patch; this is expected for this tool and is documented in the artifact summary.

## 2. Other first-cohort jobs: no acceptance from setup-only artifacts

The earlier cohort artifacts for `ansible-1`, `cookiecutter-2`, `httpie-2` and `keras-1` in run 39648272888 only include a completed fixed-side setup and no buggy-side target-test exit code. Their summaries have `runtime_python_observed=null`, no paired commits, and no target exit codes. They are **not reproduced pairs**. In that attempt the workflow's buggy-side compilation was terminated during legacy virtualenv activation (`$1: unbound variable`); this is a harness/runtime shell failure, not an application bug.

The follow-up cohort run is [run 39649913996](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39649913996). It improved the runner prep, and the remaining shell-activation failure led to the current runner change: run the pinned BugsInPy compilation script under a fresh Bash process with `SHELLOPTS` removed. The latest run must be inspected before reporting any additional target-test results.

## 3. Acceptance status and prohibition

- Accepted confirmatory cases: **0**
- Accepted upstream projects: **0**
- Model inference for the new study: **not performed**
- Human gold-root-cause decision by two independent reviewers: **not done**
- Independent evidence-sufficiency panel and E1/E2/E3 packets: **not done**
- License, leakage, prior-exposure, calibration and preregistration gates: **open**

Even for `black-3`, the report does not mark `accepted_for_confirmatory=true`. Keep raw logs and hashes intact, then request the documented independent human review, license check, prior-exposure check and evidence-packet construction before any acceptance decision.
