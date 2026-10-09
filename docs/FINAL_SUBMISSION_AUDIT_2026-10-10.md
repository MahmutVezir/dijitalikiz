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
- Özet: 179 kelime; 150–250 kelime aralığında.
- Anahtar kelimeler: 5.
- Kaynakça: 11 kaynak.
- Rapor taslağı: `docs/TUBITAK_REPORT_DRAFT.md`
- Dondurulmuş sonuç kaydı: `docs/CONFIRMATORY_RESULTS_2026-10-09.md`
- ÜYZ kullanım beyanı taslağı: `docs/AI_USAGE_DISCLOSURE_DRAFT.md`
- Güncel aday taraması ve bağımsız düzeltme tekrarı: `docs/CANDIDATE_SCREENING_2026-10-10.md`; Commons Compress #770 pre-fix/post-fix reproducer: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37993954772
- Makinece okunabilir sonuç özeti: `data/benchmark/confirmatory_result_summary.json`
- Deney artefakt denetimi: 212/212 dosya doğrulandı; 160 doğrulayıcı kayıt, 0 parse hatası, 0 hash uyuşmazlığı.
- Son kapsamlı doğrulama: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37992620612 — testler, bütünlük denetimi ve kaynak paketi/launcher kontrolü başarılı; inference işleri bilerek atlandı.

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

## Teslimden önce zorunlu kapılar

- [ ] 2026–2027 resmî Word şablonunu indir ve başlık alanlarını, bölüm sırasını, biçimi ve talimatları doğrudan şablon üzerinde doğrula.
- [ ] Raporu resmî şablona aktar; mevcut taslak başlıklarını zorunlu alanlarla karşılaştır.
- [ ] PDF üret; sayfa sınırını güncel resmî talimatlardan doğrula.
- [ ] PDF'yi sayfa sayfa görsel olarak incele: taşan tablo, boş sayfa, kopuk başlık, okunmayan şekil, yanlış sayfa numarası veya bozuk Türkçe karakter olmamalı.
- [ ] Tüm atıfların kaynakçayla bire bir eşleştiğini ve bibliyografik bilgilerin doğruluğunu kontrol et.
- [ ] TÜBİTAK'ın Üretken Yapay Zekânın Sorumlu ve Güvenilir Kullanımı rehberini incele ve gerekli şeffaf beyanı yap; `docs/AI_USAGE_DISCLOSURE_DRAFT.md` taslağını gerçek kullanım kayıtlarıyla doğrula.
- [ ] Öğrenci/öğrenciler, okul, danışman ve gerekli izin/etik alanlarını yalnızca doğru bilgilerle doldur.
- [ ] Öğrenci ve varsa danışmanın ARBİS/TYBS kayıtlarını güncel resmî kılavuza göre kontrol et.
- [ ] Dosya adı, gizlilik, PDF uzantısı ve boyut koşullarını güncel çağrı metnine göre denetle.
- [ ] Nihai PDF, rapor kaynak commit'i, sonuç JSON'u ve artifact kanıtlarını aynı sürüme bağlayan teslim manifesti oluştur.
- [ ] Başvuruyu 4 Ocak 2027 saat 17.30'dan önce tamamla; son günü bekleme.

## Son durum

**Araştırma çalıştırması tamamlandı; başvuru dosyası henüz teslim için tamamlanmış sayılmaz.** En önemli bilimsel sonraki aşama, puanlama geçerliğini ve yeni üç koşullu bilgi-eşleştirilmiş tasarımı doğrulamak; başvuru tarafında ise resmî Word şablonuna aktarım, PDF görsel denetimi, doğru kişi/okul/danışman bilgileri ve yapay zekâ kullanım beyanıdır.
