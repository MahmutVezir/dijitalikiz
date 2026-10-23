# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tek aktif hedef: 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde, tamamlanmış ve bilimsel olarak savunulabilir bir araştırma sunmak.** Bu hedef bir çalışma yönüdür; finalistlik sonucu garanti edilemez.

**Bilimsel rapor için önerilen başlık:** *Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi*

## Güncel durum — 23 Ekim 2026

**Bilimsel durum: tamamlanmadı; doğrulayıcı model çıkarımı kapalı.** Araştırma sorusu, deney tasarımı ve yazılım prototipi mevcut; ancak kabul edilmiş bağımsız vaka sayısı **0**, yeni çalışmanın formal model çıktısı **0**, kalibrasyon gözlemi **0** ve exact CUDA/model-runtime doğrulaması tamamlanmış değil.

| Bileşen | Durum |
|---|---|
| Kaynak envanteri | BugsInPy sabit sürümünde 501 ham metadata kaydı / 17 proje; bu sayı kabul edilmiş vaka sayısı değildir. |
| Güncel intake | V10 yerel metadata sırası: 100 aday / 14 upstream proje; 407 adaylık yenilenmiş kuyruğun ardından oluşturuldu. 61 tarihsel + 32 güncel teknik/maruziyet kaydı = 93 kalıcı dışlama; seçilen V10 listesiyle kesişim 0. Uzak CI doğrulaması hâlâ bekliyor. |
| Kabul edilmiş doğrulayıcı vakalar | **0**; vaka sicili bilerek boş. |
| Yazılım prototipi | Qwen adapter'ı, yapılandırılmış çıktı ayrıştırma, belirsizlik/politika katmanı, paket hash/referans denetimi, inference kapısı ve sentetik birim testleri var. |
| Semantik kanıt desteği | Prompt/parser, adapter arayüzü ve hash-bağlı paket giriş noktası mevcut. 12 temel sentetik test, hash-bağlama regresyon testleri eklenmeden önce yerelde geçmişti; yeni birleşik test paketinin tamamı için doğrulanmış geçiş sonucu yok. Son GitHub Actions denemeleri adım kaydetmeden başarısız oldu. Gerçek Qwen denetçi çağrısı ve insan puanlarıyla geçerlik de henüz doğrulanmadı. |
| Keşifsel smoke | 10 çıktı; P0 ve P1 koşullarının ikisinde de 0/5 açık kaçınma. Maruziyet, prompt sızıntısı ve runtime uyumsuzluğu nedeniyle doğrulayıcı sonuç değil. |
| Kalibrasyon / ön kayıt / runtime | Kalibrasyon verisi boş; doğrulanabilir ön kayıt yok; tam model/tokenizer/CUDA runtime denetimi tamamlanmadı. |
| Başvuru | Gerçek deney, kör puanlama ve analiz tamamlanmadan proje tamamlanmış araştırma olarak sunulamaz. |

V10 aday sırası ve maruziyet denetimi: [STAGE1_V10_METADATA_INTAKE_2026-10-23.md](research_candidates/evidence_abstention/STAGE1_V10_METADATA_INTAKE_2026-10-23.md). Tek kaynaklı güncel durum: [CURRENT_STATUS_AND_EXECUTION_PLAN_2026-10-23.md](research_candidates/evidence_abstention/CURRENT_STATUS_AND_EXECUTION_PLAN_2026-10-23.md). Semantik auditor için sınırlar ve doğrulama gereksinimleri: [SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md](research_candidates/evidence_abstention/SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md). Önceki smoke tanılaması: [EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md](research_candidates/evidence_abstention/EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md).

**Üç aşamalı plan:** (1) en az 60 kabul edilmiş bağımsız vaka/8 upstream proje, iki ayrık insan paneli, semantik auditor validasyonu, kalibrasyon, model-runtime, hash dondurma ve ön kayıt kapılarını kapat; (2) sadece tüm kapılar kapandıktan sonra E1/E2/E3 × P0/P1 deneyini yürüt, kör puanla ve önceden planlanan istatistiği hesapla; (3) gerçek sonuçları ve sınırlılıkları resmi TÜBİTAK raporuna aktar ve başvuruyu tamamla.

TÜBİTAK'ın 2026–2027 çağrısında başvuru son tarihi **4 Ocak 2027 saat 17.30 (Türkiye saati)** olarak duyurulmuştur: [resmî çağrı](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi). Finalistlik hedefi korunur; sonuç garanti edilemez. Eski CCDG verileri ve sonuçları bu yeni araştırmaya taşınmayacaktır.

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
