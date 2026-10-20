# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Durum (20 Ekim 2026):** Aşama 1 tamamlandı (hedefli literatür / ön özgünlük denetimi); Aşama 2'nin kaynak fizibilitesi tamamlandı. Karar: koşullu devam. BugsInPy, ana aday havuz olarak seçildi (upstream denetiminde 17 projede 501 ham hata kaydı). Vaka düzeyindeki test tekrar üretilebilirliği, lisans uygunluğu ve kontaminasyon denetimi tamamlanmadı; dolayısıyla doğrulanmış deney kümesi henüz hazır değil. Model çıkarımı için izin verilmemiştir.

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

- **Aşama 1 — hedefli literatür ve ön özgünlük denetimi:** tamamlandı; karar koşullu devam. Genel abstention, kodda belirsizlik/kaçınma ve LLM fault localization üzerine yakın çalışmalar belgelendi. Özgünlük kesinleşmedi.
- **Aşama 2 — veri kaynağı fizibilitesi:** tamamlandı, koşullu geçiş. Upstream BugsInPy deposunda 17 projede 501 ham bug klasörü sayıldı. Örnek metadata yapısında buggy/fixed revizyonları, patch ve hedefli test betikleri bulundu. Bu sayı kabul koşullarından geçen vaka sayısı değildir; testler uçtan uca yürütülmedi.
- **Operasyonel vaka doğrulama kapısı:** açık. En az 30 bağımsız vaka ve en az 5 upstream proje hedefi, yalnızca test, kök neden, kanıt yeterliliği, lisans ve sızıntı kapıları geçildikten sonra sayılacak.
- **Sonraki adım:** Docker/CI ortamında biçim örneklerinden farklı birkaç vaka için buggy sürümde test-fail / fixed sürümde test-pass doğrulaması; sonrasında vaka seçimi ve puanlama protokolünü dondurma.
- **Model çıkarımı kapısı:** kapalı. Sistematik tam metin taraması, veri/test doğrulaması, puanlama ve analiz planı sonuçlar görülmeden tamamlanmadan inference yok.


## Belgeler

- `LITERATURE_REVIEW.md` — hedefli literatür taraması, yakın çalışmalar ve aşama 1 kararı.
- `PROTOCOL_DRAFT.md` — araştırma soruları, aday deney tasarımı, veri ve analiz planı.

Bu çalışma şu anda planlama aşamasındadır. Herhangi bir deney yürütüldüğü, insan puanlamasının tamamlandığı veya sonuç alındığı iddia edilmemektedir.
