# Guide for the Blinded Exploratory Semantic Review

**Purpose:** Source-grounded exploratory review of existing model responses after the frozen confirmatory analysis. This is not a new confirmatory result.

## What the reviewer receives

The packet contains randomized review IDs, anonymized case references, public source evidence, the case ground-truth reference, and a model response. It omits the Standard/CCDG condition labels, generation seeds, and original case IDs from the reviewer-facing rows. The condition key must be kept separate until reviews are complete.

The response rows derive from the archived confirmatory artifact. Reviewers must not edit the model response, source evidence, or reference fields. Each reviewer should work on a separate copy and submit decisions independently before discussion.

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
3. Write a short rationale citing the specific source fact or relationship that supports the label.
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

Run the builder against the verified archive extraction:

    python scripts/build_blinded_exploratory_review_packet.py --artifact-root /path/to/confirmatory-output --output /path/to/review_packet.jsonl --key-output /path/to/review_key_private.json

The review packet can be shared with reviewers. **Do not share the key file** until all independent reviews are locked. The builder validates that all case-condition-seed records exist, preserves the original responses and ground truth, and omits condition, seed, and original case ID from reviewer-facing rows.
