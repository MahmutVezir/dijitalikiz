# TÜBİTAK 2204-A Proje Yol Haritası — Güncel Kabul Durumu

## Durum güncellemesi — 18 Ekim 2026

Bu tarihli blok, önceki 9 Ekim yol haritasının yerine geçmez; güncel başvuru/araştırma durumunu netleştirir.

### TÜBİTAK teslim durumu
- Resmî 2026–2027 Word şablonu ile 10 sayfalık rapor DOCX/PDF taslağı üretildi ve tüm sayfalar görsel olarak kontrol edildi. Son doğrulanmış build: https://github.com/MahmutVezir/dijitalikiz/actions/runs/38929963765 (artifact ID `12058990129`).
- Rapor **henüz TYBS'ye gönderilmiş nihai başvuru değildir**. Öğrenci/okul/danışman alanları, güncel ÜYZ kullanım beyanı, kaynakça atıfları, başvuru portalı alanları ve öğrencinin içeriği kendi bilgisiyle doğrulaması son insan kontrolü beklemektedir.
- Resmî yarışma sayfasındaki 2026–2027 son başvuru tarihi: **4 Ocak 2027, 17.30 Türkiye saati**. Başvuru: https://tybs.tubitak.gov.tr/ . Bu tarih değişmedikçe takvim için esas alınır.
- Ana alan **Yazılım**, tematik alan **Yapay Zekâ** olarak önerilmiştir; mevcut deney gerçek zamanlı fiziksel ikiz/sensör sistemi kurmadığı için “Dijital İkiz” sınıflandırması uygun görünmemektedir.

### Bilimsel iddialar ve insan incelemesi
- Tarihsel dondurulmuş sonuç korunur: Standard 0/80, CCDG 0/80; vaka düzeyinde 0/16 ve exact iki taraflı McNemar p=1,00. Bu, eşdeğerlik veya CCDG etkisizliği kanıtı değildir; taban etkisi nedeniyle anlamsal hipotez çözümlenememiştir.
- Tarihsel iki bağlamın bilgi paritesi kusuru geriye dönük giderilemez. Eski birincil ölçüt ve ham çıktılar değiştirilmeyecektir.
- İki kaynak/kök-neden hakemi ve ayrı adjudicator için ön davet e-postaları gönderildi; son kontrol anında yanıt/katılım teyidi yoktu. Kimse kabul etmiş sayılmaz. İnceleme paketleri ancak kişi görevi kabul ettikten sonra gönderilecek.
- Yeni v2 çalışması taslak, aday/held-out vaka listesi boş ve `model_inference_permitted=false`. Bağımsız vaka kaynağı/ground-truth incelemesi, skor kalibrasyonu, örneklem gerekçesi ve protokol dondurma tamamlanmadan inference yapılmamalıdır.

### Teknik aday taraması — yalnızca no-inference
- PR #51: https://github.com/MahmutVezir/dijitalikiz/pull/51
- Son düzeltme sonrası runner kontrolü: https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614091 başarıyla tamamlandı (repository/configuration safety tests ve historical artifact integrity).
- Altı Java vaka adayı için red/green taramasının son tekrarı bu not yazılırken sürmektedir: https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105 . Bu yalnızca hata öncesi regresyonun başarısız, sabit düzeltme revizyonunun başarılı olup olmadığını kontrol eder. İnsan kök-neden incelemesi/adjudication yerine geçmez; modele inference, eğitim veya Kaggle/GPU işi başlatmaz.
- TLS 1.3/Ed25519 adayı mevcut koşuda hata öncesi revizyonda beklenen hatayı göstermedi ve screen kapalı kaldı. Mevcut CI ortamında OpenSSL yolunun çalıştırıldığı kanıtlanmamıştır; bu aday ne doğrulanmış ne de bilimsel olarak çürütülmüş sayılır, uygun ortam/kanıt gerektirir.

### Karar
TÜBİTAK'a en güçlü ve savunulabilir yol; mevcut raporu tamamlanmış tarihsel deney olarak dürüstçe sunmak, taban etkisini ve bilgi paritesi sınırlılığını açık tutmak, yeni v2 çalışmasını tamamlanmış gibi göstermemek ve öğrencinin yöntemi/istatistiği bağımsız olarak açıklayabilmesini sağlamaktır. Finalistlik garanti edilemez. Ek çalışma, ancak gerçek ölçüm kalitesi veya tekrarlanabilirlik katkısı sağlıyorsa yapılmalıdır; sırf daha fazla çıktı üretmek için yeni inference başlatılmamalıdır.

---


**Proje:** LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi  
**Son doğrulanmış durum:** 9 Ekim 2026

## Genel durum

| İş paketi | Durum | Kanıt / not |
|---|---|---|
| Araştırma protokolü ve depo altyapısı | Tamamlandı | Frozen manifestler, istem/hash kontrolleri, şema ve evaluator |
| Model/GPU uyumluluğu | Tamamlandı | Qwen2.5-3B-Instruct, sabit revizyon, FP16/T4; GPTQ alternatifi inference öncesi reddedildi |
| Frozen pilot | Tamamlandı | 40/40 kayıt, 0 parse hatası, artifact 55/55 dosya doğrulandı |
| 16-vakalı doğrulayıcı deney | Tamamlandı | 160/160 kayıt; 212/212 artifact dosyası doğrulandı |
| İstatistiksel çıktı | Tamamlandı | Exact iki taraflı McNemar p=1,00; risk farkı 0,00; %95 CI [-0,1936; 0,1936] |
| Bilimsel hipotezin yorumu | Ölçüm nedeniyle sınırlı | Dondurulmuş literal alias eşleştiricisi taban etkisi gösterdi; CCDG'nin anlamsal etkisi çözümlenmedi |
| Rapor metni | Güncel taslak hazırlandı | Gerçek sonuçlar, skor protokolü değişikliği ve sınırlılıklar açıkça içeriliyor |
| Resmî şablon/PDF ve başvuru sistemi | Son idari işlem | Resmî 2026–2027 Word şablonuna aktarım, öğrenci/danışman bilgileri ve TYBS alanları insan tarafından doğrulanmalı |

## 1. Tamamlanan deney kapıları

- [x] Model kimliği ve tam revision donduruldu.
- [x] Generation ayarları ve beş tohum kaydedildi.
- [x] Standard / CCDG iki koşulu doğrulandı.
- [x] Ground truth'un model bağlamlarına sızmadığı kontrol edildi.
- [x] Pilot 40 inference tamamlandı.
- [x] Pilot JSON/şema ve artifact hash denetimi yapıldı.
- [x] Pilot dışındaki 16 vaka donduruldu.
- [x] Confirmatory scoring rubric hash ile manifest'e bağlandı.
- [x] 160 inference tamamlandı.
- [x] 160 JSON çıktısı ayrıştırıldı; parse hatası bulunmadı.
- [x] Tüm 212 doğrulayıcı artifact dosyası bağımsız hash ve envanter kontrolünden geçti.
- [x] Exact McNemar, risk farkı ve güven aralığı raporlandı.
- [x] Floor effect, contamination riski ve pilot sonrası ölçüt değişikliği yazılı olarak açıklandı.
- [x] README ve sonuç belgeleri güncel duruma göre eşitlendi.
- [x] Artifact yükleme action'ı Node.js 24 kullanan sürüme yükseltildi.

## 2. Sonuçların değiştirilemez bilimsel sınırları

- Dondurulmuş birincil ölçüt: Standard 0/80, CCDG 0/80 seed geçişi.
- Vaka düzeyinde 3/5 çoğunluk: Standard 0/16, CCDG 0/16.
- Exact iki taraflı McNemar p=1,00; uyumsuz vaka sayısı sıfır.
- Bu sonuç ne eşdeğerliği ne de CCDG'nin etkisizliğini ispatlar.
- Alias tabanlı eşleştirici sabit ve tekrarlanabilirdir, fakat semantik bir hakem değildir; tüm çıktılar görüldükten sonra alias eklenemez.
- Pilot çıktılarından sonra, doğrulayıcı çıktılar görülmeden önce skorlama protokolü değişmiştir. Rapor bu kronolojiyi açıkça söylemelidir.
- Bu aynı 160 kaydın yeni bir puanlamayla yeniden sunulması yalnızca keşfedici analiz olabilir; yeni doğrulayıcı kanıt sayılmaz.

## 3. Rapor ve başvuru için kalan işler

- [x] Gerçek sonuçlarla Türkçe tam rapor taslağı hazırla.
- [x] Model konfigürasyonunu rapor ile manifest arasında eşitle.
- [x] Birincil ölçüt ile tam-teşhis ikincil ölçütünü ayır.
- [x] Kaynakça kayıtlarını temel yayın/DOI/başlık bilgileriyle doğrula.
- [ ] İçeriği TÜBİTAK'ın 2026–2027 resmî Word yazım şablonuna son kez aktar.
- [ ] Resmî şablonun zorunlu alanları, bölüm sırası, 150–250 kelime özet ve sayfa aralığı için son kontrolü yap.
- [ ] Öğrenci, okul, danışman ve imza/izin bilgilerini doğru biçimde tamamla; bilinmeyen alanları tahmin etme.
- [ ] Resmî şablondan son PDF'yi üret ve tüm sayfaları görsel olarak kontrol et.
- [ ] TYBS sistemine başvuru bilgilerini gir; ARBİS kayıtlarını/başvuru kılavuzunu kontrol et.
- [ ] Ek kanıtlar (sonuç JSON'u, metodoloji/izin gerekleri, yeniden üretilebilirlik notu) gerekiyorsa ayrı ve kişisel bilgi içermeyen dosyalar olarak hazırla.
- [ ] Son teslimden önce başvuru portalında proje alanının ve dosya adlarının güncel çağrı kurallarına uyduğunu doğrula.

## 4. Kanonik kanıtlar

- Pilot run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402
- Confirmatory run: https://github.com/MahmutVezir/dijitalikiz/actions/runs/37976682761
- Results: `docs/CONFIRMATORY_RESULTS_2026-10-09.md`
- Machine-readable metrics: `data/benchmark/confirmatory_result_summary.json`
- Independent auditor: `scripts/audit_confirmatory_artifact.py`
- Scoring amendment: `docs/CONFIRMATORY_SCORING_PROTOCOL.md`
- Final report content: `docs/TUBITAK_REPORT_DRAFT.md`

## Karar

**Deneysel veri üretimi ve veri bütünlüğü aşaması tamamlandı; anlamsal hipotez dondurulmuş ölçüt ile çözümlenemedi.** Proje raporu bu negatif/taban etkisi bulgusunu dürüstçe raporlamalıdır. Resmî başvuru dosyası ancak güncel TÜBİTAK şablonuna aktarım, kişisel/kurumsal alanların doğrulanması ve nihai PDF incelemesi tamamlandığında başvuruya hazır sayılabilir.
