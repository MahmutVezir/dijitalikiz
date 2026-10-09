# Confirmatory Main Benchmark Selection Specification

## Purpose

Define the confirmatory-case selection procedure before any main-benchmark inference is inspected.

## Inclusion criteria

A case is eligible for the confirmatory benchmark only when all of the following are documented:

1. Real public software defect with a stable public identifier.
2. Primary source and publication date are recorded.
3. Buggy and fixed revisions are independently traceable.
4. The fixing change is attributable to the documented defect.
5. The root cause is independently supported by issue/fix/source evidence.
6. The failure crosses at least two named software components or layers and the dependency can be represented as explicit CCDG edges.
7. The same base evidence can be supplied to both Standard and CCDG conditions without revealing ground truth.
8. No pilot case overlap.
9. Contamination-risk audit has produced a non-unknown risk label.
10. The case assessment records `eligible_for_main=true`.
11. Case provenance and annotations are frozen before main inference.

## Exclusion criteria

Exclude a case when any of the following applies:

- synthetic, reconstructed, or model-generated provenance;
- unresolved or conflicting root-cause evidence;
- missing or unverifiable fix revision;
- component-local defect without a meaningful cross-component dependency;
- CCDG cannot add a materially explicit dependency representation over the same base evidence;
- duplicated issue or duplicate underlying defect;
- unresolved contamination audit;
- pilot case;
- post-inference selection or modification based on model results.

## Independence rule

Independence means independence of benchmark membership from model outputs. A case is not excluded merely because public material may exist; contamination risk is recorded and handled analytically.

Pilot cases are permanently kept in the pilot split for the primary confirmatory analysis. They are not promoted automatically.

## Selection procedure

1. Build a candidate pool from documented public sources.
2. Verify provenance, root cause, fix, and dependency structure.
3. Run the contamination audit.
4. Mark `eligible_for_main` deterministically.
5. Select the final case IDs without consulting model outputs.
6. Record the selected case IDs in `data/benchmark/benchmark_manifest.json`.
7. Determine and record the McNemar power assumptions and resulting target sample size.
8. Set the benchmark manifest to `frozen`.
9. Only after freezing the manifest, execute confirmatory inference.

## Required evidence per case

The final case record must contain:

- source and source URL;
- publication date;
- technology;
- error description;
- `i_base`;
- explicit CCDG nodes/relations;
- ground truth;
- provenance/fix metadata;
- contamination-risk metadata;
- `split="confirmatory"`.

Ground truth is never rendered into either experimental condition.

## Anti-leakage rule

Case selection, CCDG construction, and ground-truth annotation must be completed before the first confirmatory inference. Any change afterward is a protocol deviation and must be documented rather than silently applied.


## State as of 2026-10-09 — frozen manifest and execution provenance

The 16-case confirmatory benchmark has been frozen after validation of the completed 40-record pilot artifact. The frozen manifest records the pilot run ID, artifact ID, artifact SHA-256, and pilot source commit. The confirmatory launch commit is recorded separately.

### Verified pilot gate

- Run ID: `37968099402`; artifact ID: `11634641753`.
- Pilot source commit: `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`.
- Artifact SHA-256: `b12594415894d5cac18442d3bd6c505e843b1a14027272c1afa398a59101aca0`.
- The exported artifact contains 40/40 records, 40 JSONL entries, no parse failures, and a complete internal SHA-256/file-inventory check.
- The old strict complete-diagnostic endpoint yielded zero case-level majority passes in both conditions. This pilot outcome is not the confirmatory result and must not be used to change the case set.

### Frozen case set and scoring amendment

The confirmatory cases remain CLOSURE-4, CLOSURE-6, CLOSURE-14, MATH-305, MATH-326, MATH-358, MATH-377, MATH-392, MATH-393, MATH-405, MATH-631, MATH-859, MATH-924, TIME-1, TIME-12, and MOCKITO-19. The 16 cases were selected independently of model outputs; all pilot cases are excluded. The primary design uses 16 independent cases, two conditions, and seeds 42–46 for 160 records.

The primary endpoint is root-cause correctness with the rubric's predeclared aliases. A scoring-protocol amendment dated 2026-10-09 followed pilot-output diagnostics and is disclosed in manifest metadata. This is not represented as a fully pre-registered decision made before any model output. The final report must describe this procedural limitation, retain the frozen scoring rubric, and avoid post-hoc changes based on confirmatory results.

### Source-commit rule

The pilot source commit is `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`; the confirmatory launch commit is `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`. They are not identical because the manifest and confirmatory runner were frozen after pilot completion. The shared experimental core files—context renderer, models, legacy evaluator, prompt template, system prompt, pilot manifest, and pinned requirements—were checked and have identical blob SHAs across these two commits. Each phase must retain its own source commit and the confirmatory source-bundle checksum.

### Confirmatory run completed — frozen endpoint has a floor effect

GitHub Actions run [#95 / 37976682761](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37976682761) completed successfully for source commit `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`. Artifact ID `11640450681` was downloaded and its ZIP checksum matched `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`. Independent audit of the included manifest found 212/212 files intact and 160/160 unique run records, with zero parse failures.

Under the frozen primary root-cause alias endpoint, Standard passed 0/80 seeds and CCDG passed 0/80; all 16 case-level outcomes were failures under both conditions. The exact two-sided McNemar p-value is 1.00, paired difference 0.00, and the stored 95% paired interval is [-0.1936, 0.1936]. This is a floor-effect outcome, **not** proof of equivalence or proof that CCDG has no effect. The fixed contiguous-phrase matcher did not accept any output alias, so the intended semantic hypothesis remains unresolved by this operationalization.

Full result and limitations: [`docs/CONFIRMATORY_RESULTS_2026-10-09.md`](CONFIRMATORY_RESULTS_2026-10-09.md). Artifact integrity checker: `scripts/audit_confirmatory_artifact.py`. Any semantic review of existing outputs must be exploratory; do not revise the frozen primary score retrospectively.
