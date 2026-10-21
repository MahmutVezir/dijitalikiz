# Belirsizlik / abstention prototipi

Bu klasörde saf Python karar mantığı ve birim testleri bulunur. Model indirmez, inference yapmaz, deney verisi oluşturmaz.

Test:

    python -m unittest discover -s research_candidates/evidence_abstention/implementation -p 'test_*.py' -v

Ana API:
- normalized_entropy_from_logits ve mean_normalized_token_entropy: üretilen tokenların logit dağılımlarından normalize entropi.
- lexical_disagreement: çoklu yanıtlar arasında sözcüksel Jaccard ayrışması.
- EmpiricalConfidenceCalibrator: ayrı ve etiketlenmiş kalibrasyon setindeki gözlenen doğruluk + kanıt desteği oranından, yeterli örnek bulunan aralıklarda Laplace-yumuşatılmış ampirik olasılık üretir.
- decide(request, calibrator, policy): belirsizlik endeksini kendisi hesaplar ve aynı endeksi kalibratöre vererek güven puanını türetir; çağıran tarafın endeksle ilgisiz bir güven puanını içeri vermesini önler.

policy.calibration_id doğrulanmış kalibrasyon artefaktının SHA-256 kimliği olmalı; calibration_verified ancak artefakt ve eşikler gerçekten doğrulandıktan sonra true olabilir. Aralık örnek sayısı yetmiyorsa None döner ve motor kaçınır. Bu prototipte eşiklerin kendisi önceden dondurulmuş bir artefaktla yüklenmiş değildir.
