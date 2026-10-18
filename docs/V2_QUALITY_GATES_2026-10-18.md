# Follow-up v2 quality gates

Status: draft only. No model inference authorized.

## 1. Information parity

A, B and C must use the same source description, technology, error description and I_base facts. B expresses every approved dependency edge as prose; C expresses the exact same directed edges as triples. The edge endpoints, directions, relation labels and details must be identical. A must not expose an explicit edge list. System/task prompts, model revision, runtime, tokenizer, chat template, generation settings and output schema must be fixed across arms.

Keep repository/commit identifiers, regression-test names and outcomes, provisional root causes, gold explanations and reviewer notes outside all model contexts. Before inference, validate fact IDs, edge IDs, render hashes, token IDs and context length using the actual tokenizer/chat template; do not use whitespace token estimates or silently truncate a condition. Report B/C token-length differences and review representative renders independently.

## 2. Case admission

A candidate requires exact pre-fix and fixed SHAs, a named regression test with target-specific failure before the fix and pass after it, source evidence for one coherent root cause, a meaningful multi-component dependency path, license/provenance review, duplicate check, and a contamination-risk note. Two reviewers independently assess source and edges; a separate adjudicator resolves disagreements after both reviews are locked. Technical red/green reproduction alone is not admission. The seven calibration cases remain excluded. The six recently screened candidates still need source review/adjudication; the TLS 1.3/Ed25519 candidate remains blocked unless the intended native path is demonstrated.

## 3. Blinded answer scoring

Two independent raters see randomized answer IDs and answer text only. They do not see condition, seed, matcher outcome, provisional gold labels or one another's rating. Labels: correct, partially_correct, incorrect, unscorable. Correct requires a source-supported causal diagnosis; keyword overlap alone is insufficient. Preserve both original ratings and reasons; a separate adjudicator resolves disagreement. Current calibration gate remains at least 0.80 exact agreement and Cohen's kappa >= 0.70; if either fails or kappa is undefined, block inference. Per case-condition, at least 3/5 adjudicated correct answers constitute a pass. Cases—not repeated generations—are the primary unit.

## 4. Student ownership

Before submission, the student must explain in their own words: A/B/C and why C-vs-B is primary; information parity; the historical 0/80 vs 0/80 floor effect and what it does not prove; paired McNemar and why p=1.00 does not prove equivalence; case independence; reviewer/rater/adjudicator roles; sample-size assumptions; contamination and other limitations; and actual AI assistance. The student should trace at least one defect from pinned source through regression test and explain each report claim. An unexplained claim must be corrected or removed, not memorized.

## 5. Freeze prohibition

Do not change the main protocol manifest from draft or enable inference until case IDs and reviews, source/adjudication records, scoring calibration, tokenizer/runtime compatibility, parity tests, randomized schedule, analysis/missingness rules, evidence hashes and student approval are complete. Historical prompts, records, hashes, results and report claims remain immutable.