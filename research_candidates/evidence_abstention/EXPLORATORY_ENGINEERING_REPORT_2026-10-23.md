# Exploratory Engineering Report: Evidence-Aware Abstention Prototype

**Report status:** Exploratory engineering report; not a confirmatory efficacy study  
**As-of date:** 23 October 2026  
**Project:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Repository:** `MahmutVezir/dijitalikiz`  
**Candidate model:** `Qwen/Qwen2.5-3B-Instruct`, pinned revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`

## Abstract

This project develops a fail-closed prototype for a language model that should abstain when the available evidence is insufficient to support a root-cause diagnosis. The software includes a structured generation adapter, an uncertainty-policy interface, an evidence-packet integrity auditor, and a gate intended to block model execution until scientific prerequisites are satisfied.

The confirmatory study has **not** been executed. The accepted case registry is empty, the exact intended model/runtime has not been verified, calibration data and a frozen threshold are absent, the reviewer protocol remains a draft, and a verifiable preregistration has not been recorded. Therefore, no claim that the method reduces hallucinations, improves diagnosis reliability, or provides calibrated uncertainty is supported.

An earlier ten-output Kaggle smoke test is reported only as an engineering diagnostic. It is excluded from all confirmatory analysis because the case had been exposed during pipeline development, the prompt included patch/fixed-test information, and the environment differed from the intended runtime.

## 1. Research question and intended contribution

**Research question:** Can an evidence-aware decision policy reduce unsupported definitive root-cause diagnoses by a language model when the evidence packet is partial, insufficient, or contradictory, without causing an unacceptable increase in unnecessary abstention when evidence is sufficient?

The intended contribution is a reproducible decision pipeline that separates:
1. model-generated diagnosis candidates;
2. evidence-packet integrity checks;
3. uncertainty and disagreement signals;
4. the operational decision to answer or abstain; and
5. blinded human assessment of correctness and evidence support.

A refusal rate alone is not a success metric. The method must be evaluated jointly on unsupported definitive diagnoses, answer coverage, and unnecessary abstention on sufficient evidence.

## 2. Implementation status

Implemented in the repository:
- Qwen candidate-generation adapter with structured-output parsing and integrity checks.
- An uncertainty-policy prototype with generation-score entropy, candidate disagreement, a calibration interface, and Brier/ECE calculation utilities.
- A fail-closed inference gate that checks case registry, frozen artifact hashes, runtime verification, preregistration, calibration, and explicit authorization.
- An evidence-packet structural auditor for packet shape, hashes, evidence identifiers, and citation-reference integrity.
- Synthetic unit tests for software behavior and gate enforcement.
- Blank independent-review forms and a completion-gate plan.

These are engineering components, not evidence of scientific effectiveness. The packet auditor validates structure and citation integrity; semantic claim support remains unassessed unless independently reviewed. Gold root-cause labels and human E1/E2/E3 labels must not enter the model's runtime decision path.

## 3. Intended confirmatory design

The planned design crosses three evidence levels with two policies:
- **E1 — sufficient evidence**
- **E2 — partial evidence**
- **E3 — insufficient evidence**
- **P0 — baseline response policy**
- **P1 — evidence-aware abstention policy**

The minimum planned sample is 60 independently accepted cases from at least eight upstream projects; the target is 80. This corresponds to 360 outputs at N=60 or 480 at N=80, one output per case × evidence level × policy. The primary endpoint is the proportion of E3 cases with an unsupported definitive diagnosis, compared between P0 and P1 using paired analysis. Risk difference, an exact two-sided McNemar test, and a confidence interval are planned. Answer coverage and E1 unnecessary abstention must also be reported.

This is a planned design, not a completed preregistration. The final protocol must be frozen and independently verifiable before confirmatory generation.

## 4. Current dataset and human-review status

As of this report:
- Accepted confirmatory cases: **0**
- Accepted upstream projects: **0**
- Formal confirmatory model outputs: **0**
- Independent root-cause adjudications completed for accepted cases: **0**
- Completed disjoint evidence-sufficiency reviews: **0**

A technically observed buggy-test failure and fixed-test pass is not sufficient by itself to accept a case. Each accepted case requires source and license review, provenance and exposure checks, verified test-pair behavior, hashes and runtime metadata, two independent root-cause reviewers, and a separate disjoint pair of blinded evidence-sufficiency reviewers. The review forms currently in the repository are blank templates, not completed assessments.

Cases exposed during debugging are permanently excluded from the confirmatory sample regardless of their technical outcome.

## 5. Engineering smoke test — excluded from confirmatory analysis

A prior Kaggle smoke run generated ten outputs on one previously exposed case, with five outputs per prompt policy. Its audit records:
- P0: 5/5 outputs were diagnoses; 0/5 were explicit abstentions; 0/5 matched the provisional automated rubric.
- P1: 5/5 outputs were diagnoses; 0/5 were explicit abstentions; 0/5 matched the provisional automated rubric.
- The model self-reported confidence of 0.95; this value was not calibrated and must not be interpreted as a probability of correctness.

These counts are descriptive of that smoke run only. They are not a valid estimate of the policy effect, and no inferential test or confidence interval is reported. The case was exposed during pipeline development; the prompt included patch and successful-test information; and the observed environment (Python 3.13.15, PyTorch 2.11.0+cu128, Transformers 4.48.3) differed from the proposed locked environment (Python 3.11.9, PyTorch 2.2.1, Transformers 4.43.2, Accelerate 0.33.0). The smoke outputs are excluded from the confirmatory sample and must not be used to select thresholds.

## 6. Runtime, calibration, and preregistration

The intended exact model/tokenizer load has not been verified in the locked CUDA environment. No generation-free checkpoint-load artifact has been independently inspected and accepted. Calibration labels and a frozen threshold are absent. The preregistration status remains draft and no verifiable registry URI is recorded. Formal inference remains disabled.

The intended next steps are:
1. verify the exact locked runtime and model/tokenizer revision without generating an answer;
2. independently validate a sufficient/partial/missing/contradictory evidence decision set;
3. obtain independent, disjoint human review of eligible cases and evidence packets;
4. obtain a separate calibration set and freeze the decision threshold before confirmatory outputs;
5. freeze and hash the protocol, register it, and obtain explicit authorization;
6. only then execute the preregistered design and conduct the planned analysis.

If these requirements cannot be completed before the competition deadline, the work must be described as a prototype/feasibility study and not as confirmed evidence that hallucinations have been reduced.

## 7. Validity threats and limitations

- **Public-bug contamination:** public source code and issue histories may have appeared in model training data.
- **Case-selection and project clustering:** cases from the same upstream project may not be independent.
- **Semantic measurement:** structural citation validity does not prove that a cited item supports a causal claim.
- **Confidence interpretation:** generation-score entropy and self-reported confidence are not automatically calibrated epistemic uncertainty.
- **Abstention trade-off:** a policy can lower unsupported diagnoses merely by refusing more often; coverage and unnecessary abstention are required companion outcomes.
- **Human judgment:** independent reviewer training, blinding, adjudication, and agreement statistics are necessary.
- **Runtime reproducibility:** model and library versions must match the frozen runtime before formal inference.

## 8. Reproducibility and integrity

The repository contains the implementation, test scaffolding, candidate runtime lock, manifest, case registry, rubric, review forms, and completion-gate plan. The live manifest intentionally sets `inference_allowed=false`, has no accepted case IDs, and has empty frozen-artifact hashes. This is a protective state, not a successful experimental result.

The exploratory smoke artifact SHA-256 recorded in its audit is:
`f35f33029b0a42610e2d2ad2bfb6cedc90f2f9d7e0b14e632787872ae2a2e10d`.

The existing CI test results demonstrate software checks only. They do not establish that the model abstains appropriately or that the proposed method improves reliability.

## 9. Conclusion

The project has a working research-software scaffold and an explicit fail-closed protocol, but the scientific experiment is **not complete**. The evidence currently available does not establish reduced hallucination, calibrated uncertainty, or a causal benefit of the abstention policy. The ten-output smoke run is excluded from confirmatory analysis and did not show abstention in either condition. The next decisive milestones are independent case/evidence review, exact-runtime verification, calibration, verifiable preregistration, and authorized confirmatory execution.

**Permitted conclusion:** an evidence-aware abstention prototype and its validation infrastructure have been implemented; empirical efficacy remains unmeasured.
