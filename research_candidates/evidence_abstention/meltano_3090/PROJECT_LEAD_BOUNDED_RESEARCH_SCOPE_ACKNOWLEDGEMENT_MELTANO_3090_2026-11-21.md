# Project-Lead Bounded Research-Scope Acknowledgement — Meltano SDK #3090

Date: 2026-11-21  
Project: TÜBİTAK 2204-A — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
Candidate: meltano/sdk issue #3090 / fix PR #3091  
Dataset instance: `meltano__sdk-3091`

## Decision

The project lead acknowledges and accepts **in principle** the proposed bounded research-use scope, with the restrictions and open checks below.

The project lead's decision, recorded verbatim:

> Evet. Meltano #3090 için önerilen sınırlı araştırma kullanım kapsamını, belirtilen kısıtlarla ilke olarak kabul ediyorum. Bu karar; açık lisans, bağımlılık, bildirim ve provenans incelemelerinin tamamlandığı, hukuki izin alındığı, vakanın nihai olarak kabul edildiği veya model çıkarımına izin verildiği anlamına gelmez. Bu kontroller tamamlanmadan tam kaynak kodu, veri kümesi veya bağımlılıkların yeniden dağıtımı yapılmayacaktır.

Decision status: `bounded_research_scope_acknowledged_in_principle_with_open_verification_gates`.

## Acknowledged bounded scope

The intended work is limited to this single Meltano defect and the single selected dataset row. The scope is restricted to:

- minimal issue, test, and source excerpts necessary to explain or reproduce the defect;
- immutable upstream commit and artifact references with appropriate attribution;
- small factual test outputs and cryptographic hashes needed to audit the reproduction.

The following remain excluded:

- redistribution of the complete Meltano repository or complete dataset;
- redistribution of dependency wheels, native libraries, binaries, or a complete environment image;
- republication of third-party dependency source trees or notices beyond what is necessary and lawfully included;
- any blanket commercial-use permission or assumption that the root repository license settles every dependency's terms.

Any excerpt or item actually used must retain applicable attribution and notices. Immutable upstream links should be preferred over copying source files. The selected data row and evidence excerpts must remain minimal, and exact third-party components and notices actually used must be recorded.

## Conditions that remain open

This acknowledgement does not close any of the following:

1. **Dataset-card provenance:** The current Hub metadata displays CC-BY-4.0, while the dataset row's upstream-repository license field says Apache-2.0. The full immutable README/card commit SHA and exact raw README bytes/SHA-256 for the relevant data revision remain uncaptured. These license layers must remain distinct.
2. **Dependency scope:** The recorded test environment contains 32 distribution entries. Eight have null raw license fields; two lack license classifiers; some metadata has multiple classifiers. Canonical license texts/notices and the exact relevant transitive dependency scope remain subject to human review.
3. **Notices and source provenance:** Applicable upstream and third-party notices, the exact source/card relationship, and the provenance of any copied excerpt must be reconciled before relying on those materials beyond immutable references.
4. **Legal review:** No external legal review has been performed. This is not legal advice, a legal opinion, SPDX certification, legal clearance, or a grant of rights by any upstream or dataset rights holder.

Until the open checks are completed, this acknowledgement does **not** authorize redistribution of complete source code, the dataset, dependency packages, binaries, or environment images. It does not override any applicable license or create permission where none exists.

## Scientific-independence and acceptance boundaries

The acknowledgement concerns only the project's intended bounded documentary scope. It does not change the technical gold mechanism, E1/E2/E3 decisions, evidence labels, or scientific results. A licensing concern must be handled by pausing or narrowing the affected material, not by changing scientific labels to fit a permission conclusion.

This acknowledgement is **not**:
- final acceptance of Meltano #3090 into the v0.2 exploratory registry;
- confirmation that all source, dataset, dependency, notice, or provenance checks passed;
- legal clearance or permission for blanket redistribution or commercial use;
- authorization to load model weights, run inference, fine-tune, or train.

Meltano remains outside the accepted registry. The accepted exploratory count remains 2 cases from 2 distinct upstream projects. A separate final project-lead YES/NO case-acceptance decision remains required after the proposed case record and fail-closed validation are complete. Study-wide model execution remains unauthorized.

## Recorded by

Student project lead, by explicit confirmation in the project conversation on 2026-11-21. The record reflects the scope acknowledgement as stated; it does not claim an external legal determination or independent audit.
