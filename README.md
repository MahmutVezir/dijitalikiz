# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tek aktif hedef: 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde, tamamlanmış ve bilimsel olarak savunulabilir bir araştırma sunmak.** Bu hedef bir çalışma yönüdür; finalistlik sonucu garanti edilemez.

**Bilimsel rapor için önerilen başlık:** *Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi*

## Güncel durum — 14 Kasım 2026

> **Bu bölüm güncel kaynak durumudur.** Aşağıdaki 27 Ekim ve önceki bölümler tarihsel kayıttır; aktif veri kaynağı/örneklem durumu olarak okunmamalıdır. Güncel tek yürütme planı: [14 Kasım proje denetimi ve yol haritası](docs/PROJECT_AUDIT_AND_EXECUTION_ROADMAP_2026-11-14.md) ve [12 Kasım güncel aşamalı durum](research_candidates/evidence_abstention/CURRENT_STATUS_AND_EXECUTION_PLAN_2026-11-12.md).

**Bilimsel durum:** Henüz doğrulayıcı deney yapılmadı. Kabul edilmiş vaka/proje **0/0**, ana deney modeli çıktısı **0**, insan panelleri ve kalibrasyon tamamlanmadı, haricî ön kayıt yok ve model çıkarımı kapalıdır.

| Güncel bileşen | Doğrulanmış durum |
|---|---|
| Ana aday veri kaynağı | SWE-rebench V2 Filtered-Verified; metadata fizibilitesi ve 96 proje aday cohort'u mevcut |
| Aday kapsam denetimi | 1–56: PR/base SHA 56/56; 57–64: 8/8; 65–72: 8/8; 73–80: 8/8; 81–88: 8/8; 89–96: 8/8. Statik aday taraması 96/96 tamamlandı; bu, kabul edilmiş vaka anlamına gelmez. |
| Lisans | İlk 16: 16/16 Apache-2.0; 17–56: 40/40 exact-base root LICENSE (12 Apache-2.0, 2 BSD-2-Clause, 24 BSD-3-Clause, 2 MIT; 2 root NOTICE); 57–64: 8/8; 65–72: 8/8; 73–80: 8/8 (1 root NOTICE); 81–88: 8/8 (0 root NOTICE); 89–96: 8/8 (1 root NOTICE). Cohort genelinde exact-base root LICENSE **96/96**; nested/fayla özgü provenans incelemesi sürüyor. Row 19 Napalm Cisco fixture için ayrıca provenans incelemesi gerekiyor. |
| Doğrulayıcı vaka | 0 kabul edilmiş vaka; metadata veya statik patch eşleşmesi kabul anlamına gelmez |
| Model/runtime | Qwen2.5-3B-Instruct aday revizyonu kayıtlı; exact revision lisansı ve çalışma zamanı yükleme kontrolü tamamlanmadı |
| Ana deney | P0/P1 × E1/E2/E3 tasarımı; inference izni kapalı |
| Ayrı prototip | Beş adaylı entropy/uncertainty adaptörü ana deneyden ayrıdır; ana sonuca dahil değildir |

**Cohort denetimleri:** [17–56 lisans/provenans denetimi](research_candidates/evidence_abstention/SWE_REBENCH_V2_LICENSE_PROVENANCE_AUDIT_17_56_2026-11-14.md), [57–64. satırlar](research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_57_64_2026-11-14.md), [65–72. satırlar](research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_65_72_2026-11-14.md), [73–80. satırlar](research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_73_80_2026-11-14.md), [81–88. satırlar](research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_81_88_2026-11-14.md) ve [89–96. satırlar](research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_89_96_2026-11-14.md) — bunlar statik aday/provenans denetimleridir, vaka kabulü değildir.

**Veri kaynağı ayrımı:** Eski BugsInPy V10/V12 ve 105-ID dışlama kayıtları tarihsel/ayrı bir akıştır. Eski Stage 3 manifesti hâlâ BugsInPy referansı taşır; SWE-rebench deneyinin manifesti olarak kullanılmayacaktır. Yeni veri kaynağı için yeni sürümlü protokol/manifest gerekir. Tarihsel CCDG sonuçları da yeni araştırma verisi değildir.

**Kaggle notu:** BUNDLE_MANIFEST.json uyumluluğu PR #158 ile düzeltildi. 31 dosyalı 27 Ekim snapshot'ı ile 19 dosyalı 3 Kasım allowlist snapshot'ı farklı notebook/amaçlara aittir; karıştırılmamalıdır. Metadata intake için Kaggle gerekmiyor.

**En güncel no-inference doğrulaması:** PR [#184](https://github.com/MahmutVezir/dijitalikiz/pull/184), [#186](https://github.com/MahmutVezir/dijitalikiz/pull/186) ve [#187](https://github.com/MahmutVezir/dijitalikiz/pull/187) main'e merge edilmiştir. PR #187, 89–96 statik aday denetimini taşır. Son preflight run [43631700266](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43631700266): fail-closed preflight **13/13**, evidence-packet/citation auditor **12/12** test geçti. Readiness hâlâ `ready=false`, **21 engel**, 0 kabul edilmiş vaka/proje ve `model_inference_performed=false`. Son Research Validation run [43631700302](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43631700302) içindeki repository/configuration işi **414 test + 56 subtest** ile geçti; ayrı Historical archive integrity işi, `data/historical/confirmatory_artifact_2026-10-09.zip` canonical depoda bulunmadığı için başarısız oldu; arşiv boyutu/hash/CRC denetimleri atlandı. **CI başarıları yalnızca kod/konfigürasyon ve no-inference kontrolleridir; araştırma hazır olduğu anlamına gelmez. Model çıkarımı kapalıdır.**

---

## Güncel durum — 27 Ekim 2026

**Bilimsel durum: tamamlanmadı; doğrulayıcı model çıkarımı kapalı.** Ana soru ve eşleştirilmiş deney tasarımı tanımlı; kabul edilmiş bağımsız vaka sayısı **0**, ana çalışmanın doğrulayıcı model çıktısı **0**, kalibrasyon verisi **0** ve tam model/tokenizer/CUDA runtime doğrulaması tamamlanmış değil. Gradio arayüzü tek-vaka keşifsel demosudur; ana araştırmanın sonucu değildir.

| Bileşen | Durum |
|---|---|
| Kaynak envanteri | BugsInPy sabit sürümünde 501 ham metadata kaydı / 17 proje; bu sayı kabul edilmiş vaka sayısı değildir. |
| Güncel intake | V10 yerel metadata sırası: 100 aday / 14 upstream proje; 407 adaylık yenilenmiş kuyruğun ardından oluşturuldu. 61 tarihsel + 32 güncel teknik/maruziyet kaydı = 93 kalıcı dışlama; seçilen V10 listesiyle kesişim 0. Uzak CI doğrulaması hâlâ bekliyor. |
| Kabul edilmiş doğrulayıcı vakalar | **0**; vaka sicili bilerek boş. |
| Yazılım prototipi | prototype/ altındaki Gradio demo, Stage 3 system prompt/P0-P1 politika metni/çıktı şemasıyla eşleştirildi; ham karar otomatik değiştirilmez ve prompt/packet/output hash'leri raporlanır. Canlı model runtime testi henüz doğrulanmadı. Resmî araştırma çıktıları yalnızca Stage 3 runner'ından üretilebilir. |
| Semantik kanıt desteği | Prompt/parser, adapter arayüzü ve hash-bağlı paket giriş noktası mevcut. 12 temel sentetik test, hash-bağlama regresyon testleri eklenmeden önce yerelde geçmişti; yeni birleşik test paketinin tamamı için doğrulanmış geçiş sonucu yok. Son GitHub Actions denemeleri adım kaydetmeden başarısız oldu. Gerçek Qwen denetçi çağrısı ve insan puanlarıyla geçerlik de henüz doğrulanmadı. |
| Keşifsel smoke | 10 çıktı; P0 ve P1 koşullarının ikisinde de 0/5 açık kaçınma. Maruziyet, prompt sızıntısı ve runtime uyumsuzluğu nedeniyle doğrulayıcı sonuç değil. |
| Kalibrasyon / ön kayıt / runtime | Kalibrasyon verisi boş; doğrulanabilir ön kayıt yok; tam model/tokenizer/CUDA runtime denetimi tamamlanmadı. |
| Başvuru | Gerçek deney, kör puanlama ve analiz tamamlanmadan proje tamamlanmış araştırma olarak sunulamaz. |

Güncel ön kayıt taslağı: [PREREGISTRATION_DRAFT_V1_1.md](research_candidates/evidence_abstention/PREREGISTRATION_DRAFT_V1_1.md); bağımsız değerlendirici bulma ve körleme: [REVIEWER_RECRUITMENT_AND_PANEL_GUIDE_2026-10-23.md](research_candidates/evidence_abstention/REVIEWER_RECRUITMENT_AND_PANEL_GUIDE_2026-10-23.md). V10 aday sırası ve maruziyet denetimi: [STAGE1_V10_METADATA_INTAKE_2026-10-23.md](research_candidates/evidence_abstention/STAGE1_V10_METADATA_INTAKE_2026-10-23.md). Runner çalıştırma sorunu için depo sahibi kontrol listesi: [GITHUB_ACTIONS_RUNNER_RECOVERY_GUIDE_2026-10-23.md](research_candidates/evidence_abstention/GITHUB_ACTIONS_RUNNER_RECOVERY_GUIDE_2026-10-23.md). Tek kaynaklı güncel durum: [CURRENT_STATUS_AND_EXECUTION_PLAN_2026-10-23.md](research_candidates/evidence_abstention/CURRENT_STATUS_AND_EXECUTION_PLAN_2026-10-23.md). Semantik auditor için sınırlar ve doğrulama gereksinimleri: [SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md](research_candidates/evidence_abstention/SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md). Önceki smoke tanılaması: [EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md](research_candidates/evidence_abstention/EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md).

**Üç aşamalı plan:** (1) ana istem-politikası deneyi için en az 60 kabul edilmiş bağımsız vaka/8 upstream proje, iki ayrık insan paneli, exact model-runtime, hash dondurma ve ön kayıt kapılarını kapat; (2) yalnızca bu kapılar kapanırsa E1/E2/E3 × P0/P1 deneyini yürüt, kör puanla ve önceden planlanan istatistiği hesapla; (3) gerçek sonuçları ve sınırlılıkları resmi TÜBİTAK raporuna aktar. Beş adaylı entropi/semantik-auditor prototipi ayrı bir mühendislik koludur; bu ana karşılaştırmaya dahil değildir ve onun hakkında etkinlik/kalibrasyon iddiası için ayrı validasyon gerekir.

TÜBİTAK'ın 2026–2027 çağrısında başvuru son tarihi **4 Ocak 2027 saat 17.30 (Türkiye saati)** olarak duyurulmuştur: [resmî çağrı](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi). Finalistlik hedefi korunur; sonuç garanti edilemez. Eski CCDG verileri ve sonuçları bu yeni araştırmaya taşınmayacaktır.

## TÜBİTAK 2027 finalist odaklı yürütme planı

27 Ekim 2026 tarihinde resmî 2027 proje rehberi ve sayfada bağlı değerlendirme formları yeniden kontrol edildi. Güncel iş paketleri, karar tarihi, örneklem riskleri ve başvuru takvimi için [TÜBİTAK finalist hedefli yürütme planına](research_candidates/evidence_abstention/TUBITAK_2027_FINALIST_PRIORITY_PLAN_2026-10-27.md) bakın. Öncelik ürün ekranını genişletmek değil, bağımsız vaka kabul kapısını ve tekrarlanabilir bilimsel sonuç üretimini tamamlamaktır.

## Araştırma sorusu

Kanıtı yetersiz yazılım hata vakalarında, teşhis vermekten kaçınmaya izin veren bir politika; teşhisi zorunlu kılan politikaya kıyasla kanıtla desteklenmeyen kesin teşhisleri azaltıyor mu? Bunun yeterli kanıt bulunan vakalarda yanıt kapsamı ve gereksiz kaçınma bakımından maliyeti nedir?

## Deneyin özeti

- **Kanıt düzeyi:** E1 yeterli, E2 kısmi, E3 yetersiz.
- **Politika:** P0 zorunlu teşhis; P1 seçici teşhis/kaçınma.
- Her bağımsız vaka için 3 × 2 = 6 koşul planlanır. Vaka tekrarları bağımsız örnek sayılmaz.
- **Birincil sonuç:** E3 koşulunda kanıtla desteklenmeyen kesin teşhis oranının P0 ve P1 arasında eşleştirilmiş karşılaştırması.
- **Analiz:** iki taraflı exact McNemar testi, eşleştirilmiş risk farkı ve %95 güven aralığı.
- 80 vaka hedefinde 480; minimum 60 vakada 360 model çıktısı planlanır. Bunlar planlama sayılarıdır, üretilmiş çıktı değildir.

Özgünlük henüz kanıtlanmış değildir; LLM’lerin belirsizlikte kaçınması üzerine önceki çalışmalar bulunduğu için proje “ilk” veya “benzersiz” diye sunulmayacaktır. Araştırma odağı, yazılım hata teşhisinde kanıt seviyesi kontrollü paketler üzerinde desteklenmeyen kesin teşhis ile uygun kaçınma arasındaki deneysel karşılaştırmadır.

## Tek odak ve kapsam sınırı

Bu çalışma için şu an başka yarışma, başka araştırma hattı veya ayrı ürün hedefi yürütülmeyecektir. Depoda daha önceki DİJİTALİKİZ çalışmasına ait kod, veri, sonuçlar ve raporlar tarihsel kayıt olarak korunur; bunlar yeni çalışmanın verisi veya sonucu olarak kullanılamaz. Eski kayıtları silmek veya tarihsel sonuçları yeniden etiketlemek yerine kapsam ayrımı uygulanır. Ayrıntı: [depo kapsam ayrımı](research_candidates/evidence_abstention/REPO_SCOPE_SPLIT.md).

## Öncelikli iş sırası

1. Yeni ve maruz kalınmamış adayları belirlemek; lisans, exact runtime ve buggy-fail/fixed-pass çiftlerini doğrulamak.
2. En az 60 vaka / 8 proje kapısını sağlamak; hedef 80. Eşiği karşılamak için kabul koşulları gevşetilmez.
3. Kök neden ve E1/E2/E3 kanıt paketlerini model çıktısı görülmeden iki bağımsız değerlendiriciyle gözden geçirmek; rubriği kalibre edip dondurmak.
4. Model/tokenizer/runtime yükleme denetimini, prompt/şema/analiz/vaka hash'lerini ve denetlenebilir ön kaydı tamamlamak.
5. Ancak tüm kapılar kapandıktan sonra ayrı izinle deney çalıştırmak; kör puanlama, analiz, sınırlılıklar ve rapor denetimini tamamlamak.
6. TÜBİTAK’ın istediği biçimde tamamlanmış projeyi hazırlamak ve zamanında başvurmak.

## TÜBİTAK takvimi

TÜBİTAK’ın resmî 2026–2027 sayfasına göre başvuru aralığı 23 Eylül 2026–4 Ocak 2027’dir; sistem **4 Ocak 2027 saat 17.30’da** kapanır. Resmî sayfa ayrıca fikir aşamasında veya devam etmekte olan projelerle başvuru yapılmaması gerektiğini söylüyor: [2204-A çağrısı ve proje rehberi](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi). Bu nedenle yalnızca bir araştırma planına sahip olmak başvuru için yeterli değildir.

## Araştırma belgeleri

- [İlk 120 adayın sabit metadata-tarama sırası](research_candidates/evidence_abstention/SCREENING_COHORT_120_2026-10-21.json) — kabul edilmiş veri değil; test sonuçları görülmeden dondurulmuş intake sırası.

- [Üç ana aşamalı yürütme haritası](research_candidates/evidence_abstention/THREE_PHASE_EXECUTION_MAP_2026-10-21.md)
- [TÜBİTAK jüri ölçütleri kontrol listesi](research_candidates/evidence_abstention/TUBITAK_2204A_JURY_CRITERIA_CHECKLIST_2026-10-21.md)

- [Ana yürütme planı](research_candidates/evidence_abstention/TUBITAK_2204A_MASTER_PLAN_2026-10-21.md)
- [Araştırma özeti ve durum panosu](research_candidates/evidence_abstention/README.md)
- [Hedefli literatür incelemesi](research_candidates/evidence_abstention/LITERATURE_REVIEW.md)
- [Veri fizibilitesi ve dışlamalar](research_candidates/evidence_abstention/DATA_FEASIBILITY.md)
- [Deney tasarımı](research_candidates/evidence_abstention/STAGE3_EXPERIMENT_DESIGN.md)
- [Önceden planlanan analiz](research_candidates/evidence_abstention/ANALYSIS_PLAN_STAGE3.md)
- [Koşul istemleri](research_candidates/evidence_abstention/PROMPT_CONDITIONS.md)
- [Çıktı şeması](research_candidates/evidence_abstention/OUTPUT_SCHEMA.json)
- [Kabul sicili](research_candidates/evidence_abstention/CASE_REGISTRY.json) — şu anda bilerek boş.
- [Ön kontrol betiği](scripts/evidence_abstention_preflight.py) — yalnızca salt-okunur hazır olma denetimi yapar; model çalıştırmaz.

**Bilimsel kural:** Gerçek veri, doğrulama ve sonuç yoksa varmış gibi yazılmaz. Bir kapı tamamlanmadığında proje durumu açıkça eksik olarak kalır.

## Web tanıtım sayfası

Araştırmanın amacı, deney tasarımı, mevcut durum ve açık kaynak bağlantıları için statik tanıtım sayfası depo kökündeki [`index.html`](index.html) dosyasındadır. Sayfa, doğrulayıcı deney henüz yapılmadığını ve mevcut vaka/model çıktısı sayılarının sıfır olduğunu açıkça belirtir. Web yayınının durumu ayrıca barındırma sağlayıcısında doğrulanmalıdır.
