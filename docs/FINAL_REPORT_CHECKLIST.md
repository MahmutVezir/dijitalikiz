# TÜBİTAK 2204-A Son Rapor Kontrol Listesi — 9 Ekim 2026

## Araştırma çerçevesi
- [x] Proje başlığı ve araştırma sorusu tanımlı.
- [x] H1/H0 ve bağımsız/dependent değişkenler tanımlı.
- [x] İstatistiksel birim bağımsız yazılım vakası; seed'ler tekrar olarak tanımlı.
- [x] Ölçüt değişikliği ve kronolojisi raporda açıklandı; ön kayıt iddiası abartılmıyor.

## Veri ve provenans
- [x] Kaynak ve düzeltme revizyonları kaydedildi.
- [x] Pilot ve confirmatory split birbirinden ayrı.
- [x] 16 confirmatory vaka için contamination riski kayıtlı.
- [x] Pilot/confirmatory çakışması yok.
- [x] Model çıktıları vaka seçimi için kullanılmadı.

## Deneysel kontroller
- [x] Model ID/revision ve yükleme hassasiyeti kaydedildi.
- [x] Prompt/context/system prompt hash'leri kaydedildi.
- [x] Üretim parametreleri ve tohumlar donduruldu.
- [x] İki koşulun temel kanıtı kontrollü tutuldu.
- [x] Ground truth model context'ine verilmedi.
- [x] JSON çıktı şeması ve alias eşleştiricisi donduruldu.
- [x] 40 pilot ve 160 confirmatory run kaydı mevcut.
- [x] Ham çıktılar ve artifact'ler arşivlendi.
- [x] Artifact boyut/manifest/SHA-256 kontrolleri bağımsız doğrulandı.

## İstatistik ve yorum
- [x] Vaka düzeyinde 3/5 çoğunluk kuralı uygulandı.
- [x] Exact iki taraflı McNemar testi uygulandı.
- [x] Alpha 0,05.
- [x] Uyumsuz vaka sayıları ve CCDG-Standard risk farkı raporlandı.
- [x] %95 güven aralığı raporlandı.
- [x] Parse hataları ve tekrarlar raporlandı.
- [x] Birincil ölçütte taban etkisi, eşdeğerlik iddiasından ayrıldı.
- [x] Contamination belirsizliği ve genellenebilirlik sınırlılıkları belirtildi.

## Rapor ve resmî teslim
- [x] Türkçe rapor taslağı gerçek bulgularla güncellendi.
- [x] Model/quantization anlatımı frozen manifest ile uyumlu.
- [x] En az 10 bilimsel kaynak listelendi; kaynaklar girişte numaralı atıflarla kullanıldı.
- [ ] Taslağı 2026–2027 resmî Word şablonuna aktar.
- [ ] Özetin 150–250 kelime ve toplam bölümün güncel sayfa sınırında olduğunu teyit et.
- [ ] Kişi/okul/danışman/izin alanlarını gerçek bilgilerle tamamla.
- [ ] Son PDF'yi oluşturup her sayfayı görsel olarak denetle.
- [ ] TÜBİTAK'ın sorumlu ÜYZ rehberine göre yapay zekâ araçlarının kullanımını şeffaf biçimde beyan et; öğrenci araştırma tasarımını, kodu ve sonuçları açıklayabilmeli.
- [ ] 2026–2027 resmî Word şablonunu doğrudan kullan; bölüm sırası, yazı biçimi ve sayfa düzenini doğrula.
- [ ] Nihai PDF'yi oluştur ve her sayfayı görsel olarak denetle.
- [ ] Öğrenci/okul/danışman ve gerekli izin bilgilerini gerçek kayıtlarla tamamla.
- [ ] TYBS/ARBİS ve teslim gereksinimlerini doğrula.
- [ ] Nihai rapor, sonuç özeti, artifact ve kaynak commit'ini tutarlı biçimde arşivle.
- [ ] Ayrıntılı teslim kapıları: `docs/FINAL_SUBMISSION_AUDIT_2026-10-10.md`.

## Bilimsel karar

Araştırma çalıştırmaları ve artifact doğrulaması tamamlanmıştır. Dondurulmuş birincil ölçütte iki koşul da 0/80 seed ve 0/16 vaka düzeyinde geçiş vermiştir; exact McNemar p=1,00'dır. Bu bir taban etkisi olduğu için semantik CCDG hipotezi çözümlenmiş değildir ve sonuç CCDG'nin etkisizliğini veya iki koşulun eşdeğerliğini kanıtlamaz. Mevcut 160 koşunun birincil skoru değiştirilmemelidir.
