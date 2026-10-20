# Literatür taraması ve özgünlük denetimi — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tarama tarihi:** 20 Ekim 2026  
**Durum:** Hedefli ön tarama; sistematik derleme değildir. Kaynakların başlık/özet ve erişilebilir yayın sayfaları incelenmiştir; tüm çalışmaların tam metin yöntem karşılaştırması henüz tamamlanmamıştır.

## 1. Ön karar

**Genel abstention veya kanıt yetersizliğinde cevap vermeme yeni bir fikir değildir.** 2025–2026 literatüründe genel abstention benchmarkları, kanıt yeterliliği seviyeleri, cevap verilebilirlik kalibrasyonu, cevap vermeme sonrası açıklama/clarification ve kod üretiminde abstention incelenmiştir. Bu yüzden projemiz “yapay zekâya cevap vermemeyi öğretmek” ya da “kanıtı azaltıp cevap oranını ölçmek” şeklinde sunulmamalıdır.

**Araştırılmaya değer olası katkı (henüz doğrulanmadı):** gerçek açık kaynak yazılım kusurlarında kök neden teşhisini kaynak kod, test ve kabul edilmiş düzeltme ile doğrulamak; aynı vakalarda teşhis doğruluğu ile teşhisin sunulan kanıtça desteklenmesini ayrı puanlamak; kanıt yeterliliğini kontrollü ve körlenmiş biçimde değiştirirken uygun kaçınmayı ve yeterli kanıt varken gereksiz kaçınmayı birlikte değerlendirmek.

Bu bir *aday araştırma boşluğu* olup “ilk çalışma”, “benzersiz yöntem” veya “özgünlüğü kanıtlandı” iddiası değildir. Tam metin ve atıf ağı taraması bunu desteklemeden böyle bir iddia kullanılmayacaktır.

## 2. Yakın çalışmaların karşılaştırma matrisi

| Çalışma | Kapsam / katkı | Projemiz için anlamı | Farklılık iddiası ne gerektirir? |
|---|---|---|---|
| Wen et al. (2025), *Know Your Limits: A Survey of Abstention in Large Language Models*, TACL | Abstention yöntemleri, benchmarklar ve ölçütler üzerine kapsamlı derleme. https://aclanthology.org/2025.tacl-1.26/ | Genel abstention zaten yerleşik bir araştırma alanı. | Alanın tamamından ziyade dar görev ve doğrulama protokolü üzerinden katkı tanımlanmalı. |
| Madhusudhan et al. (2025), *Do LLMs Know When to NOT Answer?*, COLING | Abstain-QA ve answerable/unanswerable sorularda black-box değerlendirme; farklı prompt stratejileri. https://aclanthology.org/2025.coling-main.627/ | Sadece cevap ver/kaçın karşılaştırması ve prompt karşılaştırması yeterli yenilik değildir. | Yazılım kök neden teşhisi, doğrulanmış kusur kanıtları ve vaka düzeyinde puanlama farkı gösterilmeli. |
| Zhang & Wu (2026), *Do LLMs Know When Evidence is Insufficient?*, Computers, Materials & Continua | RAG için tam, kısmi, ilgisiz, eksik ve çelişkili kanıt seviyeleri; cevap/kaçınma kalibrasyonu. https://www.techscience.com/cmc/v89n1/68467 | Kontrollü kanıt yeterliliği seviyeleri tek başına yeni değildir. | Yazılım hata teşhisinde kanıt türleri, kök neden ground truth'u ve kanıtsal destek puanlamasının gerçekten farklı olup olmadığı sınanmalı. |
| Zhai et al. (2026), *Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL*, Findings of ACL | Kaçınma ve kaçınma sonrası eksik bilgi açıklamasını optimize eder. https://aclanthology.org/2026.findings-acl.985/ | “Model neyin eksik olduğunu söylesin” fikri de genel düzeyde yeni değildir. | Ek kanıt isteminin yazılım hatası için hangi ayırt edici kanıtı istediği, bağımsız bir ölçütle puanlanmalı; ana katkı diye varsayılmamalı. |
| Zhou et al. (2026), *Task Abstention for Large Language Models in Code Generation* | Kod üretiminde görevden kaçınmayı, üretim tutarlılığı ve risk kontrolüyle ele alır. https://arxiv.org/abs/2605.17029 | Yazılım/kod alanında abstention araştırması mevcut; “yazılım alanında ilk” denemez. | Kod üretimi ile mevcut projemizin kök neden teşhisi görevi arasındaki fark ve önceki debugging/fault-localization çalışmaları ayrıca incelenmeli. |
| Sharma & David (2025), *Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation* | Kod üretiminde belirsizlik tahminini doğruluk göstergesi ve abstention politikası için kullanır. https://arxiv.org/abs/2502.11620 | Belirsizliği kullanarak hatalı çıktıları filtreleme genel fikri biliniyor. | Çalışmamız belirsizlik tahmin yöntemini değil, kontrollü kanıt yeterliliği ve kanıtla desteklenen kök neden teşhisini izole etmeli. |
| Torun et al. (2026), *Evaluation of LLM-Based Software Engineering Tools: Practices, Challenges, and Future Directions* | Yazılım mühendisliği araçlarını değerlendirme, ground truth ve tekrarlanabilirlik zorlukları. https://arxiv.org/abs/2604.24621 | Veri sızıntısı, değerlendirici güvenilirliği ve tekrar üretilebilirlik tasarımın parçası olmalı. | Vaka seçimi, gold truth doğrulaması ve kör değerlendirme açık protokolle belgelenmeli. |

## 3. Geçici araştırma sorusu

**RQ:** Gerçek açık kaynak yazılım kusurlarında, yalnızca teşhis üretmeye yönlendiren bir talimat ile kanıt yetersiz olduğunda kaçınmaya açıkça izin veren bir talimat arasında; kanıtsız kesin kök neden teşhisi, kanıtla desteklenen doğru teşhis ve yeterli kanıt koşulundaki gereksiz kaçınma açısından ne fark vardır?

Bu soru, “kaçınma daha fazla olursa sistem daha güvenilir olur” varsayımını yapmaz. Başarı; yalnızca kaçınma oranını artırmak değildir. Model E1 yeterli kanıt koşulunda doğru teşhisleri korumalı, E2 kısmi kanıt ve E3 yetersiz/çelişkili kanıt koşullarında ise iddialarını kanıtla orantılı tutmalıdır.

### Geçici deneysel ayrım
- **P0 — Zorunlu teşhis:** Modelden kök neden teşhisi istenir; kaçınma davranışı için özel izin verilmez.
- **P1 — Kanıt-kalibreli politika:** Modelden kanıt yeterliyse teşhis, değilse açıkça kaçınma ve gerekirse eksik kanıtı belirtmesi istenir.
- Her iki koşulda vaka metni, kanıt, model sürümü, örnekleme ayarları ve diğer talimatlar eşleştirilmelidir. Tek farkın politika talimatı olduğu doğrulanmalıdır.
- **E1:** kök nedeni ayırt etmek için yeterli kanıt; **E2:** kısmi/ayırt etmeye yetmeyen kanıt; **E3:** yetersiz veya kontrollü çelişkili kanıt. Etiketler önceden tanımlanmalı ve bağımsız değerlendiricilerce doğrulanmalıdır.
- Aynı vakanın varyantları arasında cevabı doğrudan ele veren metinler veya düzeltme/commit sızıntısı bulunmamalıdır.

## 4. Ölçütler — ön tanım

1. **Birincil:** E3 koşulunda kanıtla desteklenmeyen kesin teşhis oranı; P0 ile P1 arasındaki fark vaka düzeyinde karşılaştırılacak.
2. **Doğru teşhis:** Kök nedenin doğrulanmış ground truth ile uyuşması.
3. **Kanıtsal destek:** Teşhis iddiasının sunulan kanıt tarafından gerçekten desteklenmesi. Doğru tahmin edilmiş olması tek başına yeterli sayılmamalı.
4. **Coverage / cevaplama oranı:** Modelin kaç vakada teşhis sunduğu.
5. **Selective risk:** Cevap verilen vakalardaki hata oranı; coverage ile birlikte raporlanmalı.
6. **E1 gereksiz kaçınma oranı:** Kanıt yeterliyken modelin teşhis vermemesi.
7. **Eksik kanıtı belirleme kalitesi (ikincil/keşifsel):** Modelin istediği ek kanıtın kök nedenleri ayırt etmek açısından yararlı olup olmadığı.

Sadece cevaplama oranı veya yalnızca modelin kendi bildirdiği güven puanı yeterli başarı ölçütü değildir. Birincil ölçüt ve analiz planı sonuçlar görülmeden sabitlenmelidir.

## 5. Veri ve değerlendirme gereklilikleri

- Gerçek açık kaynak yazılım kusurları; issue, kaynak kod, test ve kabul edilmiş düzeltme gibi izlenebilir kayıtlarla seçilmeli.
- Gold root cause, evidence sufficiency ve model çıktısının puanlaması birbirinden ayrılmalı.
- Vaka havuzu, eski DİJİTALİKİZ pilot/confirmatory/calibration vakalarından ve sonuçlarından bağımsız olmalı; eski sonuçlar yeni projenin sonucu olarak kullanılmamalı.
- En az iki bağımsız değerlendirici, mümkün olduğunca koşul/model etiketlerine körlenmiş şekilde puanlamalı; anlaşmazlık çözüm prosedürü ve değerlendiriciler arası uyum raporlanmalı.
- Veri sızıntısı, lisans, vaka bağımsızlığı, prompt eşitliği, model sürümü ve tekrar üretilebilirlik denetlenmeli.
- Örneklem büyüklüğü fizibilite ve güç/duyarlılık gerekçesiyle belirlenmeli; mevcut taslakta kesin örneklem sayısı veya inference izni yoktur.

## 6. Sistematik tarama için sonraki aramalar

İlk hedefli aramadan sonra şu kümeler ayrı ayrı taranmalıdır:
- ("bug localization" OR "fault localization" OR "root cause diagnosis") AND (abstention OR "selective prediction" OR answerability)
- ("software debugging" OR "bug diagnosis") AND ("insufficient evidence" OR uncertainty OR calibration)
- ("LLM" AND software engineering) AND ("selective risk" OR "risk-coverage" OR abstention)
- ("evidence sufficiency" OR "evidence ablation") AND ("software engineering" OR debugging OR "fault localization")
- (software defect diagnosis OR bug report) AND (confidence calibration OR abstain OR refusal)
- ("program repair" OR "bug localization") AND (uncertainty OR abstention OR answerability)

Öncelikli kaynaklar: ACL Anthology, arXiv, ACM Digital Library, IEEE Xplore, Springer ve ilgili çalışmaların atıf ağları. Her kayıt için arama tarihi, sorgu, yayın türü, görev, veri, model, kanıt müdahalesi, abstention politikası, değerlendirme birimi, ölçütler ve sınırlılıklar kaydedilmeli. Tam metne erişilemeyen çalışma “tam metin incelendi” olarak işaretlenmemeli.

## 7. Aşama 1 karar kapısı

**Şimdiki karar: DEVAM ET — ancak özgünlük iddiası koşullu.**

Gerekçe: Genel abstention ve kanıt yeterliliği çalışmaları mevcut; fakat mevcut hedefli tarama, gerçek yazılım kök neden teşhisinde bu tam deney tasarımının önceki çalışmalarla aynı olup olmadığını kesinleştirmiyor. Konuyu terk etmek için erken, özgün kabul etmek için de erken.

Aşama 2'ye geçmeden önce:
1. Bug localization / fault localization / debugging ile abstention kesişimindeki doğrudan yakın çalışmaların taranması;
2. Bu çalışmalar için tam metin karşılaştırma tablosu;
3. Vaka kaynağı ve gold root cause fizibilitesinin kanıtlanması;
4. Ana hipotez, birincil ölçüt ve örneklem planının dondurulması gerekir.

**Deney durumu:** Henüz model inference yapılmadı; sonuç veya başarı iddiası yoktur. Bu belge bir ön literatür denetimidir, sistematik derleme değildir.
