# Literatür taraması: LLM cevaptan kaçınma ve yazılım hata teşhisi

**Tarama tarihi:** 19 Ekim 2026  
**Tarama kapsamı:** İlk kapsamlı tarama; ACL Anthology, arXiv, hakemli dergi sayfaları ve genel akademik web indeksleri. Bu henüz sistematik literatür taraması değildir. Arama dizgileri, dahil etme/dışlama kayıtları ve tam metin elemesi ayrı bir aşamada hazırlanmalıdır.

## 1. Ana bulgu

Cevaptan kaçınma (abstention), seçici tahmin, kanıt yeterliliği ve LLM güven kalibrasyonu zaten etkin araştırma konularıdır. 2025–2026 tarihli çalışmalar, cevaplanabilir/cevaplanamaz soruları ayırma, kanıt azaldığında kaçınma, kaçınma sonrasında eksik bilgiyi açıklama ve kod üretiminde başarısız olabilecek görevleri reddetme konularını doğrudan incelemektedir.

Bu nedenle bu proje “LLM'ler bazen halüsinasyon yapıyor” veya “LLM'lere bilmiyorum demeyi öğretmek” gibi geniş bir iddia üzerine kurulmamalıdır.

## 2. En yakın ilgili çalışmalar

### 2.1. Genel abstention araştırmalarının haritası

**Wen, B. ve diğerleri (2025). “Know Your Limits: A Survey of Abstention in Large Language Models.” Transactions of the Association for Computational Linguistics, 13, 529–556.**

Bağlantı: https://aclanthology.org/2025.tacl-1.26/  
DOI: https://doi.org/10.1162/tacl_a_00754

Bu derleme, abstention yöntemlerini, benchmarkları ve ölçütleri sorgu, model ve insan değerleri gibi boyutlardan ele alır. Ayrıca alan/bağlam özelinde abstention becerilerinin araştırılmasını gelecekteki çalışma alanları arasında tartışır.

**Projeye etkisi:** Genel abstention fikri yeni değildir. Yazılım hata teşhisine özgü iddia ancak kapsamlı arama ve doğrudan ilişkili çalışmaların karşılaştırılmasından sonra kurulabilir.

### 2.2. Cevaplanabilir ve cevaplanamaz sorular üzerinde benchmark

**Madhusudhan, N. ve diğerleri (COLING 2025). “Do LLMs Know When to NOT Answer? Investigating Abstention Abilities of Large Language Models.”**

Bağlantı: https://aclanthology.org/2025.coling-main.627/  
Ön baskı: https://arxiv.org/abs/2407.16221

Çalışma, Abstain-QA veri kümesini ve cevaplanabilir/cevaplanamaz soru koşulları için bir değerlendirme çerçevesini tanıtır; katı istem, sözlü güven eşiği ve zincirleme düşünme istemi gibi stratejileri inceler.

**Projeye etkisi:** Yalnızca bir “cevap ver / cevap verme” ikili testi tekrarlamak yeterli değildir. Yazılım hata teşhisinin özgün kanıt yapısı ve kaynak-kod temelli doğruluk değerlendirmesi tasarımın merkezinde olmalıdır.

### 2.3. Kanıt yeterliliği düzeylerine göre cevap/kaçınma

**Zhang, H. ve Wu, W. (2026). “Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention Calibration in Retrieval-Augmented Generation.” Computers, Materials & Continua, 89(1), makale 69.**

Bağlantı: https://www.techscience.com/cmc/v89n1/68467  
DOI: https://doi.org/10.32604/cmc.2026.086343

Bu çalışma, tam destek, kısmi destek, ilgisiz, bulunmayan ve çelişkili kanıtı kapsayan beş seviyeli bir benchmark ile yedi modeli ve üç istem stratejisini inceler. Çelişkili kanıt koşulunda yüksek cevap verme/over-answer oranları bildirir; 200 örnekte insan doğrulaması da sunar.

**Projeye etkisi:** “Kanıtı azaltıp modelin kaçınmasını ölçmek” genel düzeyde bu çalışmayla ciddi ölçüde örtüşür. Özgünlük iddiası ancak görev farkından, gerçek hata kayıtlarının kaynak-revizyon doğrulamasından ve doğruluk ile kanıt desteğinin ayrı değerlendirilmesinden doğabilir. Bu farkın yeni ve yeterince anlamlı olup olmadığı ayrıca değerlendirilmelidir.

### 2.4. Cevaptan kaçınma sonrasında eksik bilgiyi açıklama

**Zhai, H., Liang, J. ve Kang, D. (Findings of ACL 2026). “Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL.”**

Bağlantı: https://aclanthology.org/2026.findings-acl.985/

Bu çalışma, cevaplanamaz sorgularda kaçınmayı ve kaçınma sonrasında hangi bilginin eksik olduğuna ilişkin açıklamayı ortak biçimde ele alır; bunu doğrulanabilir ödül sinyalleriyle eğitilen bir model üzerinden inceler.

**Projeye etkisi:** “Model, hangi kanıtın eksik olduğunu söyleyebilir mi?” tek başına yeni bir katkı değildir. Biz bunu yazılım hatası için önceden listelenmiş kanıt birimleriyle, kaynak-kod ve test kayıtlarıyla karşılaştırarak ölçebiliriz; bu yalnızca aday bir uygulama farkıdır.

### 2.5. Kod üretiminde görevden kaçınma

**Zhou, Y. ve diğerleri (2026). “Task Abstention for Large Language Models in Code Generation.”**

Bağlantı: https://arxiv.org/abs/2605.17029

CodeRefuser yaklaşımı, kod üretim görevinde bir modelin başarılı cevap üretme olasılığı düşük olduğunda görevi reddetmesini, örnekler arası tutarlılığı ve yürütme/test sonuçlarını kullanan bir kalibrasyon süreciyle ele alır. Yazarlar risk kontrolü ve çoklu hipotez testi temelli bir yaklaşım sunar.

**Projeye etkisi:** Yazılım alanında abstention çalışması zaten vardır. O çalışma kod üretimi üzerine odaklanırken bu aday proje gerçek bir kusurun kök nedenini teşhis etmeyi ele alacaktır. Bunun yeterli özgünlük sağlayıp sağlamadığı tam metin karşılaştırmasıyla doğrulanmalıdır.

### 2.6. Kod üretiminde belirsizlik ve doğruluk

**Sharma, A. ve David, C. (2025). “Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation.”**

Bağlantı: https://arxiv.org/abs/2502.11620

Çalışma, kod üretiminin doğruluğunu öngörmek için belirsizlik ölçülerini inceler ve yüksek belirsizlikli durumlarda cevap vermekten kaçınmayı da değerlendirir.

**Projeye etkisi:** Tekrar üretimler arası anlaşmazlık veya güven sinyaliyle cevapları filtrelemek, kendi başına yeni yöntem iddiası olarak sunulmamalıdır. Bu adayda temel katkı, kanıt düzeyleri ile gerçek hata kök nedeninin kaynak doğrulamasını aynı protokolde birleştirmek olabilir.

### 2.7. Yazılım mühendisliğinde LLM değerlendirmesinin sorunları

**Torun, U. B. ve diğerleri (2026). “Evaluation of LLM-Based Software Engineering Tools: Practices, Challenges, and Future Directions.”**

Bağlantı: https://arxiv.org/abs/2604.24621

Bu değerlendirme çalışması; açık uçlu çıktılar, tek ve değişmez bir ground truth bulmanın zorluğu, model çıktılarının değişkenliği ve değerlendirme yöntemlerinin güvenilirliği gibi yazılım mühendisliğine özgü konuları tartışır.

**Projeye etkisi:** Salt otomatik anahtar kelime eşleştirmesi veya tek bir LLM-as-a-judge puanı bilimsel doğruluk kanıtı olarak yeterli kabul edilmemelidir. Kaynak kod, başarısız test, düzeltilmiş revizyon ve bağımsız insan değerlendirmesi gerekir.

## 3. Aday araştırma boşluğu — dikkatli ifade

Ön tarama sonunda şu ifade araştırmaya değer görünmektedir; **henüz kanıtlanmış bir özgünlük iddiası değildir**:

> Genel LLM abstention ve kod üretiminde abstention araştırmalarından farklı olarak, gerçek açık kaynak yazılım hatalarının kök neden teşhisinde kanıt paketleri kademeli biçimde azaltıldığında modelin (a) kök nedeni doğru tahmin edip etmediği, (b) bu teşhisi sunulan kanıtın destekleyip desteklemediği ve (c) kanıt yetersizken cevap vermekten kaçınıp kaçınmadığı birlikte ölçülebilir.

Bu katkı ancak üç koşul sağlanırsa savunulabilir:
1. Yazılım hata teşhisi/bug localization, evidence ablation ve abstention kombinasyonunu doğrudan inceleyen yakın çalışmalar tam metin düzeyinde aranır.
2. Veri kümesi, daha önce kullanılan vaka havuzlarından bağımsız ve kaynak-kod düzeyinde denetlenebilir olur.
3. Önceden tanımlanmış kanıt birimleri ve çift eksenli puanlama, genel RAG kanıt yeterliliği benchmarkından ölçülebilir biçimde ayrılır.

## 4. Bir sonraki literatür taraması için arama dizgileri

- ("bug localization" OR "fault localization" OR "root cause diagnosis") AND (abstention OR "selective prediction" OR "answerability")
- ("software debugging" OR "bug diagnosis") AND ("insufficient evidence" OR uncertainty OR calibration)
- ("LLM" AND software engineering) AND ("selective risk" OR "risk-coverage" OR abstention)
- ("code generation" AND abstention) NOT root-cause diagnosis
- (evidence ablation OR evidence sufficiency) AND software engineering AND LLM

Aranacak kaynak grupları: ACL Anthology, arXiv, ACM Digital Library, IEEE Xplore, Springer, ScienceDirect ve atıf ağları. Her bulunan çalışma için görev, veri, model, evidence manipulation, abstention policy, puanlama, değerlendirme birimi ve sınırlılıklar tablosu tutulmalıdır.

## 5. Kaynaklardan çıkarılabilecek sonuçların sınırı

Bu ön tarama, aday fikrin bilimsel açıdan araştırılmaya değer olduğunu destekler; özgünlük, başarı, ulusal finalistlik veya yayınlanabilirlik garantisi vermez. Arama kapsamı henüz sistematik değildir ve bazı bağlantılarda yalnızca özet/ön baskı bilgisi incelenmiştir. Deney sonuçları üretildiğinde literatürden beklenen sonuçlara göre yorum yapılmamalı; ters veya sıfır bulgular da olduğu gibi raporlanmalıdır.
