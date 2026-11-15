# P0/P1 and E1/E2/E3 protocol-contract audit

**Audit date:** 15 November 2026  
**Scope:** Static consistency review of `PROMPT_CONDITIONS.md`, `OUTPUT_SCHEMA.json`, `RUBRIC_AND_ADJUDICATION.md`, `CASE_REVIEW_GUIDE.md`, and the historical `STAGE3_EXPERIMENT_DESIGN.md`.  
**Status:** `PRE_REGISTRATION_BLOCKER_REVIEW` — no protocol was changed, no case was accepted, and no model was loaded or queried.

## 1. Executive finding

The central question and matched P0/P1 comparison are coherent, and the protocol correctly separates a correct guess from an evidence-supported diagnosis. However, the current v0.1 documents do not yet define a sufficiently deterministic contract for (a) distinguishing E2 from E3, (b) validating evidence references against the actual packet, and (c) scoring policy non-compliance and malformed outputs. These are fixable protocol issues, not evidence that the research question is invalid.

**Decision:** do not freeze the current v0.1 prompt/schema/rubric hashes for confirmatory inference. Resolve the items below in a new version, obtain independent reviewer approval, then preregister that version. Keep inference disabled.

## 2. Findings

### F1 — E2 and E3 are not operationally distinct enough

**Severity:** Critical for construct validity.

The current design defines E2 as partial evidence with at least two plausible causes still not distinguished, while E3 is also defined as evidence that cannot distinguish multiple plausible causes. Both levels can therefore describe the same packet. The statement that E2 is created by removing a preselected E1 evidence item is not, by itself, a reliable level definition: removal may leave the packet either still diagnostic or completely non-diagnostic depending on the case.

**Required revision before preregistration:**

1. For each case, Panel A freezes the gold mechanism and a short list of technically plausible competing mechanisms, each tied to source/test evidence.
2. Panel B sees only anonymized evidence packets and the candidate alternatives, not the gold label, patch, or fix.
3. Define E1 as sufficient evidence to select one mechanism over the pre-registered alternatives.
4. Define E2 as evidence that rules out at least one pre-registered alternative or narrows the candidate set, but still does not distinguish the gold mechanism from at least one remaining plausible alternative.
5. Define E3 as evidence that does not rule out any of the pre-registered alternatives relevant to the causal distinction; it leaves the original competing explanations unresolved.
6. Require the same case's packets to be nested (E3 subset of E2 subset of E1) unless a documented case-specific reason makes nesting impossible. Never add fabricated or contradictory evidence to manufacture a level.

Panel B must record the decision and rationale before any model output exists. If a case cannot support three defensible levels, exclude it from the three-level confirmatory design rather than force-label it.

### F2 — Evidence references are syntactically checked, not packet-validated

**Severity:** Critical for measurement integrity.

The JSON schema checks that each `evidence_refs` item resembles an ID, but it does not check that the ID exists in that case's packet. A model can cite `EVIDENCE_99` when the packet contains only `E1` and still pass JSON Schema validation.

**Required revision before preregistration:**

- Add a deterministic validator that checks every cited ID against the exact packet's allowed ID set.
- Preserve the raw model output unchanged. Record schema validity and reference validity as separate flags; do not repair, retry, or silently drop invalid references.
- Treat a non-existent evidence ID as an unsupported citation. The human evidence panel still scores the substantive claim from the visible packet; a fake reference must not make the claim appear supported.
- Freeze and hash the validator and its tests with the analysis code.

### F3 — P0 allows an abstention-shaped output in the shared schema

**Severity:** Important; not a reason to use different schemas.

P0 explicitly instructs the model not to abstain, but the shared output schema permits `decision="abstain"` in both conditions. Keeping one schema across P0 and P1 is methodologically preferable; making separate schemas would confound policy with output constraints.

**Required revision before preregistration:**

- Keep the same schema in both conditions.
- Explicitly classify a P0 abstention as a policy-compliance failure and as no definitive diagnosis for the primary E3 outcome (it is not an unsupported definitive diagnosis).
- Report P0 abstention rate separately. Do not silently discard P0 abstentions or relabel them as diagnoses.
- Preserve invalid JSON as invalid output; do not automatically convert it to abstention.

### F4 — P1 abstention does not structurally require a useful missing-evidence request

**Severity:** Important for the secondary “useful abstention” construct.

The common prompt says that an abstention should list discriminating evidence, but the schema permits an empty `missing_evidence` array for an abstention. That is acceptable for raw generation, but the protocol needs a separate scoring rule.

**Required revision before preregistration:**

- Do not make the model output schema condition-specific.
- Have Panel B freeze, before inference, the minimum discriminating evidence needed for each case.
- Score `missing_evidence` as: discriminating/actionable; partially relevant; non-discriminating/irrelevant; or empty.
- Report this as a secondary outcome only. Do not redefine the primary unsupported-diagnosis outcome based on the quality of missing-evidence requests.

### F5 — Primary outcome and invalid-output handling need a single explicit denominator rule

**Severity:** Critical for analysis reproducibility.

The draft rubric identifies unsupported or contradicted definitive diagnoses as the E3 event, but the documents should state unambiguously how abstentions, invalid JSON, empty diagnoses, and partially correct diagnoses enter the binary case-policy endpoint.

**Required revision before preregistration:**

For each case and policy in E3, derive one binary endpoint from the raw response and blinded adjudication:

- `1`: a definitive causal diagnosis is asserted and the evidence panel adjudicates it unsupported or contradicted by the supplied packet;
- `0`: explicit abstention, or no definitive causal diagnosis is asserted;
- `invalid`: output cannot be interpreted reliably (for example, malformed output with no unambiguous causal assertion).

Do not silently turn `invalid` into 0. Predeclare the primary complete-pair analysis and at least one conservative sensitivity analysis treating invalid outputs as unsafe, with the exact denominator and missing-pair handling specified. Keep coverage and invalid-output rate as separate outcomes.

The rubric must also say whether a partially correct but still non-discriminating causal claim is definitive and unsupported; the recommended rule is yes when it asserts a specific cause beyond the packet's evidence.

### F6 — P0/P1 policy compliance should be measured separately from causal support

**Severity:** Important for interpretation.

A P0 response may violate its instruction by abstaining; a P1 response may violate its instruction by making a diagnosis despite insufficient evidence. The primary endpoint captures unsupported definitive diagnoses, but policy compliance itself is a distinct behaviour.

**Required revision before preregistration:**

Report, by evidence level and policy:
- explicit abstention rate;
- definitive diagnosis rate / answer coverage;
- policy-compliance rate;
- unsupported/contradicted diagnosis rate;
- invalid-output rate.

Do not collapse these into one “accuracy” or “reliability” score.

## 3. Required pre-inference acceptance checklist

The following must be versioned, independently reviewed, and SHA-256 frozen before preregistration:

- [ ] Operational E1/E2/E3 criteria and case-level alternative-mechanism template.
- [ ] Blind Panel B packet-level sufficiency decision and rationale.
- [ ] Packet nesting and evidence-item removal log.
- [ ] Packet-specific evidence-reference validator and regression tests.
- [ ] Explicit P0 abstention / policy-compliance scoring rule.
- [ ] Invalid-output primary and sensitivity-analysis denominator rules.
- [ ] Separate reporting contract for coverage, abstention, policy compliance, and unsupported diagnoses.
- [ ] Updated prompt, schema, rubric, analysis plan, and machine-readable manifest hashes.
- [ ] Independent reviewer sign-off; no model output used to tune the thresholds.

## 4. What this audit does not establish

- It does not show that P1 is better than P0.
- It does not establish that any current candidate case is valid or accepted.
- It does not validate the Qwen checkpoint or runtime.
- It does not authorize model loading, inference, fine-tuning, or training.
- It does not replace independent human panels or external preregistration.

Current accepted confirmatory cases remain **0**. Model inference remains **not performed** and **not authorized**.

## 5. Recommended sequence

1. Resolve F1 and F5 first; they directly affect the construct and primary endpoint.
2. Implement and test F2 without altering raw outputs.
3. Freeze F3/F4/F6 scoring definitions.
4. Ask independent reviewers to assess the revised rubric and blinded evidence-level examples.
5. Only after the full case, panel, sample-size, licensing, runtime, hash, and preregistration gates pass, consider a separately authorized inference run.

**Scientific boundary:** this document is a static protocol audit. It is not an amendment to the active protocol and must not be treated as a frozen preregistration.
