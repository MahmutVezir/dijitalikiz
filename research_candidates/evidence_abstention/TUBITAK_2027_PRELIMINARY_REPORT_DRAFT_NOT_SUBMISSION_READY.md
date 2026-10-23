# TÜBİTAK 2204-A 2027 — Ön Proje Raporu Taslağı

> **GÖNDERİME HAZIR DEĞİL.** Bu belge, gerçek deney tamamlandığında son rapora dönüştürülmek üzere hazırlanmış giriş ve yöntem taslağıdır. Doğrulayıcı vaka sayısı 0, geçerli ana deney çıktısı 0'dır. Bilimsel etki sonucu bulunmadığından bu belge mevcut hâliyle yarışma raporu olarak gönderilmemelidir.

**Başlık:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Teknik alt başlık:** Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi  
**Ana alan adayı:** Yazılım  
**Tematik alan adayı:** Yapay Zekâ  
**Tarih:** 23 Ekim 2026

## 1. Özet — gerçek sonuçlardan sonra tamamlanacak

Bu araştırma, büyük dil modellerinin yazılım hatalarının kök nedenini teşhis ederken kanıt yetersiz olduğunda kesin yanıt üretmek yerine cevap vermekten kaçınmaya yönlendirilmesinin etkisini ölçmeyi hedeflemektedir. Aynı gerçek yazılım kusurları için yeterli, kısmi ve yetersiz kanıt paketlerinin; teşhisi zorunlu kılan bir politika ile kanıt yetersizliğinde kaçınmaya izin veren bir politikanın eşleştirilmiş karşılaştırmasında kullanılması planlanmaktadır. Kök neden tahmininin doğruluğu ile tahminin modelin gördüğü kanıt tarafından desteklenmesi ayrı ölçütler olarak puanlanacaktır. Birincil ölçüt, yetersiz kanıt koşulunda desteklenmeyen kesin teşhis oranıdır. Cevap kapsamı ve yeterli kanıt koşulunda gereksiz kaçınma olası maliyetler olarak ayrıca raporlanacaktır.

**Bu özet tamamlanmış araştırmanın özeti değildir.** Gerçek örneklem, model çıktıları, bağımsız değerlendirme ve istatistikler elde edildikten sonra yeniden yazılmalıdır. Mevcut aşamada modelin hataları azalttığı veya hipotezin doğrulandığı iddia edilemez.

## 2. Giriş

Büyük dil modelleri yazılım sorunlarını açıklamak ve hata teşhisine yardımcı olmak için kullanılmaktadır. Ancak akıcı ve kendinden emin bir yanıt, yanıtın doğru olduğunu ya da sağlanan kanıtlarca desteklendiğini tek başına göstermez. Aynı hata izi birden fazla kök nedenle uyumlu olabilir. Modeli her durumda teşhise zorlamak, kanıtın ayırt etmeye yetmediği durumda gereğinden kesin iddialar üretmesine yol açabilir. Buna karşılık her belirsizlikte cevap vermemek de doğru yanıtları kaybettirebilir.

Cevap vermekten kaçınma (abstention), aktif bir araştırma alanıdır. Wen ve arkadaşlarının 2025 tarihli derlemesi büyük dil modellerinde abstention yöntemlerini, benchmarkları ve ölçütleri inceler. Kirichenko ve arkadaşlarının NeurIPS 2025'te yayımlanan AbstentionBench çalışması cevaplanamaz ve eksik tanımlanmış sorularda kaçınmayı farklı veri kümeleri üzerinde değerlendirir. Kod tahminlerinde cevap verme/erteleme kararı, kod üretiminde abstention ve yazılım hata yerelleştirme üzerine de yakın çalışmalar vardır. Bu nedenle genel “yapay zekâ cevap vermemeyi öğrenebilir mi?” sorusu tek başına özgün katkı olarak sunulmayacaktır.

Araştırılacak olası katkı daha dardır: kaynak kod, hedef test ve düzeltme geçmişiyle doğrulanmış yazılım kusurlarında, modelin kök neden tahmininin doğru olup olmadığı ile o tahminin görünür kanıttan çıkarılıp çıkarılamadığı ayrı değerlendirilecektir. Bu, model tesadüfen doğru tahmin etse bile kanıt paketi alternatifleri dışlamıyorsa bunun fark edilmesini sağlar. Bu olası farkın literatürde benzersiz olduğu henüz kanıtlanmamıştır; mevcut tarama hedeflidir, sistematik derleme değildir.

## 3. Araştırma sorusu ve hipotez

**Araştırma sorusu:** Gerçek açık kaynak yazılım kusurlarında, kanıt yetersizken teşhis vermekten kaçınmaya açıkça izin veren bir istem politikası (P1), teşhisi zorunlu kılan politikaya (P0) kıyasla kanıtla desteklenmeyen kesin kök neden teşhislerini azaltır mı? Bunun yeterli kanıt koşulundaki doğru teşhisler ve cevap kapsamı bakımından maliyeti nedir?

**Birincil hipotez:** E3 (yetersiz kanıt) koşulunda P1, P0'a kıyasla vaka başına kanıtla desteklenmeyen kesin teşhis oranını düşürür.

Hipotezin desteklenmesi zorunlu bir sonuç değildir. Sıfır etki, ters etki ve geçersiz/puanlanamayan çıktılar da aynı açıklıkla raporlanacaktır.

## 4. Yöntem

### 4.1 Deney tasarımı

Sabit model ve eşleştirilmiş vakalar üzerinde üç kanıt düzeyi × iki istem politikası karşılaştırması planlanmıştır. Her kabul edilen vaka için altı koşul hücresi ve her hücre için tek deterministik model yanıtı öngörülür.

- **E1 — yeterli kanıt:** Kök nedeni makul alternatiflerden ayırmaya yetecek bilgi vardır.
- **E2 — kısmi kanıt:** En az bir kritik ayırt edici bilgi eksiktir.
- **E3 — yetersiz kanıt:** Birden fazla makul açıklama açık kalır.
- **P0 — zorunlu teşhis:** Tek bir en olası kök neden belirtilmesi istenir; kaçınmaya izin verilmez.
- **P1 — seçici kaçınma:** Teşhis yalnızca kanıt yeterli ve ayırt ediciyse verilir; aksi durumda kaçınılır ve ayırt etmek için gereken ek bilgi belirtilir.

P0/P1 arasındaki tek planlı fark politika talimatıdır. Modelin gördüğü pakete gizli E1/E2/E3 etiketi, gerçek kök neden veya fixed düzeltme metni eklenmez. Aynı model sürümü, sistem talimatı, çıktı şeması ve üretim ayarları korunur.

### 4.2 Veri ve vaka kabulü

Aday kaynak, sabit revizyona bağlanmış BugsInPy açık kaynak hata veri kümesidir. Metadata kaydı tek başına vaka kabulü sayılmaz. Her vaka için kaynak/lisans incelemesi; buggy ve fixed revizyonlar; aynı hedef testin buggy sürümde kusur nedeniyle başarısız, fixed sürümde başarılı olduğunu gösteren ham loglar; çalışma ortamı; kök neden dayanağı; maruziyet/sızıntı incelemesi ve kanıt paketi hash'leri gereklidir. Önceki araştırma ya da hata ayıklama sırasında açığa çıkmış vakalar doğrulayıcı örneklemden kalıcı olarak dışlanacaktır.

Hedef 80 bağımsız kusur vakasıdır. Doğrulayıcı alt sınır en az 60 bağımsız vaka ve en az 8 upstream projedir. Bu eşik sağlanamazsa sonuçlar doğrulayıcı etki iddiası olarak sunulmayacaktır.

### 4.3 Model ve tekrar üretilebilirlik

Aday model Qwen/Qwen2.5-3B-Instruct, sabit revizyon kimliği aa8e72537993ba99e69dfaafa59ed015b17504d1 olarak belirlenmiştir. Model ve tokenizer yüklemesi, chat template, Python/PyTorch/Transformers/CUDA-GPU ortamı ve artefakt hash'leri deney öncesinde doğrulanmalıdır. Ana deney deterministiktir; otomatik yeniden üretme, bozuk JSON'u onarma veya sonuç görüldükten sonra hücre değiştirme yoktur.

### 4.4 Altın cevap ve paket bütünlüğü

Her kanıt paketinin tam olarak modele gösterilen metin biçimi SHA-256 ile bağlanır. Buna ek olarak, modelin görmediği doğrulanmış kök neden metninin hash'i kabul edilen vaka sicilinde saklanır ve kısıtlı çalıştırma veri kümesindeki metinle eşleşmesi zorunludur. Bu iki bütünlük denetimi, aynı kanıt paketi korunurken referans cevabın sessizce değiştirilmesini önlemeyi amaçlar. Hash uyuşmazlığında deney çalıştırması durdurulur; vakayı yeni bir değerle otomatik olarak güncellemek yasaktır.

### 4.5 Kör değerlendirme

Kök neden ve buggy/fixed test ilişkisini değerlendiren iki kişilik panel ile modelin görünen kanıtına dayanmasını değerlendiren, ilk panelden ayrı iki kişilik kör panel planlanmıştır. Kanıt paneli gerçek kök nedeni, fixed kodu, vaka kimliğini ve gizli kanıt düzeyi etiketini görmemelidir. İlk puanlar saklanacak, uyuşmazlıklar önceden belirlenmiş adjudication kurallarıyla çözülecektir. İnsanlar fiilen değerlendirme yapmadan bu adım tamamlanmış sayılmayacaktır.

### 4.6 Ölçütler ve analiz

**Birincil ölçüt:** E3'te desteklenmeyen kesin teşhislerin P1−P0 vaka-eşleştirilmiş risk farkı. Önceden belirlenen analiz, iki taraflı exact McNemar testi ve konservatif %95 güven aralığıdır.

**İkincil ölçütler:** E1/E2/E3 için cevap/kaçınma kapsamı; E1'de gereksiz kaçınma; kök neden doğruluğu; görünür kanıt desteği; geçersiz JSON/şema oranı; değerlendiriciler arası uyum ve ek kanıt isteminin ayırt ediciliği. Daha çok kaçınmak tek başına başarı kabul edilmeyecektir.

### 4.7 Örneklem gücü duyarlılığı

Mevcut analiz planında 60 vakalık alt sınır ve 80 vakalık hedef için senaryo tabanlı exact McNemar güç hesapları yer almaktadır. Bunlar gözlenmiş sonuç veya tarihsel pilot tahmini değildir. Örneğin, çiftlerin %30'unun iki politikada farklı sonuca sahip olduğu ve bu farklı çiftlerin %83'ünde sonucun P1 lehine olduğu varsayılırsa, iki taraflı alfa 0,05 için hesaplanan güç N=60'ta yaklaşık %78,7 ve N=80'de yaklaşık %90,1'dir. Aynı %30 discordance altında P1 lehine oran %75'e düşerse güç N=60'ta yaklaşık %49,5 ve N=80'de yaklaşık %63,4 olur.

Bu yüzden 60/80 hedefi küçük etkileri dışlamak için garanti değildir. Varsayımlar gerçek verilere dayanmamaktadır; bulgular görülmeden önceki duyarlılık değerlendirmesi olarak yorumlanmalıdır. Gerçek vaka havuzu bu örnekleme ulaşmazsa eşik sonradan gevşetilmemeli; sınırlı güç ve keşifsel yorum açıkça raporlanmalıdır.

## 5. Hazırlık durumu — bilimsel sonuç değildir

| Gösterge | Güncel doğrulanmış kayıt |
|---|---|
| Ham metadata envanteri | 501 kayıt / 17 upstream proje |
| Kalıcı maruziyet dışlaması | 93 benzersiz kimlik |
| Dışlama sonrası metadata kuyruğu | 407 aday / 14 upstream proje |
| İlk V10 metadata aday grubu | 100 aday / 14 upstream proje |
| Kabul edilmiş doğrulayıcı vaka | **0** |
| Geçerli ana deney model çıktısı | **0** |
| Tam model/tokenizer/GPU doğrulaması | Tamamlanmadı |
| Bağımsız insan puanlaması | Tamamlanmadı |
| Denetlenebilir dış ön kayıt | Tamamlanmadı |
| Birincil istatistiksel sonuç | Hesaplanamaz |

Metadata adayları araştırma örneklemi değildir. Önceki mühendislik smoke çıktıları maruziyet, prompt/protokol farkları ve çalışma ortamı sorunları nedeniyle doğrulayıcı analizden dışlanmıştır. Mevcut kayıtlardan model performansı veya hipotez hakkında sonuç çıkarılamaz.

## 6. Sınırlılıklar

Araştırma henüz ana deney verisi üretmediğinden şu anki temel sınırlılık, kabul edilmiş vaka ve geçerli model çıktısı bulunmamasıdır. Ayrıca bağımsız değerlendirme, runtime doğrulaması ve haricî ön kayıt tamamlanmamıştır. İleride deney tamamlanırsa kamuya açık hata raporları ve düzeltmelerin modelin ön eğitiminde bulunma olasılığı tamamen dışlanamayabilir; projeler arası kümelenme ve örneklem büyüklüğü genellenebilirliği sınırlayabilir. Sonuçlar yalnızca incelenen model sürümü, prompt politikası, vakalar ve ölçütler için yorumlanmalıdır.

Öz-bildirilen güven puanı kalibre edilmiş olasılık sayılmayacaktır. Entropi veya Brier/ECE tabanlı güven kalibrasyonu ayrı bir deney ve ayrı insan etiketli veri gerektirir; ana P0/P1 deneyine karıştırılmayacaktır.

## 7. Sonuç — deney bitene kadar doldurulmayacak

Mevcut hazırlık durumu araştırma sorusuna bilimsel yanıt vermeye yetmemektedir. Protokol ve yazılım altyapısının hazırlanmış olması, modelin desteksiz teşhislerini azalttığının kanıtı değildir. Sonuç bölümü ancak veri kabulü, model/runtime doğrulaması, kör insan puanlaması, denetlenebilir ön kayıt, deney, istatistiksel analiz ve tekrarlanabilirlik kontrolleri tamamlandıktan sonra yazılmalıdır.

## 8. Ön kaynakça

1. Wen, B., Yao, J., Feng, S., Xu, C., Tsvetkov, Y., Howe, B., & Wang, L. (2025). *Know Your Limits: A Survey of Abstention in Large Language Models*. TACL, 13, 529–556. https://aclanthology.org/2025.tacl-1.26/
2. Kirichenko, P., Ibrahim, M., Chaudhuri, K., & Bell, S. J. (2025). *AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions*. NeurIPS 2025 Datasets and Benchmarks Track. https://proceedings.neurips.cc/paper_files/paper/2025/hash/fb122bfc3f0127a94ded048b5b03496f-Abstract-Datasets_and_Benchmarks_Track.html
3. Madhusudhan, S. S. et al. (2025). *Do LLMs Know When to NOT Answer?* COLING 2025. https://aclanthology.org/2025.coling-main.627/
4. Rathnasuriya, D., & Yang, J. (2026). *When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions*. ICSE 2026 NIER. https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-When-to-Defer-A-Decision-Framework-for-Reliable-Code-Predictions
5. TÜBİTAK. (2026). *2204-A Lise Öğrencileri Araştırma Projeleri Yarışması — 2026–2027 çağrısı ve proje rehberi*. https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi

**Kaynakça ve rapor biçimi ön denetim durumundadır.** Kaynakların tam metin/atıf ağı incelemesi sürmektedir; nihai rapor resmî 2027 şablonuyla son kez karşılaştırılmalıdır.
