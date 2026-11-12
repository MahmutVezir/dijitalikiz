# SWE-rebench V2 vaka kapsamı ve PR/issue denetimi: 41–48. kayıtlar

**Yöntem:** Cohort'taki immutable base commit ile upstream PR base SHA karşılaştırması; PR/issue metni ve patch dosyalarının statik incelenmesi.  
**Yürütme sınırı:** Kaynak checkout, test/build, paket kurulumu, model yükleme, inference ve fine-tuning yapılmadı.

## Yönetici özeti

- **PR/base SHA eşleşmesi: 8/8 exact match.** msgspec için cohort'taki eski jcrist/msgspec adresi artık msgspec/msgspec canonical deposuna yönleniyor; exact base SHA yine birebir eşleşiyor.
- **Geçici bug adayı: 5/8** — ccdproc, ASDF, msgspec, Jinja, jsonpickle, scikit-activeml? Aşağıdaki kayıt kararlarına göre toplamı **6/8**.
- **Dışlama: 2/8** — PyBaMM ve scikit-rf.
- **Kabul edilmiş vaka: 0.** Geçici adaylar lisans, test-çifti, kök neden ve insan panellerinden geçmedi.

## Kayıt bazında kararlar

| # | Depo / PR | Bağlı issue | Base SHA | Bulgular | Ön karar |
|---:|---|---|---|---|---|
| 41 | [astropy/ccdproc PR #901](https://github.com/astropy/ccdproc/pull/901) | [#814](https://github.com/astropy/ccdproc/issues/814) | Exact | ImageFileCollection.filter yeni koleksiyon oluştururken ext değerini taşımıyor; farklı FITS extension'larına ait keyword'ler kayboluyor. Patch ext değerini koruyor ve regresyon testi ekliyor. | **Geçici bug adayı** |
| 42 | [pybamm-team/PyBaMM PR #4465](https://github.com/pybamm-team/PyBaMM/pull/4465) | [#4438](https://github.com/pybamm-team/PyBaMM/issues/4438) | Exact | ParameterValues için __iter__ ve __contains__ eklenerek dict-like kullanım sağlanıyor. PR açıkça new feature olarak işaretli; mevcut hata düzeltmesi değil. | **Dışla: feature** |
| 43 | [asdf-format/asdf PR #1907](https://github.com/asdf-format/asdf/pull/1907) | [#1821](https://github.com/asdf-format/asdf/issues/1821) | Exact | asdf.util.load_yaml recursive YAML object/tag yapısında ConstructorError üretiyor. Patch generator tabanlı YAML constructor kullanıyor ve tagged recursive nodes regresyon testi ekliyor. | **Geçici bug adayı** |
| 44 | [msgspec/msgspec PR #772](https://github.com/msgspec/msgspec/pull/772) | [#769](https://github.com/msgspec/msgspec/issues/769) | Exact | Python 3.13'te types.UnionType.__parameters__ bir descriptor döndürdüğü için _apply_params TypeError üretiyor. PR invalid/non-iterable __parameters__ durumunu güvenli ele alıyor. Cohort'taki jcrist/msgspec adresi msgspec/msgspec canonical deposuna transfer edilmiş; base SHA eşleşmesi korunuyor. | **Geçici bug adayı** |
| 45 | [pallets/jinja PR #2033](https://github.com/pallets/jinja/pull/2033) | [#2032](https://github.com/pallets/jinja/issues/2032) | Exact | ImmutableSandboxedEnvironment, MutableSequence.clear/pop metotlarını mutasyon olarak engellemiyor; template içinden liste değiştirilebiliyor. Patch metotları known-mutable allowlist'ine ekliyor ve SecurityError testleri ekliyor. Güvenlik etkisi ayrıca threat-model açısından incelenmeli. | **Geçici bug adayı** |
| 46 | [scikit-rf/scikit-rf PR #1282](https://github.com/scikit-rf/scikit-rf/pull/1282) | [#1279](https://github.com/scikit-rf/scikit-rf/issues/1279) | Exact | Touchstone yazımına Y/Z parametre export desteği ekleniyor. Issue Feature Request olarak işaretli; yeni format desteği. | **Dışla: feature request** |
| 47 | [jsonpickle/jsonpickle PR #565](https://github.com/jsonpickle/jsonpickle/pull/565) | [#564](https://github.com/jsonpickle/jsonpickle/issues/564) | Exact | Keyword-only argüman gerektiren Exception alt sınıfı decode sırasında __init__ çağrısında TypeError veriyor. Patch uygun durumda __new__ ile nesneyi oluşturup state'i geri yüklemeyi sağlıyor; issue bug etiketi taşıyor. | **Geçici bug adayı** |
| 48 | [scikit-activeml/scikit-activeml PR #504](https://github.com/scikit-activeml/scikit-activeml/pull/504) | [#503](https://github.com/scikit-activeml/scikit-activeml/issues/503) | Exact | TypiClust ve ProbCover içindeki random_state, cluster_algo'ya aktarılmadığı için aynı seed ile sonuç deterministik değil. Patch uygun cluster algoritmalarına random_state aktarıyor; issue bug bildiriyor. PR ayrıca workflow/format ve test düzenlemeleri içeriyor; hedef kök nedenin tek ve izole olduğu teyit edilmeli. | **Geçici bug adayı; scope riski** |

## Teknik doğrulama riskleri

- **msgspec:** Test, Python 3.13'te UnionType nesnesinin __parameters__ descriptor davranışını gerçekten üretmeli; sadece yapay Invalid sınıfı yeterli olabilir ama gerçek runtime reproducer'ı tercih edilmeli.
- **Jinja:** Sandbox bypass'ın engellendiği test; sadece exception değil, template içindeki mutasyon girişiminin önlenmesini de göstermeli.
- **scikit-activeml:** PR birden fazla dosyada reproducibility ve formatter ayarları değiştiriyor. Buggy/fixed karşılaştırmasında tek bir random_state aktarımı hatasının izole edildiği gösterilmeli.

## Karar ve sınırlar

- PR/base SHA: **8/8 exact match**.
- Geçici bug adayı: **6**.
- Dışlama: **2**.
- Kabul edilmiş vaka/proje: **0/0**.
- msgspec canonical depo transferi provenance notu olarak saklandı; cohort alias'ı sessizce değiştirilmedi.
- Lisans/NOTICE, dosya bazlı yeniden kullanım ve bağımlılık kapsamı tamamlanmadı.
- Upstream testleri çalıştırılmadı; insan panelleri ve model inference yapılmadı.

Bu belge metadata ve statik patch incelemesidir; kabul edilmiş vaka veya deney sonucu değildir.
