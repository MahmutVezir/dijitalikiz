# Dishka #435 — E3/E2/E1 packet manifest index

**Candidate:** `reagento__dishka-436`  
**Stage 2:** PASS  
**Stage 3:** PASS — project-lead technical gold/tier approval recorded 2026-11-16  
**Final acceptance:** not yet decided; the project lead's four-point exposure/single-adjudicator acknowledgement was recorded on 2026-11-17; schema-conformant case-record construction and validation remain  
**Inference authorization:** false

## Immutable execution artifact

- GitHub Actions run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067
- Reproduction job: `133348644460`
- Artifact ID: `14231689140`
- Artifact URL: https://github.com/MahmutVezir/dijitalikiz/actions/runs/43881610067/artifacts/14231689140
- Artifact ZIP SHA-256: `99c47e28c1707436d7dfa75dcb776f5a0865b2288f1ac16d1baee8d6684c7827`
- Local archive verification: ZIP digest matched; every entry listed in `SHA256SUMS.txt` passed verification.

The archive contains the immutable base/fixed issue logs, base/fixed dataset-selector logs, the exact selector list, base/fixed source snapshots, registry-builder diff, upstream regression-test files, runtime record, and dataset row canonicalization.

## Tier manifests

| Tier | Manifest | Manifest SHA-256 | Evidence items | Mechanisms that remain |
|---|---|---|---:|---|
| E3 | `E3_PACKET_MANIFEST_V0_1.json` | `d75d32da95bfdef73d3824677b6d6df445712967a777580b8867e769c133f131` | 7 | G1, A1, A2 |
| E2 | `E2_PACKET_MANIFEST_V0_1.json` | `8a39ab862393954451f403badd5ccea40350902b39f95ae4e0d7885e9d6751d5` | 9 | G1, A1 |
| E1 | `E1_PACKET_MANIFEST_V0_1.json` | `0fc59ca0ff6cf220b6b46784329b21cdd9d16af3f2211dd29210dd1031f94462` | 13 | G1 |

The manifests use the predeclared mechanism IDs:
- G1: `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`
- A1: `A1_SCOPE_CHAIN_PRECEDENCE`
- A2: `A2_CONSUMER_BINDING_OR_CACHE`

E2 contains every E3 evidence item unchanged and adds the exact buggy-base container/registry lookup sources. E1 contains every E2 item unchanged and adds the buggy/fixed registry-builder sources, the base-to-fix diff, and the upstream cross-scope regression test. The survivor sets match the project lead's approved Stage 3 decision.

## Verified file digests used by the manifests

### Upstream source snapshots

- Base `container.py`: `23bc4ba168e03a2f053c58f98bdf388a9bc21c920c99332fbc4bc53fb5f641c6`
- Base `registry.py`: `24a9967f47a11d63a0d12bd1f3a9ec590f12aa85d55361aba032acaf94674fe3`
- Base `registry_builder.py`: `58cdb82ab89e44549fbf8789390c085040e1f862d0d9887859310959d42dd84f`
- Fixed `registry_builder.py`: `eb245123fd20eb629b7c80ccf0a57246c1bd48db337e019d87db7447ee081a60`
- Registry-builder diff: `360e7f262662646280fc3b5cf5cfd519b28b9f4d0be7b5c2ea2c3f535a4d0e7e`
- Fixed upstream cross-scope regression test: `58b027fab7170fff552d1019b3051f2611ef068a2360e98bf3bd55681e60b462`

### Dataset and issue provenance

- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Canonical row SHA-256: `c548969ec886af21b56c93daae34db1a86b3a10c8dd1473d3d5c886549a9e86d`
- Corrected issue #435 snapshot SHA-256: `086ee0aba856f76397da74a704d98cc8a82e40e165739d9cc352b202d103e8f3`
- PR #436 snapshot SHA-256: `f87785a9189d468e4211ec60aeddf7fdaa1677915fce5dc2c7b3e7a658103d58`
- Independent issue reproducer source SHA-256: `4d06c3ab006c43b134daa7c2b6df5b13ec4e087cecde4170570d6a6f213229f8`

The dataset row is PR-derived and its timestamp matches PR #436 (`2025-04-15T22:52:26Z)); issue #435 has its own earlier timestamp (`2025-04-14T17:22:16Z`). The raw run artifact is immutable and contains the original, incorrect issue-snapshot timestamp hash. The correction is documented separately in `DISHKA_435_POST_RUN_PROVENANCE_CORRECTION_V0_1_2026-11-16.md` and does not alter any test outcome or source-code bytes.

## Attribution and scope

The pinned SWE-rebench dataset repository identifies its dataset license as CC-BY-4.0; retain dataset attribution to PrimeIntellect and the exact dataset revision in any report. The upstream Dishka source/test files at the pinned commits declare Apache-2.0. The documentary source/dependency screen is limited to this pinned reproducer/test environment, not blanket legal clearance or redistribution advice.

The student researcher has full source exposure. The study has one human adjudicator; ChatGPT is advisory input only. Do not claim perfect blinding, inter-human agreement, or Cohen's kappa.

## Acceptance status

The Stage 2/Stage 3 evidence is complete for this candidate. The case has **not** been inserted into the accepted-case registry. The project lead's explicit acknowledgement of full researcher source exposure, the single-human-adjudicator design, the prohibition on human-human reliability/Cohen's kappa claims, and exploratory-only use was recorded on 2026-11-17. This closes that acknowledgement item. Final case acceptance remains pending construction of the complete case record and successful validation against the Draft 2020-12 schema and fail-closed registry checks. The validator is structural only; it does not authenticate external URIs, re-run tests, make legal determinations, or authorize inference. No model inference is authorized.
