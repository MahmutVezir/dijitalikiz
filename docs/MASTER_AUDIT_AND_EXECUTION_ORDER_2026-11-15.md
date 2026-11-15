# Master audit and corrected execution order — 15 November 2026

**Purpose:** Consolidate the evidence-abstention project's conversation history and current repository evidence into one operational source of truth. This document supersedes conflicting status summaries; it does not authorize inference.

## Executive status

- Research question: on the same frozen model and same software-defect evidence packet, does a policy that may abstain when evidence is insufficient (P1) reduce unsupported definitive diagnoses on E3 compared with a policy required to diagnose (P0), without unacceptable loss of answer coverage on E1?
- Current dataset route: SWE-rebench V2 Filtered-Verified, pinned Parquet revision `fb9aa226b2ce37c708ea7732e7b980abacdadb67`, SHA-256 `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.
- Current candidate cohort: 96 primary project candidates, plus 17 declared project reserves and 148 within-project alternates. These are candidate metadata, not accepted cases.
- Accepted confirmatory cases/projects: **0 / 0**.
- Confirmatory model outputs: **0**. Model load, inference and fine-tuning have not been performed.
- Dataset validation gate: **OPEN**. Inference authorization: **false**.
- The V2-specific no-inference readiness report (run 43746329888) records **24 blockers**. The generic legacy Stage 3 preflight's 21-blocker report is not the authoritative V2 gate.
- Confirmatory minimum is **60 cases from 60 distinct independent upstream projects**, target 80. This is the current V2 manifest/analysis-plan design. Older documents saying 8 projects are superseded and must not be used for V2.

## 1. Reconstructed project chronology

### 4 October — repository and initial data scaffolding
- Repository `dijitalikiz` began with a mock-only pipeline, one synthetic Supabase RLS case and 14 tests.
- Collection schema/docs/folders were added; 21 tests passed.
- Five Commons Math/Defects4J candidates were listed (MATH-988, 927, 950, 938, 949), but each remained unverified and not started. No accepted case existed.
- These were early scaffolding/candidates, not experimental observations.

### 9–15 October — historical CCDG research line
- An earlier study investigated structured cross-component dependency representation (CCDG), not the current abstention hypothesis.
- It had a 40-case pilot and a 160-output validation artifact. The literal-alias comparison yielded 0/80 versus 0/80 and McNemar p=1.00; the evaluation also exposed an information-parity flaw (the Standard condition explicitly contained error information in 16/16 cases while CCDG did not).
- Prompt/scorer schema mismatch and semantic leakage issues undermined interpretation. Human scores were not available.
- This line is historical engineering/research context only. Its data, outputs and claims are not evidence for the current SWE-rebench V2 P0/P1 study.

### 21–24 October — first abstention design on BugsInPy
- The project focus changed to evidence-aware abstention. The initial source route was BugsInPy: 501 raw cases across 17 projects, approximately 500 metadata records complete, with one malformed buggy/fixed commit identity.
- At the time, accepted confirmatory cases remained 0. A `tqdm-1` base-fail/fix-pass smoke/reproduction was excluded due to prior exposure and environment/reproducibility concerns; it must not be counted as confirmatory.
- V10/V11/V12 candidate queues, 93/105-ID exposure lists, Stage 3 manifests, Kaggle notebooks, confidence/entropy prototypes and many CI tests were developed. They are not all one dataset/protocol version.
- The old BugsInPy Stage 3 manifest and the separate five-case entropy prototype are not the current SWE-rebench V2 study. Preserve them historically; do not silently merge their IDs, hashes, outputs or readiness counts into V2.
- Passing software tests (including 59- and 265-test milestones) verified software contracts only; they did not establish human calibration, dataset validity or the research hypothesis.

### 12 November — source-route pivot to SWE-rebench V2
- The current route was selected and pinned: 6,272 Parquet rows; metadata screening produced a 96-project primary candidate cohort, 17 project reserves and 148 within-project alternates.
- Candidate selection was frozen by CSV/manifest hashes. The 96 rows were statically reviewed in batches. Static review is not case acceptance.
- Exact PR/base identities and root-license checks were completed for audited batches, but per-file/nested license provenance, target-test reproduction and human review remain case-specific.
- The dataset card's CC-BY-4.0 declaration does not relicense the upstream source code. Every selected repository and used file needs its own provenance/license review.
- The current V2 registry is deliberately empty. This is correct and must not be “fixed” by filling it with unverified candidates.

### 14–15 November — current technical evidence
- Static candidate screening reached rows 1–96. Row 90 (pyfar #721 / PR #722) is a strong static candidate; its exact base/fix and test oracle have been reviewed, but no upstream target test has been run.
- Robocop #1371 (row 24) passed a controlled base-fail/fix-pass technical reproduction. pdoc #812 / PR #813 (row 95) also passed a controlled real-CLI base-fail/fix-pass reproduction. Both are excluded from confirmatory sampling under the predeclared source-exposure/debugging rule. They are technical feasibility evidence only.
- PR #206 merged the E1 coverage non-inferiority guardrail proposal. Its 10-percentage-point margin and paired bootstrap are provisional and require independent mentor/Panel B approval before preregistration.
- PR #207 merged a no-network integrity auditor for the committed timestamp register. It verifies internal CSV consistency only; it does not authenticate original API payloads.
- The expanded timestamp register now contains 113 rows: all 96 primary candidates and all 17 declared reserves. All 113 upstream GitHub records were re-fetched successfully; 112 dataset timestamps match exactly and one (`simpeg/simpeg#1633`) differs by one second. This is field-level normalized API evidence, not raw-payload cryptographic authentication. See `SWE_REBENCH_V2_FULL_TIMESTAMP_RECONCILIATION_2026-11-15.md`.
- PR #202 is still open and not mergeable. Its own timestamp workflow explicitly states that the cross-repository GitHub API reconciliation was **not executed** in that workflow. Do not call that workflow a completed API audit or merge the branch wholesale.
- Main commit `35b3da29e82c9020159b29369ada15b41620174c` has Research Validation run 43746393823: repository/configuration validation passed (**418 tests + 56 subtests**); the separate historical archive job failed because `data/historical/confirmatory_artifact_2026-10-09.zip` is not in the canonical repository. The archive is an old CCDG record, not current V2 data.
- Vercel status failures on recent PRs point to a build-rate limit; they are not Python research-test failures.

## 2. Correct / incorrect / incomplete work ledger

| Item | Verified status | Correct interpretation / action |
|---|---|---|
| 96-row V2 cohort | Frozen metadata candidate list | Do not call it 96 validated defects or 96 accepted cases |
| Static candidate audits | Rows 1–96 screened | Useful triage; not technical reproduction or semantic adjudication |
| Robocop and pdoc reproductions | Base-fail/fix-pass technically reproduced | Exclude from confirmatory sample due exposure; do not report as P0/P1 results |
| pyfar row 90 | Strong static candidate only | Next candidate for careful pre-reproduction provenance/test-oracle review; no test yet |
| Timestamp CSV register | 113 rows, 112 exact, one +1 second; all 17 reserves present | All rows re-fetched through GitHub connector; raw API payload provenance not authenticated; simpeg exception unresolved |
| PR #202 timestamp workflow | Synthetic/parser tests and exact Parquet snapshot passed; cross-repository API query explicitly not run | Do not describe as full timestamp audit; branch not mergeable |
| PR #206 E1 guardrail | Merged; implementation and tests exist | Provisional method; mentor/Panel B approval still required |
| PR #207 timestamp register audit | Merged; no-network audit added | Does not close dataset gate |
| CI test totals | 418 tests + 56 subtests passed in repository/configuration job | Software quality evidence only; not scientific validation |
| Overall Research Validation | Failure due separate historical archive presence check | Do not mislabel the repository/configuration test job as failed; recover/commit the archive or isolate that historical gate without weakening integrity checks |
| Generic Stage 3 preflight | 21 blockers; includes an 8-project minimum | Legacy BugsInPy/Stage 3 logic; not V2 source of truth |
| V2-specific preflight | 24 blockers; minimum 60 distinct projects | Authoritative current readiness report |
| Model license/runtime | Qwen revision recorded; exact license assessment and no-output runtime verification pending | No model load or inference until approved |
| Human review | Panel A/Panel B, calibration and consent pending | Must be performed by independent people; AI cannot substitute |
| Historical CCDG / BugsInPy / entropy prototype | Earlier independent tracks | Preserve, do not merge into current confirmatory data |

## 3. Resolve the design contradictions before execution

1. **Independent-project threshold:** V2 manifest and analysis plan require 60 cases from 60 distinct upstream projects (target 80). Older roadmap/preflight text saying 8 projects belongs to the earlier Stage 3 route. Update or label those legacy references; never lower the V2 threshold to 8.
2. **Timestamp provenance:** the 113-row register now covers all 96 primary candidates and all 17 declared project reserves, and every upstream GitHub record was re-fetched. This is normalized field-level evidence, not raw-response authentication. The one-second case must be handled under a written, pre-outcome rule; do not infer dataset timestamp-generation semantics without authoritative documentation.
3. **Exposure:** any candidate opened for target-test debugging or technical reproduction is excluded from confirmatory sampling under the current exposure rule. Robocop and pdoc remain excluded.
4. **Licensing:** dataset-card license and upstream-code license are separate. No code/fixture should be redistributed without exact-base, changed-file and nested provenance review.
5. **Human independence:** Panel A and Panel B must be disjoint, each with at least two reviewers; Panel B must be blinded to identity, patch, gold cause, evidence tier and policy until independent ratings are locked. The adjudicator preserves original ratings.
6. **Model claim:** the study measures behavior under an evidence packet and response policy. It does not prove internal model self-awareness or access to a literal “knows/doesn't know” state.
7. **Power:** N=60/80 are feasibility thresholds, not power guarantees. Current sensitivity scenarios show that plausible weaker effects may be substantially underpowered. Freeze the target only after a defensible prospective justification, never after seeing outcomes.

## 4. One execution sequence — no parallel redesign loops

| Order | Work package | Exact exit evidence | Owner type |
|---:|---|---|---|
| 0 | Consolidate version control | One V2 manifest/registry/preflight; mark BugsInPy Stage 3 and entropy track as legacy; remove stale 8-project references from active V2 status | Repository maintainer |
| 1 | Close V2 source/time metadata | 113/113 upstream timestamp re-fetch complete (96 primary + 17 reserves); document simpeg precision exception, raw API provenance limits and source/license provenance; immutable report and hashes | Automated audit + independent review |
| 2 | Select one untouched candidate | Static scope, exact base/fix SHA, linked issue, changed-file map, no prior exposure, no duplicate/fork/shared upstream | Source-exposed reviewer |
| 3 | Complete license/provenance | Exact-base and fix license texts, per-changed-file provenance, NOTICE/nested dependency review, permitted evidence-packet extraction | Source-exposed reviewer |
| 4 | Freeze technical reproduction plan | One issue-specific failing test, expected base failure and fixed pass, exact environment and commands specified before running | Technical reviewer |
| 5 | Reproduce candidate | Same target test fails for defect-specific reason at base and passes at exact fix; logs, source hashes, runtime hashes saved | Source-exposed operator |
| 6 | Build evidence packets | E1/E2/E3 packets from the same case; remove root-cause/patch leakage; blinded semantic sufficiency review | Panel B |
| 7 | Establish gold and independence | Panel A verifies defect/root cause/test relationship and project independence; at least two independent ratings; adjudication if needed | Panel A + auditor |
| 8 | Accumulate confirmatory cases | At least 60 accepted cases from 60 distinct projects; target 80. No exposure-contaminated cases; do not lower threshold | Independent panels + auditor |
| 9 | Approve and preregister | Freeze prompt, schema, model/tokenizer/runtime, generation settings, rubrics, exclusions, analysis code, hashes and E1 guardrail; external verifiable preregistration URI | Mentor + Panel B + project lead |
| 10 | No-output model/runtime check | Exact pinned model and tokenizer load; record software/hardware/dtype/fingerprint; no generation | Technical operator |
| 11 | Explicit inference authorization | Every data, license, human, preregistration, hash and runtime gate passes; explicit manifest/gate authorization | Project lead + mentor |
| 12 | Confirmatory run | Six conditions per case; N=60 → 360 raw outputs, N=80 → 480; deterministic generation, no retries/JSON repair; every raw output/hash retained | Runner |
| 13 | Blind scoring and analysis | Two independent Panel B ratings per response; adjudication; agreement; exact McNemar, risk difference, CI; E1 coverage guardrail; invalid-output sensitivity | Blinded reviewers + analyst |
| 14 | Robustness and report | Project-level/leave-one-project-out sensitivity, contamination and limitations, reproducibility package, TÜBİTAK report | Analyst + project lead |

**Do not start work package 11 while any prior gate is open.** A code test passing never authorizes inference.

## 5. Immediate next actions

1. Correct the active V2 status surface so it reports the V2-specific 24-blocker result and 60-distinct-project threshold; clearly label the 21-blocker/8-project report as legacy Stage 3.
2. Stop treating PR #202 as complete. Extract and review its API-audit implementation separately; the workflow evidence proves it did not execute the cross-repository API call.
3. Audit pyfar row 90's exact-base and changed-file/nested provenance and test oracle before any upstream test. Keep it unaccepted until the technical plan is frozen and independent.
4. Repair the historical archive repository copy as a separate maintenance task; it is not a V2 dataset blocker and must not distract from case validation.
5. Do not load Qwen, run inference, fine-tune, or populate the registry until the explicit gates pass.

## 6. Non-negotiable reporting language

Use these labels precisely:
- `STATIC_CANDIDATE`: issue/PR/patch metadata reviewed only.
- `TECHNICAL_REPRODUCTION_PASS`: exact base fails and exact fix passes under the same frozen test/runtime.
- `HUMAN_ADJUDICATION_PASS`: independent Panel A/Panel B criteria and audit records complete.
- `ACCEPTED_CONFIRMATORY_CASE`: every acceptance and exposure criterion passes and registry evidence is independently audited.
- `MODEL_OUTPUT`: raw output from an authorized confirmatory run only.

Never turn test counts, metadata rows, technical reproductions, exploratory artifacts or AI-generated reviews into accepted cases or hypothesis results.

## Source records

- Main commit audited: `35b3da29e82c9020159b29369ada15b41620174c`.
- V2 manifest: `research_candidates/evidence_abstention/SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json`.
- V2 registry: `research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_REGISTRY_V0_1.json`.
- V2 analysis plan: `research_candidates/evidence_abstention/SWE_REBENCH_V2_ANALYSIS_PLAN_V0_1.md`.
- V2-specific preflight: Actions run `43746329888`.
- Research Validation: Actions run `43746393823`.
- PR #202: https://github.com/MahmutVezir/dijitalikiz/pull/202 (open, unmergeable; API reconciliation not executed by its named workflow).
- PR #206: https://github.com/MahmutVezir/dijitalikiz/pull/206 (merged).
- PR #207: https://github.com/MahmutVezir/dijitalikiz/pull/207 (merged).
