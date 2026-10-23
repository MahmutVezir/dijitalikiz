# Ön kayıt taslağı v1.1 — Yazılım hata teşhisinde kanıt yeterliliği ve cevap vermekten kaçınma

**Sürüm:** 1.1-draft  
**Tarih:** 23 Ekim 2026  
**Durum:** Taslak; haricî ön kayıt yapılmadı, hash manifesti dondurulmadı ve çıkarım izni yoktur. Bu belge, önceki V1 taslağındaki yöntem çelişkisini sonuçlar görülmeden önce giderir. Önceki V1 dosyası tarihsel kayıt olarak korunur; mevcut deney planı için bu sürüm esas alınır.

## 1. Araştırma sorusu ve hipotez

**Araştırma sorusu:** Gerçek, bağımsız olarak doğrulanmış açık kaynak yazılım kusurlarında, kanıt yetersizken teşhis vermekten kaçınmaya açıkça izin veren bir talimat (P1), teşhisi zorunlu kılan temel talimata (P0) kıyasla kanıtla desteklenmeyen kesin kök-neden teşhislerini azaltıyor mu? Bu farkın, yeterli kanıt bulunan vakalarda doğru teşhis ve cevap kapsamı bakımından maliyeti nedir?

**Birincil hipotez:** E3 (yetersiz kanıt) koşulunda P1, vaka başına kanıtla desteklenmeyen kesin teşhis oranını P0'a kıyasla düşürür.

Bu bir yönlü araştırma beklentisidir; sonuçlar bunu doğrulamak zorunda değildir. Sıfır fark, ters fark veya geçersiz/puanlanamayan çıktılar da aynı açıklıkla raporlanacaktır.

## 2. Ana doğrulayıcı tasarım — istem politikası deneyi

### Model ve sabit çalıştırma davranışı

- Model: Qwen/Qwen2.5-3B-Instruct, revizyon aa8e72537993ba99e69dfaafa59ed015b17504d1.
- Modelin ve tokenizer'ın sabit revizyonda, belirtilen çalışma ortamında çıktı üretmeden yükleme denetimi yapılmalıdır.
- Ana deney için decoding deterministiktir: do_sample=false; otomatik yeniden üretim, JSON onarımı veya cevabı seçerek saklama yoktur.
- Her vaka × kanıt düzeyi × politika hücresi için **tek ham model yanıtı** alınır.
- Ana deney istemleri, çıktı şeması ve koşulların tanımları PROMPT_CONDITIONS.md ile OUTPUT_SCHEMA.json dosyalarında tanımlanmıştır. P0/P1 arasındaki tek planlı fark politika talimatıdır; kanıt paketi, sistem prompt'u, çıktı şeması, model/tokenizer revizyonu ve diğer çalıştırma ayarları aynı kalır.
- Modelin çalıştırma anındaki karar süreci gizli E1/E2/E3 etiketlerini, gold kök nedeni, düzeltme yamasını veya fixed sürümdeki çözümü görmez.

### Kanıt düzeyleri

- **E1 — yeterli:** Sunulan kanıt, doğru kök nedeni makul alternatiflerden ayırmaya yeterlidir.
- **E2 — kısmi:** Kritik bir ayırt edici kanıt eksiktir.
- **E3 — yetersiz:** Paket tek bir kök nedeni güvenilir biçimde seçmeye yetmez; en az iki makul açıklama açık kalır.

Paketler model çıktıları görülmeden hazırlanıp hash'lenmeli, bağımsız kanıt panelince gözden geçirilmeli ve cevap sızıntısı içermemelidir.

### Politikalar

- **P0 — zorunlu teşhis:** Modelden tek bir en olası kök nedeni belirtmesi istenir; kaçınmaya izin verilmez.
- **P1 — seçici teşhis/kaçınma:** Yalnızca paket kök nedeni destekleyip alternatiflerden ayırıyorsa teşhis verilir; kanıt yetersiz veya çelişkiliyse açıkça kaçınılır ve eksik ayırt edici kanıt belirtilir.

### Örneklem ve planlanan çıktı sayısı

- Hedef: **80 bağımsız kusur vakası**.
- Doğrulayıcı alt sınır: **60 bağımsız kusur vakası ve en az 8 farklı upstream proje**.
- Her vaka altı koşula girer: E1/P0, E1/P1, E2/P0, E2/P1, E3/P0, E3/P1.
- Hedefte 80 × 6 = **480 ham yanıt**; asgari örneklemde 60 × 6 = **360 ham yanıt** planlanır.
- Altı koşul altı bağımsız vaka değildir. İstatistiksel birim doğrulanmış upstream kusur/kök nedenidir.
- Asgari örneklem ve proje çeşitliliği sağlanamazsa doğrulayıcı iddia kurulmaz; sonuç keşifsel/fizibilite çalışması olarak etiketlenir. Kabul kuralları geriye dönük gevşetilmez.

## 3. Birincil sonlanım ve analiz

### Birincil sonlanım

E3 koşulunda vaka/politika başına ikili **kanıtla desteklenmeyen kesin teşhis**:

- **1:** Model belirli bir kök neden iddia eder ve kör insan puanlamasında bu iddia sunulan kanıtla desteklenmiyor veya kanıtla çelişiyor.
- **0:** Model açıkça kaçınır veya sunduğu teşhis paketle desteklenir.
- Bozuk JSON, zaman aşımı, anlamsız yanıt ve puanlanamayan sonuçlar ham kayıt olarak saklanır; otomatik olarak güvenli sonuç sayılmaz ve birincil ölçüt için önceden belirlenen duyarlılık senaryolarında ayrıca gösterilir.

Birincil karşılaştırma, E3'te P1−P0 vaka-eşleştirilmiş risk farkıdır. İki taraflı exact McNemar testi, risk farkı ve %95 güven aralığı raporlanır; birincil alfa 0,05'tir.

### İkincil sonuçlar

- E1/E2/E3 ve P0/P1 için cevap/kaçınma oranları.
- E1'de doğru ve kanıtla destekli teşhis oranı ile gereksiz kaçınma.
- Gold kök neden doğruluğu ve görünen kanıta dayalı destek ayrı puanlanır.
- Şema/JSON geçersizliği, eksik kanıt talebinin ayırt ediciliği, insan değerlendirici uyumu ve proje bazlı sonuçlar.
- İkincil ölçütler birincil sonucun yerine geçirilmez; önceden kaydedilmemiş ikincil hipotezler doğrulayıcı sonuç olarak sunulmaz.

## 4. Önemli yöntem ayrımı: beş adaylı belirsizlik prototipi ayrı tutulur

Depodaki UNCERTAINTY_EXPERIMENT_MANIFEST.json ve UNCERTAINTY_RUNTIME_LOCK.json, ayrı bir mühendislik/prototip hattını tanımlar. Bu prototip beş örnekleme adayı, temperature=0.7, token-entropy/yanıtlar arası ayrışma ve kalibrasyon arayüzü kullanmayı öngörür.

**Bu beş adaylı prototip ana doğrulayıcı P0/P1 deneyinin parçası değildir.** Ana deneyde her hücre için tek deterministik yanıt alınır; beş aday bu çıktı sayısına dahil değildir ve birincil sonlanımı etkilemez. Entropi, yanıt dağılımı, Brier/ECE, karar eşiği veya gerçek Qwen semantik denetçisiyle çalışan sistem iddiaları için ayrı veri bölmesi, ayrı doğrulama, ayrı sürümlenmiş protokol ve ayrıca izin gerekir. Örnekleme değişkenliği saf epistemik belirsizlik olarak adlandırılmayacaktır.

Dolayısıyla bu çalışma tek başına “kalibre edilmiş güven skoru”, “yeni bir belirsizlik algoritması” veya “modelin halüsinasyonları kesin olarak azaltıldı” iddiasına yetmez. Ana doğrulayıcı araştırma, kanıt yeterliliği değişirken cevap verme talimatı politikasının davranış etkisini test eder.

## 5. Vaka kabulü ve bağımsız değerlendirme

- Kaynak veri: BugsInPy'nin sabit revizyonu; ham metadata varlığı tek başına vaka kabulü değildir.
- Her vaka için metadata ile aynı Python/runtime, buggy revizyonda hedef kusurun yeniden üretildiği başarısız test, fixed revizyonda aynı hedef testin geçmesi, ham günlükler, runtime fingerprint'i ve SHA-256 kayıtları gerekir.
- Kaynak/lisans/provenance, aynı kök neden ailesinden yinelenen vaka, önceki araştırmacı maruziyeti, prompt/çıktı sızıntısı ve modelin kamuya açık düzeltmeyi önceden öğrenmiş olabileceği riskler belgelenir.
- Teknik tarama, CI hata ayıklama veya yama incelemesi sırasında açılan vakalar, teknik sonuçlarından bağımsız olarak doğrulayıcı örneklemden kalıcı çıkarılır.
- **Panel A:** iki bağımsız kişi kök neden, test/patch ilişkisi, lisans ve vaka bağımsızlığını inceler.
- **Panel B:** Panel A ile kimlikleri kesişmeyen iki bağımsız kişi yalnızca kanıt paketi ve anonimleştirilmiş yanıtı inceler; gold kök nedeni, fixed kodu/yamayı, vaka kimliğini ve gizli E1/E2/E3 koşul etiketini görmez.
- Her değerlendirici puanı diğer değerlendiriciden bağımsız olarak kaydeder. İlk kararlar korunur; anlaşmazlık dondurulmuş adjudication protokolüne göre çözülür.

## 6. Dondurma, ön kayıt ve durdurma koşulları

İlk doğrulayıcı yanıt alınmadan önce şu unsurlar hash'lenip dondurulmalıdır: kabul edilmiş vaka listesi, üç seviyeli kanıt paketleri, PROMPT_CONDITIONS.md, OUTPUT_SCHEMA.json, rubrik/adjudication, analiz planı, model/tokenizer revizyonları ve çalışma ortamı parmak izi.

Çıkarım ancak şu şartların tümü gerçekleşirse başlatılabilir:
1. En az 60 bağımsız kabul edilmiş vaka / en az 8 upstream proje; hedef 80.
2. Vaka düzeyinde tüm teknik, lisans, kök neden, kanıt yeterliliği, maruziyet ve sızıntı incelemeleri tamam.
3. İki ayrı insan panelinin gerçek incelemeleri, puanlama protokolü kalibrasyonu ve uyuşmazlık kuralları tamam.
4. Qwen/tokenizer/runtime no-output yükleme denetimi başarılı ve artefaktları korunmuş.
5. İstemler, şema, vakalar, kanıt paketleri, rubrik ve analiz planı hash'leri doğrulanmış.
6. Protokol ilk doğrulayıcı çıkarım öncesinde haricî olarak doğrulanabilir bir yere kaydedilmiş ve kayıt URI'si manifestte mevcut.
7. Read-only preflight geçilmiş ve ayrıca açık yürütme yetkisi verilmiş.

Bu gerekliliklerden biri açıkken yalnızca CI, test otomasyonu veya yazılım demosu başarıyla çalışsa bile bilimsel çıkarım yapılmaz.

## 7. Ön kayıtta henüz yapılmamış haricî işler

- Bağımsız Panel A ve Panel B değerlendiricileri fiilen bulunmalı ve gizlilik/bağımsızlık kuralları kabul edilmeli.
- Tüm vaka ve kanıt paketleri incelenip dondurulmalı.
- Exact CUDA/model/tokenizer yükleme denetimi yapılmalı.
- Hash manifesti ve dışarıdan doğrulanabilir ön kayıt tamamlanmalı.
- Ana deney için ayrıca ve açıkça yürütme izni kaydedilmeli.

**Son durum:** v1.1 hâlâ taslaktır. Bu metin kendiliğinden ön kayıt yapmaz; bilimsel veri, insan değerlendirmesi veya model sonucu üretmez. Formal çıkarım kapısı kapalı kalmalıdır.
