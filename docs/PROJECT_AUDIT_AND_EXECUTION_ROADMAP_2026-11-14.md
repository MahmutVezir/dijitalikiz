# 14 Kasım 2026 — Proje denetimi ve yürütme yol haritası

**Durum:** Ana araştırma henüz doğrulayıcı deney aşamasına geçmedi. Bu belge, mevcut depo durumunun denetimini ve bundan sonraki tek yürütme sırasını tanımlar. En güncel kanıt değiştikçe bu belge yeni tarihli sürümle güncellenmelidir.

## 1. Yönetici kararı

Araştırma fikri ve deney mantığı korunabilir; fakat veri kaynağı, eski deney manifesti ve uygulama belgeleri arasında sürüm ayrımı zorunludur. **Şu anda hiçbir model çıkarımı, fine-tuning veya doğrulayıcı vaka kabulü yapılmamalıdır.**

- Kabul edilmiş bağımsız vaka/proje: **0 / 0**.
- Doğrulayıcı model çıktısı: **0**.
- İnsan değerlendirme panelleri ve kalibrasyon: tamamlanmadı.
- Dışarıdan doğrulanabilir ön kayıt: yok; taslak.
- Model/tokenizer/runtime yükleme denetimi: tamamlanmadı.
- İstatistiksel sonuç: yok.

Bu nedenle P1'in daha güvenilir olduğu veya kanıtsız teşhisleri azalttığı ileri sürülemez.

## 2. Araştırmanın doğru ve tek kapsamı

**Araştırma sorusu:** Aynı sabit büyük dil modeli, aynı yazılım kusuru ve aynı kanıt paketi üzerinde çalışırken; yetersiz kanıtta cevap vermekten kaçınmaya izin veren P1 politikası, teşhisi zorunlu kılan P0 politikasına göre kanıtla desteklenmeyen kesin kök neden iddialarını azaltıyor mu? Bu farkın cevap kapsamı ve yeterli kanıtta gereksiz kaçınma maliyeti nedir?

- P0: model bir teşhis sunmak zorunda.
- P1: yalnızca kanıt teşhisi destekleyip makul alternatiflerden ayırıyorsa teşhis; aksi hâlde açık kaçınma.
- E1: yeterli kanıt; E2: kısmi kanıt; E3: yetersiz/ayırt edici olmayan kanıt.
- Her bağımsız vaka için altı hücre (E1/E2/E3 × P0/P1); altı çıktı altı bağımsız vaka değildir.
- Birincil sonlanım E3'te kanıtla desteklenmeyen kesin teşhis; vaka eşleştirmeli iki taraflı exact McNemar, risk farkı ve %95 güven aralığı.
- Hedef 80 vaka; doğrulayıcı alt sınır en az 60 bağımsız vaka ve en az 8 upstream proje. Bu sınır sonradan düşürülmez.
- **Doğru tahmin, kanıtla destekli teşhis değildir.** Modelin içsel belirsizliğini veya öz-farkındalığını ölçtüğümüz iddia edilmez; ölçtüğümüz şey sunulan kanıt ve cevap politikası arasındaki davranış farkıdır.

Ana deney sabit base model ve sabit tokenizer ile yürütülür. Fine-tuning ana P0/P1 karşılaştırmasına dahil değildir; ağırlık değişikliği politika etkisini karıştırır.

## 3. Veri kaynağı ve eski çalışmaların ayrımı

### 3.1 Güncel birincil aday kaynağı: SWE-rebench V2

12 Kasım tarihli ana durum dosyasına göre metadata fizibilitesi ve deterministik aday seçimi yapılmıştır:

| Kademe | Kayıt |
|---|---:|
| Pinned filtrelenmiş veri kümesi | 6.272 satır |
| Python alt kümesi | 1.952 |
| Model yayın tarihi filtresi sonrası | 349 |
| Tekrarlı/metadata filtreleri sonrası | 347 aday / 154 depo |
| Ön lisans ve bilinen maruziyet filtreleri sonrası | 261 aday / 113 depo |
| Birincil proje cohort'u | 96 proje adayı |
| Proje yedeği | 17 |
| Aynı proje içi alternatif | 148 |

İlk 56 adayın PR/base-commit eşleşmesi 56/56'dır. İlk 56 kayıtta 37 geçici bug adayı ve 19 kapsam dışı kayıt belirlenmiştir. İlk 16 adayın exact base commit kök lisans dosyası 16/16 Apache-2.0 olarak kontrol edilmiştir. **Bunların hiçbiri kabul edilmiş deney vakası değildir.** Patch/file kapsamı, NOTICE/üçüncü taraf bileşenler, exact buggy/fixed test çifti, kök neden ve bağımsız insan değerlendirmesi hâlâ gereklidir.

Ayrıca:
- Dataset kartındaki CC BY 4.0 beyanı, upstream kodu otomatik olarak CC BY 4.0 yapmaz.
- Her upstream depo ve kullanılan dosya, buggy ve fixed commit'lerde ayrı incelenmelidir.
- Model yayın tarihinden sonraki örneklerin seçilmesi kontaminasyon riskini azaltmaya yönelik bir filtredir; sıfır kontaminasyon kanıtı değildir.
- Veri kümesinin tarih alanlarının türü/zaman dilimi varsayımları ön kayıt öncesi doğrulanmalıdır.
- 96 proje adayı, 60 geçerli vaka garantisi vermez. Gerekirse açıkça tanımlı proje yedekleri, aynı lisans ve maruziyet kontrollerinden geçirilerek kullanılabilir; aynı depo içindeki alternatif yeni bir bağımsız proje sayılmaz.

### 3.2 BugsInPy: tarihsel/ayrı hat

BugsInPy için hazırlanmış V10/V12 metadata paketleri ve 105 kimlikli maruziyet listesi korunur; bunlar SWE-rebench vaka kimlikleriyle aynı şey değildir. BugsInPy dataset-level lisans/izin sorunu çözülmeden o kaynaktan yeni bir doğrulayıcı veri seti oluşturulamaz.

EXPERIMENT_MANIFEST_STAGE3.json hâlâ BugsInPy revizyonunu gösteren eski P0/P1 manifestidir. Bu dosya tarihsel/protokol kaydıdır; SWE-rebench deneyinin manifesti olarak kullanılmamalıdır. SWE-rebench birincil kaynak olarak resmen seçilecekse yeni, sürümlenmiş veri/protokol manifesti hazırlanmalı; eski manifest ve eski hash'ler geriye dönük değiştirilmemelidir.

### 3.3 Birbirinden ayrı tutulacak diğer hatlar

- UNCERTAINTY_EXPERIMENT_MANIFEST.json beş örneklemeli/entropy prototipini ayrı tanımlar. Bu prototip ana deterministik P0/P1 deneyinin parçası değildir.
- Tarihsel CCDG/160 kayıtlı deney arşivi eski araştırmadır. Yeni projenin veri seti, eğitim verisi, kalibrasyon seti veya doğrulayıcı sonucu olarak kullanılamaz.
- Gradio demo veya tekil smoke çalışmaları araştırma sonucu değildir.

## 4. Denetimde bulunan teknik ve yönetim sorunları

| Bulgu | Değerlendirme | Yapılacak işlem |
|---|---|---|
| Kaggle v2 manifest adı (BUNDLE_MANIFEST.json) | PR #158 ile canonical notebook 02 içinde kontrollü fallback olarak düzeltildi | Manifesti elle yeniden adlandırma; eski dataset/notebook eşlemesini karıştırma |
| 31 dosya / 19 dosya farkı | İki ayrı tarihli snapshot; aynı paketin sayım hatası değil | Notebook 02 yalnızca 27 Ekim v2; notebook 03 yalnızca 3 Kasım allowlist snapshot için |
| Ana Stage 3 runner'ın 24 Ekim 97-ID listesine bağlı kalması | Gerçek kod/manifest sözleşmesi tutarsızlığı | Bu PR'da runner'ı 11 Kasım 105-ID screening union'a hizala ve regresyon testi ekle |
| Kök README ve 11 Kasım runbook | 12 Kasım SWE-rebench veri kaynağı kararından sonra eskimiş | Kök README'ye güncel durum bloğu; 11 Kasım runbook'a superseded işareti |
| Stage3 manifesti ile yeni veri kaynağı | Stage3 manifesti BugsInPy; güncel ana aday SWE-rebench | Eski manifesti değiştirme; yeni kaynağı seçince yeni sürümlü manifest/protokol hazırla |
| 169 ve 165 açık PR'ları | Eski BugsInPy/V11 runner/metadata işlerine ait; yeni SWE-rebench kararını temsil etmiyor | Merge etme; kapanış/arsiv kararı ayrı ve açık olarak verilsin |
| 105-ID dışlama listesi | BugsInPy case-ID sözleşmesi | SWE-rebench satırlarına doğrudan taşınmaz; repo/PR/commit maruziyet eşlemesi dataset'e özgü yapılır |

### Güncel PR/CI bağlamı

- PR #157 birleştirilmiştir; önceki taslak durum bilgisi artık geçerli değildir.
- PR #158, Kaggle manifest fallback düzeltmesini birleştirmiştir.
- PR #168, Stage3 preflight ve analizde 105-ID screening union'ı hizalamıştır; ana runner'daki eski 24 Ekim referansı bu denetimde ayrıca bulundu ve bu PR dalında düzeltilmektedir.
- PR #170–178, SWE-rebench snapshot, metadata aday havuzu ve ilk 56 adayın kapsam/lisans incelemelerini kayda geçirmiştir.
- PR #176 no-inference preflight testi 13/13 ve evidence packet testini 12/12 geçmiş; aynı raporda ready=false, 21 engel, 0 kabul edilmiş vaka ve 0 model inference kaydedilmiştir. Testlerin geçmesi bilimsel hazır olma veya hipotez desteği değildir.
- PR #165 ve #169, eski BugsInPy V11/V12 akışına yönelik açık PR'lardır; yeni veri kaynağı rotası için birleştirilmemelidir.

## 5. Tek, aşamalı yürütme yol haritası

Her aşamanın **çıkış koşulu** sağlanmadan sonraki aşamaya geçilmez.

| Sıra | İş paketi | Çıkış koşulu / kanıt |
|---:|---|---|
| 1 | Veri kaynağını resmen dondur | SWE-rebench V2 exact snapshot, lisans/izin, zaman alanları ve veri kullanım koşulları yazılı olarak teyit; yeni manifest sürümü |
| 2 | 96 adayın metadata/PR/issue/commit denetimini tamamla | 96/96 base SHA, issue/PR kapsam kararı, exact depo kimliği ve maruziyet kaydı |
| 3 | Dosya/lisans/lineage denetimini tamamla | Her aday için buggy/fixed commit lisansı, dosya kapsamı, NOTICE/third-party ve gerekli izinlerin kaydı |
| 4 | Teknik reprodüksiyon kohortunu belirle | Önceden tanımlı teknik protokol ve sabit OS/Python/dependency matrisi; lisansı geçen adaylar |
| 5 | Hedef test çiftini çalıştır | Aynı vaka ve aynı hedef test: buggy sürümde kusura özgü başarısızlık, fixed sürümde başarı; ortam/kurulum hataları kabul edilmez; log, kaynak ve runtime hash'leri saklanır |
| 6 | Vaka ve kanıt paketlerini insanla doğrula | Panel A iki bağımsız inceleyici root-cause/test/lisans; Panel B Panel A'dan tamamen ayrı iki inceleyici E1/E2/E3 yeterliliği; ilk kararlar korunur; kalibrasyon ve adjudication kayıtlı |
| 7 | Örneklem durdurma kararı | En az 60 kabul edilmiş vaka ve 8 upstream proje; hedef 80. Sağlanmıyorsa doğrulayıcı çalışma iddiası kaldırılır, eşik düşürülmez |
| 8 | Protokolü dondur ve ön kaydet | Model/tokenizer/runtime, prompt, schema, örneklem, rubrik, analiz kodu, exclusion ledger ve tüm hash'ler; dışarıdan doğrulanabilir prereg URI |
| 9 | No-output runtime denetimi | Exact pinned model/tokenizer yüklenir; sürüm/dtype/CUDA/fingerprint doğrulanır; yanıt üretmez |
| 10 | Ayrı ve açık inference yetkisi | Lisans, veri kapısı, panel/onam, prereg, hash ve minimum N koşullarının tümü geçer; manifest/izin sadece kanıtla açılır |
| 11 | Ana deney | Vaka başına 6 deterministik çıktı; 60 vaka için 360, 80 vaka için 480 ham yanıt; retry/JSON repair yok; ham çıktılar hash'lenir |
| 12 | Kör puanlama ve istatistik | İki ayrı puan, adjudication, kappa/ham uyum, McNemar, RD, %95 CI, coverage ve E1 gereksiz kaçınma; eksik/invalid çıktı duyarlılık analizleri |
| 13 | Sağlamlık ve rapor | Proje-küme duyarlılığı, leave-one-project-out, sızıntı/kontaminasyon sınırlılıkları ve yeniden üretim paketi |
| 14 | TÜBİTAK raporu ve jüri denetimi | Yalnızca gerçekleşen sonuçlar; yöntem, veri akışı, etik/lisans, olumsuz sonuçlar, sınırlılıklar, AI kullanımı ve kaynaklar eksiksiz |

## 6. Kesin çalışma kuralları

1. Her görev bloğu tek bir somut çıktı üretir; azami 20 dakika.
2. Önce yalnızca metadata/statik inceleme; kaynak ve lisans kapısı geçmeden upstream test/build yok.
3. Teknik tarama ve hata ayıklamada açılan vaka, sonuca bakılmaksızın confirmatory havuzdan çıkarılır.
4. Vaka kabulünü model çıktısı veya LLM hakemi yapmaz; insan ve kaynak/test kanıtı yapar.
5. CASE_REGISTRY boş kalması şu an doğrudur; kanıt olmadan doldurulmayacak.
6. inference_allowed=false ve ayrı inference gate kapalı kalacak; readiness flag'i elle değiştirilmeyecek.
7. Fine-tuning yok; ana deney sabit temel modelde P0/P1 politika karşılaştırmasıdır.
8. Beş adaylı entropy/uncertainty prototype ayrı protokol, ayrı veri ve ayrı izin olmadan ana sonuca eklenmeyecek.
9. Her PR kendi branch'inde çalışır; main yalnızca test ve kanıt sonrası güncellenir.
10. Her aşama sonunda commit, PR, CI durumu, değişen dosyalar, kanıt ve kalan engeller kaydedilir.

## 7. Bir sonraki tek iş paketi

**81–88. adayların exact PR/base SHA ve bug/feature ayrımı**; eş zamanlı olarak 17–56 adaylar için exact commit lisans/NOTICE dosyası kontrollerinin eksiklerini tamamla ve 64. adayın repository redirect/base/license doğrulamasını kapat. 73–80 aralığında 73 (CrewAI) ve 78 (Narwhals) güçlü hata adayları; 80 (Dynaconf) exit-code sözleşmesi ön kayıtla dondurulursa aday; 79 (bump-my-version) commit-log kanıtı güçlendirilirse adaydır. 74–77 özellik/iyileştirme niteliği nedeniyle dışlanmıştır. Teknik yeniden üretime veya inference'a geçiş yok.

**Son karar:** Proje teknik altyapı ve aday veri araştırması bakımından ilerledi; araştırma sonucu bakımından henüz tamamlanmadı. Bu yol haritasının amacı daha fazla altyapı üretmek değil, her aday için gerçek kanıt toplayıp doğrulayıcı deneyin geçiş koşullarını sırasıyla kapatmaktır.


## 8. PR #179 doğrulaması — 14 Kasım 2026

PR #179: https://github.com/MahmutVezir/dijitalikiz/pull/179

- Evidence Abstention Preflight (No Inference), run 43618110359: **başarılı**. Fail-closed preflight ve evidence packet test adımları geçti.
- Repository/configuration validation, run 43618110310: **başarılı**. Tüm pytest paketi, compileall, tarihsel/yapılandırma kontrolleri ve no-inference güvenlik kontrolü geçti.
- Genel Research Validation workflow'u yine de **failure** olarak sonuçlandı; sebep ayrı Historical archive integrity job'ındaki eksik dosya kontrolüdür. Beklenen tarihsel ZIP dosyası main ağacında yoktur. Bu, kod/test job'ının başarısız olduğu anlamına gelmez.
- PR #179 main'e birleştirilmiştir. Kod düzeltmesi CI'da denenmiştir; genel workflow'un arşiv işi ayrı açık kalmıştır.
- PR #179'un kod işi no-inference kapsamındadır; model yüklenmedi, yanıt üretilmedi, vaka kabul edilmedi ve inference manifesti değiştirilmedi.

Eksik tarihsel dosya yolu: data/historical/confirmatory_artifact_2026-10-09.zip. Kütüphane kopyasının dosya boyutu **292,742 bayt**, SHA-256 değeri **e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd** ve ZIP CRC kontrolü başarılıdır. Bu arşiv yalnızca eski CCDG çalışmasının tarihsel kayıt bütünlüğü içindir; yeni belirsizlik/çekimserlik araştırmasının veri seti veya sonucu değildir.


## 9. Cohort rows 57–64 denetimi — 14 Kasım 2026

Detaylı kayıt: [SWE-rebench V2 case scope audit 57–64](../research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_57_64_2026-11-14.md).

- Sabit cohort CSV ve manifest hash'leri doğrulandı; GitHub Actions artifact 13960884569 indirildi, ZIP CRC kontrolü geçti ve iç CSV/manifest SHA değerleri beklenen değerlerle eşleşti.
- 57–63 satırlarında PR base SHA 7/7 eşleşti ve exact-base root LICENSE 7/7 incelendi.
- Bu yedi satırın beşi defect candidate olarak tutuldu, ikisi feature/usability isteği olduğu için dışlandı.
- 64. satır için resmi release note bugfix kaydı bulundu; repository redirect nedeniyle base SHA ve exact-base root license henüz doğrulanamadı. Provisional olarak tutulur.
- Satır 57–64 için upstream target test çalıştırılmadı; kabul edilen vaka hâlâ 0; insan adjudication ve model inference yapılmadı.


## 10. Cohort rows 65–72 denetimi — 14 Kasım 2026

Detaylı kayıt: [SWE-rebench V2 case scope audit 65–72](../research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_65_72_2026-11-14.md).

- Sabit 96 satırlı cohort CSV/manifest hash'leri yeniden doğrulandı; indirilen Actions artifact ZIP CRC kontrolünden geçti.
- Sekiz adayın PR base SHA'sı cohort'taki pinned base commit ile **8/8** eşleşti.
- Sekiz adayın exact-base root license dosyası bulundu; MIT veya MIT-style permission metinleri kaydedildi. Root `NOTICE` dosyası hiçbirinde bulunmadı; nested NOTICE, dosya-bazlı lisans ve üçüncü taraf kapsamı ayrıca açık.
- Beş aday (polyfactory #728, Pyccel #2038, Stingray #858, softlayer-python #2214, virtualenv #2907) izole teknik yeniden üretim için önceliklendirildi.
- attrs #1417 koşullu tutuldu; PR regresyon testi issue'daki inherited-subclass MCVE'yi tam temsil etmiyor.
- trimesh #2312 issue düzeltmesini içeriyor, ancak geniş ve çok konulu release PR'ı olduğundan tek görevli doğrulayıcı örneklem için bekletildi.
- pydap #481, mevcut hatanın tekrarı yerine DAP2/DAP4 API tutarlılığı ve `dimensions` → `dims` değişikliğidir; defect örnekleminden çıkarıldı.
- Upstream target testleri çalıştırılmadı; kabul edilen vaka sayısı değişmedi (**0**); insan adjudication ve model inference yapılmadı.


## 11. PR #182 doğrulaması — 14 Kasım 2026

PR #182: https://github.com/MahmutVezir/dijitalikiz/pull/182  
Merge commit: `7296e8cdcffd193c5347d3ffb398c9725240ea91`.

- Evidence Abstention Preflight (No Inference), run **43621535584**: başarılı. Fail-closed preflight testleri **13/13**, evidence-packet auditor testleri **12/12** geçti.
- Research Validation (No Inference), run **43621535481**: Repository/configuration validation işi başarılı tamamlandı.
- Aynı workflow'un ayrı Historical archive integrity işi, `data/historical/confirmatory_artifact_2026-10-09.zip` dosyası main çalışma ağacında bulunmadığı için başarısız oldu. Bu nedenle arşiv boyutu/hash/ZIP CRC ve içerik denetimi adımları atlandı. Bu, repository/configuration testlerinin başarısız olduğu anlamına gelmez.
- Preflight artefaktındaki `readiness-report.json`: `ready=false`, **21** blokaj, **0** kabul edilmiş vaka, **0** kabul edilmiş proje ve `model_inference_performed=false`.
- PR değişiklikleri yalnızca README/yol haritası/denetim raporu dokümantasyonudur. Upstream target test, insan adjudication, model load, inference veya training yapılmadı.
- Tarihsel ZIP engeli hâlâ açıktır; doğru arşiv geri yüklenip sabit SHA-256 ve ZIP bütünlüğü doğrulanmadan tarihsel archive job başarılı sayılmayacaktır.

**Sonuç:** Kod/konfigürasyon ve no-inference preflight kontrolleri geçti; genel Research Validation durumu arşiv dosyası eksikliği nedeniyle başarısızdır. Bilimsel veri kapısı ve inference izni kapalı kalır.


## 12. Cohort rows 73–80 denetimi — 14 Kasım 2026

Detaylı kayıt: [SWE-rebench V2 case scope audit 73–80](../research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_73_80_2026-11-14.md).

- Sabit cohort CSV SHA-256 `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`, manifest SHA-256 `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`; Actions ZIP CRC kontrolü geçti.
- Sekiz PR base SHA'sı cohort'taki pinned base commit ile **8/8** eşleşti.
- Sekiz adayın exact-base root LICENSE dosyası bulundu. Root `NOTICE` yalnızca APIFlask'ta bulundu; APIFairy, Flask ve Flask-Marshmallow üçüncü taraf kayıtları içeriyor.
- CrewAI #2408 (73) ve Narwhals #1869 (78) güçlü hata adayları olarak teknik yeniden üretim kuyruğuna alındı.
- Dynaconf #1293 (80) için missing-key exit status sözleşmesi açıkça sabitlenmeli; bump-my-version #325 (79) için Mercurial commit log'unu doğrulayan daha güçlü assertion hazırlanmalı.
- AzureTRE #4352, aiogram #1657, APIFlask #642 ve XKNX #1663 özellik/iyileştirme/entegrasyon genişletmesi olarak defect örnekleminden çıkarıldı.
- Upstream target testleri çalıştırılmadı; vaka kabul edilmedi (**0**); insan adjudication ve model inference yapılmadı.


## 13. PR #183 doğrulaması — 14 Kasım 2026

PR #183: https://github.com/MahmutVezir/dijitalikiz/pull/183  
Merge commit: `e17eb6a107f3c9dee6dc7dc107ad0d0647ae1724`.

- PR #183'ün Research Validation run **43621956695** içinde repository/configuration validation işi başarılı tamamlandı.
- Ayrı Historical archive integrity işi yine `data/historical/confirmatory_artifact_2026-10-09.zip` dosyasını canonical repository yolunda bulamadığı için başarısız oldu; arşiv size/SHA-256/CRC adımları atlandı.
- PR #183 yalnızca README ve yürütme yol haritasını güncelledi; deney protokolü, case registry, inference authorization veya model runtime değiştirilmedi.
- En son mevcut preflight artefaktı PR #182 run **43621535584**'tür: `ready=false`, 21 blocker, 0 accepted case/project, `model_inference_performed=false`. PR #183 dokümantasyon-only olduğundan bu bilimsel kapıları değiştirmez.

**Sonuç:** Repository/configuration doğrulaması geçti; genel workflow tarihsel arşiv eksikliği yüzünden başarısızdır. Bu iki sonucu tek bir “CI geçti” veya “CI tamamen bozuk” hükmünde birleştirme.
