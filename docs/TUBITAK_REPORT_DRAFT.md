# TÜBİTAK 2204-A Proje Raporu — Sonuçlarla Güncellenmiş Taslak

> **Durum:** Deneyler tamamlandı ve artifact'ler doğrulandı. Bu dosya, 2026–2027 resmî TÜBİTAK Proje Yazım Şablonu'na aktarılmak üzere hazırlanmış içerik taslağıdır; resmî Word şablonuna son aktarım, başvuru alanları ve PDF son kontrolü ayrıca yapılmalıdır. Sonuçlar dondurulmuş deney kayıtlarından alınmıştır. Doğrulayıcı deneyin birincil ölçütü taban etkisi göstermiştir; bu rapor CCDG'nin anlamsal olarak etkisiz olduğunu iddia etmez.

## Proje adı

**LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**

**Ana alan:** Yazılım  
**Tematik alan:** Dijital İkiz  
**Proje türü:** Kontrollü deneysel araştırma

## Proje özeti

Büyük dil modelleri (LLM), yazılım hatalarını açıklama ve kök nedenlerini belirleme amacıyla kullanılmaktadır. Ancak aynı hata kanıtlarının düz metin yerine bileşenler arasındaki ilişkileri açıkça gösteren yapılandırılmış bir bağımlılık grafiğiyle sunulmasının tanı doğruluğuna etkisi belirsizdir. Bu projede, Çapraz-Bileşen Bağımlılık Grafiği (Cross-Component Dependency Graph, CCDG) temsilinin Standard Context'e kıyasla kök neden teşhisine katkısı kontrollü olarak incelenmiştir. Deneylerde sabit bir Qwen2.5-3B-Instruct model checkpoint'i kullanılmış; dört gerçek yazılım hatası üzerinde 40 koşuluk pilot ve pilot vakalarından bağımsız 16 vaka üzerinde 160 koşuluk doğrulayıcı deney yürütülmüştür. Her vaka, Standard ve CCDG koşullarında beş sabit tohumla çalıştırılmış; aynı vaka iki koşulda eşleştirilmiş ve istatistiksel analiz birimi bağımsız yazılım vakası olarak tanımlanmıştır. Tüm 200 inference çıktısı ayrıştırılmış, ham çıktı hash'leri ve artifact dosya envanteri doğrulanmıştır. Dondurulmuş doğrulayıcı birincil ölçütü, her vaka için önceden belirlenmiş kök neden ifadelerinin açıklamada bitişik ifade olarak eşleşmesine dayanır. Bu ölçütte Standard 0/80, CCDG 0/80 geçiş üretmiş; 16 vakanın tamamı iki koşulda da başarısız sınıflandırılmış ve exact iki taraflı McNemar testi p=1,00 bulunmuştur. Bu sonuç, kullanılan eşleştiricinin taban etkisini göstermektedir; koşulların eşdeğerliğini veya CCDG'nin etkisizliğini kanıtlamaz. Araştırmanın anlamsal hipotezi bu operasyonelleştirmeyle çözümlenememiştir.

## Anahtar kelimeler

Büyük dil modelleri; yazılım hata teşhisi; kök neden analizi; CCDG; Defects4J.

## İçindekiler

1. [Giriş](#1-giriş)
2. [Amaç ve hipotezler](#2-amaç-ve-hipotezler)
3. [Yöntem](#3-yöntem)
4. [Bulgular](#4-bulgular)
5. [Tartışma](#5-tartışma)
6. [Sınırlılıklar](#6-sınırlılıklar)
7. [Sonuç ve öneriler](#7-sonuç-ve-öneriler)
8. [Yeniden üretilebilirlik ve kanıt kayıtları](#8-yeniden-üretilebilirlik-ve-kanıt-kayıtları)
9. [Kaynakça](#kaynakça)

## 1. Giriş

Büyük dil modelleri doğal dilde hata açıklama, kod üretme ve yazılım mühendisliği iş akışlarında giderek daha fazla araştırılmaktadır. Gerçek hata kayıtlarının kontrollü biçimde incelenmesi, modellerin yalnızca örnek kodlarda değil, gerçek yazılım projelerinde de hangi koşullarda başarılı olduğunu ölçmek için önemlidir. Defects4J, gerçek Java projelerinden alınan hata örnekleri ve hata düzeltme sürümleriyle kontrollü yazılım çalışmaları için bir veri kaynağı sağlamaktadır [1]. SWE-bench gibi çalışmalar ise gerçek GitHub sorunlarının çözümünde model performansını ölçmenin, bağlamı ve çok dosyalı değişiklikleri doğru anlamayı gerektirdiğini göstermektedir [2].

Kod temsillerinde yapısal bilginin kullanılması yeni bir fikir değildir. GraphCodeBERT, kodla ilişkili veri akışı bilgisini temsil öğrenimine dahil eden bir yaklaşım örneğidir [3]. CodeBERT ve kod üzerinde eğitilmiş büyük dil modellerinin değerlendirilmesine yönelik çalışmalar da kod anlama ve üretme görevlerinin ayrı değerlendirme gerektirdiğini vurgulamaktadır [4, 5]. Yazılım mühendisliği için LLM literatürünü inceleyen sistematik çalışmalar, görevler, veri kümeleri ve değerlendirme yöntemleri arasında önemli farklılıklar bulunduğunu raporlamıştır [6]. Qwen2.5 teknik raporu, bu araştırmada kullanılan model ailesinin mimari ve değerlendirme bağlamını açıklar; ancak tek başına bu projedeki CCDG hipotezini destekleyen doğrudan kanıt değildir [7].

İstemleme ve akıl yürütme çalışmaları, modelden istenen görev tanımının ve sunulan kanıtların çıktıları etkileyebileceğini göstermiştir [8, 9]. Modelin kendi çıktısını denetlemesi üzerine yapılan çalışmalar [10] ve dış bilgi kaynaklarını modele sağlayan retrieval-augmented generation yaklaşımı [11] da bağlamın ve doğrulama stratejisinin önemini gösterir; ancak bunlar CCDG etkisini doğrudan sınamaz. Bununla birlikte, bileşenler arası bağımlılıkların açık bir grafik olarak verilmesinin, aynı temel hata kanıtlarını kullanan standart bir bağlama göre kök neden teşhisini artırıp artırmadığı ayrı bir deneysel sorudur. Bu proje, genel LLM yetenekleri hakkında geniş bir iddia ileri sürmek yerine, tek bir sabit model ve belirli gerçek yazılım hataları üzerinde iki bağlam temsilini eşleştirilmiş bir tasarımla karşılaştırmaktadır.

**Araştırma sorusu:** Aynı yazılım hatasına ilişkin temel kanıtlar korunurken, bileşenler arası bağımlılıkların açık CCDG biçiminde sunulması LLM'nin kök neden teşhis doğruluğunu Standard Context'e göre artırır mı?

## 2. Amaç ve hipotezler

Araştırmanın amacı, açık ve yapılandırılmış çapraz-bileşen bağımlılık temsilinin LLM tabanlı hata teşhisine etkisini tekrarlanabilir bir deneyle ölçmektir.

- **H1 (araştırma beklentisi):** CCDG koşulu, Standard Context'e kıyasla vaka düzeyinde kök neden doğruluğunu artırır.
- **H0 (istatistiksel sıfır hipotezi):** Dondurulmuş doğrulayıcı ölçütte Standard ve CCDG koşullarının vaka düzeyindeki başarı olasılıkları arasında fark yoktur.

Birincil doğrulayıcı ölçüt, pilot sonrası ve doğrulayıcı inference başlamadan önce dondurulan vaka-özel kök neden alias eşleştiricisidir. Bu puanlama protokolü, pilot çıktılarından sonra ölçüm sorunu teşhis edilerek değiştirilmiştir. Bu nedenle nihai raporda ölçüt, tüm model çıktıları görülmeden önce kaydedilmiş gibi sunulmamaktadır. Önceki tam-teşhis puanı ve pilot verisi değiştirilmemiş; tam-teşhis ölçütü ikincil sonuç olarak korunmuştur.

## 3. Yöntem

### 3.1 Araştırma tasarımı

Aynı bağımsız yazılım vakası iki koşulda değerlendirilmiştir:

1. **Standard Context:** Hata ve bileşenler hakkında temel kanıtlar standart metinsel bağlamla sunulmuştur.
2. **CCDG Context:** Aynı temel kanıtlar korunarak, bileşenler ve aralarındaki bağımlılık ilişkileri açık ve yapılandırılmış bir grafik temsiliyle sunulmuştur.

Temel bağımsız değişken bağlamın temsil biçimidir. Model checkpoint'i, temel vaka kanıtları, sistem istemi, ana istem şablonu, tohumlar ve üretim ayarları sabit tutulmuştur. Ground truth iki deney koşulunun model bağlamlarına eklenmemiştir.

### 3.2 Veri ve vaka seçimi

Pilot deney dört gerçek Apache Commons Math / Defects4J hatasından oluşturulmuştur: MATH-927, MATH-950, MATH-949 ve MATH-988. Her pilot vakası iki koşulda beş sabit tohumla çalıştırılmıştır: **4 × 2 × 5 = 40 inference**.

Doğrulayıcı deney, pilot vakalarını içermeyen 16 bağımsız vakadan oluşmaktadır: CLOSURE-4, CLOSURE-6, CLOSURE-14, MATH-305, MATH-326, MATH-358, MATH-377, MATH-392, MATH-393, MATH-405, MATH-631, MATH-859, MATH-924, TIME-1, TIME-12 ve MOCKITO-19. Vaka seçimi model çıktılarından bağımsız olarak yapılmış; kaynak, düzeltme revizyonu, kök neden kanıtları, CCDG uygunluğu ve contamination (eğitim verisine sızma/maruziyet) riski kayıt altına alınmıştır. Doğrulayıcı deney **16 × 2 × 5 = 160 inference** olarak yürütülmüştür.

Seçilen tüm doğrulayıcı vakalar için kamuya açık olma kaynaklı contamination riski yüksek olarak etiketlenmiştir. Bu etiket, vakaların modelin eğitim verisinde kesinlikle bulunduğunu göstermez; yalnızca bu ihtimalin araştırma açısından bir sınırlılık olduğunu belirtir.

### 3.3 Model ve üretim ayarları

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

### 3.4 Ölçüm aracı ve vaka düzeyi karar

Her inference sonucu JSON formatında istenmiş ve ayrıştırılmıştır. Dondurulmuş doğrulayıcı birincil ölçüt, her vaka için kaynak kanıtları ve ground truth temel alınarak önceden yazılan kök neden alias ifadelerinden en az birinin `root_cause_class` ve `explanation` alanlarının birleştirilmiş metninde normalleştirme sonrası **bitişik ifade** olarak bulunmasına dayanır. Noktalama işaretleri ve boşluklar normalleştirilir; eş anlamlı olabilecek fakat alias ifadesiyle bitişik eşleşmeyen açıklamalar geçiş sayılmaz. Ayrıştırma veya şema hataları başarısız koşu olarak ele alınır.

Bir vaka-koşul bileşimi, beş tohumun en az üçünde birincil ölçütü geçtiğinde başarılı sayılır. Beş tohum bağımsız yazılım vakaları olarak sayılmamıştır; istatistiksel birim yazılım hatasıdır.

Bu ölçüt deterministik ve tekrarlanabilir olmakla birlikte semantik bir değerlendirici değildir. Anlamca doğruya yakın bir açıklamayı, sabit alias dizisi bitişik geçmediği için başarısız sayabilir. Bu sınırlılık, sonuçların yorumunda merkezi önemdedir.

### 3.5 Veri bütünlüğü ve tekrarlanabilirlik

Her kayıt model kimliği ve revizyonu, tohum, koşul, istem/bağlam hash'leri, ham çıktı hash'i, zaman damgaları ve ayrıştırılmış sonuçla ilişkilendirilmiştir. Deney kaynakları sabit Git commit'leri üzerinden paketlenmiştir. Pilot ve doğrulayıcı artifact'leri GitHub Actions'ta saklanmış; artifact içindeki dosya manifestleri dosya boyutu ve SHA-256 hash'leri üzerinden yeniden kontrol edilmiştir. Normal depo güncellemeleri deney çıktılarının üzerine yazmamıştır.

### 3.6 İstatistiksel analiz

Birincil karşılaştırma, aynı yazılım vakası için Standard ve CCDG koşullarından elde edilen ikili vaka düzeyi sonuçların eşleştirilmiş karşılaştırmasıdır. İki taraflı exact McNemar testi, α = 0,05 ile kullanılmıştır. Etki, CCDG başarısı eksi Standard başarısı olarak tanımlanan eşleştirilmiş risk farkıyla raporlanmıştır. %95 güven aralığı, iki uyumsuz sonuç oranı için Wilson skor aralıklarını kullanan önceden kayıtlı Newcombe-tipi yaklaşımla hesaplanmıştır.

Örneklem planlaması, doğrulayıcı sonuçlar görülmeden önce kaydedilen McNemar tasarım varsayımlarına dayanmıştır: P(Standard doğru, CCDG yanlış)=0,05 ve P(Standard yanlış, CCDG doğru)=0,60; hedef güç 0,80, α=0,05 ve 16 bağımsız vaka için hesaplanan güç yaklaşık 0,807'dir. Bu değerler tasarım varsayımlarıdır; gözlenen pilot veya doğrulayıcı sonuçlardan türetilmemiştir.

## 4. Bulgular

### 4.1 Çalıştırma ve bütünlük sonuçları

| Ölçüt | Pilot | Doğrulayıcı deney |
|---|---:|---:|
| Bağımsız vaka sayısı | 4 | 16 |
| Beklenen inference | 40 | 160 |
| Bulunan inference | 40/40 | 160/160 |
| JSON ayrıştırma hatası | 0 | 0 |
| Doğrulanan artifact dosyası | 55 | 212 |
| Eksik / fazla / hash'i uyuşmayan artifact dosyası | 0 | 0 |

Doğrulayıcı deney, GitHub Actions run ID `37976682761` üzerinde başarıyla tamamlanmıştır. Artifact ID `11640450681`, arşiv SHA-256 değeri `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd` şeklindedir. Bağımsız denetimde 212/212 dosya, 160/160 inference kaydı doğrulanmış; ham çıktı hash'lerinde uyuşmazlık ve beklenmeyen dosya bulunmamıştır. Bu kontroller çalıştırma ve veri bütünlüğünü doğrular; tek başlarına teşhis doğruluğunu kanıtlamaz.

### 4.2 Dondurulmuş birincil ölçüt

| Sonuç | Standard Context | CCDG Context |
|---|---:|---:|
| Inference kaydı | 80 | 80 |
| Ayrıştırma hatası | 0 | 0 |
| Alias ölçütünü geçen inference | 0/80 (%0) | 0/80 (%0) |
| 3/5 çoğunluk kuralıyla başarılı vaka | 0/16 (%0) | 0/16 (%0) |
| İkincil tam-teşhis geçişi | 0/80 (%0) | 0/80 (%0) |

Vaka düzeyindeki eşleştirilmiş tablo aşağıdadır.

|  | CCDG başarılı | CCDG başarısız |
|---|---:|---:|
| Standard başarılı | 0 | 0 |
| Standard başarısız | 0 | 16 |

Exact iki taraflı McNemar testi **p = 1,00** üretmiştir. Gözlenen eşleştirilmiş risk farkı (CCDG − Standard) **0,00**; hesaplanan %95 güven aralığı **[-0,1936; 0,1936]** olmuştur. Sıfır uyumsuz vaka vardır; bütün vakalar her iki koşulda da ölçüte göre başarısız sayılmıştır. Bu nedenle sıfır hipotezi reddedilememiştir.

### 4.3 Sonucun doğru yorumu

Birincil ölçütte iki koşulda da hiç geçiş olmaması, belirgin bir **taban etkisine** işaret eder. Bitişik ifade kuralı, aynı kavramı farklı kelimelerle açıklayan çıktıları başarısız sayabilir. Örneğin, bir çıktının hata akışını ve `UNCOND` / `ON_EX` kenar türleri arasındaki karışıklığı tarif etmesi, sabit alias ile tam ifade eşleşmesi üretmedikçe geçiş sayılmayabilir. Bu durum, ölçütün anlamsal doğruluğu tam olarak yansıtmadığını gösteren bir ölçüm sınırlılığıdır; tüm model cevaplarının doğru olduğunu göstermez.

Bu sebeple p=1,00 sonucu **koşulların eşdeğer olduğunun kanıtı değildir** ve **CCDG'nin etkisiz olduğunu kanıtlamaz**. Bulgular yalnızca, dondurulmuş literal-alias ölçütü altında fark tespit edilmediğini göstermektedir. Projenin asıl bilimsel sorusu olan CCDG'nin anlamsal kök neden teşhisini artırıp artırmadığı bu ölçüm aracıyla çözümlenememiştir.

### 4.4 Puanlama protokolü değişikliği

Pilot deneyden sonra, katı tam-teşhis puanlamasının doğal dildeki açıklama biçimlerini başarısız sayabileceği görüldüğünden, doğrulayıcı deneyin birincil ölçütü kaynak kanıtlarına dayalı sabit kök neden alias'larına dönüştürülmüştür. Değişiklik 9 Ekim 2026'da, doğrulayıcı çıktılar incelenmeden önce kayda alınmıştır; ancak pilot çıktıları puanlama sorununun teşhisi için görülmüştür. Bu nedenle bu karar, bütün model çıktıları görülmeden önce eksiksiz biçimde ön kayıt yapılmış bir karar olarak sunulmamaktadır. Vaka seçiminin model çıktılarından bağımsız olduğu ve alias ifadelerinin model çıktılarından türetilmediği kaydedilmiştir. Pilot değerlendirmesi ve doğrulayıcı sonuçlar sonradan değiştirilmemiştir.

## 5. Tartışma

Bu araştırmanın güçlü yönleri, iki koşulun aynı vakalar üzerinde karşılaştırılması, tohumların bağımsız vaka sayılmaması, model revizyonunun sabitlenmesi, ground truth'un model bağlamlarından çıkarılması ve çıktıların hash'lerle doğrulanmasıdır. Araştırma aynı zamanda ölçüm aracının deney sonucunu nasıl sınırlayabileceğini ortaya çıkarmıştır: ölçüt tutarlı biçimde uygulanmış ve denetlenebilir olmasına karşın, bitişik ifade eşleşmesini anlamsal doğruluğun vekili olarak kullanması olası yanlış negatifler üretmektedir.

Sonuç, CCDG lehine istatistiksel kanıt sağlamamaktadır; ancak birincil ölçütün tüm vakaları başarısız sınıflandırması nedeniyle CCDG aleyhine güvenilir bir etkisizlik sonucu da sağlamamaktadır. Anlamsal soruyu sınamak için yeni bir doğrulayıcı deneyden önce, skorlayıcının insan uzmanlar tarafından körlenmiş koşullarda test edilmesi, eşanlamlı/parafraz vakalarının önceden tanımlı kurallarla puanlanması ve yeni bağımsız vaka örnekleminin sonuçlara bakılmadan önce kaydedilmesi gerekir. Bu mevcut 160 çıktının sonradan yeniden puanlanması halinde yapılacak değerlendirme yalnızca keşfedici (exploratory) sayılmalı; değiştirilen puanlar mevcut doğrulayıcı sonuç gibi sunulmamalıdır.

## 6. Sınırlılıklar

1. **Ölçüm aracı:** Sabit alias'ın bitişik ifade eşleştirmesi semantik değerlendirme değildir; parafrazları kaçırabilir.
2. **Taban etkisi:** Birincil ölçütte tüm vakaların başarısız olması farkları gözlemlemeyi engellemiştir.
3. **Örneklem:** Doğrulayıcı örneklem 16 yazılım hatası ve belirli açık kaynak Java projeleriyle sınırlıdır; tüm diller, hata türleri veya modeller için genellenemez.
4. **Contamination riski:** Vakalar kamuya açık olduğundan eğitim verisine geçmiş olma olasılığı vardır; bu üyelik doğrudan doğrulanmamıştır.
5. **Anotasyon:** CCDG kenarlarının ve ground truth'un hazırlanmasında insan yorumundan kaynaklanan hata riski vardır.
6. **Puanlama protokolü kronolojisi:** Birincil ölçüt pilot sonrası değiştirilmiş ve bu değişiklik kayda alınmıştır. Bu nedenle ön kayıt sınırlılığı açıkça belirtilmelidir.
7. **Model kapsamı:** Sonuçlar yalnızca sabitlenen Qwen2.5-3B-Instruct checkpoint'i, FP16 yüklemesi, istemleri, ayarları ve seçilen vaka havuzu bağlamında geçerlidir.

## 7. Sonuç ve öneriler

Pilot ve doğrulayıcı deneylerin teknik çalıştırması tamamlanmış; 40 pilot ve 160 doğrulayıcı inference kaydı, JSON ayrıştırma ve artifact hash kontrolleriyle doğrulanmıştır. Dondurulmuş doğrulayıcı birincil alias ölçütünde Standard ve CCDG koşullarının ikisi de 0/80 geçiş göstermiş; 16 vakanın tamamı iki koşulda da başarısız sınıflandırılmıştır. Exact iki taraflı McNemar sonucu p=1,00 ve gözlenen risk farkı 0,00'dır.

Bu bulgu, CCDG'nin anlamsal teşhiste yararsız olduğu ya da iki yöntemin eşdeğer olduğu şeklinde yorumlanamaz. Ölçüt taban etkisi göstermiştir ve araştırmanın anlamsal hipotezini cevaplayamamıştır. Bilimsel olarak savunulabilir sonuç, test edilen operasyonelleştirmede fark tespit edilmediğini ve daha geçerli bir ölçüm aracına ihtiyaç bulunduğunu belirtmektir. Sonraki çalışma, ölçütü bağımsız uzmanlarca doğrulama ve yeni vaka örnekleminde yeni bir doğrulayıcı protokolü önceden kaydetme üzerine kurulmalıdır.

## 8. Yeniden üretilebilirlik ve kanıt kayıtları

- Depo: https://github.com/MahmutVezir/dijitalikiz
- Pilot çalıştırma: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402
- Doğrulayıcı çalıştırma: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37976682761
- Pilot kaynak commit: `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`
- Doğrulayıcı kaynak commit: `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`
- Doğrulayıcı artifact ID: `11640450681`
- Doğrulayıcı artifact SHA-256: `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`
- Sonuç özeti: `data/benchmark/confirmatory_result_summary.json`
- Ayrıntılı sonuç ve bağımsız denetim: `docs/CONFIRMATORY_RESULTS_2026-10-09.md`, `scripts/audit_confirmatory_artifact.py`
- Skorlama değişikliği: `docs/CONFIRMATORY_SCORING_PROTOCOL.md`

## Kaynakça

[1] Just, R., Jalali, D., & Ernst, M. D. (2014). Defects4J: A Database of Existing Faults to Enable Controlled Testing Studies for Java Programs. *Proceedings of the International Symposium on Software Testing and Analysis (ISSTA)*. https://doi.org/10.1145/2610384.2628055

[2] Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? *International Conference on Learning Representations (ICLR)*. https://arxiv.org/abs/2310.06770

[3] Guo, D., Ren, S., Lu, S., Feng, Z., Tang, D., Liu, S., et al. (2021). GraphCodeBERT: Pre-training Code Representations with Data Flow. *International Conference on Learning Representations (ICLR)*. https://arxiv.org/abs/2009.08366

[4] Feng, Z., Guo, D., Tang, D., Duan, N., Feng, X., Gong, M., et al. (2020). CodeBERT: A Pre-Trained Model for Programming and Natural Languages. https://arxiv.org/abs/2002.08155

[5] Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. de O., Kaplan, J., et al. (2021). Evaluating Large Language Models Trained on Code. https://arxiv.org/abs/2107.03374

[6] Hou, X., Zhao, Y., Liu, Y., Yang, Z., Wang, K., Li, L., et al. (2024). Large Language Models for Software Engineering: A Systematic Literature Review. *ACM Transactions on Software Engineering and Methodology, 33*(8), Article 220. https://doi.org/10.1145/3695988

[7] Qwen Team. (2024). Qwen2.5 Technical Report. https://arxiv.org/abs/2412.15115

[8] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/2201.11903

[9] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. *International Conference on Learning Representations (ICLR)*. https://arxiv.org/abs/2210.03629

[10] Chen, X., Lin, M., Schärli, N., & Zhou, D. (2023). Teaching Large Language Models to Self-Debug. https://arxiv.org/abs/2304.05128

[11] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems (NeurIPS)*. https://arxiv.org/abs/2005.11401
