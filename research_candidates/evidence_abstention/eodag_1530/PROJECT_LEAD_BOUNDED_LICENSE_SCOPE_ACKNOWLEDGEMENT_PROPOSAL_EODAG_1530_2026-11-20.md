# Project-lead bounded documentary scope acknowledgement proposal — EODAG #1530

Date: 20 November 2026  
Candidate: CS-SI/eodag issue #1530 / PR #1536

## Proposed scope

A narrow educational/scientific study of one EODAG duplicate-key configuration defect, one immutable SWE-rebench dataset row (`cs-si__eodag-1536`), and the exact pinned CPU-only reproduction. The study may retain the canonical selected row and minimal source excerpts needed to explain the defect, link to immutable upstream revisions, and cite the dataset repository. Upstream EODAG attribution and the applicable `NOTICE` content must be preserved where required for any retained or distributed upstream source materials. The dataset attribution must be kept distinct from the row-level EODAG Apache-2.0 source license.

## Identified documentary facts

- Upstream EODAG root license at the exact base: Apache-2.0.
- Exact-base `setup.cfg` declares Apache 2.0 and `LICENSE`.
- Exact-base `NOTICE` contains third-party attribution/license information.
- The selected row's `license` field is Apache-2.0 for the upstream EODAG repository; it is not the dataset repository's license.
- The exact pinned dataset revision is recorded as CC-BY-4.0.
- The focused CPU reproduction environment resolved 52 distributions. The artifact records metadata for all 52 and passed `pip check`; metadata presence is not a full notice, native-library, SPDX or legal review.
- PyArrow 19.0.1 was used in a separate environment to extract the Parquet row; it is not part of the 52-distribution source-test runtime.
- The public repository and CI artifacts are publicly accessible; they are not private-only.

## Explicit exclusions proposed

- No redistribution of the complete SWE-rebench dataset.
- No redistribution of the complete EODAG repository.
- No redistribution of installed wheels, binary packages, native libraries, or the full 52-package environment.
- No claim of blanket permission for optional EODAG extras, external provider data, or commercial product use.
- No legal-clearance or formal legal-review claim.

## Scientific-independence condition

This acknowledgement would be limited to the factual scope and boundaries above. It must not alter the gold mechanism, evidence tiers, case labels, dataset results, or model responses. If a material licensing or redistribution concern is found, pause the affected artifact/activity and review it separately; do not modify scientific outcomes to fit the licensing position.

## Decision requested

Please acknowledge this bounded scope only if it accurately describes the intended research and distribution boundaries. This is not legal advice, legal clearance, or formal legal review. The case remains unaccepted; schema/registry validation and a separate final YES/NO decision are still required. Model execution remains unauthorized.
