# TÜBİTAK 2204-A 2027: Theme Fit and Evaluation-Rubric Audit

**Audit date:** 2026-10-10  
**Project:** LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi  
**Current intended main field:** Yazılım  
**Current intended thematic field:** Dijital İkiz  
**Status:** Risk audit; not a claim of eligibility or award likelihood

> **Superseded decision note (15 October 2026):** this document preserves the risk analysis recorded on 10 October. After checking the official 2027 guide's Digital Twin definition against the completed work, the current report is now classified as **Software / Artificial Intelligence**. The completed experiment is not a live sensor-fed twin, so the Digital Twin label should not be forced. See [the dated decision note](TUBITAK_2027_THEME_DECISION_2026-10-15.md).

## Current call and deliverable constraints

The official 2204-A page says that the 2026–2027 application window is 23 September 2026 through **4 January 2027 at 17:30**. The application must be complete and in the prescribed format; an unfinished or merely proposed project is not enough. Recheck the official page before submission in case of later updates:

- Competition page and current call: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
- Project guide linked from the official page: https://tubitak.gov.tr/sites/default/files/2026-09/lise_proje_rehberi_2027_onaya_sunulan.pdf
- The evaluation forms linked on the same official page are currently labeled 2025; the page should be checked again for any updated forms before the application is finalized:
  - Pre-evaluation criteria: https://tubitak.gov.tr/sites/default/files/2025-11/on_degerlendirme_kriterleri_2025_web.pdf
  - Regional/final criteria: https://tubitak.gov.tr/sites/default/files/2025-11/sergi_kriterleri_2025_web.pdf

The 2027 guide specifies a project title of at most 15 words and a 150–250 word abstract with the method and core findings, without citations or extended interpretation. The current title appears to meet the title-length limit; the final abstract must be written only after the study protocol/results are settled.

## Critical thematic-fit risk

The guide describes a digital twin as a virtual copy of an asset, system, or process that is continuously updated by real-time sensor data and used for monitoring, analysis, prediction, or optimization. The same guide states that software projects should make a scientific contribution to software-development practice and report appropriate data collection and analysis, not focus only on the software product.

The current experiment is primarily an LLM diagnosis benchmark, and the historic case graphs are revision-specific static annotations. That is not, by itself, a continuously updated digital twin. Calling the current artifact a complete real-time digital twin would overstate what has been built.

### Honest path to make the intended theme defensible

Define the research object narrowly as a **revision-bound software-system twin prototype**, not an operational real-time twin. Each case record must be traceable to an exact repository revision and include:

1. the software system/version represented;
2. named components and explicit, source-evidenced dependency edges;
3. the observed failure signal (regression test/output) at the pre-fix revision;
4. the fixed revision and evidence that the same regression test passes;
5. provenance, graph version/hash, and a clear difference between observed evidence and inferred causal annotation.

The future experiment then tests a precise sub-question about whether representing this version-bound twin's dependencies as graph triples adds diagnostic value beyond giving the identical dependency facts as prose. The report must explicitly say that this is a prototype/snapshot model rather than claim live sensor synchronization.

**Go/no-go rule:** the project lead and advisor must review the thematic fit before submitting. If a version-bound software-system twin cannot be substantiated from the evidence, do not invent telemetry or force the label; reassess the thematic field while the application is still editable. A strong research question in the wrong thematic category can be disadvantaged even if the code is technically sound.

## Map to the currently linked evaluation rubrics

The linked pre-evaluation form currently allocates importance points as follows: problem/research question 20, method 20, creativity/impact 30, results/discussion 30. The linked regional/final form allocates problem 15, method 10, creativity/impact 15, results/discussion 20, and presentation/project mastery 40. These weights are taken from the forms currently linked on the official page; verify whether TÜBİTAK publishes a 2027-specific replacement before final submission.

| Criterion | Evidence required in this project | Current action / acceptance rule |
|---|---|---|
| Problem and research question | Clear gap: whether graph representation itself adds value over equivalent dependency facts; measurable primary contrast | State C-vs-B as primary; A-B and A-C secondary; freeze comparisons before inference |
| Method | Matched information, independent defect cases, fixed model/revision, repeat policy, justified statistical unit and sample size | Three-arm v2 design; independent case is the unit, seeds are repeated observations |
| Creativity and impact | Novel and practical contribution, not merely an LLM demo | Show whether an explicit software dependency twin improves fault localization over an information-matched baseline; report null/adverse results honestly |
| Results and discussion | Accurate, reproducible outputs and limits | Preserve old 40/160 records unchanged; label their finding inconclusive; do not present tooling tests as model evidence |
| Presentation and mastery | Students can explain the causal question, evidence, code, scoring, statistics, contamination risks and limits independently | Prepare a student-authored demonstration and oral-defense questions only after results are frozen |

## Submission integrity requirements

- The 40-run pilot and 160-run confirmatory outputs are a completed historical experiment with a floor effect. Never revise those scores retrospectively.
- The v2 study has not run; its outcomes must not be implied in the report.
- Calibration examples, reviewer annotations, and reproduction results must be genuine; do not fabricate successful red/green checks, human labels, or performance gains.
- Every claimed result must point to a reproducible artifact or source. Every conclusion must match the data, including inconclusive or negative results.
- The student must understand and be able to explain the project; the assistant may support tools and editing but must not be represented as the project author.

## Acceptance checklist before final report drafting

- [ ] Advisor/student explicitly approve the Digital Twin fit based on actual revision-linked state/evidence; otherwise reassess thematic field before submission.
- [ ] Independent calibration examples and two blinded human reviews are complete; reliability thresholds pass.
- [ ] Selected calibration cases have independently reproduced pre-fix failures and fixed-revision passes.
- [ ] New held-out confirmatory sample is separate from calibration and prompt development.
- [ ] C-vs-B primary design, secondary contrasts, multiplicity handling, and a justified sample size are frozen before inference.
- [ ] V2 prompts have archived exact hashes and tokenizer-derived token counts for all arms/cases.
- [ ] Current official 2027 template, report length, criteria, and submission dates have been rechecked.
- [ ] Final report, source/appendix evidence, references, and poster/presentation pass a separate review.
