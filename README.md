# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tek aktif hedef: 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde, tamamlanmış ve bilimsel olarak savunulabilir bir araştırma sunmak.** Bu hedef bir çalışma yönüdür; finalistlik sonucu garanti edilemez.

**Bilimsel rapor için önerilen başlık:** *Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi*

## Güncel durum — 21 Ekim 2026

**Proje tamamlanmış değildir.** Araştırma sorusu, taslak deney tasarımı ve ön kontroller hazırlandı; fakat doğrulanmış vaka kümesi ve yeni deney sonucu henüz yoktur.

| Kontrol | Kanıtlanan durum |
|---|---|
| Kaynak envanteri | BugsInPy sabit revizyonunda 17 projeden 501 ham metadata kaydı |
| Temel metadata kapısı | 500 kayıt geçti; 1 kayıt buggy/fixed commit tutarsızlığı nedeniyle sorunlu |
| Gerçek test çifti doğrulaması | 0 |
| Kabul edilmiş bağımsız doğrulayıcı vaka | **0** |
| Yeni proje için LLM çıkarımı | **Yapılmadı; kapalı** |
| Teknik ön kontrol | GitHub Actions geçti; rapor yine de `ready=false` diyor |

Ayrıntı: [metadata envanteri sonucu](research_candidates/evidence_abstention/METADATA_INVENTORY_RESULT_2026-10-21.md), [teknik hazırlık denetimi](research_candidates/evidence_abstention/STAGE4_TECHNICAL_READINESS_2026-10-21.md) ve [ön kontrol çalışması](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39619057132).

501 kayıt bir deney örneklemi değildir. Doğrulayıcı çalışma için **en az 60 bağımsız vaka ve en az 8 ayrı upstream proje** gereklidir; hedef 80 vakadır. Her vaka için aynı hedef testin buggy sürümde beklenen kusuru göstermesi, fixed sürümde geçmesi, uygun lisans, doğrulanmış kök neden, kanıt seviyeleri, sızıntı ve önceki maruziyet kontrolleri gerekir.

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
