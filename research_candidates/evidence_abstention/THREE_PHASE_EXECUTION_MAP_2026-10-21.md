# Üç ana aşamalı yürütme haritası — 21 Ekim 2026

**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Tek hedef:** TÜBİTAK 2204-A 2027 için tamamlanmış, doğrulanabilir ve bilimsel olarak savunulabilir bir çalışma hazırlamak.  
**Durum:** Ana Aşama 1 üzerinde çalışılıyor. Yeni araştırma için LLM inference yapılmadı.

Bu belge önceki teknik aşamaları üç ana teslimata birleştirir. Bir dosyanın, bir CI koşusunun veya test otomasyonunun tamamlanması bilimsel projenin tamamlandığı anlamına gelmez.

## Aşama 1 — Veri, protokol ve çalıştırma kapılarını kapat

**Mevcut aşama. Henüz tamamlanmadı.**

### Tamamlanan hazırlık parçaları
- Hedefli literatür taraması ve aday katkı tanımı yazıldı; bu sistematik derleme veya özgünlüğün kanıtı değildir.
- Sabit BugsInPy revizyonu `11c5f1eea954a42132cfd06bf257766a7963e0fd` üzerinde metadata envanteri oluşturuldu: 501 ham kayıt / 17 proje; 500 kayıt asgari alan kapısını geçti, 1 kayıtta buggy ve fixed commit kimlikleri aynı.
- Güncellenmiş, dışlamalarla uzlaştırılmış kuyrukta 487 metadata adayı / 17 proje var; B1 = 78, B2+ = 409. Beş önceki maruziyet ve sekiz workflow-debug vakası kalıcı dışlandı. İlk triage partisi kabul edilmiş deney örneklemi değildir.
- Fail-closed readiness betiği ve birim testleri oluşturuldu. Son tamamlanmış kontroller `ready=false`, 0 kabul edilmiş vaka/proje ve açık bilimsel engelleri raporladı.
- Boş vaka sicili, iki panelin ayrılmasını zorunlu tutan kabul kuralları ve manuel vaka inceleme formu/rehberi oluşturuldu.
- Daha önce açılmış fizibilite/smoke vakaları kalıcı olarak doğrulayıcı örneklem dışına çıkarıldı.
- Yedi önce açılmamış aday üzerinde yalnızca teknik hedef-test sinyallerini toplamak için bir no-inference iş akışı hazırlandı. Bu adaylar iş akışını doğrulama amacıyla kullanıldığından sonuç ne olursa olsun doğrulayıcı örnekleme girmeyecek.
- İlk biten Black-2 artefaktında Python 3.8.3 eşleşti, fakat buggy taraftaki hata eksik `tests/data/fmtonoff4.py` fixture'ından kaynaklandı; bu geçerli reprodüksiyon sayılmadı. Workflow açıkça listelenmiş fixture'ları buggy çalışma ağacına kopyalayacak şekilde düzeltildi.
- FastAPI-1 ve Scrapy-1 için buggy tarafta hedefe özgü görünen hata, fixed tarafta geçiş çıktı; iç artifact checksum listeleri doğrulandı. Bunlar da workflow-debug vakası oldukları için kalıcı dışlamada; insan root-cause/lisans/kanıt incelemesi yapılmadı.

### Dondurulmuş başlangıç tarama sırası

[İlk 120 adaylık metadata-only cohort](SCREENING_COHORT_120_2026-10-21.json), güncel 487 adaylı kuyrukta kalıcı dışlamalardan sonra ilk 120 sıra numarasını korur. Bu, vaka kabulü veya doğrulayıcı örneklem değildir. Her adayın neden geçtiği/kaldığı kayda alınır; yedekler 121. sıradan aynı sırayla kullanılır, sonuçlara göre seçim yapılmaz.

### Kapatma kapısı
Aşağıdakilerin hepsi gerçek kayıt ve bağımsız kanıtla tamamlanmadan Aşama 1 kapanmaz:

1. **En az 60 kabul edilmiş bağımsız vaka ve en az 8 upstream proje**; hedef 80. Aynı hata ailesi/PR/kök neden kopyaları bağımsız sayılmaz.
2. Her vaka için metadata Python sürümüyle aynı runtime; aynı hedef test buggy sürümde hedef kusuru göstermeli ve fixed çalışma ağacında geçmeli. Ortam/kurulum hatası bug reproduksiyonu değildir.
3. Her vaka için uygun lisans/provenance, kaynak ve patch incelenmesi, kök neden ground truth'u, önceki maruziyet ve bilgi sızıntısı denetimi.
4. E1/E2/E3 kanıt paketleri model çıktıları görülmeden hazırlanmalı, iki bağımsız kanıt yeterliliği puanlayıcısı tarafından onaylanmalı ve hash'lenmeli.
5. Ground-truth paneli en az iki bağımsız inceleyiciden oluşmalı; kanıt yeterliliği panelinin kimlikleri bu panelle kesişmemeli. Rubrik kalibrasyonu, uyuşmazlık ve adjudication protokolü dondurulmalı.
6. Qwen/Qwen2.5-3B-Instruct aday modelinin exact revision, tokenizer/chat template, lisans, kütüphaneler, GPU/precision ve runtime fingerprint'i fiilen doğrulanmalı.
7. Prompt, şema, analiz planı, tasarım, rubrik, runtime ve kabul edilmiş vaka listesi için doğru SHA-256 değerleri hesaplanıp dondurulmalı; protokol model çıktılarından önce denetlenebilir biçimde ön kayda alınmalı.
8. Read-only preflight `ready=true` vermeli ve ayrıca açık, ayrı inference izni verilmeli. Preflight tek başına izin değildir.

**Şu anki kararı:** Aşama 1 açık. Kabul edilmiş vaka sayısı sıfır olduğundan inference çalıştırmak yasak/erken olur. Otomatik triage adayları kabul etmez.

## Aşama 2 — Dondurulmuş deneyin yürütülmesi

**Başlamadı; Aşama 1 kapanmadan başlamayacak.**

- Sabit tek model ve runtime ile, her kabul edilen vaka üzerinde E1/E2/E3 × P0/P1 tasarımında altı çıktı alınır.
- N=60 için 360, N=80 için 480 model çıktısı planlanır. Bunlar henüz gerçek çıktı değildir.
- Her ham çıktı, istek sırası, prompt/kanıt hash'i, model/tokenizer revision, runtime fingerprint ve schema sonucu ile saklanır.
- Otomatik tekrar üretme, JSON'u düzeltme, çıktı seçerek saklama veya sonuçlara göre prompt/hipotez değiştirme yapılmaz.
- Hatalar ve eksik çıktılar görünür şekilde kaydedilir; kod/ortam sorunu vaka dışlama kararı olarak sonradan saklanmaz.

## Aşama 3 — Kör puanlama, istatistik, rapor ve başvuru

**Başlamadı; gerçek deney verisi gerektirir.**

- Koşul etiketlerini olabildiğince gizleyerek bağımsız puanlayıcılarla kök neden doğruluğu, kanıtsal destek, karar/kaçınma ve eksik kanıt talepleri puanlanır.
- İlk bağımsız puanlar korunur; anlaşmazlıklar dondurulmuş adjudication protokolüyle çözülür. Ham anlaşma ve Cohen kappa / uygun olduğunda ağırlıklı kappa raporlanır.
- Birincil sonuç E3 altında vaka başına kanıtsız kesin teşhis oranının P0/P1 eşleştirilmiş farkıdır. İki yönlü exact McNemar, P1−P0 risk farkı ve %95 güven aralığı önceden planlandığı gibi raporlanır.
- İkincil sonuçlar ana hipotezin yerine geçirilmez; sıfır fark ve olumsuz sonuçlar da saklanır. Proje kümelenmesi/sınırlı proje sayısı raporda açıkça belirtilir.
- Resmî TÜBİTAK rapor şablonu ve güncel başvuru kontrolü tamamlanır. İç hedef 4 Kasım 2026'dır; resmî başvuru kapanışı **4 Ocak 2027, 17.30**. Devam eden/fikir aşamasındaki çalışma tamamlanmış proje gibi sunulmaz.

## Bu aşamada yürütülen teknik yardımcı hat

Güncel ilk-dalga iş akışı: [GitHub Actions run 39638198482](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39638198482). Bu hat sadece daha önce görülmemiş adayları teknik olarak yoklar. Onun yeşil olması bilimsel kabul, kök neden onayı veya model deneyi anlamına gelmez.

Metadata envanteri ve triage-artifact testleri: [run 39639138266](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39639138266). Bu CI yalnızca araçları/artefakt doğrulama kodunu sınar; BugsInPy test çiftlerini bu iş akışında çalıştırmaz.

## Ana dosyalar
- [Ana yürütme planı](TUBITAK_2204A_MASTER_PLAN_2026-10-21.md)
- [Manuel vaka inceleme rehberi](CASE_REVIEW_GUIDE.md)
- [Manuel vaka inceleme formu](CASE_REVIEW_INTAKE_TEMPLATE.json)
- [Literatür ve özgünlük denetimi](LITERATURE_REVIEW.md)
- [Veri fizibilitesi](DATA_FEASIBILITY.md)
- [Teknik readiness](STAGE4_TECHNICAL_READINESS_2026-10-21.md)
- [Jüri ölçütleri kontrol listesi](TUBITAK_2204A_JURY_CRITERIA_CHECKLIST_2026-10-21.md)


## Güncel CI ve analiz yardımcıları — 21 Ekim 2026

**Analiz kodu:** `scripts/analyze_evidence_abstention_results.py` ve `ANALYSIS_RUNBOOK.md` eklendi. Bu araç, ancak manifestin inference izni açıkça verilmiş, veri kapısı CLOSED, ön kayıt URI'si doğrulanabilir, iki değerlendiricili protokol ve kalibrasyon tamam, model/runtime doğrulanmış ve hash'ler dondurulmuşsa sonuç analizi yapabilir. CSV her kabul edilmiş vaka için tam altı nihai/adjudike hücre içermelidir. İçerik sentetik testlerle sınanmıştır; gerçek araştırma sonucu değildir.

**Yeni kohort testinin ilk CI bulgusu:** [run 39647103338](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39647103338) ilk sekiz seçimin dondurulmuş matrisini başarıyla yeniden oluşturdu; ancak vaka ortamı kurulumunda upstream BugsInPy aracı `~/.bashrc` bulunmadığı için durdu. Bu, bug/fix test çifti sonucu değildir. Runner hazırlığına boş `~/.bashrc` oluşturma adımı eklendi; bunu izleyen koşunun geçmesi beklenmeden hiçbir vaka kabul edilmeyecek.

**Bilimsel durum değişmedi:** Kabul edilmiş vaka 0; gerçek model çıkarımı 0; ön kayıt ve insan puanlaması henüz tamam değil.


## Sonraki denetim güncellemesi — 21 Ekim 2026

Yeni tamamlanan [ilk-dalga no-inference koşusu](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39644280706) yedi teknik tarama işinin tamamını ve artefakt hash denetimlerini başarıyla bitirdi. Sonuçlar [FIRST_WAVE_TRIAGE_RESULTS_2026-10-21.md](FIRST_WAVE_TRIAGE_RESULTS_2026-10-21.md) dosyasına kaydedildi.

Bu daha yeni koşuda:
- Black-2, Scrapy-1 ve Tornado-1 için otomatik denetimde hedef bug-reprodüksiyonuyla uyumlu ham buggy-fail/fixed-pass sinyali görüldü; insan incelemesi hâlâ zorunlu.
- FastAPI-1 ve Sanic-1 için benzer ham sinyal olsa da otomatik artefakt denetimi buggy günlüklerinde ortam/bağımlılık riski uyarısı verdi. Bunlar hedef kusurun kanıtı sayılmıyor.
- Luigi-1 ve TheFuck-1 için eksiksiz buggy-fail/fixed-pass çifti işareti oluşmadı; ortam/bağımlılık uyarıları mevcut.
- Bu yedi kayıt workflow geliştirme/teknik triage amacıyla incelendiği için doğrulayıcı analizden kalıcı dışlanmıştır. Önceki beş maruziyet vakasıyla birlikte kuyruğun dışında kalırlar.

**Aşama durumu değişmedi:** Doğrulayıcı vaka sayısı 0; doğrulanmış proje sayısı 0; LLM çıkarımı yapılmadı; analiz istatistiği hesaplanmadı. Koşunun başarı sonucu yalnızca otomasyon ve artefakt kontrollerini gösterir. Ana Aşama 1, en az 60 vaka/8 proje, iki ayrı insan değerlendirici paneli, kanıt paketleri, kaynak/lisans/sızıntı incelemesi, kesin runtime doğrulaması, hash dondurma ve denetlenebilir ön kayıt kapıları tamamlanana kadar açık kalır.


## Batch v2 runner finding and V3 queue decision — 21 October 2026

The V2 cohort freeze passed in [run 39659544932](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39659544932), but technical-screen output is not accepted: the inspected PySnooper-2 artifact shows `pytest: command not found` on both sides, and the spaCy-1 artifact never reached test execution. The fail-closed audit is therefore retained. A pinned `pytest==6.2.5` bootstrap is now in the workflow, and [V4 intake](SCREENING_COHORT_120_V4_2026-10-21.json) skips 24 IDs exposed across previous runner-debug batches. The intake remains 120 candidates / 17 projects and 0 accepted cases. The next completed CI run and all raw artifacts require inspection; inference stays off.


The V3 run also revealed that a strict metadata parser rejected a valid fixed-commit line with whitespace before the equals sign; the parser has been corrected. V4 is the current 120-candidate intake, skipping 24 exposed IDs. Accepted cases remain zero until CI artifacts and the scientific/human validation gates are complete; model inference remains disabled.


## V5/V6 technical findings and V7 intake

Run [39663084349](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39663084349) screened the V5 first-eight batch: seven cases showed automated buggy-fail/fixed-pass signals and Httpie-4 failed on both sides. All eight were permanently excluded because the batch was used to validate the workflow.

The V6 run [39664581005](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39664581005) exposed a second runner defect: the over-escaped pytest detector did not bootstrap pytest for Matplotlib-3, and both test logs reported "pytest: command not found". This is an environment/harness issue, not an upstream bug result. All eight V6 first-batch candidates are now permanently excluded because their results were inspected while debugging the detector. Details and the ZIP hash are in [the V6 defect audit](STAGE2_V6_RUNNER_DEFECT_AND_V7_HANDOFF_2026-10-21.md).

The detector has been moved to a unit-tested helper, and the workflow runs its regression tests before the case matrix. The active [V7 intake](SCREENING_COHORT_120_V7_2026-10-21.json) skips 48 exposed/debug IDs and takes the next 120 candidates in deterministic queue order. The new CI run must validate the detector and all raw artifacts before any case is considered for human scientific review.

**Scientific status remains:** accepted cases 0; accepted upstream projects 0; model inference 0. Stage 1 still requires systematic search archiving, independent advisor review and preregistration. Stage 2 still requires at least 60 accepted independent cases across at least 8 projects, licensing/provenance, two independent ground-truth reviewers, a separate two-person evidence-sufficiency panel, E1/E2/E3 packets and leakage/exposure checks.
