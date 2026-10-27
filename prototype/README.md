# Kanıt Tabanlı Hata Teşhisçisi — prototip

Bu klasör, önceden eğitilmiş Qwen/Qwen2.5-3B-Instruct modelini sabit revision ile yükleyen ve kanıt paketini değerlendirerek yapılandırılmış teşhis/kaçınma çıktısı veren mühendislik prototipidir. Sıfırdan eğitilmiş bir model değil, önceden eğitilmiş LLM etrafında kurulmuş bir uygulamadır.

## Neler yapar?

- Kod, traceback ve ek bağlam alır.
- Kanıt parçalarına CODE_1, TRACE_1, CONTEXT_1 kimlikleri verir.
- P0 (teşhis vermeye çalış) ve P1 (yetersiz kanıtta kaçın) politikasını destekler.
- Sabit Qwen revision'ı ve deterministik decoding kullanır.
- JSON şeması ile kanıt kimliklerini denetler; P1'de kaynak gösteremeyen teşhisi yayımlamaz.
- Semantik doğruluğu otomatik kanıtladığını iddia etmez.

## Çalıştırma

GPU'lu Python ortamında `torch`, `transformers`, `accelerate` ve `gradio` hazırsa proje kökünden:

```bash
python prototype/gradio_app.py
```

Model ağırlıkları sabit Hugging Face revision'ından indirilir; Hub erişimi gerekir. GPU yoksa uygulama sessizce CPU'ya geçmez. İsteğe bağlı CPU denemesi `EVIDENCE_ALLOW_CPU=1` ile etkinleştirilebilir.

## Bilimsel sınır

Bu prototip doğrulayıcı deney runner'ından ayrıdır. Vaka sicilini okumaz/değiştirmez, manifest izinlerini açmaz ve deney sonucu üretmez. JSON/atıf biçim kontrolü, kök nedenin gerçekten kanıtlandığı anlamına gelmez. Halüsinasyon azaltımı iddiası için bağımsız vaka ve kör insan değerlendirmeleri gerekir.
