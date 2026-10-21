# Literature supplement and originality checkpoint (2026-10-21)

## Scope and status

This is a targeted extension of the existing literature review, not a systematic review or PRISMA search. Searches on 21 October 2026 covered LLM abstention/answerability, evidence sufficiency, code-generation abstention, code prediction deferral, software fault localization, and repair hallucination. The search-engine result list is not a complete corpus, and the listed work was checked at title/abstract or publisher-page level. Full-text and citation-chain screening remains open.

## Relevant adjacent work

| Work | Why it matters | Consequence for this project |
|---|---|---|
| Kirichenko et al. (2025), *AbstentionBench* — https://arxiv.org/abs/2506.09038 | Broad benchmark of unanswerable/underspecified prompts across multiple datasets. | General abstention is not a new research question. |
| Madhusudhan et al. (2025), *Do LLMs Know When to NOT Answer?* — https://aclanthology.org/2025.coling-main.627/ | Black-box abstention evaluation with answerable and unanswerable questions. | Answer quality and appropriate abstention must be measured together. |
| Oehri et al. (2025), *Trusted Uncertainty in Large Language Models (UniCR)* — https://arxiv.org/abs/2509.01455 | Calibrated, risk-aware refusal from multiple uncertainty signals; includes code-generation settings. | A prompt-only abstention study may be a weak contribution without strong task-specific ground truth. |
| Sharma & David (2025), *Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation* — https://arxiv.org/abs/2502.11620 | Relates uncertainty estimation to correctness in generated code and discusses abstention. | “Abstention for code” is already studied; distinguish diagnosis from code generation. |
| Rathnasuriya & Yang (ICSE 2026 NIER), *When to Answer and When to Defer* — https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-When-to-Defer-A-Decision-Framework-for-Reliable-Code-Predictions | Directly discusses calibrated code predictions, deferral, and external validation. | Do not claim that answer/defer behavior for code predictions is new. |
| Zhou et al. (2026), *Task Abstention for Large Language Models in Code Generation* — https://arxiv.org/abs/2605.17029 | Uses execution-based consistency and calibrated abstention for code-generation tasks. | Keep our task specific to root-cause diagnosis rather than generated-code correctness. |
| Zhang & Wu (2026), *Do LLMs Know When Evidence is Insufficient?* — https://www.techscience.com/cmc/v89n1/68467 | Evaluates abstention across evidence-sufficiency levels in RAG. | The evidence-level manipulation itself is not novel; the potential distinction is independently validated software bugs with source/test/fix ground truth. |
| Zhai et al. (ACL Findings 2026), *Abstain-R1* — https://aclanthology.org/2026.findings-acl.985/ | Trains a 3B model for abstention and post-refusal clarification. | “Can a small model abstain and request missing evidence?” is not enough as an originality claim. |
| Rathnasuriya & Yang (2026) plus Xiao et al. (2025), *Large Language Models for Fault Localization: An Empirical Study* — https://arxiv.org/abs/2510.20521 | Code prediction and fault-localization evaluation already exist. | Ground truth and task definition must clearly separate root-cause explanation from line-level localization. |
| Cai et al. (2026), *Better Understanding, Better Fixes?* — https://arxiv.org/abs/2609.04909 | Studies hallucination in intermediate and final artifacts of automated program repair. | Evidence grounding in software debugging is a close neighbour and needs full-text comparison. |
| Kalai et al. (Nature 2026), *Evaluating large language models for accuracy incentivizes hallucinations* — https://doi.org/10.1038/s41586-026-10549-w | Examines how evaluation incentives affect hallucination and abstention. | Avoid a rubric that rewards refusal unconditionally; measure both unsupported answers and lost answer coverage. |

## Search trail

Queries used on 21 October 2026 included:
- “large language models selective prediction abstention benchmark answerability calibration evidence insufficiency”
- “LLM abstention software bug localization root cause diagnosis uncertainty”
- “large language model answer abstention code debugging root cause analysis”
- “evidence sufficiency benchmark code generation”
- “Task Abstention for Large Language Models in Code Generation”
- “When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions”
- “LLM fault localization empirical study uncertainty hallucination”
- “abstention code generation uncertainty calibration”

This is a repeatable query log, not an exhaustive database search. Search-ranking effects, title/abstract-only screening, missing full texts and unsearched citation networks remain limitations.

## Updated originality decision

**Originality is not established; risk is substantial.** The defensible candidate contribution is narrower: independently verified real-world software-bug root causes; the same target regression test failing on the buggy revision and passing on the fixed revision; preconstructed and human-reviewed evidence levels; and separate outcome measures for correctness versus whether the diagnosis is supported by the evidence actually shown to the model. The study also measures the cost of selective abstention on answer coverage and sufficient-evidence cases.

This is a *candidate contribution*, not a claim of being first or unique. The project should not enter inference until the source/license and test-pair gates, two disjoint human review panels, blind calibration, runtime/prompt/analysis hashes, and pre-registration are complete.