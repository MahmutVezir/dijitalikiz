# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tek aktif hedef:** 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde, tamamlanmış ve bilimsel olarak savunulabilir bir araştırma sunmak. Finalistlik garanti edilemez; ölçütümüz gerçek kanıt ve dürüst raporlamadır.

**Güncel bilimsel durum (21 Ekim 2026):** Proje tamamlanmadı. Aşama 1 hedefli literatür ve araştırma sorusu taslağı bakımından ilerledi; sistematik derleme, protokol dondurma ve ön kayıt tamamlanmadı. Aşama 2 metadata envanteri koşullu tamamlandı: BugsInPy revizyonunda 501 ham kayıt/17 proje, 500 temel metadata-kalifiye kayıt ve 1 commit tutarsızlığı bulundu. 487 satırlı tarama kuyruğundan V5 alım sırası ilk 32 maruziyet/teknik hata vakasını atlayarak 120 aday belirler; bu adaylar test/lisans/kök neden/kanıt incelemesi tamamlanmadan kabul edilmiş sayılmaz. Kabul edilmiş bağımsız vaka sayısı hâlâ 0'dır; model çıkarımı kapalıdır.

**Tek yürütme planı:** [TÜBİTAK 2204-A ana planı](TUBITAK_2204A_MASTER_PLAN_2026-10-21.md). Resmî başvuru son tarihi 4 Ocak 2027, saat 17.30’dur; [TÜBİTAK 2204-A çağrısı](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi).

**Depo kullanımı:** Bu depo, yeni projenin planlama, sürüm kontrolü, doğrulama ve belgelendirme altyapısı olarak kullanılacaktır. Çalışma ayrı bir dalda yürütülür; DİJİTALİKİZ'in tarihsel TÜBİTAK 2204-A deneyleri, sonuçları, manifestleri ve raporu değiştirilmez.

## Resmî proje adı

**Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ**

## Çalışmanın kapsamı

Proje, gerçek yazılım hatalarının kök nedenini teşhis eden bir büyük dil modelinin kanıt yeterliliği değiştiğinde nasıl davrandığını inceleyecektir. Amaç, modelin yalnızca doğru cevabı bulup bulmadığını değil, cevabının gördüğü kanıtlarla desteklenip desteklenmediğini ve yetersiz kanıtta uygun biçimde cevap vermekten kaçınıp kaçınmadığını da ölçmektir.

### Temel araştırma sorusu

Kanıt yetersiz yazılım hata vakalarında, cevap vermekten kaçınmaya izin verilen bir politika, teşhis vermeyi zorunlu kılan politikaya kıyasla kanıtla desteklenmeyen kesin teşhisleri azaltır mı; bunun yanıt kapsamı ve yeterli kanıt bulunan vakalardaki gereksiz kaçınma üzerindeki maliyeti nedir?

### Taslak deney

- Her vaka için kaynak kodu, test ve düzeltme kayıtlarıyla doğrulanmış bir kök neden belirlenir.
- Kanıt paketleri önceden tanımlanmış yeterli, kısmi ve yetersiz seviyelere ayrılır.
- Aynı model ve aynı temel girdiyle, zorunlu teşhis ve seçici cevap/kaçınma politikaları karşılaştırılır.
- Teşhis doğruluğu, kanıtsal destek, yanıt kapsamı, seçici hata ve gereksiz kaçınma ayrı ölçülür.
- Vaka başına tekrarlar bağımsız vaka olarak sayılmaz.

## Bilimsel sınırlar

1. Genel LLM abstention alanında önceki çalışmalar vardır; projenin özgünlüğü kanıtlanmış değildir.
2. Yeni veri havuzu, DİJİTALİKİZ'in pilot, confirmatory, kalibrasyon ve önceden incelenmiş vakalarından bağımsız olmalıdır.
3. Sistematik literatür taraması, veri fizibilitesi, puanlama protokolü ve analiz planı tamamlanmadan model çıkarımı yapılmaz.
4. Sonuçlar ne olursa olsun değiştirilmeden raporlanır; sonuçlara bakarak hipotez veya birincil ölçüt değiştirilmez.
5. Bu proje, DİJİTALİKİZ'in önceki sonuçlarını yeniden etiketleyerek veya yeni proje sonucuymuş gibi kullanarak ilerlemeyecektir.

## Aşama durumu

- **Aşama 1 — literatür ve özgünlük:** hedefli ön tarama tamamlandı. Genel abstention ve kod alanında belirsizlik yönetimi zaten araştırılıyor; bu nedenle özgünlük kesin değil. Tam sistematik derleme yapılmış gibi sunulmayacak.
- **Aşama 2 — veri fizibilitesi:** kaynak-kümesi fizibilitesi tamamlandı (koşullu); BugsInPy upstream'inde 17 projede 501 ham hata klasörü sayıldı. Bu bir kabul edilmiş örneklem sayısı değildir. En az 60 kabul edilmiş vaka / 8 proje doğrulanmadı.
- **CI vaka smoke:** [PySnooper denemesi](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460135014) beklenen buggy-fail koşulunu sağlamadı. [tqdm'un ilk denemesi](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460540758) fixed tarafta başarısız oldu; import yolu düzeltilince [sonraki smoke](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759) buggy-fail/fixed-pass verdi. Runtime ile metadata Python sürümleri eşleşmediği ve vaka incelenmiş olduğu için hiçbir smoke vakası ana örnekleme alınmaz.
- **Aşama 3 — deney tasarımı:** tamamlandı belge olarak. Faktörler E1/E2/E3 kanıt seviyesi × P0 zorunlu teşhis/P1 seçici kaçınma politikası; her vaka için altı çıktı. Birincil sonuç E3 altındaki kanıtsız kesin teşhis oranı; eşleştirilmiş karşılaştırma exact McNemar testi, RD ve %95 CI. 80 vaka hedefi, en az 60 ve 8 proje doğrulayıcı alt sınırı.
- **Araştırma kapsamını ayırma:** [REPO_SCOPE_SPLIT.md](REPO_SCOPE_SPLIT.md) kapsam kuralıdır; [USE_FOR_THIS_PROJECT/MANIFEST.json](USE_FOR_THIS_PROJECT/MANIFEST.json) izin verilen materyalleri ve [DO_NOT_USE_AS_EVIDENCE/MANIFEST.json](DO_NOT_USE_AS_EVIDENCE/MANIFEST.json) yasaklanan tarihsel veri/sonuçları makine tarafından okunabilir biçimde listeler.
- **Model çıkarımı:** kapalı. Henüz LLM inference veya yeni projenin deneysel sonucu yoktur. Vaka-kabul kapıları, lisans, ground truth, kanıt yeterliliği, sızıntı incelemesi ve runtime/prompt/analiz hash'leri kilitlenmeden inference yapılmayacak.

## Belgeler

- [İlk 120 adayın sabit tarama sırası](SCREENING_COHORT_120_2026-10-21.json) — metadata-only aday listesi, 0 kabul edilmiş vaka.

- [Üç ana aşamalı yürütme haritası](THREE_PHASE_EXECUTION_MAP_2026-10-21.md) — projenin ne kadarının hazır olduğunu ve hangi kanıt kapılarının hâlâ açık kaldığını tek noktada toplar.

- [Manuel vaka inceleme rehberi](CASE_REVIEW_GUIDE.md) — test/lisans/ground truth/kanıt/sızıntı kabul sırası.
- [Manuel vaka inceleme formu (JSON)](CASE_REVIEW_INTAKE_TEMPLATE.json) — boş şablon; kabul edilmiş vaka değildir.

- [Aday doğrulama kuyruğu sonucu](SCREENING_QUEUE_RESULT_2026-10-21.md) — 487 metadata adayını 17 proje arasında dengeli tarama sırasına koyar; kabul edilmiş vaka anlamına gelmez.

- `TUBITAK_2204A_MASTER_PLAN_2026-10-21.md` — TÜBİTAK 2204-A için tek aktif yürütme planı.
- `TUBITAK_2204A_JURY_CRITERIA_CHECKLIST_2026-10-21.md` — resmî ön değerlendirme ölçütlerine göre kapı kontrolü.

- `REPO_SCOPE_SPLIT.md` — repo kullanım kapsamı.
- `LITERATURE_REVIEW.md` — hedefli literatür taraması ve özgünlük sınırı.
- [`LITERATURE_SWEEP_SUPPLEMENT_2026-10-21.md`](LITERATURE_SWEEP_SUPPLEMENT_2026-10-21.md) — 2025–2026 yakın çalışmaların ek taraması ve daraltılmış özgünlük kararı; sistematik derleme değildir.
- `DATA_FEASIBILITY.md` — kaynak-kümesi denetimi ve CI başarısızlıkları.
- `STAGE3_EXPERIMENT_DESIGN.md` — deney tasarımı.
- `PROMPT_CONDITIONS.md` — eşleştirilmiş prompt koşulları.
- `OUTPUT_SCHEMA.json` — yapılandırılmış çıktı şeması.
- `ANALYSIS_PLAN_STAGE3.md` — sonuçlardan önce tanımlanmış analiz planı.
- `EXPERIMENT_MANIFEST_STAGE3.json` — inference kapısı kapalı manifest.
- `STAGE3_REVIEW_AND_EXIT.md` — Aşama 3 tasarım kapanış denetimi ve kalan inference kapıları.
- `PROTOCOL_DRAFT.md` — protokol taslağı.
- `USE_FOR_THIS_PROJECT/` — yeni proje için kullanılabilir dokümantasyonun kopyaları ve izin manifesti.
- `DO_NOT_USE_AS_EVIDENCE/` — eski DİJİTALİKİZ verileri/sonuçları için dışlama politikası ve manifest.
- `USE_FOR_THIS_PROJECT/REUSE_RULES.md` — yeniden kullanım kuralları.

Bu çalışma şu anda planlama aşamasındadır. Herhangi bir deney yürütüldüğü, insan puanlamasının tamamlandığı veya sonuç alındığı iddia edilmemektedir.


## Aşama 4 — teknik hazırlık durumu (21 Ekim 2026)

- [Teknik hazırlık ve açık kapılar](STAGE4_TECHNICAL_READINESS_2026-10-21.md)
- [Boş vaka sicili](CASE_REGISTRY.json): bilerek boş; hiçbir vaka doğrulayıcı olarak kabul edilmedi.
- [Runtime adayı](RUNTIME_LOCK.json): resmi, kuantize edilmemiş Qwen2.5-3B-Instruct revizyonu aday olarak belgelendi; henüz yükleme doğrulaması yok.
- [İnsan puanlama rubriği ve adjudication taslağı](RUBRIC_AND_ADJUDICATION.md): iki bağımsız değerlendirici ve körleme kuralları taslaklandı; kalibrasyon/dondurma tamamlanmadı.
- `scripts/evidence_abstention_preflight.py` ve `tests/test_evidence_abstention_preflight.py`: yalnızca read-only kapı denetimi ve birim testleri; model çağırmaz.
- `.github/workflows/evidence-abstention-preflight.yml`: no-inference CI doğrulaması; inference veya dış veri indirmesi yok. [İlk doğrulama çalışması başarılı](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39615830978): üç birim test geçti; rapor 0 kabul edilmiş vaka ve 16 açık inference blokajı gösterdi.

**Geçiş kararı:** Teknik altyapı hazırlanıyor. Doğrulanmış vaka sayısı sıfır olduğu için Stage 4 pilot LLM çıkarımı başlatılmayacak. En az 60 vaka/8 proje, tüm vaka/kanıt/lisans/sızıntı kapıları, iki değerlendiricili kalibrasyon, model/tokenizer/runtime denetimi, dosya hash'leri ve denetlenebilir ön kayıt tamamlanmadan inference yasaktır. Bu bir başarısız deney sonucu değil, henüz deney yürütülmediği anlamına gelir.


## Aşama 2 — metadata envanterini otomatikleştirme

Aşama 2 envanter sonucu: [METADATA_INVENTORY_RESULT_2026-10-21.md](METADATA_INVENTORY_RESULT_2026-10-21.md). Sabitlenmiş BugsInPy revizyonunda 501 ham kayıt/17 proje, 500 temel metadata-kalifiye kayıt ve bir metadata sorunu bulundu; 0 test çifti doğrulandı, 0 vaka kabul edildi.


- scripts/inventory_bugsinpy_candidates.py sabitlenmiş BugsInPy revizyonundaki metadata kayıtlarını CSV'ye dönüştürür.
- tests/test_inventory_bugsinpy_candidates.py fail-closed ve metadata-only kurallarını sınar.
- .github/workflows/evidence-abstention-metadata-inventory.yml sadece pinned upstream metadata ağacını indirip envanter artifact'ı üretir; test yürütmez ve model çağırmaz.
- Envanter otomasyonu tek başına hiçbir vakayı kabul etmez. Operasyonel vaka doğrulama tamamlanana kadar accepted cases = 0 ve inference = false kalır.


**Yeni doğrulama notu:** Envanter CI'sı başarılı; fakat dışlanan tqdm smoke testinin yeniden çalıştırması [run 39618666531](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618666531) fixed test tarafında tekrar başarısız oldu. Tek önceki olumlu smoke çalışması tekrarlanabilir kanıt sayılmıyor. Aşama 2 hâlâ 0 kabul edilmiş vaka ve açık operasyonel doğrulama kapısında.


## Tek odak kararı

Bu çalışma için başka yarışma veya ayrı araştırma hattı yürütülmeyecek. Şu an yapılacak iş, vaka kabul kapısını gerçek kanıtlarla kapatmak ve başvuruya hazır tamamlanmış bir bilimsel çalışma üretmektir. 501 ham metadata kaydı, 500 temel metadata-kalifiye kayıt olarak kalır; bunların hiçbiri otomatik kabul edilmiş deney vakası değildir. En az 60 kabul edilmiş bağımsız vaka / 8 proje ve tüm yöntem kapıları sağlanana kadar model çıkarımı kapalı tutulur.

 
**Exact-runtime smoke note:** The previously exposed `BugsInPy-tqdm-1` diagnostic now completed under its metadata Python 3.6.9. Buggy target test failed with the target TypeError and a teardown error; fixed target test passed. This case remains permanently excluded. See [the data-feasibility record](DATA_FEASIBILITY.md). The initial diagnostic ZIP's embedded checksum list had runner-absolute paths; a follow-up workflow fix adds portable relative checksums and self-validation, pending its next CI run.


## Aşama 1 devamı — analiz sözleşmesi ve ilk sekiz ön-kohort denemesi

- [Analiz runbook'u](ANALYSIS_RUNBOOK.md) ve boş [adjudike sonuç şablonu](ADJUDICATED_RESULTS_TEMPLATE.csv) eklendi. Sonuç betiği [`scripts/analyze_evidence_abstention_results.py`](../../scripts/analyze_evidence_abstention_results.py) gerçek puanlama tablosu olmadan deney sonucu üretmez ve analiz çağrısında ayrıca kapalı inference, açık veri kapısı, preregistration, iki puanlayıcı protokolü, kalibrasyon, model/runtime doğrulaması ve dondurulmuş hash'leri şart koşar.
- Analiz yardımcısının sentetik veriye dayalı 9 testi geçti: [run 39647152364](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39647152364). Bu, analiz kodunun matematik/şema kapılarını test eder; gerçek model verisi değildir.
- [İlk sekiz önceden sıralanmış adayın teknik taraması](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39647103338) hâlen yürütülüyor. İlk turda upstream BugsInPy derleme betiğinin GitHub runner'ında bulunmayan `~/.bashrc` nedeniyle hata verdiği gözlendi; hiçbir hedef test sonucu üretilmedi. Workflow'a boş `~/.bashrc` oluşturma düzeltmesi eklendi; yeni koşu bu düzeltmeyi sınayacak.
- Sekiz adayın hiçbiri kabul edilmiş sayılmaz; çalışma kayıtları `accepted_for_confirmatory=false`, `llm_inference_performed=false` olarak kalır. Teknik tarama sonuçları insanın kök neden, lisans, kanıt yeterliliği veya maruziyet onayı yerine geçmez.


## Kör puanlayıcı güvenilirliği

- [Kör puanlayıcılar arası uyum protokolü](RATER_AGREEMENT_PROTOCOL.md) ve boş [ham puanlama şablonu](BLINDED_RATER_SCORES_TEMPLATE.csv) eklendi.
- [Uyum analiz betiği](../../scripts/analyze_evidence_abstention_rater_agreement.py) her görevi iki bağımsız puanlayıcı ile, kök neden ve kanıtsal destek panellerini birbirinden ayırarak değerlendirir; ham anlaşma, Cohen kappa, kategori sayıları ve bootstrap %95 aralığını raporlar.
- [Analiz CI'sı](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39649070365) sonuç analizi için 10/10 ve puanlayıcı uyumu için 7/7 sentetik testi geçti. Bu rapor gerçek insan puanları değildir; doğrulanmış kabul edilen vaka sayısını değiştirmez.


## Yeni doğrulama kayıtları — 21 Ekim 2026

- [İlk-dalga teknik tarama sonuçları](FIRST_WAVE_TRIAGE_RESULTS_2026-10-21.md): run [39644280706](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39644280706) tamamlandı; 7/7 teknik işler/artefakt denetimleri geçti, ancak tüm vakalar triage amaçlı ve ana doğrulayıcı örneklem dışı.
- [Yürütme haritası](THREE_PHASE_EXECUTION_MAP_2026-10-21.md): son triage kararı ve inference kapılarının güncel durumu.
- [Literatür ve özgünlük sınırı](LITERATURE_REVIEW.md): 21 Ekim güncellemesinde 2026 fault-localization ve hallucination azaltma çalışmaları eklendi. Sistematik tarama ve özgünlük kanıtı hâlâ tamamlanmış sayılmıyor.
- Güncel Aşama 1 kararları, 60 vaka/8 proje alt sınırı, panel ayrımı, runtime/hash/pre-registration kapıları tamamlanmadan model çıkarımı yapılmasına izin vermiyor.


## Kohort teknik bulguları

- [İlk dondurulmuş kohortun teknik bulguları](COHORT_TECHNICAL_FINDINGS_2026-10-21.md) içinde black-3 hedef testinin ham buggy-fail/fixed-pass sinyali, patch ile test arasındaki bağlantı, artefakt hash'leri ve eksik insan değerlendirme kapıları kaydedildi.
- Aynı belge, ilk koşudaki kurulum/aktivasyon hatalarını gerçek hata üretimi saymadığımızı ve diğer adayları test çifti doğrulanmadan kabul etmediğimizi açıkça ayırır.
- Güncel runner düzeltmesini denetleyen [kohort batch 1 Actions koşusu](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39651002472) halen incelenmelidir; yalnızca o koşunun biten artefaktları teknik durum raporuna eklenir.

- [Black-3 ön teknik inceleme kaydı](PRELIMINARY_CASE_SCREEN_BugsInPy-black-3_2026-10-21.md): ham teknik test çifti ve MIT lisansı ilk kontrolü belgelenmiştir; bağımsız insan panelleri tamamlanmadığı için vaka kabul edilmemiştir.


### Geçersiz çıktıların duyarlılık analizi

Analiz betiği, birincil insan-adjudikeli E3 outcome'unu değiştirmeden, bütün E3 `invalid_output` kararlarını güvensiz sayan ayrı bir muhafazakâr duyarlılık hesaplaması da üretir. Bu, protokolde vaat edilen iki uç senaryolu raporlamayı teknik olarak destekler. Sentetik testler hesaplama kodunu denetler; gerçek araştırma sonucu değildir.


## Cohort exposure correction — 21 October 2026

The original 120-case intake file is preserved as a historical record, but eight cases from it were later used for runtime/workflow debugging and are permanently excluded from confirmatory use. See [the exposure audit](COHORT_EXPOSURE_AUDIT_2026-10-21.md) and the deterministic [exposure-clean screening intake v2](SCREENING_COHORT_120_V2_2026-10-21.json). The v2 list contains 120 unique IDs across 17 upstream projects and does not overlap the eight excluded IDs. It is a screening order only: **0 accepted cases; LLM inference remains off**. It does not establish confirmatory eligibility or replace the requirement to freeze the confirmatory sample and protocol before inference.


- [V3 teknik tanılama kohortu](SCREENING_COHORT_120_V3_2026-10-21.json) — araç/kurulum hatalarını ayıklarken kullanılan 120 adaylık tarihsel sıra; ilk 8’i doğrulayıcı örneklemden kalıcı dışlandı.
- [Güncel V4 tarama sırası](SCREENING_COHORT_120_V4_2026-10-21.json) — 24 maruziyet vakası atlanmıştır; 120 aday, 17 proje, 0 kabul edilmiş vaka; doğrulayıcı örneklem değildir.


- [V3 teknik tanılama kohortu](SCREENING_COHORT_120_V3_2026-10-21.json) — metadata parser/runner debug sırası; ilk sekiz adayı kalıcı dışlandı.
- [V4 teknik tanılama kohortu](SCREENING_COHORT_120_V4_2026-10-21.json) — test bağımlılıkları ve runner davranışını incelemek için kullanılan tarihsel sıra; ilk sekiz adayı kalıcı dışlandı.
- [Güncel V5 tarama sırası](SCREENING_COHORT_120_V5_2026-10-21.json) — 32 maruziyet vakası atlanmıştır; 120 aday, 17 proje, 0 kabul edilmiş vaka; doğrulayıcı örneklem değildir.
