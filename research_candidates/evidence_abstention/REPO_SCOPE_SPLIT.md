# DİJİTALİKİZ deposunun yeni araştırma için kapsam ayrımı

**Yeni çalışma:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Kapsam ayrımı tarihi:** 20 Ekim 2026  
**Geçerli dal:** `research/evidence-abstention-draft-2026-10-19`

## Neden bu ayrım var?

Bu GitHub deposu ilk olarak farklı bir çalışma için oluşturuldu: LLM tabanlı çapraz-bileşen hata teşhisi ve TÜBİTAK 2204-A raporlaması. Yeni çalışma farklı bir araştırma sorusuna sahip. Aynı depoyu teknik ve belgelendirme altyapısı olarak kullanabiliriz; ancak eski deneylerin verisini, model çıktılarını, metriklerini ve sonuçlarını yeni projenin kanıtı gibi kullanamayız.

Bu dosya ve iki JSON manifesti, eski dosyaları taşımadan/silmeden **bilimsel bir kapsam sınırı** kurar. Eski deneyin kayıtları korunur. Klasör ve dosya adları aşağıda açıkça sınıflandırılmıştır. Taşıma/silme yapılmamasının nedeni, eski deneyin CI/artefakt ve teslim bağlantılarını kırmamak; ayrım, iki kontrollü dizin ve bu kapsam manifesti üzerinden uygulanır.

**Aşama durumu:** Aşama 1 hedefli literatür denetimi tamamlandı; Aşama 2 kaynak fizibilitesi tamamlandı ancak doğrulayıcı örneklem hazır değil; Aşama 3 deney tasarımı tamamlandı. Bir BugsInPy-tqdm smoke testi CI'da buggy-fail/fixed-pass verdi, ancak Python sürümü dataset metadata'sıyla eşleşmedi ve vaka incelemeye maruz kaldığı için ana örneklemden dışlandı. Model çıkarımı kapalıdır.

## Bölüm A — Bu proje için kullanılabilecekler

### A1. Yeni projeye ait birincil dokümantasyon

Aşağıdaki dosyalar yeni projenin araştırma planı ve karar kayıtlarıdır:
- `research_candidates/evidence_abstention/README.md`
- `research_candidates/evidence_abstention/LITERATURE_REVIEW.md`
- `research_candidates/evidence_abstention/DATA_FEASIBILITY.md`
- `research_candidates/evidence_abstention/PROTOCOL_DRAFT.md`
- `research_candidates/evidence_abstention/FEASIBILITY_FORMAT_SAMPLE.csv` — sadece metadata şeması/format örneği. CSV'deki dört BugsInPy örneği doğrulayıcı veri kümesine alınamaz.
- Bu dizine eklenen `REPO_SCOPE_SPLIT.md`, `STAGE3_EXPERIMENT_DESIGN.md`, `PROMPT_CONDITIONS.md`, `OUTPUT_SCHEMA.json`, `ANALYSIS_PLAN_STAGE3.md`, `EXPERIMENT_MANIFEST_STAGE3.json` ve `STAGE3_REVIEW_AND_EXIT.md`.
- `USE_FOR_THIS_PROJECT/` içinde yeni projenin izinli dokümantasyonunun erişilebilir kopyaları bulunur; `DO_NOT_USE_AS_EVIDENCE/` içinde eski veri/sonuçların bu yeni projede kullanılmasını yasaklayan kapsam kaydı bulunur. Eski kaynak dosyalar tarihsel izlenebilirlik için yerlerinde kalır.

`USE_FOR_THIS_PROJECT/` dizini yeni araştırmaya ait belgelerin erişimi kolaylaştırılmış kopyalarını, yeniden kullanım politikasını ve [MANIFEST.json](USE_FOR_THIS_PROJECT/MANIFEST.json) izin kaydını içerir. `DO_NOT_USE_AS_EVIDENCE/` ise dışlanan tarihsel materyallerin [MANIFEST.json](DO_NOT_USE_AS_EVIDENCE/MANIFEST.json) kaydını içerir. Çelişki olursa doğrudan üst dizindeki tarihli, yetkili doküman dikkate alınır.

### A2. Yeni, bağımsız hata vakaları için kaynak

- Upstream BugsInPy deposu: https://github.com/soarsmu/BugsInPy
- Sayımın yapıldığı BugsInPy revizyonu: `11c5f1eea954a42132cfd06bf257766a7963e0fd`
- Yalnızca kaynağı, lisansı, buggy/fixed revizyonları, tetikleyici testi ve kök nedeni ayrıca doğrulanan yeni vakalar kullanılabilir.
- Kaynak kodu veya düzeltme yamasını bu depoya topluca kopyalamak yerine yalnızca gereken metadata, atıf, test günlüklerinin özeti ve içerik hash'leri tutulur.
- `BugsInPy-black-1`, `BugsInPy-tqdm-1`, `BugsInPy-httpie-1`, `BugsInPy-youtube-dl-1` vakaları patch/metadata inceleme örneği olarak açıldı; doğrulayıcı analizden dışlanır.
- `BugsInPy-PySnooper-1` CI smoke denemesinde buggy revision testten geçtiği için beklenen hata yeniden üretilemedi; ana örneklemden kalıcı dışlanır.
- `BugsInPy-tqdm-1` ilk smoke koşusu import/geçiş sorunu nedeniyle başarısız oldu. Kaynak checkout'u açıkça import edecek şekilde düzeltilen sonraki [CI koşusu](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759) buggy-fail/fixed-pass verdi; ancak runtime Python 3.8.18 iken metadata Python 3.6.9 kaydediyor. Üstelik vaka patch/metadata incelemesine maruz kaldığı için ana örneklemden kalıcı dışlanır.

### A3. Yalnızca yöntem fikri/şablonu olarak incelenebilecek eski dosyalar

- `docs/ANALYSIS_PLAN.md`
- `docs/SCORING_RUBRIC_CALIBRATION_PROTOCOL.md`
- `docs/SEMANTIC_SCORING_REVIEW_PROTOCOL.md`
- `docs/CONTAMINATION_AUDIT.md`
- `docs/CANDIDATE_SOURCE_AUDIT_2026-10-10.md`
- `docs/DATA_COLLECTION_PROTOCOL.md`
- `docs/POWER_PLANNING.md`
- `schemas/` ve `tests/` altındaki doğrulama örüntüleri
- `scripts/power_mcnemar.py` gibi genel hesaplama örnekleri

Bu dosyalar yalnızca bağımsız yöntem tasarımı için okunabilir. Eski vakalar, etiketler, analiz sonuçları, görev varsayımları ve proje-özel kod doğrudan taşınamaz. Her kod uyarlaması yeniden gözden geçirilmeli, test edilmeli ve yeni çalışmanın protokolüne göre yazılmalıdır.

### A4. Sınırlı, izinli CI kullanımı

- `.github/workflows/evidence-abstention-case-smoke.yml`: yalnızca kilitlenmiş vaka için test-fail/test-pass çiftini yeniden üretme amaçlıdır. LLM çağrısı yoktur ve bu smoke vakası ana örnekleme girmez.
- Eski CI dosyalarının hiçbirini bu yeni deney için otomatik çıkarım başlatmak üzere kullanma. Yeni deney pipeline'ı ancak vaka doğrulaması, lisans/sızıntı incelemesi, model/prompt dondurması ve önceden kaydedilmiş analiz planı kapandıktan sonra ayrıca geliştirilecektir.

## Bölüm B — Bu projede bilimsel veri/sonuç olarak kullanılamayacaklar

### B1. Eski proje verileri ve vaka havuzları

Aşağıdaki yollar yeni araştırmanın vaka havuzuna, pilotuna, kalibrasyonuna veya doğrulayıcı analizine taşınamaz:
- `data/benchmark/**`
- `data/calibration/**`
- `data/candidates/**`
- `data/candidate_case_drafts/**`
- `data/pilot/**`
- `data/followup_v2/**`
- `data/incident_audits/**`
- `RSC-Bench-pilot-v1.0-stage4-gated/**`
- `RSC-Bench-pilot-v1.0-stage4-gated.zip`
- `rsc-bench-v0.1.zip`
- `kaggle/confirmatory_kernel.py`

Bu kayıtlar önceki çalışmanın parçasıdır; bazıları kalibrasyon veya önceden görülmüş vaka içerebilir. Üzerlerine yeni etiket yazmak, yeniden adlandırmak ya da yeni projeye aitmiş gibi göstermek yasaktır.

### B2. Eski kodun doğrudan deney/puanlama motoru olarak kullanılması

Aşağıdaki eski paket/iş akışları yeni deneyin koşulu, prompt'u, veri işleyicisi veya çıktı puanlayıcısı olarak doğrudan çalıştırılamaz:
- `dijitalikiz/context.py`, `context_v2.py`, `evaluation.py`, `candidate_assessment.py`, `pilot_config.py`
- `scripts/run_pilot.py`, `scripts/run_confirmatory.py`, `scripts/evaluate_pilot.py`, `scripts/evaluate_confirmatory.py`, `scripts/finalize_pilot.py`, `scripts/finalize_confirmatory.py`
- `scripts/build_pilot_*`, `scripts/build_confirmatory_*`, `scripts/validate_*benchmark*`, `scripts/validate_*calibration*`, `scripts/analyze_followup_v2.py`
- `schemas/benchmark_manifest.schema.json`, `schemas/research_case.schema.json` ve diğer eski proje şemaları eski veriyle birlikte yeni çalışmaya kopyalanamaz. Yalnızca bir gereksinim örüntüsü olarak okunabilirler.

### B3. Eski sonuçlar/raporlar yeni projenin sonucu değildir

Aşağıdaki belgeler geçmiş çalışmanın veya TÜBİTAK teslim hazırlığının tarihsel kaydıdır; yeni projede sonuç kanıtı veya literatür kaynağı yerine kullanılamaz:
- `docs/CONFIRMATORY_RESULTS_2026-10-09.md`
- `docs/HISTORICAL_EXPERIMENT_SCIENTIFIC_AUDIT_2026-10-15.md`
- `docs/PILOT_*.md`, `docs/FINAL_*.md`
- `docs/TUBITAK_*.md`
- `docs/RESEARCH_PATH_DECISION_2026-10-15.md`
- `data/benchmark/confirmatory_result_summary.json`
- Eski Kaggle/Actions inference çıktıları, arşivleri ve metrikleri.

Eski çalışmanın 160 kayıtlık confirmatory sonucu ve diğer ölçümleri yeni projenin örneklemine katılmaz, yeni projenin hipotezini destekleyen kanıt gibi gösterilmez ve yeni sonuçlarla birleştirilmez.

## Karar kuralı

Bir dosyanın “kullanılabilir” olması, doğrudan deneyde kullanılması anlamına gelmez. Yeni veri olarak kullanılacak her vaka için veri kökeni, lisans, buggy/fixed test, kök neden, E1/E2/E3 kanıt paketi, kontaminasyon riski ve dosya hash'leri ayrıca doğrulanmalıdır. Bu kapılar kapanana kadar **LLM inference kapalıdır**.

**Koruma ilkesi:** Bu ayrım eski depoyu silmez, geçmiş sonuçları düzeltmez ve `main` dalını değiştirmez; yalnızca yeni araştırmada neyin kullanılabileceğini açıklar.


## Aşama 2 metadata envanteri otomasyonu

21 Ekim 2026'da eklendi: scripts/inventory_bugsinpy_candidates.py, onun birim testleri ve .github/workflows/evidence-abstention-metadata-inventory.yml. Bu iş akışı yalnızca pinned BugsInPy metadata alanlarını ve hash'lerini envantere çıkarır; bug/fixed testlerini çalıştırmaz ve vaka kabul etmez. Kapsam sınırı aynı kalır: yeni araştırmada tarihsel DİJİTALİKİZ verileri/sonuçları kullanılmaz; kabul edilmiş vaka sayısı henüz 0'dır.


## Tek aktif hedef kararı — 21 Ekim 2026

Bu araştırma dalının tek aktif hedefi **2027 TÜBİTAK 2204-A'da finalistlik düzeyinde, tamamlanmış ve bilimsel olarak savunulabilir bir proje sunmaktır**. Başka yarışma veya ayrı araştırma hattı bu çalışmanın yürütme gündeminde değildir. Uygulama planı: [TUBITAK_2204A_MASTER_PLAN_2026-10-21.md](TUBITAK_2204A_MASTER_PLAN_2026-10-21.md).

TÜBİTAK'ın [resmî 2026–2027 çağrı sayfası](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi), başvuru kapanışını 4 Ocak 2027 saat 17.30 olarak belirtir ve fikir aşamasındaki veya devam etmekte olan projelerle başvuru yapılmaması gerektiğini söyler. Bu nedenle araştırma planı hazır olması tamamlanma sayılmaz.

Bu karar eski DİJİTALİKİZ deney kayıtlarının silinmesini, değiştirilmesini veya yeni çalışmanın kanıtı olarak yeniden kullanılmasını gerektirmez. Tarihsel deney kaynakları değişmeden korunur; yeni çalışma için yalnızca bağımsız doğrulaması yapılan vakalar kullanılabilir. Ana dalın eski araştırma durumu korunur; bu düzenlemeler yalnızca araştırma dalında yapılmıştır.

2026-10-21 itibarıyla accepted confirmatory cases = 0 ve yeni çalışma için LLM inference = false. Model deneyi, veri ve değerlendirme kapıları kapanana kadar başlatılmayacaktır.
