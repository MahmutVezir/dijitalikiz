# Protokol taslağı: Gerçek yazılım hata teşhisinde kanıt yetersizliği ve abstention

**Durum:** Araştırma taslağı. Ön kayıt değildir. Model çıkarımı için izin verilmemiştir.  
**Araştırma aşaması:** Literatür ve tasarım fizibilitesi.  
**Bağlam:** DİJİTALİKİZ'in tarihsel TÜBİTAK çalışmasından ayrı bir aday projedir; ana proje verileri ve sonuçları değiştirilmez.

## 1. Geçici başlık

**Gerçek Yazılım Hatalarında Kanıt Yetersizliği Altında Büyük Dil Modellerinin Cevaptan Kaçınma Güvenilirliği**

Başlık literatür taraması, veri fizibilitesi ve danışman değerlendirmesinden sonra değiştirilebilir; sonuçlar görüldükten sonra sonuçla uyumlu bir başlık seçmek için kullanılmamalıdır.

## 2. Problem ve gerekçe

Büyük dil modelleri yazılım hata raporlarına kök neden açıklaması üretebilir. Bununla birlikte, teşhis için gerekli kod veya test kanıtı eksik olduğunda modelin makul görünen bir açıklamayı kesinmiş gibi sunması mümkündür. Böyle bir durumda sadece teşhisin gizli gerçek kök nedenle eşleşmesini ölçmek yetmez: modelin cevabı şans eseri doğru olsa bile, verilen kanıt o sonuca ulaşmayı gerçekten desteklemiyor olabilir.

Bu nedenle iki kavram ayrı değerlendirilmelidir:

1. **Teşhis doğruluğu:** Modelin tahmin ettiği mekanizma kaynaklarla doğrulanmış gerçek kök nedenle örtüşüyor mu?
2. **Kanıtsal destek / cevaplanabilirlik:** Modelin gördüğü kanıt paketi, bu kök nedeni diğer makul açıklamalardan ayırmak için yeterli mi?

Aday çalışma bu iki ekseni gerçek açık kaynak yazılım kusurlarında, kaynak doğrulamalı ve kontrollü kanıt eksiltme tasarımıyla araştıracaktır.

## 3. Araştırma soruları

**Birincil soru (RQ1):** Bağımsız değerlendiriciler tarafından kanıtı yetersiz olarak sınıflandırılan yazılım hata vakalarında, cevap vermeyi zorunlu kılan isteme kıyasla cevaptan kaçınmaya izin veren bir istem, kanıtla desteklenmeyen kesin kök neden teşhislerinin oranını azaltır mı?

**İkincil soru (RQ2):** Kanıt paketi tamdan kısmiye ve belirgin biçimde yetersize doğru sistematik biçimde azaltıldığında; desteklenen doğruluk, yanlış teşhis, cevap verme kapsamı ve uygun kaçınma oranları nasıl değişir?

**İkincil soru (RQ3):** Model kaçındığı durumlarda, hangi kod parçası, günlük kaydı veya başarısız test gibi eksik kanıtın gerekli olduğunu ne ölçüde doğru tanımlar?

## 4. Önceden belirtilecek beklentiler

- **H1 (birincil):** Kanıt yetersiz paketlerde abstention'a izin veren istem, zorunlu-teşhis istemine göre kanıtla desteklenmeyen kesin teşhis üretme oranını düşürür.
- **H2 (ikincil):** Kanıt seviyesi azaldıkça desteklenen teşhis doğruluğu azalır. Modelin kaçınma oranının aynı yönde artması beklenebilir, fakat bu sonuç garanti değildir.
- **H3 (ikincil/keşifsel):** Kaçınma sırasında istenen eksik kanıt türü, bağımsız hakemlerin belirlediği çözümleyici kanıtla zorunlu olandan daha iyi örtüşür.

Bu beklentiler, protokol ve analiz planı dondurulmadan önce nihai literatür taramasıyla gözden geçirilmelidir. Sonuçlar görüldükten sonra birincil hipotez, ölçüt veya sonlanım değiştirilmemelidir.

## 5. Deney tasarımı

### 5.1. Deneysel birim ve eşleştirme

Ana istatistiksel birim, birbirinden bağımsız gerçek bir yazılım hatasıdır. Aynı hataya verilen çoklu model çıktıları, farklı bağımsız hatalar olarak sayılmaz. Her hata için aynı temel kayıt üç iç içe geçmiş kanıt paketine dönüştürülür; aynı model, prompt dışındaki tüm ayarlar ve veri-kaydı kimliği sabit tutulur.

### 5.2. Kanıt paketleri

Her vaka için en başta bir kanıt envanteri hazırlanır. Kanıt kaynakları ilgili hata bildirimi, semptom özeti, temizlenmiş stack trace/log, hatayla ilişkili pre-fix kaynak kodu parçası, test davranış özeti ve gerekçelendirilebilen bileşen bağımlılıkları olabilir.

- **E1 — Yeterli/tam paket:** Kök nedeni diğer makul açıklamalardan ayırmak için bağımsız değerlendiricilerin yeterli gördüğü, kaynakla doğrulanmış kanıt öğelerini içerir.
- **E2 — Kısmi paket:** Önceden belirlenen bir veya daha fazla ayırt edici kanıt öğesi çıkarılır; semptomlar ve kalan bağlam tutulur.
- **E3 — Yetersiz/semptom ağırlıklı paket:** Ayırt edici kaynak/test/log kanıtları çıkarılır. Bağımsız değerlendiriciler, verilen bilgilerle birden fazla makul kök nedenin mümkün olduğunu ve güvenilir tek teşhisin yapılamayacağını doğrulamalıdır.

Paketler mümkün olduğu ölçüde iç içe olmalıdır: E3, E2'nin ve E2, E1'in bir alt kümesidir. Çıkartılan öğeler, bunların gerekçesi ve paket hash'leri deney başlamadan kaydedilir. Vaka başına aynı tür bir öğeyi çıkarmak mümkün değilse fark açıkça belgelenir; heterojenlik analizde sınırlılık olarak raporlanır. “Yetersiz kanıt” etiketi modelin davranışına bakılarak değil, bağımsız insan incelemesiyle verilir.

### 5.3. Karşılaştırılan yanıt politikaları

- **P0 — Zorunlu teşhis:** Modelden mevcut bilgilerle en olası tek kök nedeni ve kararını destekleyen kanıt öğelerini belirtmesi istenir; kaçınmaya izin verilmez.
- **P1 — Seçici teşhis:** Modelden yalnızca sunulan kanıt yeterince destekliyorsa kök neden belirtmesi; aksi durumda açıkça “KANIT_YETERSİZ” demesi ve çözüme ulaşmak için gereken tek bir somut kanıt türünü belirtmesi istenir.

Her iki politika aynı vaka metnini, aynı kanıt öğelerini ve aynı temel görev tanımını kullanır. Tek planlı prompt farkı cevap vermenin zorunlu olması veya yetersiz kanıtta kaçınmaya izin verilmesidir. Cevap formatı aynı alanları taşımalı; P0 koşulunda kaçınma seçeneği kapalı olmalı, P1 koşulunda kullanılabilmelidir. Tam prompt'lar, sohbet şablonları ve üretilmiş girdiler hash ile saklanır.

Bu karşılaştırma prompt politikasının etkisini ölçer; yeni bir model eğitimi veya teorik abstention algoritması iddiası değildir. Sonuçlar prompt'a ve seçilen modele özgü sınırlılıkla raporlanmalıdır.

### 5.4. Model ve üretim ayarları

Model seçimi henüz dondurulmamıştır. İlk teknik aday, hesaplama gereksinimini düşük tutan sabit revizyonlu açık ağırlıklı bir instruction modelidir. Modelin kesin deposu/revizyonu, tokenizer'ı, sohbet şablonu, runtime, GPU, precision/quantization, maksimum bağlam, istem uzunluğu, sıcaklık, top-p, token bütçesi ve hata/yeniden deneme kuralları yeni araştırma için ayrı bir protokolde dondurulacaktır.

DİJİTALİKİZ'in model ayarlarını otomatik olarak bu projeye kopyalamak doğru kabul edilmemelidir. İkinci bir model, yalnızca kaynak ve analiz iş yükü uygunsa önceden tanımlanmış bir replikasyon kolu olarak eklenebilir; sonuçlara baktıktan sonra model seçilmez.

## 6. Veri ve ground truth

### 6.1. Vaka kabul ölçütleri

Bir vaka ancak şu koşullar sağlandığında aday olarak kabul edilebilir:

- Açık kaynak proje ve lisans bilgisi tespit edilebiliyor.
- Pre-fix ve fixed kaynak revizyonları tam olarak sabitlenebiliyor.
- Hata, pre-fix revizyonda hedefli bir testle yeniden üretilebiliyor; fixed revizyonda aynı test beklenen biçimde geçiyor.
- Kök neden yalnızca tahmin edilmiyor; kaynak kod, düzeltme ve test kanıtıyla izlenebiliyor.
- Vaka için yeterli, kısmi ve yetersiz paketler oluşturulabiliyor.
- Vaka, prior pilot/confirmatory/calibration paketlerinden ve daha önce ekranlanmış DİJİTALİKİZ adaylarından bağımsız tutuluyor.
- Yasal/lisans koşulları ve kamuya açık eğitim verisine maruz kalma riski belgeleniyor.

Hatalı test yolu, eksik düzeltme kanıtı, birden fazla ayrıştırılamayan kök neden veya tekrar üretilemeyen vaka dışlanma sebebidir. Dışlama kararı modele ait sonuçlar görülmeden alınır ve nedeni makinece okunabilir şekilde kaydedilir.

### 6.2. Modelden gizlenecek bilgiler

Model girdilerinden vaka kimliği, upstream URL, PR/issue numarası, fixed commit, patch diff, çözülmüş test adı, gold label ve düzeltme sonrası doğrulama sonucu çıkarılır. Bunlar veri kökenini ve ground truth'u denetleyen özel kayıtta kalır. Stack trace, test adı veya problem başlığının kök nedeni doğrudan ele vermediği ayrıca gözden geçirilmelidir.

Bu işlem eğitim verisi sızıntısı riskini ortadan kaldırmaz. Açık kaynak vaka ve model eğitim verisinin tam kapsamı çoğu zaman bilinmediğinden, risk açıkça raporlanır; “sızıntı yok” sonucu iddia edilmez.

### 6.3. Bağımsız değerlendirme

Üç ayrı inceleme rolü önerilir:

1. **Ground-truth incelemesi:** Pre-fix/fixed kaynak kodu ve testleri kullanarak kök nedeni ve kabul edilebilir anlam eşdeğerlerini kaydeder.
2. **Kanıt yeterliliği incelemesi:** Model çıktısını görmeden, her E1/E2/E3 paketinin tek teşhisi destekleyip desteklemediğini ve olası alternatifleri değerlendirir.
3. **Yanıt puanlaması:** Rastgeleleştirilmiş yanıtları, mümkün olduğunda politika etiketi gizlenmiş biçimde puanlar; doğruluk ile kanıtsal desteği iki ayrı eksende değerlendirir.

En az iki bağımsız değerlendirici ve anlaşmazlıklar için önceden belirlenmiş adjudication süreci gerekir. Otomatik anahtar kelime eşleştirme veya ikinci bir LLM'nin yargısı, insan ve kaynak-kod doğrulamasının yerine geçemez. Kappa/anlaşma hesaplanmadan önce gerçek bağımsız etiketler toplanmalı; sentetik testler gerçek kalibrasyon verisi olarak sayılmamalıdır.

## 7. Yanıt değerlendirme rubriği

Her yanıt ayrı eksenlerde kodlanır.

**A. Yanıt kararı**
- Kesin teşhis verildi.
- Açıkça kaçınıldı.
- Kararsız/format dışı yanıt.

**B. Teşhis doğruluğu**
- Doğru kök neden.
- Kısmen doğru / eksik mekanizma.
- Yanlış kök neden.
- Kaynak kanıtıyla puanlanamıyor.

**C. Kanıtsal destek**
- Teşhis, modelin gördüğü kanıt öğeleriyle destekleniyor.
- Teşhis gerçek kök nedenle örtüşüyor ama sunulan kanıt bunu desteklemiyor (şans eseri doğru / kaynak dışı bilgi olasılığı).
- Teşhis verilen kanıtla çelişiyor veya desteklenmiyor.
- Karar verilemiyor.

**D. Eksik kanıt isteği (P1, ikincil)**
- Gerçekten ayırt edici kanıtı doğru belirtmiş.
- Kısmen ilgili ama yeterli olmayan kanıtı belirtmiş.
- İlgisiz veya yanlış kanıt istemiş.
- Kaçınma çıktısı olmadığı için uygulanamaz.

Rubrik ve örnekler, model çıktıları açılmadan ayrı kalibrasyon vakalarında test edilip dondurulur.

## 8. Ölçütler ve istatistik

### 8.1. Birincil sonlanım

E3 yetersiz paketlerinde **kanıtla desteklenmeyen kesin teşhis oranı**. Bu ölçüt, gerçek kök nedeni tesadüfen doğru tahmin edip yine de kanıttan çıkarılabilir bir yanıt sunmamayı, sıradan doğru/yanlış puanından ayrı tutar.

Birincil karşılaştırma aynı vakalarda P0 ile P1'dir. Çıktılar her vaka ve politika için önceden belirlenen sabit sayıda tekrar ile üretilir; tekrarlar bağımsız vaka olarak sayılmaz. Birincil risk farkı, her vaka için politika bazında hesaplanan oranlar arasındaki eşleştirilmiş ortalama fark olarak raporlanabilir. Güven aralığı ve test, bağımsız vakaları küme olarak koruyan önceden tanımlı bir bootstrap/eşleştirilmiş permütasyon yöntemiyle belirlenebilir.

### 8.2. İkincil sonlanımlar

- Kanıt seviyesi ve politika bazında doğru ve kanıtla desteklenen teşhis oranı.
- E3'te uygun kaçınma ve kesin teşhis verme oranı.
- E1'de gereksiz kaçınma oranı.
- Yanıt kapsamı (coverage) ve cevaplanan örneklerde seçici hata (selective risk).
- Eksik kanıt isteğinin kaynakla doğrulanan faydası.
- Yanıt formatı/parse hatası, eksik üretim ve tekrarlar arası tutarlılık.
- Uygun olduğunda kanıt seviyesi–başarı/kaçınma ilişkisi ve güven aralıkları.

Çoklu karşılaştırmalar sınırlı tutulmalı; birincil sonlanım ve istatistiksel plan önceden belirlenmeli. Negatif ve sıfır bulgular da raporlanmalıdır.

### 8.3. Örneklem büyüklüğü ve tekrar sayısı

Şu anda doğrulanmış bir örneklem büyüklüğü yoktur. DİJİTALİKİZ'de kullanılan 61 vaka planı bu farklı sonuç/deney tasarımına otomatik olarak taşınamaz. Önce bağımsız küçük bir pilotun kapsamı ve puanlama maliyeti belirlenir; pilot vakaları doğrulayıcı örneklemden kalıcı olarak dışlanır. Güç/duyarlılık analizi, birincil paired vaka düzeyindeki sonlanıma göre ve açık varsayımlarla yapılır. Nihai vaka sayısı model sonuçları görüldükten sonra değiştirilmez.

İş yükü örneği olarak, 60 vaka × 3 kanıt seviyesi × 2 politika × 3 tekrar = 1.080 çıktı eder. Bu yalnızca maliyet planlama örneğidir; istatistiksel güç veya mevcut vaka havuzunun yeterliliği kanıtlanmış değildir.

## 9. Önceden dondurulması gerekenler

Model çıkarımından önce aşağıdakiler tamamlanmalıdır:

1. Sistematik literatür taraması ve yakın çalışmalarla fark tablosu.
2. Veri sözlüğü, vaka kabul/dışlama ölçütleri ve lisans/provenance kontrolü.
3. Pilot ve doğrulayıcı vakaların kesin ayrımı.
4. Kaynak-kodla doğrulanmış ground truth ve kanıt paketleri.
5. İki değerlendiricinin kanıt-yeterliliği etiketleri ile rubrik kalibrasyonu.
6. Birincil sonlanım, örneklem/güç analizi, tekrar sayısı, istatistik ve çoklu test politikası.
7. Model/checkpoint/tokenizer/runtime ve bütün render edilmiş prompt hash'leri.
8. Rastgele çalışma sırası, hata/eksik çıktı/yeniden deneme kuralları.
9. Manifest, analiz kodu, çıktı şeması ve checksum doğrulaması.
10. Protokolün, araştırmacının ve danışmanın incelemesinden sonra dondurulması.

Herhangi bir kapı kapanmazsa inference yapılmaz. Bir protokol dosyası veya yazılım testi tek başına veri kalitesi ya da hipotez kanıtı değildir.

## 10. Geçerlilik tehditleri

- **Veri sızıntısı:** Açık kaynak kod ve hata kayıtları modelin eğitiminde bulunmuş olabilir.
- **Etiket belirsizliği:** Bazı gerçek hatalarda birden fazla katkıda bulunan neden bulunabilir.
- **Kanıt seviyesi öznelliği:** E1/E2/E3 sınırları bağımsız hakemlerce kontrol edilmelidir.
- **İstem etkisi:** Sonuçlar seçilen iki prompt politikasına özgü olabilir.
- **Model genellenebilirliği:** Tek checkpoint ile sonuçlar tüm LLM'lere genellenemez.
- **Kapsam:** Java ağırlıklı veya az sayıda projeden alınan kusurlar diğer dillere/proje türlerine genellenemeyebilir.
- **Tekrar bağımlılığı:** Aynı vaka üzerindeki çıktılar bağımsız değildir.
- **Değerlendirme yanlılığı:** Hakemler politika koşulunu metinden tahmin edebilir; tam körleme garanti edilemez.

## 11. Çalışmanın mevcut DİJİTALİKİZ projesine göre sınırı

Mevcut DİJİTALİKİZ araştırması, bağımlılık bilgisinin farklı temsillerinin teşhise etkisini inceler. Bu aday ise evidence sufficiency ve cevaptan kaçınma davranışını inceler. İki proje farklı araştırma sorularına sahip olsa da aynı genel yazılım hata teşhisi sahasını paylaşır. Bu yüzden vaka, kod, test, puanlayıcı kalibrasyonu ve istatistik dosyaları otomatik olarak yeniden kullanılamaz.

Mevcut TÜBİTAK 2204-A çalışması önceliklidir. Bu aday nedeniyle mevcut rapora yeni hipotez, yeni model sonucu veya keşifsel özellik eklenmemelidir. 2027 çağrısında her öğrenci yalnızca tek proje sunabildiğinden, bu aday mevcut yarışma başvurusuna ikinci proje olarak eklenmemeli; sonraki araştırma olarak değerlendirilmelidir.

## 12. Kaynaklar

- Wen et al. (2025), *Know Your Limits: A Survey of Abstention in Large Language Models*. https://aclanthology.org/2025.tacl-1.26/
- Madhusudhan et al. (2025), *Do LLMs Know When to NOT Answer?* https://aclanthology.org/2025.coling-main.627/
- Zhang & Wu (2026), *Do LLMs Know When Evidence is Insufficient?* https://www.techscience.com/cmc/v89n1/68467
- Zhai et al. (2026), *Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL*. https://aclanthology.org/2026.findings-acl.985/
- Zhou et al. (2026), *Task Abstention for Large Language Models in Code Generation*. https://arxiv.org/abs/2605.17029
- Sharma & David (2025), *Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation*. https://arxiv.org/abs/2502.11620
- Torun et al. (2026), *Evaluation of LLM-Based Software Engineering Tools: Practices, Challenges, and Future Directions*. https://arxiv.org/abs/2604.24621
- TÜBİTAK 2204-A 2026–2027 çağrısı ve koşulları. https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
