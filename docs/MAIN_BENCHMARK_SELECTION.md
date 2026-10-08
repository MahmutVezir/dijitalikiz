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


## Current state — 2026-10-08

The repository currently contains a screening pool of 21 candidate records. The confirmatory manifest remains `draft` with zero selected case IDs. Sixteen additional candidates have provisional CCDG/ground-truth annotations, but their contamination risk remains `unknown`; they are therefore not eligible for confirmatory promotion yet.

This is intentional. A large candidate pool is preferable to prematurely freezing a small or contaminated benchmark. The final sample size must be determined from predeclared McNemar discordant-pair assumptions, not from observed model outcomes.

