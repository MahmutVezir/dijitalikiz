# Human-evaluator amendment — v0.1

**Date:** 18 November 2026  
**Protocol scope:** SWE-rebench V2 evidence-abstention exploratory/feasibility study, v0.2  
**Status:** Project-lead instruction recorded; second human evaluator identified by first name only in private conversation. Written agreement, eligibility, independence and exposure checks remain pending. This amendment does not authorize model loading, inference, scoring, or case acceptance.

## 1. Decision and role separation

The student project lead remains the sole project lead and final decision-maker for protocol changes, candidate acceptance, scientific interpretation, deviations and release of study results.

A second human evaluator has been identified (private working name: Hasan). To minimize personal data in the public repository, the public record uses the pseudonym **Rater B**. Rater B's proposed role is an independent human scorer of the raw model responses. Rater B is not automatically an external auditor, legal reviewer, co-investigator, gold-standard adjudicator or author of the final scientific interpretation.

ChatGPT remains an AI research assistant. Its critique is not a human rating and will be stored separately.

## 2. Scope of independent human rating

For every model response included in the analysis dataset, Rater A (the student project lead) and Rater B will independently score the same raw response using the frozen v0.2 evidence-support rubric.

Before scoring is unlocked:
- Rater B must explicitly agree to participate.
- Rater B must complete a written case-by-case exposure screen.
- Rater B must not have seen the hidden gold mechanism, source patch/fixed code, model outputs, or case-specific adjudication for the response being scored.
- Rater B must not have contributed to candidate-specific reproduction, prompt calibration, or construction of the evaluation packets for cases to be scored.
- The response package must use randomized response IDs and omit case/project identity, issue/PR, source repository, hidden evidence-tier label, P0/P1 policy label, gold mechanism, patch/fix, and the paired response from the other policy.
- Both raters must submit and lock their original ratings independently before any discussion or adjudication.

If Rater B has prior exposure to a case or cannot be kept blind to the required information, that case-response rating is marked exposed and excluded from the blinded-rater agreement analysis under a predeclared rule. It must not be silently scored as blinded.

## 3. What remains single-researcher

E1/E2/E3 semantic tier construction and technical-gold adjudication remain the project lead's responsibility, supported by explicit evidence-to-mechanism rationales and a separately labelled ChatGPT critique. Rater B will not be shown hidden source, gold mechanism or tier labels before independent output scoring is locked. Therefore this amendment adds a second human rater for model-output evidence-support scoring; it does **not** claim independent human validation of gold mechanisms or E1/E2/E3 tier sufficiency.

Gold-correctness scoring may occur only after both raters' evidence-support decisions are locked. The project lead will record gold correctness separately. Gold correctness must never overwrite an evidence-support rating.

## 4. Disagreement handling

Preserve both raw independent ratings. The project lead adjudicates disagreements only after both ratings are locked, with a separate adjudication record containing the original labels, final label, reason and timestamp. Consensus discussion must not replace the two original ratings.

The analysis will report:
- raw exact agreement;
- the category confusion matrix and category-wise agreement;
- nominal six-category Cohen's kappa for evidence-support ratings;
- binary agreement and Cohen's kappa for the prespecified E3 primary endpoint, where estimable;
- the number and proportion of adjudicated disagreements and unscorable/exposed ratings.

Agreement statistics are descriptive and exploratory, not a pass/fail gate or proof that the rubric is universally validated. Because multiple responses belong to the same case, confidence intervals, when reported, must use case-cluster resampling rather than treating every response as an independent case. Small-sample and category-prevalence limitations must be disclosed. No minimum kappa threshold will be used to accept or reject cases.

## 5. Exposure and case eligibility are not waived

Adding Rater B does not erase the project lead's prior source exposure, candidate-specific pipeline/debug exposure, or any candidate's pre-existing exclusion status. It does not authorize changing an exposure value to "none" without evidence.

The existing v0.2 candidate rule excluding cases used for earlier pipeline debugging, test-oracle troubleshooting or prompt calibration remains unchanged. CTAPIpe #2732 remains on conditional hold pending a truthful project-lead exposure decision; Rater B's participation cannot cure that issue.

## 6. Gates before Rater B can score

Required before any human output scoring:
1. Rater B's explicit agreement and role confirmation.
2. Completed exposure/independence screen for every candidate case.
3. Review and calibration using separate, permanently non-study examples.
4. Frozen dual-human scoring rubric, response blinding procedure and adjudication record format.
5. CI tests for the updated reviewer contract.
6. Internal hash freeze of the protocol amendment, analysis plan and rubric.
7. Explicit project-lead approval to begin scoring after all model execution gates are independently cleared.

No model outputs currently exist. This amendment does not authorize generating them.
