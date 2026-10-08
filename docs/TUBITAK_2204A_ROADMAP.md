# TÜBİTAK 2204-A Experimental Readiness Roadmap

Project: LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi

## Governing rule

No scientific result is marked complete without actual inference data. No result, p-value, effect size, benchmark conclusion, or hypothesis decision may be fabricated or inferred from code readiness.

## Status at 2026-10-08

### Phase 0 — Protocol and repository integrity
- [x] Research question frozen
- [x] Standard vs CCDG conditions frozen
- [x] Primary endpoint defined
- [x] Five-seed replication defined
- [x] Case-level majority rule defined
- [x] Exact two-sided McNemar test defined
- [x] Alpha = 0.05 defined
- [x] Model checkpoint revision frozen
- [x] Prompt/system prompt hashes pinned
- [x] Pilot manifest exists
- [x] Deterministic evaluator exists
- [x] Integrity audit exists
- [x] CI/test infrastructure exists

### Phase 1 — Pilot preflight
- [x] Three pilot cases identified
- [x] 30-run design is mechanically specified
- [x] Fail-closed local preflight script added (`scripts/pilot_preflight.py`)
- [x] Pilot preflight execution procedure documented (`docs/PILOT_PREFLIGHT.md`)
- [x] Frozen generation parameters are recorded
- [x] Ground truth is excluded from model context by protocol
- [x] Parse/schema failures are defined as failed runs
- [x] Kaggle execution packages the exact private Git commit instead of cloning the private repository
- [x] Kaggle pilot workflow is manual-only; ordinary pushes cannot launch scientific inference
- [x] Pilot runner is fail-closed against accidental overwrite and supports safe resume
- [x] Environment capture records source commit and GPU details
- [ ] Execute environment capture on the actual inference machine
- [ ] Verify the exact local model revision is available
- [ ] Verify GPU/VRAM/RAM and inference backend
- [ ] Run 30 real inferences
- [ ] Preserve immutable raw outputs
- [ ] Run evaluator
- [ ] Run case-level analysis
- [ ] Run pilot integrity audit on generated artifacts
- [ ] Produce pilot QA report

### Phase 2 — Pilot decision gate
- [ ] Confirm 30/30 records exist
- [ ] Confirm all frozen hashes/configurations match
- [ ] Report parse failures
- [ ] Report schema failures
- [ ] Report duplicate outputs
- [ ] Report seed agreement
- [ ] Report complete-pass rates
- [ ] Document contamination risk
- [ ] Decide whether any pilot case is eligible for the confirmatory benchmark using a predeclared rule
- [ ] Do not modify protocol based on observed outcome

### Phase 3 — Confirmatory benchmark construction
- [x] Define independent-case exclusion guard in the benchmark manifest validator
- [ ] Define independent-case inclusion criteria
- [ ] Define exclusion criteria
- [x] Define contamination audit procedure
- [ ] Build candidate case pool
- [ ] Verify source/fix provenance
- [ ] Verify ground truth independently
- [ ] Build and audit CCDG
- [ ] Run leakage audit
- [ ] Freeze final case IDs
- [ ] Freeze final benchmark manifest
- [ ] Perform power analysis using predeclared discordant-pair assumptions
- [ ] Freeze sample size before confirmatory inference

### Phase 4 — Confirmatory experiment
- [ ] Capture environment
- [ ] Freeze model/revision
- [ ] Freeze prompts
- [ ] Freeze benchmark
- [ ] Freeze ground truth
- [ ] Freeze CCDG
- [ ] Run Standard condition
- [ ] Run CCDG condition
- [ ] Preserve raw outputs and metadata
- [ ] Run deterministic evaluator
- [ ] Run integrity audit
- [ ] Run case-level aggregation

### Phase 5 — Statistical analysis
- [ ] Build paired case-level 2x2 table
- [ ] Run exact two-sided McNemar test
- [ ] Report discordant pairs
- [ ] Report paired effect size
- [ ] Report confidence interval
- [ ] Report secondary descriptive metrics
- [ ] Report parse/schema failure rates
- [ ] Report seed agreement
- [ ] Perform predefined sensitivity analyses, if any
- [ ] Do not add post-hoc inferential tests without labeling them exploratory

### Phase 6 — Scientific interpretation
- [ ] Determine whether H0/H1 is supported according to the frozen decision rule
- [ ] Analyze cases where CCDG helps
- [ ] Analyze cases where CCDG does not help
- [ ] Analyze cases where CCDG hurts
- [ ] Analyze failure modes
- [ ] Discuss contamination
- [ ] Discuss model/generalization limits
- [ ] Discuss CCDG construction limitations
- [ ] Discuss benchmark limitations
- [ ] State negative/null findings honestly if present

### Phase 7 — TÜBİTAK 2204-A report
- [ ] Use the official 2026-2027 report template
- [ ] Project title <= 15 words
- [ ] Turkish report
- [ ] Abstract 150-250 words
- [ ] Report within the official page limit
- [ ] Problem/research question
- [ ] Objectives
- [ ] Literature and research gap
- [ ] Hypotheses
- [ ] Method
- [ ] Dataset/case selection
- [ ] CCDG construction
- [ ] Ground truth
- [ ] Experimental design
- [ ] Model and generation settings
- [ ] Evaluation
- [ ] Statistical analysis
- [ ] Results
- [ ] Discussion
- [ ] Limitations
- [ ] Conclusion
- [ ] References
- [ ] Appendices/evidence prepared separately where appropriate

### Phase 8 — Submission and defense
- [ ] Check all TYBS fields
- [ ] Check ARBIS records
- [ ] Check required forms
- [ ] Check licenses and attribution
- [ ] Check no fabricated/altered results
- [ ] Check no unnecessary brand promotion in report
- [ ] Similarity/originality review
- [ ] Final PDF visual inspection
- [ ] Prepare poster
- [ ] Prepare 3-minute project explanation
- [ ] Prepare 30-60 second answers to jury questions
- [ ] Prepare reproducibility package
- [ ] Archive final commit/tag

## Hard stop

The project must NOT be marked scientifically complete while Phase 1 real inference and Phase 3 confirmatory benchmark construction remain incomplete.

The current repository is therefore **protocol-ready / experiment-pending**, not result-complete.
