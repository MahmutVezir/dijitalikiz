# Study design decision — v0.2 exploratory/feasibility
**Date:** 16 November 2026  
**Status:** Approved working direction by project lead; draft protocol only. Not preregistered. No case accepted. No model use authorized.

## 1. Decision recorded
The project lead selected:
  Study type: 20 case exploratory/feasibility study.
- Model route: retain the pinned Qwen/Qwen2.5-3B-Instruct candidate, subject to exact-revision license and runtime review before loading or inference.
- Working team: project lead (student researcher) and ChatGPT as an AI research assistant. ChatGPT is not a human co-investigator, independent human rater, legal reviewer, or external auditor.
- No recruitment of additional human evaluators is planned under this working arrangement.

## 2. Research question
On the same frozen language model and same software-defect case, does allowing abstention when the visible evidence does not distinguish plausible causes (P1), compared with requiring a diagnosis (P0), change the rate of unsupported definitive root-cause claims in E3 evidence conditions, while preserving useful diagnosis behavior in E1?

The study distinguishes:
1. gold-root-cause correctness;
2. support from the evidence actually visible to the model;
3. whether the model abstains;
4. whether the response follows the assigned policy.

A correct guess is not automatically an evidence-supported diagnosis. The study does not measure or prove internal model self-awareness.

## 3. Sample and independence
- Target: 20 accepted cases from 20 distinct upstream projects.
- Fifteen cases is the preferred analysis threshold, not an eligibility floor.
- One case per upstream project. Forks, mirrors, transfers, duplicate issues, and shared upstream identities are grouped and cannot be counted as independent projects.
- If 15 qualifying independent projects cannot be obtained, report the achieved smaller feasibility sample and its limits; do not duplicate projects to inflate N or relax acceptance criteria.
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

Because the project will not recruit a second human panel, E-level decisions will be recorded as single-researcher judgments supported by explicit evidence-to-mechanism rationales, with ChatGPT's separate AI critique recorded as advisory only. This arrangement does not establish inter-rater reliability or independent human validation. Cases with unresolved ambiguity are excluded or reported as unclassified; they are not forced into a tier.

## 6. Scoring and analysis
Primary exploratory outcome: for E3, whether an asserted causal diagnosis is unsupported, partially supported, or contradicted by the visible packet. A valid abstention without diagnosis leakage is not an unsupported diagnosis. An asserted diagnosis is not considered supported merely because it matches the hidden gold cause.

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
No second human evaluator is part of this project arrangement. Therefore:
- no human-human Cohen's kappa will be calculated or claimed;
- ChatGPT's scores or critiques will never be represented as a second human rating;
- AI critique and researcher decisions will be stored separately;
- disagreement between the researcher and AI critique will be reported as an audit trail, not as inter-rater reliability;
- no independent external-audit attestation will be claimed.

This is a material limitation. The project will present the E1/E2/E3 framework as a proposed operational method applied in a feasibility study, not as a fully validated measurement instrument.

## 8. Technical, legal, and execution gates
A candidate is not accepted until the pinned dataset row, exact base/fix commits, issue scope, reproducible base-fail/fix-pass test, license/provenance, exposure status, alternatives, evidence packets, hashes, and case record are complete.

The Qwen revision remains a candidate only. Its exact license is recorded as `qwen-research`; the license text and its implications for educational competition use, model access, outputs, and public artifact redistribution must be assessed before use. This document is not legal advice or license clearance.

No model loading, inference, fine-tuning, training, or upstream code execution is authorized by this design decision. Each requires its own completed gate and explicit approval.

## 9. Interpretation boundary
A favorable result would be preliminary evidence about this particular model revision, software-defect sample, packet-construction procedure, prompt contrast, and one-response-per-cell setup. It would not establish universal hallucination reduction, general model self-awareness, or superiority across models and domains. A null or mixed result is still reportable.

## 10. Sequential candidate intake and achieved-N reporting
Candidates are reviewed in the frozen primary-cohort order, followed by the 17 distinct-project reserves if needed. Within-project alternatives may replace a failed issue but do not add an independent project. Stop at 20 accepted cases or exhaustion of the frozen eligible queue. Keep every case that meets the unchanged acceptance criteria. Do not lower the criteria or exclude valid cases merely because N is below 15.

If the achieved N is 1–4, report case-level feasibility only. If N is 5–14, report paired descriptive results without a hypothesis-test claim. If N is 15–20, exploratory paired summaries and exact McNemar may be reported, still without confirmatory efficacy claims. All inference remains subject to separate explicit authorization after the remaining gates.

## 11. Current status
- Accepted cases/projects: 0/0.
- Technical reproductions eligible for this sample: 0.
- Evidence packet sets: 0.
- Model loaded: no.
- Model inference: no.
- Protocol preregistered: no.
- Inference authorization: false.
