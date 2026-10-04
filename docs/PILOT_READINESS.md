# Aşama 2.6 — Pilot Readiness

## Status

The source-level fix revisions for the five Apache Commons Math candidates were independently verified against the public apache/commons-math Git history.

Verified fixes:
- MATH-927: 185e3033ef43527a729c9dda5d57ed0537921a27
- MATH-950: 424cbd201ca5969181d68cff99d8b9b77a41cefe
- MATH-938: 73605560b9f0205ac641ec602145756305a41f79
- MATH-949: f83bbc1d68bd457dfccd370afb248126ce031eb6
- MATH-988: d270055e874148a2742604be36ab977eec030fba

## Assessment-level pilot eligibility

- MATH-927: eligible
- MATH-950: eligible
- MATH-988: eligible
- MATH-938: not eligible — cross-component criteria fail
- MATH-949: not eligible — cross-component criteria fail

## Pilot promotion gate

Three eligible cases have now been promoted into data/pilot/ as complete ResearchCase records:

- MATH-927
- MATH-950
- MATH-988

The records contain i_base, explicit CCDG edges, and independently annotated ground truth. The pilot manifest is frozen. Ground truth remains outside both Standard and CCDG model contexts.

No main benchmark case is promoted or executed from these pilot records automatically.

## Scientific controls

- No LLM inference result is currently stored in the repository.
- No pilot accuracy claim is made.
- No fine-tuning is part of the pilot.
- Model, revision, system prompt, user prompt, generation parameters, seeds, evaluator, and pilot cases must not be changed after the first inference.
- Contamination audit completed: MATH-927 and MATH-988 are high-risk public-overlap cases; MATH-950 is medium risk. This is an exposure-risk assessment, not proof of training inclusion.

## Remaining execution gate

Before confirmatory/main benchmarking:

1. Execute the 30 frozen pilot inference runs.
2. Evaluate all 30 records with the frozen evaluator.
3. Inspect parse failures, seed duplication, and condition integrity.
4. Preserve the completed contamination audit and account for its risk labels when selecting/interpreting the main benchmark.
5. Freeze the main benchmark power assumption and independent case set.
