# pdoc #812 / PR #813 — yeniden üretim öncesi aday incelemesi

**Denetim tarihi:** 15 Kasım 2026  
**Durum:** `STATIC_STRONG_CANDIDATE_WITH_PROVENANCE_AND_TEST_SCOPE_HOLD`  
**İşlem sınırı:** Metadata, issue/PR, patch, exact-base kaynak ve lisans metaverisi statik olarak incelendi. Upstream test/build çalıştırılmadı; paket kurulmadı; model yüklenmedi, inference veya fine-tuning yapılmadı.

## 1. Dondurulmuş cohort kimliği

- Veri kaynağı: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Immutable Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Frozen cohort: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Cohort CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- Cohort satırı: **95**
- Instance: `mitmproxy__pdoc-813`

12 Kasım tarihli 89–96 statik aday denetimi, pdoc #813'ü güçlü kusur adayı olarak işaretlemişti. Bu, teknik reproduksiyon veya vaka kabulü değildir.

## 2. Issue ve upstream PR kimliği

- Repository: [mitmproxy/pdoc](https://github.com/mitmproxy/pdoc)
- Issue: [#812 — pdoc does not work if "." is specified while specifying the directory](https://github.com/mitmproxy/pdoc/issues/812)
- PR: [#813 — Make `pdoc .` work](https://github.com/mitmproxy/pdoc/pull/813)
- Frozen base: `57ee1d628027feffbd734180287e74294ddab7df`
- PR head/fix commit: `75863d3abac0843a4ca0f3d562db2bc21d6ba6dc`
- Merge commit: `7391e8a5fb966d4c2c98fe6030c1d3b552949e54)
- PR açıklaması: `fix #812`

Issue, bir Python proje kökünde `python -m pdoc .` komutunun `ValueError: No modules found matching spec: .` hatası vermesini anlatır. Issue sahibi dizinde `__init__.py`, `function_app.py`, alt paketler ve `pyproject.toml` bulunduğunu belirtmiştir.

## 3. Statik patch ve kök neden hipotezi

PR #813 üç dosyayı değiştirmiştir:

- `CHANGELOG.md`
- `pdoc/extract.py`
- `test/test_extract.py`

Exact-base `pdoc/extract.py` içinde `parse_spec`, import edilebilir modül bulunamadığında göreli `Path` nesnesini `pspec` olarak saklıyordu. PR fix'i bu dalda `pspec.resolve()` kullanarak yolu mutlaklaştırır. Böylece mevcut çalışma dizinini `Path(".")` olarak taşımak yerine gerçek dizin yoluyla modül adını hesaplayan sonraki dalın çalışması hedeflenir.

Patch açıklaması ve kod farkı issue ile mantıksal olarak uyumludur. Ancak yalnızca bu statik eşleşme, kusurun exact base sürümünde başarıyla yeniden üretildiğini kanıtlamaz.

## 4. Upstream regresyon testinin kapsamı ve açık soru

PR, `test/test_extract.py::test_parse_spec` içine şu davranışları eklemiştir:

- `demopackage/subpackage` dizinine geçiş;
- `parse_spec(".") == "demopackage.subpackage"`;
- `parse_spec("..") == "demopackage"`.

Bu test, `parse_spec` fonksiyonunun göreli dizinleri doğru modül adına çevirmesini denetler. Ancak doğrudan issue'da bildirilen tam komut olan `python -m pdoc .` çağrısını, proje kökünde bir paket `__init__.py` dosyası varken çalıştırmaz.

**Bir sonraki teknik testin zorunlu koşulu:** Dondurulmuş base ve fix commitlerinde aynı sentetik proje dizini oluşturulmalı; proje kökünde `__init__.py` ve en az bir basit modül olmalı; süreç o kökte çalıştırılarak gerçek CLI üzerinden `python -m pdoc .` çağrılmalı. Base sürümde issue'ya özgü hata, fix sürümde başarılı dokümantasyon üretimi gözlenmeli. Ayrıca geçerli bir alt paket / üst paket kontrolü korunmalı. Yalnızca `parse_spec` birim testiyle yetinilmemelidir.

### Issue yorumlarından gelen kapsam uyarısı

Issue yorumlarında kullanıcı, dizin adında nokta bulunan bir varyantın Windows/pdoc 15.0.4 üzerinde hâlâ sorunlu göründüğünü bildirmiştir. Upstream maintainer, `__init__.py` bulunan bir dizinin Python modülü olduğunu ve modül adında nokta kullanılmaması gerektiğini açıklamıştır. Bu varyantı ana reproduksiyonla birleştirmemek gerekir: geçerli Python paket adı olan bir proje kökü ve geçersiz modül adı içeren dizin senaryosu farklı koşullardır.

## 5. Lisans / provenans kontrolü — açık hold

14 Kasım tarihli 17–56 exact-base lisans denetiminde row 55–56 dışında row 95 pdoc için:
- exact-base root `LICENSE` mevcut;
- root lisans, audit tablosunda MIT olarak sınıflandırılmış;
- Git blob SHA-1: `9d75d3de543742e219b1c7301901a95f65ad353a`;
- root `NOTICE` dosyası bulunmadı.

Ek statik incelemede exact-base `pyproject.toml` şu metaveriyi bildiriyor:

`license = { text="MIT-0" }`

Buna karşılık exact-base kök `LICENSE` dosyasının metni “Copyright 2024 Maximilian Hils” ile başlayan standart MIT izin metnidir. Bu iki ifade aynı şeymiş gibi varsayılmamalıdır. PR #813 bu lisans dosyasını veya `pyproject.toml` dosyasını değiştirmemiştir; dolayısıyla durum fix PR'ından kaynaklanan bir fark değildir, ancak cohort kaydındaki lisans sınıflandırmasıyla dağıtım metaverisi arasında açıklanması gereken bir uyumsuzluktur.

**Karar:** Herhangi bir kaynak/test fixture'ı araştırma paketine kopyalanmadan veya dağıtılmadan önce lisans metaverisi ve kök lisansın ilişkisi bağımsız provenance incelemesiyle netleştirilmelidir. Bu rapor hukuki görüş veya yeniden dağıtım izni değildir.

## 6. Mevcut karar

**Statik ön karar:** Güçlü hata adayı; teknik reproduksiyon ve lisans/provenans kapıları açık.

Henüz:
- exact-base/fix test çalıştırması yapılmadı;
- buggy-fail/fixed-pass sonucu doğrulanmadı;
- Panel A kök neden / kaynak / lisans onayı alınmadı;
- Panel B E1/E2/E3 yeterlilik değerlendirmesi yapılmadı;
- vaka `CASE_REGISTRY.json` içine eklenmedi.

Bu nedenle kabul edilmiş doğrulayıcı vaka sayısı **0** olarak kalır. Bu kayıt, ana deney için başarı veya hipotez desteği değildir.

## 7. Devam koşulları

1. MIT-0 metaverisi ile kök MIT lisans metni arasındaki farkı provenance incelemesiyle açıklığa kavuştur.
2. Yalnızca geçerli Python paket dizinini kullanan, issue'ya özgü exact CLI reproducer'ını önceden yaz ve test kimliğini dondur.
3. Aynı sabit runtime altında exact base ve exact fix üzerinde aynı testi çalıştır; ham log, ortam fingerprint'i ve SHA-256 kaydet.
4. Sonuçları ancak bundan sonra teknik aday olarak raporla; insan panelleri ve kanıt paketi onayı olmadan vaka kabulü yapma.

**Önemli sınır:** Bu statik inceleme tek başına `CASE_REGISTRY`, deney manifesti veya inference yetkisini değiştirmez. Model inference/training yapılmamıştır.
