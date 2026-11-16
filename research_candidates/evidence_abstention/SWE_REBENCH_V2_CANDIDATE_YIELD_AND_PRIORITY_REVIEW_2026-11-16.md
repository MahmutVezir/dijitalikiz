# v0.2 candidate yield and technical-review priority — 16 November 2026

## Purpose

This note assesses whether the selected v0.2 exploratory design can realistically reach 15 accepted cases from distinct upstream projects. It does not change the frozen cohort, acceptance criteria, or sample-size thresholds.

## The count target is project-level

- Feasibility floor: **15 accepted cases from 15 distinct upstream projects**.
- Target: **20 accepted cases from 20 distinct upstream projects**.
- One case per canonical upstream project. A second issue from the same repository is a replacement candidate, not an additional independent case.
- Six condition cells per accepted case produce 90 planned raw outputs at 15 cases and 120 at 20 cases. These are planned counts only.

The frozen metadata selection contains 96 primary candidates from 96 distinct repositories, plus 17 project-level reserves from 17 additional repositories. It also contains 148 within-project alternatives across 53 repositories; those alternatives can replace a rejected issue in an already represented project, but they do **not** increase the number of independent projects. Thus the pre-review frame contains 113 distinct project candidates, not 261 independent projects.

## Static scope-screen yield

The 12 existing scope-audit batches classify the 96 primary rows as follows. Counts below include provisional, conditional, and explicitly held defect-shaped candidates; they are not accepted cases.

| Cohort rows | Candidate / conditional / hold count | Audit interpretation |
|---|---:|---|
| 1–8 | 4 | Provisional |
| 9–16 | 4 | Provisional |
| 17–24 | 5 | 4 provisional + 1 conditional |
| 25–32 | 5 | Provisional |
| 33–40 | 6 | Provisional |
| 41–48 | 6 | Provisional |
| 49–56 | 7 | Provisional, including issue/patch alignment caveat |
| 57–64 | 6 | 5 defect candidates + 1 repository/base/license hold |
| 65–72 | 7 | 5 defect candidates + 1 conditional + 1 scope hold |
| 73–80 | 4 | 2 strong + 1 additional + 1 conditional |
| 81–88 | 6 | 3 strong + 3 conditional |
| 89–96 | 7 | 3 strong + 4 conditional |
| **Total** | **67** | Broad static shortlist only |

A second-pass review has already removed SimPEG row 63 from the primary shortlist: the linked issue describes an ambiguous API/docstring mismatch, while PR #1633 deprecates the property rather than implementing the issue's proposed integer result. This leaves **66 rows** in the current broad candidate/conditional/hold planning shortlist. The normalized row-level ledger has now been generated at `SWE_REBENCH_V2_COHORT_96_STATIC_TRIAGE_LEDGER_V0_1_2026-11-16.json`: 96/96 ranks appear exactly once. It records 29 excluded, 49 provisional, 10 conditional, 2 held, and 6 explicitly strong rows. The ledger is a deterministic extraction of the existing audit decisions, not a new adjudication; human review is still required before treating 66 as a final cohort statistic.

## Is 15 achievable?

At face value:
- 15 accepted cases require 15.6% of the 96 primary rows, or 22.7% of the current 66-row broad shortlist.
- 20 accepted cases require 20.8% of the 96 primary rows, or 30.3% of the current 66-row broad shortlist.

These percentages are arithmetic feasibility thresholds, **not empirical pass-rate estimates**. The 66-row shortlist contains conditional and held candidates, and every candidate can still fail technical reproduction, exact-base provenance, license/dependency review, independence/exposure, gold adjudication, or E1/E2/E3 construction. No historical conversion rate is available yet. Therefore 15 is plausible enough to pursue, but not guaranteed; 20 is a stretch target.

If primary candidates fail, the preselected 17 distinct-project reserves can be screened under the same rules. Within-project alternatives can replace an issue only when they do not create duplicate/related defects and do not change the one-project-one-case rule. No new candidate may be added merely because the observed count is low; any expansion beyond the frozen 113-project frame requires a documented sampling-frame amendment before outcomes are seen.

## Second-pass findings and current priority

### SimPEG row 63 — exclude from the strict shortlist

- Cohort instance: `simpeg__simpeg-1633`
- PR: https://github.com/simpeg/simpeg/pull/1633
- Linked issue: https://github.com/simpeg/simpeg/issues/1609
- The issue reports that a survey `components` property disagrees with its docstring and returns the first receiver's components. It also acknowledges that the expected aggregate is undefined when receivers contain different components.
- The PR deprecates the property and adds tests for a `FutureWarning`; it does not make the property return the issue's suggested integer value.
- The timestamp discrepancy is reconciled against the PR endpoint, and the root MIT license was screened, but those facts do not repair the issue/patch oracle mismatch.

**Decision:** do not spend the first reproduction slot on this candidate. Retain the timestamp and license records for provenance; mark the case not accepted and excluded from the strict primary bug shortlist unless a narrower, independently justified test contract is later approved.

### pyfar row 90 — first technical candidate, pending dependency-license gate

- PR: https://github.com/pyfar/pyfar/pull/722
- Issue: https://github.com/pyfar/pyfar/issues/721
- Exact base: `648dda4c60c5a6f74acf335f7808c590c9d23929`
- Fixed revision: `a4d72d380bb8ddb0950d334eb1b0793ee6d86e0e`
- Exact-base root license: MIT.
- The issue provides numerical counterexamples: an energy reference of 20 produced output energy 0.05 rather than target 1. The patch uses square-root scaling for energy/power and adds parameterized tests over targets and channel-handling modes.
- The PR also removes the old energy/power expected-value rows from a previous parameterized test. The replacement test appears aligned with the intended target semantics, but the changed oracle must be independently checked before reproduction is considered decisive.

**Decision:** prioritize a frozen fail-to-pass reproduction dossier, but do not install or execute upstream code until the direct/transitive dependency license and changed-file/fixture provenance review is complete. This remains a candidate, not an accepted case.

### pdoc row 95 — hold for license clarification

- PR: https://github.com/mitmproxy/pdoc/pull/813
- Issue: https://github.com/mitmproxy/pdoc/issues/812
- Exact base: `57ee1d628027feffbd734180287e74294ddab7df`
- The exact-base `LICENSE` file contains standard MIT terms, while exact-base `pyproject.toml` declares `MIT-0`. This discrepancy must be clarified or resolved through authoritative upstream licensing evidence before execution or use.

**Decision:** do not select it as the immediate reproduction candidate while this license metadata conflict remains open.

## Required path from 0 to 15+

1. Normalize all 96 static decisions into one machine-readable row-level ledger, retaining excluded and conditional records.
2. Complete changed-file, fixture, root/nested NOTICE, and direct/transitive dependency provenance for the first small reproduction batch.
3. For each candidate that clears that gate, run the same frozen defect-specific test at the exact buggy base and exact fixed revision in an isolated, locked environment. Preserve raw logs, environment lock, commit IDs, and SHA-256.
4. Reject candidates that do not demonstrate the same test failing at base and passing at fix, or whose test oracle does not match the issue contract.
5. Review project lineage, forks/transfers, related issues, defect clusters, and previous researcher/pipeline/model exposure. Keep one accepted case per distinct upstream project.
6. Create the technical gold and blinded E1/E2/E3 evidence packets; the student researcher makes and records the human decision. ChatGPT provides separately logged advisory critique only.
7. Repeat through the primary list, then the 17 distinct-project reserves if needed. Report the actual funnel: screened → defect-shaped → license/provenance cleared → reproduced → independent/exposure cleared → gold/evidence accepted.

## Non-negotiable safeguards

- Do not lower the 15-project floor to force a result.
- Do not count multiple issues from one project as independent cases.
- Do not count the 148 within-project alternatives as extra independent projects.
- Do not accept a case on PR closure, a root LICENSE file alone, a CI pass, or structural JSON validation alone.
- Do not load the model or run inference until all case, protocol, scoring, analysis, license, runtime, and preregistration gates are closed and the separate inference authorization is recorded.

**Current accepted cases: 0. Current inference authorization: false.**
