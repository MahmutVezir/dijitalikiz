# Meltano #3090 — Stage 2 artifact integrity review

**Review date:** 2026-11-21  
**Artifact:** reproduction run 44331092872, artifact 14440520435  
**Disposition:** local archive integrity verified

## Verification results

- Downloaded artifact ZIP: 18,363 bytes.
- ZIP SHA-256 recomputed locally: b1336169d7b6d8e4e47edbcd920d842ad525c7a4e2df841b998182099bed1bd3; matches GitHub's artifact digest.
- ZIP CRC/integrity test: passed; no corrupt member reported.
- Internal SHA256SUMS.txt: all 14/14 files matched after normalizing the manifest's leading ./ path prefix.
- Canonical dataset row: meltano__sdk-3091; row SHA-256 318893b8546a4a6b2d8bc75d986a079c818951658fc1293ac59ba05d84682266.
- Base independent reproducer: failed as expected; the second sibling remained an empty object.
- Fixed independent reproducer: passed (1 test).
- Frozen dataset selector: failed on the buggy base and passed on the fixed revision, with the same selector.

## Archived provenance files

- upstream-LICENSE.txt: SHA-256 046b03106bbadbc6529527c9cebdd1b21174fca4d6f84d59fbe5e7aa38a86168.
- upstream-pyproject.toml: SHA-256 5dab19c5d782d4198157cc138319288a0ea6347aab66acf0840bf1a6281f6d30.
- pr-3091-full.patch: SHA-256 1396da1bbd0408532925757c9cebdd1b21174fca4d6f84d59fbe5e7aa38a86168.
- dataset-test.patch: SHA-256 2477c14b21eb7c63022dc02f05c787d324e92a99a60b9970b2e62ba988318e11.
- dependency-license-inventory.json: SHA-256 148d671c1c5e1f3cad17899e8361a1bde05057227ee56ef4225064c4a70ec623; 32 installed distribution entries.
- dataset-extraction-license-inventory.json: SHA-256 0820f6ee592d6482bad674d510aacc37f56d3c335c1c7da9414c83749443f7a2; one extraction tool entry (pyarrow 19.0.1).

The package metadata inventory contains unresolved license metadata flags; these are recorded in the separate bounded-scope review. Archive integrity does not amount to legal clearance.
