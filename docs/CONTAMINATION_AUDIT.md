# Model Contamination Audit Protocol

## Purpose

Assess whether the frozen model could have encountered the exact benchmark cases, their ground-truth diagnoses, or a substantially equivalent public solution during model training.

This is a risk assessment, not proof that contamination did or did not occur.

## Frozen model

- Model: Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4
- Revision: 68c4276063d1496cdf13d0b8e8221f899bfa77f7

## Audit scope

For each pilot/final case, search at minimum:

- exact issue identifier;
- exact issue title where available;
- distinctive error text;
- distinctive root-cause phrase;
- distinctive fix description;
- fix commit identifier when publicly exposed.

Record:

- query;
- source searched;
- date;
- result;
- interpretation.

Do not modify the benchmark based on whether the model happens to answer correctly.

## Risk labels

- **low**: no meaningful public overlap found by the documented audit;
- **medium**: related public material exists, but exact case exposure is unclear;
- **high**: exact case/solution appears in a plausible training source;
- **unknown**: audit could not establish a defensible classification.

The current repository assessments use **unknown** until this audit is actually performed.

## Reporting

The final report must state the audit limitation explicitly. Absence of evidence is not evidence of absence.

## Completed web-index audit — 2026-10-04

The audit was performed against the frozen Qwen2.5-3B-Instruct-GPTQ-Int4 checkpoint family and the three pilot cases. The search is evidence of public exposure, not proof of model training inclusion.

| Case | Searches performed | Public overlap found | Risk |
|---|---|---|---|
| MATH-927 | Exact issue ID/title, GammaDistribution cloning, BitsStreamGenerator, fix revision | Exact Apache JIRA report contains the root cause and fix; an academic thesis also reproduces the exact fix commit and defect description. | **high** |
| MATH-950 | Exact issue ID/title, RESET_STATE, EventState, AbstractIntegrator, fix revision | No additional indexed training-like copy was found in the executed web search. The original Apache issue remains publicly accessible from the case provenance. | **medium** |
| MATH-988 | Exact issue ID/title, SubLine.intersection, NullPointerException, fix revision | A publicly indexed research paper reproduces the Defects4J case metadata, affected method, fix description, and exact fix revision. | **high** |

Interpretation:
- **MATH-927 and MATH-988 are high-risk contamination cases** and should not be used as the sole basis for a strong causal claim about CCDG effectiveness.
- **MATH-950 remains medium risk**, not low risk, because public provenance exists even though the search did not locate an additional indexed reproduction.
- The frozen model repository identifies the selected checkpoint as a GPTQ-quantized Qwen2.5-3B-Instruct model and points to the Qwen2.5 family; the public model card does not establish that any particular Apache Commons Math case was included in training.
- Therefore the audit does **not** claim that the model memorized any case. It only establishes varying degrees of public exposure risk.

Sources consulted during this audit included the official Apache JIRA page for MATH-927, the public research literature reproducing the MATH-927 and MATH-988 fix metadata, and the official Hugging Face model card for the frozen model family.
