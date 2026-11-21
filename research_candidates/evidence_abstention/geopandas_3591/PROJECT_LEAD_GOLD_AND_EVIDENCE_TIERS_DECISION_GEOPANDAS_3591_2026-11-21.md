# Project-lead gold mechanism and evidence-tier decision — GeoPandas #3591

**Decision date:** 21 November 2026
**Approval timestamp captured:** 2026-11-21T20:58:43+03:00 (Europe/Istanbul)
**Candidate:** geopandas/geopandas issue #3590 / PR #3591
**Frozen cohort rank:** 52
**Frozen dataset row:** geopandas__geopandas-3591
**Decision source:** The project lead explicitly accepted the complete recommendation in the ChatGPT conversation on 21 November 2026.

## 1. Approved gold mechanism

**Project-lead decision: APPROVED.**

**Gold ID:** G1_NONEMPTY_ALL_NULL_FLOAT_GEOMETRY_SKIPS_AUTO_COERCION

When geometry=None and the input has a single-level column named geometry, the buggy GeoDataFrame.__init__ only routes that column through _ensure_geometry when its dtype is geometry, object, or the frame is empty with float dtype. A non-empty all-np.nan geometry column has float dtype and misses the coercion condition. The constructor therefore leaves the active geometry unset; the later CRS guard raises the observed error. The fix adds a non-empty/all-missing predicate to the implicit geometry-coercion condition.

The diagnostic target is the implementation mechanism, not only the external API contract.

## 2. Approved alternative mechanisms

- A1_SINGLE_ROW_DATA_SHAPE_OR_ALIGNMENT: the failure arises from one-row pandas data construction, shape or column alignment rather than the GeoPandas dtype-eligibility gate. E2 reporter follow-up evidence that the older version also handled ten all-NaN rows weakens this explanation sufficiently to remove it at E2.
- A2_CRS_ACTIVE_GEOMETRY_STATE_TRANSITION: the CRS/active-geometry state transition is the primary defect independently of the dtype-eligibility predicate. This remains live at E2; E1 source control flow shows the CRS guard is downstream of the missed automatic coercion, so it is eliminated at E1.

## 3. Project-lead-approved evidence tiers

| Tier | Decision | Surviving mechanisms | Rationale |
|---|---|---|---|
| E3 | **ABSTAIN** | G1, A1, A2 | Frozen problem statement gives input, error, workaround and valid-geometry contrast, but not the constructor's internal dtype recognition predicate. |
| E2 | **ABSTAIN** | G1, A2 | Issue comments and fixed test source weaken/eliminate the one-row-only alternative but do not disclose the constructor predicate or distinguish G1 from the CRS state-transition alternative. |
| E1 | **ANSWER** | G1 | Pinned buggy/fixed source, null-normalization helper and the E1-only PR review suggestion establish the omitted all-null predicate as the surviving mechanism. |

The packets are nested: E2 inherits E3; E1 inherits E2 and E3. The exact PR review suggestion that spells out the all-null predicate is E1-only and is not present in E2.

## 4. Frozen evidence packet manifests

| Tier | Path | SHA-256 |
|---|---|---|
| E3 | research_candidates/evidence_abstention/geopandas_3591/GEOPANDAS_3591_E3_PACKET_MANIFEST_V0_1.json | 8a59516e9a4282cab88b7a0372c4402f8f069cff037ddfc39269ce4c212727a8 |
| E2 | research_candidates/evidence_abstention/geopandas_3591/GEOPANDAS_3591_E2_PACKET_MANIFEST_V0_1.json | a7af85fae4233326ad22370131880f30739034137287ed01b1ac6cf0ec03e9ed |
| E1 | research_candidates/evidence_abstention/geopandas_3591/GEOPANDAS_3591_E1_PACKET_MANIFEST_V0_1.json | f616ee1036b77fde6fa77fff9efe27fd26c6dd78cf6657046c4071b0e47e5dbb |

The E3 row-identity capture references the no-inference extraction audit (run 44924570231, job 136907864713, artifact 14715535728; artifact SHA-256 1abca7d09dfcbf4c4ba773ab87fb21225ec8f4208f44f2f7fbb19b613352459b). Evidence snapshot files are stored beneath research_candidates/evidence_abstention/geopandas_3591/source_snapshots/.

## 5. Execution and validity boundaries

- Frozen selector: geopandas/tests/test_geodataframe.py::TestConstructor::test_geometry_nan_scalar (one selector).
- **Stage 2 has not been run.** No pinned reproduction environment, raw base-fail/fixed-pass log, or Stage 2 artifact exists for this candidate. The fixed PR regression tests are source evidence only; they are not claimed executed.
- These manifests are frozen semantic source packets only, not Stage 2 reproduction evidence.
- Candidate disposition remains **HOLD**; this decision is not final case acceptance and does not add the candidate to the exploratory registry.
- Prior pipeline/debug exposure remains none; researcher source exposure is full and disclosed. No blinded researcher adjudication or inter-rater reliability is claimed. ChatGPT is advisory, not an independent human rater.
- No legal/licensing clearance, redistribution approval, or commercial permission is asserted.
- No model loading, inference, fine-tuning or training was performed or authorized.

**Next gate:** a separate explicit project-lead decision is required before any Stage 2 exact base/fix reproduction. This gold/tier approval does not authorize Stage 2 or model inference.
