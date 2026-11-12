# Güncel proje durumu ve yürütme planı

**Durum tarihi:** 12 Kasım 2026  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Hedef:** TÜBİTAK 2204-A 2027 için tamamlanmış, gerçek kanıta dayalı, yeniden üretilebilir ve jüri önünde savunulabilir araştırma. Finalistlik bir hedeftir; garanti değildir.

> Bu dosya, 21 ve 27 Ekim tarihli planlardaki aktif veri kaynağı ve operasyon takvimi bilgilerinin yerine geçen güncel durum kaydıdır. Eski dosyalar tarihsel karar/provenans olarak korunur; güncel vaka sayısı ve geçiş kapıları bu dosyadan okunmalıdır.

## 1. Genel değerlendirme

**Mühendislik ve süreç yönetimi bakımından ilerleme olumlu; araştırma bakımından henüz erken aşamadayız.**

Olumlu kanıtlar:
- Araştırma sorusu ve kontrollü P0/P1 karşılaştırması tanımlı.
- SWE-rebench V2 kaynağı için metadata-only fizibilite, ön eleme ve deterministik 96 projelik cohort üretimi tamamlandı.
- 96 ana aday, 17 proje yedeği ve 148 aynı proje içi alternatif ayrıldı. Bunlar kabul edilmiş vaka değildir.
- No-inference testleri tekrarlanabilir şekilde çalışıyor; son denetim commit'inde preflight ve evidence-packet testleri geçti.
- İlk sekiz kaydın seçili base commit noktalarındaki kök lisans dosyaları tek tek kontrol edildi ve Apache-2.0 olarak doğrulandı.

Açık bilimsel gerçek:
- **Kabul edilmiş bağımsız vaka: 0**
- **Kabul edilmiş upstream proje: 0**
- **Ana deney modeli çıktısı: 0**
- **Gold root-cause ve evidence-tier insan değerlendirme panelleri: tamamlanmadı**
- **Ön kayıt: tamamlanmadı**
- **Model/runtime doğrulaması: tamamlanmadı**
- Bu nedenle hipotezin desteklendiği, P1'in daha iyi olduğu veya halüsinasyonların azaldığı söylenemez.

## 2. Araştırma sorusu ve sabit deney mantığı

Birincil soru: **Yazılım hatası teşhisinde kanıtın yetersiz olduğu durumlarda cevap vermekten kaçınmaya izin veren politika, teşhis vermeyi zorunlu kılan politikaya kıyasla kanıtla desteklenmeyen kesin teşhis oranını düşürüyor mu?**

- **P0:** Model teşhis vermek zorunda.
- **P1:** Model, mevcut kanıt ayırt edici değilse teşhisten kaçınabilir ve hangi kanıtın eksik olduğunu belirtir.
- **E1:** Teşhisi alternatiflerden ayırmaya yeterli kanıt.
- **E2:** Kısmi/eksik ayırt edici kanıt.
- **E3:** Birden fazla makul kök nedenin hâlâ mümkün olduğu yetersiz kanıt.

Aynı temel model, tokenizer, decoding ayarları ve runtime iki politikada da korunmalıdır. Birincil sonuç E3 altında kanıtla desteklenmeyen kesin teşhis oranıdır. Kök neden doğruluğu, kanıtsal destek, kapsam/coverage ve E1'de gereksiz kaçınma ayrı ölçülür.

**Doğru tahmin, kanıtla destekli teşhis demek değildir.** Çalışma modelin öz farkındalığını kanıtlamaz; yalnızca sunulan kanıt altındaki karar politikasının etkisini ölçer.

Birincil karşılaştırmada model fine-tuning'i yapılmayacaktır. Eğitim, P0/P1 politika etkisini model ağırlığı değişikliğiyle karıştırır ve araştırma sorusunu bulandırır. Önceden eğitilmiş sabit model araştırma aracı olarak kullanılacaktır.

## 3. Veri kaynağı ve cohort — tamamlanan metadata aşaması

Kaynak adayı: PrimeIntellect/SWE-rebench-V2-Filtered-Verified.

- Sabitlenmiş filtered-train Parquet: 6.272 satır.
- Python alt kümesi: 1.952 satır.
- Qwen2.5 model çıkış tarihinden sonraki tarih filtresi sonrası: 349 satır.
- Gerekli metadata/tekrarlı kimlik kontrollerinden sonra: 347 aday / 154 repo.
- Ön lisans allowlist'i ve bilinen maruziyet dışlamaları sonrası: 261 aday / 113 repo.
- Deterministik örnekleme: 96 ana proje adayı, 17 proje yedeği, 148 aynı proje içi alternatif.

Sabit seçim tohumu ve kaynak dosyası/cohort manifest hash'leri önceki cohort seçimi PR'ında kayıtlıdır. Bu 96 kayıt yalnızca aday havuzudur; testlerin geçmesi, lisansın tamamlanması veya insan gold label onayı olmadan kabul edilmiş vaka sayılmaz.

Veri kartındaki CC BY 4.0 beyanı, upstream depolardaki kaynak kod lisanslarını otomatik olarak değiştirmez. Satırın upstream repo lisansı ayrıca denetlenir. Parquet içindeki created_at alanı string'dir; tarihi UTC kabul etme varsayımı ön kayıt öncesinde açıkça teyit edilmelidir.

Qwen2.5-3B-Instruct'ın yayımlanma tarihinden sonraki kayıtları seçmek, olası ezberleme/maruziyet riskini azaltmaya dönük bir önlemdir; sıfır kontaminasyon kanıtı değildir.

## 4. Şu anki aşama: kaynak lisansı, lineage, PR/issue kapsamı ve exposure denetimi

İlk 8 adayın sabit base commit'lerinde kök lisans dosyaları exact commit SHA üzerinden okundu; 8/8 Apache-2.0 metni. Recursive Git tree sorguları truncated=false döndürdü.

İlk 16 adayın GitHub PR'leri cohort metadata'sıyla eşleştirildi. **16/16 PR base SHA, cohort'taki base_commit ile birebir eşleşti.** Dolayısıyla seçilen commit ve upstream PR provenance bağı bu ilk 16 kayıtta doğrulandı; bu eşleşme tek başına vaka kabulü anlamına gelmez.

### Vaka tipi taraması

- **İlk 8 kayıtta 4 geçici bug adayı:** reagento/dishka, ecmwf/earthkit-data, wntrblm/nox, databricks/dbt-databricks.
- **İlk 8 kayıtta 4 dışlama:** aristanetworks/anta yalnızca test kodu değişikliği; python-tuf enhancement; python-bigquery feature request; Cloud SQL connector feature request.
- **9–16 kayıtlarında 4 geçici bug adayı:** getmoto/moto (çoklu ECR image tag'lerinin listelenmemesi), pyro-ppl/numpyro (AIES warmup sonrası MCMC.run hatası), OpenMDAO/dymos (add_control/set_control_options varsayılan değerlerinin uygulanmaması), CS-SI/eodag (provider config anahtarının çakışması).
- **9–16 kayıtlarında 4 dışlama:** D-Wave samplers için yeni close() API'si; FastMCP resource template optional arg desteği; kafka-python timeout_ms API parametreleri; PennyLane GroverOperator work_wires property.

İlk 16'da toplam **8 geçici bug adayı / 8 dışlanan kayıt** var. Bu küçük sıralı batch'in oranı tüm 96 adaya genellenemez. Adaylar, test yeterliliği ve buggy-fail/fixed-pass yeniden üretimi tamamlanmadığı için kabul edilmiş vaka değildir.

FastMCP için cohort'taki eski repo adı jlowin/fastmcp artık GitHub tarafından PrefectHQ/fastmcp deposuna yönlendiriliyor. PR #164'ün base SHA'sı cohort commit'iyle eşleşiyor; bu repo transferi/isim sahipliği değişimi olarak kaydedildi, commit uyuşmazlığı değil.

### Lisans ve lineage durumu

- İlk 8'in kök lisans metinleri Apache-2.0 olarak doğrulandı. ANTA NOTICE, python-tuf ek MIT lisansı ve earthkit-data ECMWF ek rezerv notu ayrıca kayıtlı.
- **9–16 kayıtlarının exact base commit lisansları henüz incelenmedi.** Metadata'daki Apache-2.0 alanı tek başına hukuki temizlik sayılmaz.
- Google ilişkili iki depo için bağımsızlıkta kurumsal kümeleme notu korunuyor.
- İlk 16 kayıt bilinen BugsInPy dört depo dışlama listesiyle ad eşleşmesi göstermiyor; bu, geniş model pretraining kontaminasyonunu dışlamaz.

Ayrıntılı raporlar:
- [İlk 8 kök lisans ve lineage denetimi](SWE_REBENCH_V2_FIRST8_SOURCE_LICENSE_LINEAGE_AUDIT_2026-11-12.md)
- [İlk 8 PR/issue kapsam denetimi](SWE_REBENCH_V2_FIRST8_CASE_SCOPE_AUDIT_2026-11-12.md)
- [9–16 PR/issue kapsam denetimi](SWE_REBENCH_V2_CASE_SCOPE_AUDIT_09_16_2026-11-12.md)

**Aşama 3 tamamlanmadı.** Cohort'un kalan kayıtları aynı sabit kuralla taranmalı; 9–16 lisans kontrolü de bekliyor. Kök lisans taraması, her vaka içindeki patch dosyaları, üçüncü taraf bileşenler, issue/PR metinleri ve test bağımlılıklarının tam kullanım değerlendirmesinin yerine geçmez. Kaynak/test kapısı hâlâ kapalıdır.

## 5. Son no-inference CI kapısı

Güncel PR #175 başındaki commit için [Evidence Abstention Preflight run #330](https://github.com/MahmutVezir/dijitalikiz/actions/runs/43265860360) başarılı tamamlandı.

- Preflight unit tests: 13/13 geçti.
- Evidence packet audit tests: 12/12 geçti.
- Readiness report: ready=false.
- Kabul edilmiş vaka/proje: 0/0.
- Açık engel: 21.
- model_inference_performed=false.

Bu CI sonucu, kapı denetimlerinin testlerini geçtiğini gösterir; deneyin hazır olduğunu göstermez. Başlıca engeller: dataset gate açık, doğrulanabilir ön kayıt yok, iki değerlendiricili rubrik/adjudication ve kalibrasyon dondurulmadı, exact model/tokenizer/runtime yükleme ön kontrolü geçmedi, zorunlu SHA-256 freeze kayıtları eksik, 60 vaka/8 proje eşiği karşılanmadı ve inference için açık yetki yok.

## 6. Aşamalı yol haritası

| Aşama | İş | Çıkış koşulu | Durum |
|---|---|---|---|
| 1 | Araştırma sorusu, literatür sınırı, P0/P1 × E1/E2/E3 protokolü | Önceden belirlenmiş ölçütler ve adil karşılaştırma | Taslak olarak hazır; sistematik literatür ve prereg tamamlanmalı |
| 2 | Kaynak veri metadata fizibilitesi ve cohort oluşturma | Sabit veri revizyonu, hash, kurallar ve deterministik seçim | Metadata aşaması tamamlandı |
| 3 | Kaynak lisansı, repo lineage, PR/issue tipi, exposure ve case-level provenance | Her aday için exact commit, dosya lisansı, issue tipi, notice, fork/upstream ve maruziyet incelemesi | Devam ediyor; ilk 16/96 PR eşleşti, 8/16 geçici bug adayı |
| 4 | Buggy/fixed teknik yeniden üretim | Exact environment; buggy hedef test başarısız, fixed aynı test başarılı; tüm log/hash'ler saklı | Başlamadı; lisans kapısına bağlı |
| 5 | Gold root-cause ve evidence-tier etiketleme | Model çıktısını görmeyen en az iki bağımsız inceleyici; uyuşmazlık/adjudication kaydı | Başlamadı |
| 6 | Protokolü kilitleme ve preregistration | Prompt, schema, model, tokenizer, runtime, rubrik, analiz ve vaka hash'leri; prereg URI | Başlamadı |
| 7 | Kontrollü model değerlendirmesi | Ayrı izin sonrası sabit modelde P0/P1 × E1/E2/E3; ham çıktılar saklı | Kapalı |
| 8 | İstatistik, hata analizi ve raporlama | Exact McNemar, risk farkı, %95 CI, coverage ve gereksiz kaçınma sonuçları; sınırlılıklar | Başlamadı |
| 9 | TÜBİTAK raporu ve jüri provası | Sonuçlarla tutarlı rapor, tekrar üretim eki, savunma | Başlamadı |

## 7. Örneklem ve analiz eşikleri

- Hedef: 80 bağımsız vaka.
- Doğrulayıcı alt sınır: 60 bağımsız vaka ve en az 8 gerçek upstream proje.
- Her vaka için E1/E2/E3 × P0/P1 = 6 çıktı; 80 vaka için 480 planlanan çıktı.
- Aynı repo ailesi, fork, tekrarlı issue veya aynı kök neden bağımsız proje/vaka sayısını yapay biçimde artırmamalı.
- 60 vaka/8 proje sağlanamazsa, protokol doğrulayıcı çalışma olarak sunulamaz; sonuç görüldükten sonra eşik düşürülmez.

## 8. Çalışma ritmi ve güvenlik kuralları

- Her kullanıcı mesajında tek, sınırları belli bir iş paketi yürütülür; azami çalışma bloğu 20 dakikadır.
- Her paketin sonunda değişen dosyalar, exact commit/PR/CI kanıtı, test durumu ve kalan engeller raporlanır.
- Kaynak lisansı temizlenmeden upstream testleri çalıştırılmaz.
- Dataset, case-level ground truth, evidence tier, insan değerlendirme, model/runtime, prompt, analiz ve ön kayıt kapıları kapanmadan model inference başlatılmaz.
- Ana deney için fine-tuning yapılmaz; P0/P1 karşılaştırmasında model ve runtime sabit tutulur.
- İnsan etik/onay gerekliliği, değerlendirici onamı ve veri kullanım sınırları yazılı olarak netleştirilir.
- Olumsuz veya sonuçsuz sonuçlar değiştirilmeden raporlanır.

**Bir sonraki tek iş paketi:** 9–16. adayların exact base commit'lerindeki kök lisans dosyalarını, LICENSE/NOTICE/COPYING eklerini ve fork/transfer lineage durumlarını kontrol etmek. Bu lisans kapısı kapanmadan upstream kaynak kodu veya testleri çalıştırılmayacak.
