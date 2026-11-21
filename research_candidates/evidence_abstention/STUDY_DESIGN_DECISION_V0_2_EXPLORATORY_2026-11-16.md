# Study design decision — v0.2 exploratory/feasibility
**Date:** 16 November 2026  
**Status:** Approved working direction by project lead; draft protocol only. Not preregistered. No case accepted. No model use authorized.

## 1. Decision recorded
The project lead selected:
  Study type: sequential exploratory/feasibility study; primary target 15 accepted cases, stretch target 20, and no eligibility floor beyond one valid case for a feasibility report.
- Model route: retain the pinned Qwen/Qwen2.5-3B-Instruct candidate, subject to exact-revision license and runtime review before loading or inference.
- Working team: project lead (student researcher), a second human output-rater candidate (public pseudonym: Rater B; participation and independence screening pending), and ChatGPT as an AI research assistant. ChatGPT is not a human co-investigator, human rater, legal reviewer, or external auditor.
- The project lead remains the sole project lead and final decision-maker. Rater B's proposed role is limited to independent, blinded scoring of raw model responses; Rater B is not automatically a gold-standard adjudicator or external auditor.

## 2. Research question
On the same frozen language model and same software-defect case, does allowing abstention when the visible evidence does not distinguish plausible causes (P1), compared with requiring a diagnosis (P0), change the rate of unsupported definitive root-cause claims in E3 evidence conditions, while preserving useful diagnosis behavior in E1?

The study distinguishes:
1. gold-root-cause correctness;
2. support from the evidence actually visible to the model;
3. whether the model abstains;
4. whether the response follows the assigned policy.

A correct guess is not automatically an evidence-supported diagnosis. The study does not measure or prove internal model self-awareness.

## 3. Sample and independence
- Primary target: 15 accepted cases from 15 distinct upstream projects.
- Stretch target: 20 accepted cases from 20 distinct upstream projects if more candidates pass the same unchanged gates.
- One valid case is sufficient for case-level feasibility. Fifteen is the primary target and preferred analysis threshold, not an eligibility floor.
- One case per upstream project. Forks, mirrors, transfers, duplicate issues, and shared upstream identities are grouped and cannot be counted as independent projects.
- If 15 qualifying independent projects cannot be obtained, retain every case that passes the unchanged acceptance criteria. Report the achieved N and its limits; do not duplicate projects to inflate N or relax acceptance criteria. With N=1–4, report case-level feasibility only; with N=5–14, report paired descriptive results without a hypothesis-test claim; with N=15–20, exploratory paired summaries and exact McNemar may be reported, still without confirmatory efficacy claims.
- The existing 96 primary rows and 17 project reserves are candidate metadata only. None is accepted by this decision.

The 20-case target is not a power guarantee. This is not a confirmatory efficacy trial and will not be described as one.

## 4. Conditions and planned outputs
Each accepted case contributes six cells:
- E1/P0, E1/P1
- E2/P0, E2/P1
- E3/P0, E3/P1

At one raw response per cell, 20 cases yield 120 outputs; 15 cases yield 90. Repeated generations do not increase the independent case count. No retry, JSON repair, or selective rerun is permitted in the primary dataset.

P0 requires a diagnosis. P1 permits explicit abstention when visible evidence does not distinguish the predeclared mechanisms. All other model, tokenizer, packet, output schema, generation, and runtime settings must be held constant.

## 5. Evidence-level method
For each case, prepare a predeclared set of at least three plausible causal mechanisms: one technically supported gold mechanism and at least two alternatives. Construct nested evidence packets:
- E3: none of the predeclared mechanisms is eliminated by the visible evidence;
- E2: at least one alternative is eliminated, while at least two mechanisms remain plausible;
- E1: only one mechanism remains, and it matches the independently documented technical gold.

The level is a semantic claim about discriminability, not packet length or number of files. The evidence IDs, source snapshots, and packet contents must be immutable and hash-recorded. A structural validator can verify IDs, nesting, and hashes; it cannot prove causal sufficiency.

E1/E2/E3 semantic tier decisions remain the project lead's judgments, supported by explicit evidence-to-mechanism rationales and a separately recorded advisory ChatGPT critique. Rater B will not see hidden gold, source code, patches, or tier labels before model-output scoring is locked; therefore Rater B is not a second human adjudicator of gold or tier sufficiency. Cases with unresolved tier ambiguity are excluded or reported as unclassified; they are not forced into a tier.

## 6. Scoring and analysis
Primary exploratory outcome: for E3, whether an asserted causal diagnosis is unsupported or contradicted by the visible packet. Partially supported is retained as a separate category and excluded from the strict primary binary endpoint. A valid abstention without diagnosis leakage is not an unsupported diagnosis. An asserted diagnosis is not considered supported merely because it matches the hidden gold cause.

Secondary descriptive outcomes:
- gold-root-cause correctness;
- evidence-support category;
- abstention and diagnosis coverage;
- P0/P1 policy compliance;
- citation validity;
- invalid output rate;
- usefulness of missing-evidence requests;
- E1 answer coverage and E2 behavior.

Report paired case-level counts, risk differences, uncertainty intervals, and exact McNemar results as exploratory summaries only. With N=15–20, do not claim adequate power, definitive efficacy, or formal non-inferiority. E1 coverage is descriptive; the earlier −0.10 non-inferiority proposal is not carried forward as a confirmatory decision rule.

## 7. Reviewer and agreement limitations

Two human raters are planned for model-output evidence-support scoring:
- Rater A: the student project lead.
- Rater B: a second human evaluator identified by the project lead; public records use a pseudonym, and explicit agreement plus case-specific exposure/independence screening remain pending.

Both raters must independently score the same raw response using randomized response IDs. Neither may see the other rating before locking. Rater B must not see case identity, hidden evidence-tier label, P0/P1 policy identity, source repository, issue/PR, patch/fixed source, hidden gold mechanism, or the paired response from the other policy. Any prior exposure is logged; a rating is not described as blinded where the screen does not support that claim.

The project lead adjudicates disagreements only after both original ratings are locked. Both raw ratings remain immutable. Report exact agreement, category confusion, six-category Cohen's kappa, and E3 binary agreement/kappa where estimable. Because outputs are clustered within cases and the study is small, agreement statistics are exploratory/descriptive; confidence intervals, if reported, must resample at case level. No minimum kappa threshold determines case acceptance.

Rater B's role is output scoring only. Gold correctness and E1/E2/E3 semantic tier decisions remain the project lead's responsibility, with ChatGPT critique separately labelled advisory. This does not establish independent human validation of the gold mechanisms or evidence-tier construction. ChatGPT is never counted as a human rater. No independent external-audit attestation is claimed.

Rater B's status remains identified/pending confirmation. No second-rater score, agreement statistic, or completed calibration is claimed at this stage.

## 8. Technical, legal, and execution gates
A candidate is not accepted until the pinned dataset row, exact base/fix commits, issue scope, reproducible base-fail/fix-pass test, license/provenance, exposure status, alternatives, evidence packets, hashes, and case record are complete.

The Qwen revision remains a candidate only. Its exact license is recorded as `qwen-research`; the license text and its implications for educational competition use, model access, outputs, and public artifact redistribution must be assessed before use. This document is not legal advice or license clearance.

No model loading, inference, fine-tuning, training, or upstream code execution is authorized by this design decision. Each requires its own completed gate and explicit approval.

## 9. Interpretation boundary
A favorable result would be preliminary evidence about this particular model revision, software-defect sample, packet-construction procedure, prompt contrast, and one-response-per-cell setup. It would not establish universal hallucination reduction, general model self-awareness, or superiority across models and domains. A null or mixed result is still reportable.

## 10. Sequential candidate intake and achieved-N reporting
Candidates are reviewed in the frozen primary-cohort order, followed by the 17 distinct-project reserves if needed. Within-project alternatives may replace a failed issue but do not add an independent project. Stop at 20 accepted cases or exhaustion of the frozen eligible queue; 15 is the primary target and 20 the stretch target. Keep every case that meets the unchanged acceptance criteria. Do not lower the criteria or exclude valid cases merely because N is below 15.

If the achieved N is 1–4, report case-level feasibility only. If N is 5–14, report paired descriptive results without a hypothesis-test claim. If N is 15–20, exploratory paired summaries and exact McNemar may be reported, still without confirmatory efficacy claims. All inference remains subject to separate explicit authorization after the remaining gates.

## 11. Current status
- Accepted cases/projects: 0/0.
- Technical reproductions eligible for this sample: 0.
- Evidence packet sets: 0.
- Model loaded: no.
- Model inference: no.
- Protocol preregistered: no.
- Inference authorization: false.

## 12. Human-evaluator amendment (18 November 2026)

A prospective dual-human output-scoring procedure has been added in `HUMAN_EVALUATOR_AMENDMENT_V0_1_2026-11-18.md` and `SWE_REBENCH_V2_DUAL_HUMAN_OUTPUT_SCORING_RUBRIC_V0_1_DRAFT_2026-11-18.md`. Rater B's explicit agreement, independence/exposure screen, calibration and rubric freeze are pending. This amendment does not alter case eligibility, waive candidate-specific pipeline/debug exposure, or authorize model inference.
