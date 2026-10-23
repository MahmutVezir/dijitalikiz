# Proje güncel durumu ve en az aşamalı yürütme planı

**Tarih:** 23 Ekim 2026  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**TÜBİTAK hedefi:** 2027 TÜBİTAK 2204-A  
**Karar:** Proje hedefi korunuyor; bilimsel deney tamamlanmış değil. Bu belge, güncel durum ve sonraki işleri tek yerde toplar; ön kayıt veya deney sonucu değildir.

## Yönetici özeti

Projenin araştırma sorusu, hedefli literatür notları, deney tasarımı, veri tarama/çıkarma kuralları ve yazılım prototipi büyük ölçüde belgelendi. Ancak **0 kabul edilmiş bağımsız vaka, 0 doğrulayıcı model çıktısı, tamamlanmamış insan incelemeleri, boş kalibrasyon verisi ve doğrulanmamış tam CUDA/runtime yüklemesi** nedeniyle araştırma hipotezi hakkında sonuç verilemiyor.

Bir önceki mühendislik smoke çalışmasında 10 çıktı (P0: 5; P1: 5) üretildi fakat iki koşulda da 0/5 açık kaçınma görülmüştü. Bu çalışma maruziyet, prompt sızıntısı ve runtime uyumsuzluğu nedeniyle doğrulayıcı çalışmadan dışlanmıştır; yalnızca mühendislik tanılamasıdır. Ayrıntı: [EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md](EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md).

## Ne tamamlandı?

- Araştırma sorusu ve aday bilimsel katkı tanımlandı; literatür taramasının hedefli olduğu ve özgünlüğün kanıtlanmadığı açıklandı.
- BugsInPy sabit revizyonunda 501 ham metadata kaydı / 17 upstream proje envanteri oluşturuldu; bu kabul edilmiş örneklem değildir.
- V9'un yerini alan **V10 metadata-only intake** hazırlandı: sabit BugsInPy envanterindeki 501 ham metadata kaydı üzerinden, 61 tarihsel + 32 güncel = 93 kalıcı maruziyet/dışlama kimliği birleştirildi. Bu filtreyle 407 metadata adayı / 14 proje kaldı; V10'un ilk 100 adayı 14 proje içeriyor ve dışlama kümesiyle kesişimi 0. Bu sıra yerel olarak yeniden üretildi; remote CI yürütmesi henüz doğrulanmadı. Hiçbir V10 adayı kabul edilmiş vaka değil ve V9 teknik tarama grupları hâlâ kalıcı dışlamada. Ayrıntı: [V10 intake raporu](STAGE1_V10_METADATA_INTAKE_2026-10-23.md), [93 ID'lik maruziyet birleşimi](EXPOSURE_UNION_2026-10-23.json), [dondurulmuş V10 sıra manifesti](SCREENING_COHORT_100_V10_2026-10-23.json), [GitHub Actions runner kurtarma rehberi](GITHUB_ACTIONS_RUNNER_RECOVERY_GUIDE_2026-10-23.md).
- Qwen yapılandırılmış yanıt adapter'ı, katı JSON ayrıştırma, çoklu aday entropy/lexical disagreement sinyalleri, kalibrasyon arayüzü, Brier/ECE metrikleri, kanıt paketi/hash auditor'ı ve fail-closed inference kapısı oluşturuldu.
- Karar katmanı; kanıt desteği/çelişki sinyalleri veya kalibrasyon eksikse teşhis üretmek yerine kaçınıyor.
- Semantik auditor prompt/parser arayüzü ve adapter eşlemesi eklendi. Hash-bağlı giriş noktası, araştırma istemini dışarıdan dondurulmuş kanıt paketi SHA-256'sına bağlayacak şekilde PR #121 ile birleştirildi; değiştirilmiş paket ve etiket sızıntısı için ek regresyon testleri yazıldı. 12 temel sentetik test, bu son giriş noktası eklenmeden önce izole yerel koşuda geçmişti; güncellenmiş tam semantik-auditor test paketinin geçişi doğrulanmış değildir. GitHub Actions kayıtları adım göstermiyor ve günlükler `BlobNotFound` döndürüyor. Gerçek Qwen denetçi çağrısı ve kör insan puanlarıyla geçerlik hâlâ yok. Ayrıntı: [SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md](SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md).
- Tarihsel DİJİTALİKİZ/CCDG veri ve sonuçları yeni araştırmadan ayrıldı; bunlar yeni çalışmanın kanıtı olarak kullanılmayacak.

## V10 veri kuyruğu düzeltmesi — 23 Ekim 2026

Eski V10 denemesi, yalnızca 2026-10-22 tarihli 32 ID'lik ek listeyi kullandığında eski 2026-10-21 maruziyet günlüğündeki kayıtların yeniden kuyruğa girebileceği için geçersiz sayıldı ve onunla devam edilmedi. Düzeltmede iki kaynak birleştirilerek 93 benzersiz ID kalıcı olarak çıkarıldı. Yeni kuyruk 407 aday / 14 proje; dondurulan ilk 100 aday 14 proje ve maruziyet kümesiyle kesişim 0. Kaynak envanter ve yenilenmiş kuyruk hash'leri V10 raporunda kayıtlıdır.

Bu, **metadata sırası doğrulamasıdır**, bug-fix test çifti doğrulaması değildir. İzole yerel kopyalar `py_compile` kontrolünü geçti; 407 satırlı kuyruk ve 100 adaylık intake yeniden üretildi, kuyruk SHA-256'sı V10 manifestiyle eşleşti ve seçilen ID'lerle 93 dışlama kimliğinin kesişimi 0 çıktı. Bu kontrol orijinal historical JSON dosyasının bayt düzeyinde kopyasıyla değil, kaynak kayıttan çıkarılmış 61 ID listesiyle yapıldı; dolayısıyla remote CI veya kaynak dosyanın ham hash'i yerine geçmez. GitHub Actions run 39984142075 yeniden denendi ancak yine adım kaydetmedi ve log indirmesi `BlobNotFound` döndürdü. Ana doğrulayıcı vaka sicili boş kalır; hiçbir vaka otomatik kabul edilmez.

## Ne kaldı?

| Blokaj | Mevcut durum | Kapanış ölçütü |
|---|---|---|
| Doğrulayıcı vaka havuzu | 0 kabul | En az 60 bağımsız vaka, en az 8 upstream proje; hedef 80. Her vaka için aynı hedef testte buggy-fail/fixed-pass ve gerçek kayıtlı Python sürümü. |
| Kök neden/provenance | Tam bağımsız inceleme yapılmadı | Her vaka için iki bağımsız insan incelemesi, lisans/kök neden/patch-test ilişkisi ve uyuşmazlık kaydı. |
| E1/E2/E3 kanıt yeterliliği | Tamamlanmadı | Farklı ve bağımsız iki kişilik kör panel; altın kök neden ve koşul etiketi gösterilmeden paket onayı. |
| Semantik auditor/entropi prototipi | Kod iskeleti ve hash-bağlı giriş mevcut; yeni test paketi ve gerçek Qwen çağrısı doğrulanmadı | Bu kol ana P0/P1 doğrulayıcı deneyden ayrıdır. Operasyonel sistem/kalibre eşik iddiası için ayrı örneklem, kör insan karşılaştırması ve ayrı izin gerekir; ana istem-politikası hipotezinin birincil ölçütüne dahil edilmez. |
| Model/runtime | Aday kilitli fakat doğrulanmadı | Tam Qwen/tokenizer revision, chat template, Python/PyTorch/Transformers/CUDA ayarları ve yükleme artefaktı kontrolü. |
| Model-güven kalibrasyonu | Veri boş | Yalnızca ayrı entropi/semantik-auditor prototipi için geçerlidir. Ana P0/P1 istem-politikası çalışmasında modelin kendine verdiği güven skoru ya da kalibre eşik kullanılmaz. |
| Ön kayıt ve izin | Taslak/kapalı | Son protokol ve hash manifesti sonuçlar görülmeden denetlenebilir kayıtla yayımlanmalı; ayrıca açık yürütme izni. |
| CI/runner | Son durum için tüm test adımları kanıtı tamamlanmış değil | Gerçek runner atanmalı, yeni birimin test logu ve iş artefaktı incelenmeli. İş runner'a başlamadıysa “test geçti” sayılmaz. |
| Resmî rapor | Final sonuçlar yok | Yöntem, gerçek sonuç, sınırlılıklar, dışlamalar, kaynakça ve resmi şablon kontrolü. |
| Başvuru uygunluğu | Öğrenci/ekip beyanı gerekiyor | Son çağrı koşullarını ve daha önceki/benzer yarışma başvurularını öğrenci ve danışman kayıtlarından doğrulama; bunu otomatik doldurmak mümkün değil. |

## En az sayıda aşamayla tamamlama

### Aşama 1 — Veri, yöntem ve çalıştırma kapılarını kapat

1. GitHub Actions runner sorununu ayır: basit no-inference iş akışı gerçekten adımları çalıştırıyor mu? Sonra tüm birim testlerini çalıştır ve ham logu/arşivi denetle.
2. Tarama kuyruğunda önceden açılmamış vakaları belirlenmiş sırayla işle; teknik test sinyali verenleri otomatik kabul etme.
3. İki ayrık insan panelini fiilen oluştur ve vaka başına kaynak/lisans/kök neden/kanıt paketlerini gözden geçir.
4. Ana doğrulayıcı deneyde yalnızca dondurulmuş P0/P1 istem talimatları kullanılır; entropy, semantik-auditor kararı veya eşik çıktısı bu koşullara karıştırılmaz. Entropi/semantik-auditor prototipi, etkinliği iddia edilmeden önce ayrı bir mühendislik-validasyon kolunda ele alınır.
5. Ana deney için model/tokenizer/runtime'ı çıktı üretmeden denetle; yalnızca ana deneyde kullanılan prompt, şema, analiz planı, vaka/kanıt paketleri, rubrik ve runtime hash'lerini dondur; protokolü sonuçlardan önce kaydet. Ayrı adapter validasyonu yürütülecekse onun calibration/auditor artefaktları farklı bir sürüm/ön kayıt altında tutulur.
6. En az 60 kabul edilmiş bağımsız vaka / 8 proje şartı ve diğer kapılar sağlanmadan inference çalıştırma. 4 Kasım iç kontrolünde bu eşik sağlanmıyorsa açık bir go/no-go kararı al; eşiği sessizce gevşetme.

**Aşama 1 çıkışı:** audit edilebilir veri sicili, bağımsız değerlendirici kayıtları, tam model-runtime kontrolü, ana deney hash manifesti, kayıtlı protokol ve açık izin. Model güven kalibrasyonu, yalnızca ayrı adapter iddiası için gerekli ayrı çıktıdır.

### Aşama 2 — Deneyi yürüt ve bilimsel sonucu üret

1. Aynı sabit model ve runtime ile kabul edilen her vakada E1/E2/E3 × P0/P1 koşullarını çalıştır.
2. En az 60 vaka için 360, 80 vaka için 480 çıktının ham metnini, seed/prompt/kanıt hash'lerini, model sürümünü ve şema hatalarını sakla. Bunlar planlanan sayılardır, gerçekleşmiş çıktı sayısı değildir.
3. Koşullara kör bağımsız puanlama yap; kök neden doğruluğu, görünen kanıt desteği ve karar/kaçınma etiketlerini ayrı kaydet.
4. Önceden planlanmış birincil sonuç için eşleştirilmiş risk farkı, iki taraflı exact McNemar testi ve %95 güven aralığını hesapla; E1 gereksiz kaçınma ve yanıt kapsamını da raporla.

**Aşama 2 çıkışı:** gerçek veri, ham çıktılar, kör puanlama, istatistik, tekrarlanabilir analiz artefaktları ve sınırlılıklar.

### Aşama 3 — TÜBİTAK raporu ve teslim

1. Gerçek bulguları, sıfır/olumsuz sonuçları ve metodolojik sınırlılıklarıyla yaz.
2. 2026–2027 resmi proje raporu şablonuna yerleştir; başlık, özet, anahtar kelime, kaynakça, sayfa biçimi, izinler ve bütünlük kontrollerini resmî belgelerle doğrula.
3. Öğrenci, danışman ve ekip uygunluk beyanlarını tamamla; TYBS'de başvuruyu son günün öncesinde gözden geçir.

Resmî çağrı sayfasında başvuru dönemi 23 Eylül 2026–4 Ocak 2027; kapanış **4 Ocak 2027 saat 17.30 (Türkiye saati)** olarak ilan edilmiştir: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi. Yarışmaya başvurunun tamamlanmış proje üzerinden yapılması gerekir.

## Korunacak bilimsel kurallar

- Önceden incelenen teknik/debug vakaları doğrulayıcı örnekleme geri alınmaz.
- Ham aday sayısı, CI'ın yeşil olması, prompt yazılması ve sentetik birim testleri gerçek deney sonucu değildir.
- Yapısal hash/referans kontrolü, semantik destek doğrulaması değildir.
- Modelin kendi verdiği 0.95 gibi güven beyanları kalibre edilmiş olasılık sayılmaz.
- E1/E2/E3 altın etiketleri, gold kök neden ve patch çalışma zamanı kararına sızdırılmaz.
- Hipotez, birincil ölçüt veya dışlama kuralları sonuç görüldükten sonra değiştirilmez.
- Türkiye finalisti olma hedefi korunur ancak garanti verilemez.

## Güvenlik kapısı düzeltmesi ve güncel CI durumu — 23 Ekim 2026

PR [#130](https://github.com/MahmutVezir/dijitalikiz/pull/130) ana dala birleştirildi. Analiz betiği ve yeni inference kapısı artık yalnızca ilk 13 eski dışlama kimliğine güvenmiyor; kanonik `EXPOSURE_UNION_2026-10-23.json` içindeki 93 kalıcı dışlamanın tamamını kontrol edecek şekilde güncellendi. Ayrıca analiz öncesi `frozen_hashes` alanının sadece dolu olması yeterli değil: zorunlu dosyaların SHA-256 değerlerinin mevcut dosyalarla bire bir eşleşmesi aranıyor. Sentetik regresyon testleri bu kontroller için eklendi.

Bu düzeltmenin ardından ilişkili GitHub Actions denemeleri API'de başarısız göründü, fakat işlerin adım listeleri boştu (`steps=null/[]`), günlük indirmeleri `BlobNotFound` döndürdü ve artefakt oluşmadı. Dolayısıyla bu kayıtlar ne “testler geçti” ne de “test kod hatasından çöktü” sonucunu destekler. **PR #130 birleştirildi, ancak bu PR'ın yeni testleri için denetlenebilir uzak CI sonucu henüz yoktur.** Birleştirme durumu testlerin geçişiyle karıştırılmamalıdır.

V10 metadata intake için yerel/artefakt destekli tekrar üretim denetimi aynı sonuçları koruyor: sabit BugsInPy envanteri 501 satır/17 proje; tam 93-ID dışlama birleşimi sonrasında 407 satır/14 proje; V10 ilk 100 aday/14 proje; seçilen kimlikler ile dışlama birleşimi kesişimi 0. Bu yalnızca metadata sırası ve maruziyet filtrelemesi doğrulamasıdır. Uzak builder iş akışının gerçekten çalıştığı henüz kanıtlanmadı.

Güncel bilimsel kapılar değişmedi: kabul edilmiş bağımsız vakalar 0, doğrulayıcı model çıktısı 0, doğrulanmış Qwen/CUDA runtime yok, kalibrasyon gözlemi yok, ön kayıt taslak ve inference izni kapalı. Aşama 1'deki sıradaki eylem, depo sahibinin GitHub Actions ekranında bir runner'ın gerçekten atandığını ve log/artifact'ların üretildiğini doğrulamasıdır. Bu operasyonel engel kalkınca V10 aday teknik taraması, protokolde belirlenmiş sırayla başlatılabilir; geçmişte debug için açığa çıkan vakalar geri eklenemez.

## Ek doğrulama kapıları ve runner ataması — 23 Ekim 2026

- [PR #132](https://github.com/MahmutVezir/dijitalikiz/pull/132) inference gate'e sabit artefakt yolları, güvenli göreli yol denetimi ve kanonik boş `CASE_REGISTRY.json` şartını ekledi; [PR #133](https://github.com/MahmutVezir/dijitalikiz/pull/133) aynı kurallara göre sentetik test fixture'larını ve sonuç analizindeki sicil yolu denetimini hizaladı. Her ikisi de ana dala birleştirildi. Bunlar veri-kaynağı güvenliğine dair yazılım değişiklikleridir; araştırma vakası kabul etmez ve hipotez hakkında sonuç üretmez.
- V10 doğrulama koşusunun ham API kaydı daha ayrıntılı incelendi: run `39985336539`, attempt 3; job `120546618992`; durum birkaç saniye içinde tamamlandı/başarısız, `runner_id=0`, boş `runner_name`, `steps=[]`, log ve artefakt yok. Diğer iki örnek (`39991977270` / job `120545733659`; `39991977312` / job `120545733724`) aynı deseni gösteriyor. Dolayısıyla bu kayıtlar birim testlerinin başarısız olduğunu göstermez; test adımları kaydedilmemiştir. Sebep kesinleştirilmiş değildir.
- Uzak yürütme için depo sahibinin operasyonel kontrolü: GitHub deposunda **Settings → Actions → General** altında Actions/workflow izinlerini; hesapta **Billing & plans → Actions** altında kullanım kotasını, ödeme yöntemi ve bütçe durdurma ayarını kontrol et. GitHub belgeleri özel depolarda kullanım kotası/ödeme kısıtlarının hosted runner kullanımını engelleyebildiğini belirtir; burada bunun gerçekten sebep olduğu henüz kanıtlanmadı. Ayarlar normalse yukarıdaki run/job kimlikleri ve `runner_id=0` metaverisiyle GitHub Support'a başvurulmalı.
- Runner sorunu çözülene kadar daha fazla V10 adayını yalnızca iş akışı hata ayıklamak için çalıştırmak doğru değildir; böyle kullanılan adaylar kalıcı olarak maruz kalmış sayılabilir. Aday testlerine geçmeden önce metadata tekrar üretilebilirliği gerçek log/artefaktlarla kanıtlanmalı. V10 hâlen 100 metadata adayıdır; kabul edilmiş deney vakası sayısı 0'dır.

## Primary preflight exposure guard — PR #140, 23 October 2026

[PR #140](https://github.com/MahmutVezir/dijitalikiz/pull/140) merged a defense-in-depth control into the primary Stage 3 preflight. Its frozen input contract now includes the full `EXPOSURE_UNION_2026-10-23.json`; the union must contain 93 unique, non-empty IDs and an exact count, the manifest must use the canonical registry/union paths, and a case marked `accepted_for_confirmatory=true` is blocked if its ID appears anywhere in the permanent exposure union—even when its row claims `prior_exposure_clearance=true`. Regression tests were added for this behavior, malformed/duplicated unions, and noncanonical paths. The primary experiment manifest was not modified to permit inference.

**This code change is merged; the new tests have not been verified in a real runner.** Post-merge Actions:
- [39995370426](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39995370426), jobs 120557400108 and 120557400493: both ended after about two seconds with `runner_id=0`, empty runner name, and no steps.
- [39995357117](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39995357117), job 120557355541: no runner and no steps.
- [39995356861](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39995356861), jobs 120557352459 and 120557352825: no runner and no steps.

These are pre-runner dispatch failures, not Python test logs. Consequently it is not correct to claim the modified test suite passed or failed on these runs. The minimal one-shell-step probe in [run 39994780466](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39994780466) failed with the same zero-step signature, which isolates the current blocker from project test logic. The underlying cause is not yet determined; repository owner must inspect Actions settings and account usage/budget, then contact GitHub Support if those appear normal.

Current science gates after PR #140 remain unchanged: 93 exclusions, 0 accepted cases, 0 confirmatory model outputs, empty calibration data, no verifiable preregistration, and inference disabled. No new candidate tests should run until the minimal runner starts recording real steps and logs, since using candidates to troubleshoot the runner would permanently expose them.

## Tekil hash sözleşmesi ve adaptör ayrımı — PR #143, 23 Ekim 2026

[PR #143](https://github.com/MahmutVezir/dijitalikiz/pull/143) ana deneyin salt-okunur ön denetimi ile sonuç analiz betiği arasındaki hash anahtar uyuşmazlığını giderdi. Her iki katman artık aynı on bir depo-köklü tam dosya yolunu arar; eksik hash, hash eşleşmezliği veya beklenmeyen ek bir hash yolu kapıyı kapalı tutar. Ana deneyin bu zorunlu kümesine vaka sicili, 93 kimlikli maruziyet birleşimi, prompt, şema, tasarım/analiz, rubrik, runtime kilidi ve analiz kodu dahildir.

Ana P0/P1 istem-politikası deneyi, beş-adaylı entropy/kalibrasyon adaptöründen ayrı tutulur. Bu yüzden adaptöre ait `CALIBRATION_DATA.json`, ana karşılaştırmanın zorunlu hash sözleşmesinden çıkarıldı; bu veri yalnızca ayrı adaptör üzerinde Brier/ECE veya kalibre güven skoru iddiaları yapılacaksa ayrı protokol ve doğrulamayla kullanılır. Adaptör manifesti inference kapalı durumunu korur.

**CI sınırı:** PR #143 birleştirildi; ancak ilişkili GitHub Actions işlerinde runner atanmadı (`runner_id=0`, `steps=[]`). Kod değişikliklerinin gerçek Python testlerinden geçtiği henüz doğrulanmadı. Bu sözleşme tutarlılığına ilişkin statik çapraz kontrol dışında test başarısı iddiası yoktur. Mevcut ana deney manifestinde `frozen_hashes={}`, kabul edilmiş vakalar 0 ve inference kapalıdır.

## Nihai durum

**Yazılım prototipi var; bilimsel etkinlik henüz ölçülmedi.** En büyük dış bağımlılıklar bağımsız değerlendiriciler, yeterli ve kabul edilmiş gerçek vaka havuzu, semantik auditor validasyonu ve gerçek GPU/runtime doğrulamasıdır. Bu işler tamamlanmadan projeye “halüsinasyon azaltıldı” veya “hipotez doğrulandı” denmeyecektir.


## Added verification — exact local reconstruction of V10 metadata order (23 October)

The preserved metadata inventory artifact from run 39640796171 was downloaded and independently hash-checked (`069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb`). Reconstructing the deterministic project-interleaved queue against the full 93-ID historical/current exposure union yielded 407 candidates across 14 projects and matched the frozen V10 queue SHA-256 exactly (`91c926665752e0e44c6a4ba499422d2af23c6156f4d61b675e29ca0288a27ece`). The first 100 IDs also match the frozen V10 sequence exactly; they span 14 projects and have zero intersection with the exposure union.

A strict reproducibility checker and seven synthetic regression tests were added. The local synthetic test run is 7/7 passing, including tampered queue hash, changed order, reintroduced exposure, absent inventory IDs, malformed exclusion payloads, and pre-acceptance. The new GitHub Actions run [39985336539](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39985336539) remains **unverified**: the job returned no steps and log retrieval returned `BlobNotFound`. The run therefore does not show that any CI test executed. No bug/fix test pair, human review, accepted case, calibrated score, or formal model output was generated by these checks.


## Remote runner retry — 23 October 2026

The failed V10 metadata-reproducibility job was explicitly rerun. It again completed without recorded steps or uploaded artifacts, and log retrieval remained unavailable. Thus the checked-in Actions workflow still has no auditable remote execution result. This does not negate the separate artifact-backed local reproduction of the 501-row inventory, 407-row queue and exact frozen V10 order, but it blocks claiming the new verifier/workflow itself passed CI. No case tests or model outputs were produced.


## Kaggle çalıştırıcısı ve gizli koşul etiketi güvenliği — 23 Ekim 2026

Son protokol denetiminde `kaggle_stage3_p0_p1.py` içinde bir yöntemsel kusur tespit edildi: eski sürüm `evidence_level` etiketini prompt'a ekliyor, protokolün kanonik `OUTPUT_SCHEMA.json`/prompt metniyle uyuşmayan bir öz-bildirilen `confidence` alanı kullanıyor ve kanonik Stage 3 ön denetimini çağırmıyordu. Bu, gelecekteki çıktıları protokol dışına çıkarabilirdi. Düzeltme PR'ında çalıştırıcı prompt'undan gizli seviye etiketi kaldırıldı, model çıktısı kanonik şemaya hizalandı, geçersiz JSON için otomatik onarım/yeniden üretme engellendi, kanonik ön denetim inference kapısının zorunlu ön şartı yapıldı ve çalıştırıcı SHA-256 dondurulmuş dosya kümesine eklendi.

Bu düzeltme doğrulama amaçlı bir kod değişikliğidir; **model çağrısı yapılmadı ve deney izni açılmadı**. Yeni Python testlerinin uzak CI'da çalıştığı henüz gösterilemedi, çünkü en son GitHub Actions işleri runner atanmadan sona eriyor. Güncel kayıt ve depo sahibinin yapması gereken Actions/billing kontrolü: [issue #18](https://github.com/MahmutVezir/dijitalikiz/issues/18). Çalıştırıcıyı yeni haliyle doğrulamak için önce gerçekten adım kaydeden no-inference CI veya bağımsız yerel test yürütmesi gerekir.
