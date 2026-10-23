# TÜBİTAK 2204-A — Nihai Karar ve Tamamlama Planı

**Karar tarihi:** 23 Ekim 2026  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Önerilen bilimsel başlık:** Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi  
**Karar:** **Koşullu devam. Tek odak bu projedir; fakat şu an başvuruya hazır veya bilimsel olarak tamamlanmış değildir.** Bu belge durum ve karar kaydıdır; deney sonucu veya ön kayıt değildir.

## 1. Karar özeti

Araştırma sorusu ölçülebilir ve proje yönünü korumaya değer. Ancak şu anda elimizde tamamlanmış bir deney değil, araştırma tasarımıyla teknik hazırlık altyapısı vardır. Modelin belirsizlik altında daha güvenilir davrandığına, halüsinasyonlarının azaldığına veya önerilen yaklaşımın başarılı olduğuna dair doğrulanmış yeni bir sonuç yoktur.

**Yapılacak iş:** Yeni modeli veya istemleri rastgele denemek yerine, aynı yazılım hata vakalarında kanıt yeterliliğini sistematik biçimde değiştirerek “zorunlu teşhis” ile “kanıt yetersizse kaçınmaya izin veren politika”yı önceden belirlenmiş ölçütlerle karşılaştırmak. Önceki DİJİTALİKİZ/CCDG deneyinin çıktıları, veri kümesi ve istatistikleri bu yeni araştırmanın kanıtı olarak kullanılmayacaktır.

## 2. Erişilebilen güncel kanıtlara göre durum

| Bileşen | Durum | Yorum |
|---|---|---|
| Araştırma sorusu ve hedefli literatür taraması | Taslak hazır | Tarama sistematik derleme değildir; özgünlük kanıtlanmış değildir. |
| Veri kaynağı | BugsInPy sabit revizyonu seçildi | Envanterde 501 ham metadata kaydı / 17 upstream proje vardı; bu sayı doğrulanmış vaka sayısı değildir. |
| Güncel metadata tarama grubu | 100 aday / 13 upstream proje | Aday metadata'sı, deney verisi anlamına gelmez. |
| Kabul edilmiş bağımsız doğrulayıcı vaka | **0** | Vaka sicili bilerek boş. |
| Model/araç altyapısı | Kısmen hazır | Qwen adapter'ı ve fail-closed kapıları var; gerçek CUDA/model yükleme doğrulaması tamamlanmış sayılmıyor. |
| Yeni proje için model çıkarımı | **0** | Deney henüz yürütülmedi. |
| Kör insan puanlaması ve istatistik | Başlamadı | Gerçek model çıktısı ve bağımsız puanlayıcı kararları gerekir. |
| Başvuru raporu | Hazırlanabilir taslak altyapısı var | Gerçek sonuçlar olmadan tamamlanmış proje raporu olarak sunulamaz. |

V9 teknik tarama partilerindeki sonuç sinyalleri vaka kabulü değildir. V9 offset-0 ve offset-8 gruplarındaki adaylar, teknik tarama sırasında incelendikleri için ana doğrulayıcı örneklemden kalıcı olarak dışlanmıştır. Özellikle Keras-5 ve Tornado-6, teknik açıdan incelenmiş adaylar olarak yararlı devir kayıtlarına sahiptir; ancak **kabul edilmiş doğrulayıcı vaka değildir** ve kabul siciline eklenmemelidir.

Güncel dosyalar:
- [Proje ana durumu](README.md)
- [22 Ekim aşama durumu](STAGE_STATUS_2026-10-22.md)
- [Ana yürütme planı](TUBITAK_2204A_MASTER_PLAN_2026-10-21.md)
- [Deney manifesti](EXPERIMENT_MANIFEST_STAGE3.json)
- [Vaka sicili](CASE_REGISTRY.json)
- [V9 teknik tarama ve devir kaydı](STAGE1_V9_BATCH0_REVIEW_HANDOFF_2026-10-22.md)
- [Maruziyet/dışlama kaydı](EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json)

## 3. Araştırmanın dondurulacak kapsamı

**Araştırma sorusu:** Gerçek açık kaynak yazılım kusurlarında, kanıt yetersizken teşhis vermeye zorlamak yerine seçici cevap vermeme politikasına izin vermek, kanıtla desteklenmeyen kesin kök neden teşhislerini azaltır mı; bunun yeterli kanıt bulunan vakalarda doğru yanıt ve cevap kapsamı bakımından maliyeti nedir?

- **E1 — yeterli kanıt:** Kanıt paketi, kök nedeni makul alternatiflerden ayırmaya yeterlidir.
- **E2 — kısmi kanıt:** Bazı ayırt edici kanıt eksiktir.
- **E3 — yetersiz kanıt:** Paket tek bir kök nedeni güvenilir biçimde seçmeye yetmez.
- **P0 — zorunlu teşhis:** Modelden kök neden teşhisi istenir.
- **P1 — seçici teşhis/kaçınma:** Model kanıt destekliyorsa teşhis verir; desteklemiyorsa açıkça kaçınır ve eksik kanıtı belirtir.

Her bağımsız vaka için E1/E2/E3 × P0/P1 olmak üzere altı çıktı planlanmıştır. Önceden yazılmış protokolde hedef 80 vaka, asgari doğrulayıcı örneklem 60 vaka ve en az 8 farklı upstream projedir; bu hedefte 480, asgari örneklemde 360 çıktı gerekir. Bu sayılar **planlama sayılarıdır, gözlenmiş sonuç değildir**.

### Birincil ölçüt

E3 vakalarında kanıtla desteklenmeyen kesin teşhis oranının P1 ile P0 arasındaki vaka eşleştirmeli farkı. Önceden belirlenmiş analiz: iki taraflı exact McNemar testi, P1−P0 risk farkı ve %95 güven aralığı.

### Ayrı raporlanacak ikincil ölçütler

Kök neden doğruluğu; teşhisin görünen kanıtla desteklenmesi; yanıt kapsamı; E1 koşulunda gereksiz kaçınma; modelin istediği ek kanıtın ayırt ediciliği. “Kök nedeni doğru tahmin etme” ile “sunulan kanıtın bu iddiayı desteklemesi” aynı ölçüt değildir.

**Sınır:** Şu anki tasarım, Qwen üzerinde iki karar politikasını inceleyen kontrollü bir deneydir; yeni bir temel model eğitildiği veya doğrulanmış epistemik-belirsizlik kalibrasyonu geliştirildiği iddia edilmeyecektir. Token entropisi ve yanıtlar arası sözcüksel ayrışma, doğrulanmış etiketli kalibrasyon verisi bulunana kadar birincil karar ölçütü yapılmayacaktır. Gold E1/E2/E3 etiketi modele girdi olarak verilmemelidir; bu, cevaplanabilirlik bilgisini sızdırır ve deneyi döngüsel hâle getirir.

## 4. Özgünlük ve bilimsel iddia sınırı

Genel olarak “LLM belirsizlikte cevap vermekten kaçınsın” fikri yeni değildir. Ön taramada aşağıdaki yakın çalışmalar bulundu:

- Wen et al., *Know Your Limits* (TACL, 2025): https://aclanthology.org/2025.tacl-1.26/
- Madhusudhan et al., *Do LLMs Know When to NOT Answer?* (COLING, 2025): https://aclanthology.org/2025.coling-main.627/
- Rathnasuriya & Yang, *When to Answer and When to Defer* (ICSE-NIER, 2026): https://doi.org/10.1145/3786582.3786845
- Zhou et al., *Task Abstention for Large Language Models in Code Generation* (2026): https://arxiv.org/abs/2605.17029
- Zhang & Wu, *Do LLMs Know When Evidence is Insufficient?* (2026): https://www.techscience.com/cmc/v89n1/68467
- Chen et al., *Measure Twice, Locate Once: Mitigating Hallucinations in LLM-based Agents for Repository-Scale Fault Localization* (2026): https://doi.org/10.1145/3831589

Dolayısıyla “ilk”, “benzersiz” veya “özgünlüğü kanıtlanmış” denmeyecektir. Savunulabilecek **aday katkı**, gerçek yazılım kusurlarında kontrollü kanıt yeterliliği koşulları boyunca, gerçek kök neden doğruluğunu ve teşhisin gösterilen kanıtla desteklenmesini ayrı puanlayıp; E3'te kanıtsız kesin teşhisi E1'deki gereksiz kaçınmayla birlikte ölçmektir. Bu dar katkının da literatürde benzersiz olduğu henüz kanıtlanmamıştır; tam metin ve atıf zinciri taraması tamamlanmalıdır.

## 5. Model çalıştırma öncesi zorunlu kapılar

Aşağıdakilerin tamamı gerçek kayıtlarla geçilmeden doğrulayıcı çıkarım yapılmamalıdır:

1. **Teknik hat:** GitHub Actions/runner sorunu netleştirilmeli; ham günlük ve arşiv doğrulamasını üreten iş akışı birim testleriyle doğrulanmalı. Sonuç günlükleri erişilemiyorsa CI'ın geçtiği varsayılmamalı.
2. **Örneklem:** Önceden maruz kalınmış vakalar dışarıda tutularak en az 60 bağımsız vaka ve en az 8 upstream proje doğrulanmalı; hedef 80. Her vakada kayıtlı Python/runtime eşleşmesi, buggy revizyonda hedef kusurun yeniden üretimi ve fixed revizyonda aynı testin geçmesi şart.
3. **Bilimsel vaka kabulü:** Kaynak, lisans, kök neden, test/patch ilişkisi, vaka bağımsızlığı, önceki maruziyet ve bilgi sızıntısı kontrol edilmeli. Kurulum hatası bir yazılım kusurunun yeniden üretimi sayılmamalı.
4. **İki ayrı insan inceleme paneli:** En az iki bağımsız inceleyici kök neden/provenance panelinde, panelden farklı en az iki bağımsız inceleyici ise vaka kimliği ve gold kök nedeni görmeden kanıt yeterliliği panelinde görev almalı. İlk puanlar ve uyuşmazlık çözümü korunmalı. Boş formlar hazırdır; gerçek incelemeler tamamlanmış değildir.
5. **Kanıt paketleri:** E1/E2/E3 paketleri model yanıtları görülmeden hazırlanmalı ve hash'lenmeli. E3 gerçekten birden fazla makul açıklamayı açık bırakmalı; yanıltıcı veya yapay olarak bozulmuş kanıt kullanılmamalı.
6. **Model/runtime:** Qwen/Qwen2.5-3B-Instruct'in sabit revision ve tokenizer'ı, lisansı, chat template'i, FP16 ayarı, kütüphaneler ve gerçek GPU/runtime yüklemesi çıktısız ön kontrolde doğrulanmalı.
7. **Dondurma ve ön kayıt:** İstemler, çıktı şeması, vaka sicili, puanlama rubriği, analiz planı ve runtime parmak izinin SHA-256 değerleri doğrulanmalı; protokol ilk model yanıtı alınmadan önce denetlenebilir bir yerde kaydedilmeli.
8. **Açık yürütme izni:** Read-only preflight “ready=true” vermeli ve ardından ayrı, açık yetkilendirme alınmalı. Sadece CI'ın yeşil olması veya teknik bir dosyanın oluşması çıkarım izni değildir.

## 6. Öncelik sırasına göre tamamlama planı

**Öncelik 1 — CI ve veri toplama:** Teknik koşu altyapısını istikrarlı hâle getir; yeni, maruz kalınmamış adayları sabit bir örnekleme kuralıyla sıraya al. Önceki debug/teknik tarama grupları doğrulayıcı örnekleme geri sokulmayacak.

**Öncelik 2 — İnsan incelemesini fiilen tamamlama:** Dört bağımsız değerlendirici bulunmalı veya iki ayrı, kimlikleri kesişmeyen panel için yeterli bağımsız uzmanlar ayarlanmalı. Bir yapay zekâ metni veya otomatik test, insan değerlendirmesinin yapılmış olduğunun yerine geçmez.

**Öncelik 3 — Protokol ve runtime'ı dondurma:** Veri eşiği, reviewer kararları, evidence packet'leri ve model/runtime kontrolleri kapanınca manifest, hash'ler ve ön kayıt tamamlanmalı.

**Öncelik 4 — Deneyi tek seferde yürütme:** Her vaka için altı koşul; ham model çıktıları, prompt/kanıt hash'leri, runtime bilgisi ve şema hataları eksiksiz saklanmalı. Sonuca bakarak prompt değiştirme, çıktıyı seçerek saklama ya da hatalı JSON'u sessizce düzeltme yapılmamalı.

**Öncelik 5 — Kör puanlama ve analiz:** Çıktılar en az iki bağımsız puanlayıcı tarafından önceden belirlenmiş rubrikle değerlendirilerek ilk notlar saklanmalı. Birincil sonuç, etki büyüklüğü ve belirsizlik aralığı raporlanmalı; anlamsız veya olumsuz sonuçlar da korunmalı.

**Öncelik 6 — Rapor/başvuru:** Gerçek sonuçlar ve sınırlılıklar yazıldıktan sonra resmî 2026–2027 yazım şablonuna aktarılmalı, kaynakça ve bütünlük denetimi yapılmalı, son PDF kontrol edilmeli.

### İç kontrol takvimi

- **23–31 Ekim:** CI/runner hatası; gözden geçirici organizasyonu; örneklem ve protokol dondurma hazırlığı.
- **1–4 Kasım:** Veri ve insan incelemesi kapılarının durumu için açık bir go/no-go kararı. Kapılar geçilmezse çıkarım izni verilmez.
- **Kasım:** Yalnızca bütün kapılar geçtiğinde model deneyini yürütme ve kör puanlama.
- **Aralık:** Analiz, sınırlılıklar, kaynakça, resmî şablon ve başvuru öncesi teknik denetim.
- **Resmî son tarih:** 4 Ocak 2027, saat 17.30 (Türkiye saati). Tarihin yaklaşması bilimsel kabul eşiklerini geriye dönük gevşetme gerekçesi değildir.

## 7. TÜBİTAK başvurusu için karar

Resmî çağrı ve kılavuz: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi

TÜBİTAK 2204-A başvurusu fikir veya devam eden çalışma olarak değil, tamamlanmış araştırma olarak hazırlanmalıdır. Bu nedenle şu an rapora “model halüsinasyonu azalttı”, “güven skoru kalibre edildi”, “hipotez doğrulandı” veya “proje tamamlandı” ifadeleri yazılamaz. Bulgular elde edilmeden sonuç bölümü doldurulmayacak; mevcut eski CCDG sonuçları bu boşluğu kapatmak için taşınmayacaktır.

Resmî rehberdeki rapor biçimi ve son şablon başvuru öncesi tekrar kontrol edilmeli. Depodaki önceki resmi-şablon QA kaydında raporun Türkçe PDF, 2–20 sayfa, 150–250 kelimelik özet, en fazla 15 kelimelik başlık ve en fazla beş anahtar kelime gereklilikleri kaydedilmiştir; göndermeden önce bunlar güncel resmî belgede bir kez daha doğrulanmalıdır.

## Nihai karar

**Konu korunuyor; proje henüz bitmiş sayılmıyor.** Şu an teslim edebileceğimiz en doğru mühendislik sonucu, araştırma sorusu ve deney altyapısını kanıt sınırlarıyla dondurmak ve model çalıştırma öncesi kapıları kapatmaktır. Asıl bilimsel proje ancak yeterli ve kabul edilmiş vaka havuzu, bağımsız insan incelemeleri, doğrulanmış runtime, gerçek model çıktıları ve sonuç analizi tamamlanınca biter. Bu şartları yok sayarak sahte bir “tamamlanmış proje” üretmek yerine, jüri önünde savunulabilecek tek çizgiyi izliyoruz.
