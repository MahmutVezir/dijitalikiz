# Belirsizlik / abstention prototipi

Bu klasör, sabit bir temel LLM üzerine kurulacak kanıt-yeterliliği ve cevap vermeme karar katmanının saf Python prototipini ve birim testlerini içerir.

## Kod kapsamı

- `uncertainty_policy.py`: normalize entropi, yanıtlar arası ayrışma, ampirik kalibrasyon ve cevap/kaçınma karar mantığı.
- `qwen_uncertainty_adapter.py`: Qwen2.5-3B-Instruct için **inference adapter**; fine-tuning veya ağırlık eğitimi yapmaz.
- `qwen_runtime_preflight.py`: model/tokenizer/runtime kontrolü; tek başına cevap üretme yetkisi vermez.
- `uncertainty_inference_gate.py`: read-only inference gate. Gate kapalıyken model yüklenmez ve generation yapılmaz.
- `evidence_packet_audit.py` ve `semantic_evidence_auditor.py`: kanıt paketinin yapısal doğrulaması ve daha sonra insan değerlendirmesiyle doğrulanması gereken semantik denetim arayüzü.

## Test

    python -m unittest discover -s research_candidates/evidence_abstention/implementation -p 'test_*.py' -v

## Eğitim ve inference ayrımı

Bu prototipte **fine-tuning/training kodu yoktur**. Qwen adapter yalnızca sabit model ağırlıklarıyla inference yapabilecek şekilde tasarlanmıştır. Ana doğrulayıcı araştırma sorusu, aynı sabit modelin P0 (kanıt-yeterliliği/abstention kuralı olmadan) ve P1 (kanıta dayalı cevap/kaçınma politikasıyla) koşullarındaki davranışını karşılaştırmaktır. Bu aşamada model ağırlıklarını eğitmek araştırma değişkenlerini karıştırır ve ana karşılaştırmayı geçersizleştirebilir.

Birincil deney için yeni bir LLM eğitmek zorunlu değildir. Önce sabit temel model ve dondurulmuş politika karşılaştırılır. Ayrı bir fine-tuning çalışması ancak yeterli lisanslı veri, bağımsız insan etiketleri, proje-bazlı train/validation/test ayrımı, ön kayıt ve ayrı bir araştırma sorusu oluşturulduktan sonra ikincil çalışma olarak değerlendirilebilir.

## Güvenlik kapısı

- Şu an `UNCERTAINTY_EXPERIMENT_MANIFEST.json` içinde `inference_allowed=false`.
- En az 60 kabul edilmiş bağımsız vaka (hedef 80), en az 8 upstream proje, iki ayrık insan değerlendirme paneli, doğrulanmış test çiftleri, lisans/leakage incelemesi, dondurulmuş ön kayıt ve runtime doğrulaması gerekir.
- 105-ID kalıcı maruziyet birleşimi `EXPOSURE_UNION_2026-11-11.json` olarak sabitlenmiştir.
- Ayrı ve açık inference yetkilendirmesi olmadan `load_authorized_qwen()` çağrılmamalıdır.

Model kararındaki güven puanı, modelin kendi beyanından alınmamalı; bağımsız kalibrasyon setindeki gözlenen doğruluk ve kanıt desteğiyle kalibre edilmelidir. Kalibrasyon aralığında yeterli örnek yoksa sistem `None` üretmeli ve cevap vermekten kaçınmalıdır.
