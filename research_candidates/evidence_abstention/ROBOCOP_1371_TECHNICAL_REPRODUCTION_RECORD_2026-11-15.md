# Robocop #1371 — teknik yeniden üretim kaydı

**Denetim tarihi:** 15 Kasım 2026  
**Durum:** `TECHNICAL_REPRODUCTION_PASS` / `HUMAN_ADJUDICATION_PENDING` / `NOT_ACCEPTED_FOR_CONFIRMATORY`  
**Kapsam:** SWE-rebench V2 birincil cohort, 24. kayıt; yalnızca teknik kusur yeniden üretimi.  
**Model durumu:** Model yükleme, inference, fine-tuning veya eğitim yapılmadı.

## 1. Veri kümesi ve aday kimliği

- Veri kaynağı: `PrimeIntellect/SWE-rebench-V2-Filtered-Verified`
- Sabit Parquet revision: `fb9aa226b2ce37c708ea7732e7b980abacdadb67`
- Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`
- Dondurulmuş cohort: `SWE_REBENCH_V2_COHORT_96_PRIMARY_2026-11-12.csv`
- Cohort CSV SHA-256: `84552868fc2914ebe2421b6b2ce5b6afaabe6a032f9cf9441a6251d2611248db`
- Manifest SHA-256: `77ccd2746e77a0e0d0bb7c7aeaafd8a8c694da8973469fb126708377d4ebcadf`
- Cohort instance: `marketsquare__robotframework-robocop-1374`
- Cohort satırı: **24**

12 Kasım tarihli 17–24 kapsam denetiminde bu kayıt, geçici bug adayı olarak sınıflandırılmıştır. O tarihte hiçbir upstream test çalıştırılmamış ve hiçbir vaka kabul edilmemiştir.

## 2. Upstream kaynak ve kusur

- Repository: [MarketSquare/robotframework-robocop](https://github.com/MarketSquare/robotframework-robocop)
- Issue: [#1371 — robocop format --check does not seem to return correct exit code](https://github.com/MarketSquare/robotframework-robocop/issues/1371)
- Fix PR: [#1374 — Fix robocop format --check always returning 0](https://github.com/MarketSquare/robotframework-robocop/pull/1374)
- Frozen base: `271e73253a70710cc80374128efa9eabb549b5f2`
- Exact fix: `ceb6824fb4d80442937497a740edf60a5b6382e0`
- Upstream merge commit: `6ed3c579e5d14fae89471be29503f73a051105af)

Issue bildirimi, `robocop format --check` komutunun biçimlendirme gerektiren dosyalar bulunduğu hâlde `0` çıkış kodu vermesini tarif eder. Issue yorumunda upstream maintainer, formatter sonucunun tam sayı olarak döndürüldüğünü ancak CLI çıkış kodu olarak yükseltilmediğini açıklar. Base ve fix kaynak kodu karşılaştırması bu açıklamayla tutarlıdır.

Base sürümde `RobocopFormatter.formatting_result`, `check` açık ve değişen dosya varsa `1` döndürür; ancak bu değer CLI sürecinin çıkış koduna çevrilmez. Fix sürümünde metot `typer.Exit(code=...)` yükselterek çıkış kodunu açıkça sonlandırır. PR ayrıca bu davranış için dört durumlu regresyon matrisi ekler.

PR #1374'ün değiştirdiği dosyalar:
- `docs/releasenotes/6.0.3.rst`
- `src/robocop/formatter/runner.py`
- `tests/formatter/__init__.py`
- `tests/test_cli.py`

## 3. Lisans ve provenansın mevcut kapsamı

14 Kasım tarihli 17–56 lisans/provenans denetimi, 24. satırın exact-base kök lisansını Apache-2.0 olarak kaydeder:
- Base commit: `271e73253a70710cc80374128efa9eabb549b5f2`
- Kök `LICENSE` Git blob SHA-1: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`
- Kök `NOTICE`: denetimde bu repository için kayıtlı değil.

Bu, dosya bazlı tam hak temizliği veya hukuki görüş değildir. Kanıt paketine alınacak her gerçek kaynak/test dosyasının telif başlıkları, iç içe lisanslar ve yeniden dağıtım/atıf gereklilikleri ayrıca korunmalıdır. Kök lisans dosyasının bulunması tek başına tüm dosyaların provenansını kapatmaz.

## 4. Teknik yeniden üretim tasarımı

Aynı dört parametrik durum, iki exact commit üzerinde aynı test betiği ve aynı çalışma ortamıyla yürütülmüştür:

| `--check` | Dosyanın yeniden biçimlendirilmesi gerekiyor mu? | Beklenen exit code |
|---|---|---:|
| Kapalı | Evet | 0 |
| Kapalı | Hayır | 0 |
| Açık | Evet | 1 |
| Açık | Hayır | 0 |

Test, upstream PR #1374'ün `NormalizeSeparators` formatter test fixture'ını kullanır; CLI, `typer.testing.CliRunner` ile çağrılır. Testin amacı yalnızca doğru çıkış kodunu kontrol etmektir; model veya model çıktısı bu sürece dahil değildir.

### Sabit çalışma ortamı

- GitHub Actions run: [43710082201](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43710082201)
- İlgili job: `132799529536` — Upstream Robocop
- Proje harness commit: `b6d27db13a4802fcddf24133901bcb7106eeb604`
- Runner: `ubuntu-24.04`
- Python: `3.11.18`
- uv: `0.5.13`
- Bağımlılıklar: base commit içindeki `uv.lock`, `uv sync --frozen --all-extras --dev`
- Robot Framework: `6.1.1` (upstream CI'nin Python 3.11 matrisiyle eşleşir)
- pytest: `8.3.5`
- Base ve fix commitleri **aynı sanal ortamda**, aynı kurulu bağımlılıklar ve aynı test betiğiyle sırayla yürütülmüştür.
- `uv pip check`: 24 paket kontrol edilmiş; uyumsuz bağımlılık bulunmamıştır.

### Gerçek sonuç

**Base commit** `271e73253a70710cc80374128efa9eabb549b5f2`:
- 1 test başarısız, 3 kontrol testi başarılı.
- Tek başarısız durum: `--check` açık ve dosya biçimlendirme gerektiriyor.
- Gerçek CLI exit code: `0`; beklenen: `1`.
- Pytest assertion: `assert 0 == 1`.

**Fix commit** `ceb6824fb4d80442937497a740edf60a5b6382e0`:
- Aynı dört testin tamamı başarılı.
- Sonuç: `4 passed`.

Bu run, base-fail/fix-pass teknik kapısını aynı kilitli ortamda geçmiştir. GitHub Actions job özeti ayrıca runtime freeze ve iki test logu için SHA-256 özetlerini kaydeder.

## 5. Bilimsel karar ve sınırlamalar

**Teknik karar: Yeniden üretim başarılı.**

Bu sonuç yalnızca belirli upstream kusurunun sabitlenmiş base/fix sürümleri arasında yeniden üretilebildiğini destekler. Aşağıdakileri **kanıtlamaz**:
- İki bağımsız insan panelinin root cause veya kanıt yeterliliği konusunda uzlaştığını,
- E1/E2/E3 kanıt düzeylerinin kalibre edildiğini,
- modelin belirsizliği doğru değerlendirdiğini,
- P1 politikasının P0'dan daha güvenilir olduğunu,
- hipotezin doğrulandığını.

Proje protokolünün teknik tarama/hata ayıklama maruziyeti kuralı gereği, bu vaka artık ana doğrulayıcı örnekleme alınmayacaktır. Yalnızca teknik fizibilite/kalibrasyon örneği olarak tutulabilir. Bu nedenle:

- `CASE_REGISTRY.json` değiştirilmez.
- Kabul edilmiş doğrulayıcı vaka sayısı **0** kalır.
- Bu vaka için üretilen teknik test çıktıları ana P0/P1 deney sonucu olarak kullanılmaz.
- İnsan değerlendirmeleri yapılmış gibi gösterilmez.

## 6. Kalan işler

1. Teknik vaka kaydını ve upstream kaynak kimliğini bağımsız bir Panel A incelemesine sunmak; bu inceleme vaka kabulü için değil, araştırma prosedürünün kalibrasyonu içindir.
2. E1/E2/E3 paketlerinde yeterli/kısmi/yetersiz kanıt farkının model çıktısını veya gold root cause bilgisini açığa çıkarmadığını bağımsız Panel B ile kontrol etmek.
3. Confirmatory kohort için bu vakadan ayrı, daha önce teknik olarak açılmamış aday seçmek.
4. Yeni adayda aynı exact-base/fix, lisans/provenans ve runtime koşullarını sıfırdan uygulamak.

**Nihai kayıt:** Robocop #1371 teknik olarak yeniden üretildi; doğrulayıcı vaka olarak kabul edilmedi ve ana deneyde kullanılmayacaktır.


## 7. Aynı günkü araştırma-geneli no-inference kapısı

15 Kasım 2026 tarihli bağımsız preflight çalışması:
- Workflow run: [43710537747](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43710537747)
- Job: `132800899879`
- Fail-closed preflight testleri: **13/13 başarılı**
- Kanıt paketi/atıf bütünlüğü testleri: **12/12 başarılı**
- Artifact: `evidence-abstention-preflight-logs-43710537747-1.zip`
- Artifact SHA-256: `bc910df5e290a18db0c73aefa614639232d9af1b4128099ff01085c16b083252`

Readiness raporu:
- `ready=false`
- Kabul edilmiş bağımsız vaka: **0**
- Kabul edilmiş upstream proje: **0**
- Blokaj: **21**
- `model_inference_performed=false`

Blokaj grupları: inference yetkisi kapalı ve veri kapısı açık; doğrulanabilir ön kayıt URI'si yok; iki değerlendiricili rubrik/adjudication ve bağımsız kalibrasyon tamamlanmamış; exact model/tokenizer/runtime yükleme preflight'ı geçmemiş; 12 protokol/veri/kod girdisinin SHA-256 dondurması eksik; minimum 60 vaka/8 upstream proje sağlanmamış; çalışma runtime lock henüz doğrulanmamış.

Bu no-inference sonucu Robocop teknik tekrarını doğrulayıcı vaka hâline getirmez. Robocop kaydı ve CASE_REGISTRY'nin boş kalması birbiriyle tutarlıdır.
