# TÜBİTAK 2204-A tek odaklı yürütme planı

**Tarih:** 21 Ekim 2026  
**Tek hedef:** 2027 TÜBİTAK 2204-A yarışmasında finalistlik düzeyinde, tamamlanmış ve kanıtla savunulabilir bir araştırma sunmak.  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Bilimsel rapor başlığı (öneri):** Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi  
**Durum:** DEVAM EDİYOR — yeni çalışma için henüz deneysel sonuç yoktur.

## Üç ana aşamalı karar haritası

Ayrıntılı tarih/sorumluluk görünümü için [üç ana aşamalı yürütme haritasına](THREE_PHASE_EXECUTION_MAP_2026-10-21.md) bak. Proje üç ana teslimata ayrılır: (1) veri/protokol/runtime kapılarını kapat, (2) yalnızca izin sonrası dondurulmuş deneyi yürüt, (3) kör puanlama/istatistik/rapor/başvuruyu tamamla. Şu an 1. aşamadayız ve henüz tamamlanmadı.

## 1. Başarı ölçütümüz

Amaç sadece bir dosya veya çalışan demo üretmek değildir. Başvuruya, jüri sorularına dayanabilecek araştırma sorusu, adil karşılaştırma, bağımsız vaka kanıtı, önceden tanımlanmış analiz, gerçek sonuçlar, tekrarlanabilirlik ve dürüst sınırlılıklar içeren tamamlanmış bir çalışma sunmaktır.

Finalistlik hedefimiz nettir; ancak hiçbir dosya, model veya plan finalistliği garanti etmez. Sonucu belirleyecek şeyi kontrol edebiliriz: bilimsel doğruluk, metodolojik tutarlılık, uygulama ve anlatım kalitesi.

## 2. Resmî takvim ve kritik sınır

TÜBİTAK’ın [2026–2027 2204-A çağrı sayfasında](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi) başvuru dönemi 23 Eylül 2026–4 Ocak 2027 olarak duyurulmuştur; başvuru sistemi 4 Ocak 2027 saat 17.30’da kapanır. Aynı sayfada, fikir aşamasındaki veya devam etmekte olan projelerle başvuru yapılamayacağı açıkça belirtilir.

İç kontrol hedefi 4 Kasım 2026’dır. Bu tarih bilimsel kabul eşiklerini gevşetme gerekçesi olamaz. Kasım başında veri kapısı sağlanamıyorsa gerçek durum kaydedilir, kaynak stratejisi/iş yükü değerlendirilir ve karar gerekçesi belgelenir; yalnızca başvuru yetişsin diye düşük kaliteli vakalar kabul edilmez.

## 3. Araştırma sorusu ve hipotez

**Birincil soru:** Kanıtı yetersiz yazılım hatası vakalarında seçici cevap vermeme politikasına izin vermek, teşhis vermeyi zorunlu kılan politikaya göre kanıtla desteklenmeyen kesin teşhis oranını düşürür mü?

**Birincil hipotez:** E3 (yetersiz kanıt) koşulunda P1 seçici teşhis/kaçınma politikası, P0 zorunlu teşhis politikasına göre unsupported definitive diagnosis oranını azaltır.

- E1: bağımsız incelemecilerin kök nedeni alternatiflerinden ayırmaya yeterli bulduğu kanıt.
- E2: önceden tanımlanmış ayırt edici kanıtın bir kısmının eksik olduğu kanıt.
- E3: birden fazla makul açıklamanın hâlâ mümkün olduğu yetersiz kanıt.
- P0: zorunlu teşhis.
- P1: kanıt destekliyorsa teşhis; desteklemiyorsa açıkça kaçınma ve eksik ayırt edici kanıtı belirtme.

Modelin tesadüfen doğru tahmin etmesi, tahminin elindeki kanıtlarla desteklendiğini tek başına kanıtlamaz. Bu iki ölçüm birbirinden ayrılacaktır.

### 3.1 Yakın literatür ve katkı sınırı

Bu alanda doğrudan önceki çalışmalar vardır: [ICSE-NIER 2026 “When to Answer and When to Defer”](https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-When-to-Defer-A-Decision-Framework-for-Reliable-Code-Predictions) kod modellerinde belirsizlik/kalibrasyon/abstention çerçevesini; [Zhang & Wu (2026)](https://www.techscience.com/cmc/v89n1/68467) RAG için kanıt yeterliliği seviyeleri altında answer-abstention davranışını ele alır. Bu nedenle genel abstention davranışı veya kanıt seviyesine göre cevap oranı değişimi özgün iddia olamaz. Çalışmanın **aday** ayrımı, gerçek kusur kök neden vakalarında aynı kanıt gradyanı üzerinde doğru kök neden ile görülen kanıtın desteklediği teşhisi ayrı puanlamak ve E3'te kanıtsız kesin teşhisi, E1'de gereksiz kaçınmayla birlikte ölçmektir. Bunun özgünlüğü kanıtlanmış değildir; [hedefli literatür karşılaştırması](LITERATURE_REVIEW.md) bunu açıkça kaydeder ve sistematik tarama yerine geçmez.

## 4. Mevcut kanıt ve açık kapılar

21 Ekim 2026 itibarıyla sabitlenmiş BugsInPy metadata envanterinde 17 projede 501 kayıt vardır; 500 kayıt temel metadata kapısını geçmiş, bir kayıtta buggy ve fixed commit aynı görünmüştür. Bu envanter testleri çalıştırmamış, kök nedenleri insan tarafından doğrulamamış ve kanıt paketlerini değerlendirmemiştir.

- Doğrulanmış buggy-fail/fixed-pass test çifti: **0**
- Kabul edilmiş bağımsız doğrulayıcı vaka: **0**
- Kabul edilmiş upstream proje: **0**
- Yeni çalışma için model çıkarımı: **yapılmadı**
- Model/runtime adayı: resmi, kuantize edilmemiş Qwen2.5-3B-Instruct; exact runtime yükleme doğrulaması henüz yok.
- Son fail-closed preflight run: [39619057132](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39619057132). CI işi başarılı tamamlanmış, ancak deney hazır olma kararı **ready=false** kalmıştır.

Bu, modelin kötü performans gösterdiği anlamına gelmez; yeni deney henüz yürütülmemiştir.

## 5. Vaka kabul kapısı

Her aday için [Manuel vaka inceleme rehberi](CASE_REVIEW_GUIDE.md) ve [boş JSON formu](CASE_REVIEW_INTAKE_TEMPLATE.json) kullanılacaktır. Bu formun doldurulması yalnızca kaynak/karar kayıtlarını düzenler; reviewer kararı ve gerçek artefaktlar olmadan bir vakayı kabul etmez.

Her vaka, model çıktısı üretilmeden önce şu koşulların hepsini geçmelidir:

1. Sabitlenmiş kaynak/metadata revizyonu, upstream repository ve izin/lisans bilgisi kayıtlı.
2. Buggy ve fixed revizyonlar farklı ve test komutu belirli.
3. Kayıtlı hedef test, uygun runtime altında buggy sürümde hedeflenen nedenle başarısız, fixed sürümde başarılı.
4. İki ayrı test günlüğü ve test ortamının fingerprint'i korunmuş ve SHA-256 ile kaydedilmiş.
5. Kök neden, kod/test/düzeltme kanıtlarıyla en az iki bağımsız inceleyici tarafından onaylanmış.
6. E1/E2/E3 paketleri, birden fazla makul alternatif ve paket başına hash, model çıktıları görülmeden hazırlanmış/onaylanmış.
7. Lisans, cevap sızıntısı, eğitim verisi kontaminasyonu riski ve önceki inceleme maruziyeti değerlendirilmiş.
8. Aynı hata ailesi, upstream PR veya kök neden kopyaları bağımsız örnek gibi sayılmamış.

Daha önce açılan fizibilite/smoke vakaları ana doğrulayıcı kümeden kalıcı olarak dışlanır. Metadata varlığı bir vakayı otomatik kabul ettirmez.

## 6. Örneklem ve önceden belirlenmiş analiz

- Hedef: **80 bağımsız vaka**.
- Doğrulayıcı alt sınır: **60 vaka ve 8 farklı upstream proje**.
- Her vaka için E1/E2/E3 × P0/P1 düzeninde altı çıktı: N=80 ise 480; N=60 ise 360 planlanan çıktı.
- Birincil birim vaka; koşullar/çıktılar bağımsız vaka sayılmaz.
- Birincil karşılaştırma: E3 altında vaka başına P0 ve P1 unsupported definitive diagnosis sonucu; iki taraflı exact McNemar testi, P1−P0 risk farkı ve %95 güven aralığı.
- İkincil sonuçlar (kök neden doğruluğu, kanıt desteği, cevap kapsamı, E1 gereksiz kaçınma, eksik kanıt isteğinin uygunluğu) birincil sonuca karıştırılmaz.
- Geçersiz JSON otomatik düzeltilmez ve yanıtlar tekrar üretilerek seçilmez; ham çıktı ve tüm hata kayıtları korunur.
- Sonuç görüldükten sonra hipotez, vaka dışlama kuralı veya birincil ölçüt değiştirilmeyecektir.

N=60 / 8 proje şartı sağlanmazsa çalışma bu protokol altında doğrulayıcı sonuç olarak sunulmaz. Örneklem eşiği geriye dönük gevşetilmez.

## 7. Jüri ölçütlerine göre kalite güvencesi

[TÜBİTAK jüri ölçütleri kontrol listesi](TUBITAK_2204A_JURY_CRITERIA_CHECKLIST_2026-10-21.md) ayrı bir kapı olarak kullanılacaktır. Resmî sayfanın bağladığı ön değerlendirme formunda problem/araştırma sorusu ve yöntem %20'şer; yaratıcılık/etki ve sonuçlar/tartışma %30'ar ağırlıktadır. Bu, kanıtlanmış bir puan veya finalistlik olasılığı değildir. Bugünkü en büyük eksik, %30 ağırlıklı sonuçlar/tartışma kısmı için gerçek deney sonuçlarının henüz bulunmamasıdır.

## 8. Teknik ve insan değerlendirme kapıları

Model çıkarımından önce şu işler kapanmalıdır:

- [ ] Model kartı ve lisans incelemesi.
- [ ] Exact model ve tokenizer revision yükleme deneyi; chat template ve tokenizer fingerprint'i.
- [ ] Python, kütüphane, donanım, CUDA ve precision/runtime fingerprint'i.
- [ ] Prompt koşulları, çıktı şeması, analiz planı, rubrik, runtime ve kabul edilmiş vaka listesi için doğrulanmış SHA-256 freeze kaydı.
- [ ] İki değerlendiricinin rubriği bağımsız incelemesi ve kalibrasyonu; kalibrasyonda kullanılan vakalar ana örneklemden ayrı.
- [ ] Protokol ve birincil ölçütün çıktı alınmadan önce denetlenebilir biçimde ön kaydı.
- [ ] Veri ve model kapıları tamamlandıktan sonra ayrı, açık deney yürütme izni.

Hazır olma betiği read-only'dir. CI'nın yeşil olması, `ready=true` anlamına gelmez ve tek başına çıkarım izni vermez.

## 9. İş takvimi — karar kapılarıyla

### 21 Ekim–4 Kasım: veri fizibilitesini gerçek vakaya dönüştürme

- Maruz kalınmamış aday kuyruğunu belirle ve upstream proje dağılımını incele.
- Her adayda exact ortam ve hedef testin iki revizyonda davranışını dene.
- Lisans, gold truth, kanıt seviyeleri ve sızıntı kontrollerini kayıt altına al.
- 4 Kasım kontrolünde kabul edilen vaka/project sayısını raporla. Hedef sağlanmadıysa bunu açıkça belirt ve kalan süre için kaynak/uygulanabilirlik kararı ver; kapıları gevşetme.

### 5–15 Kasım: tasarımı kilitleme

- Yakın literatürle farkı ve sınırlı özgünlük iddiasını netleştir.
- İki değerlendirici protokolü ve kalibrasyonunu tamamla.
- Ön kaydı, prompt/şema/analiz hash'lerini ve runtime doğrulamasını dondur.
- Yalnızca tüm engeller kapanırsa inference izni için inceleme yap.

### 16 Kasım–10 Aralık: deney ve kör puanlama

- Altı koşullu planı değiştirmeden çalıştır.
- Ham çıktıları değişmez sakla; tekrarlı deneme ve otomatik yanıt düzeltme yapma.
- Cevapları koşulları mümkün olduğunca gizlenmiş şekilde iki bağımsız puanlayıcıya ver; uyuşmazlıkları kayıtlı adjudication ile çöz.
- Gerçek gözlem sayıları, eksik çıktılar ve dışlamaları kaydet.

### 11–22 Aralık: analiz ve bilimsel denetim

- Önceden belirlenmiş birincil istatistiği ve güven aralığını çalıştır.
- İkincil sonuçları birincil hipotez yerine geçirmeden raporla.
- Ölçüm, kontaminasyon, veri/ortam sınırlılıklarını, değerlendiriciler arası uyumu ve tekrarlanabilirlik kanıtlarını yaz.
- Olumsuz veya sonuçsuz bulguları değiştirmeden koru.

### 23 Aralık–2 Ocak: başvuruya hazır son paket

- TÜBİTAK’ın güncel resmî rapor şablonuna göre raporu tamamla.
- Kaynaklar, yöntem, gerçek sonuçlar, grafik/tablo, sınırlılıklar ve kaynak/izin kayıtlarını denetle.
- Kod/veri manifesti ve ekler üzerinden bağımsız tekrar kontrolü yap.
- Danışman/jüri provasıyla çalışmayı sonuç, yöntem ve sınırlılık sorularına karşı test et.

### 3–4 Ocak: başvuru güvenliği

Başvuru formu ve tüm yüklemeler önceden doğrulanır. Son tarih **4 Ocak 2027 17.30** olduğundan, son dakikada dosya yazımı veya deney çalıştırılması planlanmaz.

Bu takvim agresif bir iç plandır; kapıların geçtiğine dair kanıt değildir.

## 10. Başvuruya hazır sayılma kapısı

Çalışma, aşağıdakiler olmadan “tamamlandı” kabul edilmeyecektir:

- [ ] Özgünlük iddiası yakın çalışmalar karşısında dürüstçe sınırlandırıldı.
- [ ] Deney örneklemi ve tüm kabul/dışlama gerekçeleri doğrulanabilir.
- [ ] Analiz planı ve protokol sonuçlardan önce donduruldu.
- [ ] Model/runtime ve çıktı üretiminin kayıtları var.
- [ ] İki bağımsız puanlayıcı ve adjudication kayıtları var.
- [ ] Birincil sonuç, güven aralığı ve sınırlılıklar gerçek veriden üretildi.
- [ ] TÜBİTAK rapor formatı ve başvuru gereklilikleri karşılandı.
- [ ] Bağımsız teknik/bilimsel denetim ve sözlü savunma provası yapıldı.

Herhangi bir kapının başarısız olması saklanmayacak. Gerektiğinde “sonuçsuz/fizibilite” demek, doğrulayıcı başarı iddia etmekten daha doğrudur.

## 11. Kapsam kuralı

Bu tarihten itibaren çalışma önceliği yalnızca bu TÜBİTAK 2204-A projesidir. CERN, IYPT, NASA ve başka proje/yarışma yolları bu çalışma için yürütme gündemine alınmaz. Önceki DİJİTALİKİZ deney kayıtları tarihsel olarak korunur ve bu çalışmanın yeni verisi/sonucu gibi kullanılamaz.

## 12. Ana dosyalar

- Araştırma durumu ve dizin: [README.md](README.md)
- Jüri ölçütleri kontrol listesi: [TUBITAK_2204A_JURY_CRITERIA_CHECKLIST_2026-10-21.md](TUBITAK_2204A_JURY_CRITERIA_CHECKLIST_2026-10-21.md)
- Literatür: [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md)
- Veri fizibilitesi: [DATA_FEASIBILITY.md](DATA_FEASIBILITY.md)
- Deney tasarımı: [STAGE3_EXPERIMENT_DESIGN.md](STAGE3_EXPERIMENT_DESIGN.md)
- Analiz planı: [ANALYSIS_PLAN_STAGE3.md](ANALYSIS_PLAN_STAGE3.md)
- Prompt koşulları: [PROMPT_CONDITIONS.md](PROMPT_CONDITIONS.md)
- Vaka sicili: [CASE_REGISTRY.json](CASE_REGISTRY.json)
- Teknik readiness: [STAGE4_TECHNICAL_READINESS_2026-10-21.md](STAGE4_TECHNICAL_READINESS_2026-10-21.md)
- TÜBİTAK resmî sayfası: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
