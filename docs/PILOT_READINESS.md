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

## Execution gate

No case is promoted to data/pilot/.

The current candidate records are provenance/intake records and do not yet contain the complete experimental ResearchCase payload (i_base, explicit CCDG edges, and independently annotated ground truth). Therefore, an assessment-level eligible_for_pilot=true is not treated as permission to run an LLM pilot.

Before the first LLM call, the three eligible candidates must receive complete, independently sourced experiment records and pass schema validation. Ground truth must remain outside both Standard and CCDG model contexts.

## Scientific controls

No LLM inference, fine-tuning, main benchmark, or accuracy claim is made at this stage.
