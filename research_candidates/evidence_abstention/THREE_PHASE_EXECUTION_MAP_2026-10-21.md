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
- 495 metadata adayı için proje-dengeli manuel tarama kuyruğu üretildi; ilk triage partisi kabul edilmiş deney örneklemi değildir.
- Fail-closed readiness betiği ve birim testleri oluşturuldu. Son tamamlanmış kontroller `ready=false`, 0 kabul edilmiş vaka/proje ve açık bilimsel engelleri raporladı.
- Boş vaka sicili, iki panelin ayrılmasını zorunlu tutan kabul kuralları ve manuel vaka inceleme formu/rehberi oluşturuldu.
- Daha önce açılmış fizibilite/smoke vakaları kalıcı olarak doğrulayıcı örneklem dışına çıkarıldı.
- Yedi önce açılmamış aday üzerinde yalnızca teknik hedef-test sinyallerini toplamak için bir no-inference iş akışı hazırlandı. Bu adaylar iş akışını doğrulama amacıyla kullanıldığından sonuç ne olursa olsun doğrulayıcı örnekleme girmeyecek.
- İlk biten Black-2 artefaktında Python 3.8.3 eşleşti, fakat buggy taraftaki hata eksik `tests/data/fmtonoff4.py` fixture'ından kaynaklandı; bu geçerli reprodüksiyon sayılmadı. Workflow açıkça listelenmiş fixture'ları buggy çalışma ağacına kopyalayacak şekilde düzeltildi.
- FastAPI-1 ve Scrapy-1 için buggy tarafta hedefe özgü görünen hata, fixed tarafta geçiş çıktı; iç artifact checksum listeleri doğrulandı. Bunlar da workflow-debug vakası oldukları için kalıcı dışlamada; insan root-cause/lisans/kanıt incelemesi yapılmadı.

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
