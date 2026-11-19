# Dishka #435 — patch URI and SHA-256 reconciliation

**Record date:** 19 November 2026  
**Case:** `reagento__dishka-436` / issue #435 / PR #436  
**Purpose:** document and resolve a URI/content-hash mismatch in the proposed v0.2 case record.

## 1. Mismatch found

The proposed record originally paired the mutable upstream URI:

`https://github.com/reagento/dishka/pull/436.diff`

with SHA-256:

`c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`

That digest does **not** identify the content returned by the current PR-level `.diff` endpoint. The current endpoint retrieval produced a different content digest (`f57d8bd11868e663023eb38f8cd239703a802fb6805a61c487c0d265fbfb1ceb`). Therefore the old URI/hash pair was not retained as if it were a match.

## 2. Exact source of the recorded digest

The digest `c5a6e5ed...` identifies the file `full-pr.diff` generated in the latest verified Dishka reproduction artifact by running `git diff` over the exact pinned source revisions:

- Buggy base: `8718d5af93f9e48bc2506c64827663fdccc5ad89`
- Fixed revision: `b1eae11734e64551d7b101195f27cb6870e1c364`

The producing workflow step is equivalent to:

```bash
git -C upstream-dishka diff \
  8718d5af93f9e48bc2506c64827663fdccc5ad89 \
  b1eae11734e64551d7b101195f27cb6870e1c364 \
  > reproduction-evidence/full-pr.diff
```

The latest repeat artifact is:

- Run: `44572926370`
- Dishka job: `135733170187` — success
- Artifact: `14553229664`
- Artifact URI: `https://github.com/MahmutVezir/dijitalikiz/actions/runs/44572926370/artifacts/14553229664`
- Outer ZIP SHA-256: `7f10db7e6f1b033eef7cd34476e3e34b3dbd28687310ccb3707ffddc5d5a6f10`
- Inner `full-pr.diff` SHA-256: `c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`
- ZIP CRC: PASS; 33 members; 32/32 internal SHA256SUMS entries independently verified.

## 3. Corrected case-record reference

The canonical case record now uses:

`https://github.com/MahmutVezir/dijitalikiz/actions/runs/44572926370/artifacts/14553229664#path=full-pr.diff`

with SHA-256:

`c5a6e5edc41d5a321fb95dc0bdb81ee449870eb53278a5d91582c2478395efde`

The technical reproduction baseline and fixed-run records both point to the same exact verified archive, with its outer SHA-256. This is a correction to the evidence pointer only; the pinned base/fixed commits, changed file set, test selectors and scientific interpretation are unchanged.

## 4. Retention and reproducibility limitation

The GitHub Actions artifact is configured for 90-day retention. It is an evidence transport/reference, not permanent archival storage. If it expires, the full diff can be regenerated from the two pinned commits using the command above and checked against the recorded SHA-256. The immutable source commits and the exact reconstruction procedure are the durable provenance anchors.

This reference correction does not provide legal clearance or authorize redistribution. The existing project-lead documentary license-scope decision remains limited to its expressly stated experimental scope and expressly does not grant blanket redistribution approval.
