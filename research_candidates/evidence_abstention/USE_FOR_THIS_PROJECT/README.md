# Bu proje için kullanılabilir materyaller

**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Durum:** Aşama 1 hedefli literatür taraması tamamlandı; Aşama 2 kaynak fizibilitesi koşullu geçti; Aşama 3 deney tasarımı belgelendirme olarak tamamlandı. **Doğrulanmış deney veri kümesi hazır değildir ve model çıkarımı kapalıdır.**

Bu klasör, yeni araştırmanın tasarım belgelerini ve yeniden kullanım kurallarını tek yerde toplar. Burada bulunmak, bir belgenin nihai ön kayıt olduğu veya bir veri vakasının deney için kabul edildiği anlamına gelmez.

## Tasarım ve yöntem

- [Aşama 3 tasarım kapanış denetimi](STAGE3_REVIEW_AND_EXIT.md)
- [Deney tasarımı](STAGE3_EXPERIMENT_DESIGN.md)
- [Prompt koşulları](PROMPT_CONDITIONS.md)
- [JSON çıktı şeması](OUTPUT_SCHEMA.json)
- [Analiz planı](ANALYSIS_PLAN_STAGE3.md)
- [Fail-closed deney manifesti](EXPERIMENT_MANIFEST_STAGE3.json)
- [Protokol taslağı](PROTOCOL_DRAFT.md)
- [Hedefli literatür ve ön özgünlük denetimi](LITERATURE_REVIEW.md)
- [Veri kaynağı fizibilitesi](DATA_FEASIBILITY.md)
- [Metadata biçim örnekleri — doğrulayıcı veri değildir](FEASIBILITY_FORMAT_SAMPLE.csv)
- [Yeniden kullanım kuralları](REUSE_RULES.md)

## Depo kapsamı

- [Yetkili kapsam ayrımı](../REPO_SCOPE_SPLIT.md)
- [İzin verilen materyallerin makine tarafından okunabilir manifesti](MANIFEST.json)
- [Kullanılamayan eski veri ve sonuçlar için dışlama politikası](../DO_NOT_USE_AS_EVIDENCE/README.md)
- [Dışlama manifesti](../DO_NOT_USE_AS_EVIDENCE/MANIFEST.json)

## Açık kapılar

1. En az 60 bağımsız kabul edilmiş vaka ve en az 8 ayrı upstream proje (hedef 80).
2. Her vaka için kayıtlı ortamda buggy-fail/fixed-pass logları, lisans kontrolü ve doğrulanmış kök neden.
3. E1/E2/E3 kanıt paketlerinin model çıktılarından bağımsız değerlendirilmesi.
4. İki değerlendiricili puanlama rubriği ve anlaşmazlık çözümünün dondurulması.
5. Prompt, şema, vaka paketi, model/tokenizer/runtime, runner ve analiz dosyalarının SHA-256 hash'leri.
6. Ön kayıt ve ayrıca onaylanmış inference izni.

Eski DİJİTALİKİZ pilot/confirmatory verileri, puanları, sonuçları ve TÜBİTAK raporları bu araştırmanın bilimsel kanıtı değildir. Tarihsel dosyalar kaynak konumlarında korunur; [dışlama politikası](../DO_NOT_USE_AS_EVIDENCE/README.md) onları yeni deneyden ayırır.
