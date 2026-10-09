# TÜBİTAK 2204-A Son Teslim Denetimi — 10 Ekim 2026

## Kapsam ve resmî kaynaklar

Bu denetim, 2026–2027 (58. yarışma) dönemi için TÜBİTAK'ın güncel 2204-A sayfası ve burada bağlantısı verilen 2026–2027 proje yazma şablonu esas alınarak hazırlanmıştır.

- Resmî yarışma sayfası: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
- 2026–2027 Word şablonu: https://tubitak.gov.tr/sites/default/files/2026-09/proje_yazma_sablonu_2026-2027.docx
- Son başvuru: 4 Ocak 2027, 17.30 (Türkiye saati)
- Başvuru sistemi: https://tybs.tubitak.gov.tr/

## Şu an doğrulanabilen rapor özellikleri

- Proje başlığı: **LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**
- Başlık uzunluğu: 11 kelime; 15 kelimelik sınırın altında.
- Özet: 179 kelime; 150–250 kelime aralığında.
- Anahtar kelimeler: 5; mevcut rehber sayfasındaki sınırla uyumlu.
- Kaynakça: 11 kaynak.
- Rapor taslağı: `docs/TUBITAK_REPORT_DRAFT.md`
- Bilimsel sonuç kaydı: `docs/CONFIRMATORY_RESULTS_2026-10-09.md`
- Makinece okunabilir sonuç özeti: `data/benchmark/confirmatory_result_summary.json`
- Deney artefakt denetimi: 212/212 dosya doğrulandı; 160 doğrulayıcı kayıt, 0 parse hatası, 0 hash uyuşmazlığı.
- Son rapor düzenlemesinden sonra doğrulama workflow'u başarılı tamamlandı: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37990926952
- Son doğrulama yalnızca doğrulama amaçlıydı; yeni inference çalıştırılmadı.

## Kritik bilimsel karar — değiştirilmemeli

Dondurulmuş birincil alias ölçütünde Standard 0/80, CCDG 0/80; her iki koşulda da vaka düzeyinde 0/16 çoğunluk başarısı vardır. Exact iki taraflı McNemar p=1,00'dır. Bu taban etkisi, CCDG'nin etkisiz olduğunu veya iki koşulun eşdeğer olduğunu kanıtlamaz. Mevcut doğrulayıcı çıktılar geriye dönük yeniden puanlanırsa bu sonuçlar yalnızca keşfedici olarak etiketlenebilir. Yeni doğrulayıcı iddia için ölçüm aracı bağımsız değerlendiricilerle önceden doğrulanmalı ve yeni bağımsız vaka örneklemi sonuçlara bakılmadan önce kaydedilmelidir.

## Ön değerlendirme kriterlerine göre çalışma planı

TÜBİTAK sayfasındaki bağlantılı değerlendirme formunda (son erişilebilir sürüm 2025 PDF) ön değerlendirme ağırlıkları: problem/araştırma sorusu 20, yöntem 20, yaratıcılık ve etki 30, sonuçlar ve tartışma 30. 2026–2027 için yeni bir değerlendirme PDF'si yayımlanırsa bu kayıt güncellenmelidir.

- **Problem ve soru:** CCDG'nin çapraz bileşen kök neden teşhisine katkısı açık ve ölçülebilir tanımlanmalı.
- **Yöntem:** eşleştirilmiş Standard/CCDG koşulları, vaka başına beş sabit seed, 3/5 vaka çoğunluk kuralı, model/revizyon, prompt hash'leri ve istatistiksel birim açıkça anlatılmalı.
- **Yaratıcılık ve etki:** CCDG'nin yenilik iddiası literatürle karşılaştırılmalı; deney etkisiz/kararsız sonuç verdiğinden pratik fayda kanıtlanmış gibi yazılmamalı.
- **Sonuçlar ve tartışma:** taban etkisi, ölçüm geçerliği, kamuya açık veri nedeniyle contamination riski ve genellenebilirlik sınırları açıkça raporlanmalı.
- **Sunum ve proje hakimiyeti:** final aşamasında ağırlığı yüksek olan sözlü savunma için öğrenci kendi kodunu, deney tasarımını, istatistiği, sınırlılıkları ve yapay zekâ kullanımını açıklayabilmeli.

## Teslimden önce zorunlu kapılar

- [ ] 2026–2027 resmî Word şablonunu indir ve başlık alanlarını, bölüm sırasını, biçimi ve talimatları doğrudan şablon üzerinde doğrula.
- [ ] Raporu resmî şablona aktar; mevcut taslak başlıkları şablondaki zorunlu alanlarla karşılaştır.
- [ ] PDF üret; toplam uzunluğun güncel rehberdeki sayfa sınırına uyduğunu doğrula.
- [ ] PDF'yi sayfa sayfa görsel olarak incele: taşan tablo, boş sayfa, kopuk başlık, okunmayan kod/şekil, yanlış sayfa numarası veya bozuk Türkçe karakter olmamalı.
- [ ] Tüm atıfların kaynakçayla bire bir eşleştiğini ve bibliyografik bilgilerin doğruluğunu kontrol et.
- [ ] TÜBİTAK'ın Üretken Yapay Zekânın Sorumlu ve Güvenilir Kullanımı rehberini incele; izin verilen beyan biçimine göre araç kullanımını şeffaf biçimde belirt. Araç kullanımı öğrenciye ait araştırma tasarımı, kodun anlaşılması ve sonuçların doğrulanmasının yerini almamalı.
- [ ] Öğrenci/öğrenciler, okul, danışman ve gerekli izin/etik alanlarını yalnızca doğru bilgilerle doldur; tahmin veya uydurma bilgi kullanma.
- [ ] Öğrenci ve varsa danışmanın ARBİS kayıtlarını güncelle; TYBS başvuru ve yükleme adımlarını resmî kılavuza göre kontrol et.
- [ ] Dosya adı, kişisel bilgi içermeme, PDF uzantısı ve boyut koşullarını güncel çağrı metnine göre denetle.
- [ ] Nihai PDF, rapor kaynak commit'i, sonuç JSON'u ve artifact kanıtlarını aynı son sürüme bağlayan bir teslim manifesti oluştur.
- [ ] Başvuruyu 4 Ocak 2027 saat 17.30'dan önce tamamla; son günü bekleme.

## Son durum

**Araştırma çalıştırması tamamlandı; başvuru dosyası henüz teslim için tamamlanmış sayılmaz.** En büyük kalan işler resmî Word şablonuna aktarım, PDF görsel denetimi, doğru kişi/okul/danışman bilgilerinin eklenmesi ve yapay zekâ kullanımının rehbere uygun biçimde beyan edilmesidir.
