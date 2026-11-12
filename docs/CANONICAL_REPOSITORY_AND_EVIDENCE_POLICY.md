# Canonical repository and evidence policy

## Single source of truth

`MahmutVezir/dijitalikiz` is the only canonical repository for project-authored code, notebooks, experiment protocols, review tools, test specifications, metadata, and evidence indexes. Development branches and pull requests must be created inside this repository. Do not create project forks, duplicate project repositories, or standalone gists as alternate sources of truth.

## Upstream dependencies

The experiment uses BugsInPy and upstream software projects as external research material. Workflows must fetch these repositories at the exact pinned commit IDs recorded in the cohort and case manifests. This is not a second project repository. Do not copy whole upstream codebases or fixed patches into this repository until license and redistribution terms have been checked and recorded.

## Case provenance

Each candidate case must have a stable ID, upstream repository URL, pinned BugsInPy metadata revision, buggy and fixed commit IDs, Python version, target test command, metadata hashes, technical outcome, and evidence artifact ID/digest. Case acceptance is a separate human-reviewed decision. A technical signal must never automatically add a case to the confirmatory registry.

## Durable evidence

Commit the project-authored code, normalized metadata-only cohort index, case-selection record, and evidence manifest to this repository. The V12 100-case index, first eight-case metadata selection, and evidence manifest are committed under `research_candidates/evidence_abstention/generated_v12/`. The full BugsInPy inventory and queue CSVs remain reproducible from the pinned upstream commit and are retained only as a 90-day Actions artifact because the benchmark's dataset-level license is unresolved; do not redistribute them until permission/license review is complete. GitHub Actions artifacts are temporary and must not be treated as long-term storage. Do not claim a raw file is permanently stored unless it is actually committed and retrievable from this repository.

## Research safety gates

Keep `accepted_for_confirmatory=false` and `llm_inference_performed=false` until license review, two-reviewer ground-truth review, evidence-tier review, leakage/prior-exposure review, and protocol/hash freeze are complete. Never silently replace failed or blocked candidates after observing their outcome.


## Historical archive recovery

The legacy CCDG confirmatory ZIP was recovered from the user's ChatGPT Library and its SHA-256/ZIP CRC/212-file manifest/160-record structure were rechecked. The archive is not yet committed to `data/historical/confirmatory_artifact_2026-10-09.zip`; the repository-local historical gate remains blocked until the exact ZIP is uploaded and its expected hash passes. This legacy CCDG archive is not the new abstention dataset and must not be used as confirmatory data for the abstention study.
