# TÜBİTAK 2204-A Proje Yol Haritası — Güncel Kabul Durumu

## Operasyonel güncelleme — 18 Ekim 2026, en son denetim

Bu bölüm, aşağıdaki tarihsel notları silmeden güncel durumu tamamlar.

### Resmî şartname ve başvuru bütünlüğü
- 2026–2027 çağrı metni ve proje rehberi resmî TÜBİTAK sayfasında yayımlıdır. Şu an görünen son başvuru: **4 Ocak 2027, 17.30 Türkiye saati**. Başvuru TYBS üzerinden yapılır: https://tybs.tubitak.gov.tr/
- Güncel kural bazlı uygunluk matrisi PR #55 ile ana dala alındı: https://github.com/MahmutVezir/dijitalikiz/blob/main/docs/TUBITAK_2027_RULE_BY_RULE_COMPLIANCE_MATRIX_2026-10-18.md . Doğrulama koşusu 39138496424 başarılıdır. Bu, matris dosyasının doğrulanmasıdır; başvuru sahibinin bütün kuralları karşıladığını kanıtlamaz.
- Önceki yıl TÜBİTAK'a başvuru ve son başvuru tarihinden önce başka yarışmaya aynı/benzer proje sunma bilgisi hâlâ başvuru sahibi tarafından doğrulanmalıdır. Bu iki bilgi tahmin edilmemeli; netleşmeden başvuruya son onay verilmemelidir.
- TÜBİTAK'ın Ocak 2026 ÜYZ rehberi: https://tubitak.gov.tr/sites/default/files/2026-01/UYZ_Rehberi_v04_TR.pdf . Proje taslağı/kod/analiz gibi önemli ÜYZ kullanımının online formun özel alanında; araç ve sürüm, kullanılan aşamalar/bölümler, kullanımın niteliği ve kapsamı belirtilerek beyan edilmesi gerekir. Mevcut rapordaki paragraf bu alanın yerine geçmez; final beyanı gerçek kullanım kayıtlarıyla eşleştirilmelidir.
- Kaynak kodu stili tutarlı ve profesyonel olacak şekilde iyileştirilebilir. Fakat commit/provenance kayıtları veya zorunlu ÜYZ beyanı, katkıyı gizleyip yalnızca insan yazmış izlenimi yaratmak için silinmemeli ya da yanıltıcı biçimde yeniden yazılmamalıdır. Gerçek insan katkısı, araç yardımı ve kontrol adımları ayrıştırılmalıdır.

### V2 bilimsel kalite ilerlemesi
- PR #53 ile bilgi eşleştirme, kaynak kabulü, kör puanlama/kalibrasyon ve öğrenci savunması kalite kapıları ana dala alındı: https://github.com/MahmutVezir/dijitalikiz/blob/main/docs/V2_QUALITY_GATES_2026-10-18.md . No-inference doğrulaması 39137180429 başarılıdır.
- PR #54 ile A/B/C temel bağlam eşitliği, B/C kenar listesi sırası/alanları ve parite sözleşmesi için testler ana dala alındı: https://github.com/MahmutVezir/dijitalikiz/commit/4ee1d39d77886c3d980641607b0899f91c60a159 . No-inference doğrulaması 39137689364 başarılıdır.
- PR #56 ile vaka kimliği/kaynak URL'si/tarih ve ground-truth alanlarının A/B/C model bağlamlarına sızmasını canary değerlerle test eden ek test ana dala alındı: https://github.com/MahmutVezir/dijitalikiz/commit/7cee91d778ecdf2384bc1dd36b58266f29752c37 . No-inference doğrulaması 39139372063 başarılıdır.
- V2 manifestinin durumu hâlâ `status=draft`, `model_inference_permitted=false`; vaka listesinde sıfır kabul edilmiş yeni vaka vardır ve dokuz kapının tümü beklemektedir. Hiçbir yeni inference, training, GPU veya Kaggle çalışması başlatılmadı.
- Teknik red/green taramasındaki beş geçiş, insan kaynak incelemesi veya vaka kabulü yerine geçmez. TLS 1.3/Ed25519 adayı uygun OpenSSL yolunda hedeflenen hata öncesi başarısızlığı kanıtlayana kadar engelli kalır.
- Akademik kaynak incelemesi/hakemlik için ön davetler gönderildi; son posta kontrolünde kabul/yanıt görünmüyordu. Kabul teyidi olmadan kör paket gönderilmemeli; hiçbir puan, uzlaşma ya da adjudication yapılmış gibi kaydedilmemelidir.

### Teslim raporu ve öğrenci sahipliği
- Son doğrulanmış rapor derlemesi 10 sayfa DOCX/PDF'yi görsel kontrolden geçirdi: https://github.com/MahmutVezir/dijitalikiz/actions/runs/38929963765 . Bu önceki kaynak sürümünün derleme kanıtıdır; son içerik onayı ve başvuru tamamlanması değildir.
- Öğrenci, yöntemi, tüm sonuçları, sınırlılıkları, kaynak delillerini ve ÜYZ kullanımını kendi cümleleriyle açıklayabilmelidir. Herhangi bir iddiayı anlayamıyorsa ezberlemek yerine kaynakla doğrulamalı ve gerekirse düzeltmeli/kaldırmalıdır.
- İzin/etik/onam gerekliliği, insan puanlama yöntemine göre başvuru sahipleri tarafından önceden değerlendirilmelidir. Gereken belgeler veri toplanmadan önce alınmalı; “izin gerekmez” varsayımıyla ilerlenmemelidir.
- Mevcut başvuru son onayı, doğru kişisel/okul/danışman bilgileri, ARBİS/TYBS kayıtları, önceki yarışma durumu ve ÜYZ özel beyanı öğrenci/başvuru sahibi tarafından yapılmadan tamamlandı sayılmaz.

---

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
- Son düzeltme sonrası repository/configuration safety tests ve historical artifact integrity, run 39135614091'de başarıyla tamamlandı.
- Altı Java vaka adayı için red/green taraması run 39135614105'te tamamlandı: beş adayda hata öncesi regresyon başarısızlığı ve sabit düzeltme sürümünde temiz geçiş doğrulandı; bir TLS 1.3/Ed25519 adayı fail-closed kaldı. Kanıtlar: https://github.com/MahmutVezir/dijitalikiz/actions/runs/39135614105 .
- TLS adayının günlüğünde sabitlenmiş hata öncesi sürümde 7 testin tamamı başarılıydı (0 fail, 0 error, 0 skip); beklenen kırmızı regresyon gösterilemedi. Düzeltme kodunun hedeflediği OpenSSL yolunun bu ortamda çalıştırıldığı kanıtlanmamıştır. Bu aday “geçti” veya “çürütüldü” olarak değil, uygun native/OpenSSL test kanıtı bekleyen bloklu aday olarak tutulmalıdır. Diğer beş teknik red/green geçişi de yalnızca regresyon yeniden üretilebilirliğini gösterir; insan kök-neden incelemesi/adjudication yerine geçmez.
- Tarama model inference, eğitim veya Kaggle/GPU işi başlatmadı. PR #51 taslaktır; ekranlama sonucuna bakılarak otomatik vaka kabulü veya protokol açılması yapılmamalıdır.

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


## 2026-10-18 — Submission-integrity and repository-quality gate

### Goal
Prepare a complete, student-owned, scientifically defensible 2026–2027 TÜBİTAK 2204-A application, aiming for the Türkiye final without promising an outcome or misrepresenting work.

### Required order before cosmetic repository cleanup
1. **Eligibility and contest-history stop gate:** obtain the applicant's truthful confirmation of age/school eligibility, prior TÜBİTAK submissions, and any prior/planned submission of the same or similar project to another competition. Do not submit until any disqualifying ambiguity is resolved.
2. **Finish the actual research, not just the code:** retain historical results unchanged; complete independent source/license/revision checks for new held-out cases; close two-reviewer ground-truth adjudication, scorer calibration, tokenizer/prompt/runtime checks, analysis-code review, and preregistration freeze. No model inference before the manifest explicitly permits it after all gates close.
3. **Ethics/permissions:** before collecting expert ratings or any human-subject data, determine and document applicable institutional/TÜBİTAK/MEB permission and consent requirements. Never assume permission is unnecessary.
4. **Student ownership:** the student must independently explain the question, conditions, code, source evidence, statistics, limitations, and conclusions; conduct a mock defense against the real report and show at least one source-backed regression case. Remove claims the student cannot substantiate.
5. **AI-use transparency:** preserve accurate records of generative-AI support. The final TYBS AI-use disclosure must identify the actual tools/versions and stages/scope used, in accordance with the current TÜBİTAK guide. The existing report draft mentions ChatGPT support for research planning, code/test drafts, automated checks, research documents and report language; this statement must be verified against actual usage and the applicant's understanding, not silently deleted to hide assistance.
6. **Report and submission freeze:** use the current official 2026–2027 template and the latest official rules; reconcile every in-text citation and reference; rerender and inspect the final PDF; verify title/abstract/keywords/pages and attachments; confirm ARBİS/TYBS fields and downloads; save the final approved application record.
7. **Only then do human-quality cleanup:** improve naming, formatting, comments, documentation clarity, duplicated boilerplate and unused files where justified by tests and review. Preserve license/copyright notices, source attribution, material provenance, required AI-use disclosure, test results, and historical commit/evidence records. Do not rewrite Git history, falsify authorship, backdate commits, or remove records to mislead a reviewer. Cleanup must not change scientific results or conceal meaningful external/AI contributions.

### Current no-go status
- V2 protocol remains draft; model inference is disabled; the new case pool is empty and required gates remain pending.
- Historical primary result remains Standard 0/80 vs CCDG 0/80; it is inconclusive and must not be described as proof of equivalence or no effect.
- Five Java regression candidates passed the currently run technical gate; the TLS 1.3 candidate remains blocked. Technical test success alone does not establish independent ground-truth validation.
- The compliance matrix is a checklist, not proof that student-specific eligibility, previous-submission, consent, or TYBS requirements have already been met.
