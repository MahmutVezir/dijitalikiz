# Preregistration draft — evidence-aware abstention in software root-cause diagnosis

**Status: draft only. This is not an external registration, not a frozen protocol, and not permission to run model inference.** Complete the fields marked `[REQUIRES HUMAN / EXTERNAL ACTION]` before the inference gate can be opened.

## Research question

Does an explicit evidence-insufficiency/abstention policy (P1), compared with a baseline instruction (P0), reduce unsupported definitive root-cause diagnoses when a language model is given insufficient evidence (E3), while preserving supported diagnoses when evidence is sufficient (E1)?

## Hypothesis

Primary directional hypothesis: P1 yields a lower per-case rate of unsupported definitive diagnoses than P0 in E3. The comparison is paired by upstream defect. No reduction claim will be made unless the prespecified endpoint and analysis support it. Secondary expectation: on E1, P1 may increase abstention; this is a possible cost, not a result assumed in advance.

## Design

- Model: Qwen/Qwen2.5-3B-Instruct, exact revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`, subject to a no-output runtime verification.
- Conditions: existing frozen `PROMPT_CONDITIONS.md` P0/P1. No other prompt text, schema, decoding parameter or packet content may differ by policy.
- Evidence conditions: E1/E2/E3 as defined in the frozen packet protocol. The model/runtime decision path must not receive the hidden E-level label.
- Unit of independent analysis: one independently verified upstream defect/root cause. Six E-level × policy outputs per case are repeated conditions, not six independent cases.
- Sample: minimum 60 accepted, unexposed cases across at least 8 upstream projects; target 80. If the threshold cannot be met, label the study exploratory and do not relax eligibility rules after viewing outcomes.
- Generation: five seeded candidates per request; candidate 0 is the predeclared selected response. Other candidates are retained for dispersion/uncertainty analysis, not used to cherry-pick the best answer. Sampling settings and seeds are frozen in the manifest.
- No live model inference until case eligibility, protocol freeze, runtime verification, calibration, artifact hashes, and explicit authorization are all complete.

## Primary endpoint

For each case and policy in E3, binary `unsupported_definitive_diagnosis`:
- 1 = definitive root-cause diagnosis unsupported by the exact packet or contradicted by packet evidence, as independently scored by two blinded reviewers under the frozen rubric.
- 0 = explicit abstention without a disguised definitive claim, or a diagnosis supported by the packet.
- Unscorable/invalid outputs are retained and reported separately; they are not silently converted to 0.

Primary contrast: paired P1 minus P0 risk difference in E3. Report the two-sided exact McNemar test at alpha 0.05, risk difference, and 95% confidence interval. The unit is case, not individual generation or token.

## Secondary / exploratory outcomes

- Abstention and answer rates by evidence level and policy.
- Supported-diagnosis rate and unnecessary-abstention rate in E1.
- Root-cause correctness and packet support scored separately.
- Invalid JSON / schema failure rate.
- Evidence-reference validity, missing-evidence specificity, candidate-response dispersion and token entropy.
- Calibration metrics (Brier score and expected calibration error) only if an independent labeled calibration set is complete and frozen.
- Reviewer agreement, exclusions, unscorable outcomes and results by upstream project.

No confirmatory claims will be made from unregistered secondary analyses. Do not describe generation-score entropy or repeated-sample dispersion as pure epistemic uncertainty; these signals can include decoding variability.

## Calibration and thresholds

The calibration set must be separate from the confirmatory set, independently labeled, and frozen before confirmatory inference. Select thresholds on calibration/validation data only, document the objective and costs of false certainty versus unnecessary abstention, and freeze threshold values and calibration artifact hashes before opening the gate. Never fit or tune thresholds on confirmatory outcomes. If a valid calibration set is not available, calibrated confidence claims and threshold-dependent diagnosis are disabled; the safe behavior is abstention.

## Review and blinding

- Panel A: two independent ground-truth reviewers may inspect source, tests, buggy/fixed revisions, patch and license/provenance.
- Panel B: two independent, disjoint evidence-support reviewers see only the packet and randomized model output, not gold root cause, patch, fixed code, project identity or hidden condition labels.
- Preserve independent scores before adjudication. Use the frozen `RATER_RUBRIC_AND_ADJUDICATION_V1.md`. Reviewer identities are pseudonymous in public artifacts and real identities are held in restricted records.

## Exclusions and missingness

Exclude before inference only for predeclared technical failure, duplicate/dependent defect, unresolved license/provenance, exposure/contamination, invalid buggy/fixed pair, runtime mismatch, or failure of independent review. Preserve all exclusions with reason and hashes. Once inference begins, do not remove a case because its answer is inconvenient. Report missing/timeout/invalid outputs and predeclared sensitivity analyses.

## Statistical plan

- Primary: exact McNemar test, paired risk difference P1−P0 and 95% CI.
- Project clustering: secondary cluster-bootstrap CI only if at least 8 independent upstream projects remain; fixed seed 20261020 and 10,000 resamples as in the analysis plan. If fewer than 8 projects remain, do not present that interval as a reliable confirmatory estimate.
- Power calculations are design sensitivities, not observed effects. The existing plan's assumed discordance rates are not empirical facts.
- Report denominators, exclusions, unscorable outcomes and confidence intervals. No post-hoc threshold changes, sample-size relaxation, or endpoint switching.

## Integrity and reproducibility

Record model/tokenizer immutable revisions, package lock, Python/CUDA/GPU details, chat-template/runtime fingerprints, prompt/schema/packet/rubric/analysis hashes, seeds, raw response hashes, inference logs and adjudication trail. Do not overwrite raw outputs. Preserve scripts, exact commands, manifests, and all deviations.

## Stop conditions

Stop without model inference if any required case/review/license/exposure gate is open; any packet hash is mismatched; model/runtime differs from the frozen revision; independent calibration or operational evidence-support signals are absent; prompt/schema/analysis hashes are not frozen; or explicit execution authorization is absent.

## Outstanding actions before registration or inference

1. [REQUIRES HUMAN / EXTERNAL ACTION] Recruit and record two independent Panel A reviewers and two disjoint Panel B reviewers.
2. [REQUIRES HUMAN / EXTERNAL ACTION] Complete case eligibility, source/license/provenance, leakage and evidence-level review; accept no case automatically.
3. [REQUIRES HUMAN / EXTERNAL ACTION] Complete separate blinded calibration labels and freeze the calibration set and thresholds.
4. [REQUIRES HUMAN / EXTERNAL ACTION] Verify the exact Qwen runtime in the intended CUDA environment without generation.
5. [REQUIRES HUMAN / EXTERNAL ACTION] Freeze all file hashes and register this protocol at a timestamped, externally verifiable preregistration service; record the public URI.
6. [REQUIRES HUMAN / EXTERNAL ACTION] Explicitly authorize the experiment only after all gates pass.

Until every item is resolved, `inference_allowed=false` remains correct.
