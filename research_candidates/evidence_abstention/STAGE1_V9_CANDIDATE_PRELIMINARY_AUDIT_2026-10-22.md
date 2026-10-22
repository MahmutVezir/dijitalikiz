# V9 batch 0 — independent human review handoff (preliminary technical audit)

**Date:** 2026-10-22  
**Status:** Preliminary engineering cross-check only; NOT an independent human review, NOT a case acceptance decision, and NOT a model result.  
**Accepted confirmatory cases after this audit:** 0  
**Model inference on these cases:** none

This supplemental note was prepared after examining source metadata, original fixed commits, raw test logs, and downloadable screening artifacts. Because it exposes root-cause details and test outcomes, it is for coordinating the human review process, not a blinded evidence-sufficiency panel. Independent reviewers must make their own decisions and retain their own evidence notes.

## Integrity verification performed

| Candidate | Downloaded artifact | Archive SHA-256 | Inner `SHA256SUMS` |
|---|---:|---|---|
| BugsInPy-Keras-5 | `12450001876` | `66e5daa97b9e80b42c5f468bbeeff1eaf027cb21c3c1011644f345a07d38ace9` | All entries verified locally |
| BugsInPy-Tornado-6 | `12450860559` | `c73063caf15958f297a7cfa8ec0a29355ba888b35d6178c10b0001e2e93dad26` | All entries verified locally |

The artifact archives' digests match the stored candidate digests. The machine-readable summaries themselves explicitly report `manual_review_required=true`, `accepted_for_confirmatory=false`, and all human review gates still open.

## Candidate A — BugsInPy-Keras-5

### Evidence recorded in the artifact

- Dataset source revision: [BugsInPy commit 11c5f1eea954a42132cfd06bf257766a7963e0fd](https://github.com/soarsmu/BugsInPy/tree/11c5f1eea954a42132cfd06bf257766a7963e0fd/projects/keras/bugs/5).
- Upstream repository: [keras-team/keras](https://github.com/keras-team/keras).
- Buggy commit: [b847b4601d608050bab6eccd049fce28b7bf1b1f](https://github.com/keras-team/keras/commit/b847b4601d608050bab6eccd049fce28b7bf1b1f).
- Fixed commit: [e11c48d9ce3ee47bb8a966549b14cbd5b10ee70d](https://github.com/keras-team/keras/commit/e11c48d9ce3ee47bb8a966549b14cbd5b10ee70d).
- Test command: `pytest tests/keras/utils/data_utils_test.py::test_data_utils`.
- Metadata and observed Python version: 3.7.3 on both sides.
- Buggy test process exit code: 1. Fixed test process exit code: 0.
- Buggy log SHA-256: `0cdbf3efe9d0f387dbab4c6459cb8cf79c9941b98ed952b07d33f984c57ef525`.
- Fixed log SHA-256: `fc207b40653b51e27c88b7ea913bd022bf9093e66b51a4b8cff2e71c34f8c356`.
- Fixed worktree diff stat: `keras/utils/data_utils.py` and `tests/keras/utils/data_utils_test.py`, matching the two files changed in the upstream fix commit.
- The upstream Keras LICENSE file at the fixed revision declares the MIT License. Reviewers should still verify the exact files/provenance and the dataset's own redistribution terms independently.

### Preliminary technical interpretation (not an acceptance decision)

The upstream fix [explicitly describes the defect](https://github.com/keras-team/keras/commit/e11c48d9ce3ee47bb8a966bf257766a7963e0fd): `get_file()` was inconsistent with the Keras backend when `KERAS_HOME` was not the default `~/.keras` directory. The commit changes `keras/utils/data_utils.py` so the default cache directory honours `KERAS_HOME`.

In the recorded buggy log, the first default-home path assertion passes, then after `KERAS_HOME` is set to the temporary `.keras` directory, the intended assertion fails: the downloaded data remains under `/home/runner/.keras` while `K._config_path` points under the temporary test directory. The teardown then also reports leftover files because the assertion interrupted normal test cleanup. The follow-up teardown error should not be mislabelled as a separate root cause.

The fixed-state target test passes in the recorded Python 3.7.3 environment. These are strong target-specific fail/pass signals. Human reviewers still need to confirm the precise source/test/patch linkage, fixture semantics, whether the fixed worktree matches the documented patch, the BugsInPy terms, prior exposure and case independence.

## Candidate B — BugsInPy-Tornado-6

### Evidence recorded in the artifact

- Dataset source revision: [BugsInPy commit 11c5f1eea954a42132cfd06bf257766a7963e0fd](https://github.com/soarsmu/BugsInPy/tree/11c5f1eea954a42132cfd06bf257766a7963e0fd/projects/tornado/bugs/6).
- Upstream repository: [tornadoweb/tornado](https://github.com/tornadoweb/tornado).
- Buggy commit: [fb74e4816ccfa7fc6a7abd8c8aab1f415cfc1b13](https://github.com/tornadoweb/tornado/commit/fb74e4816ccfa7fc6a7abd8c8aab1f415cfc1b13).
- Fixed commit: [2905ee4fb3c283d40b10f609359e189c83a0dc06](https://github.com/tornadoweb/tornado/commit/2905ee4fb3c283d40b10f609359e189c83a0dc06).
- Target commands:
  - `python -m unittest -q tornado.test.asyncio_test.LeakTest.test_ioloop_close_leak`
  - `python -m unittest -q tornado.test.asyncio_test.LeakTest.test_asyncio_close_leak`
- Metadata and observed Python version: 3.7.0 on both sides.
- Buggy target process exit code: 1. Fixed target process exit code: 0.
- Buggy log SHA-256: `306ef13984be2ce474750fd4746a4f5180f9ff42e175bc55eb15bd5ad2e3c63f`.
- Fixed log SHA-256: `4984db83f3cb2e3d3ffdb52fc0f1b61fcd905ddb549e0ea07faeab8c5a2c3d5c`.
- Fixed worktree diff stat: `tornado/ioloop.py`, `tornado/platform/asyncio.py`, and `tornado/test/asyncio_test.py`, matching the three files changed in the upstream fix commit.
- The upstream Tornado LICENSE file at the fixed revision declares Apache License 2.0. Reviewers should independently verify the benchmark dataset's terms and any redistribution constraints too.

### Preliminary technical interpretation (not an acceptance decision)

The upstream fix [describes a leak when event loops are created and destroyed](https://github.com/tornadoweb/tornado/commit/2905ee4fb3c283d40b10f609359e189c83a0dc06). The buggy tests observe the IOLoop-to-asyncio-loop map growing by 10 entries across 10 loop creations/closures where the first test expects no growth; the second test also observes 10 entries where the fixed behavior expects at most one stale entry before cleanup. The fix removes reliance on `WeakKeyDictionary`, cleans previously closed loops at initialization, and removes the loop from the map on `IOLoop.close()`.

Both target tests fail in the buggy state with count assertions and pass in the recorded fixed state under Python 3.7.0. Those are strong target-specific fail/pass signals. Human reviewers still need to assess reference-cycle mechanics, whether all setup/teardown behavior is understood, fixed worktree/patch parity, benchmark provenance/terms, prior exposure, and independence from other selected cases.

## Required next decisions (human-led)

For each candidate, two technical reviewers must complete the blank Panel A forms independently before discussion. Any disagreement must be adjudicated while preserving original ratings. A separate two-person Panel B must assess the blinded E1/E2/E3 packets before any model output is generated. Panel A should not be asked to infer evidence sufficiency solely from the full patch; Panel B must receive only the evidence the model would see.

Neither candidate is promoted by this note. Keep `CASE_REGISTRY.json` unchanged until every case-level gate has independently documented evidence and the global validation preflight passes.
