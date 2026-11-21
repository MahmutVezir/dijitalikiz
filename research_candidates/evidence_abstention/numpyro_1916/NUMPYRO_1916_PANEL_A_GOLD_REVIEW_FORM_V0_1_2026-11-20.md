> **Supersession notice — 20 November 2026:** This form is an archived optional technical-review aid, not an active gate for NumPyro #1916 under the adopted v0.2 Dishka-equivalent route. The project lead is the single source-aware human adjudicator for technical gold and E1/E2/E3; ChatGPT is advisory only. Two independent human scorers remain required later for raw model-output evidence-support ratings only. No independent Panel A reviewers or signed reviews are claimed by this document. See `research_candidates/evidence_abstention/numpyro_1916/PROJECT_LEAD_TIER_DECISION_NUMPYRO_1916_2026-11-20.md` for the operative project-lead tier decision.

# NumPyro #1916 — Panel A independent technical gold review

**Version:** 0.1 draft  
**Date:** 20 November 2026  
**Purpose:** Independent, source-aware review of the technical defect, alternatives, and issue/patch/test alignment. This review is separate from Panel B semantic packet scoring and separate from final project-lead case acceptance.

## Candidate identifiers

- Upstream repository: https://github.com/pyro-ppl/numpyro
- Issue: https://github.com/pyro-ppl/numpyro/issues/1916
- Fix PR: https://github.com/pyro-ppl/numpyro/pull/1918
- Buggy base: `07e4c9bc4524cc0a741ba8f8ad41339d34a0288d`
- Fixed upstream merge: `5692d2da335945b756aeae02e3720b9b7f3efef2`
- Frozen source dataset row: `pyro-ppl__numpyro-1918`
- Frozen selectors: AIES and ESS variants of `test_warmup`.

## Role requirements

Two source-aware technical reviewers must complete independent initial reviews. Each must document competence, consent, conflict-of-interest screening, and any prior exposure. They must not see each other's forms before both are locked. A separate adjudicator resolves disagreements after both initial reviews are preserved. Panel A reviewers must not serve as Panel B reviewers for this candidate.

The project lead and Hasan are not assumed to be Panel A reviewers merely because they approved the design proposal. Their role, competence and consent must be separately documented. The project lead has inspected the issue, patch, pinned source and reproduction; Hasan has seen the proposed E1/E2/E3 design.

## Review sequence

1. **Issue and buggy-base pass:** Read issue #1916 and inspect only the frozen buggy-base source and issue reproducer. Independently state the suspected mechanism before viewing the fix.
2. **Alternatives pass:** Identify every materially distinct explanation that could produce the observed error. Distinguish caller misuse, sampler API contract, MCMC warmup-state handoff, JAX PRNG behavior and dependency-version incompatibility.
3. **Fix and regression pass:** Inspect PR #1918 and fixed merge. Determine exactly what changed and whether the two selectors directly test the proposed defect.
4. **Gold proposal:** State one primary mechanism if supported, otherwise preserve multiple mechanisms or mark unscorable. Cite exact source paths, line spans, commit SHAs, test IDs and reproduction evidence. Do not collapse explanations that share a symptom.
5. **Lock and adjudicate:** Preserve the complete first review. The adjudicator may add a separate rationale but must not overwrite either initial review.

## Independent reviewer form (complete one copy per reviewer)

### Reviewer declaration
- Reviewer code:
- Date/time (UTC):
- Relevant technical competence and experience:
- Conflict-of-interest screen completed: YES / NO
- Prior contribution to NumPyro, issue #1916, PR #1918, reproduction, or packet construction:
- Prior access to another reviewer's form:
- Consent to preserve an auditable technical review:

### A. Issue reproduction alignment
- Does issue #1916 describe one reproducible defect or multiple defects?
- Do the AIES and ESS selectors exercise the same underlying defect?
- Are the selectors two test variants of one case, rather than two independent cases?
- What exact observations support your answers?

### B. Buggy-base mechanism (do not inspect the fix before locking this section)
- Write the most likely causal chain in your own words:
- Exact source paths, line spans and immutable commit SHA:
- Which state field carries the key at each transition?
- What is the expected shape at each transition?
- Which exact call fails, and why?

### C. Competing mechanisms
For each candidate explanation, select SUPPORTED / PLAUSIBLE / EXCLUDED / UNRESOLVED and explain:
- Caller supplied an invalid PRNG key or used an unsupported public API lifecycle.
- EnsembleSampler itself should support a batched key at the failing split call.
- MCMC.run warmup-state handoff replaces a sampler-state scalar key with a per-chain key array.
- JAX PRNG API/version incompatibility.
- Another explanation (describe).

### D. Fix/test relationship
- Exact patch behavior:
- Does the patch address the mechanism identified above?
- Do both AIES and ESS selectors fail on the exact buggy base?
- Do both pass on the exact fixed merge under the same environment?
- Are any collection, import, dependency or fixture errors mistaken for defect failures?

### E. Proposed technical gold
- Primary mechanism:
- Necessary causal conditions:
- Competing explanations retained:
- Evidence that excludes each rejected explanation:
- What remains unknown:
- Is one root cause sufficiently supported? YES / NO / UNCLEAR

### F. Independence and role boundary
- Have you seen the proposed gold statement or AI advisory note? YES / NO
- Have you constructed or reviewed E1/E2/E3 packets? YES / NO
- Are you eligible for Panel B? The default answer for a source-aware Panel A reviewer is NO.
- Signature/reviewer code:
- Timestamp:
- Hash of this completed form (filled by custodian after receipt):

## Adjudicator record (separate person; do not merge with initial reviews)

- Reviewer A record hash:
- Reviewer B record hash:
- Main disagreements:
- Resolution and evidence:
- Final technical gold statement or unresolved status:
- Adjudicator signature/code:
- Timestamp:
- Hash of adjudication record:

## Current state

No Panel A reviewers or adjudicator are recorded as appointed in this file. No human technical gold adjudication has been completed. This form is preparation only; it does not accept NumPyro #1916, establish E1 sufficiency, or authorize model loading/inference/fine-tuning.
