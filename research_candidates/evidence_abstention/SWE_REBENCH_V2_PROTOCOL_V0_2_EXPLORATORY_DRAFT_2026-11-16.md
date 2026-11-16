# SWE rebench V2 evidence abstention protocol — v0.2 exploratory draft
**Date:** 16 November 2026  
**Status:** Exploratory/feasibility design draft. Supersedes v0.1 only as the proposed working design; v0.1 is retained as historical design record. Not preregistered. Not legal clearance. No inference or upstream execution authorization.

## 1. Research question and scope
In real software defects, does a policy that may abstain when visible evidence is insufficient (P1), compared with a policy that requires a diagnosis (P0), change the rate of unsupported definitive root-cause diagnoses?

The study distinguishes gold-root-cause correctness from support by the evidence actually shown to the model. It does not claim to measure internal model self-awareness.

This is a small exploratory/feasibility study, not a confirmatory efficacy trial.

## 2. Data source and candidate status
Candidate source: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`, Parquet revision `fb9aa226b2ce37c708ea7732e7b980abacdadb67`, SHA-256 `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.

The pinned dataset contains 6,272 rows. The frozen candidate cohort contains 96 primary project candidates and 17 declared project reserves. These are metadata candidates, not accepted defects. The dataset card's CC-BY-4.0 license does not relicense the code in the upstream repositories. Every selected source requires exact-base, changed-file, nested dependency, and notice/provenance review.

The timestamp register's one-second `simpeg/simpeg#1633` discrepancy and raw-payload authentication limitation remain open. This metadata issue must be resolved or the affected candidate excluded under a written rule before it can be accepted.

## 3. Sample and stopping
- Target: 20 accepted defects from 20 distinct upstream projects.
- Fifteen accepted defects is a preferred analysis threshold, not an eligibility floor. Any positive number of fully accepted independent cases may be retained.
- One case per independent upstream project. Forks, mirrors, transfers, duplicate issues, and shared upstreams are not independent.
- Review candidates sequentially in the frozen primary-cohort order, followed by the 17 distinct-project reserves if needed. Use within-project alternatives only to replace an issue in the same project. Stop when 20 cases are accepted or the eligible frozen queue is exhausted. Report the actual N; do not relax eligibility to hit the target.
- If fewer than 15 cases survive, retain all accepted cases. For N=1–4 report case-level feasibility only; for N=5–14 report paired descriptive results without a hypothesis-test claim; for N=15–20 exploratory paired summaries and exact McNemar may be reported. No band permits a confirmatory efficacy claim.

Each case is one independent unit. Its six condition outputs are repeated measurements, not six independent observations.

## 4. Case eligibility
A candidate must have:
1. exact dataset row and immutable repository/base/fix identifiers;
2. issue/task scope that matches the defect and patch;
3. exact-base and changed-file/nested provenance and license review;
4. a reproducible defect-specific target test that fails on the pinned buggy base and passes on the exact verified fix under the same recorded environment;
5. a documented technical root-cause mechanism and at least two plausible, testable alternatives;
6. an exposure and duplication/fork-independence audit;
7. a three-level evidence packet set with stable IDs, source provenance, and hashes;
8. a complete case record and explicit acceptance decision.

A candidate used for earlier pipeline debugging, test-oracle troubleshooting, or prompt calibration is excluded from the study sample. Prior exposure is recorded; it is not silently waived. Static review alone is not technical reproduction. A test is not described as run unless a raw execution log exists.

## 5. Ground truth and evidence levels
The technical gold record identifies the actual defect mechanism using the issue, exact base/fix, changed code, and defect-specific reproduction. It must also record at least two plausible alternative mechanisms and the observations that could distinguish them.

For each case, build three nested packets from real, provenance-backed evidence:
- E3 is a proper subset of E2;
- E2 is a proper subset of E1;
- repeated evidence IDs have identical content and source-snapshot hashes across tiers;
- E2 adds at least one evidence item to E3; E1 adds at least one to E2;
- no evidence is fabricated, rewritten, selectively paraphrased to change meaning, or silently truncated.

Semantic definitions:
- E3: all predeclared mechanisms remain possible under the visible packet; none is defensibly eliminated.
- E2: at least one alternative is eliminated by a specific evidence item, but at least two mechanisms remain possible.
- E1: exactly one mechanism remains possible and it matches the technical gold record.

A level is not determined by packet length or evidence count. If a case cannot support all three defensible tiers, it is excluded from the three-tier comparison or recorded as unclassifiable. Do not manufacture evidence or force a tier.

## 6. Review and scoring arrangement
The working team consists of the student project lead and ChatGPT as an AI research assistant. ChatGPT is not a human reviewer, independent auditor, legal reviewer, or second investigator.

The project lead records the human research decisions. ChatGPT may conduct a separately labelled AI critique using only the material assigned to that review step. The critique is advisory and is not independent human validation. Since the project has no second human rater:
- no human-human Cohen's kappa or inter-rater reliability claim is permitted;
- researcher and AI judgments remain separate;
- disagreements and their resolution are logged;
- the evidence-tier framework is reported as a proposed operationalization applied in a feasibility study, not a validated measurement instrument.

For model-output scoring, use a predeclared rubric and randomized response IDs. The scorer should see the model-visible packet and raw response, but not policy identity, hidden tier, case identity, patch, or gold cause until evidence-support scoring is locked. Because a single researcher may have source exposure, perfect blinding cannot be assumed. Record any unavoidable exposure and treat scoring as exploratory. ChatGPT may perform a separate blind-style critique, but this does not create independent human blinding.

## 7. Experimental conditions
Each case has six cells: E1/P0, E1/P1, E2/P0, E2/P1, E3/P0, E3/P1.

P0 requires a single best root-cause diagnosis even if evidence is incomplete. P1 asks for a diagnosis only when visible evidence distinguishes it from alternatives; otherwise it must explicitly abstain and identify discriminating missing evidence.

The same frozen model, tokenizer, system prompt, output schema, packet content, generation settings, and runtime must be used in both policies. Only the policy instruction changes. Use one raw generation per cell. No retries, response repair, selective reruns, or hidden prompt changes in the analysis dataset.

The common response schema records decision, root cause, evidence references, rationale, alternative hypotheses, and missing evidence. JSON/schema validity, reference validity, policy compliance, semantic evidence support, and gold correctness are separate outcomes.

## 8. Model and license
Candidate: `Qwen/Qwen2.5-3B-Instruct`, immutable revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`. The exact revision's license identifier is recorded as `qwen-research`, not Apache-2.0. License review and assessment of educational competition use, access, outputs, and public redistribution remain pending. No legal conclusion is made in this protocol.

No model load or inference until exact-revision license review, runtime specification, and explicit execution approval are complete. No fine-tuning or training is included.

## 9. Outcomes
Primary exploratory outcome: E3 strictly unsupported asserted diagnosis. A definitive causal diagnosis is in this primary category only when the visible packet does not support the asserted causal mechanism, or when the visible packet contradicts it. A partially supported diagnosis is not collapsed into this primary category; it is recorded as its own prespecified category and reported separately. A valid abstention without diagnosis leakage is not an asserted diagnosis. A correct hidden-gold match that is not justified by visible evidence remains unsupported.

Secondary descriptive outcomes, reported separately:
- gold-root-cause correctness;
- evidence-support category;
- abstention rate and diagnosis coverage;
- P0/P1 policy compliance;
- evidence-reference validity;
- invalid JSON/schema output rate;
- usefulness of missing-evidence requests;
- E1 answer coverage and E2 response behavior.

Do not combine these into a composite accuracy score.

## 10. Analysis and interpretation
For E3, retain paired case-level P0/P1 outcome counts and descriptive risk differences at any achieved N. With N=1–4, report case-level outcomes only; with N=5–14, report paired descriptive counts and risk differences without a hypothesis-test claim; with N=15–20, an exact McNemar p-value may additionally be reported as exploratory only. No definitive efficacy claim, confirmatory power claim, or formal E1 non-inferiority claim is permitted.

Report E1 coverage descriptively. The earlier −0.10 non-inferiority margin is not adopted as a decision rule in this exploratory design. Invalid outputs are retained and reported separately; do not repair, retry, or silently recode them. Any sensitivity recoding must be specified before outputs are examined and shown separately from the primary observed data.

## 11. Data integrity and reproducibility
For each case, evidence item, prompt, packet, raw model output, and analysis file, record stable IDs and SHA-256 hashes. Preserve exact raw outputs and execution logs. Record model/tokenizer revisions, library versions, hardware, precision, generation parameters, environment lock, and timestamps. A hash proves byte identity, not scientific validity or source authenticity.

## 12. Explicit stop gates
No model load or inference until:
- sample-selection and case-acceptance rules are frozen;
- exact source licenses/provenance are reviewed;
- candidate test pairs are reproduced and logged;
- evidence packet rules and scoring rubric are frozen;
- model license assessment is complete;
- runtime is specified and tested without generation;
- prompt/schema/analysis artifacts are versioned and hashed;
- the project lead explicitly authorizes the model run.

No training or fine-tuning is permitted under this protocol.

## 13. Current status
Accepted cases/projects: 0/0. Evidence packet sets: 0. Model load: not performed. Inference: not performed and not authorized. Protocol: draft, not preregistered. The prior v0.1 confirmatory design requiring 60 independent projects and independent human panels is retained as historical record and is not the selected working design for this exploratory study.
