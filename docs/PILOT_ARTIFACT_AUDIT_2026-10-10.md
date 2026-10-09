# Frozen Pilot Artifact Integrity Audit — 10 October 2026

## Scope

This is an independent file-level audit of the archived pilot artifact produced by GitHub Actions run [37968099402](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402) at source commit `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`. It does not alter or regenerate model outputs.

## Archive and manifest checks

- GitHub artifact ID: `11634641753`
- Archive SHA-256: `b12594415894d5cac18442d3bd6c505e843b1a14027272c1afa398a59101aca0`
- Expected versus observed archive hash: matched
- Internal manifest: version 1.3; finalization gate status `complete`
- Manifest files: 55 expected; 55 present
- File-size mismatches: 0
- SHA-256 mismatches: 0
- Missing listed files: 0
- Unexpected files under `pilot-output/` (excluding the manifest itself): 0
- Individual run files: 40
- JSONL records: 40
- Manifest run record count: 40

The ZIP also contains a Kaggle run log alongside the `pilot-output/` directory. That log is outside the declared artifact root and is not counted as one of the 55 manifest-listed output files.

## Frozen pilot QA

The pilot covers four cases × two conditions × five seeds = 40 inference records. Under the frozen literal scoring rule:

| Metric | Standard | CCDG |
|---|---:|---:|
| Expected / found records | 20 / 20 | 20 / 20 |
| JSON parse success | 20 / 20 | 20 / 20 |
| Parse failure rate | 0% | 0% |
| Primary-score passes | 0 / 20 | 0 / 20 |
| Case-level 3-of-5 majority passes | 0 / 4 | 0 / 4 |

There were no duplicate parsed-output groups in the QA report. These are integrity and frozen-metric observations, not evidence that every response was semantically incorrect or that CCDG has no effect. The pilot shows the same floor-effect concern later found in the confirmatory run.

## Interpretation and limitations

- The artifact passes integrity checks; this establishes record completeness and hash consistency, not the scientific validity of the primary endpoint.
- A deterministic contiguous-alias metric can reject semantically plausible paraphrases. The 0/20 results per condition must not be recast as a semantic accuracy estimate without a separately validated scoring method.
- The four pilot cases and 40 repeated generations do not constitute 40 independent software defects; the independent case count is four.
- The old pilot's context renderers were later found to be information-mismatched. Historical prompts and records remain unchanged for reproducibility.
- This audit is based on the archived artifact. A corresponding GitHub Actions audit step has been added so future validation can verify the archive and re-run the original source-version prompt/configuration checks in CI.

## Reproducibility

- Original artifact: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402
- Archive SHA-256 above is the exact downloaded ZIP hash.
- The manifest is `pilot-output/artifact_manifest.json` inside the artifact.
- The repository's historical checker is `scripts/audit_pilot_integrity.py`; run it against the artifact records using the exact source commit and its corresponding frozen prompt/configuration files.

## Status

Manual archive integrity: **pass (55/55 manifest files; zero size/hash mismatches)**.  
Frozen pilot primary metric: **0/20 in each condition; floor-effect warning**.  
The scientific hypothesis remains unresolved by this score. The old pilot remains preserved as historical evidence, not as the final word on the three-condition follow-up.
