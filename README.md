# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tek aktif hedef:** 2027 TÜBİTAK 2204-A için tamamlanmış, tekrarlanabilir ve bilimsel olarak savunulabilir bir araştırma sunmak. Finalistlik hedefi korunur; sonuç garanti edilmez.

**Bilimsel rapor için önerilen başlık:** *Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi*

## Güncel durum — 15 Kasım 2026

**Güncel yürütme planı:** [15 Kasım 2026 ana denetim ve düzeltilmiş yürütme sırası](docs/MASTER_AUDIT_AND_EXECUTION_ORDER_2026-11-15.md).

**Bilimsel durum:** Doğrulayıcı ana deney henüz çalıştırılmadı. Kabul edilmiş bağımsız doğrulayıcı vaka **0**, kabul edilmiş upstream proje **0**, ana deney modeli çıktısı **0**. İnsan panelleri, kalibrasyon, dışarıdan doğrulanabilir ön kayıt ve exact model/runtime kapıları tamamlanmadı. **Model inference kapalıdır.**

| Bileşen | Doğrulanmış durum |
|---|---|
| Aday veri kaynağı | SWE-rebench V2 Filtered-Verified; 12 Kasım tarihinde sabitlenmiş 96 proje aday cohort'u |
| Aday kapsam taraması | Cohort satırları 1–96 statik olarak incelendi; 89–96 aralığında 3 güçlü, 4 koşullu aday ve 1 dışlama belirlendi |
| Teknik yeniden üretim | 2 adayda base-fail/fix-pass: Robocop issue #1371 (row 24) ve pdoc issue #812 (row 95) |
| Confirmatory örneklem | Her iki teknik aday da araştırma protokolündeki maruziyet kuralı nedeniyle ana örneklemden çıkarıldı; kabul edilen vaka sayısı **0** |
| Lisans/provenans | pdoc row 95 exact-base root license MIT-0 olarak düzeltildi; Napalm row 19 Cisco fixture provenans hold sürüyor; seçilecek her aday için nested/per-file provenance ayrıca incelenmeli |
| Ana deney | E1/E2/E3 kanıt yeterliliği × P0 zorunlu teşhis / P1 seçici teşhis-kaçınma; inference yetkisi kapalı |
| Model/runtime | Qwen2.5-3B-Instruct aday revizyonu kayıtlı; exact model/tokenizer/runtime yükleme preflight'ı tamamlanmadı |
| Readiness | `ready=false`, 24 V2 blokajı (V2'ye özgü no-inference preflight), 0 kabul edilmiş vaka, 0 kabul edilmiş proje |
| Ayrı entropy prototipi | Beş adaylı belirsizlik/entropy prototipi ana P0/P1 deneyine dahil değildir |

### 15 Kasım teknik doğrulama kayıtları

- **Robocop #1371:** [PR #193](https://github.com/MahmutVezir/dijitalikiz/pull/193) birleştirildi. Sabit upstream base ve fix commitleri, aynı uv kilidi ve aynı test ortamında dört parametrik testle karşılaştırıldı. Base'de issue'ya özgü tek assertion beklenen şekilde başarısız; fix'te 4/4 test başarılı. Teknik reproduksiyon raporu: [ROBOCOP_1371_TECHNICAL_REPRODUCTION_RECORD_2026-11-15.md](research_candidates/evidence_abstention/ROBOCOP_1371_TECHNICAL_REPRODUCTION_RECORD_2026-11-15.md).
- **pdoc #812 / PR #813:** [PR #195](https://github.com/MahmutVezir/dijitalikiz/pull/195) birleştirildi. Gerçek `python -m pdoc . --output-directory ...` CLI çağrısı exact base'de `ValueError: No modules found matching spec: .` hatasını verdi; exact fix aynı sentetik paket ve aynı ortamda HTML üretti. Ortam Python 3.11.5 ve uv 0.6.7'dir. Lisans sınıflandırması MIT-0 olarak düzeltildi. Ayrıntılı teknik kayıt: [PDOC_813_TECHNICAL_REPRODUCTION_RECORD_2026-11-15.md](research_candidates/evidence_abstention/PDOC_813_TECHNICAL_REPRODUCTION_RECORD_2026-11-15.md) (öncesindeki statik inceleme: [PDOC_813_PRE_REPRODUCTION_REVIEW_2026-11-15.md](research_candidates/evidence_abstention/PDOC_813_PRE_REPRODUCTION_REVIEW_2026-11-15.md)).

**Önemli örneklem kuralı:** Bir aday üzerinde teknik hata ayıklama/reproduksiyon yapıldıysa, sonuç base-fail/fix-pass olsa bile confirmatory örnekleme alınmaz. Robocop ve pdoc bu nedenle mühendislik/kalibrasyon kayıtlarıdır; vaka sayısına eklenmez ve P0/P1 hipotezine kanıt oluşturmaz.

### Son CI ve güvenlik kontrolleri

- Research Validation run [43712582477](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582477): pdoc reproduksiyon job'ı başarılı; repository/configuration işi **414 test + 56 subtest** ile başarılı.
- No-inference preflight run [43712582464](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582464): fail-closed testleri **13/13**, kanıt paketi/atıf auditor testleri **12/12** başarılı. Readiness raporu `ready=false`, **21 blokaj**, 0 vaka, 0 proje ve `model_inference_performed=false` bildiriyor.
- Ayrı Historical archive integrity işi, eski CCDG arşivi `data/historical/confirmatory_artifact_2026-10-09.zip` ana depoda bulunmadığı için başarısız. Bu eski arşiv yeni belirsizlik/çekimserlik araştırmasının verisi değildir; pdoc veya Robocop reproduksiyonlarının sonucu değildir.

### Veri kaynağı ve kapsam ayrımı

- Birincil aday kaynağı: SWE-rebench V2 Filtered-Verified; sabit Parquet revision ve 96-row cohort hash'leri mevcut.
- Eski BugsInPy V10/V12 ve 105-ID dışlama kayıtları tarihsel/ayrı bir akıştır; eski Stage 3 manifesti SWE-rebench deneyi için kullanılmayacaktır.
- Tarihsel CCDG/160 kayıtlı deney bu yeni araştırmanın veri seti, kalibrasyon verisi veya sonucu değildir.
- Kaggle metadata intake için gerekmiyor. 27 Ekim 31 dosyalı snapshot ile 3 Kasım 19 dosyalı allowlist snapshot birbirinden ayrıdır.

**15 Kasım ek statik incelemesi — pyfar #722 (row 90):** [PYFAR_722_STATIC_CANDIDATE_REVIEW_2026-11-15.md](research_candidates/evidence_abstention/PYFAR_722_STATIC_CANDIDATE_REVIEW_2026-11-15.md). Issue sözleşmesi, exact base/fix kimlikleri, iki değişen dosya, MIT lisansı ve 36 kombinasyonluk yeni test matrisi incelendi. Aday güçlü statik aday olarak kalıyor; upstream test/build çalıştırılmadı, vaka kabul edilmedi ve teknik maruziyet oluşmadı. Açık test noktaları: issue'daki farklı sinyal uzunluklarının örneği ve `return_reference=True` davranışı.

**Sonraki tek araştırma adımı:** Row 90'ı henüz çalıştırılmamış aday kuyruğunda koru; diğer untouched cohort adaylarında issue kapsamı/test oracle/lisans statik taramasını sürdür. 60 vaka ve 8 proje eşiği düşürülmez.


## Tarihsel durum — 27 Ekim 2026 (SWE-rebench V2 kararıyla geçersiz / arşiv)

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

Tarihsel BugsInPy/Stage 3 ön kayıt taslağı (V2 protokolü değildir): [PREREGISTRATION_DRAFT_V1_1.md](research_candidates/evidence_abstention/PREREGISTRATION_DRAFT_V1_1.md); bağımsız değerlendirici bulma ve körleme: [REVIEWER_RECRUITMENT_AND_PANEL_GUIDE_2026-10-23.md](research_candidates/evidence_abstention/REVIEWER_RECRUITMENT_AND_PANEL_GUIDE_2026-10-23.md). V10 aday sırası ve maruziyet denetimi: [STAGE1_V10_METADATA_INTAKE_2026-10-23.md](research_candidates/evidence_abstention/STAGE1_V10_METADATA_INTAKE_2026-10-23.md). Runner çalıştırma sorunu için depo sahibi kontrol listesi: [GITHUB_ACTIONS_RUNNER_RECOVERY_GUIDE_2026-10-23.md](research_candidates/evidence_abstention/GITHUB_ACTIONS_RUNNER_RECOVERY_GUIDE_2026-10-23.md). Tek kaynaklı güncel durum: [CURRENT_STATUS_AND_EXECUTION_PLAN_2026-10-23.md](research_candidates/evidence_abstention/CURRENT_STATUS_AND_EXECUTION_PLAN_2026-10-23.md). Semantik auditor için sınırlar ve doğrulama gereksinimleri: [SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md](research_candidates/evidence_abstention/SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md). Önceki smoke tanılaması: [EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md](research_candidates/evidence_abstention/EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md).

**Tarihsel üç aşamalı plan (BugsInPy/Stage 3; V2 için kullanılmaz):** Bu bölüm 27 Ekim 2026 tarihli eski veri hattını anlatır. SWE-rebench V2 için güncel eşik 60 kabul edilmiş vaka / 60 farklı bağımsız upstream projedir; güncel sıralama yukarıdaki 15 Kasım ana denetim belgesindedir. (1) ana istem-politikası deneyi için en az 60 kabul edilmiş bağımsız vaka/60 farklı upstream proje, iki ayrık insan paneli, exact model-runtime, hash dondurma ve ön kayıt kapılarını kapat; (2) yalnızca bu kapılar kapanırsa E1/E2/E3 × P0/P1 deneyini yürüt, kör puanla ve önceden planlanan istatistiği hesapla; (3) gerçek sonuçları ve sınırlılıkları resmi TÜBİTAK raporuna aktar. Beş adaylı entropi/semantik-auditor prototipi ayrı bir mühendislik koludur; bu ana karşılaştırmaya dahil değildir ve onun hakkında etkinlik/kalibrasyon iddiası için ayrı validasyon gerekir.

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
