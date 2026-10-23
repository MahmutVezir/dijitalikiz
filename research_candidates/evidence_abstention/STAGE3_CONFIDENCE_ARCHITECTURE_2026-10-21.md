# Aşama 3 — Güven puanı ve cevap vermekten kaçınma mimarisi

**Durum:** Teknik prototip. Ana doğrulayıcı deneyin parçası değil; henüz gerçek model çıkarımı yapılmadı.  
**Tarih:** 21 Ekim 2026

## 1. Mevcut aşama denetimi

- Aşama 1 tamamlanmadı: kabul edilmiş bağımsız vaka sayısı 0; insan kök-neden ve kanıt yeterliliği incelemesi, lisans/sızıntı kapıları ve protokol ön kaydı açık.
- Aşama 2 kısmen hazır: BugsInPy metadata envanteri var (501 ham kayıt / 17 proje), fakat metadata envanteri test çiftini doğrulamaz. Model/tokenizer/runtime henüz çalıştırılıp sabitlenmedi.
- Önceden tasarlanan E1/E2/E3 × P0/P1 deneyinde P0 ve P1 her hücrede tek, greedy çıktı üretir. Aşağıdaki motor çoklu örnekleme ve logit sinyali ekler; bu nedenle mevcut doğrulayıcı koşuya sessizce bağlanmamalıdır.

## 2. Önerilen karar hattı

1. **Kanıt sözleşmesi:** Kanıt paketine sabit kimlikler verilir. E1/E2/E3 koşul etiketi deney tasarımı ve sonuçları katmanında saklanır; model istemine, adapter girdisine veya karar fonksiyonuna doğrudan verilmez. Model yalnızca gerçek çalıştırmada gördüğü kanıt paketini alır. Paket bütünlüğü ve çalışma-zamanı kanıt denetiminin sonuçları, E1/E2/E3 gold etiketiyle aynı şey değildir. Bağımsız inceleyiciler koşul etiketi ve model çıktısını görmeden kanıt yeterliliğini puanlar.
2. **Üretim kaydı:** Model/tokenizer revision, chat template, prompt/kanıt hash'i, decoding ayarları ve çalışma zamanı kaydedilir. Token entropisi hesaplanacaksa yalnızca üretilen yanıt token'larının logits değerleri kullanılır; prompt/padding token'ları dahil edilmez. Tek tek token entropileri ortalanır.
3. **Kararlılık:** Aynı vaka için önceden belirlenmiş K bağımsız üretim alınır. Prototip en az iki cevapla çalışır; gerçek deney için K ve decoding ayarları önceden belirlenmelidir. Lexical Jaccard ayrışması yalnızca kelime-temelli vekil ölçüdür; anlamsal eşdeğerlik veya saf epistemik belirsizlik ölçüsü değildir.
4. **Kanıta dayalı destek:** Yanıttaki iddiaların kanıt paketince desteklenen oranı supported_claim_coverage olarak girilir. Sadece kaynak ID'sinin var olması destek kanıtlamaz; bağımsız ve önceden tanımlı değerlendirici gerekir. Modelin kendi beyanı tek başına destek denetimi sayılmaz. Çelişki durumunun bilinmemesi de ret sebebidir.
5. **Sinyal birleştirme:** uncertainty_index = max(normalized_token_entropy, lexical_disagreement, 1 - supported_claim_coverage, self_check_conflict). Bileşenleri gelişigüzel ağırlıklandırmamak için maksimum kullanılır. Bu endeks olasılık değildir; güven puanı diye yorumlanmaz.
6. **Kalibrasyon:** Ayrı kalibrasyon bölümünde hedef etiket “kök neden doğru **ve** sunulan kanıt tarafından destekli” olur. EmpiricalConfidenceCalibrator sabit aralıklarda Laplace-yumuşatılmış ampirik başarı oranı hesaplar; bir aralıkta yeterli örnek yoksa puan üretmez. Brier skoru ve ECE raporlanır. Kalibrasyon/test ayrımı vaka ve mümkünse upstream proje düzeyinde yapılmalıdır. Kalibrasyon artefaktının SHA-256 kimliği dondurulmalı ve doğrulanmış olmalıdır.
7. **Fail-closed karar:** Paket bütünlüğü geçersiz/bilinmiyor, kanıt denetimi veya gerekli belirsizlik sinyali eksik, açık çelişki var ya da kalibrasyon/eşik dondurulmamışsa doğrudan kaçın. Motor E1/E2/E3 gold etiketini kontrol girdisi olarak kullanmaz; özellikle deneyde E3 etiketi görünür olduğu için kaçınmak, E3 altındaki kaçınma performansını döngüsel ve geçersiz hâle getirir. E3'e ait etki, modelin yalnızca yetersiz paket içeriğinden hareketle ne yaptığıyla ölçülür. Diğer durumlarda motor belirsizlik endeksini kendisi hesaplar; aynı endeks kalibratöre verilerek ampirik güven tahmini türetilir. Kalibrasyon diliminde yeterli örnek yoksa da kaçınır. Ancak bağımsız ve ayrı kalibrasyonla dondurulmuş tahmin/eşik şartları geçerse teşhis döndürür.
8. **İzlenebilir çıktı:** Karar, gerekçeli ret kodları, ham sinyaller, kalibrasyon kimliği, model ve vaka hash'leri kaydedilir. Ham model yanıtı asla otomatik onarılmaz; ret sebebi silinmez.

## 3. Pseudo-code

~~~text
packet = load_frozen_packet()
if structural_or_hash_validation(packet) is not valid:
    abstain("packet_validation_failed_or_unknown")

answers, score_vectors = generate_K_independent_answers(model, packet)
if generation_or_required_scores_are_missing:
    abstain("uncertainty_signals_incomplete")

audit = audit_visible_claims_against_visible_packet(answers, packet)
if audit is missing, malformed, or semantically unvalidated for this use:
    abstain("evidence_audit_unavailable")
if audit.explicit_contradiction or audit.self_check_conflict is unknown:
    abstain("evidence_contradiction_or_unknown")

entropy = mean_normalized_entropy_over_generated_tokens(score_vectors)
disagreement = lexical_disagreement_proxy(answers)
support = audit.supported_claim_coverage
risk = max(entropy, disagreement, 1 - support, audit.self_check_conflict)

confidence = frozen_calibrator.predict(risk)
if confidence is unavailable or calibration hash/thresholds are not verified:
    abstain("calibration_not_frozen")
if confidence is unavailable for this risk bin:
    abstain("calibration_bin_insufficient")
if risk > maximum_uncertainty or confidence < minimum_confidence:
    abstain("threshold_failed")
return diagnosis_with_evidence_refs()

# E1/E2/E3 condition labels remain in the evaluation data for stratified analysis;
# they are never supplied as a runtime decision feature or hidden-answer shortcut.
~~~



**Etiket sızıntısı için kritik sınır:** E1/E2/E3 seviyeleri deney hücrelerini ve stratifiye analizleri tanımlar; bunlar cevap motoruna doğrudan verilmez. Çalışma-zamanı adapter'ı yetersizliği yalnızca görünür paket içeriği, yapısal doğrulama ve önceden tanımlanmış denetim sinyallerinden çıkarmalıdır. Aynı Qwen modelinin anlamsal denetçisi bağımsız hakem değildir; bu sinyal bağımsız, kör insan puanlarına karşı doğrulanana kadar deneysel olarak doğrulanmış gerçek gibi raporlanamaz. Ana E1/E2/E3 × P0/P1 doğrulayıcı deney, bu çoklu örneklemeli kalibrasyon adapter'ından ayrı tutulur.

## 4. Kodda bulunan parçalar

implementation/uncertainty_policy.py içinde dış bağımlılıksız şu parçalar var:

- logitlerden normalize entropi ve üretilen tokenlar üzerinden ortalama entropi;
- çoklu cevaplar üzerinde sözcüksel Jaccard ayrışması;
- yeterli örnek olan sabit aralıklarda Laplace-yumuşatılmış ampirik güven kalibrasyonu;
- Brier skoru ve Expected Calibration Error (ECE);
- belirsizlik endeksini ve ona karşılık gelen ampirik güven puanını aynı fonksiyonda türeten karar katmanı;
- kanıt, çelişki durumu, referans, sinyal ve kalibrasyon kapılarını uygulayan fail-closed karar.

Birim testleri implementation/test_uncertainty_policy.py ile çalışır. Testler kodun davranışını denetler; model kalitesini, kalibrasyon başarısını veya halüsinasyon azalmasını kanıtlamaz.

## 5. Kör noktalar ve zorunlu tedbirler

- **Düşük token entropisi doğru yanıt demek değildir.** Dil modeli yanlış iddiayı yüksek token olasılığıyla üretebilir.
- **Aynı modelin tekrarları saf epistemik belirsizlik değildir.** Bunlar decoding/öngörüsel kararsızlığı da içerir. Daha güçlü epistemik iddia için farklı checkpoint/ensemble veya ayrı bilgi eksikliği tasarımı gerekir; bu yeni bir deney faktörüdür.
- **Self-check bağımsız doğrulama değildir.** Aynı model aynı yanlışı tekrar onaylayabilir; yardımcı bir sinyal olarak tutulmalıdır.
- **Kelime örtüşmesi semantik benzerlik değildir.** Eşanlamlı cevapları ayrı, farklı cümlelerle anlatılmış aynı kök nedeni aynı sınıfa koyabilir. Bu prototip bu sinyali yalnızca geçici vekil olarak kullanır.
- **Kanıt alıntısı ile destek farklıdır.** Model mevcut bir ID'yi anıp onun desteklemediği bir iddiada bulunabilir. İddia-kanıt desteği ayrıca değerlendirilmelidir.
- **E1/E2/E3, doğrudan üretimden elde edilen gerçek değildir.** Üretimde bu seviye ya önceden doğrulanmış bir paket metadata'sı ya da ayrıca kalibre edilmiş bir değerlendirici tarafından sağlanmalıdır. Aksi halde sistem seviyeyi bilemiyor olabilir.
- **Eşikler keyfî seçilmez.** Güven alt eşiği ve belirsizlik üst eşiği kalibrasyon/tuning verisinde seçilir, bağımsız sertifika/test verisinde değerlendirilir ve test sonuçları görülmeden dondurulur. Küçük örneklemle garanti iddiası yapılamaz.
- **Örneklem sızıntısı:** Aynı bug, kök neden veya upstream proje kalibrasyon ve test bölümlerine dağıtılmamalıdır.
- **Çoklu örnekleme maliyeti ve protokol değişikliği:** K=5 kullanımı her vaka için üretim maliyetini yükseltir ve orijinal tek-greedy tasarımını değiştirir. Tasarım, örneklem hedefi, birincil sonuç ve ön kayıt yeniden gözden geçirilmeden doğrulayıcı koşuda açılmamalıdır.
- **P0 karşılaştırması:** Her durumda kaçınan motor P0 şartına bağlanamaz; P0 zorunlu teşhis koşulu olarak kalır. Motor ayrı bir politika kolu olacaksa faktöriyel tasarım ve analiz planı önceden güncellenmelidir.
- **Kalibrasyon puanı kesinlik garantisi değildir.** Bu sürüm sabit aralıklı ampirik oran ve Laplace smoothing kullanır; conformal risk guarantee veya validasyon garantisi sunmaz.
- **Küçük kalibrasyon dilimleri:** Bir aralıkta yeterli örnek yoksa kod güven olasılığı döndürmez. Veri azlığında şişirilmiş puan yerine ret üretir.

## 6. Kabul kriterleri

Teknik prototipin birim testlerini geçmesi Aşama 1 veya 2'yi kapatmaz. Yeni mekanizma, doğrulayıcı deneyde ancak (a) bağımsız vaka kabul kapıları, (b) model/tokenizer/runtime dondurması, (c) kanıt puanlayıcılarının kalibrasyonu, (d) kalibrasyon ve test ayrımı, (e) eşikler ve protokolün ön kaydı, (f) ayrı yürütme izni tamamlandıktan sonra kullanılabilir. O zamana kadar EXPERIMENT_MANIFEST_STAGE3.json içindeki inference_allowed=false korunur.
