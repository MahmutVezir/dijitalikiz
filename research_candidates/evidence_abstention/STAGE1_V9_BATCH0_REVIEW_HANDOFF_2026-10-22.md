# V9 batch 0 — independent human-review handoff

**Status: technical screening only. No case accepted. No LLM inference.**  
Workflow: https://github.com/MahmutVezir/dijitalikiz/actions/runs/39832920370  
Frozen source: BugsInPy revision `11c5f1eea954a42132cfd06bf257766a7963e0fd`.

## Outcome-independent disposition

The first V9 batch was selected by the frozen queue before these target tests ran. All eight case jobs are now complete. Automated checks are only triage signals; every case remains `accepted_for_confirmatory=false` until the independent review protocol is complete.

| Candidate | Technical signal from artifact | Disposition |
|---|---|---|
| Keras-5 | Python 3.7.3 matches metadata; intended test command failed on buggy tree and passed on fixed tree; artifact integrity passed | Panel A review required; not accepted |
| Tornado-6 | Python 3.7.0 matches metadata; both targeted leak tests failed on buggy tree and passed on fixed tree; artifact integrity passed | Panel A review required; not accepted |
| Scrapy-6 | Buggy and fixed target command sets both failed | Not a qualifying pair on current evidence; inspect raw logs before any further action |
| Matplotlib-5 | No valid buggy-fail/fixed-pass signal; artifact flags environment/dependency or harness uncertainty | Hold/reject unless independently resolved without changing the frozen rule |
| TheFuck-6 | No valid buggy-fail/fixed-pass signal; artifact flags environment/dependency or harness uncertainty | Hold/reject unless independently resolved without changing the frozen rule |
| Luigi-6 | Runtime Python was not captured consistently; no valid target outcome pair | Not eligible on current evidence |
| SpaCy-5 | Environment setup failed before target tests; runtime and source checks incomplete | Not eligible on current evidence |
| Pandas-5 | Both target runs stopped before the target test: pinned pytest bootstrap failed (exit 4); no buggy/fixed test result | Not eligible on current evidence; preserve as environment/setup failure |

## Technical artifact evidence for the two handoff candidates

### Keras-5
- GitHub Actions artifact ID: `12450001876`
- GitHub artifact digest: `sha256:66e5daa97b9e80b42c5f468bbeeff1eaf027cb21c3c1011644f345a07d38ace9`
- Buggy/fixed runtime: Python `3.7.3` / `3.7.3`; recorded metadata `3.7.3`.
- Buggy base commit: `b847b4601d608050bab6eccd049fce28b7bf1b1f`
- Fixed commit reference: `e11c48d9ce3ee47bb8a966549b14cbd5b10ee70d`
- Target: `pytest tests/keras/utils/data_utils_test.py::test_data_utils`
- SHA-256 buggy log: `0cdbf3efe9d0f387dbab4c6459cb8cf79c9941b98ed952b07d33f984c57ef525`
- SHA-256 fixed log: `fc207b40653b51e27c88b7ea913bd022bf9093e66b51a4b8cff2e71c34f8c356`
- SHA-256 artifact audit: `9a03fea142e5159a8312fa66c7f00184062d0db5522037586284766173eb1dc6`

### Tornado-6
- GitHub Actions artifact ID: `12450860559`
- GitHub artifact digest: `sha256:c73063caf15958f297a7cfa8ec0a29355ba888b35d6178c10b0001e2e93dad26`
- Buggy/fixed runtime: Python `3.7.0` / `3.7.0`; recorded metadata `3.7.0`.
- Buggy base commit: `fb74e4816ccfa7fc6a7abd8c8aab1f415cfc1b13`
- Fixed commit reference: `2905ee4fb3c283d40b10f609359e189c83a0dc06`
- Targets: `tornado.test.asyncio_test.LeakTest.test_ioloop_close_leak` and `tornado.test.asyncio_test.LeakTest.test_asyncio_close_leak`
- SHA-256 buggy log: `306ef13984be2ce474750fd4746a4f5180f9ff42e175bc55eb15bd5ad2e3c63f`
- SHA-256 fixed log: `4984db83f3cb2e3d3ffdb52fc0f1b61fcd905ddb549e0ea07faeab8c5a2c3d5c`
- SHA-256 artifact audit: `44aced57b463d14f7e450ae417110c8016e0382b31c39e3dcb70b00a9af9d1fb`

The workflow records that BugsInPy may keep the buggy base as Git HEAD while applying the fixed revision as a working-tree patch. Panel A must inspect raw checkout logs, fixed-tree diff/status, exact test output, patch/source provenance, and license before accepting either candidate. A CI pass/fail signal is not itself proof of the root cause.

## Mandatory independent review gates

1. Two independent Panel A reviewers verify the root cause, intended test pair, source/patch provenance, license, distinctness and prior-exposure/contamination.
2. Two disjoint Panel B reviewers independently assess packet sufficiency without seeing case identity, gold root cause, patch, fixed code, hidden E-level label, or condition.
3. Create E1/E2/E3 blinded packets from the frozen evidence policy; validate only structure/hash at first. The structural validator is not a semantic sufficiency judge.
4. Preserve original independent ratings and adjudication records. No inference until at least 60 accepted cases from at least 8 upstream projects, calibration and runtime gates, artifact hashes, preregistration and explicit authorization are complete.

### Pandas-5 final artifact

- GitHub Actions artifact ID: `12450841813`
- GitHub artifact digest: `sha256:40a9a744cbbc94ac93f3961b70b10410d77a757a5eed18c019cfedca0e12da0d0`
- Target: `pytest pandas/tests/groupby/test_function.py::test_ops_not_as_index`
- Pinned pytest bootstrap failed with exit code 4 on both buggy and fixed sides; neither target test ran.
- Artifact audit SHA-256: `d57e5bfb7356d3e20502c57c8a78b04d5baaa222acaf73a9db835a174ed48823`

## Interpretation boundary

These are two technical screening candidates, not two accepted research cases. No model response has been generated. No statement about hallucination rate, abstention efficacy, confidence calibration, or hypothesis support can be inferred from this workflow.
