# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tek aktif hedef:** 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde, tamamlanmış ve bilimsel olarak savunulabilir bir araştırma sunmak. Finalistlik garanti edilemez; ölçütümüz gerçek kanıt ve dürüst raporlamadır.

**Güncel bilimsel durum (21 Ekim 2026):** Proje tamamlanmadı. Aşama 1 hedefli literatür incelemesi düzeyinde tamamlandı; sistematik derleme değildir. Aşama 2 kaynak metadata envanteri koşullu tamamlandı, ancak kabul edilmiş bağımsız vaka sayısı 0’dır. Aşama 3 tasarım belgeleri hazır, fakat protokol ön kayıtlı/dondurulmuş değildir. Aşama 4 no-inference preflight teknik olarak test edildi, ancak `ready=false`; yeni araştırma için model çıkarımı yapılmadı.

**Tek yürütme planı:** [TÜBİTAK 2204-A ana planı](TUBITAK_2204A_MASTER_PLAN_2026-10-21.md). Resmî başvuru son tarihi 4 Ocak 2027, saat 17.30’dur; [TÜBİTAK 2204-A çağrısı](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi).

**Depo kullanımı:** Bu depo, yeni projenin planlama, sürüm kontrolü, doğrulama ve belgelendirme altyapısı olarak kullanılacaktır. Çalışma ayrı bir dalda yürütülür; DİJİTALİKİZ'in tarihsel TÜBİTAK 2204-A deneyleri, sonuçları, manifestleri ve raporu değiştirilmez.

## Resmî proje adı

**Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ**

## Çalışmanın kapsamı

Proje, gerçek yazılım hatalarının kök nedenini teşhis eden bir büyük dil modelinin kanıt yeterliliği değiştiğinde nasıl davrandığını inceleyecektir. Amaç, modelin yalnızca doğru cevabı bulup bulmadığını değil, cevabının gördüğü kanıtlarla desteklenip desteklenmediğini ve yetersiz kanıtta uygun biçimde cevap vermekten kaçınıp kaçınmadığını da ölçmektir.

### Temel araştırma sorusu

Kanıt yetersiz yazılım hata vakalarında, cevap vermekten kaçınmaya izin verilen bir politika, teşhis vermeyi zorunlu kılan politikaya kıyasla kanıtla desteklenmeyen kesin teşhisleri azaltır mı; bunun yanıt kapsamı ve yeterli kanıt bulunan vakalardaki gereksiz kaçınma üzerindeki maliyeti nedir?

### Taslak deney

- Her vaka için kaynak kodu, test ve düzeltme kayıtlarıyla doğrulanmış bir kök neden belirlenir.
- Kanıt paketleri önceden tanımlanmış yeterli, kısmi ve yetersiz seviyelere ayrılır.
- Aynı model ve aynı temel girdiyle, zorunlu teşhis ve seçici cevap/kaçınma politikaları karşılaştırılır.
- Teşhis doğruluğu, kanıtsal destek, yanıt kapsamı, seçici hata ve gereksiz kaçınma ayrı ölçülür.
- Vaka başına tekrarlar bağımsız vaka olarak sayılmaz.

## Bilimsel sınırlar

1. Genel LLM abstention alanında önceki çalışmalar vardır; projenin özgünlüğü kanıtlanmış değildir.
2. Yeni veri havuzu, DİJİTALİKİZ'in pilot, confirmatory, kalibrasyon ve önceden incelenmiş vakalarından bağımsız olmalıdır.
3. Sistematik literatür taraması, veri fizibilitesi, puanlama protokolü ve analiz planı tamamlanmadan model çıkarımı yapılmaz.
4. Sonuçlar ne olursa olsun değiştirilmeden raporlanır; sonuçlara bakarak hipotez veya birincil ölçüt değiştirilmez.
5. Bu proje, DİJİTALİKİZ'in önceki sonuçlarını yeniden etiketleyerek veya yeni proje sonucuymuş gibi kullanarak ilerlemeyecektir.

## Aşama durumu

- **Aşama 1 — literatür ve özgünlük:** hedefli ön tarama tamamlandı. Genel abstention ve kod alanında belirsizlik yönetimi zaten araştırılıyor; bu nedenle özgünlük kesin değil. Tam sistematik derleme yapılmış gibi sunulmayacak.
- **Aşama 2 — veri fizibilitesi:** kaynak-kümesi fizibilitesi tamamlandı (koşullu); BugsInPy upstream'inde 17 projede 501 ham hata klasörü sayıldı. Bu bir kabul edilmiş örneklem sayısı değildir. En az 60 kabul edilmiş vaka / 8 proje doğrulanmadı.
- **CI vaka smoke:** [PySnooper denemesi](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460135014) beklenen buggy-fail koşulunu sağlamadı. [tqdm'un ilk denemesi](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460540758) fixed tarafta başarısız oldu; import yolu düzeltilince [sonraki smoke](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759) buggy-fail/fixed-pass verdi. Runtime ile metadata Python sürümleri eşleşmediği ve vaka incelenmiş olduğu için hiçbir smoke vakası ana örnekleme alınmaz.
- **Aşama 3 — deney tasarımı:** tamamlandı belge olarak. Faktörler E1/E2/E3 kanıt seviyesi × P0 zorunlu teşhis/P1 seçici kaçınma politikası; her vaka için altı çıktı. Birincil sonuç E3 altındaki kanıtsız kesin teşhis oranı; eşleştirilmiş karşılaştırma exact McNemar testi, RD ve %95 CI. 80 vaka hedefi, en az 60 ve 8 proje doğrulayıcı alt sınırı.
- **Araştırma kapsamını ayırma:** [REPO_SCOPE_SPLIT.md](REPO_SCOPE_SPLIT.md) kapsam kuralıdır; [USE_FOR_THIS_PROJECT/MANIFEST.json](USE_FOR_THIS_PROJECT/MANIFEST.json) izin verilen materyalleri ve [DO_NOT_USE_AS_EVIDENCE/MANIFEST.json](DO_NOT_USE_AS_EVIDENCE/MANIFEST.json) yasaklanan tarihsel veri/sonuçları makine tarafından okunabilir biçimde listeler.
- **Model çıkarımı:** kapalı. Henüz LLM inference veya yeni projenin deneysel sonucu yoktur. Vaka-kabul kapıları, lisans, ground truth, kanıt yeterliliği, sızıntı incelemesi ve runtime/prompt/analiz hash'leri kilitlenmeden inference yapılmayacak.

## Belgeler

- `REPO_SCOPE_SPLIT.md` — repo kullanım kapsamı.
- `LITERATURE_REVIEW.md` — hedefli literatür taraması ve özgünlük sınırı.
- `DATA_FEASIBILITY.md` — kaynak-kümesi denetimi ve CI başarısızlıkları.
- `STAGE3_EXPERIMENT_DESIGN.md` — deney tasarımı.
- `PROMPT_CONDITIONS.md` — eşleştirilmiş prompt koşulları.
- `OUTPUT_SCHEMA.json` — yapılandırılmış çıktı şeması.
- `ANALYSIS_PLAN_STAGE3.md` — sonuçlardan önce tanımlanmış analiz planı.
- `EXPERIMENT_MANIFEST_STAGE3.json` — inference kapısı kapalı manifest.
- `STAGE3_REVIEW_AND_EXIT.md` — Aşama 3 tasarım kapanış denetimi ve kalan inference kapıları.
- `PROTOCOL_DRAFT.md` — protokol taslağı.
- `USE_FOR_THIS_PROJECT/` — yeni proje için kullanılabilir dokümantasyonun kopyaları ve izin manifesti.
- `DO_NOT_USE_AS_EVIDENCE/` — eski DİJİTALİKİZ verileri/sonuçları için dışlama politikası ve manifest.
- `USE_FOR_THIS_PROJECT/REUSE_RULES.md` — yeniden kullanım kuralları.

Bu çalışma şu anda planlama aşamasındadır. Herhangi bir deney yürütüldüğü, insan puanlamasının tamamlandığı veya sonuç alındığı iddia edilmemektedir.


## Aşama 4 — teknik hazırlık durumu (21 Ekim 2026)

- [Teknik hazırlık ve açık kapılar](STAGE4_TECHNICAL_READINESS_2026-10-21.md)
- [Boş vaka sicili](CASE_REGISTRY.json): bilerek boş; hiçbir vaka doğrulayıcı olarak kabul edilmedi.
- [Runtime adayı](RUNTIME_LOCK.json): resmi, kuantize edilmemiş Qwen2.5-3B-Instruct revizyonu aday olarak belgelendi; henüz yükleme doğrulaması yok.
- [İnsan puanlama rubriği ve adjudication taslağı](RUBRIC_AND_ADJUDICATION.md): iki bağımsız değerlendirici ve körleme kuralları taslaklandı; kalibrasyon/dondurma tamamlanmadı.
- `scripts/evidence_abstention_preflight.py` ve `tests/test_evidence_abstention_preflight.py`: yalnızca read-only kapı denetimi ve birim testleri; model çağırmaz.
- `.github/workflows/evidence-abstention-preflight.yml`: no-inference CI doğrulaması; inference veya dış veri indirmesi yok. [İlk doğrulama çalışması başarılı](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39615830978): üç birim test geçti; rapor 0 kabul edilmiş vaka ve 16 açık inference blokajı gösterdi.

**Geçiş kararı:** Teknik altyapı hazırlanıyor. Doğrulanmış vaka sayısı sıfır olduğu için Stage 4 pilot LLM çıkarımı başlatılmayacak. En az 60 vaka/8 proje, tüm vaka/kanıt/lisans/sızıntı kapıları, iki değerlendiricili kalibrasyon, model/tokenizer/runtime denetimi, dosya hash'leri ve denetlenebilir ön kayıt tamamlanmadan inference yasaktır. Bu bir başarısız deney sonucu değil, henüz deney yürütülmediği anlamına gelir.


## Aşama 2 — metadata envanterini otomatikleştirme

Aşama 2 envanter sonucu: [METADATA_INVENTORY_RESULT_2026-10-21.md](METADATA_INVENTORY_RESULT_2026-10-21.md). Sabitlenmiş BugsInPy revizyonunda 501 ham kayıt/17 proje, 500 temel metadata-kalifiye kayıt ve bir metadata sorunu bulundu; 0 test çifti doğrulandı, 0 vaka kabul edildi.


- scripts/inventory_bugsinpy_candidates.py sabitlenmiş BugsInPy revizyonundaki metadata kayıtlarını CSV'ye dönüştürür.
- tests/test_inventory_bugsinpy_candidates.py fail-closed ve metadata-only kurallarını sınar.
- .github/workflows/evidence-abstention-metadata-inventory.yml sadece pinned upstream metadata ağacını indirip envanter artifact'ı üretir; test yürütmez ve model çağırmaz.
- Envanter otomasyonu tek başına hiçbir vakayı kabul etmez. Operasyonel vaka doğrulama tamamlanana kadar accepted cases = 0 ve inference = false kalır.


**Yeni doğrulama notu:** Envanter CI'sı başarılı; fakat dışlanan tqdm smoke testinin yeniden çalıştırması [run 39618666531](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618666531) fixed test tarafında tekrar başarısız oldu. Tek önceki olumlu smoke çalışması tekrarlanabilir kanıt sayılmıyor. Aşama 2 hâlâ 0 kabul edilmiş vaka ve açık operasyonel doğrulama kapısında.


## Tek odak kararı

Bu çalışma için başka yarışma veya ayrı araştırma hattı yürütülmeyecek. Şu an yapılacak iş, vaka kabul kapısını gerçek kanıtlarla kapatmak ve başvuruya hazır tamamlanmış bir bilimsel çalışma üretmektir. 501 ham metadata kaydı, 500 temel metadata-kalifiye kayıt olarak kalır; bunların hiçbiri otomatik kabul edilmiş deney vakası değildir. En az 60 kabul edilmiş bağımsız vaka / 8 proje ve tüm yöntem kapıları sağlanana kadar model çıkarımı kapalı tutulur.
