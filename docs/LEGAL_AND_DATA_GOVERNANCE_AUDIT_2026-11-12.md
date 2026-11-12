# Legal and Data Governance Audit — 12 November 2026

**Status: NOT CLEARED FOR FINAL SUBMISSION OR DATA REDISTRIBUTION.**  
This is a research-governance checklist, not legal advice. A teacher/advisor should review the final interpretation before any external submission or redistribution.

## 1. TÜBİTAK 2204-A eligibility and submission constraints

- The 2026–2027 call is open from 23 September 2026 through 4 January 2027 at 17:30 Türkiye time.
- The official call requires the submitted project to be completed and shaped by the students using their own knowledge and skills. Idea-stage or ongoing projects are not eligible.
- One project may have up to three students and one advisor. Students must be under 20 on the application deadline.
- If the research target group includes stakeholders of Ministry of National Education institutions (students, parents, teachers, administrators, staff), the required MEB research application/approval must be obtained.
- If a data collection instrument is applied to people, written voluntary consent is required. For research targeting students under 18, parental consent is mandatory. For non-MEB institutions, institution permission and participant consent are required as applicable.
- The project must not present a commercial product, brand, or institution as the focus of the report.

Official source: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi

## 2. Generative AI disclosure

TÜBİTAK's responsible generative-AI guide allows supporting uses such as literature summarization, language support, coding assistance, and visualization. Applicants remain responsible for correctness, originality, and ethics. Significant use must be disclosed transparently. Confidential data must not be entered into generative-AI tools.

Official source: https://tubitak.gov.tr/tr/kurumsal/hakkimizda/uretken-yapay-zeka-rehberi

For this project, the final report must disclose that ChatGPT was used for research planning, code review/assistance, debugging, literature discovery, and draft preparation. Mahmut must personally understand, verify, and be able to explain every submitted method, code path, experiment, and conclusion. AI-generated claims or results must never be presented as observed evidence.

## 3. BugsInPy benchmark: unresolved dataset-level license

The pinned BugsInPy repository used by the V12 workflow is `https://github.com/soarsmu/BugsInPy` at commit `11c5f1eea954a42132cfd06bf257766a7963e0fd`.

- A root `LICENSE` file was not found at the checked repository path on 12 November 2026.
- Upstream issue #94 explicitly raises the absence of license information: https://github.com/soarsmu/BugsInPy/issues/94
- The BugsInPy research paper is a scholarly publication; its publication license does not automatically license the separately maintained benchmark database, patches, metadata, or bundled source projects.
- Do not describe BugsInPy as MIT/Apache licensed. No dataset-wide license clearance has been established.
- Do not copy or redistribute the BugsInPy source tree, patches, or full metadata bundle in this repository or the final report.
- The current private repository stores only a limited metadata-only case index, source links, commit identifiers, and hashes. This reduces redistribution but is not a substitute for permission or legal clearance.

**Required before confirmatory data collection:** obtain written permission/clarification from the benchmark maintainers, or replace the dataset-level dependency with an independently curated case set sourced directly from upstream repositories with verified licenses. Until then, V12 remains a provisional candidate index only.

## 4. Upstream project licenses: per-project review required

The 13 projects represented in V12 are not governed by one common license. The exact license must be checked at each pinned source commit and for the exact files used.

Initial checks for the first eight selected projects:

| Project | Initial license evidence | Status |
|---|---|---|
| Ansible | Root `LICENSE` path not found by the initial check; inspect `COPYING`/license files at the pinned commit | Open |
| Black | MIT license file found | Initial check only |
| FastAPI | Official repository states MIT; verify exact pinned commit | Initial check only |
| Keras | Apache-2.0 license file found | Initial check only |
| Luigi | Apache-2.0 license file found | Initial check only |
| Matplotlib | Root `LICENSE` path not found by initial check; inspect repository license directory and file-level notices | Open |
| Pandas | BSD 3-Clause license file found | Initial check only |
| Scrapy | BSD-style license file found; verify exact SPDX identifier and pinned revision | Initial check only |

The remaining V12 projects (spaCy, thefuck, Tornado, tqdm, youtube-dl) also require exact-revision review before use. Some repositories contain file-level exceptions or mixed licensing (for example tqdm's license documentation identifies MIT and MPL-2.0 exceptions).

No upstream source code is to be copied into `MahmutVezir/dijitalikiz`. Tests should execute in temporary checkouts. Store only our own scripts, test harnesses, metadata references, commit IDs, hashes, and lawful research outputs.

## 5. Model license: Qwen2.5-3B-Instruct

The current candidate model `Qwen/Qwen2.5-3B-Instruct` is marked with the Qwen Research License, not Apache-2.0. Qwen's official model information distinguishes Qwen2.5-3B from the Apache-2.0 1.5B model.

- The Qwen Research License is for non-commercial research/evaluation.
- Commercial use requires a separate license.
- Redistribution of model materials or derivatives requires the agreement and attribution notice.
- The research license contains a restriction on using Qwen materials or outputs to improve a different LLM (other than Qwen or its derivatives).

Official model/license references:
- https://qwen.ai/blog?id=qwen2.5-llm
- https://github.com/QwenLM/Qwen/blob/main/Tongyi%20Qianwen%20RESEARCH%20LICENSE%20AGREEMENT
- https://huggingface.co/Qwen/Qwen2.5-3B-Instruct

A non-commercial student research project may fit the research/evaluation grant, subject to the exact license version attached to the pinned model revision. If fine-tuning is performed, keep it as a Qwen derivative and do not use its outputs to train a different LLM. Preserve the license and notice. The 1.5B Instruct model is listed as Apache-2.0 if a more permissive alternative becomes necessary, but changing model size requires a new frozen model/configuration and a fair comparison.

## 6. Human review and consent

The planned two-reviewer ground-truth/evidence panel is not yet approved or recruited.

Before collecting reviewer ratings:
1. Decide whether reviewers are MEB stakeholders or external adults.
2. If MEB stakeholders are in the target group, obtain MEB research approval before data collection.
3. Obtain written voluntary consent from each reviewer; if any under-18 students are participants, obtain parental consent.
4. Collect only the minimum information needed; do not store personal identifiers in the research dataset.
5. Publish only anonymized reviewer IDs and adjudication results, with consent and approvals documented.

## 7. Current legal gate

| Gate | Status |
|---|---|
| TÜBİTAK 2027 eligibility checked | Initial check passed; advisor review required |
| Project originality/student ownership | Must be documented and understood by student |
| Generative AI disclosure plan | Required; not yet added to final report |
| BugsInPy dataset-wide license | **Open / not cleared** |
| Per-upstream project license review | **Open / not complete** |
| Qwen 3B Research License review | Initial check; exact revision notice still to archive |
| Human-review approvals/consents | **Not started** |
| Public redistribution of upstream code/data | **Not authorized** |

**No confirmatory model inference, fine-tuning, or final TÜBİTAK submission is authorized by this document.** The next gate is dataset/legal clearance and the exact-revision license register.
