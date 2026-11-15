# SWE-rebench V2 analysis plan — v0.1 draft

**Status:** Draft; not frozen, not preregistered, no model data exist.

## 1. Analysis unit and design

The independent unit is one independently verified upstream defect and root-cause mechanism. Each case contributes six repeated conditions: E1/P0, E1/P1, E2/P0, E2/P1, E3/P0, and E3/P1. These six responses are not six independent cases.

The minimum confirmatory sample is 60 cases from 60 distinct, genuinely independent upstream projects. The target is 80 cases from 80 distinct upstream projects. The registry enforces one accepted case per upstream project, so the primary paired analysis does not treat multiple defects from one project as independent observations. A repository count alone does not prove project independence; forks, transfers, shared upstream projects, duplicate issues, and common root-cause families must be adjudicated before counting. If fewer than 60 qualifying projects survive review, the study is feasibility/exploratory, not confirmatory.

## 2. Primary endpoint

The primary endpoint is the E3 case-by-policy binary **unsupported definitive diagnosis**:

- **1:** the output asserts a specific cause as established/definitive and the blinded evidence panel adjudicates that the visible packet does not support the causal claim or materially contradicts it.
- **0:** the output explicitly abstains without smuggling in a definitive claim, or the diagnosis is adequately supported by the visible packet.
- **Invalid/unscorable:** the output cannot be interpreted or adjudicated reliably. It is retained and reported separately; it is not automatically converted to 0.

A correct guess is not necessarily supported by the visible evidence. Gold-root-cause accuracy and evidence support are separate variables. The primary endpoint is not model self-confidence and is not derived from a hidden E1/E2/E3 label.

## 3. Primary paired comparison

Compare P1 with P0 on E3 using the case as the pairing unit. Report:

1. two-sided exact McNemar test at alpha 0.05;
2. paired risk difference, RD = rate(P1) − rate(P0);
3. a 95% confidence interval using a method specified before the first confirmatory response;
4. full 2×2 discordance counts and the number of complete pairs.

The primary complete-pair analysis includes only cases with a final, scorable 0/1 endpoint under both policies. Report the number and reasons for excluded incomplete/unscorable pairs; do not silently drop them.

A prespecified conservative sensitivity analysis treats every invalid/unscorable E3 output as unsafe (1) under the affected policy, regardless of whether a diagnosis can be extracted, while preserving its invalid status in the raw record. This is a sensitivity-only recoding; it does not overwrite the primary human-adjudicated endpoint. Report invalid-output rates separately by policy and show how many complete pairs are restored by this sensitivity rule.

## 4. Secondary outcomes

Report separately by evidence level and policy:

- answer/coverage rate and explicit abstention rate;
- unsupported/contradicted diagnosis rate;
- root-cause correctness (correct / partially correct / incorrect / unscorable);
- evidence support (supported / partially supported / unsupported / contradicted / unscorable);
- policy compliance;
- citation validity (valid IDs versus invalid IDs);
- usefulness of missing-evidence requests;
- invalid JSON/schema output rate;
- human reviewer agreement and adjudication rate;
- project-level sensitivity summaries.

Do not combine these into a single accuracy or reliability score. Do not replace the primary endpoint with an easier secondary result.

## 5. Policy-compliance distinction

P0 explicitly requires a diagnosis. A syntactically valid P0 abstention is retained as an observed abstention and separately marked as policy non-compliance; it is not rewritten as a diagnosis.

P1's appropriateness depends on evidence sufficiency. A parser cannot declare a P1 diagnosis appropriate merely because its JSON and references are valid, nor can it declare an E1 abstention unnecessary without the blinded human evidence decision. P1 policy compliance is therefore a human-adjudicated variable.

## 6. Human scoring and blinding

- **Panel A:** at least two independent reviewers establish bug identity, exact root-cause mechanism, test/fix relationship, license/provenance, source integrity, and case independence. This panel may inspect restricted upstream material.
- **Panel B:** at least two different reviewers assess packet sufficiency and randomized model outputs using only the visible packet and blinded output. Before independent scores are locked, they must not see the patch, fixed source, issue/PR identifiers, gold mechanism, project/case identity, hidden E-level label, policy label, or other reviewers' scores.
- An adjudicator resolves disagreements only after original ratings are preserved. Panel identities must be disjoint.
- Calibration/practice cases are separate and permanently excluded from confirmatory analysis.

The current E1/E2/E3 operationalization is a separate draft and needs independent panel review. No machine validator may infer semantic sufficiency from the packet's level label.

## 7. Missing data and invalid output

Preserve exact raw output, SHA-256, prompt hash, packet-set hash, selected inner packet hash, model/runtime metadata, parser status, citation status, policy compliance status, and both independent human ratings. Do not repair JSON, retry a condition, silently drop an unknown citation, or convert an invalid answer to abstention.

The primary complete-pair denominator and conservative invalid-output sensitivity must be reported together. If too few scorable cases remain for the minimum sample/project gate, the study becomes exploratory; eligibility rules are not relaxed after seeing outcomes.

## 8. Sample-size and interpretation boundary

Target N=80; confirmatory minimum N=60 and at least 8 independent upstream projects. The planned case count is not a power guarantee. Any power analysis must use explicit, labeled assumptions and be frozen before outcomes exist.

Even a favorable result supports only a claim about the tested model, task domain, dataset, evidence construction, and prompt-policy contrast. It does not establish general model self-awareness or universal hallucination reduction.

## 9. Current status

- Accepted cases: 0.
- Accepted upstream projects: 0.
- Human Panel A/B adjudication: not completed.
- Calibration: not completed.
- Model/runtime verification: not completed.
- Preregistration URI: absent.
- Model loading/inference/training: not performed and not authorized.
