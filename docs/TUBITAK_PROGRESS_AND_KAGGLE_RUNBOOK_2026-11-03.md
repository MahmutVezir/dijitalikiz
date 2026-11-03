# TÜBİTAK 2204-A — doğrulanmış durum ve Kaggle yürütme notu

**Denetim tarihi:** 3 Kasım 2026  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Amaç:** 2027 TÜBİTAK 2204-A başvurusu için tamamlanmış, tekrarlanabilir ve jüri önünde savunulabilir bir araştırma yürütmek. Finalistlik bir hedeftir; sonuç garantisi değildir.

## 1. Bugünkü doğrulanmış durum

GitHub `main` dalının son commit'i 29 Ekim 2026 tarihli `01ea347a311fe916f843d453b7bdef3d9fb15624` commit'idir. Bu commit, dış değerlendiriciden Erdem aracılığıyla aktarılan üç kanıt paketi hakkındaki puan ve kategorik yeterlilik bildirimlerini ayrı alanlarda kayda geçirir:

| Paket | Bildirilen puan | Bildirilen yeterlilik kararı |
|---|---:|---|
| m8 | 96/100 | Yetersiz |
| r5 | 90/100 | Yeterli |
| q2 | 88/100 | Kısmen yeterli |

Bunlar tek bir değerlendiriciden aracılı olarak alınmış bildirimlerdir. Kriter bazlı puan dökümü yoktur. Bu kayıt, iki ayrı ve birbirinden bağımsız insan panelinin kurulduğunu, puanlama kalibrasyonunun tamamlandığını veya doğrulayıcı deney izni verildiğini göstermez.

Ana araştırmanın durumu:

- Kabul edilmiş bağımsız doğrulayıcı vaka: **0**
- Ana doğrulayıcı model çıktısı: **0**
- `EXPERIMENT_MANIFEST_STAGE3.json`: `inference_allowed=false`
- `dataset_validation_gate`: `OPEN`
- `CASE_REGISTRY.json`: boş kayıt listesi
- Qwen model/tokenizer/CUDA çalışma zamanı doğrulaması: tamamlanmış değil
- Haricî ön kayıt ve hash dondurma: tamamlanmış değil

Bu nedenle P1 politikasının kanıtsız kesin teşhisleri azalttığına ilişkin henüz hiçbir deneysel sonuç yoktur.

## 2. Ana deney — sabit kapsam

Araştırma sorusu: Gerçek açık kaynak yazılım kusurlarında, kanıt yetersiz olduğunda cevap vermekten kaçınmaya izin veren P1 politikası; teşhis vermeyi zorunlu kılan P0 politikasına kıyasla kanıtla desteklenmeyen kesin kök neden teşhislerini azaltıyor mu? Bu farkın yanıt kapsamına ve yeterli kanıt bulunan vakalardaki gereksiz kaçınmaya maliyeti nedir?

Her bağımsız kusur için aynı temel bağlamdan üç kanıt paketi hazırlanır:

- E1: yeterli kanıt
- E2: kısmi kanıt
- E3: yetersiz kanıt

Her paket iki politika altında değerlendirilir:

- P0: teşhis vermek zorunda
- P1: yalnızca kanıt destekliyorsa teşhis ver; değilse açıkça kaçın

Böylece vaka başına altı hücre ve tek deterministik model yanıtı vardır. Hedef 80 bağımsız vaka; doğrulayıcı alt sınır 60 vaka ve en az 8 farklı upstream projedir. Alt sınır sağlanamazsa örneklem eşiği geriye dönük gevşetilmez; çalışma keşifsel/fizibilite olarak raporlanır.

Birincil sonlanım E3 koşulunda kanıtla desteklenmeyen kesin teşhistir. P0/P1 vaka eşleştirmesi iki taraflı exact McNemar testi, risk farkı ve %95 güven aralığı ile analiz edilir. Teşhisin gerçek kök nedenle doğru olması ile sunulan paketteki kanıtlarca desteklenmesi ayrı değerlendirilir.

Model, ana çalışma için Qwen/Qwen2.5-3B-Instruct sabit revision'ıdır: `aa8e72537993ba99e69dfaafa59ed015b17504d1`. Ana deneyin amacı bu modeli eğitmek değildir. Beş örnekleme, entropi ve kalibrasyon kullanan ayrı prototip ana P0/P1 deneyine karıştırılmayacaktır.

## 3. Kaynak paketi kontrolü

27 Ekim tarihli `KAGGLE_VALIDATION_SOURCE_BUNDLE_2026-10-27_v2.manifest.json` manifestinde 31 dosya bulunur. Bu denetimde manifestteki 31 giriş, güncel `main` dosyalarıyla karşılaştırıldı:

- 30 dosyanın Git blob SHA-1 ve bayt uzunluğu birebir eşleşti.
- Tek fark, sonradan güncellenmiş genel `README.md` dosyasıdır.
- Stage 3 runner, deney manifesti, vaka sicili, analiz planı, preflight kodu ve test dosyalarında manifest kaynaklı bir sürüm farkı görülmedi.

Yeni `02_kaggle_source_integrity_and_tests_no_inference.ipynb` notebook'u aynı kontrolü Kaggle'da tekrarlanabilir hâle getirir. Önce bütün v2 kaynak dosyalarını denetler, sonra manifestte listelenen testleri `pytest` ile çalıştırır ve son olarak salt-okunur bilimsel hazır olma kontrolünü kaydeder. README farkını yalnızca dokümantasyon uyarısı olarak sınıflandırır; yürütülebilir kaynak/test dosyası farkları engeldir.

Notebook model yüklemez, inference yapmaz, eğitim yapmaz, paket kurmaz, vaka kabul etmez ve deney manifestini değiştirmez. Testlerin geçmesi, bilimsel vaka kabulü veya model performansı kanıtı değildir.

## 4. Kaggle yürütme adımı

1. Kaggle Input'a v2 kaynak manifestini ve kaynak dosyalarını içeren güncel `dijitalikiz-stage3-source` veri kümesini ekle. Eski 24 Ekim veri kümesinde v2 manifesti yoksa onu güncel v2 kaynak paketiyle yeni bir dataset sürümüne yükselt; eski dosyalarla sessizce devam etme.
2. Notebook `02_kaggle_source_integrity_and_tests_no_inference.ipynb` dosyasını Kaggle'a aktar ve sırayla çalıştır.
3. Üretilen `stage3_no_inference_audit_*.zip` arşivini sakla. İçinde hash denetimi, test logu, preflight engelleri ve runtime bilgisi bulunur.
4. `pytest` yoksa notebook paket kurmaz; bunu raporlar. Ortamı elle değiştirmeden önce log incelenir.
5. Testler başarısızsa yalnızca gerçek hata loguna dayanarak düzeltme yapılır. Testleri devre dışı bırakmak, vaka sicilini doldurmak veya inference iznini açmak çözüm değildir.

## 5. Bilimsel olarak hâlâ tamamlanması gereken kapılar

### Vaka kabulü ve veri kalitesi
- Tarihsel maruziyet dışlama birliği uygulanmış olmalı.
- Kaynak ve lisans/provenance kontrolü tamamlanmalı.
- Aynı kayıtlı Python sürümü/runtime altında aynı hedef test buggy sürümde hedef kusuru göstermeli, fixed sürümde geçmeli.
- Kurulum/ortam/fixture hatası hedef kusur reprodüksiyonu sayılmamalı.
- Kaynak, buggy/fixed test logları, runtime fingerprint, kök neden referansı ve E1/E2/E3 paketleri hash'lenmeli.
- Benzer/aynı kök neden vakaları bağımsız vaka gibi sayılmamalı.

### Ayrık insan panelleri
- Panel A: en az iki bağımsız kişi; kaynak, lisans, test çifti ve kök neden doğrulaması.
- Panel B: Panel A üyeleriyle kesişmeyen en az iki bağımsız kişi; yalnızca anonimleştirilmiş kanıt paketi ve kör model çıktısının yeterlilik/kanıt desteği değerlendirmesi.
- İlk bağımsız puanlar saklanmalı; uyuşmazlıklar önceden belirlenmiş adjudication yöntemiyle çözülmeli.
- Kalibrasyon/pratik vakaları confirmatory kümeden ayrı tutulmalı.

### Ön kayıt, model ve deney
- Dışarıdan doğrulanabilir ön kayıt ve eksiksiz hash manifesti.
- Sabit model/tokenizer revision ve runtime preflight.
- En az 60 kabul edilmiş vaka ve en az 8 upstream proje.
- Bütün kapılar kapandıktan ve ayrı açık yetkilendirme tamamlandıktan sonra ana altı hücreli inference.
- Kör puanlama, değerlendiriciler arası uyum ve önceden tanımlanmış istatistiksel analiz.

## 6. Takvim ve başvuru koşulu

TÜBİTAK'ın 2026–2027 çağrı sayfası başvuru tarihlerini 23 Eylül 2026–4 Ocak 2027 olarak veriyor; son gün başvurunun saat 17.30'da kapandığını belirtiyor. Resmî sayfa, projelerin rehbere göre hazırlanmış ve tamamlanmış olması gerektiğini, fikir aşamasındaki veya devam eden projelerin başvuruya uygun olmadığını da söylüyor. Başvuru öncesinde çağrı sayfası ve güncel rehber yeniden kontrol edilmelidir.

Proje planındaki 7 Kasım 2026 fizibilite karar noktası korunmalıdır: o tarihte 60 vaka/8 proje yolunda gerçekçi, kanıta dayalı bir ilerleme yoksa doğrulayıcı tasarımın kapıları gevşetilmez; çalışma inference öncesinde keşifsel/fizibilite olarak yeniden çerçevelenir.

Resmî kaynak: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi

## 7. Bilinçli olarak yapılmayan işlemler

Bu branch'te:
- `main` dalı değiştirilmedi.
- `CASE_REGISTRY.json` ve deney manifesti değiştirilmedi.
- Model indirilmedi/yüklenmedi, eğitim veya inference çalıştırılmadı.
- İnsan değerlendirmeleri yapılmış gibi gösterilmedi.
- Test başarısı veya bilimsel sonuç iddiası üretilmedi.

Bu not, doğrulanmış mevcut durumu ve bir sonraki güvenli yürütme adımını tanımlar; tamamlanmış proje raporu değildir.


## 8. 3 Kasım CI incelemesi ve test düzeltmesi

PR açılışının tetiklediği 3 Kasım 2026 tarihli CI çalışmasında iki farklı sonuç alındı:

- `Evidence Abstention Preflight (No Inference)` başarılı oldu. Fail-closed preflight ve kanıt paketi denetleyicisinin birim testleri çalıştı; bu yalnızca preflight kodunun test kapsamıdır.
- `Research Validation (No Inference)` içinde tarihsel artifact integrity işi başarılı oldu. Repository/configuration işinde 367 test ve 48 subtest geçti; bir test başarısız oldu.

Tek başarısız test: `CohortMatrixTests.test_v2_fails_closed_if_source_queue_partially_filters_exposure_ids`. Uygulama, aktif cohort içinde dışlama listesinde bulunan bir vaka gördüğü için daha erken ve daha spesifik `A prior-exposed ID appears in the active screening cohort` hatasını doğru biçimde verdi. Test fixture'ı ise aynı vakayı aktif cohort'a koymasına rağmen daha sonraki `mixes pre-filtered and unfiltered` hatasını bekliyordu. Dolayısıyla mevcut test, adının tarif ettiği karma filtre senaryosunu izole etmiyordu.

Test fixture'ı, uygulama güvenlik kontrolünü gevşetmeden düzeltildi: aktif cohort yalnızca dışlama listesindeki olmayan c/d vakalarını içeriyor; kaynak kuyrukta ise dışlama listesindeki a bulunmuyor ve b hâlâ mevcut. Böylece test artık doğrudan karma filtre provenance kontrolünü sınar. Bu düzeltmenin sonucu, yeni CI çalışması tamamlanmadan başarılı kabul edilmemelidir.

İlgili ilk CI çalışması:
- Research Validation: https://github.com/MahmutVezir/dijitalikiz/actions/runs/41644196184
- Evidence Abstention Preflight: https://github.com/MahmutVezir/dijitalikiz/actions/runs/41644196029

Düzeltme sonrası doğrulama:
- Commit: `0a0fe98684792a590d28ef430207746a6f2f1047`
- Yeni CI çalışmaları: PR değişikliğinden sonra tetiklendi; sonuçları ayrıca kontrol edilmelidir.

Bu test düzeltmesi yalnızca test senaryosunu daha doğru kurar. Vaka sicilini, maruziyet dışlama kurallarını, deney kapısını veya bilimsel sonuçları değiştirmez.
