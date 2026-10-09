# TÜBİTAK 2204-A Proje Yol Haritası — Güncel Kabul Durumu

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
