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

## 7. Doğrudan yakın çalışmalar: hedefli taramanın sonuçları

Aşağıdaki çalışmalar, genel abstention literatüründen yazılım mühendisliği alanına doğru kapsamı daraltmak amacıyla 20 Ekim 2026 tarihinde hedefli web taramasında bulundu. Kaynak sayfaları ve erişilebilir özetler incelendi; bu, tüm veri tabanlarında yürütülmüş sistematik bir derleme değildir.

| Çalışma | Görev ve yöntem | Bu projeye etkisi |
|---|---|---|
| Rathnasuriya & Yang (ICSE 2026 NIER), [When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions](https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-Defer-A-Decision-Framework-for-Reliable-Code-Predictions) | Kod modelleri için belirsizlik tahmini, kalibrasyon, seçici kaçınma ve belirsiz çıktılarda araçla doğrulamayı bir araya getiren çerçeve. | **En yakın kavramsal uyarılardan biri.** Kod alanında cevaplama/kaçınma ve doğrulama fikrini tek başına yeni diye sunamayız. Ancak odaklanan görev code prediction / sınıflandırma-üretim; bizim aday görevimiz hata teşhisi için sunulan kanıtın yeterliliği ve iddianın kanıtsal desteği. Bu görev farkı ancak tam yöntem karşılaştırmasıyla doğrulanabilir. |
| Zhou et al. (2026), [Task Abstention for Large Language Models in Code Generation](https://arxiv.org/abs/2605.17029) | Kod üretiminde görevden kaçınma; üretim tutarlılığını çalıştırma sonuçlarıyla ilişkilendiren kalibreli karar kuralı. | Kod üretiminde abstention için dağılımdan bağımsız garanti iddiası olan bir yaklaşım mevcuttur. Proje kod üretimi güvenilirliğini yeniden icat ettiğini iddia edemez. |
| Sharma & David (2025), [Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation](https://arxiv.org/abs/2502.11620) | LiveCodeBench üzerinde belirsizlik ölçülerini kod doğruluğuna bağlayıp yüksek belirsizlikte cevap vermemeyi değerlendirir. | Yalnızca belirsizlik tahmini veya yanlış kod yanıtlarını filtrelemek özgün katkı sayılmaz. |
| Rakasi et al. (2026), [When Uncertainty Isn't Enough: An Empirical Study of Self-Correction in Code Generation](https://arxiv.org/abs/2608.14659) | Kod üretiminde farklı belirsizlik sinyallerini ve belirsizliğe göre kendi kendini düzeltme politikalarını deneysel olarak karşılaştırır; sonuçlar kullanılan sinyale göre değişir. | Belirsizlik sinyalinin varlığı, daha iyi performansın otomatik kanıtı değildir. Biz de “kaçınma artarsa güvenilirlik kesin artar” varsayımı yapmamalıyız. |
| Xiao et al. (2025), [Large Language Models for Fault Localization: An Empirical Study](https://arxiv.org/abs/2510.20521) | HumanEval-Java ve Defects4J üzerinde ifade düzeyinde hata yerelleştirmesi; model, istem stratejisi, bağlam, doğruluk, tutarlılık ve maliyet değerlendirmesi. | Yazılım hatasını bulma performansı zaten benchmark'larla inceleniyor. Yalnızca LLM'leri arıza yerelleştirmesinde karşılaştırmak yeterli değil. |
| Wang et al. (2026), [Exploring the potential and limitations of large language models for novice program fault localization](https://www.sciencedirect.com/science/article/pii/S0164121225004005) | Codeflaws, Condefects ve BugT dâhil veri kümeleriyle farklı LLM'lerin acemi programcıların hata yerelleştirmesindeki performansını inceler. | Yayımlanmış hata yerelleştirme çalışmaları ve veri kaynakları mevcut; ayrıca yeni veri kümesi kurmanın gerekçesi açıklanmalı. Mevcut özet, bizim kanıt yeterliliği/abstention protokolümüzü değerlendirdiğini göstermiyor. |
| Wen et al. (TACL 2025), [Know Your Limits](https://aclanthology.org/2025.tacl-1.26/) | Genel abstention yöntemleri, benchmarklar ve ölçütleri üzerine derleme. | Genel yöntem düzeyinde katkı iddiasını sınırlar. |
| Zhang & Wu (2026), [Evidence Sufficiency Benchmark](https://www.techscience.com/cmc/v89n1/68467) | RAG'de beş düzeyli kanıt yeterliliği ve cevap/kaçınma kalibrasyonu. | Kontrollü kanıt seviyesi kullanımı tek başına özgün değildir. |
| Zhai et al. (Findings of ACL 2026), [Abstain-R1](https://aclanthology.org/2026.findings-acl.985/) | Cevaptan kaçınma ve kaçınma sonrası anlamlı açıklama/eksik bilgi belirtmeyi verifiye edilebilir pekiştirmeli öğrenmeyle ele alır. | Kaçınma sonrası gerekli bilgiyi belirtmek de genel düzeyde daha önce ele alınmıştır. |
| Madhusudhan et al. (COLING 2025), [Do LLMs Know When to NOT Answer?](https://aclanthology.org/2025.coling-main.627/) | Answerable/unanswerable sorular için Abstain-QA ve black-box abstention değerlendirmesi. | Genel cevaplanabilirlik/kaçınma değerlendirmesi mevcut. |

### Araştırma boşluğu hakkındaki güvenilir ifade

Hedefli tarama, şu bileşenlerin **ayrı ayrı** önceden araştırıldığını gösteriyor: (a) genel LLM abstention, (b) kanıt yeterliliği ve cevap/kaçınma kalibrasyonu, (c) kod üretiminde belirsizlik ve abstention, (d) LLM tabanlı yazılım hata yerelleştirmesi.

Bu taramada, **gerçek yazılım kusurlarında kontrollü kanıt yeterliliği seviyelerini; kök neden ground truth doğruluğu ile sunulan kanıta dayalı destek ölçüsünü ayırarak; uygun kaçınma ve yeterli kanıt varken gereksiz kaçınma maliyetiyle birlikte** değerlendiren tam eşleşmeli bir çalışma tespit edilmedi. Ancak bu ifade yalnızca hedefli tarama için geçerlidir. “Böyle bir çalışma yoktur” veya “ilk çalışma” sonucuna varılamaz; ACM/IEEE/Scopus benzeri indekslerde tam atıf ağı ve tam metin taraması yapılmamıştır.

## 8. Aşama 1 sonuç ve karar kapısı

**Durum: TAMAMLANDI — hedefli literatür taraması ve ön özgünlük denetimi.** Bu etiket, sistematik derlemenin tamamlandığı anlamına gelmez.

**Karar: KOŞULLU DEVAM (conditional go).**

Gerekçe:
1. Konu bilimsel olarak anlamlı; kanıtsız kesin teşhisin maliyetini incelemek yazılım mühendisliği bağlamında ölçülebilir bir sorudur.
2. Genel abstention, kodda belirsizlik/kaçınma ve hata yerelleştirmesi alanları zaten aktif araştırma konularıdır.
3. Aday farklılık, yalnızca “kaçınma politikasını denemek” değil; gerçek hata vakalarında kanıt yeterliliğini kontrollü değiştirmek ve **gerçek kök neden doğruluğu ile kanıtsal desteği ayrı ölçerek** hata azaltımı ile yanıt kapsamı arasındaki değiş tokuşu değerlendirmektir.
4. Bu farkın özgünlüğü henüz kesin değildir; başvuru metninde “ilk” veya “özgünlüğü kanıtlanmış” denmeyecektir.

### Aşama 2'ye geçiş kararı

Aşama 2'de model çalıştırılmayacak. Önce gerçek kusur vakalarının, pre-fix/fixed revizyonların ve yeniden üretilebilir testlerin toplanabilirliği küçük bir veri-fizibilite denetimiyle değerlendirilecek. Ayrıca tam metin/atıf zincirini de içeren daha geniş bir literatür taraması, inference öncesi zorunlu kontrol olarak kalacak.

**Inference durumu:** Kapalı. Sonuç, başarı, etki büyüklüğü veya finalistlik iddiası yoktur. DİJİTALİKİZ'in eski pilot/confirmatory sonuçları bu yeni araştırmaya aktarılmayacaktır.


## 9. Genişletilmiş hedefli literatür taraması — 21 Ekim 2026

Bu ek, ilk ön taramayı güncellemek için 21 Ekim 2026 tarihinde yayıncı/konferans sayfaları ve erişilebilir özetler üzerinden yapılan yeni aramaları kaydeder. Tarama sorguları; LLM abstention/answerability, evidence sufficiency, answer-or-defer in code predictions, task abstention in code generation ve LLM software fault localization terimlerini kapsadı.

### 9.1 Ek teyit edilen çalışmalar

| Çalışma | Kaynakta doğrulanan kapsam | Araştırma tasarımına etkisi |
|---|---|---|
| Wen et al. (2025), [Know Your Limits: A Survey of Abstention in Large Language Models](https://aclanthology.org/2025.tacl-1.26/) | TACL derlemesi; yöntemler, benchmarklar ve ölçütleri query/model/human-values çerçevesiyle sınıflandırıyor. | Genel cevap vermeme fikri veya ölçütleri yeni katkı olarak ileri sürülemez. |
| Madhusudhan et al. (COLING 2025), [Do LLMs Know When to NOT Answer?](https://aclanthology.org/2025.coling-main.627/) | Cevaplanabilir/cevaplanamaz sorular, Abstain-QA, black-box değerlendirme ve prompt stratejileri. | Yalnızca zorunlu yanıt ile kaçınma iznini karşılaştırmak yeterli özgünlük değildir. |
| Rathnasuriya & Yang (ICSE 2026 NIER), [When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions](https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-When-to-Defer-A-Decision-Framework-for-Reliable-Code-Predictions) | Kod tahminleri için ne zaman cevaplanacağı/ne zaman erteleneceği üzerine karar çerçevesi; ICSE 2026 NIER programında. | Yazılım/kod görevlerinde cevaplama–erteleme kararı yakın alandır. Görev farkı, yalnızca başlık benzerliğine değil tam yöntem ve ölçüt karşılaştırmasına dayanmalıdır. |
| Zhou et al. (2026), [Task Abstention for Large Language Models in Code Generation](https://arxiv.org/abs/2605.17029) | Kod üretiminde güvenilir olmayan görevlerden kaçınmak için kalibreli abstention kuralı ve kod çalıştırma tutarlılığı. | Kod alanında abstention ve hata azaltma konuları zaten doğrudan ele alınıyor; “yazılımda ilk” iddiası kurulamaz. |
| Zhai et al. (Findings of ACL 2026), [Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL](https://aclanthology.org/2026.findings-acl.985/) | Kaçınma kararının yanı sıra cevap verilemeyen sorularda neyin eksik olduğunu açıklamayı da optimize ediyor. | Eksik kanıt talebi tek başına yeni katkı değildir; bizim çalışmada bu talep bağımsız bir ayırt edicilik ölçütü olmalıdır. |
| Zhang & Wu (2026), [Do LLMs Know When Evidence is Insufficient?](https://www.techscience.com/cmc/v89n1/68467) | RAG için kanıt yeterliliği seviyeleriyle cevap/kaçınma kalibrasyonu benchmarkı. | Kanıt seviyelerini kademelendirmek genel olarak yeni değildir. |
| Xiao et al. (2025), [Large Language Models for Fault Localization: An Empirical Study](https://arxiv.org/abs/2510.20521) | HumanEval-Java ve Defects4J üzerinde LLM'lerin ifade düzeyinde hata yerelleştirme performansını ve istem etkilerini inceleyen ampirik çalışma. | Hata yerelleştirmesi için benchmark ve model karşılaştırması mevcut; yeni katkı kanıt yeterliliği ile iddia desteğini ayırmalıdır. |
| [Review of Large Language Model-Based Software Fault Localization Techniques](https://ieeexplore.ieee.org/document/11320391/) (IEEE DSA 2025; IEEE Xplore kaydı 12 Ocak 2026'da eklenmiş) | 21 LLM tabanlı fault-localization çalışmasını beş yaklaşım sınıfında derleyen inceleme. | Bu alan için geniş bir önceki çalışma haritası bulunduğundan, tam metin atıf takibi başvuru öncesi önemlidir. |

### 9.2 Bu taramadan çıkarılabilecek ve çıkarılamayacak sonuçlar

**Desteklenen sonuç:** Genel abstention, kanıt yeterliliği, kod üretiminde görevden kaçınma ve LLM tabanlı fault localization ayrı ayrı önceden araştırılmıştır. Bu nedenle araştırmamızın katkısı “model bazen cevap vermesin” veya “kanıtı azalttığımızda cevap oranı değişiyor mu?” şeklinde tanımlanamaz.

**Şimdilik savunulabilecek aday ayrım:** Gerçek kusurlar üzerinde aynı vaka için kanıt paketlerini önceden tanımlı biçimde E1/E2/E3 seviyelerine dönüştürmek; gerçek kök nedenle örtüşmeyi ve yalnızca paketin desteklediği teşhisi ayrı puanlamak; E3'te kanıtsız kesin teşhis oranını, E1'de gereksiz kaçınma ve yanıt kapsamıyla birlikte raporlamak.

**Kanıtlanmamış nokta:** Bu taramada tam olarak bu üç unsuru aynı deneyde birleştiren birebir eşleşen çalışma tespit edilmedi; ancak bu, böyle bir çalışma bulunmadığının kanıtı değildir. Tüm ACM/IEEE/Scopus kayıtlarının tam metinleri ve atıf ağları sistematik olarak incelenmiş değildir. Bu sebeple proje “ilk çalışma” veya “özgünlüğü kanıtlanmış” olarak tanımlanmayacaktır.

### 9.3 Aşama 1 için kapatma tanımı

**Hedefli literatür taraması ve ön özgünlük sentezi: tamamlandı (21 Ekim 2026).** Bu, sistematik derleme değildir. Kaynak başlığı/özeti veya erişilebilir yayın sayfasından daha ileri yöntem iddiası çıkarılmayacaktır. Preregistration ya da resmi yarışma raporundan önce, danışmanla tam metin ve atıf zinciri kontrolü hâlâ yapılmalıdır; bu sonraki kalite kapısı olarak korunur.



## 10. Yakın çalışmalarla karşılaştırma ve özgünlük sınırı — 21 Ekim 2026

Bu bölüm, proje katkısını daha dar ve savunulabilir biçimde tanımlar. Kaynak sayfaları ve erişilebilir özetler kontrol edilmiştir; tüm çalışmaların tam metni ve atıf ağları üzerinden sistematik tarama yapılmış değildir.

| Çalışma | Kaynaktan doğrulanabilen kapsam | Bizim tasarımla örtüşen taraf | Proje için sonuç |
|---|---|---|---|
| [Wen et al., *Know Your Limits* (TACL, 2025)](https://aclanthology.org/2025.tacl-1.26/) | LLM abstention yöntemleri, benchmark’ları ve ölçütlerini query/model/human-values bakışlarıyla sınıflayan derleme. | Kaçınma için genel kavramlar ve değerlendirme ölçütleri. | Genel “LLM cevap vermekten kaçınmalı” fikri özgünlük iddiası olamaz. |
| [Rathnasuriya & Yang, *When to Answer and When to Defer* (ICSE-NIER, 2026)](https://conf.researchr.org/details/icse-2026/icse-2026-nier/47/When-to-Answer-and-When-to-Defer-A-Decision-Framework-for-Reliable-Code-Predictions) ([arXiv ön baskısı](https://arxiv.org/abs/2605.19369)) | Kod modelleri için belirsizlik tahmini, kalibrasyon, seçici abstention ve kaçınılan örnekleri araçla ele almayı birleştiren çerçeve. | Alan doğrudan yazılım/kod ve answer-vs-defer davranışı. | Bu, en yakın yazılım mühendisliği çalışmasıdır. Proje yeni bir genel abstention çerçevesi veya kalibrasyon algoritması sunduğunu iddia etmemeli. Tasarımımızın ayırıcı sorusu, gerçek kusur kök neden teşhislerinde kontrollü kanıt eksiltme ile “gold root cause ile örtüşme” ve “modelin gördüğü kanıtın iddiayı desteklemesi” ölçümlerini ayrı tutmaktır. Bu farkın literatürde eşsiz olduğu henüz kanıtlanmış değildir. |
| [Zhou et al., *Task Abstention for Large Language Models in Code Generation* (arXiv, 16 Mayıs 2026)](https://arxiv.org/abs/2605.17029) | Kod üretiminde görevden kaçınma; birden çok hipotez sınamasına dayalı kalibre kural ve üretim tutarlılığını kod yürütme sonuçlarıyla değerlendirme. | Kod alanında abstention ve işlevsel yanlışlık riski. | Görevimiz kod üretmek değil; mevcut yazılım hatasına tanı koymak ve sunulan kanıtla tanının desteklenip desteklenmediğini değerlendirmektir. Yine de kod alanındaki abstention araştırması olduğu için doğrudan ilgili çalışma olarak atıflanmalı. |
| [Zhang & Wu, *Do LLMs Know When Evidence is Insufficient?* (Computers, Materials & Continua, 2026)](https://www.techscience.com/cmc/v89n1/68467) | RAG için beş kanıt yeterlilik seviyesi, yedi model/beş aile, üç istem stratejisi ve 200 örnekte insan doğrulaması; özet, çelişkili kanıtta yüksek over-answer oranları raporlar. | Kanıt yeterliliği gradyanı ve cevap vermeme ölçümü, yeni projemize çok yakındır. | “Kanıt seviyesini düşürüp abstention’ı ölçmek” tek başına özgün katkı değildir. Projemiz, retrieval/RAG sorularından farklı olarak gerçek hata düzeltme geçmişine dayalı yazılım kök neden vakalarında, gerçek kök neden doğruluğu ile sadece görülen kanıta dayalı destek ayrımına odaklanmalıdır. |
| [Madhusudhan et al., *Do LLMs Know When to NOT Answer?* (COLING 2025)](https://aclanthology.org/2025.coling-main.627/) | LLM’lerin cevap vermemesi gerektiği durumları tanıması konusunda abstention araştırması. | Genel abstention kararının güvenilirliği. | İlgili çalışma literatür karşılaştırmasında kalmalı; yalnızca başlık/özetinden daha ileri yöntem ayrıntısı varsayılmamalı. |
| [*Abstain-R1* (Findings of ACL, 2026)](https://aclanthology.org/2026.findings-acl.985/) | Abstention odaklı bir LLM yöntem çalışması. | Modelin gerektiğinde cevap vermemesi. | Bu çalışma yöntem/öğrenme yaklaşımı yönünden incelenmeli; proje şu an yeni model eğitimi veya RL algoritması önermiyor. |
| [Xiao et al., LLM tabanlı yazılım fault localization ampirik çalışması](https://arxiv.org/abs/2510.20521) ve [LLM-based software fault localization review (IEEE)](https://ieeexplore.ieee.org/document/11320391/) | Yazılım kusuru/hata yerelleştirmesinde LLM performansı ve önceki yöntemler. | Kusur teşhisi bağlamı, kök neden/konum tahmini. | Salt teşhis doğruluğu yerine kanıt desteği ve uygun kaçınma maliyetini ayrı ölçmek gerekir. Tam metin ve atıf karşılaştırması kapanış öncesi yapılmalı. |

### 10.1 Bu araştırmanın savunulabilecek katkı cümlesi

> “Bu çalışma, gerçek ve kaynak kodu/test/düzeltme geçmişiyle doğrulanmış yazılım hata vakalarında, aynı temel vaka için yeterli, kısmi ve yetersiz kanıt paketlerini karşılaştırır. Zorunlu teşhis ile seçici kaçınma politikalarını eşleştirerek, gizli gerçek kök nedenle örtüşmeyi ve yalnızca modelin gördüğü kanıtla desteklenmeyi ayrı puanlar; E3'te kanıtsız kesin teşhisleri ve E1'de gereksiz kaçınmayı birlikte ölçer.”

Bu cümle **aday katkı tanımıdır**, kanıtlanmış özgünlük beyanı değildir. Sonuçlar alınmadan önce başka bir çalışmanın bu tasarımın tüm ana unsurlarını zaten birleştirdiği bulunursa, farklılık açıkça yeniden değerlendirilmelidir. Yakın tam metinler ve referans zincirleri danışmanla kontrol edilmeden “ilk”, “benzersiz” veya “literatürde yapılmamış” ifadeleri kullanılmayacaktır.

### 10.2 Tasarım için zorunlu sınırlar

1. Yeni çalışmanın birincil sonucu bir modelin genel abstention kalitesi veya kod üretme başarısı değildir; E3 koşulunda desteklenmeyen kesin kök neden teşhisi oranındaki P0-P1 farkıdır.
2. Kök neden doğruluğu ile kanıtsal destek aynı etikette birleştirilmeyecektir. Model tesadüfen doğruyu tahmin etmiş olsa da kanıt paketi alternatiflerden ayrım yapmıyorsa bu destekli teşhis olarak puanlanamaz.
3. E1 gereksiz kaçınma, yanıt kapsamı ve eksik kanıt isteğinin ayırt ediciliği raporlanır; birincil sonuç yerine geçirilmez.
4. Tasarım modeli fine-tune etmeyi, yeni abstention algoritması önermeyi veya genel uncertainty calibration yöntemini ICSE 2026 çalışmasının yerine koymayı hedeflememektedir.
5. Mevcut tarama hedeflidir; sistematik derleme olarak sunulamaz. Nihai ön kayıt öncesi yakın yayınların tam metinleri, kaynakları ve atıf ağları izlenerek tekrar denetlenmelidir.
