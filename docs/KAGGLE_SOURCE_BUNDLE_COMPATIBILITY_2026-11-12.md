# Kaggle source-bundle compatibility audit — 12 November 2026

## Finding

The 31-file and 19-file counts refer to two different, intentionally versioned source snapshots. They are not two measurements of one identical package, and the 19-file snapshot is not the complete GitHub repository.

### Snapshot A — 27 October v2 source bundle

- Bundle name: `kaggle_validation_source_bundle_2026-10-27_v2`
- Source commit recorded in its manifest: `99663c2874424feb9cec1d965432030f5cdb3ef8`
- Manifest filename in the uploaded Kaggle dataset: `BUNDLE_MANIFEST.json`
- Expected source-file count: 31
- Intended consumer: `02_kaggle_source_integrity_and_tests_no_inference.ipynb`
- Purpose: validate the frozen 27 October source bundle and its file hashes without model inference.

The current tracked version of notebook 02 accepts its canonical v2 manifest path and a guarded `BUNDLE_MANIFEST.json` fallback. The fallback is valid only if the bundle name, source commit, expected file count and per-file hashes match. Do not rename the manifest by hand.

### Snapshot B — 3 November current-branch audit bundle

- Manifest filename: `KAGGLE_STAGE3_CURRENT_BRANCH_AUDIT_2026-11-03.manifest.json`
- Intended consumer: `03_kaggle_current_branch_no_inference_audit.ipynb`
- Expected file count in that audit: 19
- Purpose: a deliberately scoped, allow-listed current-branch no-inference audit.

The 19 files are the inputs required by that audit contract, not every file in `MahmutVezir/dijitalikiz`. The repository itself contains substantially more project code, tests, documentation, notebooks and evidence records.

## Root cause of the Kaggle manifest error

The error `Exactly one v2 source-bundle manifest ... found 0` means the running notebook did not find the manifest filename/path it was coded to discover in the attached Kaggle input. The 27 October dataset contains `BUNDLE_MANIFEST.json`, not the other notebook's 3 November manifest. A stale notebook copy may also lack the guarded fallback now present in notebook 02.

The 31-versus-19 mismatch is therefore a snapshot/consumer mismatch, not proof that twelve source files were deleted from the canonical GitHub repository.

## Safe operating rule

1. Treat `MahmutVezir/dijitalikiz` as the canonical source of truth.
2. Never mix the 27 October v2 input with the 3 November current-branch notebook.
3. Never rename or edit a manifest to make a check pass.
4. For the new V12 metadata intake, use the GitHub Actions workflow `evidence-abstention-metadata-inventory.yml`; it pins the BugsInPy commit and uses the 105-ID exposure union directly from the repository. Kaggle is not needed for this metadata-only stage.
5. Before any future Kaggle model run, generate a new immutable source snapshot from the exact approved PR/main commit, include all required project-authored code and tests, produce a manifest automatically, and verify its hashes before inference.
6. Keep upstream source checkouts external and temporary; do not bundle them into our repository unless the exact license permits it.

## Current status

- V12 metadata generation now succeeds in GitHub Actions (run `43236394154`).
- V12 cohort and first-batch metadata selection are committed in `research_candidates/evidence_abstention/generated_v12/`.
- No model inference or training has been performed.
- The old Kaggle v2 and 3 November notebooks remain historical audit artifacts; they are not the current V12 intake workflow.
