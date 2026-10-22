# Aşama Durum Raporu — 22 Ekim 2026

**Araştırma:** Belirsizlik altında kanıtla desteklenmeyen kesin teşhisten kaçınma  
**Hedef:** 2027 TÜBİTAK 2204-A için tamamlanmış ve savunulabilir araştırma  
**Karar:** Aşama 1, 2 ve 3'ün bilimsel/deneysel kapanışı henüz sağlanmadı. Aşama 3'ün yazılım prototipi ve testleri hazır; gerçek model deneyi kapalı. Aşama 4 model çıkarımı başlatılmadı.

## Durum özeti

| Aşama | Bugünkü durum | Kanıt |
|---|---|---|
| 1 — Veri, protokol ve bağımsız doğrulama | Açık | 501 ham metadata kaydı / 17 proje; kabul edilmiş doğrulayıcı vaka sayısı 0. V8 ilk sekiz teknik aday taraması tamamlandı. Dört aday ayrı insan incelemesine aktarıldı; hiçbiri kabul edilmedi. |
| 2 — Model ve çalıştırma hattı | Kısmen uygulandı | Qwen/Qwen2.5-3B-Instruct adapter'ı ve ayrı inference kapısı var. Canlı Qwen yükleme testi yapılmadı; runtime manifestinde doğrulama hâlâ not_run. |
| 3 — Belirsizlik, kalibrasyon ve kaçınma | Yazılım prototipi test edildi; model davranışı doğrulanmadı | Normalize token entropisi, çoklu yanıt ayrışması, ampirik kalibrasyon, Brier/ECE, fail-closed karar katmanı, katı JSON parser ve Qwen adapter'ı mevcut. Son CPU CI çalışmasında 37 test geçti. |
| 4 — Önceden kaydedilmiş gerçek deney | Başlamadı | Kabul edilmiş veri, doğrulanmış runtime, dolu kalibrasyon kümesi, dondurulmuş hash'ler, doğrulanabilir ön kayıt ve ayrı yürütme izni yok. |

## Aşama 1 — V8 teknik tarama sonucu

Sabit kaynak revizyonu BugsInPy 11c5f1eea954a42132cfd06bf257766a7963e0fd üzerinde, metadata sırası korunarak sekiz aday kontrol edildi. İş akışı: [GitHub Actions run 39818472947](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39818472947).

- **FastAPI-5, Keras-4, Scrapy-5, Sanic-5:** kayıtlı Python sürümü eşleşti; buggy revision'daki hedef test başarısız, fixed revision'daki aynı hedef test başarılı; artefakt hash denetimi geçti. Bunlar yalnızca bağımsız kök-neden incelemesine aktarıldı.
- **Black-6:** buggy günlükte eksik test fixture'ı veya harness dosyası uyarısı.
- **Matplotlib-4:** ortam/bağımlılık hatası sinyali; fixed hedef test de başarısız.
- **Luigi-5:** runtime Python metadata ile açıkça eşleşmedi veya tutarlı biçimde kaydedilemedi.
- **Pandas-4:** pinlenmiş pytest kurulumu, hedef test her iki revision'da da çalıştırılmadan önce başarısız oldu.

Ham artefaktlar ve SHA-256 değerleri [V8 insan inceleme kuyruğunda](STAGE1_MANUAL_REVIEW_QUEUE_V8_2026-10-22.json) kaydedildi. Bu rapor hiçbir vakayı kabul etmez. İnsan kök-neden paneli, ayrı ve disjoint kanıt yeterliliği paneli, lisans/provenance, leakage ve vaka bağımsızlığı kontrolleri hâlâ zorunludur. Global kabul eşiği en az 60 bağımsız vaka ve en az 8 upstream projedir; hedef 80 vakadır.

## Aşama 2 — Model bağlantısı

Qwen adapter'ı beş önceden tohumlanmış aday üretimini, her adayın ham çıktısını/hash'ini ve üretilen tokenların Transformers generation-score entropisini kaydedebilecek teknik altyapıya sahip. Skorlar decoding işlemcilerinden sonra gelen generation scores'tur; ham base-model logits diye adlandırılmıyor.

Buna rağmen:
- tam model/tokenizer/runtime yükleme doğrulanmadı;
- inference için yeterli kabul edilmiş vaka ve gözden geçirilmiş kalibrasyon verisi yok;
- bağımsız kanıt desteği ve çelişki değerlendirme modülü üretimde doğrulanmadı;
- ana doğrulayıcı manifestinde inference izni kapalı kaldı.

## Aşama 3 — Mevcut mekanizma ve yöntem sınırları

Uygulama; normalize token entropisi, yanıtlar arası sözcüksel Jaccard ayrışması, yeterli örnek bulunduğunda Laplace-yumuşatılmış ampirik kalibrasyon, Brier skoru, ECE ve eksik/çelişkili kanıt, geçersiz referans, eksik sinyal veya kalibrasyon yokluğunda fail-closed karar içeriyor. Bir model açıkça kaçınma istediğinde karar katmanı bunu teşhise çevirmiyor.

Son doğrulanan test akışı: [Actions run 39821402510](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39821402510). Ayrı, salt-okunur inference hazırlık kapısı: [Actions run 39821402359](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39821402359).

Bu durum modelin halüsinasyon oranının düştüğünü kanıtlamaz. Aynı modelin tekrarlı örneklemeleri saf epistemik belirsizlik ölçüsü değildir; decoding değişkenliğini de içerir. Sözcüksel ayrışma semantik eşdeğerlik ölçüsü değildir. Kalibrasyon verisi boş olduğundan geçerli bir güven olasılığı henüz yoktur. Ayrıca veri setindeki gold E1/E2/E3 etiketi karar motoruna runtime tahmini gibi verilmemelidir; böyle yapmak cevaplanabilirlik koşulunu sızdırır ve testi döngüsel hâle getirir. Ayrı runtime kanıt-yeterliliği değerlendiricisi henüz doğrulanmadı.

## Aşama 4'e geçiş kriterleri

Gerçek model deneyi ancak aşağıdaki bütün koşullar kapandıktan sonra yürütülmelidir:

1. En az 60 kabul edilmiş bağımsız hata vakası / en az 8 ayrı upstream proje; hedef 80.
2. Aynı kayıtlı Python/runtime'da buggy-fail ve fixed-pass hedef test günlükleri; doğrulanmış kaynak, lisans, root-cause ground truth ve önceki maruziyet/leakage denetimi.
3. Kök neden için en az iki bağımsız değerlendirici ve bu panelle çakışmayan iki kanıt yeterliliği değerlendiricisi; hazırlanmış E1/E2/E3 paketleri.
4. Qwen ve tokenizer'ın sabit revision ile no-output runtime yükleme denetimi; runtime ve chat-template fingerprint'lerinin kaydı.
5. Ayrı, gerçek etiketli kalibrasyon kümesi; threshold'ların bağımsız validation verisinde seçilip dondurulması; gereken artefakt SHA-256 değerlerinin doğrulanması.
6. Deney protokolünün sonuçlar görülmeden doğrulanabilir biçimde ön kaydı ve ayrıca açık yürütme izni.

Mevcut ayrı manifest bu koşulları karşılamıyor ve bilerek inference_allowed=false tutuyor. Bu nedenle gerçek Qwen inference veya halüsinasyon azalması iddiası bu raporun parçası değildir.

## İlgili pull request'ler

- [PR #79 — Qwen belirsizlik adapter'ı ve kapalı çıkarım altyapısı](https://github.com/MahmutVezir/dijitalikiz/pull/79)
- [PR #80 — V8 teknik tarama ve bağımsız insan inceleme kuyruğu](https://github.com/MahmutVezir/dijitalikiz/pull/80)

Her iki PR da taslak durumundadır; ana dalın bilimsel vaka sicili değiştirilmemiştir.
