# SWE-rebench V2 vaka kapsamı ve PR/issue eşleştirme denetimi: 25–32. kayıtlar

**Denetim kapsamı:** 12 Kasım 2026 tarihinde dondurulmuş 96 projelik birincil aday havuzunun 25–32. satırları.  
**Yöntem:** Exact cohort base SHA ile GitHub PR base SHA karşılaştırması; issue metni/etiketi ve değişen dosyaların statik patch incelemesi.  
**Yürütme sınırı:** Upstream kaynak checkout edilmedi; test/build çalıştırılmadı; paket kurulmadı; model yüklenmedi, inference veya fine-tuning yapılmadı.

## Yönetici özeti

- **PR/base commit eşleşmesi: 8/8 exact match.**
- **Geçici bug adayı: 5/8** — Meltano SDK, DataComPy, Amaranth, ctapipe, Werkzeug.
- **Katı bug örnekleminden dışlama: 3/8** — CTFd (istenen davranış/özellik), JAX (issue enhancement etiketiyle yeni int4 görünüm desteği), Robyn (OpenAPI override özelliği).
- **Kabul edilmiş doğrulayıcı vaka: 0.** Geçici adaylar test çiftinin kusura duyarlılığı, kaynak/lisans, kök neden ve bağımsız insan incelemesinden geçmedi.
- 25–32 grubunun oranı tüm cohort'a genellenemez.

## Kayıt bazında kararlar

| # | Cohort instance / depo | PR ve issue | Base SHA | Statik kapsam bulgusu | Ön karar |
|---:|---|---|---|---|---|
| 25 | CTFd/CTFd — CTFd flag kayıtları | [PR #2767](https://github.com/CTFd/CTFd/pull/2767), [issue #851](https://github.com/CTFd/CTFd/issues/851) | Exact | Static/regex flag içeriğinde boşlukların create/update sırasında kırpılması isteniyor. Issue mevcut hatalı davranıştan çok istenen davranış talebi olarak yazılmış; PR bu yeni davranışı uyguluyor. | **Dışla: özellik/iyileştirme** |
| 26 | meltano/sdk — Singer SDK | [PR #3091](https://github.com/meltano/sdk/pull/3091), [issue #3090](https://github.com/meltano/sdk/issues/3090) | Exact | Aynı JSON Schema referansı birden çok property tarafından kullanıldığında mutable visited set yüzünden ikinci property boş nesneye dönüşüyor. PR, recursion stack'i tuple ile izliyor ve aynı referansı kullanan iki property için regresyon testi ekliyor. Issue açıkça regression bug bildiriyor. | **Geçici bug adayı** |
| 27 | capitalone/datacompy — DataComPy | [PR #404](https://github.com/capitalone/datacompy/pull/404), [issue #58](https://github.com/capitalone/datacompy/issues/58) | Exact | Issue eşit iki boş NumPy dizisinin yanlışlıkla eşit değil sayılmasını bug olarak bildiriyor. PR NumPy list/array ve Polars List/Array karşılaştırma desteği ekliyor. PR başlığı feature dese de issue mevcut yanlış karşılaştırma sonucunu raporluyor. Boş-dizi özel durumunun hedef testte gerçekten kapsandığı ayrıca doğrulanmalı. | **Geçici bug adayı; hedef test uygunluğu riski** |
| 28 | jax-ml/jax — JAX | [PR #25650](https://github.com/jax-ml/jax/pull/25650), [issue #25620](https://github.com/jax-ml/jax/issues/25620) | Exact | int4/uint4 dtype için ndarray.view bit-width hesabı ekleniyor. Bağlı issue açıkça enhancement etiketli ve yeni dtype desteği talep ediyor. Önceden belirlenen katı mevcut-bug ölçütüne alınmıyor. | **Dışla: enhancement/yeni destek** |
| 29 | sparckles/Robyn — Robyn | [PR #1002](https://github.com/sparckles/Robyn/pull/1002), [issue #961](https://github.com/sparckles/Robyn/issues/961) | Exact | Kullanıcının OpenAPI JSON dosyasını uygulamaya override olarak verebilmesi ekleniyor. PR ve issue metinleri yeni özellik talebini gösteriyor. | **Dışla: özellik geliştirme** |
| 30 | amaranth-lang/amaranth — Amaranth | [PR #1519](https://github.com/amaranth-lang/amaranth/pull/1519), [issue #1518](https://github.com/amaranth-lang/amaranth/issues/1518) | Exact | Format string içindeki literal süslü parantezler RTLIL/Yosys çıktısını bozuyor ve YosysError üretiyor. Patch literal { ve } karakterlerini escape ediyor; issue bug etiketli ve regresyon testi eklenmiş. | **Geçici bug adayı** |
| 31 | cta-observatory/ctapipe — ctapipe | [PR #2732](https://github.com/cta-observatory/ctapipe/pull/2732), [issue #2730](https://github.com/cta-observatory/ctapipe/issues/2730) | Exact | Muon skewness/excess-kurtosis alanlarında birim taşıyan sayısal değerler yazıcıda float/to_value uyumsuzluğu oluşturuyor. Patch boyutsuz değerleri birimsiz float'a dönüştürüyor; issue DataWriter hatasını somut biçimde raporluyor ve regresyon testi tipleri denetliyor. | **Geçici bug adayı** |
| 32 | pallets/werkzeug — Werkzeug | [PR #2956](https://github.com/pallets/werkzeug/pull/2956), [issue #2955](https://github.com/pallets/werkzeug/issues/2955) | Exact | Boş authorization parametresi parse_dict_header içinde IndexError üretiyor. Patch boş anahtarları atlıyor ve invalid authorization girdileri için test ekliyor. | **Geçici bug adayı** |

## Geçici adaylar için sonraki teknik doğrulama koşulları

- **Meltano SDK:** Aynı referansı iki property'nin kullandığı test buggy/base sürümde ikinci property'yi boş bırakmalı; fixed sürümde iki referansı da çözmeli.
- **DataComPy:** Özellikle iki boş NumPy dizisinin eşitliği hedef testte bulunmalı. Yalnızca dolu dizilerin desteklenmesi, issue'daki özgün hatayı doğrulamaz.
- **Amaranth:** Literal süslü parantezli Format girdisi aynı RTLIL/Yosys hata yolunu tetiklemeli; fixed tarafta hedef dönüşüm geçmeli.
- **ctapipe:** DataWriter hatasının kök nedeni ile birimsiz skewness/excess-kurtosis çıktısı doğrudan bağlanmalı; yalnızca tip testi yeterli sayılmamalı.
- **Werkzeug:** Boş authorization parametresi buggy sürümde IndexError, fixed sürümde güvenli parse/atlama davranışı üretmeli.

## Karar ve sınırlar

- PR/base SHA provenance: **8/8 exact match**.
- Geçici bug adayı: **5**.
- Katı bug örnekleminden dışlanan: **3**.
- Kabul edilmiş doğrulayıcı vaka/proje: **0/0**.
- Lisans: Bu rapor exact-commit root LICENSE, değişen dosya lisansı, NOTICE ve bağımlılık kapsamını onaylamaz. Ayrı lisans/lineage denetimi gerekir.
- Test: Hiçbir upstream test çalıştırılmadı. Dataset FAIL_TO_PASS sayısı, testin hedef kusuru doğru sınadığına kanıt değildir.
- İnsan incelemesi: Gold root cause ve E1/E2/E3 yeterlilik panelleri yapılmadı.
- Model: Model yükleme, inference ve fine-tuning yapılmadı.

**Bir sonraki sınırlı iş paketi:** cohort'un 33–40. satırlarını aynı değişmez dahil etme/dışlama kurallarıyla incelemek. İlk 32 için gözlenen aday oranına dayanarak doğrulayıcı örneklem yeterliliği ayrıca izlenecek; gerektiğinde önceden tanımlı proje yedekleri ve aynı projedeki alternatif issue kayıtları kullanılacak. Kaynak/lisans ve teknik doğrulama kapıları kapanmadan upstream testleri çalıştırılmayacak.

Bu belge metadata ve statik patch incelemesidir; hukuki uygunluk görüşü, doğrulanmış veri kümesi, kabul edilmiş vaka kaydı veya deney sonucu değildir.
