# pyro-ppl/numpyro #1916 — candidate review

**Cohort rank:** 12 of 96 primary candidates  
**Dataset instance:** `pyro-ppl__numpyro-1918`  
**Issue:** https://github.com/pyro-ppl/numpyro/issues/1916  
**Fix PR:** https://github.com/pyro-ppl/numpyro/pull/1918  
**Review status:** verified fallback candidate if Dishka fails a remaining gate. NumPyro remains a provisional technical candidate: Stage 2 exact base-fail/fixed-pass is verified; the real E1/E2/E3 packet set has now passed the structural CI contract; semantic tier adjudication, candidate exposure/independence, documentary license-scope review and final acceptance remain open. The case is **not accepted**.

## 1. Defect contract

Issue #1916 reports that calling `MCMC.run` after `MCMC.warmup` with an AIES ensemble kernel raises a JAX PRNG-key shape error in vectorized multi-chain execution. The reporter also states that ESS exhibits the same error.

PR #1918 changes the warmup-state handoff for ensemble kernels: when `_warmup_state` exists, it supplies the first key from the batched key array; non-ensemble kernels retain the prior behavior. The PR adds a `test_warmup` regression test parameterized over AIES and ESS with 10 vectorized chains.

## 2. Pinned source and dataset identity

- Upstream repository: `pyro-ppl/numpyro`
- Buggy base: `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`
- PR head: `d5367f16abee85a1d7788784c71eb908ecb12df7`
- Fixed upstream merge revision: `5692d2da335945b756aeae02e3720b9b7f3efef2`
- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Dataset revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Dataset Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Exact row: `pyro-ppl__numpyro-1918`
- Canonical row SHA-256: `d0dfd87ddd0598ebf368352385419aad6e2d571d2ac83dad04fe57612a7b9646`
- Row metadata: `pyro-ppl/numpyro`, base SHA above, `2024-11-28 00:54:29`, Python, Apache-2.0
- Frozen selectors:
  - `test/infer/test_ensemble_mcmc.py::test_warmup[AIES]`
  - `test/infer/test_ensemble_mcmc.py::test_warmup[ESS]`

The dataset row was authenticated in the run and stored in the artifact. The two selectors are test variants within one upstream project; they are not two independent cases.

## 2A. Exact source-code cross-check

The upstream files were fetched independently at the pinned revisions and compared around the failing path:

- Buggy-base `numpyro/infer/mcmc.py`, Git blob SHA-1 `dd3ec0c3a782c1e1530b138153d821392ee5bebd`: lines 654–660 split a scalar key into per-chain keys, then pass the resulting array unchanged into `_warmup_state`.
- Buggy-base `numpyro/infer/ensemble.py`, Git blob SHA-1 `64a2870ade0565cb6547cc92d97c11502e769bfd`: lines 190–193 unpack the state and call `random.split(rng_key)`.
- Fixed `numpyro/infer/mcmc.py`, Git blob SHA-1 `7dd596bca382c4f6517e93458c5806c690cddb59`: lines 661–664 use `rng_key[0]` only for ensemble kernels and preserve the full key array for non-ensemble kernels.
- Fixed regression test file, Git blob SHA-1 `bda377b993ef198960eddc0b27b9e217978d20a3`: lines 101–115 add the AIES/ESS vectorized warmup-then-run test.

The source-level difference matches the observed runtime trace. These anchors support the proposed mechanism but do not replace Stage 3 human adjudication.

## 3. Latest exact Stage 2 reproduction — 18 November 2026

Latest branch-head workflow: https://github.com/MahmutVezir/dijitalikiz/actions/runs/44338919763

- Workflow run: `44338919763`
- Job: `134923384282` (`numpyro-issue-1916-reproduction`)
- Job conclusion: **success**
- Artifact ID: `14441559416`
- Artifact: `numpyro-issue-1916-reproduction`
- Artifact ZIP SHA-256: `b90d9c22614e277c3888cca9d7d62b97dfc51523bf9d145e20083e9a6c5ff360`
- Independent local verification: outer SHA-256 matched the GitHub artifact digest; ZIP CRC passed; all 15 payload-file hashes in `SHA256SUMS.txt` passed.

Observed selector results, using the same pinned CPU environment and the same two test selectors:

| Revision | AIES selector | ESS selector | Contract |
|---|---:|---:|---|
| Buggy base `07e4c9b...` | Executed and failed with the reported PRNG-key shape error | Executed and failed with the reported PRNG-key shape error | 2/2 expected failures |
| Fixed merge `5692d2d...` | Passed | Passed | 2/2 passes |

The failing path reaches `numpyro/infer/ensemble.py` in `EnsembleSampler.sample`, where `random.split(rng_key)` receives a traced key array with shape `(10, 2)`; JAX requires one key at this call site. The fixed run passes both selectors (one pass per selector). The reporter's original example uses 100 chains; the pinned regression selectors exercise 10 chains.

Relevant artifact hashes:
- Full upstream PR patch: `d05cbdbc3b934c55ace104d7d031c9987d61db5e1abba815104eab8004af5512`
- Dataset-only test patch applied to the buggy base: `03df1473e0a8ebcdba4f5981b2f8dfeef57484088a66c495bcc903204dbb51e4`
- Buggy-base test log: `0c4e0e335b80877185ab2b54ec527add0bd1e1b9c733511c4f71aa09e4ba20c1`
- Fixed-revision test log: `e268b6d982d0d335970c28310727c3e822e7e1684a076db2f2b854b9b186901b`
- Dependency lock file SHA-256: `8a160de15a15792632268e9840879fe262b98413ac1c5fe7bcf4253631f6bbb5`
- Dependency-license inventory artifact SHA-256: `20b6109dae0af95a6c4917cadca00c958e5aa9cc02f11c536854c78305d7eaba`

This closes the previous review's statement that the corrected workflow had not run. The 18 November repeat is the current evidence; the historical failed attempt against the fork-only PR-head SHA remains recorded as workflow history, not as the current result.

## 4. Source and dependency license screen

- The exact-base NumPyro source declares Apache License 2.0; both changed source/test files carry SPDX Apache-2.0 headers.
- The reproduction uses a CPU-only pinned environment. No GPU, external service or downloaded model is required.
- The lock explicitly pins 17 runtime/test packages and their transitive requirements. The workflow recorded license text/classifier metadata for all 17 before executing upstream source tests; the metadata-presence gate passed.
- The captured NumPy 1.26.4 metadata identifies its binary distribution's bundled OpenBLAS (BSD-3-Clause), LAPACK (BSD-3-Clause-Attribution) and GCC runtime library/libgfortran (GPL-3.0-with-GCC-exception). This merits a scope/notice check; it does not by itself establish a license conflict or determine what must be redistributed in the final project artifact.
- Metadata presence is not legal clearance. The inventory does not replace review of bundled components, notices, redistribution scope or competition-use conditions.
- Project-lead acknowledgement of the narrow dependency/license scope remains open. This is not legal advice or blanket approval for optional extras or redistribution.

## 5. Proposed technical mechanism and alternatives

A separate Stage 3 proposal is recorded in `NUMPYRO_1916_GOLD_AND_EVIDENCE_TIERS_DRAFT_2026-11-18.md`. In brief, the leading mechanism is a mismatch between the batched per-chain PRNG key carried through the warmup-state path and the singleton key expected by `EnsembleSampler.sample`. The upstream fix's conditional selection of `rng_key[0]` for ensemble kernels is consistent with that mechanism.

The mechanism, alternative hypotheses, and the proposed E1/E2/E3 evidence subsets are **drafts for project-lead adjudication**. The fix patch and fixed-revision pass records are reserved for hidden adjudication evidence and are not proposed as model-visible packet items, to avoid leaking the correction. The three-tier set is not yet operationalized or validated.

## 6. Independence, exposure and acceptance

- The cohort contains one primary candidate for `pyro-ppl/numpyro`; the project can contribute at most one accepted case.
- The student project lead has reviewed the issue, PR, source patch and reproduction results during candidate screening. This exposure is disclosed; perfect blinding is not claimed.
- Rater B's case-specific exposure/independence screen and participation status have not been confirmed. Rater B is for blinded model-output scoring only, not technical-gold or E1/E2/E3 adjudication.
- Fork/lineage, issue-family duplication and the final candidate-specific exposure decision remain open.
- The public issue/PR dates are after the September 2024 release of Qwen2.5-3B-Instruct. This timing reduces one narrow exposure concern but does not establish complete training-data provenance.

Current disposition:
- Static issue/patch alignment: strong.
- Exact dataset row and selectors: authenticated.
- Stage 2 exact base-fail/fixed-pass: passed, repeated on the 18 November branch head.
- Source/dependency documentary metadata: recorded; human license-scope sign-off pending.
- Technical gold and at least two alternatives: proposed, not adjudicated.
- E1/E2/E3 packet construction and packet-set hash: built and pinned; structural CI validation passed in run `44537219541`. Semantic adequacy remains unadjudicated and the packets have not been released for blind review.
- Independence/exposure review: open.
- Stage 3 adjudication: not complete.
- Final case acceptance: **not accepted**.
- Model loading, inference and fine-tuning authorization: **false**.


## Stage 3 packet construction addendum — 19 November 2026

The project lead reports that a second reviewer concurred with proceeding on the E1/E2/E3 design logic, conditional on preserving the scientific safeguards. This is not semantic tier adjudication or case acceptance; the reviewer identity is retained outside the public record.

Two real-case files were added:
- `numpyro_1916/OPERATIONAL_EVIDENCE_PACKET_SET_V0_1_2026-11-19.json`
- `numpyro_1916/EVIDENCE_PACKET_PROVENANCE_V0_1_2026-11-19.json`

Packet-set SHA-256: `7156e7c0bebf694946495b638f8dd21fbe45b7fbafde2607e6cc11e8b4f9bdfc`.

The exact issue-row excerpts were reconstructed from the immutable dataset row and checked against the recorded UTF-8 byte ranges and SHA-256 values: narrative/reproducer bytes [0,836), traceback bytes [838,5775). The two buggy-base source excerpts were fetched at commit `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d` and their excerpt hashes match the proposal: `mcmc.py` lines 654–660 and `ensemble.py` lines 190–193. The inner packets contain 1, 2 and 4 items for E3, E2 and E1 respectively; repeated items are byte-identical and the evidence ID sets are strictly nested.

A real-packet regression test was added to `implementation/test_evidence_level_packet_set.py`, calling the existing `validate_packet_set` with the externally pinned packet-set SHA. Its CI result has not yet been observed, so the existing operational validator is **not yet reported as passed on this real packet**. The manifest construction and SHA-256 computations were performed; CI confirmation remains pending.

Semantic adequacy remains open. In particular, the E1 source excerpts expose both the MCMC key-array handoff and the ensemble sampler's scalar `random.split` call, but an independent panel must decide whether this truly eliminates the sampler-contract alternative. The project lead's design approval cannot substitute for Panel B's blinded mechanism ratings. No fix patch, fixed-pass log, gold label, or E-level label is included in the model-facing inner packets. The outer packet set is for preparation/validation only.

Current disposition: Stage 2 passed; Stage 3 packet construction complete; structural CI validation pending; semantic adjudication pending; exposure/independence and human license-scope review open; final case acceptance remains `not_accepted`; inference remains unauthorized.


**Source hash clarification:** For the two source-code items, `source_snapshot_sha256` binds the exact verbatim excerpt snapshot; the parent files are independently anchored by immutable upstream commit and Git blob SHA-1. The excerpt's own bytes are separately bound by `content_sha256`.


## Stage 3 fallback readiness after Dishka exposure correction — 19 November 2026

### Latest repeat and structural CI result

The most recent NumPyro Stage 2 job on this branch is:
- Run: [44537219541](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44537219541)
- Job: `135605947673` — success
- Artifact ID: `14536697284`
- GitHub-reported artifact SHA-256: `88273ec9df2633d2d3a360e0f5c86188d92c5e87318e312a183bc77bf1071556`

The earlier 18 November artifact remains the latest artifact whose full archive was independently downloaded and verified in the recorded audit: run `44338919763`, artifact `14441559416`, SHA-256 `b90d9c22614e277c3888cca9d7d62b97dfc51523bf9d145e20083e9a6c5ff360`, ZIP CRC PASS and 15/15 payload hashes PASS. The newer 19 November artifact has a successful job and GitHub-reported digest; do not claim independent local archive verification for that newer artifact unless separately performed.

The full workflow run `44537219541` concluded `failure` because Nox, Werkzeug and Moto candidate jobs failed their respective selector contracts. This does not negate the successful NumPyro job or no-inference preflight job, and it must not be described as a fully green candidate matrix.

### Structural packet validation — passed, semantics still open

The exact packet-set file:
`numpyro_1916/OPERATIONAL_EVIDENCE_PACKET_SET_V0_1_2026-11-19.json`

Pinned packet-set SHA-256:
`7156e7c0bebf694946495b638f8dd21fbe45b7fbafde2607e6cc11e8b4f9bdfc`

The dedicated real-packet test passed under the successful no-inference preflight job. It verified:
- externally pinned packet-set digest;
- identical evidence content across levels for shared evidence IDs;
- strict E3 ⊂ E2 ⊂ E1 nesting;
- E2's only addition over E3 is the traceback excerpt;
- E1's additions over E2 are the two buggy-base source excerpts;
- no gold/tier/fix fields in the model-facing packet set;
- structural validator explicitly does **not** assess semantic sufficiency and performs no model inference.

Thus, packet construction/integrity is no longer the blocker. The central open question is whether the source excerpts in E1 really exclude all but one defensible cause, especially the competing “sampler should accept/map batched keys” explanation. Reviewers must be allowed to conclude E1 is insufficient. If that happens, revise the evidence design prospectively or exclude NumPyro from the three-tier sample; do not force a unique-cause label.

### Human review prerequisites — do not count a simple YES as semantic adjudication

The active `NUMPYRO_1916_PANEL_B_SEMANTIC_REVIEW_PROTOCOL_V0_1_2026-11-19.md` requires separate roles:
- Panel A: at least two independent source-aware technical reviewers to establish gold, alternatives and issue/test/fix alignment. Their initial independent records must be preserved.
- Panel B: at least two independent reviewers, disjoint from Panel A and the project lead, who have not seen the NumPyro issue, PR, patch, fixed source, gold, reproduction or packet-construction material. They must rate each coded packet separately, without tier labels or a leading list of proposed mechanisms.
- Disagreement adjudication: a third person independent of the two Panel B raters, after both initial reviews are locked.
- Restricted reviewer delivery, access log, separate opaque packet codes and randomized presentation order are mandatory. The public GitHub repository is not an access-controlled reviewer store.

The existing protocol explicitly excludes Panel Reviewer H from Panel B because this reviewer has seen the design proposal. The project lead is also excluded. Panel Reviewer B's eligibility is **unknown** until this reviewer's case-specific exposure/independence declaration is completed. A simple yes/no endorsement from someone who has seen the design or source cannot be called a blinded semantic review. If two eligible Panel B raters and the independent adjudicator cannot be found, keep semantic adjudication pending; do not weaken the requirements.

### Remaining NumPyro case-level gates

1. Screen prior pipeline/debug/test-oracle exposure; current v0.2 acceptance requires `none`.
2. Complete the candidate-specific fork/lineage, related-defect cluster and one-case-per-project independence check.
3. Complete the source/dependency/fixture notice screen, including the recorded NumPy/OpenBLAS/LAPACK/libgfortran scope; this is documentary review, not legal clearance.
4. Complete Panel A technical gold/alternative review independently and Panel B blind semantic packet review under the role restrictions above.
5. If the E1/E2/E3 thresholds are not met, do not accept this as a three-tier case. Preserve the result and move to the next technically passing candidate or amend the design prospectively before any outcomes.
6. Only after the case record is complete may the proposed v0.2 schema validation and a separate final project-lead acceptance decision be performed.

**Current disposition:** Stage 2 PASS; real packet structure PASS; semantic review pending; independence/exposure/license gates open; final accepted-case count remains 0; no model load, inference or training.


## Candidate order correction — 19 November 2026

An earlier note described NumPyro as the next candidate after Dishka had been excluded. That ordering is superseded: the project lead later clarified Dishka's prior pipeline/debug exposure as `none`, so Dishka remains first for formal proposed-case and acceptance checks. NumPyro remains the fallback candidate, not the current first-priority case. Its own Stage 2 PASS and structural packet validation remain valid, but its semantic adjudication, exposure/independence and dependency-license gates remain open.


## Superseding active-intake update — 20 November 2026

Dishka #435 has been accepted by the project lead into the v0.2 exploratory/feasibility registry and its post-acceptance no-inference CI passed on commit 931eb6dfb3728fec3c8f729d27d7038f4fd4684e. NumPyro #1916 is therefore now the **next sequential independent-project candidate**, not merely a fallback if Dishka fails.

### E1 semantic critique and proposed amendment

The original 19 November E1 showed the MCMC.run warmup-state handoff and the failing EnsembleSampler.sample random.split call, but it did not show how EnsembleSampler initializes its own state. This left a live alternative: perhaps the sampler contract expects a batched key at sample time. The pinned buggy-base EnsembleSampler.init code (numpyro/infer/ensemble.py, lines 150–183) now appears as an additional item in a separate proposed v0.2 packet set. That code checks the batch shape to derive the number of chains, then selects rng_key[0], splits it, and stores the resulting scalar key in EnsembleSamplerState. It materially strengthens the causal chain but does not itself constitute human semantic approval.

Proposed packet set: research_candidates/evidence_abstention/numpyro_1916/OPERATIONAL_EVIDENCE_PACKET_SET_PROPOSED_V0_2_2026-11-20.json; SHA-256 e1730956eb9cfc9015bb43c5725f49d3ebff9dfc3c564594060209bab5e5485d. The 19 November v0.1 packet set remains unchanged. Proposed counts are E3=1, E2=2, E1=5; strict nesting and semantic sufficiency must be confirmed by CI and independent reviewers respectively.

### Mandatory independent review and exposure boundary

The protocol requires two independent source-unexposed Panel B reviewers, a separate adjudicator, and source-aware Panel A technical review. The project lead has inspected the source, patch, and reproductions and is not eligible for blinded Panel B. Hasan has seen the E1/E2/E3 design proposal, so Hasan is also ineligible for blinded Panel B for this case; no other role is assumed without a separate competence, consent, and independence declaration. No Panel B reviewers are currently appointed, no coded packet has been delivered, and no semantic rating or adjudication exists.

### Remaining candidate gates

- Confirm upstream issue-family independence and fork/lineage classification for dataset row pyro-ppl__numpyro-1918.
- Complete exact dependency lock, upstream source, changed-file, and runtime-license scope review; project-lead acknowledgement remains pending and is not legal clearance.
- Reconcile the latest Stage 2 artifact's GitHub digest with an independently downloaded archive before relying on it as locally integrity-verified; the earlier 18 November artifact has local ZIP CRC and 15/15 payload-hash verification.
- Run no-inference CI against the proposed v0.2 packet set; do not call structural validity a semantic result.
- Obtain Panel A/Panel B participation and separate adjudication under the already-approved protocol; otherwise the case remains not accepted.

No model loading, inference, fine-tuning, or training is authorized.



## Superseding evidence and review update — 20 November 2026

### Stage 2 archive independently verified

The 19 November NumPyro reproduction artifact was downloaded and checked locally:
- Workflow run: `44537219541`; job: `135605947673`; artifact: `14536697284`.
- Local ZIP SHA-256: `88273ec9df2633d2d3a360e0f5c86188d92c5e87318e312a183bc77bf1071556`, matching the GitHub-reported artifact digest.
- ZIP CRC: PASS; all 15 entries in `SHA256SUMS.txt`: PASS.
- The artifact contains the exact Parquet row snapshot, both selectors, base-fail and fixed-pass JSON result files, environment freeze, and a 17-package dependency-license metadata inventory.
- The exact pinned base/fixed commits and both selectors match the candidate review above. The AIES and ESS selectors each fail on the buggy base with the batched PRNG-key shape error and pass on the fixed merge (2/2 expected base failures; 2/2 fixed passes).

### Dataset/source license distinction

The exact dataset row records the source repository's license as Apache-2.0. The dataset repository's current Hugging Face metadata identifies the dataset itself as CC-BY-4.0; this is a separate license layer. The current card metadata was retrieved on 20 November 2026, but the card's license field has not yet been independently authenticated from the exact pinned dataset revision. The upstream NumPyro root `LICENSE.md`, setup.py metadata, and both modified files' SPDX headers identify Apache-2.0. The pinned dependency inventory is recorded, but metadata presence is not legal clearance; several entries require exact notice/scope review.

Detailed record: `numpyro_1916/NUMPYRO_1916_DEPENDENCY_LICENSE_SCOPE_REVIEW_V0_1_2026-11-20.json`.

### Issue-family and project independence screen

The canonical project is `pyro-ppl/numpyro` (upstream repository is not a fork); the merged fix PR originated from contributor fork `amifalk/numpyro`. The candidate consists of one issue, one PR, one dataset row and two AIES/ESS test variants. These two selectors are one defect case, not two independent samples. The upstream repository is distinct from the first accepted project, `reagento/dishka`.

Related same-repository issues #2132, #2338, #2359 and #2392 concern adjacent warmup/resume, repeated-run, vectorized-chain or ensemble-kernel behavior, but their documented symptoms/mechanisms differ. They are retained as a related issue-family cluster and excluded from the independent-case count. NumPyro still contributes at most one accepted case. The reviewer/adjudicator role requirements remain open; neither the project lead nor Hasan is eligible for blinded Panel B because each has seen candidate source/design material.

Detailed record: `numpyro_1916/NUMPYRO_1916_ISSUE_FAMILY_INDEPENDENCE_REVIEW_V0_1_2026-11-20.json`.

### Proposed E1 packet CI status

The separate v0.2 proposed packet set (E3=1, E2=2, E1=5; SHA-256 `e1730956eb9cfc9015bb43c5725f49d3ebff9dfc3c564594060209bab5e5485d`) passed the added structural regression test in Research Validation run `44730945050` on commit `848410738109f24bf3f87403760d15b29071dd66`. The repository-wide validation reported 454 passed, 6 skipped, 56 subtests passed. The no-inference preflight run `44730944964` also passed, with 1 accepted case/1 project and 13 global study-readiness blockers. This CI result validates structure/hashes only; it does not validate E1 semantic sufficiency or accept NumPyro.

### Current disposition

Stage 2 reproduction and artifact integrity: PASS. Proposed E1 v0.2 packet structure and CI: PASS. Upstream project independence from Dishka: PASS. Related issue-family review: documented, with neighboring issues retained as one NumPyro cluster. Dependency/source and dataset-license scope: documented, project-lead scope acknowledgement and exact pinned dataset-card license authentication still pending. Panel A, two blinded Panel B reviewers, separate adjudicator and restricted access-controlled delivery: NOT completed. Final case acceptance: NOT accepted. Model load, inference and fine-tuning: prohibited.


## 20 November 2026 — operational review handoff prepared

The latest candidate-scope and structural CI updates are recorded in the progress ledger. A separate Panel A gold review form is available at `numpyro_1916/NUMPYRO_1916_PANEL_A_GOLD_REVIEW_FORM_V0_1_2026-11-20.md`. A local Panel B bundle builder is available at `implementation/build_numpyro_1916_blinded_review_packets.py`; its regression tests are at `tests/test_build_numpyro_1916_blinded_review_packets.py`. The builder emits two randomized reviewer ZIPs and a separate custodian mapping, but does not upload or send files. Do not use it until two eligible, source-unexposed Panel B reviewers are consented and a restricted delivery store/access log are available. No reviewer or adjudicator is currently recorded; no semantic rating or case acceptance is implied.


## Case-specific timestamp reconciliation — 20 November 2026

The exact pinned row's raw `created_at` value is `2024-11-28 00:54:29`. GitHub's upstream PR #1918 `created_at` value is `2024-11-28T00:54:29Z`; these match after UTC normalization. The issue itself was created earlier, at `2024-11-25T14:53:29Z`, so the dataset timestamp corresponds to the PR, not the issue. The pinned row SHA-256 is `d0dfd87ddd0598ebf368352385419aad6e2d571d2ac83dad04fe57612a7b9646`, and the source Parquet SHA-256 is `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`. The raw row was included in the locally verified Stage 2 artifact. This verifies the NumPyro row's timestamp provenance; it does not close the cohort-wide dataset timestamp gate.


## Branch-head CI and disposition update — 20 November 2026

The no-inference preflight workflow was extended so that changes to the NumPyro evidence directory and its three dedicated review-test modules trigger an explicit NumPyro contract step. The step is included in the uploaded preflight log artifact.

- Commit: `982ec18982591b1c21989f6fb3b68720f26241cc`.
- Workflow run: `44736373993`, overall conclusion **success**.
- No-inference preflight job: `136288676575`, **success**.
- NumPyro-specific tests: **8 passed** across the proposed packet/provenance, license/independence, and blinded-bundle builder test modules.
- All preflight groups: packet audit 12; operational/nested packets 25; NumPyro review contracts 8; selector runner 6; exploratory acceptance/readiness 24; study-design/dual-human scoring 10. Total: **85 passed**.
- Preflight log artifact: `14628258416`; SHA-256 `33585baab1d76690ab23b01dc6888fd0f340dcccc2003a650a9b0c413f4dca52`.

The readiness report remains `blocked_before_inference`: one accepted case/project (Dishka #435), 13 global blockers, `ready_for_inference=false`, and `inference_authorized=false`. The same run's Dishka reproduction and raw-provenance audit succeeded; its Qwen license-metadata capture ran without loading model weights and succeeded. Other candidate reproductions were skipped.

The full repository Research Validation on the immediately preceding commit `62b5915ed1eec6d7460d6060de76122c66a6d1b3` passed 460 tests, with 6 skipped and 56 subtests passed. The following commit `982ec189` changed the preflight workflow only; its branch-head no-inference tests are the 85-pass result above.

**NumPyro disposition is unchanged:** Stage 2 and structural packet validation remain technically passed; semantic sufficiency is not assessed; Panel A/Panel B human review, adjudication, exact pinned dataset-card license authentication, human license-scope acknowledgement, and final project-lead acceptance remain open. NumPyro is not accepted. Dishka's existing acceptance is unchanged. No model loading, inference, fine-tuning, or training was performed or authorized.


## Independent issue reproducer added and verified — 20 November 2026

To match the Dishka evidence standard, a separate public-API reproducer was added in `reproduction/numpyro_issue_1916/test_issue_1916.py`. It does not call the upstream PR's parameterized test. It follows the reporter's actual `MCMC.warmup()` then `MCMC.run()` sequence with AIES, 100 vectorized chains, and the exact pinned CPU-only dependency lock.

- Workflow: [NumPyro #1916 independent reproducer run 44737978562](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44737978562).
- Commit: `2b0f4f95e951b6ab7079a20f057ada701660d1ce`.
- Job: `136294098282`, conclusion: success.
- Exact buggy base: `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`.
- Exact fixed merge: `5692d2da335945b756aeae02e3720b9b7f3efef2`.
- Buggy-base outcome: the independent reproducer executed and failed at `EnsembleSampler.sample -> jax.random.split` with the expected key-array shape `(100, 2)`; collection succeeded and the defect-specific signature was present.
- Fixed-revision outcome: the same test and same environment passed (`1 passed in 3.70s`).
- Runtime: CPython 3.11.9; CPU-only JAX/JAXlib 0.4.35; 17 pinned runtime/test packages; `pip check` passed.
- Reproducer SHA-256: `90e6ed63eda943e6fd623e24b4b3cafcd0c7c5f43db80394135cfaac4bbbe71d`.
- Dependency lock SHA-256: `8a160de15a15792632268e9840879fe262b98413ac1c5fe7bcf4253631f6bbb5`.
- Artifact: `14629441931`; GitHub digest and independently downloaded outer SHA-256: `26142beee2bbb09c16933d59f54b3480a2445e52f7f2dbfa63fee0a5cb53f581`. ZIP CRC passed; all 10/10 internal SHA256SUMS entries passed.

This closes the missing standalone issue-reproducer parity point against Dishka. Together with the separately verified two frozen AIES/ESS dataset selectors, NumPyro now has an independent public-API reproducer plus its exact dataset-selector base-fail/fixed-pass evidence.

### Candidate disposition and remaining human decision

The project lead's 20 November instruction is recorded as a **conditional preference to count NumPyro if its evidence is at least equivalent to Dishka**; the project lead reports Hasan shares that preference. The technical reproduction comparison now meets that threshold. This statement is not represented as Hasan's signed review or as a blinded assessment.

The proposed causal mechanism remains: during the documented warmup-resume path, `MCMC.run` replaces the ensemble sampler state's scalar PRNG key with the per-chain key batch; `EnsembleSampler.sample` then calls `random.split` as though it received a single key. The pinned initializer excerpt shows that the ordinary ensemble state stores a scalar key. The exact model-facing E1/E2/E3 proposal remains structural-only; the source-aware human project-lead gold/tier decision must be explicitly recorded, using the same single-adjudicator exploratory limitation accepted for Dishka. Hasan's concurrence may be recorded as project-lead-reported supplementary input; no blind-review or inter-rater reliability claim will be made.

The bounded documentary license-scope acknowledgement and the project-lead's case-specific `prior_pipeline_debug_exposure` declaration also remain to be recorded. Dataset-card attribution and scope are not legal clearance. No model operation is authorized. Final NumPyro acceptance remains pending; Dishka's accepted record is unchanged.


## Superseding v0.2 adjudication-route clarification — 20 November 2026

This addendum supersedes candidate-specific wording above that treated two independent blinded Panel A reviewers, two blinded Panel B reviewers and a third adjudicator as mandatory **for technical gold and E1/E2/E3 tier construction**.

The controlling v0.2 exploratory protocol and the Dishka #435 accepted precedent use this division of responsibility:

- The student project lead is the single source-aware human adjudicator for the candidate's technical gold mechanism, alternatives, and E1/E2/E3 tier membership/rationale.
- ChatGPT is an advisory critic only, not a human rater or adjudicator.
- Hasan's contribution may be recorded as project-lead-reported, source-aware supplementary technical input. It is not a separate signed independent adjudication, a blind review, or inter-rater evidence.
- The project lead's full source exposure must be disclosed. No researcher blinding or Cohen's kappa / human-human agreement claim is made for gold/tier construction.
- The two-human requirement in the active v0.2 protocol applies to the later independent scoring of raw model responses for evidence support (Rater A and eligible, consented, case-unexposed Rater B). It does not make two external source-unexposed reviewers a precondition for the project lead to decide gold/E1/E2/E3.
- Rater B's consent, exposure screen and scoring-rubric freeze remain required before model-output scoring. They do not replace or independently validate the gold/tier decision.

Accordingly, NumPyro's next gold/tier gate is the project lead's explicit source-aware technical decision, with ChatGPT critique and any Hasan input separately labelled. The proposed E1 packet's causal sufficiency must be assessed honestly; the project lead may decide E1 is insufficient, in which case the three-tier case is not accepted or must be revised prospectively. No tier is forced.

The technical evidence now meets the Dishka Stage 2 parity threshold: two frozen AIES/ESS selectors plus the independent 100-chain public-API warmup-to-run reproducer, all exact buggy-base failures and matching fixed-revision passes. This is **not** the final case-acceptance decision.

### Latest independent reproducer repeat — branch head 20 November 2026

- Workflow: [NumPyro #1916 independent reproducer run 44741768086](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44741768086).
- Job: `136306920441`, conclusion: success.
- Latest artifact: `14630982034`, GitHub SHA-256 `bdbe89447f1b1b5b4bbbd3c682d90d6f56e6abe0d2097eddce79acaf9e32fc0d`.
- The archive was downloaded and independently checked: outer SHA-256 matched the GitHub digest, ZIP CRC passed, and all 10/10 internal SHA256SUMS entries passed.
- The same public-API 100-chain AIES reproducer failed on the pinned buggy base with the expected `(100, 2)` JAX PRNG-key shape error and passed on the exact fixed merge (`1 passed in 3.00s`).

### Remaining candidate-specific gates

1. Project-lead source-aware gold, alternatives and E1/E2/E3 decision.
2. Bounded documentary dependency/license scope acknowledgement, including the NumPy/OpenBLAS/LAPACK/GCC-runtime notices; this is not legal clearance.
3. Explicit candidate-specific prior pipeline/debug exposure declaration. The value must be truthful; the v0.2 eligibility rule requires `none`.
4. Complete case-acceptance record, fail-closed schema/registry validation, and a separate final project-lead YES/NO.

The current proposed packet-set structural pass does not establish semantic sufficiency. No model weights have been loaded; inference, fine-tuning and training remain unauthorized.
