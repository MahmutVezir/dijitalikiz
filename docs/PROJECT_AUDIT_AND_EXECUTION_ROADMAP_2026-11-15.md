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

**17–56 lisans/provenans denetimi sonuçlarını vaka düzeyinde kapat; ardından güçlü adaylar için fail-to-pass test yeniden üretim planı hazırla.** 17–56 için exact-base root lisans 40/40, PR/base SHA 40/40, root NOTICE 2/40 ve 151 changed-file path statik taraması tamamlandı. Ancak row 19 Napalm #2152'de eklenen Cisco NX-OS `show_version.txt` fixture'ının kaynağı/yeniden dağıtım izni açıklığa kavuşmadı; bu fixture kullanılmamalı ve vaka provenans hold'da kalmalı. Diğer aralıklarda da seçilecek her vakanın gerçek changed source/test dosyaları ve nested lisansları ayrıca kontrol edilmeli. 64. adayın repository redirect/base/license engeli çözüldü. 89–96 statik taraması tamamlandı. Upstream target test veya inference başlatma; önce seçilecek adayların lisans/provenans ve test-oracle kapılarını kapat.

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


## 16. Cohort rows 81–88 ve row 64 redirect çözümü — 14 Kasım 2026

Detaylı kayıt: [SWE-rebench V2 case scope audit 81–88](../research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_81_88_2026-11-14.md).

- Sabit 96 satırlı CSV: 17.409 byte, SHA-256 `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`; manifest: 2.711 byte, SHA-256 `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`; cohort ZIP SHA-256 `d9d1fc04cb84233c021006f13205623ea9aa390caa6eb54ca4bc9d974e9a4c6c`; ZIP CRC check passed.
- Sekiz PR base SHA'sı pinned cohort base commit ile **8/8** eşleşti. Sekiz exact-base root LICENSE dosyası bulundu; root NOTICE **0/8**.
- python-tabulate #362 (82), Copier #1998 (84) ve markdownify #202 (87) güçlü hata adaylarıdır.
- subliminal #1218 (81), Packit #2556 (86) ve cloudpathlib #474 (88) koşullu tutuldu; sırasıyla issue/enhancement kapsam karışımı, `--config`/ `--config-path` long-option farkı ve geniş Python 3.13 uyumluluk patch'i giderilmeden kabul edilmeyecek.
- pyjanitor #1451 (83) ve frictionless-py #1729 (85) özellik/iyileştirme talepleri olduğundan hata örnekleminden çıkarıldı.
- Upstream target tests, human adjudication, inference veya training yapılmadı; kabul edilen yeni vaka **0**.

### Row 64 transfer/redirect resolution

- Eski `OceanParcels/Parcels` repository adresi yeni owner `Parcels-code/Parcels` üzerinden doğrulandı.
- PR #1723 base SHA, cohort'taki `a1f76d2f7ca4b50de874e61b752ec8ccaf50283e` ile birebir eşleşti.
- Linked bug issue #1722 bulundu; exact-base `LICENSE.md` (MIT) blob `ad992e728bfe484b4e761b455a2d2adce29a0a7f` doğrulandı; root NOTICE yok.
- Bu işlem row64'ün repository redirect/base/root-license metadata blocker'ını kapatır. Row64 hâlâ yalnızca adaydır; fail/pass execution ve insan adjudication yapılmadı.

### Rows 89–96 candidate screen — 14 November 2026

- Static audit report: [SWE-rebench V2 rows 89–96](../research_candidates/evidence_abstention/SWE_REBENCH_V2_CASE_SCOPE_AUDIT_89_96_2026-11-14.md).
- All eight PR base commits match the frozen cohort base SHA (**8/8**); all eight pinned base commits contain an identifiable root LICENSE (**8/8**).
- Root NOTICE is present in **1/8** repositories: cfn-lint (row 96), attributing cfn-flip to Amazon. The other seven have no root NOTICE in the exact-base tree; this is not proof that nested or per-file third-party notices are absent.
- Strong static defect candidates: pyfar #722 (90), PyDESeq2 #349 (94), and pdoc #813 (95).
- Conditional candidates: pyairtable #422 (91), DSPy #1853 (92), Faker #2203 (93), and cfn-lint #3991 (96). Conditions: issue-contract ambiguity; broad serializer/enum changes; missing explicit uniqueness assertions; and incomplete handling of the second validation condition in the cfn-lint issue, respectively.
- FastCRUD #190 (89) is excluded because the PR combines multiple unrelated behaviors/root causes.
- Repository redirects were resolved: FastCRUD now lives at `benavlabs/fastcrud`; PyDESeq2 now lives at `scverse/PyDESeq2`. In both cases the exact pinned base SHA still matched.
- No target tests, human adjudication, model inference, or training were performed. Newly accepted confirmatory cases remain **0**.

**Çıkış durumu:** Statik aday taraması **96/96** satıra ulaştı. 89–96 aralığında 3 güçlü aday, 4 koşullu aday ve 1 dışlama belirlendi; doğrulayıcı kabul edilen vaka hâlâ **0**. 17–56 lisans/NOTICE ve tüm aralıklardaki nested NOTICE/üçüncü taraf/dosya düzeyi provenance incelemesi açık kalır.

### PR #187 CI and readiness snapshot — 14 November 2026

- PR: [#187 — Audit SWE-rebench V2 cohort rows 89–96](https://github.com/MahmutVezir/dijitalikiz/pull/187), draft/open; not merged at the time of this snapshot.
- No-inference preflight run [43631185613](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43631185613): 13/13 fail-closed preflight tests passed; 12/12 evidence-packet/citation-auditor tests passed.
- Readiness JSON from that run: `ready=false`; `blocker_count=21`; `accepted_case_count=0`; `accepted_project_count=0`; `model_inference_performed=false`.
- Repository/configuration validation in run [43631185664](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43631185664): **414 tests and 56 subtests passed**.
- The separate Historical archive integrity job in the same run failed at the canonical-file presence gate: `data/historical/confirmatory_artifact_2026-10-09.zip` was not present in the repository. Archive size/hash/CRC and historical-record audit steps were skipped. This remains an unresolved reproducibility/evidence blocker.
- CI success confirms the tested repository/configuration and no-inference safety checks only. It does not establish dataset validity, accepted cases, human agreement, preregistration, model/runtime readiness, or permission to run inference.




## 17. Rows 17–56 lisans/provenans durumu düzeltmesi — 14 Kasım 2026

Detaylı rapor: [SWE-rebench V2 rows 17–56 exact-base license and file-provenance audit](../research_candidates/evidence_abstention/SWE_REBENCH_V2_LICENSE_PROVENANCE_AUDIT_17_56_2026-11-14.md).

- Exact PR/base SHA eşleşmesi: **40/40**.
- Exact-base root LICENSE veya license symlink: **40/40**.
- Root NOTICE: **2/40** (Napalm row 19, Modin row 22).
- PR changed-file paths: **151**; hiçbir PR LICENSE/NOTICE/COPYING/third_party adlı bir path değiştirmedi.
- Row 19 Napalm #2152, Cisco NX-OS copyright ve GPL/LGPL bileşen notları içeren `show_version.txt` test fixture'ı ekliyor. Bu fixture için kaynak ve yeniden dağıtım dayanağı netleşmedi; benchmark evidence packet'e kopyalanmamalı. Aday vaka bu provenance hold çözülmeden kabul edilmemeli.
- Nested lisanslar ve dosya düzeyi köken kayıtları seçilecek her vaka için ayrıca incelenmeli; root LICENSE tek başına yeterli değil.
- Bu denetim hiçbir vakayı CASE_REGISTRY'ye eklemez; kabul edilmiş vaka sayısı **0** ve inference izni kapalıdır.

**Tarihsel arşiv notu:** 9 Ekim 2026 CCDG ZIP'inin iki ayrı Library kopyası 14 Kasım'da yerel olarak doğrulandı: her biri 292,742 bayt, SHA-256 `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd`, 214 ZIP girdisi, 214 benzersiz ad ve CRC hatası yok. Arşiv GitHub çalışma ağacında hâlâ bulunmuyor; bu nedenle Research Validation historical archive job'ı henüz başarılı sayılamaz. Bu eski CCDG arşivi yeni çekimserlik çalışmasının verisi değildir.


## 18. Napalm row 19 fixture identity/provenance follow-up — 14 November 2026

- Issue [#2151](https://github.com/napalm-automation/napalm/issues/2151) comment contains the user's raw NX-OS output; PR [#2152](https://github.com/napalm-automation/napalm/pull/2152) adds a 50-line mock fixture.
- Both contain `NXOS: version 10.3(5) [Maintenance Release]`, which is the parser-relevant line.
- They are not the same full output: issue comment reports Cisco copyright 2002–2024, Nexus9000 C93180YC-FX3, serial ABC12345DE, uptime 1d 1h 11m 11s, System version 10.2(6); PR fixture reports copyright 2002–2017, Nexus 3048, serial TM6012EC74B, uptime 50d 5h 9m 7s, System version 7.0(3)I4(7).
- The fixture's source/redistribution basis and exact relation to the reported device output are unestablished. Row 19 is therefore a **conditional bug candidate with provenance/test-identity hold**, not an unqualified temporary candidate.
- Do not redistribute the 50-line fixture in a case packet. A minimal synthetic fixture may be designed around the parser-relevant line, but it must independently reproduce failure at the frozen base and pass at the exact fix commit before the case can proceed.
- No upstream test or model inference was run during this follow-up.


## 19. Technical reproductions on 15 November 2026 — scientific exposure disposition

### Robocop #1371 (SWE-rebench V2 row 24)

- Repository: `MarketSquare/robotframework-robocop`.
- Issue: #1371; upstream fix PR: #1374.
- Exact base: `271e73253a70710cc80374128efa9eabb549b5f2`.
- Exact fix: `ceb6824fb4d80442937497a740edf60a5b6382e0`.
- Harness: [PR #193](https://github.com/MahmutVezir/dijitalikiz/pull/193), merged.
- Run [43710740947](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43710740947): upstream issue-specific reproduction passed. Under one uv-locked environment, base produced one expected issue-specific failing assertion and three passing controls; fix passed all four tests. Python 3.11.18; uv 0.5.13; Robot Framework 6.1.1; pytest 8.3.5.
- Technical report: [ROBOCOP_1371_TECHNICAL_REPRODUCTION_RECORD_2026-11-15.md](../research_candidates/evidence_abstention/ROBOCOP_1371_TECHNICAL_REPRODUCTION_RECORD_2026-11-15.md).

### pdoc #812 (SWE-rebench V2 row 95)

- Repository: `mitmproxy/pdoc`.
- Issue: #812; upstream fix PR: #813.
- Exact base: `57ee1d628027feffbd734180287e74294ddab7df`.
- Exact fix: `75863d3abac0843a4ca0f3d562db2bc21d6ba6dc`.
- Harness: [PR #195](https://github.com/MahmutVezir/dijitalikiz/pull/195), merged.
- Run [43712582477](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582477), job `132807166042`: real CLI base-fail/fix-pass reproduction passed. Base produced `ValueError: No modules found matching spec: .`; fix generated HTML from the same synthetic package root, same command, same venv. Python 3.11.5 (upstream CI matrix); uv 0.6.7; upstream `uv.lock` used with `--frozen`. Runtime and test-log SHA-256 values were written to the GitHub Actions job summary.
- Exact-base `pyproject.toml` says MIT-0 and exact-base root LICENSE blob is `9d75d3de543742e219b1c7301901a95f65ad353a`. The same blob is present at the fix commit. Upstream commit [65b8242f3b75e0c499135e31f20f01caa70f7a04](https://github.com/mitmproxy/pdoc/commit/65b8242f3b75e0c499135e31f20f01caa70f7a04) records the explicit Unlicense-to-MIT-0 transition. The earlier MIT-vs-MIT-0 concern is corrected; the root license and metadata are consistent.
- Detailed technical report: [PDOC_813_PRE_REPRODUCTION_REVIEW_2026-11-15.md](../research_candidates/evidence_abstention/PDOC_813_PRE_REPRODUCTION_REVIEW_2026-11-15.md).

### Common scientific disposition

These two examples are successful engineering reproductions, not accepted confirmatory cases. Both were opened for technical debugging, so the predeclared exposure rule excludes them from the confirmatory sample. No record was added to `CASE_REGISTRY.json`; the accepted independent case count remains **0** and accepted project count remains **0**. Neither result is evidence for or against the P0/P1 hypothesis.

### 15 November repository validation and readiness

- Run [43712582477](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582477): pdoc reproducer job passed; repository/configuration validation passed with **414 tests + 56 subtests**.
- Preflight run [43712582464](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43712582464): fail-closed tests **13/13** and evidence-packet/citation auditor tests **12/12** passed.
- Readiness remains `ready=false`, **21 blockers**, 0 accepted cases, 0 accepted projects, and `model_inference_performed=false`.
- The separate historical archive job still fails because the old CCDG ZIP is absent from the canonical repository path. This is a repository historical-artifact issue, not a pdoc/Robocop candidate or new research dataset failure.

### Next single work package

Start static scope/oracle/provenance review for SWE-rebench V2 row 90 (`pyfar/pyfar` PR #722). Verify issue contract, expected normalization semantics, exact base SHA, changed-file list, nested/file-level license provenance, and the upstream test's sensitivity to the reported bug. Do not run upstream tests/build or model inference until the static and rights gates are closed. If row 90 is exposed by technical debugging, apply the same confirmatory exclusion rule. Do not reduce the minimum sample size of 60 independent cases across at least 8 upstream projects.
