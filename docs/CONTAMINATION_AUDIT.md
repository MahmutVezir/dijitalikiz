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
