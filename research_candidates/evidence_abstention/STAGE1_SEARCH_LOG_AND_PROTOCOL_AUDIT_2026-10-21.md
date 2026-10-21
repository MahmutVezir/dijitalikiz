# Aşama 1 araştırma denetimi ve literatür arama günlüğü — 21 Ekim 2026

## Karar

**İç araştırma hazırlığı güçlendirildi; Aşama 1 bilimsel olarak kapatılmış değildir.** Bu belge hedefli web taramasını kaydeder. Bu tarama PRISMA uyumlu sistematik derleme olarak sunulamaz: arama motorlarının indeks kapsamı, tam metin erişimi, yinelenen kayıtların sistematik ayıklanması ve bağımsız başlık/özet taraması tamamlanmış değildir.

## Dondurulması önerilen araştırma sorusu

Aynı gerçek yazılım kusuru ve aynı temel bağlam için, insan panelince yetersiz kanıt olarak sınıflanan E3 koşulunda, cevap vermekten kaçınmaya izin veren politika (P1), kesin teşhis vermeyi zorunlu kılan politikaya (P0) kıyasla desteklenmeyen kesin kök-neden teşhislerini azaltıyor mu; bunun yeterli kanıtlı vakalardaki doğru teşhis ve yanıt kapsamı maliyeti nedir?

Bu soru **istem/politika müdahalesini** sınar. Tek başına modelin iç belirsizliği “bildiğini”, iyi kalibre olduğunu veya tüm görevlerde daha güvenilir olduğunu kanıtlamaz.

## 21 Ekim 2026 arama günlüğü

Arama arayüzü: genel web indeksinde hedefli arama. Aşağıdaki sorgular kullanıldı:

1. `("large language models" abstention uncertainty answering when not to answer benchmark 2025 2026)`
2. `software engineering LLM abstention uncertainty code bug localization evidence sufficiency benchmark 2024 2025 2026`
3. `selective prediction abstention large language models calibration confidence survey 2024 2025`
4. `LLM abstention software bug localization fault localization uncertainty benchmark root cause diagnosis answer abstention code`
5. `large language model abstention software engineering debugging diagnosis benchmark "uncertainty" 2025 2026`
6. `selective prediction language models software engineering code repair root cause localization confidence abstention`

Bu sorgularla aşağıdaki yakın çalışmaların yayın sayfaları/özetleri görüldü. Bu liste tarama günlüğüdür; bütün sonuçların kapsamlı envanteri değildir.

| Çalışma | Bu proje açısından anlamı | Kaynak |
|---|---|---|
| Wen et al., *Know Your Limits: A Survey of Abstention in Large Language Models* (TACL 2025) | Abstention yöntemleri, benchmarkları ve ölçütleri genel alanda zaten inceleniyor; geniş bir “ilk” iddiası savunulamaz. | https://aclanthology.org/2025.tacl-1.26/ |
| Madhusudhan et al., *Do LLMs Know When to NOT Answer?* (COLING 2025) | Cevaplanabilir/cevaplanamaz sorularda black-box abstention ölçümü ve AUCM benzeri değerlendirme zaten var. | https://aclanthology.org/2025.coling-main.627/ |
| Kirichenko et al., *AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions* (NeurIPS 2025) | Çoklu alanda abstention benchmarkı var; yalnızca genel “cevap vermeme” davranışı özgün katkı değildir. | https://proceedings.neurips.cc/paper_files/paper/2025/hash/fb122bfc3f0127a94ded048b5b03496f-Abstract-Datasets_and_Benchmarks_Track.html |
| Zhang & Wu, *Do LLMs Know When Evidence is Insufficient?* (2026) | Kanıt yeterliliğine dayalı abstention değerlendirmesi RAG bağlamında incelenmiş; E1/E2/E3 ve kanıtsal destek ayrımıyla ilişkili. | https://www.techscience.com/cmc/v89n1/68467 |
| Rathnasuriya & Yang, *When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions* (ICSE-NIER 2026) | Kod tahmininde ne zaman cevap verilip erteleneceği ve araç kullanımı yakın araştırma alanı. | https://doi.org/10.1145/3786582.3786845 |
| Geng et al., *A Survey of Confidence Estimation and Calibration in Large Language Models* (NAACL 2024) | Öz-bildirim güveni ile gerçek doğruluk/kalibrasyonun ayrılması gerektiğini destekler. | https://aclanthology.org/2024.naacl-long.366/ |
| Kalai et al., *Evaluating large language models for accuracy incentivizes hallucinations* (Nature 2026) | Abstention'ı otomatik olarak yanlış sayan ölçütler tahmin etmeyi teşvik edebilir; yanıt kapsamı ve uygun kaçınma birlikte ölçülmeli. | https://doi.org/10.1038/s41586-026-10549-w |
| *LLMs (Almost) Never Abstain Under Medical Uncertainty* (ACL 2026) | Alana özgü benchmarklar ve abstention seçeneği etkisi zaten inceleniyor; bizim iddiamız yazılım hata teşhisinin özel kanıt yapısına daraltılmalı. | https://aclanthology.org/2026.acl-long.1365/ |

## Özgünlük kararı

Şu aşamada “ilk”, “benzersiz” veya “literatürde yapılmamış” denmeyecek. Savunulabilir olabilecek dar katkı şudur: gerçek açık kaynak kusurlarından doğrulanmış kök neden; aynı testin buggy revizyonda başarısız ve fixed revizyonda başarılı olduğuna ilişkin tekrarlanabilir teknik kanıt; kök neden doğruluğu ile kanıtsal desteği ayrı etiketleyen kör insan panelleri; ve kanıt yeterliliği seviyeleri boyunca cevap/kaçınma politikasının eşleştirilmiş değerlendirmesi. Bu katkının özgünlüğü tam sistematik arama ve uzman incelemesi olmadan kesinleşmiş değildir.

## Protokol düzeltmeleri (inference öncesi zorunlu)

1. P0/P1 istemleri yalnızca kaçınma politikası yönünden farklı olmalı; hash ve testlerle kontrol edilmeli.
2. E1/E2/E3 kanıt paketleri önceden dondurulmalı; E3'te çözümü doğrudan açığa çıkaran patch/fix ifadeleri bulunmamalı.
3. Birincil sonlanım E3'te desteklenmeyen kesin teşhis oranı olarak sabitlenmeli; E1 doğru/destekli teşhis ve gereksiz kaçınma koruyucu ölçütleri olarak raporlanmalı. P1'in sürekli kaçınması, birincil metriği tek başına yapay biçimde iyileştirebilir.
4. Vaka bazlı eşleştirilmiş analiz, ham uyumsuz çift sayıları, risk farkı ve %95 güven aralığı raporlanmalı; tekrarlı model çağrıları bağımsız vaka gibi sayılmamalı.
5. Hedef 80, asgari doğrulayıcı örneklem 60 bağımsız vaka ve en az 8 upstream proje olarak korunmalı. Eşikler sonuç görüldükten sonra gevşetilmemeli.
6. İki kişilik kök-neden paneli ile ayrı ve kesişmeyen iki kişilik kanıt-yeterliliği paneli kullanılmalı. Kalibrasyon vakaları ana örneklemden çıkarılmalı. Değerlendiricilerin yerine model-judge kullanılarak “ground truth” üretilmemeli.
7. Ön kayıt URI, model/runtime, prompt/schema, vaka ve kanıt manifestleri ile analiz betiği hash'leri inference'dan önce kaydedilmeli.

## Aşama 1 için çıkış durumu

- [x] Araştırma sorusu daraltıldı; politika müdahalesi ile modelin iç belirsizlik bilgisi ayrıldı.
- [x] Yakın literatür örnekleri ve kaynak URL'leri kaydedildi.
- [x] Özgünlük iddiası daraltıldı; “ilk çalışma” iddiası reddedildi.
- [x] Birincil metrikte sürekli kaçınma riskine karşı koruyucu ölçütler tanımlandı.
- [ ] Tam sistematik arama protokolü, veri tabanları, tarih aralığı, dahil/dışla ölçütleri, duplicate kayıtları ve arama çıktılarının kalıcı arşivi tamamlanmadı.
- [ ] Bağımsız alan uzmanı/araştırma danışmanı incelemesi ve imzalı karar yok.
- [ ] Ön kayıt oluşturulmadı; URI yok.
- [ ] Prompt, veri, runtime ve analiz hash'leri nihai olarak dondurulmadı.

**Sonuç:** İç taslak işleri büyük ölçüde hazır; Aşama 1'in nihai çıkış kapısı açık kalır. Bu, belirsizliği saklamak değil, bilimsel kapanış ölçütünü doğru uygulamaktır.
