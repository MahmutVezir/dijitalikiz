# TÜBİTAK 2204-A rapor derlemesi — 16 Ekim 2026

**Durum:** Başarılı derleme; öğrenci tarafından son içerik onayı ve başvuru öncesi kontrol hâlâ gerekli. Bu kayıt, başvuru gönderimi veya tamamlanmamış araştırmanın tamamlandığı iddiası değildir.

## Kaynaklar ve derleme kanıtı

- Kaynak depo: `MahmutVezir/dijitalikiz`
- Kaynak dalı: `fix/tubitak-report-build-toc`
- Kaynak commit: `1ee867c24ac71c7bf36e6b66c4f8598ce65b5e9b`
- Resmî Word şablonu: https://tubitak.gov.tr/sites/default/files/2026-09/proje_yazma_sablonu_2026-2027.docx
- Şablon indirme/derleme workflow'u: https://github.com/MahmutVezir/dijitalikiz/actions/runs/38928518027
- Workflow artifact: `tubitak-official-template-2026-2027`, artifact ID `12057054078`; GitHub'da kısa süreli saklanır.
- Üretilen artifact ZIP SHA-256: `24611f2cfaf68e4bc1e88c6e49918e5d75e187e5b73344d49d2ac590a46f1e74`
- Markdown kaynak SHA-256: `a1ae03ac0ee2cfbb5417934cdb4163023f77d2e4db9f858ac23448469b7d52ba`
- Resmî DOCX şablon SHA-256: `195975a64cda8bc3175c6211be108f2b4293ee0893f061bcdfc3ac184989cc87`
- Üretilen DOCX SHA-256: `f9d447653bf10fe474600a273777eac021b6eef162fb780f3ada87e6fb862128`
- Üretilen PDF SHA-256: `6c74600d1e7ebf866258f012cbfed29122f6aba4b696174caddc1f76b3e7158a`

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

## İlk başarısız derlemeden öğrenilenler

Workflow run `38797017701`, 16 Ekim 2026 retry attempt #2'de resmî şablonu başarıyla indirmiş; ancak kaynak Markdown'daki geçici içindekiler başlığı, `scripts/build_tubitak_report_docx.py` bölüm sırası kontrolünü durdurmuştur. Bu rapor kaynağından sadece navigasyon bloğu kaldırıldı; bilimsel paragraflar, tablolar, tarihsel sonuçlar, istemler veya veri artefaktları değiştirilmedi. Sonraki build run `38928518027` başarıyla tamamlandı.
