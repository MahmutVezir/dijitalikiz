# Aşama 1 çıkış denetimi — 21 Ekim 2026

## Karar

**Aşama 1 için iç araştırma taslağı oluşturma işi ilerlemiş durumda; bilimsel/protokol kapısı henüz kapanmış değildir.** Bu ayrım özellikle korunur: hedefli literatür taraması ve deney taslağı hazır olması, sistematik tarama, bağımsız uzman incelemesi, protokol dondurma veya ön kayıt yerine geçmez.

## 1. Araştırma sorusunun kapsamı

Mevcut birincil soru şudur: aynı yazılım kusuru ve aynı kanıt paketi altında, kaçınmaya izin veren politika (P1), zorunlu teşhis politikası (P0) ile karşılaştırıldığında E3 — insan panelince yetersiz bulunan kanıt — durumunda desteklenmeyen kesin teşhis oranını azaltıyor mu?

Bu bir **politika talimatı müdahalesi** sorusudur. P0 açıkça “kaçınma”yı yasakladığı, P1 ise yetersiz kanıtta kaçınmaya izin verdiği için sonuçlardan tek başına modelin iç belirsizliğini bildiği, güven kalibrasyonu yaptığı veya genel olarak güvenilir olduğu çıkarılamaz. Makale ve TÜBİTAK raporu bu sınırı açıkça söylemelidir.

## 2. Birincil ölçütün tuzakları ve yorum kuralı

E3’te “kaçınma veya desteklenen ifade = desteklenmeyen kesin teşhis değil” kodlaması P1’in sürekli kaçınması durumunda da düşük birincil oran üretebilir. Bu nedenle:

- Birincil sonlanım, önceden belirlenmiş olarak E3’te P0–P1 eşleştirilmiş desteklenmeyen kesin teşhis oranı olarak kalabilir; ham vaka düzeyindeki 0/1 değerler ve uyumsuz çiftler raporlanır.
- Sonucun pratik yararı **E1 koruyucu ölçütleriyle** birlikte yorumlanır: E1’de doğru ve kanıtla destekli teşhis oranı, E1’de gereksiz kaçınma ve yanıt kapsamı açıkça raporlanır.
- E3 birincil ölçüt iyileşse fakat E1’deki doğru/destekli teşhis veya yanıt kapsamı belirgin biçimde kötüleşse, bulgu “seçici kaçınma daha iyi” olarak genellenmez; güvenlik-kapsam ödünleşimi olarak raporlanır.
- E1 koruyucu ölçütleri için doğrulayıcı bir eşdeğerlik/olmama-kötüleşme iddiası ancak marjı, örneklem gücü ve test yöntemi önceden bağımsız biçimde onaylanırsa kurulabilir. Aksi durumda ikincil sonuçlar betimleyici/keşifseldir.

Bu kural, çıktılar görülmeden önce açıkça protokole ve analiz planına işlenmelidir.

## 3. İddia sınırları

Hedefli 2025–2026 taramasında genel abstention benchmarkları, kod üretiminde belirsizlik/kaçınma, kod tahmininde erteleme, kanıt yeterliliği ve yazılım hata yerelleştirme/onarma halüsinasyonları gibi yakın çalışmalar bulundu. Bu nedenle “ilk çalışma”, “benzersiz yöntem” ve “daha önce yapılmadı” iddiaları mevcut kanıtla desteklenmiyor.

Olası dar katkı, gerçek açık kaynak kusurlarından doğrulanmış kök nedenler; buggy revizyonda hedef testin başarısız, fixed revizyonda aynı testin başarılı olduğunun kanıtlanması; modelin gördüğü kanıt paketlerinin önceden tanımlanıp kör insan panelince etiketlenmesi; ve doğruluk ile kanıtsal desteğin ayrı ölçülmesi birleşimidir. Bu katkının literatürdeki özgünlüğü tam metin/atıf zinciri taraması tamamlanmadan kanıtlanmış sayılmaz.

## 4. Protokolü dondurmadan önce zorunlu kararlar

1. Sistematik arama kapsamı (veri tabanları, tarih aralığı, dahil/dışla ölçütleri, yinelenen kayıtlar ve karar günlüğü) oluşturulmalı; hedefli tarama sistematik tarama gibi adlandırılmamalı.
2. P0/P1 istemlerinin gerçekten yalnızca politika talimatında ayrıştığı hash ve otomatik testlerle doğrulanmalı.
3. E1/E2/E3 paketleri yuvalanmış kanıt kuralıyla hazırlanmalı; her silinen kanıt öğesi için gerekçe kaydedilmeli; gold root-cause veya fix sızıntısı aranmalı.
4. Puanlama rubriği, ayrı ve kesişmeyen iki kişilik panel, kalibrasyon vakaları ve uyuşmazlık/adjudication işlemi bağımsız kişiler tarafından onaylanmalı. Kalibrasyon vakaları ana örnekleme dahil edilmemeli.
5. Hedef 80, minimum 60 bağımsız vaka ve en az 8 upstream proje koşulu korunmalı. 60/80 altına düşülürse kabul ölçütleri geriye dönük gevşetilmemeli; yetersiz örneklem keşifsel raporlanmalı.
6. Analiz betiği, model/tokenizer/runtime, prompt/schema, vaka ve kanıt manifestleri ile hash'ler inference öncesi dondurulmalı ve kamuya açık/kurumsal bir ön kayıt kimliği oluşturulmalı.

## 5. Mevcut durum

- Hedefli literatür supplement'i: yazıldı; sistematik derleme değil.
- Taslak RQ/hipotezler, promptlar, JSON schema, rubrik ve analiz planı: mevcut; bağımsız review ve hash freeze tamamlanmadı.
- Ön kayıt URI: boş; ön kayıt yapılmadı.
- Model/runtime yükleme preflight'ı: çalıştırılmadı.
- Model çıkarımı: **yapılmadı ve yetkilendirilmedi**.

## Çıkış ölçütü

Bu memo Aşama 1'in eksiklerini somutlaştırır; kendisi Aşama 1'in nihai olarak geçtiğine ilişkin bir beyan değildir. Aşama 1 ancak yukarıdaki maddeler kayıt altına alınıp bağımsız araştırma/proje danışmanı tarafından incelenince kapatılabilir.