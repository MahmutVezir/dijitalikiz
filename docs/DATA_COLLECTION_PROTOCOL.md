# Data Collection and Assessment Protocol

## Scope

This protocol separates candidate intake from scientific eligibility assessment.

Candidate records are evidence records. They must not be modified merely to make a case eligible.

Assessment records live separately in `data/assessments/` so the candidate evidence schema can remain strict.

## IC1–IC7

A candidate is eligible for the pilot only when all seven criteria pass:

- **IC1:** real public software bug.
- **IC2:** bug identifier and provenance are independently verifiable.
- **IC3:** root cause is reliably identifiable from independent evidence.
- **IC4:** the fixing revision/commit is independently verifiable.
- **IC5:** the fault has a meaningful cross-component relationship.
- **IC6:** that relationship can be represented explicitly as a CCDG.
- **IC7:** Standard versus CCDG can be compared under controlled experimental conditions.

Assessment values are researcher-entered evidence judgments. The software must not infer them from an LLM response.

## Eligibility rule

`eligible_for_pilot` is computed deterministically:

- IC1–IC7 must all be `pass`;
- dependency strength must be `strong` or `moderate`;
- CCDG suitability must be `strong` or `moderate`.

Otherwise the case is not eligible.

## Contamination

Contamination risk is recorded separately as low/medium/high/unknown with a reason. Do not invent evidence of model exposure or training-data membership.

## Split integrity

Assessment does not move cases between candidate, pilot, main, validation, or excluded directories. Split assignment is a later controlled step.

## Prohibited actions during assessment

Do not:
- invent issue URLs, revisions, root causes, fixes, or dependencies;
- use model output as ground truth;
- run the pilot;
- run the main experiment;
- fine-tune a model;
- silently alter candidate evidence;
- convert synthetic examples into real cases.
