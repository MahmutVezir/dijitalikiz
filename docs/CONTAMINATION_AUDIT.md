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

- low: no meaningful public overlap found by the documented audit;
- medium: related public material exists, but exact case exposure is unclear;
- high: exact case/solution appears in a plausible training source;
- unknown: audit could not establish a defensible classification.

## Completed web-index audit — 2026-10-04

The audit was performed against the frozen Qwen2.5-3B-Instruct-GPTQ-Int4 checkpoint family and the three pilot cases. The search is evidence of public exposure, not proof of model training inclusion.

| Case | Searches performed | Public overlap found | Risk |
|---|---|---|---|
| MATH-927 | Exact issue ID/title, GammaDistribution cloning, BitsStreamGenerator, fix revision | Exact Apache JIRA report contains the root cause and fix; an academic thesis also reproduces the exact fix commit and defect description. | high |
| MATH-950 | Exact issue ID/title, RESET_STATE, EventState, AbstractIntegrator, fix revision | No additional indexed training-like copy was found in the executed web search. The original Apache issue remains publicly accessible from the case provenance. | medium |
| MATH-988 | Exact issue ID/title, SubLine.intersection, NullPointerException, fix revision | A publicly indexed research paper reproduces the Defects4J case metadata, affected method, fix description, and exact fix revision. | high |

These risk labels are now the authoritative assessment-level contamination fields for the three pilot cases.

Interpretation:
- MATH-927 and MATH-988 are high-risk contamination cases and should not be used as the sole basis for a strong causal claim about CCDG effectiveness.
- MATH-950 remains medium risk, not low risk, because public provenance exists even though the search did not locate an additional indexed reproduction.
- The frozen model repository identifies the selected checkpoint as a GPTQ-quantized Qwen2.5-3B-Instruct model and points to the Qwen2.5 family; the public model card does not establish that any particular Apache Commons Math case was included in training.
- Therefore the audit does not claim that the model memorized any case. It only establishes varying degrees of public exposure risk.

Sources consulted during this audit included the official Apache JIRA page for MATH-927, the public research literature reproducing the MATH-927 and MATH-988 fix metadata, and the official Hugging Face model card for the frozen model family.

No claim in this document should be interpreted as proof of training-set membership.

## Pre-freeze public-source audit for confirmatory pool — 2026-10-08

A second audit was recorded for the proposed confirmatory pool before any confirmatory inference. The audit used the exact defect identifier, public issue URL, and exact fixing commit for each case. The purpose was to resolve the risk label without consulting model outputs.

All 16 proposed confirmatory cases have high public-exposure risk because their exact defect identifiers and fixing commits are available in the public Defects4J/project ecosystem. This label means that training-data exposure is plausible; it does not establish that the Qwen checkpoint contains the case or memorized its solution.

| Case | Public source/fix anchor | Risk |
|---|---|---|
| CLOSURE-4 | Google Code issue 873; fix efefb736fccc2039b5fb079710b3f2ac82b8c6e4 | high |
| CLOSURE-6 | Google Code issue 635; fix 9f7a353385bf0b93cdaeaa56cc5b1450db790127 | high |
| CLOSURE-14 | Google Code issue 779; fix 4b15b25f400335b6e2820cb690430324748372f9 | high |
| MATH-305 | Apache JIRA MATH-305; fix ef9b639afc3dd8d1c35eab23cc9cb6b3a6a2c858 | high |
| MATH-326 | Apache JIRA MATH-326; fix ce185345fa26d4f96979cbebfbb0e9def817305f | high |
| MATH-358 | Apache JIRA MATH-358; fix 061f50175cf7047856a934f9a827dbe6fd818334 | high |
| MATH-377 | Apache JIRA MATH-377; fix c640932de203b33683679879cdf4b1b637d473d3 | high |
| MATH-393 | Apache JIRA MATH-393; fix d4b02f6a3a90cb468731d6156d571d284bd070b1 | high |
| MATH-405 | Apache JIRA MATH-405; fix 784e4f69ec67d511a0620a2b030688f186ebb959 | high |
| MATH-631 | Apache JIRA MATH-631; fix c0b4954297ce01b64487c09a1dcfcc0124f7053b | high |
| MATH-392 | Apache JIRA MATH-392; fix 30c9e8c111f0e49acb8e9e7f6119230844fe1ee3 | high |
| MATH-859 | Apache JIRA MATH-859; fix 66dece126a7a3130cc79b44e0527b8b5eea41bcc | high |
| MATH-924 | Apache JIRA MATH-924; fix 2836a6f9efcd30effe2f1125d47c38f62f96ed09 | high |
| TIME-1 | Joda-Time issue 93; fix 9a62b06be5d0df8e833ff8583398cca386608cac | high |
| TIME-12 | Joda-Time issue 8; fix 77a6b3a44da7ae4af62e88b4b27eeefec2d768c2 | high |
| MOCKITO-19 | Mockito issue 205; fix 110ffa80070bf54ab8efabdaaa27b193a93d6128 | high |

This audit is intentionally conservative: public availability raises exposure risk rather than serving as a claim of actual contamination.

## Date-basis note

For several historical Apache/Google cases, the issue-creation date was not consistently exposed in the current source record used by the repository. The confirmatory case files therefore record the exact fixing-commit date in the publication_date field and additionally mark the basis as fixed_revision_date. This is a metadata convention, not an assertion that the fix date equals the original issue publication date.

## Selection replacement note — 2026-10-08

MATH-844 was removed from the preselected confirmatory manifest and replaced by MATH-392. The replacement has a clearer cross-component fixing change spanning `AbstractMultipleLinearRegression`, `OLSMultipleLinearRegression`, and `GLSMultipleLinearRegression`. MATH-844 remains in the repository only as a screened candidate and is not part of the 16-case confirmatory set.
