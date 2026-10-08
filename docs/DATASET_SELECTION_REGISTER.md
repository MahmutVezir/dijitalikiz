# Candidate Selection Register

Updated: 2026-10-08

## Purpose

This register records the research-case pool before confirmatory benchmark freezing. It prevents silent case substitution and makes the selection process reproducible.

## Pool snapshot

Total candidate records: **21**

| Group | Cases | Status |
|---|---|---|
| Frozen pilot / permanently excluded from main | MATH-927, MATH-950, MATH-988 | Pilot |
| Previously screened out | MATH-938, MATH-949 | CCDG/dependency unsuitable |
| Provisional Apache Commons Math candidates | MATH-924, MATH-405, MATH-326, MATH-377, MATH-393, MATH-631, MATH-358, MATH-859, MATH-844, MATH-305 | Screening pool |
| Provisional Joda-Time candidates | TIME-1, TIME-12 | Screening pool |
| Provisional Mockito candidate | MOCKITO-19 | Screening pool |
| Provisional Closure Compiler candidates | CLOSURE-4, CLOSURE-6, CLOSURE-14 | Screening pool |

## Candidate provenance rule

For candidate admission, the repository records:

1. a stable public issue identifier;
2. a primary issue URL;
3. a Defects4J buggy/fixed revision pair or equivalent stable fix provenance;
4. issue/fix evidence URLs;
5. a provisional base-context representation;
6. a provisional CCDG representation;
7. a deterministic assessment record.

A candidate does not become a confirmatory case merely because it has passed this screening stage.

## Why candidates remain provisional

The current additional candidates deliberately carry `contamination_risk="unknown"` and `eligible_for_main=false`. Before benchmark freeze, each selected case must receive a case-specific contamination audit and an independent final review of ground truth and CCDG edges.

This prevents the benchmark from being selected or altered after model outputs are observed.

## Important exclusions

- MATH-927, MATH-950 and MATH-988 are pilot cases and cannot be promoted.
- MATH-938 and MATH-949 were screened out because the current dependency/CCDG assessment did not establish sufficiently strong cross-component structure.
- Duplicate or issue/fix-mismatched Mockito mappings were rejected during mining rather than added as artificial candidates.

## Mining observations

The Apache Commons Math release history explicitly documents several relevant fixes, including MATH-924 (large uncorrelated-observation handling with a diagonal matrix), MATH-405 (Levenberg-Marquardt consistency), MATH-377 (chi-square computation) and MATH-326 (L-infinity vector norm). These entries support provenance screening, not the final experimental result.

For Joda-Time, issue #93 describes a concrete `Partial.with` NPE involving unsupported duration metadata, and issue #8 concerns Gregorian ERA handling during LocalDate/LocalDateTime conversion.

For Mockito, issue #205 documents wrong-field injection with `@InjectMocks`; the corresponding Defects4J fix changes the candidate-filter chain used for property/setter injection.

## Freeze conditions

The final benchmark manifest may be changed to `status="frozen"` only after:

- final case files exist;
- pilot overlap is absent;
- provenance/fix evidence is complete;
- ground truth is independently checked;
- CCDG is independently checked;
- contamination risk is no longer unknown for any selected case;
- power assumptions are explicitly recorded;
- `required_case_count` and `achieved_power` satisfy the frozen validator;
- no model output has been consulted for selection.

