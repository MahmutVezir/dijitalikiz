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
- [x] Tematik alan resmî 2027 rehberine göre yeniden değerlendirildi: mevcut çalışma canlı sensör verisiyle güncellenen bir dijital ikiz kurmadığından rapor `Yazılım / Yapay Zekâ` sınıflandırmasına hizalandı; karar notu `docs/TUBITAK_2027_THEME_DECISION_2026-10-15.md` dosyasındadır.

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


## 5. Repo-side validation status (separate from research results)

- [x] Path filters updated in merge commit `e58303cba30e6dc9727646e389742551a974e6cf` so `docs/**`, `data/benchmark/**`, and `data/sample_cases/**` edits trigger the no-inference validation.
- [ ] Obtain a runner-backed successful `Research Validation (No Inference)` run. Current checks are still runner-blocked: main-branch merge run `38781184907` and PR #29 run `38782157548` failed before steps. Job `116581493867` and job `116584852346` report `runner_id=0`, empty `runner_name`, and `steps=[]`; runner smoke run `38779073729` showed the same pre-step failure. This is not evidence that pytest or artifact validators failed, and it is not a passing run.
- [ ] Repository owner checks `Settings → Actions → General` for hosted `ubuntu-24.04` eligibility and `Settings → Billing and licensing → Usage` for Actions quotas/spending restrictions; then retries validation and verifies actual step outputs.
- [ ] Only after actual test steps execute should repository CI be marked passing. This repository QA gate does not change the frozen experiment outputs or their already recorded integrity audits.

## 7. Tarihsel deney bilimsel denetimi — 15 Ekim 2026

- [x] Historical context renderer farkı vaka düzeyinde denetlendi: Standard'da 16/16 hata açıklaması; CCDG'de 0/16; I_base ve Source/Technology 16/16 ortak.
- [x] Sözcüksel ipucu taraması ile 7/16 vakada I_base içinde açık fix/corrected ipucu, geniş taramada 5/16 vakada ek/örtüşen remediation ipucu bulundu. Bu sayılar regex triage işaretleridir; semantik etiket veya eğitim verisi sızıntısı kanıtı değildir.
- [x] Aktif benchmark manifesti 16 vaka belirtirken arşiv cases klasöründe MATH-844 dahil 17 JSON dosyası vardır. MATH-844 aktif manifest/rubrikte olmadığı için tarihsel örnekleme dahil değildir; dosya inventory raporunda ayrı gösterilir.
- [x] Non-mutating audit script ve dört test taslağı ayrı dalda eklendi. İzole yerel doğrulama harness'inde eşdeğer dört senaryo 4/4 geçti; bu, GitHub Actions veya tam depo pytest geçişi değildir.
- [x] Bu bulgular docs/HISTORICAL_EXPERIMENT_SCIENTIFIC_AUDIT_2026-10-15.md içinde raporlandı ve tarihsel rapor taslağına eklendi.
- [x] Resmî MEB/TÜBİTAK kayıtlarına dayanarak 2023–2026 ödül projeleri kıyaslama notu hazırlandı: docs/TUBITAK_WINNER_BENCHMARK_2023_2026.md. Erişilemeyen tam rapor yöntemleri varsayılmadı.
- [ ] Araştırma denetimi ve rapor güncellemeleri için PR açılmalı/incelemeli; runner ataması çözülmeden otomatik repo testleri geçerli sayılmamalı.

## 6. Kör anlamsal inceleme paketi düzeltmesi — 15 Ekim 2026

- [x] İlk v1.1 inceleme ZIP'lerinde beklenen kök neden `reference.root_cause` olarak ve doğrudan kaynak URL'leriyle gösteriliyordu. Bunlar **geçersiz/superseded** kabul edilmeli ve değerlendiricilere gönderilmemeli.
- [x] Düzeltilmiş v1.2 paketleri üretildi ve kaynak arşivdeki 160/160 kayıtla ham çıktı SHA-256 değerleri eşleştirildi. Yeni paket hash'leri ve sınırlılıklar `docs/BLINDED_SEMANTIC_REVIEW_PACKET_AUDIT_2026-10-15.md` dosyasındadır.
- [ ] Gerçek bağımsız değerlendiriciler paketi ayrı ayrı tamamlayıp ilk kararlarını kilitlemeli; boş paketler insan değerlendirmesi sayılmaz.
- [ ] Kaynak-koda dayalı hakemlik yalnızca iki bağımsız değerlendirme kilitlendikten sonra ayrı adjudication kaydında yapılmalı. İlk puanların bu sürümü, kanıt özetine dayalı keşifsel değerlendirmedir; bağımsız kaynak kodu doğrulaması değildir.
- [ ] CI runner sorunu çözülüp gerçek test adımları çalışana kadar PR #29'daki kod değişikliği testlerden geçmiş sayılmamalıdır.
