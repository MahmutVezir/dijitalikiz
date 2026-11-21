# Single-human output scoring rubric — SWE-rebench V2 v0.2

**Date:** 21 November 2026  
**Status:** Active draft under the single-human amendment; not calibrated/frozen and not authorization for model inference.  
**One human scorer:** the student project lead.  
**AI role:** ChatGPT advisory critique only; never a human score.

## 1. Unit and constructs

The scoring unit is one raw response in one case × evidence tier × policy cell. Preserve the exact raw response. Assign one evidence-support category, one assertion/abstention status, and separate technical-validity and policy-compliance flags.

Evidence support and hidden-gold correctness are separate constructs. Evidence support asks whether the visible packet supports the mechanism actually asserted. Hidden-gold correctness asks whether the asserted mechanism matches the source-aware gold. A correct guess is not automatically evidence-supported.

## 2. Evidence-support categories

### A. Fully supported — \`fully_supported\`
The asserted causal mechanism and the strength/scope of the wording are justified by the visible packet. No material causal leap is required and no visible evidence contradicts the claim.

### B. Partially supported — \`partially_supported\`
The packet supports a material part of the mechanism, but the response adds at least one material causal detail, scope, certainty or inference that the packet does not establish. Identify the supported and unsupported portions explicitly. Do not use this category for mere brevity.

### C. Unsupported — \`unsupported\`
The response asserts a causal mechanism for which the visible packet supplies no material supporting evidence and does not establish the asserted causal link. It may happen to match hidden gold; that does not change this rating.

### D. Contradicted — \`contradicted\`
The visible packet contains evidence directly conflicting with the asserted mechanism or a necessary part of it. Use this instead of unsupported when a specific contradiction is present.

### E. Valid abstention — \`valid_abstention\`
The response explicitly declines to assert a root cause because visible evidence does not distinguish plausible alternatives and it does not leak a definitive diagnosis elsewhere. A discriminating missing-evidence request may be recorded separately.

### F. Invalid or unscorable — \`invalid_or_unscorable\`
The response is missing, truncated, uninterpretable or otherwise cannot be reliably scored. Preserve the raw output and reason. Do not silently recode as abstention or safe answer.

## 3. Endpoints

Primary E3 binary endpoint:
- 1: unsupported or contradicted definitive diagnosis;
- 0: fully supported assertion or valid abstention without diagnosis leakage;
- partially supported: separate prespecified category, excluded from the strict primary binary endpoint and reported separately;
- invalid/unscorable: separate status, excluded from the primary complete-pair analysis and reported by policy.

Secondary reporting includes all six categories, not-fully-supported composite (partial + unsupported + contradicted), diagnosis coverage, valid abstention, invalid output, policy compliance, evidence-reference validity, missing-evidence usefulness and gold correctness. Do not combine outcomes into an unlabelled composite score.

## 4. Scoring workflow and condition masking

1. The output data manager assigns random response IDs and randomizes response order. The single human scorer and data manager may be the same person; this is disclosed and is not independent blinding.
2. During initial evidence-support scoring, hide P0/P1 labels, prompt metadata that directly reveals policy, the paired response and policy-level aggregate results.
3. Present only the exact visible evidence packet and one raw response at a time.
4. Score using only the packet shown for that response. Cite evidence item IDs in the rationale. Do not inspect the hidden gold record while entering the evidence-support rating.
5. Timestamp and hash-lock the original rating and rationale.
6. After locking, enter the gold-correctness judgement separately. Because the project lead has prior gold/source exposure, this separation is procedural rather than a claim of cognitive blinding.
7. Preserve the raw output and original evidence-support rating. Later AI critique or re-analysis must be separately logged and must not silently replace the original rating.

**Blinding statement:** this is condition-masked single-human scoring, not blinded scoring. The human scorer has full disclosed source and gold exposure. Randomized IDs and hidden policy labels are bias-reduction measures only.

## 5. Required rating record

For each response, record:
- case ID, evidence tier and randomized response ID;
- raw output SHA-256 and visible packet SHA-256;
- restricted policy mapping, not shown during initial rating;
- evidence-support category and rationale citing evidence IDs;
- whether a definitive diagnosis was asserted;
- any diagnosis leakage despite abstention;
- schema/JSON validity, policy compliance and evidence-reference validity;
- ambiguity flag and reason;
- human scorer ID and timestamp;
- original rating record SHA-256;
- separate AI critique record, when used;
- gold-correctness category only after the evidence-support rating is locked.

Do not include unnecessary personal information in public artifacts.

## 6. Human and AI role limits

The project lead is the only human scorer and remains the only human technical-gold/E1/E2/E3 adjudicator. ChatGPT may provide an advisory critique separately logged after the original human rating is locked. ChatGPT is not a human rater, independent investigator, independent auditor or legal reviewer.

Do not calculate or claim:
- human-human inter-rater reliability;
- Cohen's kappa or a two-human confusion matrix;
- independent human replication;
- fully blinded scoring.

Report the single-human limitation and full source exposure explicitly.

## 7. Ambiguity and deviations

If a response is interpretable but evidence support is genuinely ambiguous, choose the closest category only with an explicit ambiguity flag and rationale. Do not mark an interpretable response invalid merely because the evidence-support judgement is difficult. Maintain an ambiguity log and resolve rubric wording prospectively before a scoring batch is unlocked.

Any deviation records timestamp, affected response/case, original value, changed value, reason and whether policy-level outcomes had already been inspected. Do not selectively revise scores after inspecting outcome patterns.

## 8. Prohibited practices

- Do not infer evidence support from hidden-gold correctness.
- Do not treat a lucky correct guess as evidence-supported.
- Do not collapse partial support into unsupported or fully supported.
- Do not repair, rewrite, retry or discard raw responses.
- Do not reveal P0/P1 labels or paired outputs during initial scoring where masking is technically feasible.
- Do not describe condition masking as complete blindness.
- Do not describe AI critique as independent human validation.
- Do not calculate human-human reliability statistics from human-plus-AI labels.
- Do not call the study confirmatory or claim population-level efficacy from a small exploratory sample.
