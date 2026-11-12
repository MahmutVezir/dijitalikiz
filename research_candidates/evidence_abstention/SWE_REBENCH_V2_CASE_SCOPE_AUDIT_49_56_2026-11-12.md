# SWE-rebench V2 vaka kapsamı ve PR/issue denetimi: 49–56. kayıtlar

**Yöntem:** Cohort'taki immutable base commit ile upstream PR base SHA karşılaştırması; PR/issue metni ve patch dosyalarının statik incelenmesi.
**Yürütme sınırı:** Kaynak checkout, test/build, paket kurulumu, model yükleme, inference ve fine-tuning yapılmadı.

## Yönetici özeti

- **PR/base SHA eşleşmesi: 8/8 exact match.**
- **Geçici bug adayı: 7/8** — geofileops, Lektor, music21, GeoPandas, Babel, Gammapy, django-bird.
- **Katı yazılım-bug örnekleminden dışlama: 1/8** — Holidays (ülke takvimindeki içerik/veri düzeltmesi; PR bunu supported-market holiday correction olarak sınıflandırıyor).
- Lektor vakasında issue'nin talebi ile PR'ın çözdüğü dosya modu davranışı tam olarak aynı değil; aday geçici tutuldu ama issue–patch uyumu teknik incelemede özel doğrulama gerektiriyor.
- **Kabul edilmiş vaka: 0.** Hiçbir kayıt bug-fail/fixed-pass yeniden üretimi, tam lisans/provenance, bağımsız kök neden incelemesi ve kanıt seviyesi panelinden geçmedi.

## Kayıt bazında kararlar

| # | Depo / PR | Bağlı issue | Base SHA | Bulgular | Ön karar |
|---:|---|---|---|---|---|
| 49 | [geofileops/geofileops PR #649](https://github.com/geofileops/geofileops/pull/649) | [#648](https://github.com/geofileops/geofileops/issues/648) | Exact | copy_layer/append_to fonksiyonlarının varsayılan dst_layer değeri dokümantasyondaki gibi hedef dosya adının stem'i olmuyor. Patch varsayılanı ve dahili katman aktarımını düzeltiyor; ilgili geofile testleri güncelleniyor. | **Geçici bug adayı** |
| 50 | [lektor/lektor PR #1214](https://github.com/lektor/lektor/pull/1214) | [#1213](https://github.com/lektor/lektor/issues/1213) | Exact | Build artifact dosyaları tempfile.mkstemp nedeniyle 0600 kipinde oluşturuluyor; PR normal dosyalarla aynı umask tabanlı dosya kipini sağlayan geçici dosya/atomic_open yardımcılarını ekliyor. Ancak issue özellikle group-readable izin talep ediyor; PR'ın test ettiği davranış normal dosya kipiyle eşleşme. | **Geçici bug adayı; issue–patch uyumu riski** |
| 51 | [cuthbertLab/music21 PR #1736](https://github.com/cuthbertLab/music21/pull/1736) | [#1735](https://github.com/cuthbertLab/music21/issues/1735) | Exact | Stream.splitByQuarterLengths içinde splitAtQuarterLength dönüşündeki özel tuple alt sınıfı normal tuple'a dönüşüyor; spannerList erişimi AttributeError üretiyor. Patch tuple alt sınıfı davranışını ve split sonuçlarını düzeltiyor; regresyon testi ekliyor. | **Geçici bug adayı** |
| 52 | [geopandas/geopandas PR #3591](https://github.com/geopandas/geopandas/pull/3591) | [#3590](https://github.com/geopandas/geopandas/issues/3590) | Exact | GeoDataFrame constructor, geometry sütunundaki tek değer np.nan olduğunda mevcut geometry sütununu tanımıyor ve CRS atamasında ValueError üretiyor. Patch all-NA geometry durumunu ele alıyor ve scalar/array regresyon testleri ekliyor. | **Geçici bug adayı** |
| 53 | [python-babel/babel PR #1141](https://github.com/python-babel/babel/pull/1141) | [#1129](https://github.com/python-babel/babel/issues/1129) | Exact | Babel parse_time, bazı locale formatlarında saniye alanı bulunmadığında format_str.index('s') nedeniyle ValueError veriyor. Patch seconds alanını opsiyonel hale getiriyor ve saniyesiz H:mm testini ekliyor. | **Geçici bug adayı** |
| 54 | [gammapy/gammapy PR #5525](https://github.com/gammapy/gammapy/pull/5525) | [#5524](https://github.com/gammapy/gammapy/issues/5524) | Exact | TemplatePhaseCurveTemporalModel init aşamasında phasecurve template'ini normalize etmiyor; norm farklıysa flux sistematik biçimde yanlış hesaplanıyor. Patch tabloyu init sırasında normalize ediyor ve integral/norm beklenen değerlerini güncelliyor. | **Geçici bug adayı** |
| 55 | [joshuadavidthomas/django-bird PR #219](https://github.com/joshuadavidthomas/django-bird/pull/219) | [#218](https://github.com/joshuadavidthomas/django-bird/issues/218) | Exact | Static asset URL'leri django_bird storage prefix'ini içermediğinden URL ile collectstatic dosya yolu uyuşmuyor. Patch storage url() metodunda prefix'i garanti ediyor ve template/static URL testlerini güncelliyor. | **Geçici bug adayı** |
| 56 | [vacanza/holidays PR #2106](https://github.com/vacanza/holidays/pull/2106) | [#2103](https://github.com/vacanza/holidays/issues/2103) | Exact | Columbus Day'in ülke çapında holiday olarak döndürülmesi yerine yalnızca ilgili subdivision'larda gösterilmesi için takvim verisi ve test snapshot'ları değişiyor. PR kendisini supported country/market holiday update olarak sınıflandırıyor; değişiklik bir yazılım yürütme kusurundan çok takvim içeriği düzeltmesi. | **Dışla: veri/içerik düzeltmesi** |

## Teknik doğrulama riskleri

- **Lektor:** Issue 1213'ün group-readable dosya modu talebi ile PR'ın normal dosya kipine (umask) dönme çözümü birebir aynı hedef değildir. Vaka tutulacaksa araştırma sorusuna konu edilen tek kök neden, artifact oluşturucunun 0600 kipini zorlaması olarak açıkça sınırlandırılmalı; test aynı umask altında normal dosya ve artifact kiplerini karşılaştırmalı.
- **music21:** Aynı hedef test buggy/base sürümde özel tuple yerine plain tuple üretip AttributeError vermeli; fixed sürümde sonuç özel tuple tipini ve spanner metadata'sını korumalı.
- **GeoPandas:** Yalnızca tek np.nan geometri ve all-NA geometry sütunu test edilmemeli; normal boşluk/None/valid geometry davranışı da regresyona karşı korunmalı.
- **Gammapy:** Normalizasyonun matematiksel referansı (phase integral = 1) bağımsız biçimde belirlenmeli; patch'in değiştirdiği beklenen norm değerleri alan referansına göre doğrulanmalı.
- **Holidays:** Bir takvim içeriği uyuşmazlığının yazılım kök neden araştırmasına uygun olup olmadığına dair önceden tanımlı kapsam kuralı uygulanmalı; bu taramada ana yazılım-bug havuzuna alınmadı.

## Karar ve sınırlar

- PR/base SHA: **8/8 exact match**.
- Geçici bug adayı: **7**.
- Katı yazılım-bug örnekleminden dışlama: **1**.
- Kabul edilmiş vaka/proje: **0/0**.
- Upstream root LICENSE/NOTICE, değişen dosyalar ve bağımlılık kapsamı ayrıca denetlenmedi; bu rapor lisans izni vermez.
- Upstream testler çalıştırılmadı; insan panelleri, model yükleme, inference ve eğitim yapılmadı.

Bu belge metadata ve statik patch incelemesidir; kabul edilmiş vaka veya deney sonucu değildir.
