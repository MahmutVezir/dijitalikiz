# Single-human research and evaluation amendment — v0.2

**Date:** 21 November 2026  
**Scope:** Active SWE-rebench V2 evidence-abstention exploratory/feasibility study  
**Status:** Project-lead instruction recorded; prospective governance amendment. No model loading, inference, scoring, case acceptance or training is authorized by this document.

## 1. Actual team composition

The project has one human participant: the student project lead. The student project lead is the sole human researcher, technical adjudicator, evidence-tier decision-maker, output scorer and final decision-maker.

ChatGPT is an AI research assistant only. It may help inspect source material, check consistency, identify alternative explanations and provide separately labelled advisory critiques. It is not a human participant, co-investigator, independent reviewer, external auditor, legal reviewer, second rater or source of human consensus.

There is no Rater B, no technical-review panel and no independent human reviewer in this project. No peer concurrence, external review or independent legal sign-off is claimed. Previous drafts that described a second human evaluator are superseded for the active v0.2 study and retained only as historical records.

## 2. Single-human technical adjudication

The project lead alone:
- authenticates candidate identity, issue/PR scope and exact frozen-row evidence;
- identifies the technical gold mechanism and predeclares plausible alternatives;
- decides whether E3, E2 and E1 support ABSTAIN or ANSWER;
- records full source exposure separately from prior pipeline/debug exposure;
- approves or rejects each case for the exploratory registry;
- interprets outputs and reports deviations.

Each decision must have an evidence-to-claim rationale, source links, immutable identifiers and hashes where applicable. For difficult decisions, the research log should include a deliberate counter-hypothesis check: state the strongest alternative, what evidence supports it, and exactly which observation eliminates or retains it.

ChatGPT's critique is stored separately and is never counted as a second human vote. The human's decision and rationale remain authoritative; disagreement with the AI critique is preserved rather than hidden.

## 3. Single-human output scoring procedure

One human scorer (the project lead) scores each raw model response using the frozen v0.2 evidence-support rubric. The unit is one response in one case × evidence tier × policy cell.

To reduce avoidable expectation effects without overstating blindness:
1. A data-preparation step assigns randomized response IDs and randomizes scoring order.
2. During evidence-support scoring, the scorer is not shown the P0/P1 policy label, prompt metadata that directly reveals policy, the paired response from the other policy, or policy-level aggregate results.
3. Each response is scored separately against only the evidence packet visible to the model in that cell.
4. The scorer records the evidence-support category, rationale with evidence IDs, assertion/abstention status, leakage, ambiguity, validity and compliance flags.
5. The original rating is timestamped and hash-locked before opening or consulting the separate gold adjudication record for that scoring event.
6. Gold correctness is recorded separately after evidence-support scoring is locked. A correct hidden-gold guess must remain unsupported when the visible packet does not support the asserted mechanism.
7. The AI critique, if used, is recorded separately after the human's original score is locked. It cannot silently overwrite the original human rating.

## 4. Blinding and exposure limitations

This is **condition-masked single-human scoring, not blinded human scoring**.

The project lead has full disclosed exposure to the upstream issue, PR, source, patch, gold mechanism and evidence-tier decisions. The same person also prepares the case and scores the model outputs. Therefore:
- do not claim blinding to case identity, source, hidden gold, patch or evidence tier;
- do not claim an independent human score, independent adjudication, inter-rater reliability or Cohen's kappa;
- do not present the AI critique as independent human validation;
- explicitly disclose common-method, expectancy and researcher-exposure risks in the report.

Masking P0/P1 labels, paired outputs and aggregate results is a bias-reduction control only. It cannot remove the researcher's prior knowledge or guarantee that policy condition will not be inferred from response wording.

## 5. Reliability and reporting

There is one human rating per raw response. Consequently, no human-human agreement statistic is defined or calculable. Do not compute Cohen's kappa or a two-rater confusion matrix from human-plus-AI labels.

Report:
- the single-rater procedure and scoring order;
- the project lead's full source exposure;
- whether policy labels and paired responses were masked during initial scoring;
- raw output and packet hashes, scorer ID, timestamp and score rationale;
- ambiguity, invalid/unscorable and deviation counts;
- the lack of independent human replication as a central limitation.

An intra-rater repeatability check may be added only by a prospective dated amendment before outcome-pattern inspection. It would be a consistency diagnostic for the same person, not inter-rater reliability or independent validation.

## 6. Candidate eligibility and independence remain unchanged

This amendment does not relax:
- one case per distinct upstream project;
- exact frozen-row and source identity checks;
- issue/patch/test scope alignment;
- exact buggy-base fail / fixed-revision pass reproduction;
- at least two plausible, testable alternative mechanisms;
- nested E3/E2/E1 packet requirements;
- source/dependency provenance and attribution review;
- the exclusion for candidate-specific prior pipeline debugging, test-oracle troubleshooting or prompt calibration.

Full researcher source exposure must not be relabelled as no exposure. The existing truthful declaration of prior pipeline/debug exposure remains a separate field and is not changed by this amendment.

## 7. Supersession and active artifacts

This amendment supersedes the dual-human working arrangement described in:
- \`HUMAN_EVALUATOR_AMENDMENT_V0_1_2026-11-18.md\`;
- \`SWE_REBENCH_V2_DUAL_HUMAN_OUTPUT_SCORING_RUBRIC_V0_1_DRAFT_2026-11-18.md\`.

Those files remain in the repository as historical evidence of the earlier proposed design. They are not active procedures and must not be used to claim a second rater exists.

The active output-scoring rubric is:
\`SWE_REBENCH_V2_SINGLE_HUMAN_OUTPUT_SCORING_RUBRIC_V0_2_2026-11-21.md\`.

The active study protocol and analysis plan must be updated to cite this amendment and rubric. A CI test must enforce the single-human role contract and reject reintroduction of a fictitious second rater or panel.

## 8. Scientific boundaries

The study remains exploratory/feasibility, single-model and small-sample. A single-human scoring procedure reduces the strength of measurement-reliability claims; it does not invalidate a transparently reported exploratory case-level study, but it materially limits the conclusions.

No case acceptance, model execution authorization, preregistration, fine-tuning or training follows from this amendment. All global dataset, model-license, runtime, provenance and execution blockers remain independently active.
