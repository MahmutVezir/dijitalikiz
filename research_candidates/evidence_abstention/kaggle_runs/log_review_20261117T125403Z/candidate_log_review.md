# 11 Aday Kaggle Log İncelemesi

- Run ID (UTC): `20261117T125403Z`
- Kaynak ZIP SHA-256: `b4b8b536e82e7ac93e94bbb51d63f71185a2b7ab2515178480189f8cf783b777`
- ZIP CRC bütünlüğü: **PASS**
- Model yükleme/çıkarım/eğitim: **YOK**
- Otomatik vaka kabul kararı: **YOK**

> Ön sınıflandırma etiketleri yalnızca log taramasına dayalı triyajdır. Başarısız job tek başına adayın geçersiz olduğunu göstermez.

| Aday job | Başarısız adım | Ön kategori | Bulunan/eksik artifact |
|---|---|---|---|
| `nox-issue-919-reproduction` | Clone exact upstream source and prepare pinned patch | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/14 |
| `numpyro-issue-1916-reproduction` | Run dataset FAIL_TO_PASS selectors on buggy base (failure required) | `test_step_failed_cause_unresolved` | 0/12 |
| `werkzeug-issue-2955-reproduction` | Run dataset FAIL_TO_PASS selectors on buggy base (failure required) | `test_step_failed_cause_unresolved` | 0/10 |
| `robocop-issue-1371-reproduction` | Clone exact upstream source and prepare pinned patch | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/7 |
| `pyfar-issue-721-reproduction` | Run dataset FAIL_TO_PASS selectors on buggy base (failure required) | `test_step_failed_cause_unresolved` | 0/10 |
| `eodag-issue-1530-reproduction` | Clone and authenticate exact upstream source snapshots | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/5 |
| `moto-issue-8269-reproduction` | Clone exact Moto source and prepare patch | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/2 |
| `meltano-issue-3090-reproduction` | Clone exact Singer SDK source and authenticate license | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/5 |
| `python-control-issue-1144-reproduction` | Run exact dataset selectors on patched buggy base (failure required) | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/11 |
| `qutip-issue-2646-reproduction` | Apply exact PR patch and run dataset selectors on buggy base (failure required) | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/11 |
| `amaranth-issue-1518-reproduction` | Clone exact Amaranth source and prepare patch | `source_checkout_or_patch_step_failed_cause_unresolved` | 0/5 |

## nox-issue-919-reproduction

- Başarısız adım: Clone exact upstream source and prepare pinned patch
- Atlanan adımlar: Run independent issue reproducer on buggy base (failure required), Run dataset FAIL_TO_PASS selectors on buggy base (failure required), Run independent issue reproducer and dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 14 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dependency-groups-pyproject.toml`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/attrs-pyproject.toml`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/attrs-LICENSE`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/DEPENDENCY_GROUPS_1_3_0_LICENSE_REVIEW_2026-11-16.md`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dependency-groups-LICENSE.txt`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/attrs-source-commit.txt`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dataset-test.patch`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/dependency-groups-source-commit.txt`
- `collected_artifacts/nox-issue-919-reproduction/nox-issue-919-reproduction/reproduction-evidence/ATTRS_24_3_0_LICENSE_REVIEW_2026-11-16.md`

## numpyro-issue-1916-reproduction

- Başarısız adım: Run dataset FAIL_TO_PASS selectors on buggy base (failure required)
- Atlanan adımlar: Run identical dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 12 eksik
- Ön kategori: `test_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/base-commit.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/fixed-commit.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/environment-lock-sha256.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/test-environment-freeze.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/base-dataset-test.log`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/source-and-dataset-sha256.txt`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/numpyro-issue-1916-reproduction/numpyro-issue-1916-reproduction/reproduction-evidence/dataset-test.patch`

## werkzeug-issue-2955-reproduction

- Başarısız adım: Run dataset FAIL_TO_PASS selectors on buggy base (failure required)
- Atlanan adımlar: Run identical dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 10 eksik
- Ön kategori: `test_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/environment-lock-sha256.txt`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/test-environment-freeze.txt`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/base-dataset-test.log`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/source-and-dataset-sha256.txt`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/werkzeug-issue-2955-reproduction/werkzeug-issue-2955-reproduction/reproduction-evidence/dataset-test.patch`

## robocop-issue-1371-reproduction

- Başarısız adım: Clone exact upstream source and prepare pinned patch
- Atlanan adımlar: Run dataset FAIL_TO_PASS selectors on buggy base (failure required), Run identical dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 7 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/test-environment-freeze.txt`
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/robocop-issue-1371-reproduction/robocop-issue-1371-reproduction/reproduction-evidence/dataset-test.patch`

## pyfar-issue-721-reproduction

- Başarısız adım: Run dataset FAIL_TO_PASS selectors on buggy base (failure required)
- Atlanan adımlar: Run identical dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 10 eksik
- Ön kategori: `test_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/environment-lock-sha256.txt`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/test-environment-freeze.txt`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/base-dataset-test.log`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/source-and-dataset-sha256.txt`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/pyfar-issue-721-reproduction/pyfar-issue-721-reproduction/reproduction-evidence/dataset-test.patch`

## eodag-issue-1530-reproduction

- Başarısız adım: Clone and authenticate exact upstream source snapshots
- Atlanan adımlar: Run identical issue reproducer on buggy base (failure required), Run identical issue reproducer on fixed revision (pass required), Extract exact dataset row and record FAIL_TO_PASS selectors without executing upstream tests
- Artifact: 0 bulundu; 5 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/eodag-issue-1530-reproduction/eodag-issue-1530-reproduction/reproduction-evidence/base-user_conf_template.yml`
- `collected_artifacts/eodag-issue-1530-reproduction/eodag-issue-1530-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/eodag-issue-1530-reproduction/eodag-issue-1530-reproduction/reproduction-evidence/issue-1530-source.patch`
- `collected_artifacts/eodag-issue-1530-reproduction/eodag-issue-1530-reproduction/reproduction-evidence/upstream-NOTICE.txt`
- `collected_artifacts/eodag-issue-1530-reproduction/eodag-issue-1530-reproduction/reproduction-evidence/upstream-LICENSE.txt`

## moto-issue-8269-reproduction

- Başarısız adım: Clone exact Moto source and prepare patch
- Atlanan adımlar: Run independent issue reproducer on buggy base (failure required), Run exact dataset FAIL_TO_PASS selectors on patched buggy base (failure required), Run same issue reproducer and dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 2 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/moto-issue-8269-reproduction/moto-issue-8269-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/moto-issue-8269-reproduction/moto-issue-8269-reproduction/reproduction-evidence/dependency-license-inventory.json`

## meltano-issue-3090-reproduction

- Başarısız adım: Clone exact Singer SDK source and authenticate license
- Atlanan adımlar: Run independent source reproducer on buggy base (failure required), Extract exact dataset row and authenticate timestamp, Run exact dataset selectors on patched buggy base (failure required), Run same source and dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 5 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/meltano-issue-3090-reproduction/meltano-issue-3090-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/meltano-issue-3090-reproduction/meltano-issue-3090-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/meltano-issue-3090-reproduction/meltano-issue-3090-reproduction/reproduction-evidence/pr-3091.patch`
- `collected_artifacts/meltano-issue-3090-reproduction/meltano-issue-3090-reproduction/reproduction-evidence/upstream-pyproject.toml`
- `collected_artifacts/meltano-issue-3090-reproduction/meltano-issue-3090-reproduction/reproduction-evidence/upstream-LICENSE.txt`

## python-control-issue-1144-reproduction

- Başarısız adım: Run exact dataset selectors on patched buggy base (failure required)
- Atlanan adımlar: Run same reproducer and dataset selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 11 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/source-provenance-sha256.txt`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/dataset-extraction-license-inventory.json`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/upstream-pyproject.toml`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/upstream-LICENSE.txt`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/base-issue-test.log`
- `collected_artifacts/python-control-issue-1144-reproduction/python-control-issue-1144-reproduction/reproduction-evidence/pr-1145.patch`

## qutip-issue-2646-reproduction

- Başarısız adım: Apply exact PR patch and run dataset selectors on buggy base (failure required)
- Atlanan adımlar: Run same reproducer and selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 11 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/dataset-row-sha256.txt`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/pr-2694.patch`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/source-provenance-sha256.txt`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/dataset-extraction-license-inventory.json`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/dataset-fail-to-pass-selectors.txt`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/upstream-pyproject.toml`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/dataset-row-canonical.json`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/upstream-LICENSE.txt`
- `collected_artifacts/qutip-issue-2646-reproduction/qutip-issue-2646-reproduction/reproduction-evidence/base-issue-test.log`

## amaranth-issue-1518-reproduction

- Başarısız adım: Clone exact Amaranth source and prepare patch
- Atlanan adımlar: Run independent RTLIL reproducer on buggy base (failure required), Extract and authenticate exact dataset row, Apply exact PR patch and run dataset selectors on buggy base (failure required), Run same reproducer and selectors on fixed revision (pass required)
- Artifact: 0 bulundu; 5 eksik
- Ön kategori: `source_checkout_or_patch_step_failed_cause_unresolved`

Eksik artifact yolları:
- `collected_artifacts/amaranth-issue-1518-reproduction/amaranth-issue-1518-reproduction/reproduction-evidence/SHA256SUMS.txt`
- `collected_artifacts/amaranth-issue-1518-reproduction/amaranth-issue-1518-reproduction/reproduction-evidence/pr-1519.patch`
- `collected_artifacts/amaranth-issue-1518-reproduction/amaranth-issue-1518-reproduction/reproduction-evidence/dependency-license-inventory.json`
- `collected_artifacts/amaranth-issue-1518-reproduction/amaranth-issue-1518-reproduction/reproduction-evidence/upstream-pyproject.toml`
- `collected_artifacts/amaranth-issue-1518-reproduction/amaranth-issue-1518-reproduction/reproduction-evidence/upstream-LICENSE.txt`
