# TÜBİTAK 2204-A Son Rapor Kontrol Listesi — 15 Ekim 2026

## 1. Tamamlanmış tarihsel araştırma

- [x] Proje başlığı, araştırma sorusu, hipotez ve değişkenler tanımlı.
- [x] İstatistiksel birim bağımsız yazılım vakası; seed'ler tekrar ölçümleri olarak ele alındı.
- [x] Pilot (40 kayıt) ve doğrulayıcı deney (160 kayıt) ayrı tutuldu.
- [x] Model/checkpoint, çalışma ortamı, istem/bağlam hash'leri ve üretim ayarları kayıtlı.
- [x] Ham çıktılar, artifact manifestleri ve SHA-256 kontrolleri arşivlendi.
- [x] Dondurulmuş birincil ölçüt, exact iki taraflı McNemar testi, eşleştirilmiş risk farkı ve %95 güven aralığı raporlandı.
- [x] Taban etkisi, bilgi-paritesi sorunu, contamination riski ve genellenebilirlik sınırlılıkları açıklandı.
- [x] Pilot sonrası puanlama değişikliğinin kronolojisi şeffaf biçimde belirtildi; tam ön kayıt iddiası ileri sürülmedi.
- [x] Tarihsel sonuçlar değiştirilmedi: Standard 0/80, CCDG 0/80, vaka düzeyinde 0/16 başarı her iki koşulda; exact iki taraflı McNemar p=1,00. Bu, CCDG'nin etkisizliğini veya koşulların eşdeğerliğini kanıtlamaz.

## 2. Rapor taslağı ve biçim denetimi

- [x] Rapor, resmî 2026–2027 Word şablonu kullanılarak üretildi.
- [x] Başlık 11 kelime; 15 kelime sınırının içinde.
- [x] Özet boşlukla sayımda 186, regex sayımında 191 kelime; 150–250 aralığında.
- [x] Beş anahtar kelime kullanıldı.
- [x] 10 sayfalık PDF üretildi; 20 sayfalık üst sınıra uyuyor.
- [x] PDF açılabilir, şifrelenmemiş ve metin tabanlı.
- [x] DOCX OOXML paketi ve tablo yapısı doğrulandı.
- [x] Tüm 10 sayfa görüntüye dönüştürülüp görsel olarak incelendi.
- [x] Sonuç tablosundaki yüzdeler düzeltildi (0%, yüzde işareti artık sayıdan önce değil).
- [x] İş-zaman çizelgesi, tamamlanmış tarihsel deneyi gelecekteki takip araştırmasından ayıracak şekilde düzeltildi.
- [x] Eski pilot ve doğrulayıcı artifact hash'leri, kayıt sayıları ve sonuçlar değiştirilmedi.

## 3. Başvuru öncesinde öğrenci tarafından yapılması gerekenler

- [ ] Öğrenci raporu baştan sona okuyup yöntem, kod, istatistik, sınırlılıklar ve sonuçları bağımsız biçimde açıklayabildiğini doğrulamalı.
- [ ] ÜYZ kullanım beyanını gerçek kullanım kaydı ve güncel TYBS alanlarıyla eşleştirip onaylamalı.
- [ ] TYBS isterse öğrenci, okul, danışman ve izin alanları yalnızca gerçek/otoritatif bilgilerle tamamlanmalı; bu taslakta bilgi uydurulmamalı.
- [ ] Resmî 2026–2027 rehberindeki son dosya, biçim ve yükleme gereksinimleri başvuru anında yeniden kontrol edilmeli.
- [ ] ARBİS/TYBS kayıtları doğrulanmalı ve son rapor teslim sistemine öğrenci/okul yetkilisi tarafından gönderilmeli.
- [ ] Güncel DOCX/PDF SHA-256 değerleri başvuru öncesi son sürümde yeniden kontrol edilmeli.

## 4. Ayrı tutulması gereken takip araştırması

- [x] Yeni üç koşullu takip tasarımı, tarihsel sonucun yerine geçmeyecek gelecekteki araştırma olarak tanımlandı.
- [x] V2 protokolü `draft` ve `model_inference_permitted=false` durumunda tutuluyor.
- [ ] Yeni vakalar için bağımsız kaynak incelemesi, iki değerlendirici ve ayrı hakem kararları tamamlanmalı.
- [ ] Puanlama kalibrasyonu/düzeyler arası uyum doğrulanmalı.
- [ ] Model/tokenizer uyumluluğu, prompt token/hash denetimi, randomize sıra ve analiz hash'leri tamamlanıp protokol dondurulmalı.
- [ ] Altı yeni adayın gerçek red-green testleri yalnızca GitHub runner atama sorunu çözüldükten sonra çalıştırılmalı. Son önceki deneme hiç adım çalıştırmadığı için bu adaylar için kanıt sayılmaz.

## Bilimsel sonuç

Tarihsel deney ve artefakt denetimleri tamamlanmıştır; ancak donmuş literal-alias ölçütünün taban etkisi nedeniyle semantik CCDG hipotezi çözümlenmemiştir. Mevcut sonuçlar değiştirilmemeli. Takip araştırması öneri olarak raporlanmalı ve tamamlanmış tarihsel çalışmanın verisiyle karıştırılmamalıdır.

Başvuruya hazır Word/PDF üretimleri bu depodaki kaynak taslaktan ayrı teslim dosyalarıdır; kişisel başvuru alanları doğrulanmadığı ve TYBS gönderimi yapılmadığı için bu rapor **nihai gönderim** değildir.
