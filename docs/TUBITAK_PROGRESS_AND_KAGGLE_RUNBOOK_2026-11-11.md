# TÜBİTAK 2204-A — proje durumu ve çalışma planı
**Denetim tarihi:** 11 Kasım 2026  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

## 1. TÜBİTAK'a göre sınıflandırma

- **Ana alan:** Yazılım
- **Tematik alan önerisi:** Yapay Zekâ
- **Önerilen başlık:** *Yazılım Hata Tanısında Yapay Zekânın Kanıta Dayalı Cevap Vermeme Yeteneği*

Bu seçim, projenin yazılım hata tanısı için bir yapay zekâ yönteminin güvenilirliğini deneysel olarak incelemesinden kaynaklanır. “Dijital İkiz” teması yalnızca depo adında bulunuyor diye seçilmemelidir; bu çalışmanın asıl araştırma nesnesi dijital ikiz modelleme değil, yetersiz kanıtta tanı üretme/üretmeme davranışıdır. 2027 rehberi “Yazılım” ana alanını ve “Yapay Zekâ” tematik alanını ayrı ayrı listeler. Ana alan ve tema, projenin nihai amacına göre seçilmelidir.

## 2. Araştırma problemi ve soru

**Problem:** Yazılım hatası tanısında bir yapay zekâ modeli, verilen hata raporu veya kod parçacığı kök nedeni belirlemek için yetersiz olduğunda yine de kesin bir tanı üretebilir. Bu yanıt tesadüfen doğru çıksa bile, sunulan kanıt tarafından desteklenmiyorsa güvenilir bir teşhis değildir.

**Araştırma sorusu:** Aynı büyük dil modeli, aynı vaka ve aynı kanıt içeriği üzerinde çalıştırıldığında, seçici cevap vermeme politikası yetersiz kanıtta kanıtsız kesin kök neden iddialarını zorunlu cevap politikasına kıyasla azaltır mı; bunu yaparken yeterli kanıtta doğru ve kanıt destekli cevap kapsamasını ne kadar korur?

**Temel ayrım:** “Doğru tahmin” ile “kanıtla desteklenen tanı” ayrı ölçülür. Değerlendirici, modelin tahmininin sonradan doğru çıkmasına bakarak eksik kanıttan yapılmış iddiayı kanıt destekli saymamalıdır.

## 3. Önceden tanımlı deney tasarımı

Mevcut Stage 3 manifestindeki tasarım şu şekildedir:

- Sabit model adayı: `Qwen/Qwen2.5-3B-Instruct`
- Model ve tokenizer revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`
- Çözümleme: `do_sample=false`, `temperature=0`, en fazla 512 yeni token; runtime doğrulaması henüz yapılmadı.
- Vaka hedefi: 80 bağımsız vaka; doğrulayıcı analiz için asgari 60 kabul edilmiş vaka; en az 8 ayrı upstream proje.
- Her vaka için altı koşul: E1 yeterli / E2 kısmi / E3 yetersiz kanıt × P0 zorunlu tanı / P1 seçici cevap vermeme.
- 80 vakada 480; 60 vakada 360 model çıktısı oluşur.

**Birincil sonuç:** E3 koşulunda kanıtsız kesin tanı oranının P0 ve P1 arasında vaka bazında eşleştirilmiş farkı. Planlanan karşılaştırma iki yönlü exact McNemar testi ve güven aralıklarıdır.

**İkincil sonuçlar:** E1 koşulunda gereksiz cevap vermeme oranı, kanıt destekli doğru cevap kapsaması, E2 koşulundaki belirsiz cevap davranışı, seçicilik/risk-kapsama dengesi ve güven puanı kalibrasyonu. Modelin kendi beyan ettiği güven tek başına gerçek kanıt yeterliliği kabul edilmemelidir.

**Değerlendirme ilkesi:** Kök neden ve buggy/fixed test doğrulaması yapan panel, model yanıtlarını görmemelidir. Kanıt seviyelerini ve model çıktılarını puanlayan ikinci panel de ilk panelden bağımsız olmalıdır. Panel üyeleri için önceden yazılmış rubrik, örneklerle kalibrasyon, uyuşmazlık/adjudikasyon kuralı ve körleme kaydı tutulmalıdır.

## 4. Bugünkü doğrulanmış durum

| Kontrol | Durum |
|---|---|
| Tek özel GitHub kaynak deposu | Hazır: `MahmutVezir/dijitalikiz` |
| BugsInPy pinned revision ve V11 metadata dondurma | Hazır, fakat V11 adayları artık yalnızca teknik tarihçe |
| V11 teknik vaka paketleri | 8 arşivin bütünlük kontrolü geçti |
| V11 buggy-fail/fixed-pass teknik sinyali | 5 vaka |
| V11 ortam/kurulum engeli | 3 vaka |
| V11 vakalarının doğrulayıcı örnekleme uygunluğu | Hayır; sekizinin tamamı kalıcı olarak dışlandı |
| Önceki maruziyet sicili hatası | Bulundu ve 105 kimlikli yeni birleşimle düzeltildi |
| Kabul edilmiş doğrulayıcı vaka | 0 |
| İki bağımsız panel ve kalibrasyon | Tamamlanmadı |
| Ön kayıt | Taslak; URI ve hash dondurma yok |
| Model runtime doğrulaması | Yapılmadı |
| Model inference | Yapılmadı; kapı kapalı |

Önemli: V11'in “workflow success” durumu testlerin tümünün başarılı olduğu anlamına gelmez. Beş teknik çift ve üç ortam blokajı birbirinden ayrılmıştır. V11 paketleri araştırma altyapısını geliştirmek için kullanıldığından hiçbirini doğrulayıcı analize taşımıyoruz.

## 5. Sonraki teknik adımlar

1. **Dışlama kaydını kullan:** Yeni vaka seçimi için yalnızca `EXPOSURE_UNION_2026-11-11.json` kullanılmalı. Eski 97-ID dosyası tarihsel kaynak olarak değişmeden kalır. Yeni birleşim 105 kimlik içerir; Black-9'un önceki maruziyet kaydında bulunup 97-ID listede atlanmış olması açıkça kayda geçirilmiştir.
2. **V12 metadata intake:** Pinned BugsInPy envanterini yeniden oluştur, 105 kimlikli birleşimi uygula, en az sekiz upstream projeyi koruyan yeni metadata cohort'u üret ve hash'lerini commit etmeden test başlatma.
3. **Ortam sorunlarını doğrula:** Luigi paket kurulumu, Pandas GCC bayrağı ve Matplotlib eski NumPy/easy_install engelini yeni, maruziyetsiz adaylarda değil; ayrılmış teknik test fixture'larında düzelt. V11 vakalarının kendisini tekrar çalıştırıp confirmatory adayı hâline getirme.
4. **Bilimsel kabul paneli:** Yeni adayların lisans/provenance, buggy-fail/fixed-pass, gerçek kök neden, testin hedeflenen hatayı ölçmesi, Python runtime eşleşmesi, kanıt seviyeleri ve sızıntı kontrollerini iki bağımsız değerlendiriciyle tamamla.
5. **Ön kayıt ve prompt freeze:** Rubrik, istem şablonları, örnekler, eşikler, model revision, tokenizer, runtime, seed/decoding ayarları ve analiz kodunu hash'leyip deney başlamadan dondur.
6. **Inference izni:** En az 60 kabul edilmiş bağımsız vaka, en az sekiz upstream proje, iki panel onayı, lisans kontrolü, kalibrasyon ve tüm hash kontrolleri tamamlanmadan açma. 80 vaka hedefi korunmalı.
7. **Analiz:** Vaka eşleştirmesini ve eksik çıktı kuralını önceden tanımla. Yalnızca p-değeri değil etki büyüklüğü, güven aralığı, vaka bazlı ham sayılar ve risk-kapsama dengesi raporla.

## 6. 4 Ocak 2027 başvurusuna yönelik sıkıştırılmış plan

Bu takvim hedef önerisidir; gerçekleşmiş iş olarak sunulamaz.

| Tarih | Hedef çıktı |
|---|---|
| 11–16 Kasım | V12 metadata intake, 105-ID dışlama kontrolü, yeni runner regression testleri |
| 17–30 Kasım | En az 60, hedef 80 vaka için lisans ve buggy/fixed/ground-truth incelemeleri; iki değerlendirici rubriği ve kalibrasyonu |
| 1–5 Aralık | Ön kayıt, prompt ve runtime freeze; no-inference preflight ve Kaggle yükleme doğrulaması |
| 6–17 Aralık | Kapılar sağlanırsa eşleştirilmiş 360–480 model çıktısının üretilmesi |
| 18–24 Aralık | İstatistiksel analiz, hata/sızıntı/sağlamlık incelemesi, sonuçların tekrar üretim kontrolü |
| 25–30 Aralık | Proje raporu, şekiller, tablo, kaynakça, yöntem ve sınırlılıklar |
| 31 Aralık–3 Ocak | Danışman ve bağımsız son denetim, TYBS başvuru alanları ve dosya kontrolü |
| 4 Ocak 2027 17:30'dan önce | Başvurunun TYBS'de tamamlanması |

Bu takvim çok sıkıdır. En az 60 vaka ve iki panel onayı yetişmiyorsa eşik sonuçlar görüldükten sonra düşürülmemeli; örneklem/iddialar bilimsel olarak yeniden kapsamlandırılmalı ve bitmemiş çalışma tamamlanmış gibi sunulmamalıdır.

## 7. Etik ve başvuru uygunluğu

TÜBİTAK'ın 2026–2027 çağrısında başvurular 23 Eylül 2026–4 Ocak 2027 arasında alınır; son gün saat 17:30'da sistem kapanır. Başvuru tarihinde 20 yaşından gün almamış lise öğrencileri katılabilir. Proje tamamlanmış olmalı; devam eden veya yalnızca fikir aşamasındaki çalışmalar başvuruda kabul edilmez. En çok üç öğrenci ve bir danışman bulunabilir; danışman zorunlu değildir.

Araştırmada insanların puanlama/inceleme verileri kullanılacaksa katılımcıların gönüllü katılım ve bilgilendirme kayıtları düzenlenmeli; MEB kurum paydaşlarıyla veri toplama söz konusuysa ilgili araştırma izni gerekliliği kontrol edilmelidir. 18 yaş altı öğrenci katılımcı varsa veli onamı da gerekir. İzin/onam gereklilikleri uygulamadan önce danışman ve TÜBİTAK yönergeleriyle teyit edilmelidir.

TÜBİTAK rehberi, yazılım projesinin yalnızca bir ürün göstermesini yeterli saymaz; bilimsel yönteme, uygun veri toplama/analize, test ve iyileştirmeye, özgün katkının açık biçimde ortaya konmasına önem verir. Bu nedenle jüriye “bir yapay zekâ yaptık” yerine karşılaştırmalı deney, ölçüm tanımları, eşleştirilmiş ham veri, sınırlılıklar ve yeniden üretilebilir kanıt sunulmalıdır.

## 8. Kaynak ve başvuru sayfaları

- 2027 çağrı sayfası ve takvim: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
- 2027 proje rehberi: https://tubitak.gov.tr/sites/default/files/2026-10/2204A_proje_rehberi_2027.pdf
- Tek proje kaynağı: https://github.com/MahmutVezir/dijitalikiz

## 9. Açık karar

Bu raporun tarihi itibarıyla çalışma, **altyapı ve teknik tarama aşamasında**; TÜBİTAK'a sunulmaya hazır bir araştırma sonucu değildir. Sonuç uydurulmayacak, test kurulumu hatası gerçek yazılım hatası diye sunulmayacak, kanıt yetersizliği doğru tahminle örtülmeyecek ve hiçbir vaka insan incelemesi olmadan kabul edilmeyecektir.
