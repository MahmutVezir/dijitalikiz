# SWE-rebench V2 evidence-abstention protocol — v0.1 draft

**Date:** 15 November 2026  
**Status:** Draft engineering/protocol scaffold. Not preregistered. Not legal clearance. Not permission for model loading, generation, upstream testing, fine-tuning, or training.

## 1. Research question

In independently verified software defects, does a policy that may abstain when visible evidence is insufficient (P1) reduce unsupported definitive root-cause diagnoses relative to a policy that requires a diagnosis (P0), while preserving supported answers when evidence is sufficient?

The project measures the distinction between a correct guess and a diagnosis supported by the evidence actually shown. It does not claim to establish model self-awareness.

## 2. Source snapshot and candidate cohort

The leading candidate source is `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`, pinned to Parquet file revision `fb9aa226b2ce37c708ea7732e7b980abacdadb67` and SHA-256 `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.

The prior metadata-only feasibility run observed 6,272 rows and read only the safe columns required for candidate selection. It produced 96 primary candidates, 17 project-level reserves, and 148 within-project alternatives. However, that cohort was screened using a UTC assumption for timezone-naive `created_at` strings that is not established by the source schema lineage. Those CSV/manifest hashes identify historical outputs only; the cohort is quarantined and must not be used for confirmatory sampling until date provenance is resolved and a new versioned cohort is generated. The previous primary CSV SHA-256 is `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`; its historical manifest SHA-256 is `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`.

A fail-closed rerun against the exact pinned Parquet snapshot (GitHub Actions run 43726530902, 15 November 2026) observed all 6,272 `created_at` values as timezone-naive strings. It assigned UTC to 0 rows, admitted 0 rows to the date-eligible pool, and skipped cohort generation. This confirms the ambiguity affects the entire snapshot; it does not prove that the original upstream timezone was non-UTC. Exact timestamp reconciliation remains open.

These are candidate rows, not accepted cases. Project-level reserves and within-project alternatives do not count as extra independent cases until a documented selection rule and project-independence decision apply. A repo rename, fork, mirror, shared upstream, duplicate issue, or common root-cause family can invalidate naive repository-level independence.

The dataset card's CC-BY-4.0 declaration does not relicense source code in the underlying repositories. Exact-base license files, changed-file provenance, third-party notices, and reuse obligations remain open per selected case. A separate timestamp-semantics audit found that the filtered dataset card/Parquet schema describe `created_at` as a string, while the embedded upstream dataset card describes it as `int64` Unix milliseconds. The reviewed filtered-dataset generation excerpt does not demonstrate a `created_at` conversion. Naive string values carry no timezone offset, so the former UTC assumption is unsupported. The metadata auditor now rejects naive dates by default; the historical 96-row cohort is quarantined pending authoritative reconciliation and a fresh cohort build.

## 2A. Timestamp provenance and cohort quarantine

The immutable Parquet file is pinned, but immutability alone does not establish the semantic timezone of a timestamp field. The filtered dataset's published schema declares `created_at` as a string; the embedded upstream card describes it as `int64` Unix milliseconds. The reviewed filter-generation excerpt filters and maps other fields but does not demonstrate how `created_at` is serialized. A naive value such as `2021-06-22 22:21:33` cannot be assigned UTC without independent evidence.

Operational rule: explicit timezone-bearing ISO timestamps may be normalized to UTC; numeric timestamps may be interpreted as Unix milliseconds only when the exact source schema/unit is verified; timezone-naive strings/datetimes are excluded from candidate screening by default. The historical `assume_utc_historical_only` parser mode is solely for reproducing the old feasibility output and is not valid for confirmatory cohort construction. The previous 96/17/148 cohort output is retained as a historical audit artifact, not a current eligible cohort. A new cohort must be generated under a versioned snapshot after resolving this discrepancy against the authoritative source record (preferably the exact GitHub PR/issue `created_at` field) and then all hashes must be regenerated.

Detailed evidence and decision log: `SWE_REBENCH_V2_TIMESTAMP_SEMANTICS_AUDIT_2026-11-15.md`. The full-snapshot fail-closed result is retained there, with artifact ID `14166229237`.

## 3. Case acceptance

No row is accepted automatically. Before a case enters the new SWE-rebench registry it must pass:

1. Exact dataset row, immutable repository base commit, PR/base relationship, issue/task scope, and fork/ancestry checks.
2. Exact base and changed-file license/provenance review; ambiguous rights remain excluded.
3. Reproducible target test showing the intended failure at the pinned base and the same target passing at the verified fixed state, with matched runtime and raw logs.
4. Two independent Panel A ground-truth reviews of the causal mechanism, with preserved initial decisions and adjudication.
5. Three evidence packets constructed before model output and independently reviewed by a disjoint Panel B.
6. Leakage and prior-exposure audit. Any candidate previously used to debug or calibrate the screening/runner pipeline, or opened for target-test troubleshooting before a prospective case-validation assignment, is permanently excluded regardless of the observed outcome. A planned technical reproduction is a separate protocol-assigned activity: the designated technical validator and packet preparer may inspect restricted source material, but their identities and access are logged; they cannot serve on blinded Panel B or as the confirmatory analyst. Panel A may inspect source/fix material to establish gold truth, but is likewise disjoint from Panel B. The confirmatory analyst must not have seen the gold cause or fix. Every source-exposed person is listed in the case record. A case with prior pipeline-debug exposure is ineligible even if its technical results look favorable.
7. Complete hashes, review records, and a case-level acceptance decision.
8. An independent external auditor, disjoint from Panel A, Panel B, the confirmatory analyst, technical/legal reviewers, packet preparer, and any adjudicator, reviews artifact authenticity and the consistency of the legal, reproduction, gold-standard, and evidence-tier records. This audit occurs only after Panel B ratings are locked. The auditor is listed among source-exposed persons and cannot serve as the confirmatory analyst or on Panel B.

The case acceptance validator now requires a separate external-audit attestation after Panel B lock before a record can count as a structurally complete confirmatory case. It checks role separation and the explicit prior-debug exclusion, but it cannot authenticate the auditor, open or hash-check referenced artifacts, or prove that access restrictions were observed. Passing this gate is not itself independent audit evidence; the attestation and every referenced artifact still require external verification.

The separate historical BugsInPy registry is not reused or modified for this new source.

## 4. Evidence levels and packet contract

For each case, the model must receive three nested evidence packets:

- E3 is a proper subset of E2.
- E2 is a proper subset of E1.
- A repeated evidence ID must identify exactly the same kind, content, and source snapshot across levels.
- E2 and E1 each add at least one existing, provenance-backed evidence item.
- No fabricated, contradictory, rewritten, or silently truncated evidence may be used to force levels.

The current operational proposal defines levels against a pre-registered set of at least three plausible causal mechanisms. Panel B records which mechanisms remain possible or are excluded by specific visible evidence. E1 leaves only the true mechanism after blinded ratings are locked; E2 removes at least one alternative but leaves at least two mechanisms; E3 removes none. Cases unable to support all three defensible levels are excluded from this three-level confirmatory design.

The outer packet-set wrapper carries E1/E2/E3 keys and is used only for pre-inference structural validation. It must not be passed to the model. The prompt builder validates the packet-set hash and selects exactly one inner packet. The model sees only evidence item IDs, kinds, and visible contents. It does not see the case/project identity, packet ID, E-level label, policy label, source hashes, gold root cause, patch, fixed commit, test patch, PR description, issue/PR identifiers, or hidden quality labels.

Structural validation proves only hash/integrity and set relationships. It does not prove that the evidence entails a causal claim or that a level is semantically adequate.

## 5. Conditions and response contract

The same model revision, tokenizer revision, system instruction, output schema, visible packet, generation settings, and token budget are used in both policies. Only the policy instruction differs.

- P0 asks for the single most likely diagnosis and does not permit abstention.
- P1 asks for a diagnosis only when visible evidence distinguishes it from plausible alternatives; otherwise it asks for explicit abstention and discriminating missing evidence.

The common output schema contains `decision`, `root_cause`, `evidence_refs`, `rationale`, `alternative_hypotheses`, and `missing_evidence`. A diagnosis requires a non-empty root cause and at least one citation. An abstention requires an empty root cause.

JSON validity, reference validity, semantic evidence support, and policy compliance are separate fields. A valid reference is not proof of entailment. An unknown ID is flagged while the observed decision and root-cause text remain unchanged. Raw output is never repaired, retried, or silently converted to abstention.

The new contract code builds blinded prompts and audits supplied raw responses only. It contains no model loader or generation function.

## 6. Outcomes and analysis

The primary outcome is the E3 case-level binary rate of unsupported definitive diagnosis. Human reviewers score support against the visible packet, not the hidden gold answer. A correct guess can still be unsupported.

The primary paired contrast is P1 minus P0 using two-sided exact McNemar, paired risk difference, and a prespecified 95% interval. The complete-pair denominator includes cases with a final scorable 0/1 adjudication under both policies. Invalid/unscorable outputs are retained, counted, and reported separately; a conservative sensitivity analysis treats invalid E3 outputs as unsafe without altering the primary adjudicated data.

Root-cause correctness, evidence support, abstention rate, coverage, policy compliance, citation validity, missing-evidence usefulness, invalid output rate, and reviewer agreement are reported separately. P0 abstention is an observed policy violation, not a diagnosis. P1 compliance cannot be inferred by the parser because its appropriateness depends on evidence sufficiency.

## 7. Model and runtime

Candidate model: `Qwen/Qwen2.5-3B-Instruct`, immutable revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`. Exact revision license review is pending. Runtime load verification has not been performed. Draft deterministic settings are recorded in the manifest but are not frozen.

The primary comparison does not fine-tune model weights. A training change would confound the prompt-policy comparison and requires a separate research question and protocol.

## 8. Sample and stopping rules

Target: 80 accepted independent defects. Confirmatory minimum: 60 defects across at least 8 genuinely independent upstream projects. Each defect contributes six repeated policy/evidence cells; repeated generations or variants do not increase the independent case count.

If the exact licenses, valid test pairs, independent ground truth, evidence tiers, exposure checks, review calibration, sample minimum, runtime, preregistration, or frozen hashes remain open, no model inference is allowed. If the final sample does not meet the minimum, report a feasibility/exploratory study; do not relax case eligibility after seeing results.

## 9. Current state

- New SWE-rebench case registry: empty.
- Accepted independent cases/projects: 0/0.
- Panel A and Panel B approvals: pending.
- Exact selected-source licenses: incomplete.
- Model exact-revision license and runtime: pending.
- Protocol hashes and external preregistration: not frozen/not registered.
- Model load, generation, fine-tuning, and training: not performed.
- Inference authorization: false.

This document is a versioned draft for review. It does not close any scientific, legal, human-review, or execution gate.
