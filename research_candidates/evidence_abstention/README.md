# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Durum (20 Ekim 2026):** Aşama 1 — hedefli literatür ve ön özgünlük denetimi tamamlandı. Aşama 2 — kaynak fizibilitesi tamamlandı (koşullu); BugsInPy upstream'inde 17 projede 501 ham hata klasörü sayıldı, fakat doğrulanmış örneklem hazır değil. Aşama 3 — eşleştirilmiş deney tasarımı, iki prompt koşulu, JSON çıktı şeması ve analiz planı belgelendi. Bir BugsInPy-tqdm smoke koşusu CI'da buggy-fail/fixed-pass verdi; ancak metadata Python 3.6.9, smoke runtime Python 3.8.18 olduğundan bu tam ortam tekrarı ve kabul edilmiş vaka değildir. Karar: tasarım çalışması tamamlandı; uygulamaya/inference'a geçiş izni yok.

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
