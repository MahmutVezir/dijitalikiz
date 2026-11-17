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

- Teknik yeniden üretim: önceki doğru test-only yöntemli çalışmalarda issue reproducer ve sekiz dataset selector için base FAIL / fixed PASS kanıtı mevcut.
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
- Önceki Actions dataset selector çalıştırmasında shell word splitting parametrik selector'ları bozdu; ayrıca test_validation_options selector'ının pinned upstream koleksiyonunda bulunmadığı görüldü.
- Ortak selector koşucusu artık her node ID'yi tek argv öğesi olarak iletiyor ve selector/collection hatasını gerçek test failure olarak sınıflandırmıyor.
- **Kalan kapı:** yeni run'da tam selector listesi, eksik selector dahil, tek tek değerlendirilmelidir. Uyuşmayan selector sessizce çıkarılmayacak; exact dataset-row/oracle uyuşmazlığı kaydedilecek.

## Aktif teknik batch

17 Kasım 2026 itibarıyla yeni no-inference çalışması [44103128787](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44103128787) için:

- no-inference-preflight: PASS.
- Selector-runner contract tests: PASS.
- 12 candidate job preflight'tan sonra kuyruğa alındı; bu kayıt oluşturulurken henüz candidate sonucu oluşmamıştı.
- Batch: Dishka rank 2, Nox rank 6, Moto rank 9, NumPyro rank 12, EODAG rank 16, Robocop rank 24, Meltano SDK rank 26, Amaranth rank 30, Werkzeug rank 32, Python-Control rank 35, QuTiP rank 39 ve PyFar rank 90.
- Earthkit-data rank 4 bu batch'e dahil değildir; fixture/provenance kapısı çözülmeden çalıştırılmayacaktır.

Bu batch'in önceki run'ı [44097375066](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44097375066) için ayrı metodolojik erratum oluşturuldu. On adayın eski dataset sonuçları, buggy base üzerine tam üretim diff'i uygulanmış olması nedeniyle kabul kapısı açısından karar dışıdır. Eski loglar tarihsel kanıt olarak korunur.

## Sonraki ana-kohort sırası

Aktif batch'in aday sonuçları ve ham logları sınıflandırıldıktan sonra, henüz teknik batch'e alınmamış adaylar ana kohort sıra numarasıyla ele alınır. İlk sonraki inceleme sırası:

| Rank | Aday | İlk kontrol |
|---:|---|---|
| 15 | OpenMDAO / Dymos #1165 | Minimal OpenMDAO ortamı, tüm doğrudan/geçişli bağımlılık lisansları ve daraltılmış issue-specific test |
| 17 | SkyPilot #5985 | SSH/LSTRIP davranışının gerçek entegrasyon yolu ve mock'lu reproducer |
| 19 | Napalm #2152 | Harici fixture ve provenance koşullu hold'u |
| 21 | PyThaiNLP #1046 | Exact row, issue/patch alignment, bağımlılık ve licence gate |
| 22 | Modin #7554 | Exact row, test oracle ve minimal environment |
| 27 | DataComPy #404 | Hedef testin defect-specific olup olmadığı |
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
