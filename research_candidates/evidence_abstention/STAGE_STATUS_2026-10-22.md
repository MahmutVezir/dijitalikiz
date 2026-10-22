# Aşama Durum Raporu — 22 Ekim 2026

**Araştırma:** Belirsizlik altında kanıtla desteklenmeyen kesin teşhisten kaçınma  
**Hedef:** 2027 TÜBİTAK 2204-A için tamamlanmış ve savunulabilir araştırma  
**Karar:** Aşama 1, 2 ve 3'ün bilimsel/deneysel kapanışı henüz sağlanmadı. Aşama 3'ün yazılım prototipi ve testleri hazır; gerçek model deneyi kapalı. Aşama 4 model çıkarımı başlatılmadı.

## Durum özeti

| Aşama | Bugünkü durum | Kanıt |
|---|---|---|
| 1 — Veri, protokol ve bağımsız doğrulama | Açık | 501 ham metadata kaydı / 17 proje; kabul edilmiş doğrulayıcı vaka sayısı 0. V8'in ilk 8 adayı ile workflow doğrulaması sırasında çalıştırılan offset-8 grubu kalıcı olarak dışlandı (16 ID). V9 intake: 100 aday / 13 proje. V9 offset-0 taraması tamamlandı (run 39832920370); 8 vaka artefaktı denetlendi, iki vaka yalnızca insan inceleme kuyruğuna alındı. |
| 2 — Model ve çalıştırma hattı | Kısmen uygulandı | Qwen adapter'ı, ayrı inference kapısı ve sabit model/tokenizer yüklemesi için çıktısız ön kontrol kodu var. CPU CI testleri geçti; gerçek CUDA yükleme denetimi yapılmadı. Runtime manifestinde doğrulama hâlâ `not_run`. |
| 3 — Belirsizlik, kalibrasyon ve kaçınma | Yazılım prototipi test edildi; model davranışı doğrulanmadı | Normalize token entropisi, çoklu yanıt ayrışması, ampirik kalibrasyon, Brier/ECE, fail-closed karar katmanı ve katı JSON parser mevcut. Son Qwen prototip CI çalışmasında 42 test geçti; bunlar sentetik/CPU yazılım testleridir, model performansı sonucu değildir. |
| 4 — Önceden kaydedilmiş gerçek deney | Başlamadı | Kabul edilmiş veri, gerçek GPU runtime doğrulaması, dolu bağımsız kalibrasyon kümesi, dondurulmuş artefakt hash'leri, doğrulanabilir ön kayıt, operasyonel kanıt-yeterliliği değerlendiricisi ve ayrı yürütme izni yok. |

## Aşama 1 — V8 teknik tarama sonucu

Sabit kaynak revizyonu BugsInPy 11c5f1eea954a42132cfd06bf257766a7963e0fd üzerinde, metadata sırası korunarak sekiz aday kontrol edildi. İş akışı: [GitHub Actions run 39818472947](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39818472947).

- **FastAPI-5, Keras-4, Scrapy-5, Sanic-5:** kayıtlı Python sürümü eşleşti; buggy revision'daki hedef test başarısız, fixed revision'daki aynı hedef test başarılı; artefakt hash denetimi geçti. Bunlar yalnızca bağımsız kök-neden incelemesine aktarıldı.
- **Black-6:** buggy günlükte eksik test fixture'ı veya harness dosyası uyarısı.
- **Matplotlib-4:** ortam/bağımlılık hatası sinyali; fixed hedef test de başarısız.
- **Luigi-5:** runtime Python metadata ile açıkça eşleşmedi veya tutarlı biçimde kaydedilemedi.
- **Pandas-4:** pinlenmiş pytest kurulumu, hedef test her iki revision'da da çalıştırılmadan önce başarısız oldu.

Ham artefaktlar ve SHA-256 değerleri [V8 insan inceleme kuyruğunda](STAGE1_MANUAL_REVIEW_QUEUE_V8_2026-10-22.json) kaydedildi. Bu rapor hiçbir vakayı kabul etmez. İnsan kök-neden paneli, ayrı ve disjoint kanıt yeterliliği paneli, lisans/provenance, leakage ve vaka bağımsızlığı kontrolleri hâlâ zorunludur. Global kabul eşiği en az 60 bağımsız vaka ve en az 8 upstream projedir; hedef 80 vakadır.

## 22 Ekim ek teknik ilerleme

- Deterministik tarama matrisine `--batch-offset` eklendi; 8'li gruplar sabit sıra korunarak seçiliyor. Negatif/uyumsuz offset, eksik grup, kaynak hash değişimi, prior-exposure yeniden eklenmesi ve tek grupta yinelenen upstream proje testlerde reddediliyor.
- Metadata-only cohort builder için 4 test paketi — toplam 19 test — geçti: [Actions run 39831836486](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39831836486). Bu, adayların buggy/fixed testlerini çalıştırdığı anlamına gelmez.
- Teknik vaka tarama iş akışı artık `workflow_dispatch` ile elle çalıştırılacak şekilde ayarlandı; normal push/PR değişikliklerinin aynı vakaları yanlışlıkla tekrar çalıştırıp maruziyet yaratması önleniyor. V8 offset 8 grubunun testleri tamamlandı; grubun tamamı doğrulayıcı örneklemden dışlandı. Yeni V9 offset-0 koşusu ayrı tek-seferlik dalda tamamlandı; sonuçların özeti aşağıdaki son güncellemede yer alıyor.
- Çıktı üretmeyen Qwen çalışma-zamanı ön kontrolü eklendi. En son CPU testleri: [Actions run 39831582614](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39831582614) ve [Actions run 39831583513](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39831583513), ikisi de başarılı. Ön kontrol kodunun CI testleri geçti; gerçek Qwen ağırlıkları bu testlerde yüklenmedi.
- Yeni inceleme PR'leri: [PR #82 — çıktısız Qwen runtime ön kontrolü](https://github.com/MahmutVezir/dijitalikiz/pull/82) ve [PR #83 — deterministik grup taraması](https://github.com/MahmutVezir/dijitalikiz/pull/83). İkisi de taslak; ana dala merge edilmiş sayılmıyor.

## Aşama 2 — Model bağlantısı

Qwen adapter'ı beş önceden tohumlanmış aday üretimini, her adayın ham çıktısını/hash'ini ve üretilen tokenların Transformers generation-score entropisini kaydedebilecek teknik altyapıya sahip. Skorlar decoding işlemcilerinden sonra gelen generation scores'tur; ham base-model logits diye adlandırılmıyor.

Buna rağmen:
- tam model/tokenizer/runtime yükleme doğrulanmadı;
- inference için yeterli kabul edilmiş vaka ve gözden geçirilmiş kalibrasyon verisi yok;
- bağımsız kanıt desteği ve çelişki değerlendirme modülü üretimde doğrulanmadı;
- ana doğrulayıcı manifestinde inference izni kapalı kaldı.

## Aşama 3 — Mevcut mekanizma ve yöntem sınırları

Uygulama; normalize token entropisi, yanıtlar arası sözcüksel Jaccard ayrışması, yeterli örnek bulunduğunda Laplace-yumuşatılmış ampirik kalibrasyon, Brier skoru, ECE ve eksik/çelişkili kanıt, geçersiz referans, eksik sinyal veya kalibrasyon yokluğunda fail-closed karar içeriyor. Bir model açıkça kaçınma istediğinde karar katmanı bunu teşhise çevirmiyor.

Son doğrulanan test akışı: [Actions run 39821402510](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39821402510). Ayrı, salt-okunur inference hazırlık kapısı: [Actions run 39821402359](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39821402359).

Bu durum modelin halüsinasyon oranının düştüğünü kanıtlamaz. Aynı modelin tekrarlı örneklemeleri saf epistemik belirsizlik ölçüsü değildir; decoding değişkenliğini de içerir. Sözcüksel ayrışma semantik eşdeğerlik ölçüsü değildir. Kalibrasyon verisi boş olduğundan geçerli bir güven olasılığı henüz yoktur. Ayrıca veri setindeki gold E1/E2/E3 etiketi karar motoruna runtime tahmini gibi verilmemelidir; böyle yapmak cevaplanabilirlik koşulunu sızdırır ve testi döngüsel hâle getirir. Ayrı runtime kanıt-yeterliliği değerlendiricisi henüz doğrulanmadı.

## Aşama 4'e geçiş kriterleri

Gerçek model deneyi ancak aşağıdaki bütün koşullar kapandıktan sonra yürütülmelidir:

1. En az 60 kabul edilmiş bağımsız hata vakası / en az 8 ayrı upstream proje; hedef 80.
2. Aynı kayıtlı Python/runtime'da buggy-fail ve fixed-pass hedef test günlükleri; doğrulanmış kaynak, lisans, root-cause ground truth ve önceki maruziyet/leakage denetimi.
3. Kök neden için en az iki bağımsız değerlendirici ve bu panelle çakışmayan iki kanıt yeterliliği değerlendiricisi; hazırlanmış E1/E2/E3 paketleri.
4. Qwen ve tokenizer'ın sabit revision ile no-output runtime yükleme denetimi; runtime ve chat-template fingerprint'lerinin kaydı.
5. Ayrı, gerçek etiketli kalibrasyon kümesi; threshold'ların bağımsız validation verisinde seçilip dondurulması; gereken artefakt SHA-256 değerlerinin doğrulanması.
6. Deney protokolünün sonuçlar görülmeden doğrulanabilir biçimde ön kaydı ve ayrıca açık yürütme izni.

Mevcut ayrı manifest bu koşulları karşılamıyor ve bilerek inference_allowed=false tutuyor. Bu nedenle gerçek Qwen inference veya halüsinasyon azalması iddiası bu raporun parçası değildir.

## İlgili pull request'ler

- [PR #79 — Qwen belirsizlik adapter'ı ve kapalı çıkarım altyapısı](https://github.com/MahmutVezir/dijitalikiz/pull/79)
- [PR #80 — V8 teknik tarama ve bağımsız insan inceleme kuyruğu](https://github.com/MahmutVezir/dijitalikiz/pull/80)

Her iki PR da taslak durumundadır; ana dalın bilimsel vaka sicili değiştirilmemiştir.

## V8 maruziyet kararı ve V9 başlangıcı — 22 Ekim 2026

- Offset-8 koşusu [39830777415](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39830777415) tamamlandı: 6/8 teknik buggy-fail/fixed-pass sinyali; 2/8 vaka her iki sürümde test-harness/bağımlılık hatasına düştü. İki grubun tamamı maruziyet nedeniyle doğrulayıcı örneklemden outcome-independent olarak çıkarıldı.
- Önceki deneme [39830674411](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39830674411) selection artifact publish aşamasında başarısız oldu; bu koşuda vaka testleri başlatılmadı.
- On altı dışlama `EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json` dosyasına yazıldı; önceki 21 Ekim logu değiştirilmedi. Dört eski ve altı yeni teknik sinyal, [keşifsel kök-neden inceleme devir dosyasında](STAGE1_EXPLORATORY_REVIEW_HANDOFF_2026-10-22.md) birleştirildi. Bu 10 kayıt doğrulayıcı örnekleme uygun değildir.
- Yeni intake `SCREENING_COHORT_100_V9_2026-10-22.json`: 100 kalan metadata ID'si, 13 upstream proje; ilk 16 V8 ID'si dışlama listesine alındı. `CASE_REGISTRY.json` güncellendi ama `records` hâlâ boş ve kabul sayısı 0.
- V9 ilk sekiz vaka tek seferlik dalda taranıyor: [Actions run 39832920370](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39832920370). Matrix freeze başarılı oldu; bu raporun son güncellemesinde tüm vaka artefaktları henüz tamamlanmadığından hiçbir V9 teknik sonucu sınıflandırılmadı.
- Metadata-only seçim testleri [39831836486](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39831836486) başarılıdır (toplam 19 test). Bu testler veri seçme kodunu doğrular; gerçek buggy/fixed vaka testlerini veya model davranışını doğrulamaz.



## Son güncelleme — V9 batch 0 artefaktları tamamlandı

**İş akışı:** [39832920370](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39832920370). Tüm 8 vaka işi tamamlandı; matrix freeze işi başarılı.

- **Keras-5:** Python 3.7.3 metadata/runtime eşleşmesi; hedef test buggy tarafında başarısız, fixed tarafında başarılı; artefakt SHA denetimi geçti.
- **Tornado-6:** Python 3.7.0 metadata/runtime eşleşmesi; iki hedef test buggy tarafında başarısız, fixed tarafında başarılı; artefakt SHA denetimi geçti.
- **Scrapy-6:** buggy ve fixed test kümeleri geçerli fail/pass çifti oluşturmadı.
- **Matplotlib-5 ve TheFuck-6:** ortam/bağımlılık veya harness belirsizliği; geçerli fail/pass çifti yok.
- **Luigi-6:** runtime Python bilgisi tutarlı biçimde kaydedilmedi.
- **SpaCy-5:** ortam kurulumu hedef testten önce başarısız.
- **Pandas-5:** pinned pytest bootstrap iki tarafta da hedef testten önce başarısız; hedef test sonucu yok.

Tüm sekiz aday hâlâ `accepted_for_confirmatory=false`. **Teknik sinyal veren iki aday, kabul edilmiş vaka değildir.** Ayrıntılı kayıtlar [V9 insan inceleme devir raporunda](STAGE1_V9_BATCH0_REVIEW_HANDOFF_2026-10-22.md) ve JSON hash manifestinde tutulur. [PR #87](https://github.com/MahmutVezir/dijitalikiz/pull/87) taslak/açık durumdadır; kabul sicilini değiştirmez.

## Protokol ilerlemesi

- [PR #86](https://github.com/MahmutVezir/dijitalikiz/pull/86) birleştirildi: bağımsız ve körlenmiş değerlendirici rubriği ile ön kayıt taslağı ana dala eklendi.
- [PR #88](https://github.com/MahmutVezir/dijitalikiz/pull/88) taslak/açık: kalibrasyon protokolü ve fail-closed güven eşiği kuralları.
- Bu belgeler **taslak** durumundadır; kayıtlı ön kayıt URI'si, reviewer kimlikleri, kalibrasyon etiketleri veya dondurulmuş eşikler oluşturulmuş değildir.

## Nihai durum ve karar

1. **Aşama 1 — açık:** V9 batch 0 iki teknik inceleme adayı sağladı; kabul edilen bağımsız vaka sayısı hâlâ 0. En az 60 kabul edilmiş vaka / en az 8 upstream proje eşiği karşılanmadı.
2. **Aşama 2 — kısmen hazır:** Qwen adapter ve no-output runtime preflight kodu mevcut; gerçek CUDA model yüklemesi henüz doğrulanmadı.
3. **Aşama 3 — yazılım prototipi mevcut, bilimsel doğrulama eksik:** CPU testleri geçmiştir. Kalibrasyon kümesi boş; bağımsız runtime anlamsal kanıt-desteği/çelişki değerlendiricisi henüz doğrulanmamıştır. Modelin gerçek abstention başarısı ölçülmedi.
4. **Aşama 4 — başlatılmadı:** Gerçek model çıkarımı, ön kayıt, kalibrasyon, kabul edilmiş vaka sicili ve açık yürütme izni olmadan çalıştırılmamalıdır.

Bu aşamada otomatik olarak tamamlanabilecek dosya/CI işleri büyük ölçüde hazırdır. Kalan kritik işler bağımsız insan değerlendirmesi, erişim kontrollü kör paketlerin hazırlanması, kalibrasyon etiketleri, gerçek Kaggle/CUDA no-output runtime doğrulaması ve dışarıdan doğrulanabilir ön kayıttır. Bunları yapmış gibi göstermek bilimsel olarak yanlış olacağından inference kapısı kapalı kalır.

## Additional clarification — Kaggle exploratory smoke audit

On 22 October 2026, a **separate engineering smoke** completed on Kaggle: [GitHub Actions run 39837255019](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39837255019), kernel `mahmutvezir/qwen-e1-p0-p1-ansible4-ddc46f9e-39837255019-1`, artifact SHA-256 `f35f33029b0a42610e2d2ad2bfb6cedc90f2f9d7e0b14e632787872ae2a2e10d`. It produced 10 outputs on the previously exposed Ansible-4 case (five per policy); both policies produced 5/5 diagnoses, 0/5 model abstentions and 0/5 matches under a provisional automated rubric. The included file checksums passed.

This run is **not** an official or confirmatory result and does not contradict the “Stage 4 not started” status for the registered uncertainty experiment. The smoke used a separate prompt template that showed the full patch and successful fixed-test output to the model, contrary to the frozen study prompt protocol. It also used Python 3.13.15 / torch 2.11.0+cu128 / transformers 4.48.3 rather than the dedicated study runtime lock. Confidence values were model self-reports, not calibrated probabilities. See [full smoke audit](../docs/EVIDENCE_ABSTENTION_KAGGLE_SMOKE_AUDIT_2026-10-22.md).

PR [#91](https://github.com/MahmutVezir/dijitalikiz/pull/91) merged the Qwen adapter fix to pass an explicit attention mask and fail closed on candidate prompt/seed integrity defects. The CI run at the time caught two stale test assertions in the wider suite; repairs are being submitted separately. The registered study's inference manifest remains closed and the accepted case registry remains empty.

The two one-off Kaggle smoke workflow definitions used for engineering checks have now been preserved as inactive historical files outside `.github/workflows/`. This addresses the repository's single-canonical-Kaggle-workflow validation without deleting the historical run or its outputs. The official inference manifest remains closed.

## Son güncelleme — V9 offset-8 tarama ve maruziyet koruması

**Workflow:** [39841744307](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39841744307). Sekiz vaka için dondurulmuş seçim artefaktı doğrulandı. Altı hedefte buggy-fail/fixed-pass teknik sinyali var: Tqdm-6, YouTube-dl-6, Ansible-6, Black-8, FastAPI-7 ve Keras-6. Bunlar kabul edilmiş vakalar değildir; patch/test diff'leri, lisans ve kök neden bağımsız insan incelemesi bekliyor. Luigi-7'de pinli pytest kurulumu iki tarafta da başarısız oldu; Matplotlib-6 matrix işi vaka artefaktı üretmeden başarısız oldu. Hiçbir model çıkarımı yapılmadı.

Ayrıntılı handoff: [STAGE1_V9_OFFSET8_REVIEW_HANDOFF_2026-10-22.md](STAGE1_V9_OFFSET8_REVIEW_HANDOFF_2026-10-22.md). Ham vaka ve hash bilgileri: [EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json](EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json). Bu grubun sekiz ID'sinin tamamı, sonuçlarından bağımsız olarak doğrulayıcı örneklemden kalıcı şekilde dışlandı; toplam exposure ledger 32 ID içeriyor ve CASE_REGISTRY boş.

## Kuyruk koruması ve CI durumu

Erişim/örneklem maruziyetini önleyen kuyruk oluşturucu ana dala alındı. Oluşturucu tarihli exposure ledger'ı okuyor, bütün kaydedilmiş ID'leri atlıyor, ledger SHA-256'sını özet kaydına yazıyor ve ledger bozuk/tutarsızsa fail-closed davranıyor. Ancak bu değişikliklerden sonra metadata-builder ve genel Research Validation CI işlerinde başarısızlık görüldü. GitHub Actions günlükleri mevcut erişim yolunda alınamadığından neden henüz doğrulanmadı; bu nedenle son genel doğrulamanın geçtiği iddia edilmiyor. Sonraki mühendislik önceliği bu regresyonu tanılamak ve tüm CI kontrollerini yeşile çevirmek. Bilimsel inference kapısı açık değil.
