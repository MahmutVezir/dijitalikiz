# Aşama 3 — Deney tasarımı ve önceden belirlenmiş analiz

**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Sürüm:** 0.1 — tasarım dondurma taslağı  
**Tarih:** 20 Ekim 2026  
**Durum:** Tasarım belgelendi; veri doğrulama kapısı ve model çıkarımı kapalı. Bu dosya yayımlanmış bir preregistration kaydı değildir.

## 1. Araştırma sorusu

Gerçek açık kaynak yazılım kusurlarında, cevap vermekten kaçınmaya izin veren bir talimat; teşhis vermeyi zorunlu kılan talimata kıyasla, kanıtla desteklenmeyen kesin kök neden teşhislerini azaltıyor mu? Bu azalmanın bedeli, özellikle kanıtın yeterli olduğu vakalardaki teşhis kapsamı ve gereksiz kaçınma üzerinde nedir?

Bu çalışma “daha çok kaçınma = daha güvenilir model” varsayımını yapmaz. Güvenilirlik ve cevap kapsamı birlikte raporlanır.

## 2. Hipotezler

- **H1 — Birincil:** E3 (yetersiz kanıt) altında, seçici cevap/kaçınma politikası P1, zorunlu teşhis politikası P0'a göre kanıtla desteklenmeyen kesin teşhis oranını azaltır.
- **H2 — İkincil:** P1'in E3'te teşhis kapsamını düşürmesi beklenebilir; kapsam ile seçici risk birlikte raporlanır.
- **H3 — İkincil:** E1 (yeterli kanıt) altında P1'in gereksiz kaçınması ölçülür. Veriler bunu desteklemeden “doğru teşhisleri korur” denmez.
- **H4 — Keşifsel:** P1'in istediği eksik kanıtın, bağımsız değerlendiricilerin kök nedenleri ayırt etmek için gerekli gördüğü kanıtla uyumu incelenir.

Hipotezler çıktı görülmeden değiştirilmez. Gerekli değişiklik olursa mevcut analiz “sonradan yapılan” olarak işaretlenir ve yeni bir bağımsız doğrulayıcı çalışma planlanır.

## 3. Faktöriyel, eşleştirilmiş tasarım

Her bağımsız yazılım hatası için aynı kök neden ve ortak bağlamdan üç kanıt paketi hazırlanır; her paket iki politika talimatıyla test edilir.

| Faktör | Seviye | Operasyonel tanım |
|---|---|---|
| Kanıt seviyesi | E1 — yeterli | Kök nedeni makul alternatiflerden ayırmak için yeterli ayırt edici kanıt mevcut. |
| Kanıt seviyesi | E2 — kısmi | Yararlı bağlam mevcut ancak en az iki makul kök neden henüz ayırt edilemiyor; E1'den önceden tanımlı bir kanıt öğesi çıkarılmış. |
| Kanıt seviyesi | E3 — yetersiz | Paket birden fazla makul kök nedeni ayırt edemiyor. Gerekli kanıtın eksik olduğu, model çıktıları görülmeden bağımsız değerlendiricilerce doğrulanmış. |
| Politika | P0 — zorunlu teşhis | Modelden tek bir en olası kök neden belirtmesi istenir; cevap vermekten kaçınmaması açıkça söylenir. |
| Politika | P1 — seçici teşhis | Yalnızca paket teşhisi yeterince destekliyorsa cevap vermesi; aksi durumda açıkça kaçınması ve hangi ayırt edici kanıtın eksik olduğunu belirtmesi istenir. |

Her vaka başına 3 × 2 = 6 çıktı üretilir. Aynı hatanın üç kanıt seviyesindeki çıktıları bağımsız vaka sayılmaz. Tasarımda tekrarlı örnekleme kullanılmaz; ana çalışmada her hücre için tek, sabit ayarlı greedy çıktı alınır.

## 4. Vaka seçimi ve örneklem

- **Birincil kaynak:** BugsInPy; denetimde kullanılan upstream commit: 11c5f1eea954a42132cfd06bf257766a7963e0fd.
- **Hedef örneklem:** 80 bağımsız kök neden vakası.
- **Asgari doğrulayıcı hedef:** 60 kabul edilmiş vaka ve en az 8 ayrı upstream proje. N=40–59 elde edilirse sonuçlar sınırlı güçle raporlanır; N<60 veya 8 proje altı durumda çalışma keşifsel/fizibilite çalışması olarak adlandırılır, güçlü doğrulayıcı iddia kurulmaz.
- Proje başına hedef örneklem payı %20'yi aşmamalıdır. Aynı kök neden/PR/bug ailesi, kopya varyantlar ve önceki incelemeye maruz kalmış vakalar dışlanır.
- Her vaka için açık lisans/kaynak, buggy/fixed commit, hedefli test, hata kök nedeni ve kanıt yeterliliği insan değerlendirmesiyle doğrulanmalıdır.
- Dört metadata/patch format örneği (BugsInPy-black-1, BugsInPy-tqdm-1, BugsInPy-httpie-1, BugsInPy-youtube-dl-1) ile PySnooper-1 CI smoke örneği, ana veri kümesinde kalıcı olarak dışlanır.
- Model eğitim verisinde kamuya açık hata ve düzeltmelerin bulunmadığı kesin kanıtlanamaz; kontaminasyon riski sınırlılık olarak kaydedilir.

## 5. Model ve üretim ayarları

Önceden bilinen açık checkpoint, tekrar üretilebilir tek-model değerlendirmesi için aday birincil model olarak sabitlenir:

- Model: Qwen/Qwen2.5-3B-Instruct
- Revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
- do_sample=false, temperature=0.0, max_new_tokens=512
- Harici arama, retrieval, kod çalıştırma veya araç çağrısı yoktur.
- Tokenizer ve chat template model revision'ıyla birlikte pinlenir; Transformers ve ilgili runtime sürümleri, donanım bilgisi ve model dosyalarının hash'leri inference öncesi manifestte dondurulur.
- Her istek ayrı, geçmiş mesaj içermeyen bir oturumda yürütülür. Bir vaka/politika çıktısı başka isteğe bağlam olarak verilmez.
- Aynı JSON şeması her iki politika için kullanılır. Otomatik düzeltme, yeniden istem veya schema hatası sonrası sessiz tekrar yapılmaz; geçersiz çıktı ayrıca raporlanır.

Bu seçim tek model için sonuç çıkarır; diğer modellere genelleme yapılmaz. Sonradan ikinci model eklenirse keşifsel replikasyon olarak ayrılır.

## 6. Çıktı puanlama ve körleme

İki bağımsız değerlendirici kullanılır. Puanlama paketi mümkün olduğunca politika etiketi, model bilgisi ve çıktı sırasına körlenir. Yanıt içeriği bazen politikayı ele verebileceği için körlemenin kusursuz olduğu iddia edilmez.

Kök neden ground truth'u ayrı bir panelce, tam kaynak/test/fix kanıtı kullanılarak doğrulanır. Kanıtsal destek, modelin gördüğü kanıt paketi üzerinden ayrı puanlanır; sonradan görülen düzeltme yaması modele sunulmayan kanıt olarak değerlendirmeye sızdırılmaz.

Her çıktı için:
1. Karar: teşhis / kaçınma / geçersiz çıktı.
2. Kök neden doğruluğu: doğru / kısmen doğru / yanlış / puanlanamaz.
3. Kanıtsal destek: paketçe destekli / paketin desteklemediği kesin iddia / paketle çelişkili / puanlanamaz.
4. Gerekçe kanıt referansları: paketteki öğe ID'leriyle uyumlu / uyumsuz.
5. Eksik kanıt isteği: ayırt edici / kısmen yararlı / ilgisiz / uygulanamaz.

Anlaşmazlıklar, koşullar açılmadan önce belirlenmiş çözüm protokolüne göre ele alınır. Ham bağımsız puanlar, uzlaşılmış puanlar ve kategorik uyum (uygun olduğunda Cohen's kappa ve güven aralığı) saklanır. Tek bir LLM hakem veya anahtar kelime eşleştirmesi ground truth değildir.

## 7. Birincil sonuç ve istatistik

**Birincil sonuç:** E3 altında, bir vakanın çıktısının mevcut kanıtın desteklemediği veya onunla çelişen kesin kök neden iddiası üretip üretmediği (ikili, vaka düzeyinde sonuç).

- P0 ve P1 aynı E3 paketine ait eşleştirilmiş vaka sonuçları üzerinden karşılaştırılır.
- Etki yönü RD = risk(P1) − risk(P0) olarak raporlanır; negatif değer P1 lehine daha düşük kanıtsız kesin teşhis oranıdır.
- Eşleştirilmiş ikili sonlanım için iki taraflı exact McNemar testi, risk farkı ve %95 güven aralığı raporlanır. Kaynak projeler içindeki kümelenme göz ardı edilmez; proje-kümeli duyarlılık analizi ayrıca raporlanır. Proje sayısı yetersizse kümeli belirsizlik tahmininin sınırlı olduğu açıkça belirtilir.
- Aynı vakaya ait E1/E2/E3 ve P0/P1 çıktıları ayrı bağımsız gözlemler gibi sayılmaz.
- İkincil sonuçlar: E1 gereksiz kaçınma oranı, E1 doğru/kanıt destekli teşhis oranı, her seviyede yanıt kapsamı, E2/E3 kanıtsız kesin teşhis oranı, cevaplanan vakalardaki seçici hata ve eksik kanıt isteği niteliği.
- Çoklu ikincil sonuçlar keşifsel olarak etiketlenir; yalnızca anlamlı görünen alt gruplar raporlanmaz.

### Örneklem gücü duyarlılığı

Örneklem hedefini gerekçelendirmek için exact McNemar testinin senaryo tabanlı duyarlılığı hesaplandı. Varsayımlar veri gözlemi değil, tasarım senaryosudur: vaka başına politika çiftlerinin %30'unda sonuçlar farklılaşsın ve farklılaşan çiftlerin %83'ünde fark P1 lehine olsun. Bu, beklenen mutlak risk farkı yaklaşık 0,198 iken, iki taraflı α=0,05 için yaklaşık güç N=40'ta %56, N=60'ta %79, N=80'de %90'dır. Fark daha küçükse güç belirgin biçimde düşer; örneğin %15 puan risk farkı senaryosunda N=80 gücü yaklaşık %63'tür. Bu nedenle 80 hedefi anlamlı bir etki senaryosuna dayanır, küçük etkileri dışlamak için garanti değildir.

## 8. Veri bütünlüğü, sızıntı ve tekrar üretilebilirlik

- Her vaka için kaynak URL, lisans, upstream commit kimlikleri, test komutu, buggy/fixed logları ve SHA-256 hash'leri kaydedilir.
- Model girdisine fixed patch, çözüm commit'i, issue/PR kimliği, etiket/başlık üzerinden doğrudan çözüm ipuçları veya gold root-cause metni konmaz.
- E1/E2/E3 varyantları model çıktıları görülmeden üretilir ve hash'lenir. Yalnızca önceden tanımlı kanıt öğeleri değiştirilir; sahte hata/kanıt üretilmez.
- İsteklerin yürütme sırası sabit seed ile karıştırılır; her koşulun ham prompt'u ve çıktısı saklanır.
- Geçersiz ve eksik çıktılar silinmez; önceden belirlenen kurallara göre raporlanır.
- Analiz betiği, birincil sonlanım, eşleştirme kuralı ve dışlama listesi ilk model çıktısı alınmadan önce hash ile dondurulur.

## 9. Kilit ve geçiş kapısı

Bu tasarım, Aşama 3'ün yöntem dokümanı olarak tamamlanmıştır. Ancak model çıkarımı için onay değildir. Inference öncesinde aşağıdaki kapılar birlikte geçmelidir:
1. en az 60 kabul edilmiş vaka, hedef 80 ve en az 8 proje; her vaka buggy fail / fixed pass loguyla doğrulanmış;
2. her vaka için lisans, ground truth, kanıt yeterliliği ve leakage review tamamlanmış;
3. iki değerlendiricinin puanlama yönergesi ve anlaşmazlık çözümü dondurulmuş;
4. model/tokenizer/runtime uyumluluğu doğrulanmış, model revision ve tüm manifest hash'leri kilitlenmiş;
5. promptlar, output schema ve analiz planı sonuçlar görülmeden dondurulmuş;
6. proje/dataset ayrımının REPO_SCOPE_SPLIT.md ile uyumlu olduğu denetlenmiş.

**Aşama 3 sonucu:** Deney tasarımı yazılı ve kararları açık; veri ve runtime kapıları kapalı olduğu için çalışma henüz yürütmeye hazır değil. Hiçbir deney sonucu elde edilmiş gibi raporlanamaz.


## 10. 21 Ekim 2026 ön-çıkarım model adayı düzeltmesi

Daha önce yazılmış GPTQ-Int4 adayının yerine resmi, kuantize edilmemiş [Qwen/Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) checkpoint'inin `aa8e72537993ba99e69dfaafa59ed015b17504d1` revizyonu, FP16 ve quantization yok ayarlarıyla **yalnızca aday** olarak kaydedildi. Depodaki tarihsel README, önceki GPTQ yüklemesinde başlatılmış parametreler ve geçersiz örnekleme olasılıkları görüldüğünü belirtir. Bu nedenle eski tercihi yeni çalışmaya doğrulanmış kabul ederek taşımadık.

Bu düzeltme önceden çıktı üretilmeden yapılan bir yöntem kaydıdır; exact model/tokenizer yüklemesi, lisans incelemesi, runtime fingerprint ve dosya hash'leri henüz doğrulanmamıştır. Bu dosya bir ön kayıt değildir ve inference izni vermez. Yetkili güncel runtime adayı `RUNTIME_LOCK.json` ve manifestteki kayıttır.
