# TÜBİTAK 2204-A Proje Raporu Taslağı

**Proje Ana Alanı:** Yazılım  
**Proje Tematik Alanı:** Yapay Zekâ  
**Proje Adı (Başlığı):** LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi

## Yapay Zeka Araçları Kullanım Beyanı

**Kullanılan araçlar:** OpenAI ChatGPT (GPT-6; erişim dönemi: Eylül-Ekim 2026) ve deney yanıtlarını üreten sabit Qwen/Qwen2.5-3B-Instruct modeli (Ekim 2026).

**Kullanım amacı:** Araştırma sorusu ve yöntem taslağını netleştirme, alternatif deney tasarımlarını değerlendirme, Python kodu ve test taslakları hazırlama, GitHub Actions doğrulama akışlarındaki hataları inceleme, bütünlük kontrollerini ve rapor taslaklarını geliştirme. Qwen modeli ise dondurulmuş deney koşullarında yazılım hatalarına ilişkin yanıt üretmek için deney konusu olarak kullanılmıştır.

**Kullanım kapsamı:** ChatGPT desteği araştırma planı ve deney taslağı, Python kod/test taslakları, GitHub Actions doğrulama akışlarını inceleme, veri/artifact bütünlük denetimlerini yorumlama, V2'nin bilgi-paritesi ve kaynak-sızıntısı testleri, kalite kapıları/TÜBİTAK uygunluk dokümantasyonu ve rapor dilini gözden geçirme aşamalarını içermiştir. Bazı yeni testler ve insan puanlayıcı uzlaşmasını ölçmeye yönelik yardımcı bir denetim aracı da ÜYZ desteğiyle taslaklanmıştır; aracın gerçek insan puanı üretmediği ve kalibrasyon eşiğini kendiliğinden geçirmediği açıkça korunmaktadır. Sentetik test örnekleri ampirik model başarısı verisi değildir. Qwen yanıtları deney kayıtlarında saklanmış; tarihsel sonuçlar sonradan tercih edilen hipotezi destekleyecek şekilde değiştirilmemiştir.

**İnsan müdahalesi:** Kod ve artefaktlar otomatik test ve SHA-256 bütünlük denetimleriyle kontrol edilmiştir. Ancak ölçüm aracının taban etkisi ve tarihsel bağlamlar arasındaki bilgi paritesi sınırlılığı açıkça raporlanmıştır. Başvuru sahibi, nihai raporu ve yöntemini bağımsız biçimde açıklayabildiğini başvuru öncesinde doğrulamalı; bu beyanı gerçek kullanım kayıtları ve güncel TYBS alanlarıyla son kez eşleştirmelidir.

## Özet

Büyük dil modelleri (LLM), yazılım hatalarını açıklama ve kök nedenlerini belirleme amacıyla kullanılmaktadır. Ancak bağımlılık ilişkilerinin açık bir grafik olarak sunulmasının kök neden teşhisine katkısı, bağlamdaki diğer bilgi farklarından ayrılarak ölçülmelidir. Bu projede Standard Context ile CCDG Context koşulları karşılaştırılmış; sonraki kod denetimi iki bağlamın tam bilgi eşdeğerliğine sahip olmadığını ortaya çıkarmıştır. Bu nedenle sonuçlar saf grafik gösterimi etkisi olarak yorumlanmamaktadır. Deneylerde sabit bir Qwen2.5-3B-Instruct model checkpoint'i kullanılmış; dört gerçek yazılım hatası üzerinde 40 koşuluk pilot ve pilot vakalarından bağımsız 16 vaka üzerinde 160 koşuluk doğrulayıcı deney yürütülmüştür. Her vaka, Standard ve CCDG koşullarında beş sabit tohumla çalıştırılmış; aynı vaka iki koşulda eşleştirilmiş ve istatistiksel analiz birimi bağımsız yazılım vakası olarak tanımlanmıştır. Tüm 200 inference çıktısı ayrıştırılmış, ham çıktı hash'leri ve artifact dosya envanteri doğrulanmıştır. Dondurulmuş doğrulayıcı birincil ölçütü, her vaka için önceden belirlenmiş kök neden ifadelerinin açıklamada bitişik ifade olarak eşleşmesine dayanır. Bu ölçütte Standard 0/80, CCDG 0/80 geçiş üretmiş; 16 vakanın tamamı iki koşulda da başarısız sınıflandırılmış ve exact iki taraflı McNemar testi p=1,00 bulunmuştur. Bu sonuç, kullanılan eşleştiricinin taban etkisini göstermektedir; koşulların eşdeğerliğini veya CCDG'nin etkisizliğini kanıtlamaz. Araştırmanın anlamsal hipotezi bu operasyonelleştirmeyle çözümlenememiştir.

## Anahtar Kelimeler

Büyük dil modelleri; yazılım hata teşhisi; kök neden analizi; CCDG; Defects4J.

## Amaç

Araştırmanın amacı, açık ve yapılandırılmış çapraz-bileşen bağımlılık temsilinin LLM tabanlı hata teşhisine etkisini tekrarlanabilir bir deneyle ölçmektir.

- **H1 (araştırma beklentisi):** CCDG koşulu, Standard Context'e kıyasla vaka düzeyinde kök neden doğruluğunu artırır.
- **H0 (istatistiksel sıfır hipotezi):** Dondurulmuş doğrulayıcı ölçütte Standard ve CCDG koşullarının vaka düzeyindeki başarı olasılıkları arasında fark yoktur.

Birincil doğrulayıcı ölçüt, pilot sonrası ve doğrulayıcı inference başlamadan önce dondurulan vaka-özel kök neden alias eşleştiricisidir. Bu puanlama protokolü, pilot çıktılarından sonra ölçüm sorunu teşhis edilerek değiştirilmiştir. Bu nedenle nihai raporda ölçüt, tüm model çıktıları görülmeden önce kaydedilmiş gibi sunulmamaktadır. Önceki tam-teşhis puanı ve pilot verisi değiştirilmemiş; tam-teşhis ölçütü ikincil sonuç olarak korunmuştur.

## Giriş

Büyük dil modelleri doğal dilde hata açıklama, kod üretme ve yazılım mühendisliği iş akışlarında giderek daha fazla araştırılmaktadır. Gerçek hata kayıtlarının kontrollü biçimde incelenmesi, modellerin yalnızca örnek kodlarda değil, gerçek yazılım projelerinde de hangi koşullarda başarılı olduğunu ölçmek için önemlidir. Defects4J, gerçek Java projelerinden alınan hata örnekleri ve hata düzeltme sürümleriyle kontrollü yazılım çalışmaları için bir veri kaynağı sağlamaktadır (Just et al., 2014). SWE-bench gibi çalışmalar ise gerçek GitHub sorunlarının çözümünde model performansını ölçmenin, bağlamı ve çok dosyalı değişiklikleri doğru anlamayı gerektirdiğini göstermektedir (Jimenez et al., 2024).

Kod temsillerinde yapısal bilginin kullanılması yeni bir fikir değildir. GraphCodeBERT, kodla ilişkili veri akışı bilgisini temsil öğrenimine dahil eden bir yaklaşım örneğidir (Guo et al., 2021). CodeBERT ve kod üzerinde eğitilmiş büyük dil modellerinin değerlendirilmesine yönelik çalışmalar da kod anlama ve üretme görevlerinin ayrı değerlendirme gerektirdiğini vurgulamaktadır (Feng et al., 2020; M. Chen et al., 2021). Yazılım mühendisliği için LLM literatürünü inceleyen sistematik çalışmalar, görevler, veri kümeleri ve değerlendirme yöntemleri arasında önemli farklılıklar bulunduğunu raporlamıştır (Hou et al., 2024). Qwen2.5 teknik raporu, bu araştırmada kullanılan model ailesinin mimari ve değerlendirme bağlamını açıklar; ancak tek başına bu projedeki CCDG hipotezini destekleyen doğrudan kanıt değildir (Qwen Team, 2024).

İstemleme ve akıl yürütme çalışmaları, modelden istenen görev tanımının ve sunulan kanıtların çıktıları etkileyebileceğini göstermiştir (Wei et al., 2022; Yao et al., 2023). Modelin kendi çıktısını denetlemesi üzerine yapılan çalışmalar (X. Chen et al., 2023) ve dış bilgi kaynaklarını modele sağlayan retrieval-augmented generation yaklaşımı (Lewis et al., 2020) da bağlamın ve doğrulama stratejisinin önemini gösterir; ancak bunlar CCDG etkisini doğrudan sınamaz. Bununla birlikte, bileşenler arası bağımlılıkların açık bir grafik olarak verilmesinin, aynı temel hata kanıtlarını kullanan standart bir bağlama göre kök neden teşhisini artırıp artırmadığı ayrı bir deneysel sorudur. Bu proje, genel LLM yetenekleri hakkında geniş bir iddia ileri sürmek yerine, tek bir sabit model ve belirli gerçek yazılım hataları üzerinde iki bağlam temsilini eşleştirilmiş bir tasarımla karşılaştırmaktadır.

**Araştırma sorusu:** Aynı yazılım hatasına ilişkin temel kanıtlar korunurken, bileşenler arası bağımlılıkların açık CCDG biçiminde sunulması LLM'nin kök neden teşhis doğruluğunu Standard Context'e göre artırır mı?

## Yöntem

### Araştırma tasarımı

Aynı bağımsız yazılım vakası iki koşulda değerlendirilmiştir:

1. **Standard Context:** Hata ve bileşenler hakkında temel kanıtlar standart metinsel bağlamla sunulmuştur.
2. **CCDG Context:** Bağımlılık kenarları ve I_base maddeleri sunulmuştur; ancak tarihsel oluşturucu açık hata açıklaması bölümünü Standard Context'teki gibi eklememiştir.

Model checkpoint'i, sistem istemi, ana istem şablonu, tohumlar ve üretim ayarları sabit tutulmuştur. Ground truth iki deney koşulunun model bağlamlarına eklenmemiştir. Ancak bağlam oluşturucularının kod denetimi, iki koşulun sunulan bilgi bakımından tam eşleştirilmediğini göstermiştir: Standard Context açık hata açıklamasını içerirken CCDG Context açık bağımlılık kenarları eklemiş ve açık hata açıklaması alanını dışarıda bırakmıştır. Bu yüzden tarihsel deney, yalnızca grafik gösteriminin nedensel etkisini izole edememektedir. Bu fark mevcut sonuçlar görülerek sonradan düzeltilmemiş; tarihsel kod, istem hash'leri ve kayıtlar yeniden yazılmamıştır.

### Veri ve vaka seçimi

Pilot deney dört gerçek Apache Commons Math / Defects4J hatasından oluşturulmuştur: MATH-927, MATH-950, MATH-949 ve MATH-988. Her pilot vakası iki koşulda beş sabit tohumla çalıştırılmıştır: **4 × 2 × 5 = 40 inference**.

Doğrulayıcı deney, pilot vakalarını içermeyen 16 bağımsız vakadan oluşmaktadır: CLOSURE-4, CLOSURE-6, CLOSURE-14, MATH-305, MATH-326, MATH-358, MATH-377, MATH-392, MATH-393, MATH-405, MATH-631, MATH-859, MATH-924, TIME-1, TIME-12 ve MOCKITO-19. Vaka seçimi model çıktılarından bağımsız olarak yapılmış; kaynak, düzeltme revizyonu, kök neden kanıtları, CCDG uygunluğu ve contamination (eğitim verisine sızma/maruziyet) riski kayıt altına alınmıştır. Doğrulayıcı deney **16 × 2 × 5 = 160 inference** olarak yürütülmüştür.

Seçilen tüm doğrulayıcı vakalar için kamuya açık olma kaynaklı contamination riski yüksek olarak etiketlenmiştir. Bu etiket, vakaların modelin eğitim verisinde kesinlikle bulunduğunu göstermez; yalnızca bu ihtimalin araştırma açısından bir sınırlılık olduğunu belirtir.

### Model ve üretim ayarları

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Sabit checkpoint revizyonu: `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- Yükleme hassasiyeti: FP16
- Kuantizasyon: yok
- Temperature: 0,2
- Top-p: 1,0
- Örnekleme: açık (`do_sample=true`)
- Maksimum yeni token: 256
- Tohumlar: 42, 43, 44, 45, 46
- Çalışma ortamı: Python 3.11; PyTorch 2.2.1; Transformers 4.43.2; GPU ortamında iki NVIDIA Tesla T4

İlk planlamada değerlendirilen GPTQ checkpoint'i, herhangi bir araştırma kaydı yazılmadan önce model yükleyicisinin bazı parametrelerde beklenmeyen başlatma bildirmesi ve tek örnekli örnekleme testinde geçersiz olasılıklarla karşılaşılması nedeniyle kullanılmamıştır. Yerine tam revizyonu sabitlenmiş resmî Qwen2.5-3B-Instruct checkpoint'i alınmış ve FP16 olarak yüklenmiştir. Bu, inference öncesi model uyumluluğu düzeltmesidir; pilot kayıtları başladıktan sonra yapılmış bir model değişikliği değildir.

### Ölçüm aracı ve vaka düzeyi karar

Her inference sonucu JSON formatında istenmiş ve ayrıştırılmıştır. Dondurulmuş doğrulayıcı birincil ölçüt, her vaka için kaynak kanıtları ve ground truth temel alınarak önceden yazılan kök neden alias ifadelerinden en az birinin `root_cause_class` ve `explanation` alanlarının birleştirilmiş metninde normalleştirme sonrası **bitişik ifade** olarak bulunmasına dayanır. Noktalama işaretleri ve boşluklar normalleştirilir; eş anlamlı olabilecek fakat alias ifadesiyle bitişik eşleşmeyen açıklamalar geçiş sayılmaz. Ayrıştırma veya şema hataları başarısız koşu olarak ele alınır.

Bir vaka-koşul bileşimi, beş tohumun en az üçünde birincil ölçütü geçtiğinde başarılı sayılır. Beş tohum bağımsız yazılım vakaları olarak sayılmamıştır; istatistiksel birim yazılım hatasıdır.

Bu ölçüt deterministik ve tekrarlanabilir olmakla birlikte semantik bir değerlendirici değildir. Anlamca doğruya yakın bir açıklamayı, sabit alias dizisi bitişik geçmediği için başarısız sayabilir. Bu sınırlılık, sonuçların yorumunda merkezi önemdedir.

### Veri bütünlüğü ve tekrarlanabilirlik

Her kayıt model kimliği ve revizyonu, tohum, koşul, istem/bağlam hash'leri, ham çıktı hash'i, zaman damgaları ve ayrıştırılmış sonuçla ilişkilendirilmiştir. Deney kaynakları sabit Git commit'leri üzerinden paketlenmiştir. Pilot ve doğrulayıcı artifact'leri GitHub Actions'ta saklanmış; artifact içindeki dosya manifestleri dosya boyutu ve SHA-256 hash'leri üzerinden yeniden kontrol edilmiştir. Normal depo güncellemeleri deney çıktılarının üzerine yazmamıştır.

### İstatistiksel analiz

Birincil karşılaştırma, aynı yazılım vakası için Standard ve CCDG koşullarından elde edilen ikili vaka düzeyi sonuçların eşleştirilmiş karşılaştırmasıdır. İki taraflı exact McNemar testi, α = 0,05 ile kullanılmıştır. Etki, CCDG başarısı eksi Standard başarısı olarak tanımlanan eşleştirilmiş risk farkıyla raporlanmıştır. %95 güven aralığı, iki uyumsuz sonuç oranı için Wilson skor aralıklarını kullanan önceden kayıtlı Newcombe-tipi yaklaşımla hesaplanmıştır.

Örneklem planlaması, doğrulayıcı sonuçlar görülmeden önce kaydedilen McNemar tasarım varsayımlarına dayanmıştır: P(Standard doğru, CCDG yanlış)=0,05 ve P(Standard yanlış, CCDG doğru)=0,60; hedef güç 0,80, α=0,05 ve 16 bağımsız vaka için hesaplanan güç yaklaşık 0,807'dir. Bu değerler tasarım varsayımlarıdır; gözlenen pilot veya doğrulayıcı sonuçlardan türetilmemiştir.

## Proje İş-Zaman Çizelgesi

Çizelgede **X** tamamlanan/yürütülen işi, **P** planlanan işi gösterir. Tarihsel pilot ve doğrulayıcı model çalıştırmaları ile dondurulmuş birincil analiz Ekim 2026 itibarıyla tamamlanmıştır. Bununla birlikte, tarihsel 160 yanıt için hazırlanan kör değerlendirme paketleri henüz gerçek insan puanlarıyla doldurulmamıştır; bu ek çalışma tamamlanmış sayılmaz. İki bağımsız değerlendiricinin ilk puanları gerçekten teslim edilip kilitlenirse, dönen dosyalar yapısal olarak doğrulanacak ve sonuçlar yalnızca **post-hoc keşifsel** analiz olarak raporlanacaktır. Puanlar başvuru için son rapor dondurulmadan önce gelmezse insan değerlendirmesinin yapılmadığı açıkça yazılacak; semantik başarı oranı veya değerlendirici anlaşması uydurulmayacaktır. Bu ek değerlendirme tarihsel bilgi-paritesi kusurunu geriye dönük düzeltmez ve dondurulmuş birincil sonucu değiştirmez. Yeni üç koşullu V2 deneyi ayrı bir gelecek çalışmasıdır ve tüm protokol kapıları kanıtla kapanmadan model çıkarımına izin verilmemektedir.

| İşin adı | Nisan | Mayıs | Haziran | Temmuz | Ağustos | Eylül | Ekim | Kasım | Aralık | Ocak |
|---|---|---|---|---|---|---|---|---|---|---|
| Literatür ve hipotezler |  |  |  |  |  | X | X |  |  |  |
| Vaka seçimi, CCDG ve deney düzeneği |  |  |  |  |  | X | X |  |  |  |
| Pilot/doğrulayıcı deney ve istatistiksel analiz |  |  |  |  |  |  | X |  |  |  |
| Kör insan değerlendirmesi (post-hoc keşifsel) |  |  |  |  |  |  | P | P |  |  |
| Dönen JSONL dosyalarının yapısal doğrulanması ve keşifsel analizi |  |  |  |  |  |  | P | P |  |  |
| Rapor son kontrolü ve başvuru paketi |  |  |  |  |  |  | X | P | P | P |

## Bulgular

### Çalıştırma ve bütünlük sonuçları

| Ölçüt | Pilot | Doğrulayıcı deney |
|---|---:|---:|
| Bağımsız vaka sayısı | 4 | 16 |
| Beklenen inference | 40 | 160 |
| Bulunan inference | 40/40 | 160/160 |
| JSON ayrıştırma hatası | 0 | 0 |
| Doğrulanan artifact dosyası | 55 | 212 |
| Eksik / fazla / hash'i uyuşmayan artifact dosyası | 0 | 0 |

Doğrulayıcı deney, GitHub Actions run ID `37976682761` üzerinde tamamlanmıştır. Arşiv kimliği ve SHA-256 değeri Ek 1’de verilmiştir. Bağımsız denetimde 212/212 dosya ve 160/160 inference kaydı doğrulanmış; ham çıktı hash'lerinde uyuşmazlık ve beklenmeyen dosya bulunmamıştır. Bu kontroller çalıştırma ve veri bütünlüğünü doğrular; tek başlarına teşhis doğruluğunu kanıtlamaz.

### Dondurulmuş birincil ölçüt

| Sonuç | Standard Context | CCDG Context |
|---|---:|---:|
| Inference kaydı | 80 | 80 |
| Ayrıştırma hatası | 0 | 0 |
| Alias ölçütünü geçen inference | 0/80 (0%) | 0/80 (0%) |
| 3/5 çoğunluk kuralıyla başarılı vaka | 0/16 (0%) | 0/16 (0%) |
| İkincil tam-teşhis geçişi | 0/80 (0%) | 0/80 (0%) |

Vaka düzeyindeki eşleştirilmiş tablo aşağıdadır.

|  | CCDG başarılı | CCDG başarısız |
|---|---:|---:|
| Standard başarılı | 0 | 0 |
| Standard başarısız | 0 | 16 |

Exact iki taraflı McNemar testi **p = 1,00** üretmiştir. Gözlenen eşleştirilmiş risk farkı (CCDG − Standard) **0,00**; hesaplanan %95 güven aralığı **[-0,1936; 0,1936]** olmuştur. Sıfır uyumsuz vaka vardır; bütün vakalar her iki koşulda da ölçüte göre başarısız sayılmıştır. Bu nedenle sıfır hipotezi reddedilememiştir.

### Sonucun doğru yorumu

Birincil ölçütte iki koşulda da hiç geçiş olmaması, belirgin bir **taban etkisine** işaret eder. Bitişik ifade kuralı, aynı kavramı farklı kelimelerle açıklayan çıktıları başarısız sayabilir. Örneğin, bir çıktının hata akışını ve `UNCOND` / `ON_EX` kenar türleri arasındaki karışıklığı tarif etmesi, sabit alias ile tam ifade eşleşmesi üretmedikçe geçiş sayılmayabilir. Bu durum, ölçütün anlamsal doğruluğu tam olarak yansıtmadığını gösteren bir ölçüm sınırlılığıdır; tüm model cevaplarının doğru olduğunu göstermez.

Bu sebeple p=1,00 sonucu **koşulların eşdeğer olduğunun kanıtı değildir** ve **CCDG'nin etkisiz olduğunu kanıtlamaz**. Bulgular yalnızca, dondurulmuş literal-alias ölçütü altında fark tespit edilmediğini göstermektedir. Projenin asıl bilimsel sorusu olan CCDG'nin anlamsal kök neden teşhisini artırıp artırmadığı bu ölçüm aracıyla çözümlenememiştir.

### Puanlama protokolü değişikliği

Pilot deneyden sonra, katı tam-teşhis puanlamasının doğal dildeki açıklama biçimlerini başarısız sayabileceği görüldüğünden, doğrulayıcı deneyin birincil ölçütü kaynak kanıtlarına dayalı sabit kök neden alias'larına dönüştürülmüştür. Değişiklik 9 Ekim 2026'da, doğrulayıcı çıktılar incelenmeden önce kayda alınmıştır; ancak pilot çıktıları puanlama sorununun teşhisi için görülmüştür. Bu nedenle bu karar, bütün model çıktıları görülmeden önce eksiksiz biçimde ön kayıt yapılmış bir karar olarak sunulmamaktadır. Vaka seçiminin model çıktılarından bağımsız olduğu ve alias ifadelerinin model çıktılarından türetilmediği kaydedilmiştir. Pilot değerlendirmesi ve doğrulayıcı sonuçlar sonradan değiştirilmemiştir.

### 15 Ekim 2026 tarihli geriye dönük tasarım denetimi

Tarihsel ham çıktıları ve birincil sonuçları değiştirmeden yapılan ek kod/veri denetimi, Standard Context oluşturucusunun 16 vakanın tümünde açık hata açıklaması alanını içerdiğini; CCDG oluşturucusunun ise bu alanı hiçbir vakada sunmadığını ve bunun yerine açık bağımlılık kenarları eklediğini gösterdi. Her iki koşul da kaynak/teknoloji ve I_base maddelerini paylaşmıştır. Dolayısıyla tarihsel karşılaştırma grafik gösteriminin tek başına nedensel etkisini belirleyememektedir.

Ayrıca 16 aktif vakanın 7'sinde I_base içinde “the fix”, “corrected” veya “before the fix” gibi açık düzeltme ipuçları bulundu. Bu sözcüksel tarama bir LLM eğitim verisi sızıntısı kanıtı değildir; yalnızca deney girdisinin bazı vakalarda kök nedeni veya çözüm yönünü kısmen açıklayabildiğine ilişkin bir uyarıdır. Dondurulmuş bağlamlar ve puanlar geriye dönük değiştirilmemiştir; bulgu bu araştırmanın ölçüm ve tasarım sınırlılıklarını açıklayan, sonradan yapılmış bir denetim olarak raporlanmaktadır. Ayrıntılar: docs/HISTORICAL_EXPERIMENT_SCIENTIFIC_AUDIT_2026-10-15.md.

Ölçüm aracının olası yanlış-negatif etkisini somutlaştırmak için, dört dondurulmuş Standard/seed-42 çıktısı ile ilgili vakaların alias listeleri karşılaştırıldı: MATH-305 yanıtı MathUtils.distance içindeki tamsayı taşmasını; CLOSURE-14 yanıtı finally üzerinden exception/fall-through ayrımını; MATH-393 yanıtı kaydedilmiş en iyi optimum yerine sarılmış optimizer durumunun dönmesini; TIME-12 yanıtı Calendar.ERA bilgisinin göz ardı edilmesini açıklıyordu. Dördünde de literal alias eşleşmesi oluşmadı. Bu kayıtlar insan hakemlerince henüz puanlanmadığından **kesin doğru yanıtlar olarak değil, kör anlamsal incelemede değerlendirilmesi gereken olası yanlış-negatif adayları** olarak ele alınır. İnsan değerlendirmesi olmadan semantik doğruluk oranı hesaplanmamıştır.


### Kör anlamsal değerlendirme hazırlığı ve durumu (15 Ekim 2026)

Tarihsel 160 model yanıtına, dondurulmuş birincil ölçütü değiştirmeden uygulanacak sonradan-körlenmiş keşifsel değerlendirme için iki ayrı v1.2 paket hazırlanmıştır. Her paket 160 yanıtı, 16 anonim vaka referansını ve 160 benzersiz değerlendirme kimliğini içerir. Kaynak arşivinin SHA-256 manifest denetiminde 212/212 dosya doğrulanmış; eksik, fazla, boyut uyuşmazlığı veya hash uyuşmazlığı saptanmamıştır. İki değerlendirici paketinin kaynak kayıtlara karşı bağlantı denetimleri her biri için 160/160 eşleşmiştir. Paketlerin SHA-256 değerleri ve sınırları ek denetim raporunda kayıtlıdır.

Bu aşamada paketlerin bütünlük denetiminden geçmesi, yanıtların insanlar tarafından puanlandığı anlamına gelmez. **15 Ekim 2026 itibarıyla gerçek değerlendirici puanları teslim alınmamıştır.** Bu nedenle anlamsal başarı oranı, değerlendirici anlaşması veya Cohen kappa hesaplanmamıştır. Bu istatistikler gerçek ve bağımsız insan puanları gelmeden raporlanamaz.

Paketler açık kök neden cevap anahtarını, doğrudan kaynak URL'lerini ve kaynak vaka kimliklerini değerlendiriciden saklayacak şekilde hazırlanmıştır. Bununla birlikte teknik içerik, vaka veya deney koşulunun tahmin edilmesine hâlâ imkân verebilir; kusursuz körleme garanti edilmez. Bu işlem sunulmuş problem özeti ve temel olgulara dayanan keşifsel puanlamadır; bağımsız kaynak kodu/doğrulama testi incelemesinin yerine geçmez. İki ilk değerlendirme dosyası kilitlenmeden cevap anahtarı açılmamalı ve anlaşmazlıklar tartışılmamalıdır.

Bu değerlendirme, önceki literal-alias sonuçlarının yerine geçmeyecek ve tarihsel Standard ile CCDG bağlamları arasındaki bilgi içeriği farkını geriye dönük gideremeyecektir. İnsan puanları elde edilirse sonuçlar açıkça **post-hoc keşifsel** olarak verilecek; kaynak-revizyonu ve regresyon kanıtına dayalı uyuşmazlık çözümü ilk puanlardan ayrı kaydedilecektir.

Ayrı bir gelecek çalışma olarak tasarlanan V2 doğrulayıcı deney de bu raporda tamamlanmış bir çalışma değildir: güncel manifest hâlâ taslak durumunda, vaka listesi boş, model çıkarımına izin kapalı ve dokuz protokol kapısının tümü beklemededir. Bu kapılar kanıtla kapanmadan V2 modeli çalıştırılmayacaktır.

## Sonuç ve Tartışma

Araştırmanın olumlu yönleri, aynı vaka havuzunun iki koşulda çalıştırılması, tohumların bağımsız vaka sayılmaması, model revizyonunun sabitlenmesi, ground truth'un model bağlamlarından çıkarılması ve çıktıların hash'lerle doğrulanmasıdır. Bununla birlikte, kod denetimi Standard ve CCDG bağlamlarının sunulan bilgi bakımından tam eşleştirilmediğini göstermiştir: Standart bağlam açık hata açıklamasını içerirken CCDG bağlamı bunu aynı biçimde sunmamış ve açık bağımlılık kenarları eklemiştir. Bu karışan değişken, tarihsel deneyin yalnızca grafik gösterimi etkisini izole etmesini engeller. Ayrıca birincil ölçüt, bitişik ifade eşleşmesini anlamsal doğruluğun vekili olarak kullandığından parafrazları yanlışlıkla başarısız sayabilir.

Sonuç, CCDG lehine istatistiksel kanıt sağlamamaktadır; ancak birincil ölçütün tüm vakaları başarısız sınıflandırması nedeniyle CCDG aleyhine güvenilir bir etkisizlik sonucu da sağlamamaktadır. Anlamsal soruyu sınamak için yeni bir doğrulayıcı deneyden önce, skorlayıcının insan uzmanlar tarafından körlenmiş koşullarda test edilmesi, eşanlamlı/parafraz vakalarının önceden tanımlı kurallarla puanlanması ve yeni bağımsız vaka örnekleminin sonuçlara bakılmadan önce kaydedilmesi gerekir. Ayrıca koşullar arasında aynı temel hata açıklamasını koruyan üç koşullu tasarım kullanılmalı; CCDG üçlüleri aynı bağımlılık bilgisini doğal dilde sunan karşılaştırma koluyla sınanmalıdır. Bu mevcut 160 çıktının sonradan yeniden puanlanması halinde yapılacak değerlendirme yalnızca keşfedici (exploratory) sayılmalı; değiştirilen puanlar mevcut doğrulayıcı sonuç gibi sunulmamalıdır.

### Sınırlılıklar

**Bağlam bilgi paritesi:** Tarihsel Standard Context açık hata açıklamasını içerirken CCDG Context bu alanı aynı biçimde sunmamıştır; CCDG ayrıca açık bağımlılık kenarları eklemiştir. Bu karışan değişken, saf temsil etkisinin ayrıştırılmasını engeller.

1. **Ölçüm aracı:** Sabit alias'ın bitişik ifade eşleştirmesi semantik değerlendirme değildir; parafrazları kaçırabilir.
2. **Taban etkisi:** Birincil ölçütte tüm vakaların başarısız olması farkları gözlemlemeyi engellemiştir.
3. **Örneklem:** Doğrulayıcı örneklem 16 yazılım hatası ve belirli açık kaynak Java projeleriyle sınırlıdır; tüm diller, hata türleri veya modeller için genellenemez.
4. **Contamination riski:** Vakalar kamuya açık olduğundan eğitim verisine geçmiş olma olasılığı vardır; bu üyelik doğrudan doğrulanmamıştır.
5. **Anotasyon:** CCDG kenarlarının ve ground truth'un hazırlanmasında insan yorumundan kaynaklanan hata riski vardır.
6. **Puanlama protokolü kronolojisi:** Birincil ölçüt pilot sonrası değiştirilmiş ve bu değişiklik kayda alınmıştır. Bu nedenle ön kayıt sınırlılığı açıkça belirtilmelidir.
7. **Model kapsamı:** Sonuçlar yalnızca sabitlenen Qwen2.5-3B-Instruct checkpoint'i, FP16 yüklemesi, istemleri, ayarları ve seçilen vaka havuzu bağlamında geçerlidir.

### Sonuç

Pilot ve doğrulayıcı deneylerin teknik çalıştırması tamamlanmış; 40 pilot ve 160 doğrulayıcı inference kaydı, JSON ayrıştırma ve artifact hash kontrolleriyle doğrulanmıştır. Dondurulmuş doğrulayıcı birincil alias ölçütünde Standard ve CCDG koşullarının ikisi de 0/80 geçiş göstermiş; 16 vakanın tamamı iki koşulda da başarısız sınıflandırılmıştır. Exact iki taraflı McNemar sonucu p=1,00 ve gözlenen risk farkı 0,00'dır.

Bu bulgu, CCDG'nin anlamsal teşhiste yararsız olduğu ya da iki yöntemin eşdeğer olduğu şeklinde yorumlanamaz. Ölçüt taban etkisi göstermiştir ve araştırmanın anlamsal hipotezini cevaplayamamıştır; ayrıca koşulların bilgi içeriği tam eşleştirilmediği için saf grafik gösterimi etkisi izole edilememiştir. Bilimsel olarak savunulabilir sonuç, tarihsel kurulumda dondurulmuş birincil ölçüt altında fark tespit edilmediğini, ancak bu tasarımın anlamsal hipotezi çözümlemek için yetersiz kaldığını belirtmektir. Sonraki çalışma, kaynak kanıtlarına dayalı ölçüt kalibrasyonu ve aynı temel bilgiyi koruyan üç koşullu (Standart, bağımlılık bilgisi içeren düz metin, CCDG üçlüleri) yeni bağımsız vaka tasarımıyla önceden dondurulmuş bir protokol izlemelidir.

## Öneriler

1. Puanlama aracını kaynak kod, hata raporu, başarısız test ve sabit düzeltme revizyonuyla doğrulanmış örnekler üzerinde kalibre etmek; doğru parafraz, yanlış mekanizma, olumsuzlama ve birden fazla ihtimal içeren yanıtları ayırmak.
2. Yeni doğrulayıcı çalışmada aynı temel hata açıklamasını koruyan üç koşul kullanmak: Standart bağlam (A), bağımlılık bilgisi içeren düz metin (B) ve aynı kenar bilgilerini üçlülerle gösteren CCDG (C). Birincil karşılaştırmayı C-B olarak önceden belirlemek.
3. Puanlama protokolünü, bağımsız vaka listesini, model/tokenizer sürümünü, tüm istem hash’lerini, örneklem büyüklüğünü ve analiz planını inference öncesinde dondurmak; her bağımsız yazılım hatasını bir istatistiksel birim saymak ve olumlu, olumsuz veya belirsiz sonuçları, sonradan eşik ya da puanlama değiştirmeden raporlamak.

## Kaynaklar

Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. de O., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger, G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S., . . . Zaremba, W. (2021). Evaluating large language models trained on code. *arXiv*. https://doi.org/10.48550/arXiv.2107.03374

Chen, X., Lin, M., Schärli, N., & Zhou, D. (2023). Teaching large language models to self-debug [Preprint]. *arXiv*. https://arxiv.org/abs/2304.05128

Feng, Z., Guo, D., Tang, D., Duan, N., Feng, X., Gong, M., Shou, L., Qin, B., Liu, T., Jiang, D., & Zhou, M. (2020). CodeBERT: A pre-trained model for programming and natural languages. In *Findings of the Association for Computational Linguistics: EMNLP 2020* (pp. 1536–1547). https://doi.org/10.18653/v1/2020.findings-emnlp.139

Guo, D., Ren, S., Lu, S., Feng, Z., Tang, D., Liu, S., Zhou, L., Duan, N., Svyatkovskiy, A., Fu, S., Tufano, M., Deng, S. K., Clement, C., Drain, D., Sundaresan, N., Yin, J., Jiang, D., & Zhou, M. (2021). GraphCodeBERT: Pre-training code representations with data flow. In *International Conference on Learning Representations*. https://mlanthology.org/iclr/2021/guo2021iclr-graphcodebert/

Hou, X., Zhao, Y., Liu, Y., Yang, Z., Wang, K., Li, L., Luo, X., Lo, D., Grundy, J., & Wang, H. (2024). Large language models for software engineering: A systematic literature review. *ACM Transactions on Software Engineering and Methodology, 33*(8), Article 220. https://doi.org/10.1145/3695988

Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. R. (2024). SWE-bench: Can language models resolve real-world GitHub issues? In *The Twelfth International Conference on Learning Representations*. https://openreview.net/forum?id=VTF8yNQM66

Just, R., Jalali, D., & Ernst, M. D. (2014). Defects4J: A database of existing faults to enable controlled testing studies for Java programs. In *Proceedings of the International Symposium on Software Testing and Analysis* (pp. 437–440). https://doi.org/10.1145/2610384.2628055

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-T., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. In *Advances in Neural Information Processing Systems* (Vol. 33, pp. 9459–9474). https://arxiv.org/abs/2005.11401

Qwen Team. (2024). Qwen2.5 technical report [Preprint]. *arXiv*. https://arxiv.org/abs/2412.15115

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. In *Advances in Neural Information Processing Systems* (Vol. 35, pp. 24824–24837). https://doi.org/10.52202/068431-1800

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. R., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In *International Conference on Learning Representations*. https://mlanthology.org/iclr/2023/yao2023iclr-react/

## Ekler

### Ek 1. Dondurulmuş deney kayıtları ve bütünlük kanıtı

Pilot çalıştırma: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402; kaynak commit `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`. Doğrulayıcı çalışma: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37976682761; kaynak commit `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`; artifact ID `11640450681`.

Doğrulayıcı arşiv SHA-256: `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`.

Bağımsız denetimler pilotta 55/55 manifest dosyası ve 40/40 kaydı; doğrulayıcı arşivde 212/212 dosya ve 160/160 kaydı doğrulamıştır. Boyut veya SHA-256 uyuşmazlığı bulunmamıştır. Bu kontroller veri bütünlüğünü gösterir; teşhis doğruluğunu tek başına kanıtlamaz.

### Ek 2. Aday vaka için bağımsız düzeltme kanıtı ve kaynak kod

Apache Commons Compress #770 kaynak PR: https://github.com/apache/commons-compress/pull/770. Sabit düzeltme commit'i `bab5629f6b3cea44cf0622cdd92c8cefcfbf360a`. Bağımsız regresyon tekrarı: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37993954772. Aynı test, düzeltme öncesi sürümde beklenen biçimde başarısız ve sabit sürümde başarılı olmuştur.

Bu aday, dondurulmuş 16 vakalık doğrulayıcı deney kümesine eklenmemiştir; yalnızca gelecek çalışma için adaydır. Araştırma kodu, testler, kaynak değerlendirmeleri ve yeniden üretilebilirlik belgeleri https://github.com/MahmutVezir/dijitalikiz adresindeki proje deposunda sürümlenmiştir. Başvuruya ayrıca dosya yüklenmesi gerekirse güncel TYBS talimatları izlenmelidir.
