# Dishka #435 — case-acceptance readiness audit

**Prepared:** 2026-11-18  
**Candidate:** `reagento__dishka-436`  
**Status:** Technically reproduced; human gold/tier and study-limitations approvals recorded; **not accepted**.  
**Accepted-case registry:** remains 0.  
**Model loading/inference/training:** not performed and not authorized.

This is a readiness record, not a case-acceptance record. It deliberately does not insert the candidate into the v0.2 registry or represent pending human decisions as completed.

## 1. Dataset identity and provenance

- Dataset: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Instance: `reagento__dishka-436`
- Cohort role/rank: primary / rank 2
- Canonical full-row SHA-256: `c548969ec886af21b56c93daae34db1a86b3a10c8dd1473d3d5c886549a9e86d`
- Dataset row timestamp: `2025-04-15T22:52:26Z`
- Dataset source resource: PR #436, created `2025-04-15T22:52:26Z` — exact timestamp match.
- Separate defect issue #435 was created `2025-04-14T17:22:16Z`; it is the defect narrative, not the timestamp source for this PR-derived dataset row.
- The historical timestamp register's `is_pull_request=false` value conflicts with the `/pull/436` URL. The resource-type and timestamp discrepancy is recorded, not silently rewritten, in `REAGENTO_DISHKA_436_RESOURCE_TYPE_RECONCILIATION_2026-11-16.md` and `reproduction/dishka_issue_435/DISHKA_435_POST_RUN_PROVENANCE_CORRECTION_V0_1_2026-11-16.md`.
- The row timestamp was reconciled against the PR resource; the project-wide raw-payload provenance gate remains open. Do not represent the global dataset provenance gate as closed.

## 2. Source identity and independence

- Canonical upstream: `reagento/dishka`; GitHub reports it is not a fork.
- Dataset-linked source: https://github.com/reagento/dishka/pull/436
- Linked defect report: https://github.com/reagento/dishka/issues/435
- Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
- Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`
- Changed paths:
  - `src/dishka/registry_builder.py`
  - `tests/unit/container/override/test_alias.py`
  - `tests/unit/container/override/test_context_var.py`
  - `tests/unit/container/override/test_provide.py`
  - `tests/unit/container/test_context_vars.py`
- Related-issue screen: #151, #275, #16, #420, and #466. The review found no duplicate report of the same defect contract.
- One case maximum applies to `reagento/dishka`; no second Dishka row may be counted as an independent project.

## 3. Technical reproduction — independently rechecked

Latest completed repeat:
- Workflow run: `44111403900`
- Job: `134137813966`
- Artifact: `14340572651`, `dishka-issue-435-reproduction-44111403900-1`
- Downloaded archive SHA-256: `183b8c62af381d012234f2f5cee6e9d40e70c4f8cdcb6b21f10e79f0425921f0`
- ZIP size: 226,404,514 bytes; 33 members; ZIP CRC check passed.
- `SHA256SUMS.txt`: all 32 listed entries independently recalculated and passed.
- Runtime: Ubuntu 22.04.5 LTS, CPython 3.11.9.
- Issue reproducer selector: `test_issue_435_override_lower_scope` in `test_issue_435.py`.
  - Buggy base: one test fails with `AssertionError: 1 != 42`.
  - Fixed revision: same test passes.
- All eight frozen dataset FAIL_TO_PASS selectors:
  - Buggy base: all eight fail with defect-related assertions/errors.
  - Fixed revision: all eight pass (`8 passed in 0.06s`).
- Reproduction environment-lock SHA-256: `2900c96dc32539abdb34b89a3a8444277cb03ec6f5455c3c7d861b12d8e94dab`.
- Dataset-test lock SHA-256: `86df530333234a4da0407f344d39b7851aac892fd9ad485a5c1ed7b9d8870d5d`.
- No model was loaded; no inference, fine-tuning, or training was performed.

The independently reproduced failure mechanism is a stale per-scope factory registration. The fixed builder delays registry population until provider processing is complete and uses the final processed-factory map.

## 4. Human technical adjudication already recorded

The project lead explicitly approved on 2026-11-16:
- Gold mechanism `G1_STALE_PER_SCOPE_FACTORY_REGISTRATION`.
- Alternatives `A1_SCOPE_CHAIN_PRECEDENCE` and `A2_CONSUMER_BINDING_OR_CACHE`.
- E3 survivors: G1, A1, A2.
- E2 survivors: G1, A1.
- E1 survivor: G1 only.
- The stated E3 → E2 → E1 evidence-to-mechanism rationale.

The project lead explicitly acknowledged on 2026-11-17:
- Full source-level researcher exposure to the issue/fix materials already reviewed.
- One human adjudicator (the student project lead); ChatGPT is advisory AI input only.
- No human-human inter-rater reliability or Cohen's kappa claim.
- Exploratory feasibility use only, not confirmatory efficacy evidence.

The decision record is `reproduction/dishka_issue_435/HUMAN_ADJUDICATION_DECISION_DISHKA_435_V0_1_DRAFT_2026-11-16.md`. These approvals do **not** constitute final case acceptance.

## 5. E1/E2/E3 packet evidence

The packet index records the following immutable manifest digests and membership:
| Tier | Manifest SHA-256 | Evidence items | Approved surviving mechanisms |
|---|---|---:|---|
| E3 | `d75d32da95bfdef73d3824677b6d6df445712967a777580b8867e769c133f131` | 7 | G1, A1, A2 |
| E2 | `8a39ab862393954451f403badd5ccea40350902b39f95ae4e0d7885e9d6751d5` | 9 | G1, A1 |
| E1 | `0fc59ca0ff6cf220b6b46784329b21cdd9d16af3f2211dd29210dd1031f94462` | 13 | G1 |

E2 inherits E3 evidence unchanged; E1 inherits E2 evidence unchanged. The raw reproduction archive and each of its internal files have passed the independent checks above. Packet-manifest presence and structural nesting do not replace the semantic approval already made by the project lead.

## 6. License-screen boundary — sign-off still required

Recorded exact-base evidence:
- Root `LICENSE`: Apache-2.0; exact-base Git blob SHA-1 `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`.
- Exact-base `pyproject.toml` declares Apache-2.0.
- Changed production and test files are documented as inheriting the repository Apache-2.0 license.
- Minimal issue reproducer: Python 3.11.9, stdlib `unittest`, direct source import, no pip-installed dependencies.
- Dataset-selector environment: pinned `pytest==8.3.5`, `iniconfig==2.0.0`, `packaging==24.2`, `pluggy==1.5.0`.
- Dataset extraction environment: pinned PyArrow 19.0.1, separate from upstream-code execution.
- License manifest SHA-256: `34e09fdcf5d33849659490e2e50cdf80c8c5c8e6f01108dd542c60de203cf360`.

The recorded documentary conclusion is limited to the exact source files and the specified reproduction/test/extraction environments. It is **not** legal advice, a legal opinion, blanket clearance for optional dependencies, or blanket authorization to redistribute third-party source or dependencies. The project lead's explicit sign-off of this limited scope remains open. Until then, the acceptance record must not set the license-review fields to `passed`.

## 7. Exposure distinction

The study protocol excludes a candidate used **before prospective case validation** for runner/pipeline debugging, target-test-oracle troubleshooting, or prompt calibration. It distinguishes that exclusion from a planned technical reproduction performed under the prospective validation procedure.

Project records identify Robocop #1371 and pdoc #812 as earlier pipeline/debug-exposed exclusions. Dishka #435 is not listed among those excluded candidates; its recorded reproducer and frozen selectors are prospective case-validation runs. The researcher’s full source exposure is a separate, already acknowledged limitation and must remain disclosed.

**Proposed record classification:** `prior_pipeline_debug_exposure = none`, `researcher_source_exposure = full`.  
**Required before acceptance:** project-lead confirmation that Dishka was not used for earlier runner/pipeline debugging or test-oracle troubleshooting before its prospective validation assignment. If that classification is not `none`, the active v0.2 validator permanently excludes this candidate; the validator must not be weakened to admit it.

## 8. Remaining case-level gates

1. Project-lead confirmation of the prior pipeline/debug exposure classification.
2. Project-lead sign-off of the bounded documentary license-screen scope above.
3. Build the Draft 2020-12 schema-conformant acceptance record using verified artifact URIs and SHA-256 values; do not set `acceptance_decision = accepted` while either sign-off is open.
4. Run the active v0.2 case validator and fail-closed registry validator on that record.
5. Obtain the separate, explicit final case-acceptance decision before adding the record to the registry.

## 9. Project-wide execution gate remains blocked

The latest completed no-inference readiness run inspected in this audit is `44318994967`, job `134852608128`, artifact `14434555521`. It completed all four test groups (12 + 24 + 6 + 15 = 57 tests passed), but its report was `blocked_before_inference`, with 11 blockers, 0 accepted cases, and `ready_for_inference=false`.

The blockers include the global dataset/raw-payload provenance gate, upstream source/license audit, exact Qwen revision license/use review, model/tokenizer/runtime verification, generation-setting freeze, internal protocol/analysis/scoring hash freeze, and the absence of at least one fully accepted case. Accepting Dishka would not, by itself, close those global gates or authorize inference.

A fresh no-inference preflight was triggered on the subsequent PR head and was queued at the time of this record. Its result must be inspected before reporting a newer readiness state.

**Final disposition:** Dishka is a strong, technically reproduced exploratory candidate with approved gold/tier decisions, but it is **not accepted**. Global accepted-case count remains 0. No model loading, inference, fine-tuning, or training is authorized.


## 10. Latest project-wide no-inference gate recheck (2026-11-18)

The updated PR head was audited again by workflow run `44321922276`, job `134862837135`, artifact `14434269076` (`evidence-abstention-preflight-logs-44321922276-1`). The downloaded ZIP SHA-256 is `f4c32af4f87c08c8001a850e876f0a77babda9796b7f083525c99d45b6aa0a26`; archive CRC passed; five files are present.

All 57 tests passed: 12 packet-audit, 24 operational-packet/triage, 6 selector-runner, and 15 v0.2 acceptance/preflight tests. The resulting report nevertheless remains `blocked_before_inference`, `ready_for_inference=false`, with 11 blockers and 0 accepted cases/projects. It confirms a valid empty registry and a valid acceptance schema, not an accepted case. The blocker list is unchanged from section 9; no inference, fine-tuning, or training was performed.

This run supersedes section 9's earlier completed preflight reference. The separate workflow fan-out for candidate reproductions continued independently; those results must be assessed and recorded per candidate rather than counted from job completion alone.


## 11. Latest Dishka reproduction repeat and project preflight (2026-11-18)

The most recent Dishka repeat on this branch completed successfully:
- Run `44322262968`, job `134864350055`, artifact `14436220610` (`dishka-issue-435-reproduction-44322262968-1`).
- Downloaded ZIP SHA-256: `c40178034053a7d2f3eead80cb8dc22027578767406384711d54e670d9234a5a`; archive size 54,107,858 bytes; 33 members; CRC PASS; **32/32** internal SHA256SUMS entries passed.
- Issue reproducer: buggy base `AssertionError: 1 != 42`; fixed revision PASS.
- Frozen dataset selectors: **8/8 fail** on the buggy base and **8/8 pass** on the fixed revision (`8 passed in 0.07s`).
- This is another technical replication only; it does not constitute final case acceptance or close the limited license/exposure gates.

The same PR-head no-inference preflight run `44322262968`, job `134864024369`, artifact `14434582787`, was downloaded and checked. ZIP SHA-256: `529b14f588d7850930aa94dc49b0b1caa1f05d56919f8e3b5f4b6d324b27e4e7`; CRC PASS; five members. The report remains `blocked_before_inference`, `ready_for_inference=false`, with 11 blockers, 0 accepted cases/projects, and no model loading/inference/fine-tuning. All 57 preflight tests passed (12 + 24 + 6 + 15).
