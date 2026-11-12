# SWE-rebench V2 vaka kapsamı ve PR/issue denetimi: 33–40. kayıtlar

**Yöntem:** Cohort'taki immutable base commit ile upstream PR base SHA karşılaştırması; PR/issue metni ve patch dosyalarının statik incelenmesi.  
**Yürütme sınırı:** Kaynak checkout, test/build, paket kurulumu, model yükleme, inference ve fine-tuning yapılmadı.

## Yönetici özeti

- **PR/base SHA eşleşmesi: 8/8 exact match.**
- **Geçici bug adayı: 6/8** — Click, WeasyPrint, python-control, PSyclone, QuTiP, mpmath.
- **Dışlama: 2/8** — PyBaMM (yeni iterable/membership özelliği), Skrub (daha anlaşılır hata mesajı/erken doğrulama iyileştirmesi).
- **Kabul edilmiş vaka: 0.** Geçici adaylar teknik yeniden üretim, lisans ve bağımsız insan incelemesi bekliyor.

## Kayıt bazında kararlar

| # | Depo / PR | Bağlı issue | Base SHA | Bulgular | Ön karar |
|---:|---|---|---|---|---|
| 33 | [pallets/click PR #2788](https://github.com/pallets/click/pull/2788) | [#2746](https://github.com/pallets/click/issues/2746) | Exact | Option.flag_value ile envvar birlikteyken flag_value yerine environment variable'ın içeriği kullanılıyor. PR, bu davranışı düzeltip regresyon testi ekliyor. | **Geçici bug adayı** |
| 34 | [Kozea/WeasyPrint PR #2416](https://github.com/Kozea/WeasyPrint/pull/2416) | [#2270](https://github.com/Kozea/WeasyPrint/issues/2270) | Exact | Non-breaking space içeren metinde otomatik tireleme/kelime bölme davranışı yanlış. Patch satır kırılma noktalarını ve tireleme aralığını yeniden işliyor. Ancak PR'daki yeni testin açıklaması issue #1817'ye atıf yapıyor; #2270 için test duyarlılığı ayrı doğrulanmalı. | **Geçici bug adayı; test-provenance riski** |
| 35 | [python-control PR #1145](https://github.com/python-control/python-control/pull/1145) | [#1144](https://github.com/python-control/python-control/issues/1144) | Exact | Nyquist/Nichols/describing-function çizimlerinde verilen ax nesnesi yok sayılıyor ve çizimler yanlış subplot'a düşüyor. Patch global pyplot çağrılarını hedef axes nesnesine bağlıyor; regresyon testi konumu kontrol ediyor. | **Geçici bug adayı** |
| 36 | [stfc/PSyclone PR #2767](https://github.com/stfc/PSyclone/pull/2767) | [#2755](https://github.com/stfc/PSyclone/issues/2755) | Exact | PSyAD array assignment dönüşümü aktif dizilerde hatalı Fortran adjoint kodu üretiyor. Patch array shape/operation işleme yolunu genişletiyor ve dönüşüm hatalarını ele alıyor. | **Geçici bug adayı** |
| 37 | [skrub-data/skrub PR #1445](https://github.com/skrub-data/skrub/pull/1445) | [#1438](https://github.com/skrub-data/skrub/issues/1438) | Exact | Skrub expression/choice nesneleri yanlışlıkla variable value olarak verilince daha açık TypeError üretmek için erken doğrulama ekleniyor. Issue enhancement olarak etiketli; bu mevcut kök neden hata düzeltmesinden çok API kullanılabilirlik iyileştirmesi. | **Dışla: enhancement** |
| 38 | [cogent3/cogent3 PR #2050](https://github.com/cogent3/cogent3/pull/2050) | [#2045](https://github.com/cogent3/cogent3/issues/2045) | Exact | Newick düğüm adındaki bootstrap support değerini ayrı parse edecek yeni split_name_and_support fonksiyonu ekleniyor. Issue enhancement etiketli ve yeni işlev talep ediyor. | **Dışla: yeni özellik** |
| 39 | [qutip/qutip PR #2694](https://github.com/qutip/qutip/pull/2694) | [#2646](https://github.com/qutip/qutip/issues/2646) | Exact | Mevcut coefficient nesnesi yeniden args ile oluşturulunca güncellenmiş args göz ardı ediliyor. Patch args'ı yeniden uygulatıyor ve regresyon testi ekliyor. Issue BUG etiketi taşıyor. | **Geçici bug adayı** |
| 40 | [mpmath/mpmath PR #902](https://github.com/mpmath/mpmath/pull/902) | [#511](https://github.com/mpmath/mpmath/issues/511) | Exact | Laguerre/hypergeometric hesaplamasında z=inf beklenmeyen sonuca veya NoConvergence'a yol açıyor. Patch sonsuz girdi için özel durum ele alıyor ve test ekliyor. Issue bug etiketi taşıyor. | **Geçici bug adayı** |

## Teknik doğrulama riskleri

- **WeasyPrint:** PR regresyon testinin #1817'ye atıfı ile hedeflenen #2270 issue'su arasındaki bağ açıklığa kavuşturulmalı. Buggy/fixed test çifti #2270 davranışını doğrudan sınamalı.
- **PSyclone:** Test, dizi atamasının adjoint dönüşümünde üretilen Fortran kodunu gerçekten derlemeli; yalnızca transformation exception kontrolü yeterli değildir.
- **mpmath:** Hem arbitrary precision hem fast-math context davranışı kontrol edilmeli; inf girdisinde matematiksel referans davranışı açıkça belgelenmeli.

## Karar ve sınırlar

- PR/base SHA: **8/8 exact match**.
- Geçici bug adayı: **6**.
- Dışlama: **2**.
- Kabul edilmiş vaka/proje: **0/0**.
- Kaynak lisansı/NOTICE ve dosya bazlı yeniden kullanım incelemesi tamamlanmadı.
- Upstream testleri yürütülmedi; metadata test kimlikleri test geçerliliği kanıtı sayılmadı.
- İnsan kök neden/evidence-tier panelleri yapılmadı; model inference yok.

Bu belge metadata ve statik patch incelemesidir; kabul edilmiş vaka veya deney sonucu değildir.
