# TÜBİTAK 2204-A rapor derlemesi — 16 Ekim 2026

**Durum:** Başarılı derleme; öğrenci tarafından son içerik onayı ve başvuru öncesi kontrol hâlâ gerekli. Bu kayıt, başvuru gönderimi veya tamamlanmamış araştırmanın tamamlandığı iddiası değildir.

## Kaynaklar ve derleme kanıtı

- Kaynak depo: `MahmutVezir/dijitalikiz`
- Kaynak dalı: `fix/tubitak-report-build-toc`
- Kaynak commit: `4c4bac3966cc36e84e2dbf1b60e8fe85056b157a`
- Resmî Word şablonu: https://tubitak.gov.tr/sites/default/files/2026-09/proje_yazma_sablonu_2026-2027.docx
- Şablon indirme/derleme workflow'u: https://github.com/MahmutVezir/dijitalikiz/actions/runs/38928518027
- Workflow artifact: `tubitak-official-template-2026-2027`, artifact ID `12058990129`; GitHub'da kısa süreli saklanır.
- Üretilen artifact ZIP SHA-256: `92f8146fc32e60f72f548ff0036451d1927cf89f40a5042ca091f5294296e7ba`
- Markdown kaynak SHA-256: `a1ae03ac0ee2cfbb5417934cdb4163023f77d2e4db9f858ac23448469b7d52ba`
- Resmî DOCX şablon SHA-256: `195975a64cda8bc3175c6211be108f2b4293ee0893f061bcdfc3ac184989cc87`
- Üretilen DOCX SHA-256: `72c6f407731be03ec2a57f7fb45b742d2390b6d70a84d3a90c473754f054434f`
- Üretilen PDF SHA-256: `90f8dc0873ac062c124bbb1fd31c428ec26fecb9ef89fd38af1a85eb3fc921b8`

## Biçim ve bütünlük denetimleri

- Resmî şablon DOCX paketi açıldı; `word/document.xml` bulundu; ZIP bütünlük testi geçti.
- DOCX ve PDF aynı kaynak Markdown ve aynı resmî şablon hash'leriyle derlendi.
- Belge: A4, 10 sayfa, şifrelenmemiş, aranabilir metin içeriyor.
- Başlık: 11 kelime; özet: 191 kelime; anahtar kelime: 5.
- Kenar boşlukları: üst/alt/sol/sağ yaklaşık 2,499 cm; gövde yazı tipi Times New Roman 12 pt.
- DOCX: tek bölüm, 4 tablo, tek sayfa numarası alanı.
- Gerekli 12 bölüm başlığı doğru sırada yer alıyor. Taslak yardımcı “İçindekiler (taslak gezinme)” bloğu kaynak Markdown'dan kaldırıldı; bu blok oluşturucunun resmi sıra denetimini durduruyordu ve nihai rapor gövdesinde kullanılmamalıydı.
- PDF ve DOCX ayrı render akışlarında 10'ar sayfa üretti; 10 PDF sayfasının tamamı ve 10 DOCX render sayfasının tamamı görsel olarak incelendi. Kesilmiş metin, örtüşme veya eksik glif gözlenmedi.
- Derleme manifesti; kaynak Markdown, şablon, DOCX ve PDF hash'lerini aynı çıktı kaydında tutuyor.

## Bilimsel ve başvuru sınırları

- Tarihsel deney sonucu değişmedi: literal-alias endpoint altında Standard 0/80 ve CCDG 0/80; vaka düzeyinde 0/16 başarı iki koşulda da; exact iki taraflı McNemar p=1,00. Bu, yöntemlerin eşdeğerliğini veya CCDG'nin etkisizliğini kanıtlamaz.
- Tarihsel bağlamlar bilgi açısından eşleştirilmemiştir; grafik biçiminin tek başına nedensel etkisi çıkarılamaz.
- 160 tarihsel yanıt için gerçek insan değerlendirici puanları/uyumu hâlâ mevcut değildir. Kappa veya semantik başarı oranı raporlanmamıştır.
- V2 protokolü ayrı bir gelecek çalışma olarak kalır: `status=draft`, `model_inference_permitted=false`, vaka listesi boş ve bütün kapılar beklemede.
- ÜYZ kullanım beyanı TASLAKTIR; öğrenci gerçek kullanımla eşleştirip onaylamalıdır. Öğrenci raporu, yöntemleri, istatistiği ve sınırları bağımsız olarak açıklayabildiğini doğrulamalıdır.
- Bu derleme kişisel başvuru alanlarını, TYBS kaydını veya öğrenci/okul onayını tamamlamaz. PDF başvuruya gönderilmiş değildir.

## Nihai yeniden derleme doğrulaması

PR #41, PR #40'ın başına temiz biçimde yığıldıktan sonra aynı rapor kaynağı ve aynı resmî şablonla yeniden derlendi. Seçilen son çıktı, workflow run `38929963765` ve artifact ID `12058990129` üzerinden indirildi; PDF/DOCX hash'leri bu son paketle eşleştirildi. Kaynak Markdown SHA-256 değişmedi. Bu son çıktı için PDF yeniden render edildi ve 10 sayfalık kontakt sayfası tekrar gözden geçirildi.

## İlk başarısız derlemeden öğrenilenler

Workflow run `38797017701`, 16 Ekim 2026 retry attempt #2'de resmî şablonu başarıyla indirmiş; ancak kaynak Markdown'daki geçici içindekiler başlığı, `scripts/build_tubitak_report_docx.py` bölüm sırası kontrolünü durdurmuştur. Bu rapor kaynağından sadece navigasyon bloğu kaldırıldı; bilimsel paragraflar, tablolar, tarihsel sonuçlar, istemler veya veri artefaktları değiştirilmedi. Sonraki build run `38929963765` başarıyla tamamlandı.
