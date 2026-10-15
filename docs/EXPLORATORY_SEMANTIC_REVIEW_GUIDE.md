# Guide for the Blinded Exploratory Semantic Review

**Purpose:** Blinded, evidence-summary-based exploratory review of existing model responses after the frozen confirmatory analysis. This is not a new confirmatory result or independent source-code validation.

## What the reviewer receives

The packet contains randomized review IDs, repeated-response case references, a sanitized task-domain label, a reported-problem summary, numbered base facts (B1, B2, …), and the model response. It deliberately omits the expected root cause, ground-truth fields, direct source URLs, project/repository identifiers, publication dates, condition labels, seeds, and source-case IDs. The private coordinator key maps review IDs back to the original records and raw-output hashes.

This is not perfect anonymity: class names, technical details, and response wording may allow a reviewer to infer a case or treatment. Reviewers must not search for case identifiers, attempt to infer the condition, or discuss answers before both forms are locked. Because source links and the canonical answer are withheld, the initial review is based on the evidence summaries provided in the packet; it does not itself prove source-code ground truth.

The response rows derive from the verified archived confirmatory artifact. Reviewers must not edit the model response or supplied evidence summaries. Each reviewer should work on a separate copy and submit decisions independently before discussion. Fill only the review fields. Cite the reported-problem summary or numbered base facts (for example, “B2”) in the rationale.

## Review dimensions and labels

### Root-cause correctness — primary exploratory label

Use exactly one of:
- **correct:** identifies the underlying fault mechanism supported by the source evidence, including a valid paraphrase.
- **partially_correct:** identifies part of the mechanism but omits or misstates a material qualifier, or combines a correct mechanism with an unresolved alternative.
- **incorrect:** identifies a different cause, contradicts the evidence, or provides only a symptom without the causal mechanism.
- **unscorable:** the response is empty, incoherent, or the available evidence does not permit a decision.

A generic label such as “logic error”, “implementation error”, or “dependency issue” is not automatically correct. Do not require a literal match to the canonical underscore-separated ground-truth label.

### Component localization

Use **correct**, **partially_correct**, **incorrect**, or **unscorable**. Accept a method/overload or directly responsible implementation class when the source evidence supports it, even if it is not textually identical to the canonical component. Mark partial when the response names a relevant neighboring component but does not localize the fault precisely.

### Evidence consistency

Use **consistent**, **partially_consistent**, **inconsistent**, or **unscorable**. Check whether the explanation agrees with the issue, failing test, fix and supplied base facts. Penalize fabricated implementation details, unsupported concurrency claims, and causal relations not supported by the case evidence.

### Dependency reasoning

Use **correct**, **partially_correct**, **incorrect**, **not_applicable**, or **unscorable**. Judge whether the stated propagation/dependency path is supported by the case evidence. Merely listing class names or repeating a graph edge is not enough.

### Overall diagnostic status

Use **correct**, **partially_correct**, **incorrect**, or **unscorable**. This is a secondary holistic judgment, not a substitute for the individual labels above.

## Blinding and adjudication

1. Do not attempt to infer or record the treatment condition.
2. Decide each response independently based on the reference and source evidence.
3. Write a short rationale citing the specific supplied evidence item (reported problem or B1/B2/…) that supports the label. Do not describe it as verified source-code evidence if the packet only provides the summary.
4. Do not discuss decisions with the other reviewer until both copies are complete.
5. After independent review, compute per-dimension agreement and make a separate adjudication record for disagreements. Do not replace original reviewer labels with adjudicated labels.
6. Keep this analysis marked **exploratory and post hoc**. It cannot retroactively replace the frozen primary endpoint or be presented as preregistered confirmatory evidence.

## Interpretation constraints

- These responses have already been observed, and the packet is assembled after the original confirmatory analysis. Review results are exploratory even though condition labels are masked.
- The 5 generations per case are repeated model outputs, not five independent software defects. Aggregate to one prespecified case-level outcome per condition if summarizing the review.
- Report label counts by condition only after unblinding. Report disagreement, unscorable responses, and ambiguous cases.
- Do not use this review to adjust the old alias rubric and then call its revised scores confirmatory.
- Use the review to diagnose the measurement instrument and inform a separate future protocol with new independent cases and a rubric frozen before inference.

## Packet generation

Run the builder twice against the verified archive extraction. Give only the matching packet to each reviewer; keep both key files private:

    python scripts/build_blinded_exploratory_review_packet.py --artifact-root /path/to/confirmatory-output --output /path/to/reviewer_A_packet.jsonl --key-output /path/to/reviewer_A_key_private.json --reviewer-label A
    python scripts/build_blinded_exploratory_review_packet.py --artifact-root /path/to/confirmatory-output --output /path/to/reviewer_B_packet.jsonl --key-output /path/to/reviewer_B_key_private.json --reviewer-label B

The builder uses a stable anonymous case-reference map, but independently deterministic row orders and reviewer-specific IDs. Each reviewer must receive only their own packet. The two key files are distinct and must not be shared with reviewers; keep them private until both independent review files are locked. The builder validates the expected case-condition-seed inventory and records the SHA-256 of each raw output in the private key. Reviewer-facing rows preserve the exact model responses but omit the answer key, public source URLs, project identifier, condition, seed, and original case ID. Response wording may still hint at the condition, so blinding is not claimed to be perfect. Both packets are exploratory/post hoc and do not change the frozen historical result.
