# NumPyro #1916 — Panel B semantic packet review protocol

**Version:** 0.1 draft  
**Date:** 19 November 2026  
**Candidate:** pyro-ppl/NumPyro issue #1916 / dataset row `pyro-ppl__numpyro-1918`  
**Status:** Prepared protocol draft only. No reviewer is appointed or exposure-cleared; no packet has been delivered; no review or calibration has occurred. This document does not approve the E1/E2/E3 tiers, accept the case, or authorize inference.

## 1. Purpose and separation of questions

Panel B's first task is to decide, using only the evidence actually visible in each packet, which causal explanations remain plausible and whether the evidence justifies a unique causal diagnosis. Panel B must not infer the hidden gold mechanism from source-fix knowledge.

This is separate from:
- **Stage 2 technical reproduction:** already passed; it establishes a reproducible base/fix contrast.
- **Panel A technical gold review:** two independent source-aware reviewers must establish the exact defect mechanism, alternatives, and test/fix relationship.
- **Panel B model-output review:** after a separately authorized inference study, reviewers score the raw responses under the existing output-adjudication rubric.
- **External audit:** a disjoint auditor later checks evidence authenticity and role separation.

A correct root-cause guess is not necessarily supported by a packet. Evidence sufficiency must be rated without access to hidden gold.

## 2. Role separation

### Packet custodian / technical preparer
The project lead has already inspected the public issue, PR, patch, and reproduction evidence. The project lead may prepare anonymized delivery copies and preserve the private code-to-packet map, but must not act as a blinded rater, adjudicate Panel B disagreements, or score confirmatory model outputs.

Hasan's earlier approval was approval of the proposed design, not an independent semantic rating. It does not qualify as Panel B review.

### Panel A — technical gold and alternatives
At least two independent reviewers establish the defect mechanism, competing explanations, relationship between the frozen selectors and the issue, and any scope limitation. Panel A may inspect upstream source, issue, PR, patch, and fixed revision. Panel A must not serve on Panel B or as the confirmatory analyst. Preserve each initial review before adjudication.

### Panel B — semantic packet reviewers
At least two independent reviewers rate every coded packet separately. They must be disjoint from Panel A, the project lead, Hasan (who has seen the design proposal), the technical preparer, and any person who has inspected the NumPyro patch/fixed source for this case.

Before accepting the role, each reviewer must attest:
- no prior access to the NumPyro issue/PR, patch, fixed source, gold mechanism, or this candidate's adjudication notes;
- no participation in the technical reproduction or packet construction;
- no conflicts that would compromise independent judgment;
- no external searching, repository lookup, or communication about packet identity or content during the rating period.

A reviewer who has previously seen the issue, source or fix is ineligible for this case's blinded Panel B. Reviewer identity, consent, conflict/exposure screen, and access log must be retained in restricted records.

### Adjudicator
A third person who is independent of the two raters resolves disagreements only after both original ratings are signed and locked. The adjudicator's decision is stored separately and never overwrites either initial rating.

## 3. What blinding means here

The intended blinding is to **packet-level labels, evidence-tier names, source provenance, hidden gold, patch/fixed evidence, and reviewer-to-reviewer scores**. It is not appropriate to claim perfect source-identity blinding: the verbatim issue text includes recognizable technical identifiers and may allow a reviewer to infer the library.

The custodian must:
1. Extract only each inner packet's evidence item kind and exact visible content.
2. Replace all original evidence IDs with neutral item IDs (for example, `item-01`, `item-02`); remove packet IDs, tier labels, source paths, commit IDs, issue/PR URLs, source hashes, and the outer packet-set wrapper.
3. Assign opaque packet codes using independently generated random identifiers; do not use `E1`, `E2`, `E3`, or a sequence that signals strength.
4. Randomize presentation order separately for each reviewer. Never provide a labelled comparison table or explain that the three packets are nested.
5. Preserve exact evidence content bytes. Do not paraphrase, truncate, rewrite, or silently redact technical evidence. If safe identity masking would alter semantic content, do not apply it; instead disclose that source identity may be inferable.
6. Keep the code-to-tier mapping, source provenance, and hidden gold in a restricted custodian-only record, separate from reviewer files.

The public GitHub repository is not an access-controlled reviewer store. Do not deliver review packets, mapping keys, or reviewer forms through the public repository. A restricted delivery location and an access log must exist before any review is called blinded.

After rating, ask reviewers whether they recognized the source or searched externally. Record the answer. Any reviewer who recognized the case or consulted external material is flagged; do not silently retain their score as blinded.

## 4. Independent review procedure

For each coded packet, each reviewer independently completes one form without discussing the case with the other reviewer.

1. **Technical readability:** Can the packet be interpreted without hidden context? Record missing or ambiguous information.
2. **Free-form mechanism generation:** List every plausible causal explanation consistent with the visible evidence. Do not give reviewers the project's hidden gold or a leading list of proposed alternatives.
3. **Evidence linkage:** For each proposed explanation, cite the neutral item ID and exact excerpt that supports it. A symptom, stack frame, component name, or call-site alone is not automatically a causal explanation.
4. **Alternative discrimination:** State which explanations are excluded by the visible evidence, which remain plausible, and which cannot be assessed. Explain why; do not infer that an explanation is false merely because the packet does not mention it.
5. **Unique-cause decision:** Select one: `one mechanism is uniquely supported`, `multiple mechanisms remain plausible`, `no causal mechanism can be assessed`, or `unscorable`.
6. **Missing evidence:** Specify the smallest additional evidence that would discriminate the remaining explanations.
7. **Confidence:** Record reviewer confidence in the judgment, not model confidence.

A reviewer must not use confidence language, answer length, or number of citations as a substitute for causal support.

## 5. Predeclared tier acceptance logic

The custodian retains the hidden mapping. After independent ratings are locked, a separate adjudication step compares Panel B's free-form mechanism sets with Panel A's predeclared mechanism/alternative record.

A three-tier case is defensible only if all conditions hold:

- **E3:** all predeclared plausible mechanisms remain possible; the packet does not eliminate a defensible alternative.
- **E2:** at least one predeclared alternative is excluded by visible evidence, while at least two distinct causal mechanisms remain plausible.
- **E1:** exactly one mechanism remains defensible from visible evidence, and it matches the independently adjudicated technical gold.

Panel B does not receive the tier names or gold during rating. The tier label is assigned only after the blind ratings are locked and the independent gold record is available.

Do not force a tier assignment:
- If E3 already isolates one mechanism, it is not a valid E3.
- If E2 leaves fewer than two plausible mechanisms, it is not a valid E2.
- If E1 leaves more than one plausible mechanism, it is not a valid E1.
- If the unique E1 mechanism does not match gold, the packet set is invalid.
- If one of the levels cannot be defended, revise the packet design prospectively or exclude the case from the three-level confirmatory design. Do not change evidence after viewing any model outputs.

## 6. Disagreement, calibration, and reporting

- Preserve two separate initial ratings per coded packet, with timestamps and immutable copies.
- Report exact agreement counts and each disagreement. Do not claim a reliable population-level agreement coefficient from only three packets; a meaningful agreement estimate requires a sufficiently large independent calibration set.
- Use calibration cases from outside the confirmatory cohort. A case used to train or calibrate reviewers is permanently excluded from confirmatory analysis.
- If the reviewers disagree on whether a causal mechanism is asserted, whether evidence establishes causality, or whether an alternative remains plausible, send the locked forms to the adjudicator. Preserve the adjudicator's rationale.
- Record unscorable ratings and missing evidence. Do not coerce them into an E-level.
- Freeze the final rubric, calibration instructions, reviewer role rules, packet transformation method, and hashes before confirmatory model output collection.

## 7. Panel B output scoring remains separate

When model responses eventually exist, use `SWE_REBENCH_V2_OUTPUT_ADJUDICATION_RUBRIC_V0_1.md` as a separate scoring procedure. Panel B must see the visible packet and one raw response with randomized response ID, but not the case identity, policy label, paired response, gold mechanism, fix, or evidence-tier label. The output rubric's asserted-diagnosis and evidence-support judgments must be preserved separately from root-cause correctness.

No raw response exists for this candidate today. This protocol does not create or imply model output.

## 8. Current operational gate

Before review starts, the project must still obtain:
- two qualified, consented, exposure-cleared Panel B reviewers;
- two Panel A technical reviewers and a disjoint adjudicator;
- restricted reviewer storage and a documented access log;
- anonymized packet copies with opaque IDs and an offline mapping key;
- a frozen review form and calibration set outside the confirmatory cohort.

**Current result:** preparation only. No reviewer has been appointed, no blind delivery has occurred, no semantic rating has been made, and no case has been accepted. Model loading, inference, and fine-tuning remain unauthorized.
