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


## 9. Son doğrulama — 3 Kasım 2026, 16:30 TRT itibarıyla

Önceki bölümdeki “sonuçları ayrıca kontrol edilmelidir” ifadesi artık güncel değildir. En son PR head commit'i `8d00932f378d75d4f48b349bca7dee11af8228b4` için üç CI hattının tamamı başarılıdır:

| Kontrol | Sonuç | Kapsam |
|---|---|---|
| Research Validation (No Inference) | **PASS** | 371 test + 48 subtest; 6,23 saniye |
| Evidence Abstention Preflight (No Inference) | **PASS** | Fail-closed kapı testleri ve kanıt paketi auditor testleri |
| Evidence abstention cohort builder tests | **PASS** | Metadata-only kuyruk/cohort regression testleri |
| Tarihsel deney artifact bütünlüğü | **PASS** | Sabit ID, bayt uzunluğu, SHA-256, ZIP bütünlüğü ve kayıt denetimi |
| Yeni Kaggle audit notebook statik testi | **PASS** | Notebook JSON, bütün Python hücrelerinin derlenmesi ve no-inference güvenlik koşulları |

Run bağlantıları:
- [Research Validation — 41644754017](https://github.com/MahmutVezir/dijitalikiz/actions/runs/41644754017)
- [Evidence Abstention Preflight — 41644753993](https://github.com/MahmutVezir/dijitalikiz/actions/runs/41644753993)
- [Cohort builder tests — 41644753927](https://github.com/MahmutVezir/dijitalikiz/actions/runs/41644753927)

Bu yeşil CI sonuçları yazılım ve konfigürasyon doğrulamasıdır. **Bilimsel veri kümesinin hazır olduğunu veya hipotezin desteklendiğini göstermez.**

### Son no-inference kapısının gerçek çıktısı

Run `41644753993` içindeki `readiness-report.json` yeniden okunmuştur. Sonuç:

- `ready=false`
- Kabul edilmiş bağımsız vaka: **0**
- Kabul edilmiş upstream proje: **0**
- Blokaj sayısı: **20**
- `model_inference_performed=false`

Yirmi blokajın tam dökümü:

1. Deney manifesti inference için açık yetki vermiyor.
2. Veri doğrulama kapısı `CLOSED` değil.
3. Denetlenebilir ön kayıt URI'si yok.
4. İki değerlendiricili rubrik ve adjudication protokolü dondurulmamış.
5. Bağımsız değerlendirici kalibrasyonu tamamlanmamış.
6. Tam model/tokenizer/runtime yükleme ön kontrolü geçmemiş.
7–17. Aşağıdaki on bir dosyanın SHA-256 değeri eksik veya geçersiz: prompt koşulları, çıktı şeması, analiz planı, deney tasarımı, puanlama rubriği, runtime lock, vaka sicili, maruziyet dışlama birliği, analiz kodu, inference runner ve preflight kodu.
18. Kabul edilmiş vaka sayısı 0; alt sınır 60, hedef 80.
19. Upstream proje sayısı 0; alt sınır 8.
20. Runtime lock bu çalışma için doğrulanmamış.

Dolayısıyla CI'nin yeşil olması inference yetkisini açmaz. Bu kapılar ancak gerçek kanıt ve insan değerlendirmesiyle giderilebilir; manifestteki bayrakları elle değiştirerek kapatılamaz.

### Kaggle çalıştırmasının durumu

Yeni `02_kaggle_source_integrity_and_tests_no_inference.ipynb` notebook'u GitHub CI'da statik olarak doğrulandı; **Kaggle GPU/runtime üzerinde henüz yürütülmedi**. Kullanıcı tarafındaki Kaggle Input'a tam olarak 27 Ekim v2 kaynak manifesti ve 31 kaynak dosyası eklenmeli. Notebook çalıştırıldığında bir ZIP denetim paketi üretir. ZIP'in hash, test ve preflight raporu incelenmeden Kaggle ortamı doğrulandı denmemelidir.

Bu çalışma sürümünde `main` değişmemiştir; değişiklikler PR #157 taslak dalındadır. PR'ın yeşil CI'si merge veya bilimsel deney izni anlamına gelmez.


## 10. En ileri aday vakanın (Black-9 / CASE-7F31A) durum denetimi

Mevcut metadata-only adaylar içinde en ileri teknik kanıt Black-9'dur. Kayıtlar birlikte okunduğunda:

- BugsInPy sabit revision: `11c5f1eea954a42132cfd06bf257766a7963e0fd`.
- Buggy commit: `026c81b83454f176a9f9253cbfb70be2c159d822`.
- Fixed commit: `d6db1c12a8e14833fe22da377cddc2bd1f43dc14`.
- Metadata/runtime Python: **3.8.3**; disposable venv ve import preflight kayıtları başarılı.
- Aynı hedef test: `tests.test_black.BlackTestCase.test_python2_print_function`.
- Buggy sürüm sonucu: beklenen `black.InvalidInput: Cannot parse: 6:13: print(a, file=sys.stderr)` parser hatası.
- Fixed sürüm sonucu: `Ran 1 test ... OK`.
- Hedef koşudan önce buggy/fixed commit HEAD kontrolleri, ortak test bundle hash'i ve aktif worktree import yolları doğrulanmış; koşu sonrası kaynak/test hash'leri değişmemiş.
- MIT `LICENSE` dosyası iki commit'te de bulunmuş; lisans/atıf yeniden kullanım kararı henüz bağımsız olarak onaylanmamış.
- Ön root-cause açıklaması kod farkı ve hata imzasıyla tutarlı; iki bağımsız kök neden değerlendiricisinin onayı bekleniyor.

İlgili kayıtlar:
- `BLACK_9_METADATA_GATE_2026-10-24.json`
- `BLACK_9_SOURCE_OVERLAY_PREFLIGHT_2026-10-24.json`
- `BLACK_9_DEPENDENCY_IMPORT_PREFLIGHT_2026-10-24.json`
- `BLACK_9_TEST_ENVIRONMENT_MANIFEST_2026-10-24.json`
- `BLACK_9_PAIRED_TEST_RESULT_2026-10-24.json`
- `BLACK_9_HASH_AUDIT_2026-10-24.json`
- `BLACK_9_PRELIMINARY_ROOT_CAUSE_2026-10-24.json`

### Kanıt paketi ve insan incelemesi

Black-9 için CASE-7F31A takma adıyla üç kanıt paketi taslağı hazırlanmıştır. Dondurulmuş olmayan taslak manifestinde kayıtlı model-facing SHA-256 değerleri:

| Taslak seviye | Model-facing packet SHA-256 | Şu anki durum |
|---|---|---|
| E1 | `e2407fe4ba06ef939b8ef612d43703673bcfb1392f110bbc04dc788dc7a42c54` | Yeterli olması bekleniyor; panel onayı yok |
| E2 | `96350935950d71421a2dc099f6bab7e0ea3506654c1bc8498bc2893b6ca10e82` | Kısmen yeterli olması bekleniyor; panel onayı yok |
| E3 | `abe6d42d731695cfe84a8753ff18a36bbae7301b50f8c291f1d608946e0460aa` | Yetersiz olması bekleniyor; panel onayı yok |

Bunlar taslak etiketleridir; bilimsel olarak doğrulanmış E1/E2/E3 sınıfları değildir. Kör inceleme ZIP'i için manifestte ZIP bütünlüğü başarılı, E-level anahtarı ve gold root-cause metni reviewer paketinden çıkarılmış, iki bağımsız reviewer gereksinimi yazılmıştır. Ancak manifest durumu hâlâ `reviewer_bundle_prepared_waiting_for_two_independent_reviews` ve `accepted_for_confirmatory=false) şeklindedir.

29 Ekim notundaki m8/r5/q2 kodlu üç kategori bildirimi tek değerlendiriciden aracılı olarak alınmıştır. Puanlar (96/90/88) ile kategorik kararlar ayrı veriler olarak saklanır; kriter bazlı döküm bulunmaz. Bu bildirim tek başına iki kişilik Panel B, inter-rater agreement, rubrik kalibrasyonu veya vaka kabulü oluşturmaz. Reviewer paketindeki gizli eşleştirme anahtarı açılmadan bu kategori bildirimlerini E1/E2/E3 etiketleriyle eşleştirip sonuç üretmek yasaktır.

### Black-9 için kalan kabul kararları

1. Panel A'dan iki farklı değerlendirici kaynak, lisans/atıf, hedef test çiftinin geçerliliği ve gerçek kök nedeni bağımsız incelemeli.
2. Panel B'den Panel A'dan farklı iki değerlendirici, yalnızca anonim E1/E2/E3 paketlerini dondurulmuş rubrikle bağımsız puanlamalı.
3. İlk puanlar ve gerekçeler saklanmalı; adjudication ve inter-rater agreement raporlanmalı.
4. Ham Kaggle logları ve rapor arşivi doğrudan alınarak hash'leri bağımsız yeniden doğrulanmalı; repo'daki kullanıcı-raporlu SHA kayıtları tek başına yeterli sayılmamalı.
5. Vaka ancak bütün bireysel ve genel kapılar geçtikten sonra kapalı `CASE_REGISTRY` içine eklenebilir. Bu işlemden önce inference yapılamaz.

**Sonuç:** Black-9, teknik buggy-fail/fixed-pass eşleşmesi bulunan ve insan incelemesine hazırlanmış bir adaydır; kabul edilmiş doğrulayıcı vaka değildir. Şu anki sicil sayısı 0 olarak kalır.
