# Data Collection and Assessment Protocol

Candidate evidence and scientific assessment are separate records.

## IC1-IC7
IC1 real public bug.
IC2 independently verifiable identifier and provenance.
IC3 independently identifiable root cause.
IC4 independently verifiable fixing revision or commit.
IC5 meaningful cross-component relationship.
IC6 relationship representable as CCDG.
IC7 controlled Standard versus CCDG comparison is possible.

A pilot case requires IC1-IC7 all pass, dependency strength strong/moderate, and CCDG suitability strong/moderate.

Assessment must not use model output as ground truth. Candidate records must not be altered to make them eligible.

Contamination risk is recorded separately as low/medium/high/unknown. Unknown is permitted when no exposure audit exists.

Assessment does not automatically move candidates into pilot/main/validation. `eligible_for_pilot` is a deterministic structural eligibility decision. `eligible_for_main` additionally requires a resolved contamination-risk label; it does not by itself add a case to the frozen confirmatory benchmark. Main-benchmark inclusion is controlled by the frozen benchmark manifest.

Do not invent URLs, revisions, root causes, fixes, dependencies, or model-exposure claims.
