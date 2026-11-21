# GeoFileOps #649 — timestamp reconciliation review

**Candidate:** `geofileops__geofileops-649`  
**Dataset revision:** `fb9aa226b2ce37c708ea7732e7b980abacdadb67`

The frozen canonical dataset row records `created_at` as `2025-03-06 15:39:28`. The upstream GitHub API record for PR #649 reports `created_at=2025-03-06T15:39:28Z`. The complete cohort timestamp register, part 07, independently records these normalized values as identical with `delta_seconds=0` and `match_status=exact_match`.

- Register: `research_candidates/evidence_abstention/timestamp_reconciliation_part_07_2026-11-15.csv`
- Register content SHA-256: `97f3957c9a1788f1b85f5b9778c96e157b489f84412c5e8d75d54d7133f60c8e`
- Upstream PR: https://github.com/geofileops/geofileops/pull/649
- Exact upstream created_at: `2025-03-06T15:39:28Z`
- Frozen dataset row created_at: `2025-03-06T15:39:28Z`
- Difference: `0 seconds`; row-level result: `exact_match`.

The overall 113-record timestamp audit has one unrelated one-second exception (`simpeg__simpeg-1633`). GeoFileOps #649 is not that exception; its row-level reconciliation is exact. The row-specific timestamp gate is satisfied, while the separate global dataset provenance exception remains disclosed.

No timestamp rounding or truncation has been inferred for this row.