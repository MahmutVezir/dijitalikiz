# V10 metadata-only intake — 23 October 2026

**Project:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Purpose:** Freeze a clean candidate review order only; this is not an accepted experiment dataset.  
**Inference:** Not performed. **Accepted confirmatory cases:** 0.

## 1. Why V10 replaces the earlier intake

The previous V9 intake had 100 metadata candidates from 13 upstream projects. While constructing a follow-up intake, the newest addendum alone (32 IDs) proved insufficient: older IDs in the historical exposure ledger could re-enter the queue. That attempt is discarded and must not be used as the current intake.

The corrected filter unions:
- 61 unique BugsInPy case IDs extracted from `EXPOSURE_EXCLUSION_LOG_2026-10-21.json`;
- 32 unique IDs in `EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json`.

The two sets have no overlap, giving **93 permanent exclusions**. The source files remain unchanged; the machine-readable union is recorded in [EXPOSURE_UNION_2026-10-23.json](EXPOSURE_UNION_2026-10-23.json). Their original Git blob identifiers are retained there for provenance.

## 2. Local reproduction checks

| Item | Result |
|---|---:|
| Pinned BugsInPy raw metadata inventory | 501 rows / 17 projects |
| Historical queue baseline | 487 rows; reproduced locally byte-for-byte against recorded SHA-256 |
| Union of historical/current exposure IDs | 93 unique IDs |
| Refreshed metadata queue | 407 candidates / 14 projects |
| V10 frozen intake | 100 candidate IDs / 14 projects |
| V10 IDs intersecting the 93-item exclusion union | 0 |
| Accepted confirmatory cases | 0 |
| Bug/fix test pairs run by intake builder | 0 |
| Model inference | 0 |

Provenance hashes for the local outputs:
- Metadata inventory CSV: `069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb`
- Refreshed metadata queue CSV: `91c926665752e0e44c6a4ba499422d2af23c6156f4d61b675e29ca0288a27ece`
- The matching V10 JSON manifest is stored at [SCREENING_COHORT_100_V10_2026-10-23.json](SCREENING_COHORT_100_V10_2026-10-23.json).

This was rebuilt locally from the downloaded/pinned metadata inventory using the documented deterministic project-interleaving order and exposure filtering. The V10 intake itself records that this is a local rebuild pending remote builder execution.

## 3. Remote CI caveat

The latest accessible GitHub Actions records checked during this work showed jobs in a completed/failure state but with no runner steps recorded. Their logs could not be downloaded (`BlobNotFound`). Thus the status does **not** establish that the changed queue builder tests passed or failed in a runner. It is a runner/log-availability blocker and remains open.

PR #119's V10 intake-builder additions and regression tests were merged, but the remote result could not be confirmed from runnable steps. A follow-up change in the current development branch applies the entire historical exposure ledger, adds regression coverage, and updates workflow path triggers. See the pending PR linked from the repository's current issue/PR list.

## 4. Scientific boundary

The 100 IDs are **metadata candidates only**. The V10 manifest does not imply that their tests reproduce the target bug, that the fixed revision passes, or that licenses, root causes, evidence sufficiency, independence, leakage, or human-review gates pass. Technical test runs on V10 candidates must use the fixed selection order and preserve all raw logs; any candidate used to debug the runner is then permanently excluded from the confirmatory sample regardless of outcome.

The formal study remains blocked until at least 60 independent cases across at least 8 upstream projects are accepted (target 80), two disjoint human-review panels complete their work, the semantic evidence auditor is validated against independent blinded ratings, the exact Qwen/tokenizer/GPU runtime and calibration are verified, the protocol is preregistered/frozen, and separate inference authorization is recorded.

No claim about abstention improvement, hallucination reduction, calibration quality, hypothesis support, or finalist status follows from metadata screening.


## Reproducibility-gate implementation update — 23 October 2026

A dedicated, no-inference V10 reproducibility verifier was added at `scripts/verify_evidence_abstention_v10_intake.py`. It compares the freshly rebuilt inventory and queue hashes to the frozen manifest, checks the exact 100-ID queue prefix and project counts, verifies the complete 93-ID exposure union, and requires both generated/frozen manifests to keep acceptance and inference flags closed. Regression tests additionally cover queue-hash changes, candidate-order changes, exposure reintroduction, exposure IDs absent from the inventory, malformed exclusion data and accidental pre-acceptance.

The isolated synthetic test harness run on the verifier and corresponding regression tests completed **7/7 tests successfully**. This is a code-level test using synthetic inventory/queue fixtures; it is not a run against the upstream BugsInPy inventory and is not a scientific result.

The new GitHub Actions workflow is [Evidence abstention V10 metadata reproducibility](https://github.com/MahmutVezir/dijitalikiz/actions/workflows/evidence-abstention-v10-intake-reproducibility.yml). Its first recorded run is [39985336539](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39985336539). The job is marked failed, but GitHub returned an empty step list (`steps=[]`), and log retrieval returned `BlobNotFound`. Therefore the workflow did not provide evidence that any unit test or inventory rebuild actually executed. We classify this as a **runner/log availability blocker**, not as a code-test failure or a successful validation.

**Current gate status:** synthetic verifier tests 7/7 pass locally; actual 501-row upstream inventory/407-row queue/100-row V10 rebuild in a GitHub runner remains unverified; accepted confirmatory cases remain 0; bug/fix tests and model inference remain 0.
