# Kanıt Tabanlı Hata Teşhisçisi — keşifsel prototip

Bu arayüz, araştırma sorusuna bağlı tek-vaka mühendislik demosudur. Çıktıları doğrulayıcı örnekleme girmez ve TÜBİTAK raporunda ana deney sonucu olarak kullanılamaz.

## Projeyle uyum

- Ana Stage 3 runner ile aynı sabit system prompt, P0/P1 politika metinleri, kanıt öğesi kimlikleri ve kanonik OUTPUT_SCHEMA.json kullanılır.
- Kanıt yeterliliği etiketi (E1/E2/E3) prompt'a eklenmez; model yalnızca kanıt paketini görür.
- Tek örnek üzerinden modelin ham yanıtı korunur. Geçersiz JSON veya kanıt ID'si otomatik düzeltilmez; gözlenen karar otomatik olarak abstain'e çevrilmez.
- JSON biçimi ve referans denetimi semantik destek anlamına gelmez; bu boyut not_assessed olarak kalır.
- Her raporda model revision, prompt/packet/raw-output SHA-256 ve gözlemlenebilen runtime bilgisi bulunur.

## Çalıştırma

GPU'lu Python ortamında torch, transformers, accelerate ve gradio hazırsa depo kökünden:

    python prototype/gradio_app.py

Model ağırlıkları sabit Hugging Face revision'ından indirilir; Hub erişimi gerekir. GPU yoksa uygulama sessizce CPU'ya geçmez. İsteğe bağlı CPU denemesi EVIDENCE_ALLOW_CPU=1 ile etkinleştirilebilir.

## Bilimsel sınır

Bu prototip, resmi araştırma runner'ının yerine geçmez. Ana deney için her bağımsız kabul edilmiş vaka E1/E2/E3 × P0/P1 koşullarında çalıştırılır; yalnızca research_candidates/evidence_abstention/kaggle_stage3_p0_p1.py resmi çıktı runner'ıdır. Manifestteki yürütme kapısı açıkça yetkilendirilmeden doğrulayıcı çıkarım başlatılamaz. Prototipin çalışması hipotezi kanıtlamaz.
