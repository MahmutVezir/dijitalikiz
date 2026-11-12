# TÜBİTAK 2204-A — proje durumu ve çalışma planı
**Denetim tarihi:** 12 Kasım 2026  
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


## 10. 12 Kasım 2026 — V12, GitHub Actions ve arşiv kurtarma güncellemesi

### V12 metadata-only intake

- GitHub Actions workflow: `Evidence Abstention V12 Metadata Inventory`
- Initial run: `43236394154` — successful.
- Latest verified rerun: `43239530779` — successful.
- Latest Actions artifact: `13953987822`; 189,493 bytes; SHA-256 `cb75583d1a3309033acc34a0494674e0d7ba5a4f64d8c82ad1b20ad0e5f9a539`; expires `2027-02-10T14:40:01Z`.
- The latest artifact ZIP CRC passed and all seven internal file SHA-256/byte-length records matched. The 501-row inventory, 395-row queue, 100-case index and eight-project first batch reproduced identically to the initial successful run.
- Pinned BugsInPy metadata revision: `11c5f1eea954a42132cfd06bf257766a7963e0fd`.
- Inventory: 501 metadata rows. Queue after exclusions: 395 candidate rows.
- V12 intake: 100 unique candidate IDs across 13 upstream projects.
- Permanent exposure exclusions: 105; the 97-ID 24 October union is preserved and the 8-ID 11 November addendum is applied append-only.
- First batch: 8 metadata candidates from 8 distinct projects (Ansible-8, Black-10, FastAPI-10, Keras-9, Luigi-9, Matplotlib-8, Pandas-7, Scrapy-8).
- Accepted confirmatory cases: 0. Model inference: false. No target tests were run by this V12 metadata workflow.

The ZIP CRC passed and all seven internal file size/SHA-256 records matched. A normalized 100-case cohort index, first-batch selection record, and evidence manifest are committed under `research_candidates/evidence_abstention/generated_v12/`. The original full inventory and queue CSVs are reproducible from the pinned source and retained in the temporary Actions artifact; they are not committed because the BugsInPy dataset-level license remains unresolved.

### Preflight and regression fixes

- Stage 3 preflight and analysis now reference `EXPOSURE_UNION_2026-11-11.json`, not the stale 24 October 97-ID union.
- Regression tests verify that the 105-ID union is exactly the 97-ID prior union plus the eight dated addendum IDs, including Black-9.
- The analysis helper and Kaggle audit contract tests were updated to the 105-ID screening union.
- V12 workflow contract tests were added.
- The current draft correction PR is #168: `research/2026-11-12-v12-intake-and-preflight-fix`.
- V12 metadata workflow and preflight gates have successful runs. Repository validation is passing apart from the separate historical archive storage gate described below.

### Legacy CCDG archive recovery

The original Actions artifact `11640450681` is no longer available through the Actions API. Five identical copies were recovered from the user's ChatGPT Library on 12 November 2026. All five have SHA-256 `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd` and size 292,742 bytes.

Independent checks:
- ZIP CRC: passed; 214 ZIP entries.
- Artifact manifest: 212 declared files; 0 missing and 0 size/SHA mismatches.
- Confirmatory records: 160; 160 unique record keys; 16 cases.
- Conditions: 80 Standard and 80 CCDG.
- Source commit: `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`.

The ZIP is recovered but **not yet committed** to `data/historical/confirmatory_artifact_2026-10-09.zip`. The historical Actions job now checks that canonical repository path and deliberately remains blocked until the exact file is uploaded. The archive is legacy CCDG research only; it is not the new evidence-abstention dataset and must not be used as confirmatory training/evaluation data for the new study.

### Legal and scientific blockers

1. BugsInPy has no dataset-level LICENSE file at the checked repository root; upstream issue #94 also raises the absence of license information. Written clarification/permission or an independently curated, clearly licensed replacement dataset is required before redistribution or final dataset clearance.
2. The 13 upstream project licenses must be checked at exact buggy/fixed commits and for the files used. Do not copy upstream source code into this repository.
3. Qwen2.5-3B-Instruct is under the Qwen Research License, not Apache-2.0. Preserve the exact revision/license notice; keep use non-commercial and do not use its outputs to improve a different LLM. Recheck the exact license attached to the pinned model revision before fine-tuning.
4. Two independent, disjoint review panels, written consent, applicable institutional/MEB approvals, and an AI-use disclosure are still required.
5. The model has not been trained or run for this study. The current cohort is a candidate index only.

### Next ordered actions

1. Upload the recovered historical CCDG ZIP to `data/historical/confirmatory_artifact_2026-10-09.zip`; verify its exact SHA-256 and rerun the local archive gate.
2. Complete the BugsInPy dataset-level license decision and exact-revision license register for the selected upstream projects. If permission is not obtained, switch to a clearly licensed independently curated source.
3. Freeze the technical runner and protocol using isolated fixtures. Only then test the first eight V12 candidates as a technical-validation batch; once their target outcomes are inspected, permanently exclude those eight from confirmatory sampling.
4. Rebuild a clean confirmatory candidate pool after the new exclusions, complete two-panel ground-truth/evidence adjudication, and accept at least 60 (target 80) cases across at least eight projects.
5. Freeze model, tokenizer, prompt, runtime, thresholds, preregistration and analysis hashes before inference. Only then begin model inference/fine-tuning.
6. Complete statistical analysis, limitations, AI-use declaration, consent/approval appendix and the final report before the TÜBİTAK deadline.

**Status on 12 November:** repository/code and metadata intake are substantially improved, but the scientific dataset, legal clearance, confirmatory labels, model experiment, and final report are not complete. Do not submit or claim a completed project yet.


## 11. 12 Kasım 2026 — Kaggle snapshot, inference gate and training decision

### 31/19 Kaggle source-count mismatch

The 31-file and 19-file counts belong to two different, versioned source snapshots:
- 27 October v2 bundle: 31 files, `BUNDLE_MANIFEST.json`, source commit `99663c2874424feb9cec1d965432030f5cdb3ef8`, consumed by notebook 02.
- 3 November current-branch audit: 19 allow-listed files, consumed by notebook 03.

The 19-file audit package is not the complete repository. The exact "v2 source-bundle manifest found 0" error means the running notebook did not find the manifest path/name it expected; a stale notebook copy or the wrong dataset/notebook pairing is the likely cause. Do not rename manifests manually. See `docs/KAGGLE_SOURCE_BUNDLE_COMPATIBILITY_2026-11-12.md`.

V12 metadata intake now runs directly in GitHub Actions from the canonical repository and no longer depends on either historical Kaggle bundle.

### Inference gate repaired

The separate uncertainty inference gate previously hard-coded the 23 October 93-ID exposure union. It now pins:
- `EXPOSURE_UNION_2026-11-11.json`
- exactly 105 unique exclusion IDs
- SHA-256 `9f41451bb06582ea65647f67829e97ac190cb884946b1f4f09c75d8167acb7c1`

The inference gate now also requires explicit dataset-level license clearance, exact upstream project license clearance, exact model revision license clearance, institutional approval and reviewer consent. The manifest remains deliberately closed.

### Model training decision

The current `qwen_uncertainty_adapter.py` is an inference adapter, not a fine-tuning script. The `uncertainty_policy.py` component is a pure-Python decision/calibration layer, not a neural training loop. No training script or training dataset is currently present.

The primary confirmatory study should compare P0 and P1 using the same frozen base model. Fine-tuning before this comparison would change the model and confound the effect of the abstention policy. A separate fine-tuning study is optional and requires its own licensed labeled dataset, project-disjoint splits, preregistration, and independent test set. See `research_candidates/evidence_abstention/MODEL_TRAINING_DECISION_2026-11-12.md`.

### Current hard stops

- BugsInPy dataset-level license/permission unresolved.
- Per-project license review incomplete.
- Qwen2.5-3B-Instruct exact revision license review pending; model is marked Qwen Research License, not Apache-2.0.
- Human reviewer institutional approval and written consent not obtained.
- 100 V12 candidates are metadata only; zero accepted confirmatory cases.
- No inference, fine-tuning, or model training performed.


### V12 technical-screen workflow safety

- Added `.github/workflows/evidence-abstention-v12-technical-screen.yml`.
- It is manual-dispatch only; there are no push or pull-request triggers.
- All four explicit manual confirmations default to false: dataset permission, upstream licenses, frozen protocol, and technical-screen authorization.
- Before cloning BugsInPy or running target tests, the workflow also checks the experiment manifest for cleared dataset/upstream license statuses, frozen technical-screen protocol, explicit authorization, the 105-ID union path and its SHA-256.
- It rebuilds the 100-case cohort and first batch, then compares them with the committed V12 case index and first-batch selection.
- The old `evidence-abstention-v11-technical-screen.yml` is archived and its manual dispatch has been removed. Its historical 97-ID logic must not be used for V12.
- The V12 technical-screen workflow has not been dispatched. The manifest currently says `not_frozen` and `technical_screen_authorized=false`; it will deliberately stop before any upstream checkout.
