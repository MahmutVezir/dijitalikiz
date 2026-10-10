# TÜBİTAK 2204-A Son Teslim Denetimi — 10 Ekim 2026

## Kapsam ve resmî kaynaklar

Bu denetim, 2026–2027 (58. yarışma) dönemi için TÜBİTAK'ın güncel 2204-A sayfası ve burada bağlantısı verilen 2026–2027 proje yazma şablonu esas alınarak hazırlanmıştır.

- Resmî yarışma sayfası: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
- 2026–2027 Word şablonu: https://tubitak.gov.tr/sites/default/files/2026-09/proje_yazma_sablonu_2026-2027.docx
- Son başvuru: 4 Ocak 2027, 17.30 (Türkiye saati)
- Başvuru sistemi: https://tybs.tubitak.gov.tr/

## Şu an doğrulanabilen rapor ve deney özellikleri

- Proje başlığı: **LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**
- Başlık uzunluğu: 11 kelime; 15 kelimelik sınırın altında.
- Özet: boşluk temelli sayımda 186 kelime; alternatif sözcük ayırıcısıyla 191. Her iki sayım da 150–250 kelime sınırı içinde.
- Anahtar kelimeler: 5.
- Kaynakça: 11 kaynak; bibliyografik doğruluk ve APA uyumu son insan denetimi bekliyor.
- Rapor taslağı: `docs/TUBITAK_REPORT_DRAFT.md`
- Dondurulmuş sonuç kaydı: `docs/CONFIRMATORY_RESULTS_2026-10-09.md`
- ÜYZ kullanım beyanı taslağı: `docs/AI_USAGE_DISCLOSURE_DRAFT.md`
- Güncel aday taraması ve bağımsız düzeltme tekrarı: `docs/CANDIDATE_SCREENING_2026-10-10.md`; Commons Compress #770 pre-fix/post-fix reproducer: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37993954772
- Makinece okunabilir sonuç özeti: `data/benchmark/confirmatory_result_summary.json`
- Doğrulayıcı artefakt denetimi: 212/212 dosya doğrulandı; 160 doğrulayıcı kayıt, 0 parse hatası, 0 hash uyuşmazlığı.\n- Pilot arşivi manuel denetimi: `docs/PILOT_ARTIFACT_AUDIT_2026-10-10.md`; 55/55 manifest dosyası ve 40/40 kayıt doğrulandı, boyut/hash uyuşmazlığı yok; birincil ölçüt her koşulda 0/20.
- Son kapsamlı doğrulama: https://github.com/MahmutVezir/dijitalikiz/actions/runs/38043725220 — depo testleri, 160 kayıtlık doğrulayıcı artefakt denetimi, 40 kayıtlık pilot artefakt denetimi ve kaynak paketi/launcher kontrolü başarılı; inference işleri bilerek atlandı.
- Resmî Word şablonu indirme ve DOCX bütünlüğü: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37994665457; 2026–2027 DOCX geçerli OOXML paketi olarak doğrulandı.
- Yerel rapor çıktı dosyaları: `TUBITAK_2204A_Rapor_Taslak_2026-2027.docx` ve `.pdf`; ikisi de 9 sayfalık, son render/görsel incelemeden geçirilmiş rapor taslağıdır, henüz nihai başvuru dosyası sayılmazlar.
- Word taslağı SHA-256: `cc9a1f21a3f23bb9d7dc93c6e565bead4dffb296b4ad571d42bc3af1484d81cf`.
- PDF önizlemesi SHA-256: `ec71c66078649040b37ead34f94b4b0d164a19632269c9e74dd5a00bd31d67f4`.
- Teslim manifesti taslağı: `TUBITAK_2204A_Teslim_Manifesti_Taslak.json`; SHA-256: `611010851544b05b1944d6e122c014388e7c4aedcd0c2ff43d10caf8b9e46176`.
- İndirilen resmî şablon SHA-256: `195975a64cda8bc3175c6211be108f2b4293ee0893f061bcdfc3ac184989cc87` (DOCX 25.040 bayt; geçerli OOXML paketi).

## Kritik bilimsel karar — değiştirilmeyecek

Dondurulmuş birincil alias ölçütünde Standard 0/80, CCDG 0/80; her iki koşulda vaka düzeyinde 0/16 çoğunluk başarısı vardır. Exact iki taraflı McNemar p=1,00'dır. Bu taban etkisi, CCDG'nin etkisiz olduğunu veya iki koşulun eşdeğer olduğunu kanıtlamaz.

**Ek metodolojik bulgu:** `dijitalikiz/context.py` içindeki tarihsel Standard Context, Source, Technology, Error description ve I_base içerirken, tarihsel CCDG Context açık Error description bölümünü içermez; bunun yerine açık bağımlılık kenarları ekler. Dolayısıyla eski iki koşul bilgi bakımından eşleştirilmiş değildir ve eski deney grafik gösteriminin etkisini tek başına izole edemez. Bu bulgu `docs/CONTEXT_INFORMATION_PARITY_AUDIT_2026-10-10.md` içinde kayıtlıdır. Tarihsel kod, prompt hash'leri ve sonuçlar yeniden yazılmayacak.

Yeni çalışmanın önerilen tasarımı üç koşulludur: (A) Standard temel bağlam, (B) aynı bağımlılık bilgisi cümlelerle yazılmış bağlam, (C) aynı bağımlılık bilgisi CCDG üçlüleri olarak yazılmış bağlam. Önceden tanımlanacak birincil karşılaştırma C–B olacaktır. B–A ve C–A ikincil karşılaştırmalardır.

Aynı 160 çıktının herhangi bir alternatif puanlama veya kör anlamsal incelemesi yalnızca **keşfedici/post-hoc** olabilir; tarihsel birincil sonucu değiştiremez. Bağımsız iki hakem için koşul/seed etiketi maskelenmiş inceleme dosyası üretildi, ancak henüz insan hakem değerlendirmesi tamamlanmadı. İnceleme paketi:
- `docs/EXPLORATORY_SEMANTIC_REVIEW_GUIDE.md`
- `docs/SCORING_RUBRIC_CALIBRATION_PROTOCOL.md`
- `docs/CONTEXT_INFORMATION_PARITY_AUDIT_2026-10-10.md`

Yeni doğrulayıcı deneyden önce puanlama aracı kaynak kanıtıyla kalibre edilmeli, bağımsız yeni vakalar seçilmeli, model/tokenizer ile prompt token uzunlukları ve hash'leri denetlenmeli, örneklem büyüklüğü varsayımlarla gerekçelendirilmeli ve protokol dondurulmalıdır. Örneklem duyarlılık senaryoları `docs/FOLLOWUP_SAMPLE_SIZE_SENSITIVITY_2026-10-10.md` içindedir; bu olasılıklar eski deneyden tahmin edilmemiş tasarım varsayımlarıdır.

## Ön değerlendirme kriterlerine göre çalışma planı

TÜBİTAK sayfasındaki bağlantılı değerlendirme formunda (son erişilebilir sürüm 2025 PDF) ön değerlendirme ağırlıkları: problem/araştırma sorusu 20, yöntem 20, yaratıcılık ve etki 30, sonuçlar ve tartışma 30. 2026–2027 için yeni bir değerlendirme PDF'si yayımlanırsa bu kayıt güncellenmelidir.

- **Problem ve soru:** CCDG'nin çapraz bileşen kök neden teşhisine katkısı açık ve ölçülebilir tanımlanmalı.
- **Yöntem:** Eski deneyin bilgi-paritesi sınırlılığı açıkça belirtilmeli. Yeni karşılaştırmada aynı bağımlılık bilgisinin yalnızca gösterim biçimi değiştirilerek sunulduğu doğrulanmalı.
- **Yaratıcılık ve etki:** CCDG'nin yenilik iddiası literatürle karşılaştırılmalı; mevcut deney CCDG etkisini veya pratik faydayı kanıtlamadığı için bu yönde iddia kurulmamalı.
- **Sonuçlar ve tartışma:** taban etkisi, puanlama geçerliği, bilgi-paritesi kısıtı, kamuya açık veri nedeniyle contamination riski ve genellenebilirlik sınırları açıkça raporlanmalı.
- **Sunum ve proje hâkimiyeti:** Öğrenci kendi kodunu, deney tasarımını, istatistiği, sınırlılıkları ve yapay zekâ kullanımını açıklayabilmeli.

## Teslim kapıları — durum 10 Ekim 2026

- [x] Resmî 2026–2027 Word şablonu indirildi ve OOXML/ZIP bütünlüğü kontrol edildi: [indirme ve doğrulama akışı](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37994665457).
- [x] Resmî şablonun bölüm sırası, rapor yazım kuralları ve iş-zaman çizelgesi incelendi. Word rapor taslağı bu zorunlu bölüm sırasına ve 12 punto / 2,5 cm / tek satır aralığı koşullarına göre oluşturuldu; 9 sayfa. Dosya orijinal şablonun içeriğinin üzerine doldurulmuş bir form değil, aynı kuralları izleyen düzenlenebilir rapor taslağıdır.
- [x] PDF üretildi; 9 sayfa olarak render edildi ve tüm sayfalar hem DOCX render'ında hem bağımsız PDF render'ında görsel olarak kontrol edildi. Taşan tablo, bozuk Türkçe karakter, kesilmiş metin veya boş sayfa saptanmadı.
- [x] Başlık 11 kelime; özet 186 kelime; anahtar kelime 5. Sayfa sınırı 20 sayfanın altında.
- [ ] **Şablon fontu için son dışa aktarma kontrolü:** DOCX içindeki font ailesi Times New Roman olarak ayarlandı; bu Linux ortamındaki PDF renderı Times New Roman kurulu olmadığı için uyumlu bir serif ikamesiyle üretildi. Nihai PDF'yi Times New Roman kurulu Microsoft Word/uyumlu Office ortamında tekrar dışa aktar ve görsel kontrolü tekrarla.
- [ ] Tüm 11 kaynağın bibliyografik bilgilerini ve APA biçimini insan tarafından doğrula; metin içi atıf-kaynakça eşleşmesini son kez kontrol et.
- [ ] `docs/AI_USAGE_DISCLOSURE_DRAFT.md` ve rapordaki ÜYZ beyanını gerçek kullanım kayıtları ve güncel TÜBİTAK rehberiyle öğrenci olarak gözden geçir; gerçeğe uymayan ifadeleri düzelt.
- [ ] Öğrenci(ler), okul, danışman ve gerekli izin/etik bilgilerini yalnızca doğru bilgilerle sisteme gir. Raporda gereksiz kişisel bilgi yayımlama.
- [ ] Öğrencinin ARBİS/TYBS kayıtlarını güncel resmî kılavuza göre kontrol et ve başvuru sistemindeki alanları doldur.
- [ ] Gereken kod, manifest, çıktı veya ekleri 20 sayfa/boyut ve gizlilik koşullarına göre TYBS'ye ayrıca ekle. GitHub bağlantısı tek başına jüriye erişim garantisi değildir.
- [x] Nihai DOCX/PDF hash'leri, resmî şablon kimliği ve deney artefaktı kanıtlarını bağlayan yerel teslim manifesti taslağı oluşturuldu: `TUBITAK_2204A_Teslim_Manifesti_Taslak.json`. Başvuru öncesi Office dışa aktarma sonrasında hash'ler yeniden hesaplanmalıdır.
- [ ] Başvuruyu 4 Ocak 2027 saat 17.30'dan önce tamamla; son günü bekleme.

## Son durum

**Araştırma çalıştırması tamamlandı; Word rapor taslağı ve PDF önizlemesi hazırlandı, ancak başvuru henüz teslim edilmeye hazır değildir.** Kalan kritik insan denetimleri; kaynakların doğrulanması, ÜYZ kullanım beyanının gözden geçirilmesi, gerçek öğrenci/okul/danışman ve TYBS bilgileri, ayrıca Times New Roman kurulu Office ortamından son PDF dışa aktarımıdır. Yeni semantik doğrulayıcı çalışma ise ayrı bir gelecek araştırmasıdır; mevcut tamamlanmış sonucun yerine geçmez.
