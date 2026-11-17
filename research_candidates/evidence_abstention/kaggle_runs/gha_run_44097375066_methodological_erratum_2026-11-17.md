# Metodolojik düzeltme — Actions run 44097375066

**Kayıt tarihi:** 17 Kasım 2026  
**İlgili çalışma:** [Evidence Abstention Preflight (No Inference), run 44097375066](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44097375066)  
**İlgili rapor:** [İlk Actions denetim raporu](gha_run_44097375066_audit_2026-11-17.md)  
**İlgili PR:** [#222](https://github.com/MahmutVezir/dijitalikiz/pull/222)

## Düzeltmenin nedeni

İlk denetim raporundan sonra workflow adımlarını satır satır inceleyince önemli bir metodolojik kusur bulundu: aşağıdaki on adayın dataset testi adımında, PR'ın tam diff'i buggy base üzerine uygulanıyordu. Tam diff, test dosyalarının yanı sıra üretim kodundaki düzeltmeyi de içeriyordu. Ardından “buggy base” üzerinde başarısızlık bekleniyordu.

Bu düzenek, gerçekte düzeltilmiş üretim kodunu buggy-base deneyi gibi çalıştırabildi. Dolayısıyla bu on adayın 44097375066 run'ındaki dataset FAIL/PASS sonuçları, base-fail/fixed-pass kabul kapısı için **geçerli kanıt değildir**. Eski loglar silinmemiştir; tarihsel kayıt olarak korunur. Ancak söz konusu sonuçlar adayın elenmesi veya kabulü için kullanılmayacaktır.

Etkilenen işler:

- Nox #919
- NumPyro #1916
- Werkzeug #2955
- Robocop #1371
- PyFar #721
- Moto #8269
- Meltano SDK #3090
- Python-Control #1144
- QuTiP #2646
- Amaranth #1518

EODAG #1530 farklı bir minimal YAML reproducer yolu kullanıyordu; aynı tam-PR-diff-on-buggy-base kusuru bu iş için geçerli değildir. EODAG'ın bağımsız reproducer'ı buggy base'de başarısız, fixed revision'da başarılı oldu. Bununla birlikte exact dataset row sorgusu sıfır kayıt döndürdüğü için dataset bağlantısı ve kabul kapısı hâlâ açık durumdadır.

Dishka #435 ayrı bir doğru yöntemle, sadece test dosyalarından üretilmiş test patch'ini buggy base üzerine uygulamıştı. Run 44097375066'da Dishka işi de başarılıydı; ancak bu teknik iş sonucu final vaka kabulü değildir.

## İkinci kusur: shell argüman bölünmesi

İlk beş pytest tabanlı işte selector listesi satır bazlı güvenli argüman aktarımı olmadan shell word splitting yoluyla okunuyordu. Bu yöntem boşluk ve özel karakter içeren parametrik pytest node ID'lerini parçalayabilir. Bu nedenle aşağıdaki selector hataları da otomatik olarak adayın teknik uygunsuzluğu olarak yorumlanmayacaktır:

- Nox: JSON parametreli test node ID'leri shell word splitting nedeniyle bozulabilirdi. Ayrıca test_validation_options selector'ı pinned upstream test koleksiyonunda gerçekten bulunmuyordu; bu ayrı bir veri/oracle uyuşmazlığıdır ve sessizce atılmayacaktır.
- Werkzeug: test_dict_header[=foo, ...] selector'ı pytest tarafından bulunamadı. Önce node ID'nin Parquet satırında nasıl tutulduğu ve upstream test koleksiyonundaki gerçek parametrizasyonla birebir karşılaştırılacak.
- NumPyro ve Robocop: buggy-base testlerinin geçtiği sonucu, tam üretim diff'i buggy base üzerine uygulanmış olduğundan geçerli bir defect-oracle sonucu sayılmayacaktır.

## Run 44097375066'dan korunacak geçerli gözlemler

- Beş önceki kaynak-commit fetch sorunu (Nox, Robocop, EODAG, Meltano, Amaranth) için upstream checkout ve patch hazırlığı adımları bu run'da tamamlandı; eski bad-object imzası tekrarlanmadı.
- Nox'un bağımsız issue reproducer'ı, dataset patch'inden önce pinned buggy base üzerinde çalıştı ve beklenen AssertionError: True is not false imzasını verdi. Bu bağımsız reproducer kanıtı ayrı tutulabilir; dataset selector sonucu yerine kullanılamaz.
- QuTiP'in bağımsız coefficient reproducer'ı pinned buggy base'de AssertionError: 1 != 2 verdi.
- Python-Control'ın bağımsız Nyquist-axis reproducer'ı pinned buggy base'de AssertionError: 0 not greater than 0 verdi.
- EODAG'ın bağımsız YAML reproducer'ı base/fix karşıtlığını gösterdi; dataset row kimliği ise henüz çözümlenmedi.
- PyFar, Meltano ve Amaranth test koleksiyonu eksik bağımlılıklar yüzünden durdu. Bu eksikler otomatik aday reddi anlamına gelmiyor.
- Moto'nun source provenance adımında workflow'un beklediği setup.cfg blob SHA yanlıştı. Gerçek pinned-base blob SHA cef6c2d5788a173013cc0a2307a4793c3900a200 olarak doğrulandı; LICENSE blob SHA 90a85e7149454f173dd595bdeb884340cc01e6f6 doğruydu. Beklenen hash workflow'da düzeltildi.

## Yapılan düzeltmeler

Aşağıdaki değişiklikler PR #222 dalına kaydedildi:

1. Ortak selector koşucusu eklendi: implementation/run_swe_rebench_fail_to_pass.py. Her selector ayrı bir argv elemanı olarak çalıştırılır; shell word splitting kullanılmaz.
2. Koşucu için birim testler eklendi. Boşluk/köşeli parantez içeren node ID'nin tek argüman olarak geçirildiği, base tarafında gerçek test başarısızlığı gerektiği ve fixed tarafında gerçek test başarısı gerektiği doğrulanır.
3. No-inference preflight'a selector koşucusu birim testi eklendi.
4. 12 aday işi needs: no-inference-preflight bağımlılığına alındı. Böylece no-inference ve selector-runner sözleşme testleri geçmeden aday testleri başlamaz.
5. On aday için tam PR diff'i ayrı bir provenance dosyası olarak saklanır; buggy base üzerine yalnızca ilgili test dosyalarından üretilmiş dataset-test.patch uygulanır.
6. İlk beş aday (Nox, NumPyro, Werkzeug, Robocop, PyFar) ortak strict selector koşucusunu kullanır.
7. PyFar lock'ına beautifulsoup4==4.12.3 ve soupsieve==2.6; Meltano lock'ına importlib-metadata==8.5.0 ve zipp==3.21.0; Amaranth lock'ına rfc3986==2.0.0 eklendi. Workflow lisans metadata listeleri de genişletildi. Bu ek paketlerin gerçek ortam kurulumu ve lisans metadata kontrolleri yeni Actions çalışmasında doğrulanacaktır; henüz tamamlanmış sayılmaz.
8. Moto setup.cfg beklenen blob SHA düzeltildi.

## Yeni test çalışmasının durumu

Yeni çalışma: [run 44103128787](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44103128787)

- no-inference-preflight: PASS.
- Selector-runner contract unit tests: PASS.
- Paket/kanıt bütünlüğü, operasyonel/nested packet ve v0.2 kabul-hazırlık sözleşme testleri: PASS.
- 12 aday işi, bu no-inference kapısı geçtikten sonra kuyruğa alındı. Bu kayıt anında candidate job sonuçları henüz oluşmamıştı.
- Bu nedenle yeni buggy-base/fixed-revision aday sonuçları henüz raporlanmıyor.

## Bilimsel durum

- Bu erratum, önceki aday sonuçlarını geriye dönük olarak yeşile çevirmiyor ve hiçbir adayı otomatik kabul etmiyor.
- On adayın önceki dataset test sonuçları geçersiz/karar dışı kabul edilerek yeni yöntemle yeniden üretilecek.
- Adaylar sadece aynı defect-specific selector pinned buggy base'de gerçek test başarısızlığı verdiğinde ve pinned fixed revision'da aynı test geçtiğinde Stage 2 teknik kapısını geçebilir.
- Test koleksiyon/selector hatası, import hatası, environment/provenance hatası veya expected failure assertion'ı dışındaki hata, başarılı reproducer olarak sayılmaz.
- Selector'lar dataset satırından sessizce silinmeyecek. Bir selector upstream test koleksiyonuyla uyuşmuyorsa exact row/selector uyumsuzluğu ayrı kaydedilecek ve candidate acceptance kararı verilmeden çözülecek.
- Kabul edilmiş vaka sayısı 0; 15 bağımsız proje hedefi değişmedi. Model yükleme, inference veya eğitim yapılmadı.

Bu kayıt metodolojik düzeltmedir; hukuki görüş, teknik kabul, final case acceptance veya inference authorization değildir.
