# 96 adayın kesin durum ayrımı — 16 Kasım 2026

Bu liste başarı olasılığı tahmini değildir. Adayların mevcut kanıt durumunu ve sıkı araştırma havuzuna uygunluğunu gösterir.

## Özet

| Grup | Sayı | Anlamı |
|---|---:|---|
| **Teknik olarak geçti** | 1 | Stage 2 ve Stage 3 teknik değerlendirmesi tamamlandı; nihai kabul ayrı kapıda |
| **Olabilir** | 62 | Sıkı havuzda kalabilir; Stage 2/3 kanıtı bekleniyor veya altyapı/fixture engeli var |
| **Olamaz** | 31 | Kusur değil özellik/iyileştirme, yanlış test oracle'ı veya ikinci tur kapsam denetimi nedeniyle sıkı havuzdan çıkarıldı |
| **Beklemede** | 2 | Şimdilik hold; henüz dışlanmadı ama kabul edilebilir de değil |

## 1. Teknik olarak geçti

- **reagento/dishka #436** — Stage 2 PASS; Stage 3 teknik gold/tier kararı PASS. Nihai kabul henüz yok: araştırmacının kaynak koduna maruz kalması ve tek insan adjudicator sınırlaması açıkça kabul edilmeli; ardından vaka şeması/registry validator geçmeli.

## 2. Olabilir — kanıt bekleyen 62 aday

### Hosted runner tahsisi bekleyen 11 aday

GitHub Actions bunlarda `runner_id=0`, boş runner adı ve `steps=[]` döndürdü. Bunlar teknik test başarısızlığı değildir:

- wntrblm/nox #922 — Runner tahsisi yok; lisans kaynak incelemesi kısmen tamam, exact base/fix test çifti bekliyor.
- getmoto/moto #8296 — Runner tahsisi yok; statik mekanizma güçlü, base/fix test çifti bekliyor.
- pyro-ppl/numpyro #1918 — Runner tahsisi yok; upstream merge SHA düzeltildi, düzeltme sonrası test bekliyor.
- CS-SI/eodag #1536 — Runner tahsisi yok; FAIL_TO_PASS seçicilerinin kusur kapsamı ayrıştırılmalı.
- MarketSquare/robotframework-robocop #1374 — Runner tahsisi yok; row resolver düzeltildi, düzeltme sonrası test bekliyor.
- meltano/sdk #3091 — Runner tahsisi yok; exact row/selectors ve dependency inventory bekliyor.
- amaranth-lang/amaranth #1519 — Runner tahsisi yok; exposure ve test execution bekliyor.
- pallets/werkzeug #2956 — Runner tahsisi yok; ephemeral-port-reserve lock düzeltildi, rerun bekliyor.
- python-control/python-control #1145 — Runner tahsisi yok; exact selectors ve kusur izolasyonu bekliyor.
- qutip/qutip #2694 — Runner tahsisi yok; kaynak derleme ve exact selector çifti bekliyor.
- pyfar/pyfar #722 — Runner tahsisi yok; netCDF4/cftime lock düzeltildi, rerun bekliyor.

### Harici fixture/provenans engeli

- ecmwf/earthkit-data #592 — harici GRIB fixture'ın sabitlenmiş bytes/hash/terms bilgisi ve CF kaynağı provenance'ı çözülmeden Stage 2 başlayamaz.

### Henüz tam Stage 2/3 incelemesi başlamamış diğer 50 aday

- OpenMDAO/dymos #1165 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- skypilot-org/skypilot #5985 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- napalm-automation/napalm #2152 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- PyThaiNLP/pythainlp #1046 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- modin-project/modin #7554 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- capitalone/datacompy #404 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- cta-observatory/ctapipe #2732 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- pallets/click #2788 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- Kozea/WeasyPrint #2416 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- stfc/PSyclone #2767 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- mpmath/mpmath #902 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- astropy/ccdproc #901 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- asdf-format/asdf #1907 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- msgspec/msgspec #772 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- pallets/jinja #2033 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- jsonpickle/jsonpickle #565 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- scikit-activeml/scikit-activeml #504 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- geofileops/geofileops #649 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- lektor/lektor #1214 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- cuthbertLab/music21 #1736 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- geopandas/geopandas #3591 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- python-babel/babel #1141 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- gammapy/gammapy #5525 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- joshuadavidthomas/django-bird #219 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- ApeWorX/web3.py #3690 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- PyPSA/linopy #438 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- jazzband/tablib #613 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- twisted/towncrier #696 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- litestar-org/polyfactory #728 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- pyccel/pyccel #2038 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- python-attrs/attrs #1417 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- StingraySoftware/stingray #858 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- softlayer/softlayer-python #2214 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- pypa/virtualenv #2907 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- crewAIInc/crewAI #2408 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- narwhals-dev/narwhals #1869 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- callowayproject/bump-my-version #325 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- dynaconf/dynaconf #1293 — Geçici aday; henüz exact Stage 2 base/fix çifti kanıtlanmadı.
- Diaoul/subliminal #1218 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- astanin/python-tabulate #362 — Statik taramada güçlü aday; Stage 2 exact base/fix reproduction ve sonra Stage 3 gerekiyor.
- copier-org/copier #1998 — Statik taramada güçlü aday; Stage 2 exact base/fix reproduction ve sonra Stage 3 gerekiyor.
- packit/packit #2556 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- matthewwithanm/python-markdownify #202 — Statik taramada güçlü aday; Stage 2 exact base/fix reproduction ve sonra Stage 3 gerekiyor.
- drivendataorg/cloudpathlib #474 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- gtalarico/pyairtable #422 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- stanfordnlp/dspy #1853 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- joke2k/faker #2203 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.
- scverse/PyDESeq2 #349 — Statik taramada güçlü aday; Stage 2 exact base/fix reproduction ve sonra Stage 3 gerekiyor.
- mitmproxy/pdoc #813 — Statik taramada güçlü aday; Stage 2 exact base/fix reproduction ve sonra Stage 3 gerekiyor.
- aws-cloudformation/cfn-lint #3991 — Koşullu aday; belirtilen kapsam/fixture/issue–patch riski çözülürse devam.

## 3. Olamaz — sıkı havuzdan çıkarılan 31 aday

### İkinci tur oracle/kapsam denetimiyle çıkarılan 2 aday

- databricks/dbt-databricks #995 — test oracle bildirilen cleanup/UUID kusurunu yakalamıyor.
- simpeg/simpeg #1633 — issue'daki beklenen davranış ile PR'nin yaptığı değişiklik/test oracle'ı uyuşmuyor.

### İlk statik kapsam taramasında dışlanan 29 aday

- aristanetworks/anta #956 — Exclude from primary bug-root-cause pool: test-suite correction rather than a production-code defect fix
- theupdateframework/python-tuf #2808 — Exclude from strict bug pool: classified as enhancement; retain provenance only
- googleapis/python-bigquery #2140 — Exclude from strict bug pool: feature addition
- GoogleCloudPlatform/cloud-sql-python-connector #1221 — Exclude from strict bug pool: feature addition
- dwavesystems/dwave-system #554 — Exclude from strict bug pool — feature/API addition
- PrefectHQ/fastmcp #164 — Exclude from strict bug pool — new API behavior/enhancement, not a demonstrated regression
- dpkp/kafka-python #2544 — Exclude from strict bug pool — feature addition
- PennyLaneAI/pennylane #6738 — Exclude from strict bug pool — API feature addition
- SQLMesh/sqlmesh #3654 — Dışla: improvement/feature
- terrapower/armi #2121 — Dışla: feature request
- CrossGL/crosstl #201 — Dışla: enhancement
- CTFd/CTFd #2767 — Dışla: özellik/iyileştirme
- jax-ml/jax #25650 — Dışla: enhancement/yeni destek
- sparckles/Robyn #1002 — Dışla: özellik geliştirme
- skrub-data/skrub #1445 — Dışla: enhancement
- cogent3/cogent3 #2050 — Dışla: yeni özellik
- pybamm-team/PyBaMM #4465 — Dışla: feature
- scikit-rf/scikit-rf #1282 — Dışla: feature request
- vacanza/holidays #2106 — Dışla: veri/içerik düzeltmesi
- silx-kit/silx #4282 — Exclude — feature/usability enhancement
- sissbruecker/linkding #984 — Exclude — explicitly requested new feature
- pydap/pydap #481 — Exclude — API naming/consistency migration, not a demonstrated defect
- microsoft/AzureTRE #4352 — Exclude — feature request / new endpoint and UI
- aiogram/aiogram #1657 — Exclude — enhancement / convenience API
- apiflask/apiflask #642 — Exclude — interoperability option/enhancement; keep NOTICE obligations
- XKNX/xknx #1663 — Exclude — explicit feature request
- pyjanitor-devs/pyjanitor #1451 — Exclude — explicitly proposed alias convenience API
- frictionlessdata/frictionless-py #1729 — Exclude — request to add a new configurable capability
- benavlabs/fastcrud #190 — Exclude: composite multi-issue PR

## 4. Beklemede — 2 hold

- OceanParcels/Parcels #1723 — olası bugfix; kapsam ve kanıt ayrıştırması gerekli.
- mikedh/trimesh #2312 — geniş release/çoklu değişiklik PR'si; hedef kusur izole edilmeden kabul edilemez.

## 5. Kaggle çalıştırma durumu

- Hazır notebook, workflow'un sabitlenmiş `13c598915f23378c6d586c8f3686be4054e0261f` commit'indeki `run:` adımlarını Kaggle CPU üzerinde yürütür.
- 13 workflow işini (genel no-inference preflight + 12 aday işi) ayrı worktree'lerde çalıştırır; bir adaydaki hata diğerlerini durdurmaz.
- Internet ON, GPU None; model inference/eğitim yok.
- Çıktı ZIP'i yüklenince her adayın base/fix loglarını inceleyip Stage 2'yi geçip geçmediğini belirleyeceğiz. Stage 3 insan adjudication'ı ayrıca yapılacak.

## Yöntem notu

Stage 2 PASS için aynı test/reproducer buggy base'te kusura özgü biçimde başarısız, fixed revision'da başarılı olmalı. Runner/bağımlılık/fixture/collection hatası bu şartı karşılamaz. Stage 3, gold root cause, alternatifler ve E1/E2/E3 kanıt üyelikleri için ayrı teknik ve insan değerlendirmesidir. Nihai vaka kabulü bunlardan da ayrıdır.

**Şu an kabul edilmiş vaka sayısı: 0.** Dishka'nın Stage 2+3 teknik geçişi var ama nihai kabul kaydı henüz kapatılmadı.
