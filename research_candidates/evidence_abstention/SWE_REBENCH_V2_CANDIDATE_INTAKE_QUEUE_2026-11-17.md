# v0.2 aday kabul kuyruğu ve sonraki işlem planı — 17 Kasım 2026

## Amaç

Bu kayıt, 15 bağımsız upstream proje hedefinden sapmadan 96 ana adayın ve 17 bağımsız proje rezervinin hangi sırayla ele alınacağını tanımlar. Bu bir aday kabul kararı değildir. Statik kısa liste etiketi, teknik yeniden üretim, lisans/provenance, bağımsızlık ve E1/E2/E3 kabulünün yerine geçmez.

## Sabit araştırma çerçevesi

- Ana kohort: 96 farklı upstream repository/proje.
- Statik değerlendirme sonrası geniş teknik inceleme kuyruğu: 65 satır. Bu, 65 uygun vaka veya 65 teknik başarı anlamına gelmez.
- Ayrı proje rezervi: 17 farklı upstream proje.
- Aynı projedeki 148 alternatif, vaka sayısına 148 bağımsız proje eklemez; yalnızca aynı proje içindeki bir adayı değiştirmek için kullanılabilir.
- Hedef: 15 bağımsız upstream proje; 20 proje stretch hedefidir.
- Kabul eşiği gevşetilmez. Bir proje en fazla bir kabul edilmiş vaka sağlayabilir.
- Her teknik aday aynı defect-specific testte pinned buggy base'de gerçek test failure, pinned fixed revision'da aynı testte gerçek pass göstermelidir. Collection/import/selector/setup hatası bu koşulu karşılamaz.
- Model yükleme, inference ve eğitim bu kuyrukta yetkilendirilmemiştir.

## İlk üç adayın yeri

### 1. Dishka #435 / PR #436 — ana kohort rank 2

- Teknik yeniden üretim: issue reproducer ve 8/8 dataset selector pinned buggy base'te gerçek failure, fixed revision'da pass verdi.
- Proje lideri gold mekanizma, alternatifler ve E1/E2/E3 üyelik/rasyonellerini onayladı.
- Tek insan değerlendirici, araştırmacı maruziyeti ve yalnızca keşifsel kullanım sınırlamaları kabul edildi.
- **Kalan kapı:** tam case-acceptance record, Draft 2020-12 acceptance schema doğrulaması ve fail-closed registry kontrolü. Bunlar tamamlanmadan accepted registry 0 kalır.

### 2. Earthkit-data #571 / PR #592 — ana kohort rank 4

- Issue/patch hizalaması ve exact-base Apache-2.0 root-license taraması statik olarak geçti.
- **Henüz kaynak testi çalıştırılmadı.**
- **Blokerler:** dış GRIB fikstürünün aynı byte'larla sabitlenmesi ve SHA-256'sı; fikstür kaynağı ve saklama/yeniden dağıtım koşulları; CF Conventions Appendix A kaynak sürümü ve cf_attrs.yaml üretim provenance'ı; exact Parquet row ve selector kimliği.
- Bu belgeler çözülmeden remote fikstür indirilmez ve test yürütülmez.

### 3. Nox #919 / PR #922 — ana kohort rank 6

- Bağımsız issue reproducer pinned buggy base'de beklenen hatayı verdi.
- Son doğru test-only denemede 27 dataset selector'ın 24'ü geçerliydi ve base-fail/fixed-pass verdi; 3 selector pinned source'ta bulunmuyor veya parametrik node ID kesilmiş.
- **Kalan kapı:** exact dataset row/oracle uyuşmazlığını çözmek. Üç selector sessizce çıkarılmayacak; row değiştirilmeden candidate pass sayılmayacak.

## Aktif teknik batch — doğrulanmış sonuçlar

17 Kasım 2026 itibarıyla 12 adaylı no-inference batch'in sonucu:

| Aday | Teknik sonuç | Sonraki kapı |
|---|---|---|
| Dishka #435 | Stage 2 geçti; Stage 3 gold/E1/E2/E3 teknik incelemesi proje liderince onaylandı | Tam final acceptance record ve schema/registry |
| NumPyro #1916 | 2/2 exact selector base-fail/fixed-pass | Stage 3 |
| PyFar #721 | 23/23 exact selector base-fail/fixed-pass | Stage 3 |
| Robocop #1371 | 1/1 exact selector base-fail/fixed-pass | Stage 3 |
| Meltano SDK #3090 | 1/1 exact selector + bağımsız reproducer base-fail/fixed-pass | Stage 3 |
| Amaranth #1518 | 1/1 exact selector + RTLIL reproducer base-fail/fixed-pass | Model eğitim/veri cutoff maruziyeti çözülmeden Stage 3 |
| EODAG #1530 | 2/2 exact selector + YAML reproducer base-fail/fixed-pass | Stage 3 |
| Python-Control #1144 | 3/3 exact selector + bağımsız reproducer base-fail/fixed-pass | Stage 3 |
| QuTiP #2646 | 1/1 exact selector + bağımsız reproducer base-fail/fixed-pass; tekrar run da geçti | Stage 3 |
| Nox #919 | 24/27 selector geçerli; 3 selector source/parametrik ID uyuşmazlığı | Bloklu; row/oracle kapısı |
| Werkzeug #2955 | 1/2 selector geçerli; diğeri kesilmiş parametrik node ID | Bloklu; row/oracle kapısı |
| Moto #8269 | ECR issue selector 1/1 geçti; row'daki 17 ilgisiz IoT selector'ın 5'i buggy base'te de geçti, 12'si geçersiz | Tam row karışık kapsam nedeniyle bloklu |

Aynı 96 ana kohortta sonraki ayrı doğrulamalar:
- **Dymos #1166, rank 15:** Stage 2 teknik doğrulama geçti; dependency/license kapsamı, bağımsızlık ve Stage 3 insan kararı bekliyor.
- **SkyPilot #5981, rank 17:** 1/1 exact upstream SSH regression selector pinned ortamda base-fail/fixed-pass verdi; 85 paketli lock, license metadata ve artifact hash kontrolleri geçti. Stage 3 ve eğitim verisi zaman maruziyeti incelemesi bekliyor.

**Napalm #2152, rank 19** için de exact frozen dataset selector sabitlenmiş ortamda buggy base üzerinde gerçek assertion failure, fixed revision üzerinde aynı selector için pass verdi. Pinned run 44127350027 / job 134194652784 tamamlandı; temiz artifact 14348056824 (SHA-256 `b2d6934038baf751a43ec890fa1a98763bfc10f27b1dd60b3f47aea24f2ff30d`) 15/15 iç hash kontrolünden geçti. Fixture provenance/lisans konusu Stage 3 hold olarak kalıyor; kabul kararı verilmedi.

**PyThaiNLP #1046, rank 21** için de exact frozen dataset selector pinned ortamda buggy base üzerinde gerçek assertion failure, exact fixed commit üzerinde pass verdi. İki issue örneği ayrıca tek tek test edildi; her ikisi base'de failure, fixed'te pass verdi. Bu iki destek testi yeni vaka veya selector olarak sayılmadı. Pinned run 44133576730 / job 134216923258 tamamlandı; artifact 14351751109 (SHA-256 `ce2ab3bbefd3148510992a7503d8c07b17fb87fe2c2a76173c1971d21e12dcb8`) 17/17 iç hash kontrolünden geçti. Runtime lock ve native ICU sürümleri doğrulandı. Bağımlılıkların tam lisans kapsamı, proje bağımsızlığı ve Stage 3 insan adjudication kapıları açık kaldı.

**Modin #7554, rank 22** için de iki frozen selector (DataFrameGroupBy ve SeriesGroupBy; her ikisi `AutoSwitchBackend=False`) pinned ortamda buggy base üzerinde gerçek `NotImplementedError`, exact fixed commit üzerinde pass verdi. İki selector tek dataset vakasıdır. Run 44137294820 / job 134230204005; artifact 14352871592 (SHA-256 `1eb504d1eafedd1caf395d3731ac4b736302c87b00effdea4234fc9896fffded`) 12/12 iç hash kontrolünden geçti. Ancak issue #7553 başlığı `AutoSwitchBackend is on` derken PR #7554 açıklaması ve frozen selector ID'leri `off/False` kapsamını hedefliyor; issue body boş. Bu nedenle teknik Stage 2 sonucu kaydedildi, aday koşullu kapsam incelemesinde tutuldu ve issue-title/PR-scope uyumu insan kararı bekliyor.

**DataComPy #404, rank 27** için immutable row ve üç frozen selector doğrulandı; ancak aday issue #58'e özgü Stage 2 kapısını geçemiyor. NumPy selector, test metodunun ilk adımında boş olmayan `np.array([j])` girdilerini kontrol ediyor; base mixed-object short-circuit bu noktada tüm sonuçları False yaptığı için empty-array assertion'ına ulaşılmadan test fail edebilir. Diğer iki selector Python-list ve Polars-list desteğini test ediyor. Bu nedenle frozen row mixed-scope / target-oracle hold olarak kaydedildi; hiçbir selector silinmedi veya değiştirilmedi. Discovery run 44138363070 / artifact 14351794927, SHA-256 `6dac19d093acdbc22b0ed009aa2cee5987bf57360bf0f2af9399b91b4797eca1`, 3/3 iç hash doğrulandı. Stage 2 pass sayılmadı.

Bu nedenle son kayıtlı funnel:
- Stage 2 teknik geçiş: **14 aday** (Dishka dahil; Dymos, SkyPilot, Napalm, PyThaiNLP ve Modin için ayrı doğrulamalarla).
- Stage 3 teknik/human adjudication tamamlanan: **1 aday (Dishka)**.
- Nihai kabul edilmiş bağımsız vaka: **0**.
- Nox, Werkzeug ve Moto başarısız aday diye elenmedi; exact dataset row/oracle kusurları nedeniyle bloklu.
- Model yükleme, inference veya eğitim yapılmadı.

Eski run 44097375066 için metodolojik erratum korunur. O run'daki eski test sonuçları, buggy base üzerine tam üretim diff'i uygulanmış olması nedeniyle kabul kapısı açısından karar dışıdır.

## Sonraki ana-kohort sırası

Dymos rank 15, SkyPilot rank 17, Napalm rank 19, PyThaiNLP rank 21 ve Modin rank 22 için teknik Stage 2 yeniden üretimleri tamamlandı. Napalm'ın Stage 3 kapısı Cisco NX-OS fixture provenance/lisans kapsamı nedeniyle; PyThaiNLP'nin Stage 3 kapısı dependency/native license scope, proje bağımsızlığı ve insan adjudication nedeniyle; Modin'in ise issue başlığı ile PR/frozen selector AutoSwitchBackend durumlarının uyuşmazlığı ve bağımlılık lisans incelemesi nedeniyle açık. Modin'in teknik sonucu geçmiştir ancak kapsam kararı koşulludur. DataComPy rank 27 mixed-scope / target-oracle hold olarak kapatıldı; issue-specific frozen selector seti bu haliyle kullanılmayacak. Rank 24 Robocop zaten teknik Stage 2 geçişi olarak kaydedilmiştir ve tekrar çalıştırılmayacaktır. Önceden dondurulmuş sıradaki yeni ana-kohort adayı rank 31 CTAPIpe'dir.

| Rank | Aday | İlk kontrol |
|---:|---|---|
| 19 | Napalm #2152 | Stage 2 geçti (exact selector, pinned base-fail/fixed-pass); Stage 3 için fixture provenance/lisans hold'u |
| 21 | PyThaiNLP #1046 | Stage 2 geçti (exact selector pinned base-fail/fixed-pass; iki ayrı issue reproducer destekleyici); Stage 3 için bağımlılık lisans kapsamı/bağımsızlık/human adjudication hold'u |
| 22 | Modin #7554 | Teknik Stage 2 geçti (iki exact selector pinned base-fail/fixed-pass); issue başlığı AutoSwitchBackend on derken PR/frozen selector False diyor, insan kapsam kararı ve license review bekleniyor |
| 27 | DataComPy #404 | Hold: 3 selector mixed scope; NumPy test boş olmayan array assertion'ında fail olabilir ve empty-array issue oracle'ına ulaşmayabilir; list/Polars-list selector'leri unrelated |
| 31 | CTAPIpe #2732 | Return-type/docstring sözleşme uyuşmazlığı |
| 34 | WeasyPrint #2416 | Pyphen sözlüğü kaynağı/lisansı, issue-test eşleşmesi ve native runtime |

Bu sıra sonuçlara bakılarak yeniden sıralanmaz. Bir aday açıkça geçilemeyen bir kapıda kalırsa, sebebi ve ham kanıtı kaydedilir; sonraki ana-kohort adaya geçilir. Aynı engel için en fazla iki makul düzeltme girişimi yapılır; eşik düşürülmez.

İlerleyen sıralarda 96 ana kohortun kalan kayıtları aynı yöntemle taranır. Ana kohort sonuçları yetersiz kalırsa ancak o zaman 17 bağımsız proje rezervi aynı önceden tanımlı kriterlerle açılır. Yeni aday, sadece sayı düşük diye eklenmez.

## Her aday için zorunlu işlem sırası

1. Issue, PR, canonical repo, exact base/fix commit, dataset row ve timestamp kimliğini doğrula.
2. Issue contract ile FAIL_TO_PASS selector'larının birebir uyuştuğunu incele. Selector'ın pinned source'da bulunmadığı durumları saklama veya sessizce düzeltme.
3. Root/changed-file/fixture/NOTICE ve doğrudan-geçişli dependency license provenance'ını tamamla.
4. Exact buggy base'te sadece test-only diff uygula. Tam PR diff'ini ayrı provenance dosyasında sakla; buggy base'e üretim düzeltmesi taşıma.
5. Her selector'ı boşluk/parametre kimliği korunarak tek argv öğesi halinde çalıştır. Gerçek test assertion failure'ı collection/setup failure'dan ayır.
6. Aynı selector'ları exact fixed commit'te çalıştır ve gerçek pass kaydet.
7. Raw logs, environment lock, commit SHA, dataset-row SHA-256 ve artifact manifestini kaydet.
8. Proje bağımsızlığı, related-issue clustering, researcher/model exposure ve license review kapılarını tamamla.
9. Teknik gold, alternatif mekanizmalar ve nested E1/E2/E3 paketleri oluştur. İnsan kararı ayrı kaydedilir.
10. Complete case-acceptance record schema ve fail-closed registry testlerini geçtikten sonra proje liderinin ayrı final acceptance kararı kaydedilir.

## İzleme metrikleri

Her raporda ayrı ayrı gösterilecek funnel:

- 96 ana adayın statik kapsam incelemesi
- defect-shaped / conditional / held / excluded
- issue-test oracle ve exact row doğrulaması
- license/provenance kapısını geçenler
- teknik base-fail/fixed-pass reproducer'ı geçenler
- bağımsızlık ve maruziyet kapısını geçenler
- gold ve E1/E2/E3 insan kararı tamamlananlar
- final schema/registry kabulü geçenler
- bağımsız upstream proje sayısı

**Mevcut final accepted registry: 0.** Bu sayaç, teknik job PASS veya JSON validator PASS sonucu nedeniyle artırılmaz.
