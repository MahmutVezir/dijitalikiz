# Belirsizlik / abstention prototipi

Bu klasörde sadece saf Python karar mantığı ve birim testleri vardır. Model indirilmez, inference yapılmaz, hiçbir deney verisi oluşturulmaz.

Test komutu:

    python -m unittest discover -s research_candidates/evidence_abstention/implementation -p 'test_*.py' -v

Ana API:
- normalized_entropy_from_logits(logits): sözlük logits dağılımından normalize entropi.
- lexical_disagreement(answers): çoklu yanıtlar arasında sözcüksel Jaccard ayrışması.
- EmpiricalConfidenceCalibrator: bağımsız kalibrasyon örneklerinden ampirik destekli-doğruluk oranı; aralık örnek sayısı yetersizse None.
- decide(DecisionRequest(...)): eksik/çelişkili kanıt, geçersiz referans, eksik belirsizlik sinyali veya kalibrasyon yokluğunda kaçınma.

Güven kalibrasyonu yalnızca aynı görev/model/kanıt dağılımına uygun, ayrı ve etiketlenmiş kalibrasyon verileriyle anlamlıdır. Varsayılan eşik yoktur; eşikler araştırmacı tarafından test sonuçları görülmeden önceden dondurulmalıdır. Uygulama şu an araştırma protokolüne bağlanmamıştır.
