# Anlamsal Kök Neden Puanlama Protokolü — Keşifsel Yeniden İnceleme

**Tarih:** 2026-10-09  
**Durum:** Protokol ve kör inceleme paketi hazır; puanlar henüz toplanmadı.  
**Kapsam:** Mevcut 160 doğrulayıcı çıktı için bağımsız, koşul-kör anlamsal inceleme ve gelecekteki doğrulayıcı deneyin tasarımı.

## 1. Değiştirilemeyecek mevcut sonuç

Mevcut doğrulayıcı deneyin dondurulmuş birincil sonucu aynen korunur: literal alias eşleştirmesinde Standard 0/80, CCDG 0/80; 16 vakanın hiçbirinde 3/5 çoğunluk başarısı yoktur; exact iki taraflı McNemar p=1,00'dır. Bu, ölçütün taban etkisidir; eşdeğerlik veya CCDG'nin etkisizliği kanıtı değildir. Bu dosya, dondurulmuş skoru değiştirmek için yetki vermez.

Çalışma ekibi model çıktılarının bir bölümünü zaten gördüğünden ve bu inceleme deney tamamlandıktan sonra planlandığından, mevcut çıktılara uygulanacak anlamsal puanlama **keşifseldir**. Sonuç CCDG lehine görünse dahi, mevcut deneyin önceden dondurulmuş doğrulayıcı sonucu gibi sunulamaz.

## 2. Mevcut çıktılar için puanlama protokolü

### 2.1 Körleme

- İncelemeciye yalnızca rastgele review_id, ilgili referans vakanın kodu ve modelin ürettiği teşhis alanları verilir.
- Koşul (standard/ccdg), seed, istem, kaynak commit'i ve çalıştırma zamanı gizlenir.
- Çıktılar her incelemeci için ayrı sırada sunulur.
- İncelemeciler birbirleriyle görüşmeden önce kendi puanlarını tamamlar; dış kaynaklardan vaka aramazlar.
- Çalışma sahibi koşulları biliyor olsa da, bağımsız incelemeciler koşul anahtarını görmez. Dolayısıyla bu, çalışma ekibinin bütünüyle kör olduğu anlamına gelmez.

### 2.2 Birincil anlamsal ölçüt

Yalnızca **kök nedenin semantik doğruluğu** değerlendirilir. Akıcı anlatım, uzunluk, kendinden emin ton, sınıf adını bilmek veya yalnızca semptomu tekrarlamak tek başına doğru puanı getirmez. Referans vaka, kaynak/ground-truth kayıtlarından oluşturulur; model yanıtındaki birebir metin eşleşmesi şart değildir.

Her çıktı şu üç düzeyden biriyle puanlanır:

- **2 — Doğru:** Esas nedensel mekanizmayı ground truth ile aynı biçimde tanımlar; uygun anlam eşdeğerleri kabul edilir.
- **1 — Kısmen doğru:** İlgili bileşeni veya semptomu tanır ya da mekanizmanın bir parçasını doğru söyler; ancak temel bir nedensel unsuru atlar veya maddi olarak yanlış ifade eder.
- **0 — Yanlış:** Çelişkili/yanlış bir mekanizma verir, ilgisiz bir neden ileri sürer veya referansla ilişkilendirilemeyecek kadar belirsiz kalır.

Birincil anlamsal ikili sonuçta yalnızca **2 puan** başarılı sayılır. 1 puanlık kısmi doğruluk ayrı bir ikincil betimsel ölçüttür. Boş/işe yaramaz çıktı 0 olarak puanlanır. Değerlendirme, yalnızca belirtilen kök neden iddiasına odaklanır; bileşen, etkilenen varlık, işlem ve bağımlılık ilişkileri ikincil alanlardır.

### 2.3 İncelemeciler ve anlaşmazlıklar

Tercih edilen düzen iki bağımsız incelemeci ve anlaşmazlıklar için koşul-kör üçüncü bir hakemdir. Ham anlaşma oranı ve üç düzeyli puanlar için Cohen ağırlıklı kappa raporlanır. Hakemlik sonrası puan birincil anlamsal ikili metriğe dönüştürülür. Üçüncü incelemeci bulunmuyorsa, uzlaşmayla verilen puan bağımsız hakemlikmiş gibi sunulmaz; iki ilk puan da korunur ve bu sınırlılık açıklanır.

Tek bir AI/araştırmacı değerlendirmesi, yararlı ön tarama olabilir; ancak bağımsız puanlama, gözlemciler arası güvenirlik veya doğrulayıcı kanıtın yerine geçmez.

### 2.4 Vaka düzeyi analiz

Her vaka-koşul için beş seed'in en az üçünde puan 2 alınırsa o koşul başarılı sayılır. İstatistiksel birim seed değil, bağımsız yazılım vakasıdır. Keşifsel yeniden incelemede Standard ve CCDG vaka sonuçları eşleştirilir; iki taraflı exact McNemar testi, eşleştirilmiş risk farkı ve %95 güven aralığı raporlanır. 16 vakanın her biri için iki koşulun sonucu da gösterilir; yalnızca p-değeri sunulmaz.

Sonuçlar, mevcut dondurulmuş alias skoru ile yan yana raporlanır. İki ölçüt birbirinin yerine geçirilmez ve literal skor geriye dönük düzeltilmez.

## 3. Mevcut incelemenin yorumlanması

- Anlamsal puanlama CCDG lehine fark gösterirse: mevcut koşul-kör tekrar puanlama keşifsel bulgu olarak raporlanır; hipotez için bağımsız doğrulama gerekir.
- Fark göstermezse: hipotez mevcut örnek ve model ayarlarında desteklenmemiş olur; yine de yalnızca bu küçük örneklemden evrensel etkisizlik çıkarılmaz.
- Standard koşulu daha başarılı çıkarsa: sonuç saklanmaz veya puanlama kuralı değiştirilmez; CCDG varsayımı bu veriyle desteklenmemiş olarak raporlanır.
- İncelemeciler arasında yüksek anlaşmazlık çıkarsa: bu da ölçüm aracının ek kalibrasyon gerektirdiğine dair önemli bir sonuçtur; yalnızca istenen hipotez sonucunu üretmek için kararlar yeniden yazılmaz.

## 4. Yeni bir doğrulayıcı deney için zorunlu koşullar

1. Mevcut 4 pilot ve 16 doğrulayıcı vaka yeni doğrulayıcı birincil örnekleme tekrar dahil edilmez.
2. Yeni vakaların kök nedenleri, düzeltmeleri, CCDG ilişkileri ve kaynak kanıtları model çıktıları görülmeden doğrulanıp dondurulur.
3. Vaka başına beklenen nedensel mekanizma ve kabul edilebilir anlam eşdeğerleri, inference öncesinde yazılır. Ölçüm rubriği, ayrı ve bağımsız kalibrasyon vakalarında denenir; rubrik ve hakemlik prosedürü yeni doğrulayıcı inference başlamadan önce dondurulur.
4. Mümkünse en az iki uzman puanlayıcıyla pilot/kalibrasyon verisinde önceden belirlenmiş bir anlaşma eşiği doğrulanır. Eşik karşılanmazsa rubrik kalibrasyon verisi üzerinde iyileştirilir; doğrulayıcı çıktılara bakılarak değiştirilmez.
5. Yeni vaka sayısı, makul ve ihtiyatlı eşleştirilmiş etki varsayımlarıyla yeni bir güç analizi üzerinden belirlenir. Önceki 16 vakalık tasarımın çok büyük CCDG etkisi varsayımı otomatik olarak tekrar kullanılmaz.
6. Model checkpoint/revision, sistem istemi, üretim ayarları, koşullar, vaka listesi, puanlama rubriği, dışlama kuralları ve analiz planı önceden kaydedilir.
7. Tamamlandıktan sonra sonuç ne olursa olsun raporlanır. Protokol sapmaları tarih ve gerekçeleriyle açıklanır.

## 5. Hipotez hakkında izin verilen sonuç dili

Şu an için doğru ifade: **“Dondurulmuş literal alias ölçütüyle CCDG lehine bir fark gözlenmedi; ölçütün taban etkisi nedeniyle anlamsal araştırma hipotezi çözümlenmedi.”**

Mevcut yeniden inceleme CCDG'yi desteklese bile doğru ifade: **“Koşul-kör anlamsal tekrar puanlama, CCDG lehine keşifsel kanıt sundu; bu bulgu bağımsız yeni vakalar üzerinde önceden dondurulmuş bir puanlama protokolüyle doğrulanmalıdır.”**

Yalnızca yeni, uygun biçimde önceden dondurulmuş doğrulayıcı deney sonuçları hipotezin doğrulandığı iddiasına dayanak olabilir. Pozitif sonuç üretmek için eşikler, vaka seçimi veya puanlama sonucu görüldükten sonra değiştirilmez.


## 6. Yöntemsel kaynaklar

Bu protokol, tek bir otomatik hakemi kesin doğruluk ölçütü olarak kabul etmez. Yazılım mühendisliği çıktılarında LLM-as-a-judge yaklaşımlarını insan puanlarıyla karşılaştıran 2025 tarihli bir çalışma, hakem model performansının göreve göre değiştiğini ve bazı görevlerde klasik metrikleri aşamadığını bildirir ([Wang ve diğerleri, 2025](https://doi.org/10.1145/3728963)). Bu nedenle burada bağımsız puanlayıcılar, körleme ve puanlayıcılar arası anlaşmanın raporlanması tercih edilir.

Önceden kayıt ilkeleri için OSF rehberi; hipotez, ölçüt, örneklem ve karar kurallarının veriler incelenmeden önce açık biçimde belirlenmesini önerir ([OSF: Effective Practices for a Rigorous Preregistration](https://help.osf.io/article/330-welcome-to-registrations)). Bu rehber doğrultusunda mevcut yeniden puanlama keşifsel olarak etiketlenmiştir; ileriye dönük deneyin ölçüm ve analiz kararları yeni inference başlamadan önce dondurulmalıdır.

Yazılım mühendisliği araştırmaları için topluluk standartları: [ACM SIGSOFT Empirical Standards](https://www2.sigsoft.org/EmpiricalStandards/).
