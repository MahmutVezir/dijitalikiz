# GeoPandas #3591 — publication evidence note (v0.1)

**Date:** 21 November 2026  
**Status:** Publication-oriented evidence summary. The candidate remains **HOLD** and is not an accepted study case.  
**Scope:** Whether a software root-cause diagnosis is answerable from a specified evidence tier, with abstention preferred when evidence does not distinguish competing mechanisms.

> This is an attribution-first derivative of the frozen research record. It is not legal advice or legal clearance and does not replace the underlying evidence manifests or technical reports.

## 1. Publication boundary

This note uses concise paraphrases, attribution and links. It does not reproduce the frozen dataset row, complete problem statement, source-code patch or test patch, upstream source code, full GitHub comment bodies, dependency binaries, package source distributions or model outputs. The identifiers and hashes below are provenance references, not substitutes for the underlying records.

## 2. Case identity and attribution

- Upstream project: [GeoPandas](https://github.com/geopandas/geopandas)
- Issue: [geopandas/geopandas #3590](https://github.com/geopandas/geopandas/issues/3590)
- Fix PR: [geopandas/geopandas #3591](https://github.com/geopandas/geopandas/pull/3591)
- Dataset: [Prime Intellect, SWE-rebench-V2-Filtered-Verified](https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified)
- Pinned dataset revision: fb9aa226b2ce37c708ea7732e7b980abacdadb67
- Frozen instance: geopandas__geopandas-3591
- Canonical row SHA-256: e543af0bbc5e779661c1b79c28849f67dee7c61157c000c6698b15ba1218e2
- Problem-statement SHA-256: c4aeb4909495887c065f1f7ae5ec0e321fb350e98ea789cde3f931cad597f12d
- Buggy base commit: c36eba059f6170715b63a9aa065817c64025d263
- Fixed commit: b3259ce23a37abd32650d7df098f3cdc8c4bb261

The dataset publisher declares CC BY 4.0 for the dataset. The row's source-license field identifies BSD-3-Clause for the underlying GeoPandas repository. These are different licensing/provenance layers; the dataset declaration does not replace the source-code license or establish rights in individual GitHub comments.

The GeoPandas base and fixed revisions use the same root LICENSE.txt Git blob (028603be2080134aa4817ed691fec3f449ffa609) and the same pyproject.toml blob (7e423f8efebdcdf2f11e71ca9aff4ff31b3edf8a), which declares BSD 3-Clause. The PR did not change these files. See the [pinned base license](https://github.com/geopandas/geopandas/blob/c36eba059f6170715b63a9aa065817c64025d263/LICENSE.txt) and [fixed revision](https://github.com/geopandas/geopandas/tree/b3259ce23a37abd32650d7df098f3cdc8c4bb261).

## 3. Problem and gold mechanism

The frozen issue describes a non-empty GeoDataFrame with a column named geometry containing only missing numeric values, alongside a CRS. The affected version raises an error indicating that a geometry column has not been recognized. The report provides an explicit-geometry workaround and contrasts the failure with a column containing a valid point.

The project-lead-approved implementation explanation is that the buggy constructor's implicit geometry-coercion eligibility check did not include a non-empty, all-missing geometry column. The column therefore was not normalized and installed as the active geometry before CRS validation. The fix recognizes this all-missing case. This is a mechanism summary; no source code or patch lines are reproduced.

**Gold mechanism:** G1_NONEMPTY_ALL_NULL_FLOAT_GEOMETRY_SKIPS_AUTO_COERCION.

## 4. Evidence tiers

The packets are nested: E2 includes E3; E1 includes E2 and E3.

| Tier | Approved decision | Remaining explanations | Interpretation |
|---|---|---|---|
| E3 — frozen issue statement only | **ABSTAIN** | G1, A1, A2 | Input, error, workaround and valid-geometry contrast are visible; the constructor's internal dtype-recognition branch is not. |
| E2 — E3 plus issue discussion and fixed regression-test source | **ABSTAIN** | G1, A2 | Follow-up discussion weakens a one-row-only explanation, but does not uniquely distinguish constructor eligibility from a competing geometry/CRS state explanation. Test source is not an execution log. |
| E1 — E2 plus pinned base/fix source and PR review discussion | **ANSWER** | G1 | Source control flow and the fix identify the omitted all-missing eligibility condition; the competing explanation is downstream of the missed coercion. |

### Attributed paraphrases of public discussion

These are paraphrases, not quotations:

- On 5 June 2025, maintainer account martinfleis explained that np.nan is represented as a floating-point value rather than a geometry object or None, and indicated that the reported scenario should be supported. [Issue comment](https://github.com/geopandas/geopandas/issues/3590#issuecomment-2943137874).
- Later that day, reporter account zmoon described similar older-version behavior for a longer all-missing column and for mixed missing-value types. This is a reporter follow-up observation, not an independently preserved test log. [Issue comment](https://github.com/geopandas/geopandas/issues/3590#issuecomment-2944863844).
- On 5 June 2025, martinfleis noted that the project's geometry-sanitization path already handled missing values in related cases. [Issue comment](https://github.com/geopandas/geopandas/issues/3590#issuecomment-2945606056).
- On 5 June 2025, PR reviewer account jorisvandenbossche suggested the all-missing predicate later present in the fix. This patch-specific disclosure is E1-only. [PR review discussion](https://github.com/geopandas/geopandas/pull/3591#discussion_r2130293780).

The source snapshots preserve account names, timestamps, permalinks and body hashes, but do not establish an explicit open license from each commenter. This publication note therefore paraphrases, attributes and links; it does not reproduce full comment bodies or represent them as BSD-licensed GeoPandas code.

## 5. Technical reproduction

The same frozen input was reproduced against the exact buggy base and fixed PR revision. The frozen pytest selector exists in the fixed revision, so the base side used an independent reproducer with the same input rather than claiming that a fix-added test ran on the base.

- Buggy base: independent reproducer observed the expected ValueError about assigning a CRS without a recognized geometry column.
- Fixed revision: independent reproducer succeeded; active geometry was geometry, its value was null, and CRS was EPSG:4326.
- Fixed-revision frozen pytest selector: **1 passed**.
- Runtime: Ubuntu 22.04, CPython 3.11.9. The pinned version lock matched pip freeze --all apart from the editable GeoPandas checkout; pip check reported no broken requirements.

Two successful runs were completed:

| Run | GitHub Actions | Artifact SHA-256 | Integrity |
|---|---|---|---|
| 44935740419 | [Run log](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44935740419) | bc807d9c1bdec02e72c61783d9f3e8a5640574fd620fd0da5de2ec4468a1894e | Outer digest matched; ZIP CRC passed; 17/17 internal hashes passed |
| 44936142633 | [Run log](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44936142633) | eda44a04658c9250e4fa559c824a512ec4a91e7ff3f8595db0379db9c9ecd41e | Outer digest matched; ZIP CRC passed; 17/17 internal hashes passed |

These results establish technical reproduction for one frozen case. They are not model-output results, a measure of model performance or evidence of a confirmatory study effect.

## 6. Dependency provenance and limits

A separate documentary source-level screen records license declarations and exact source-tag references for the 18 pinned third-party Python distributions. It also flags relevant native components associated with Shapely/GEOS, Pyogrio/GDAL, Pyproj/PROJ and NumPy/OpenBLAS.

The dependency file is a version lock, not a wheel-hash lock. Local wheel SHA-256 values were not retained, and the exact third-party notice set inside some platform wheels was not fully inventoried. The evidence supports the recorded runtime versions and the source-level license screen, but does not establish byte-for-byte binary reproducibility or clear redistribution of a complete environment. The Stage 2 execution archive contains logs, version metadata and the lock, not package binaries or source trees.

Do not redistribute the pinned environment as a binary bundle on the strength of this note. Any future environment distribution requires wheel-hash capture and complete platform-specific third-party notice review.

## 7. Research integrity and limitations

- The project lead disclosed full exposure to the upstream issue, comments, PR and source. No blinded researcher adjudication is claimed.
- No inter-rater reliability statistic is claimed. ChatGPT was advisory, not an independent human rater.
- This is one exploratory candidate; technical success does not establish a population-level result or confirm the study hypothesis.
- The candidate remains **HOLD** and is not in the accepted-case registry.
- No model was loaded; no inference, fine-tuning or training was performed or authorized.
- The frozen dataset, row, selector, E1/E2/E3 manifests, sample size and experiment design were not changed.

## 8. Attribution and reuse notes

1. **Dataset:** Attribute Prime Intellect and the dataset title; link to the dataset and pinned revision; identify CC BY 4.0 as the publisher-declared dataset license. This note contains paraphrased provenance summaries, not the dataset row. [Dataset card](https://huggingface.co/datasets/PrimeIntellect/SWE-rebench-V2-Filtered-Verified).
2. **GeoPandas source:** Attribute GeoPandas developers and the exact repository commits. Source redistribution must preserve the applicable BSD notice, conditions and disclaimer. This note contains no source code or patch diff. [BSD license at the fixed commit](https://github.com/geopandas/geopandas/blob/b3259ce23a37abd32650d7df098f3cdc8c4bb261/LICENSE.txt).
3. **GitHub discussion:** Attribute each commenter account and link to the original permalink. Do not present those comments as covered by the GeoPandas BSD license.
4. **Dependencies:** Do not infer a blanket license for the complete environment from individual package declarations. Consult the separate source/dependency screen and review wheel-level notices before redistribution.

## 9. Supporting research records

- [Project-lead gold and evidence-tier decision](../PROJECT_LEAD_GOLD_AND_EVIDENCE_TIERS_DECISION_GEOPANDAS_3591_2026-11-21.md)
- [Stage 2 technical reproduction result](../GEOPANDAS_3591_STAGE2_TECHNICAL_REPRODUCTION_RESULT_2026-11-21.md)
- [Source and dependency license/provenance screen](../GEOPANDAS_3591_SOURCE_AND_DEPENDENCY_LICENSE_PROVENANCE_SCREEN_2026-11-21.md)
- [License and provenance audit](../GEOPANDAS_3591_LICENSE_AND_PROVENANCE_AUDIT_2026-11-21.md)
- [E3 manifest](../GEOPANDAS_3591_E3_PACKET_MANIFEST_V0_1.json) · [E2 manifest](../GEOPANDAS_3591_E2_PACKET_MANIFEST_V0_1.json) · [E1 manifest](../GEOPANDAS_3591_E1_PACKET_MANIFEST_V0_1.json)

---

**Publication note v0.1.** Later edits to the paraphrases, evidence scope or attribution record should be versioned as a new derivative. Frozen source snapshots and experiment records should remain unchanged.
