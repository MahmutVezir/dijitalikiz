# Final Execution Runbook — Experiments Complete

## 1. Frozen pilot

The 40-run pilot is complete.

- Run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402
- Source commit: `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`
- Artifact ID: `11634641753`
- Artifact SHA-256: `b12594415894d5cac18442d3bd6c505e843b1a14027272c1afa398a59101aca0`
- Records: 40/40; parse errors: 0; independent file/hash inventory: 55/55.

## 2. Confirmatory benchmark

The 16-case, 160-run benchmark is complete.

- Run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37976682761
- Exact source commit: `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`
- Artifact ID: `11640450681`
- Artifact SHA-256: `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`
- Records: 160/160; parse errors: 0; independent file/hash inventory: 212/212.
- Evaluation: Standard 0/80, CCDG 0/80 primary alias matches; 0/16 case-level majority passes in each condition.
- Exact two-sided McNemar p=1.00; paired risk difference 0.00; 95% CI [-0.1936, 0.1936].

## 3. What the result does and does not mean

The frozen literal-alias endpoint has a floor effect and the study did not detect a difference on that endpoint. It neither proves equivalence nor proves that CCDG has no semantic effect. Do not change the alias rubric or re-label the existing 160-run analysis as confirmatory. A review or re-score of existing outputs must be labeled exploratory. A new semantic confirmatory study needs its scoring instrument validated before output inspection and a new independently selected case sample.

## 4. Final report gate

The current results have been written into `docs/TUBITAK_REPORT_DRAFT.md`. The report must disclose that the primary scoring endpoint was amended after pilot-output diagnostics and before confirmatory outputs were seen. Do not claim full preregistration before any model output was inspected.

Before portal submission:
1. Copy the text into the official 2026–2027 TÜBİTAK Word template.
2. Check the required title, 150–250-word abstract, page range, and all template fields against the current official guide.
3. Verify student/school/supervisor and any permission information from authoritative records; do not guess missing data.
4. Render the template to PDF and inspect every page.
5. Submit through TYBS, ensuring ARBİS records and any required forms are accurate.

The code/inference stage is complete. Portal submission, individual/school fields, and final official-template/PDF checks require the student's authoritative data and action in the submission system.
