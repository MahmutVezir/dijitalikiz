# TÜBİTAK 2204-A 2027 — Tematik Alan ve Araştırma Kapsamı Kararı

**Karar tarihi:** 15 Ekim 2026  
**Karar:** **Ana alan: Yazılım; önerilen tematik alan: Yapay Zekâ.**  
**Güven düzeyi:** Yüksek, mevcut araştırma kapsamı ve resmî rehber tanımı açısından. Başvuru öncesinde güncel TYBS alan seçenekleri öğrenci ve danışman tarafından son kez doğrulanmalıdır.

## 1. Karar özeti

Mevcut araştırma, sabit bir büyük dil modeliyle yazılım hatası kök-neden teşhisi görevinde bağlam/bağımlılık gösterim biçimlerinin etkisini deneysel olarak karşılaştırıyor. Projede bir CCDG (Cross-Component Dependency Graph) yazılım bileşenleri ve bağımlılıkları açık bir yapı olarak temsil eder. Bu, yazılım mimarisinin dijital bir modelini oluşturabilir; ancak tek başına TÜBİTAK'ın Dijital İkiz tanımını karşılamaz.

TÜBİTAK'ın resmî 2026–2027 rehberinde Dijital İkiz; fiziksel bir varlık, sistem veya süreçle eşleşen sanal kopya olarak açıklanır. Modelin gerçek zamanlı sensör verileriyle sürekli güncellenmesi, performans izlemesi, analiz, olası sorunları tahmin etme ve optimizasyon amaçları vurgulanır. Mevcut çalışmamız ise sabitlenmiş, geçmişe ait hata kayıtları, kod revizyonları ve statik bağımlılık temsilleri üzerinden yürütülüyor; canlı sistem telemetrisiyle sürekli güncellenen ikiz kurmuyor.

Resmî kaynaklar:
- [TÜBİTAK 2204-A yarışma sayfası ve 2026–2027 çağrısı](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi)
- [2027 Proje Rehberi — Dijital İkiz bölümü, basılı s. 16; Yapay Zekâ bölümü, basılı s. 45](https://tubitak.gov.tr/sites/default/files/2026-09/lise_proje_rehberi_2027_onaya_sunulan.pdf)

## 2. Araştırmanın bugünkü bilimsel kapsamı

Mevcut başlık korunabilir:

**LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**

Araştırmanın ana sorusu, aynı temel hata kanıtlarının standart metinsel bağlamda veya açık çapraz-bileşen bağımlılık temsiliyle sunulmasının LLM'nin kök neden teşhisine etkisidir. Bu, esasen yazılım mühendisliği ve doğal dil işleme/muhakeme kullanan bir yapay zekâ değerlendirme çalışmasıdır. Model eğitimi/öğrenmesi araştırmanın merkezinde olmadığı için “Makine Öğrenmesi” de otomatik olarak en doğru alan sayılmamalıdır; kullanılan LLM ve muhakeme görevi bakımından “Yapay Zekâ” daha doğrudan eşleşir.

CCDG'nin statik kullanımı yazılım sistemi hakkındaki yapısal modelleme ile kavramsal olarak ilişkilidir. Bununla birlikte, “dijital ikiz” terimini yalnızca grafik veya dijital model bulunduğu için kullanmak, modelin güncellenmesi ve gerçek sistemle bağlantısı hakkında kanıtsız bir iddia olur.

## 3. Üç yaklaşımın karşılaştırılması

Değerlendirme, finalistlik garantisi veya varsayılan puan tahmini değil; resmî tanıma uyum, mevcut kanıtlar, uygulanabilirlik ve yöntemsel risk karşılaştırmasıdır.

| Ölçüt | A — Dijital İkiz temasını korumak | B — Gerçek yazılım dijital ikizi kurarak araştırmayı geliştirmek | C — Yazılım / Yapay Zekâ alanına geçmek |
|---|---|---|---|
| Mevcut resmî tanıma uyum | Düşük | İkiz gerçek zamanlı veriyle güncellenirse yüksek olabilir | Yüksek |
| Mevcut deneyle süreklilik | Yüksek, fakat tema iddiası zayıf kalır | Orta-düşük; araştırma sorusu ve sistem kapsamı değişebilir | Yüksek |
| Özgünlük potansiyeli | CCDG tek başına dijital ikiz kanıtı değildir | Potansiyel olarak yüksek; dinamik model ve doğrulanmış kestirim gerekir | Deney tasarımının bilgi-paritesi ve ölçüm sorunlarını çözmesiyle anlamlı |
| Veri ve sistem gereksinimi | Şu anki sabit vakalar yeterli tema kanıtı sağlamaz | Yüksek: canlı telemetri, sürüm eşleme, durum güncellemesi, test/olay akışı | Orta-yüksek: güvenilir vakalar, geçerli ölçüm aracı ve kontrollü çıkarım |
| 4 Kasım iç hedefine uygulanabilirlik | Teknik olarak kolay, kavramsal risk yüksek | Düşük; yeni altyapı ve doğrulama gerektirir | En yüksek; mevcut çalışmayı korur ve kritik deney kapılarına odaklanır |
| En büyük risk | Tema uyumsuzluğunu yalnızca anlatımla örtmeye çalışmak | Zaman baskısıyla yüzeysel bir “ikiz” kurup bilimsel hedefi dağıtmak | Ölçüm aracının taban etkisi ve mevcut deneyin bilgi-paritesi sınırlılığını çözmeden kalmak |
| Jüri önünde savunulabilirlik | Statik grafik ile dijital ikiz arasındaki fark nedeniyle zayıf | Ancak gerçek güncelleme ve doğrulama kanıtı varsa güçlü olabilir | Gerçek çalışma kapsamı ve kanıtlarla daha doğrudan uyumlu |

### A — Aynı temada devam

Bu yaklaşım önerilmemektedir. Statik CCDG modelini dijital ikiz olarak yeniden adlandırmak bilimsel açığı kapatmaz. Mevcut araştırmanın temaya uyumunu olduğundan güçlü göstermemeliyiz.

### B — Yazılım sisteminin gerçek dijital ikizini kurmak

Gelecekte ayrı bir araştırma olarak değerlendirilebilir. Asgari olarak gerçek bir yazılım deposu/sistemiyle eşlenen, sürüm ve bileşen durumunu tutan, CI/test/çalışma telemetrisi geldikçe güncellenen, hata yayılımını veya riskini analiz eden bir sanal model gerekir. Modelin güncelleme doğruluğu ve sorun kestirimi ayrıca ölçülmelidir. Bu, birkaç görselleştirme eklemek değildir; güncel araştırmanın deneysel sorusunu ve altyapısını genişletir. Zaman kısıtı içinde tarihsel LLM deneyini bu projeye dönüştürmek, iki hedefi de yüzeysel bırakma riski taşır.

### C — Temayı araştırmanın gerçek kapsamına göre seçmek

**Önerilen seçenek budur.** Yazılım ana alanını koruyup Yapay Zekâ tematik alanını seçmek; LLM tabanlı teşhis, doğal dil işleme/muhakeme ve kontrollü model değerlendirmesiyle doğrudan ilişkilidir. Bu karar, yarışma şansını artıracağı varsayımıyla değil, araştırma içeriğini en az çarpıtan sınıflandırma olduğu için verilmektedir.

TÜBİTAK yarışma sayfası ana alan ve tematik alan seçiminin proje içeriğine göre yapılması gerektiğini ve başvuru tamamlandıktan sonra değiştirilemeyeceğini belirtiyor. Bu nedenle seçim TYBS'de başvuru gönderilmeden önce öğrenci ve danışman tarafından kontrol edilmelidir.

## 4. Bu kararı değiştirecek asgari bilimsel kanıt ne olurdu?

Dijital İkiz temasında kalmak için yalnızca bir CCDG şeması yeterli değildir. Aşağıdakiler araştırmanın asli çıktısı olmalıydı:

1. Belirli bir yazılım sisteminin bileşenleri, sürümleri ve bağımlılıkları gerçek sistemle izlenebilir biçimde eşlenmeli.
2. Gerçek CI/test/çalışma telemetrisi veya olay verileri geldikçe dijital model otomatik ve zaman damgalı şekilde güncellenmeli.
3. Dijital modelin canlı sistem durumunu ne ölçüde doğru temsil ettiği test edilmeli.
4. Hata kestirimi veya etki analizi, tanımlanmış karşılaştırma yöntemiyle değerlendirilmeli ve sonuçları gerçek olay kanıtlarıyla doğrulanmalı.

Bunlar yapılmadığı sürece rapor, mevcut çalışmayı Dijital İkiz olarak sunmamalıdır.

## 5. Bilimsel çekirdekte yapılacak yüksek etkili işler

Tema kararından bağımsız olarak, mevcut çalışmanın en kritik eksikleri yöntemsel niteliktedir:

- Tarihsel 40 kayıtlık pilot ve 160 kayıtlık doğrulayıcı çalışma ile artefakt bütünlüğü sonucu dondurulmuş kalacak.
- Tarihsel birincil puan Standard 0/80 ve CCDG 0/80 olarak raporlanacak. (p=1{,}00) taban etkisinin sonucudur; eşdeğerlik veya etkisizlik kanıtı değildir.
- Standard ve CCDG koşullarındaki temel bilgi farkı düzeltilecek; gelecekteki üç koşullu tasarımda önceden belirlenmiş birincil karşılaştırma aynı bilgiyi farklı temsil biçimlerinde sunan koşullar arasında yapılacak.
- Yeni model çıkarımından önce puanlama aracı, bağımsız vaka kaynakları, iki bağımsız değerlendirici ve hakemleme, prompt/token uzunluğu, model/runtime uyumluluğu, güç planı ve analiz manifesti dondurulacak.
- Bağımsız inceleme veya kalibrasyon kanıtı yoksa gate kapalı kalacak; tarihsel çıktılar yeni ölçüte göre puanlanırsa bu analiz keşifsel olarak işaretlenecek.
- Yapay zekâ destekli bir hata teşhis prototipi ancak doğrulanmış bulgular onu anlamlı kılıyorsa geliştirilecek; arayüz, ürünleştirme veya model eğitimi araştırma sorusunun önüne geçirilmeyecek.

## 6. Son karar

Mevcut proje için tercih **C: Ana alan Yazılım, tematik alan Yapay Zekâ**. Mevcut başlık ve ana araştırma sorusu korunabilir; Dijital İkiz iddiası rapordan çıkarılmalı. Eğer ileride gerçek sistem telemetrisiyle sürekli güncellenen yazılım dijital ikizi oluşturulursa, bu çalışma ayrı ve doğrulanabilir hedefleri bulunan yeni/ek bir araştırma olarak ele alınmalıdır.

Bu karar, bölge veya Türkiye finaline kalma garantisi değildir. Rekabetçi bir başvuru için daha önemli olan; araştırma sorusunun açıklığı, yöntem yeterliliği, özgün katkının gerçek kanıtı, sonuçların tekrarlanabilirliği ve öğrencinin projeyi bağımsız açıklayabilmesidir.

## 7. Takvim

- **4 Kasım 2026 iç hedefi:** tarihsel çalışmanın bilimsel anlatımını ve rapor ilk sürümünü tamamlamak; yeni deney için yalnızca başarıyla geçilmiş doğrulama kapılarını kullanmak.
- **Resmî son başvuru:** 4 Ocak 2027, saat 17.30 (Türkiye saati). Son tarih, güncel TÜBİTAK 2204-A yarışma sayfasında yayımlanmıştır.
