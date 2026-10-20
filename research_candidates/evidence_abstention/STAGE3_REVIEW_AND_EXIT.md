# Aşama 3 kapanış denetimi — deney tasarımı

**Denetim tarihi:** 20 Ekim 2026  
**Karar:** **AŞAMA 3 TASARIM OLARAK TAMAMLANDI; deney yürütme izni verilmedi.**  
**Dal:** `research/evidence-abstention-draft-2026-10-19`

## 1. Kapanış kapsamı

Aşama 3'te araştırma sorusu, hipotezler, faktörler, eşleştirilmiş istemler, JSON çıktı sözleşmesi, birincil/ikincil ölçütler, örneklem hedefi, istatistiksel karşılaştırma ve inference öncesi kapılar belgelendi.

Bu kapanış **ön kayıt (preregistration), veri kümesi onayı veya model çalıştırma onayı değildir**. İstem ve analiz dosyaları v0.1 taslaklarıdır; model çıktısı alınmadan önce içerik hash'leriyle ayrıca dondurulmalıdır.

## 2. Tasarımın dondurulan kararları

- **Araştırma sorusu:** E3/yetersiz kanıtta seçici cevap/kaçınma politikasının (P1), zorunlu teşhise (P0) kıyasla kanıtla desteklenmeyen kesin kök neden teşhisi oranına etkisi.
- **Faktörler:** E1 yeterli / E2 kısmi / E3 yetersiz kanıt × P0 zorunlu teşhis / P1 seçici teşhis.
- **Birim:** Bir bağımsız, doğrulanmış upstream kusur/kök neden. Her vaka için altı hücre vardır; bunlar altı bağımsız vaka değildir.
- **Birincil sonlanım:** E3 altında vaka düzeyinde kanıtla desteklenmeyen kesin teşhis; P0 ve P1 eşleştirmesi.
- **İstatistik:** İki taraflı exact McNemar, risk farkı RD = P1 − P0 ve %95 güven aralığı. Upstream proje kümelenmesi ayrıca duyarlılık analiziyle raporlanır.
- **Örneklem:** Hedef 80 bağımsız vaka; doğrulayıcı alt sınır 60 vaka ve 8 ayrı upstream proje. N=60 altına veya 8 projenin altına düşen çalışma doğrulayıcı iddia olarak sunulmaz.
- **Çıktı sayısı:** Hedefte 80 × 3 × 2 = 480 ham çıktı; asgari eşikte 60 × 3 × 2 = 360 ham çıktı. Çıktı sayısı vaka sayısı değildir.
- **Model adayı:** Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4, revision `68c4276063d1496cdf13d0b8e8221f899bfa77f`; tek model sonuçları başka modellere genellenmez.
- **Çıkarım durumu:** Kapalı. Manifestte `case_ids=[]`, `inference_allowed=false`.

## 3. Denetim bulguları

1. `PROMPT_CONDITIONS.md` P0 ve P1 için ortak system/user şablonlarını tanımlar; politika metni dışında kasıtlı fark olmaması hedeflenmiştir.
2. `OUTPUT_SCHEMA.json` geçerli JSON metnidir; karar alanını `diagnose` / `abstain` ile sınırlar ve kaçınmada boş kök neden şartını tanımlar.
3. `EXPERIMENT_MANIFEST_STAGE3.json` geçerli JSON metnidir; 80 hedef vaka, 60 alt sınır, 8 proje, vaka başına altı hücre, 480 hedef çıktı ve kapalı inference değerlerini birbiriyle tutarlı kaydeder.
4. `ANALYSIS_PLAN_STAGE3.md` birincil sonlanımı, eşleştirilmiş testi, RD yönünü, geçersiz JSON duyarlılık analizini ve proje-kümeli duyarlılık yaklaşımını belirtir.
5. Güç duyarlılığı sayıları, yalnızca varsayımsal senaryolardır. Monte Carlo kontrolü yaklaşık olarak N=40/60/80 için 0.556/0.785/0.901; alternatif senaryoda N=80 için 0.634 güç verir. Bunlar gözlenmiş etki değildir, veri temelli güç garantisi değildir.
6. GitHub Actions run [39461858759](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759) başarılı bir **smoke** işidir: BugsInPy-tqdm-1 için buggy-fail/fixed-pass adımları başarılı olmuştur. Ancak runtime Python 3.8.18, metadata Python 3.6.9'dur ve vaka patch/metadata incelemesine maruz kalmıştır. Bu nedenle ana örneklemden kalıcı olarak dışlanır; kabul edilmiş doğrulayıcı vaka sayısı hâlâ **0**.
7. `PROTOCOL_DRAFT.md` içindeki önceki genel örneklem notu Aşama 3 kararlarının önüne geçmemelidir; örneklem ve analiz için `STAGE3_EXPERIMENT_DESIGN.md`, `ANALYSIS_PLAN_STAGE3.md` ve `EXPERIMENT_MANIFEST_STAGE3.json` güncel tasarım kaynaklarıdır.

## 4. Kapanış için gereken depo ayrımı

Araştırma alanı iki mantıksal bölüme ayrılmıştır:

- `USE_FOR_THIS_PROJECT/`: yeni projeye ait taslaklar ve kuralları geçen gelecekteki bağımsız vakalar. Bu klasördeki belgeler de inference izni değildir.
- `DO_NOT_USE_AS_EVIDENCE/`: eski DİJİTALİKİZ verileri, vakaları, puanları ve TÜBİTAK sonuçlarının yeni projede kullanılmasını yasaklayan manifest/politika.

Eski dosyalar fiziksel olarak taşınmadı veya silinmedi; geçmişin izlenebilirliğini, CI bağlantılarını ve eski TÜBİTAK teslim kayıtlarını korumak için kendi yollarında bırakıldı. Kapsam sınırının yetkili açıklaması `REPO_SCOPE_SPLIT.md`, makine tarafından okunabilir listeler ise iki klasördeki `MANIFEST.json` dosyalarıdır.

## 5. Aşama 3'ün dışındaki açık kapılar

Aşama 3'ün tasarım dokümantasyonu tamamlandı; şu işler sonraki veri doğrulama/ön kayıt/yürütme aşamasında kalır:

- En az 60 yeni, kabul edilmiş vaka ve en az 8 proje bulmak; hedef 80.
- Her vaka için kayıtlı ortamda buggy-fail/fixed-pass logları, lisans ve kök neden doğrulaması.
- E1/E2/E3 paketlerini bağımsız değerlendiricilerle doğrulama; iki değerlendiricili puanlama rubriği ve uyuşmazlık çözümünü dondurma.
- Prompt, schema, vaka paketleri, model/tokenizer/runtime, runner ve analiz dosyalarının SHA-256 hash'lerini üretip manifesti güncelleme.
- Daha geniş sistematik literatür taraması ve danışman/protokol incelemesi.
- Ayrı bir onay kapısı ile inference izni verilmesi. Bu rapor tek başına izin vermez.

## 6. Nihai sonuç

**Aşama 3: TAMAMLANDI — yalnızca deney tasarımı ve yöntem dokümantasyonu.**  
**Aşama 1:** hedefli literatür/ön özgünlük taraması tamamlandı; özgünlük kesinleşmedi ve sistematik derleme değildir.  
**Aşama 2:** kaynak fizibilitesi koşullu geçti; doğrulanmış veri kümesi hazır değildir.  
**Model inference:** KAPALI. Yeni proje için doğrulanmış deneysel sonuç yoktur.
