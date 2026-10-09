# TÜBİTAK 2204-A Rapor Taslağı — Sonuç Bekleyen Sürüm

> Bu dosya gerçek deney sonuçları tamamlanmadan önce hazırlanmış yapısal taslaktır. Köşeli parantezli alanlar gerçek inference tamamlandıktan sonra otomatik/kanıta dayalı olarak doldurulmalıdır. Önceden sonuç uydurulmaz.

## Proje Adı

LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi

## Proje Özeti

[Gerçek deney tamamlandığında 150–250 kelimelik nihai özet: amaç, yöntem, veri, ana bulgu, sonuç.]

## Giriş

Modern büyük dil modelleri yazılım mühendisliği görevlerinde kullanılmaya başlanmış; ancak gerçek yazılım hatalarının teşhisinde modelin yalnızca metinsel bağlamı değil, bileşenler arasındaki yapısal bağımlılıkları da nasıl kullandığı halen ayrı bir deneysel sorudur. Defects4J, gerçek dünya yazılım hatalarını sistematik biçimde değerlendirmek için kullanılan önemli bir benchmark kaynağıdır. Kodun yapısının model girdisine açıkça taşınmasının yazılım-anlama görevlerinde yararlı olabileceği GraphCodeBERT gibi yapı-farkındalıklı yaklaşımlarda gösterilmiştir. Qwen2.5 ailesi uzun bağlam, yapılandırılmış veri analizi ve talimat izleme yetenekleri sunan açık ağırlıklı modelleri kapsar. Prompting literatürü de model çıktısının verilen bilgi yapısından etkilenebildiğini göstermektedir. Bu proje, bu genel gözlemleri doğrudan kanıt kabul etmek yerine, Standard Context ile açık CCDG Context koşullarını aynı vaka ve aynı tohumlar üzerinde karşılaştıran kontrollü bir deney kurmaktadır.

Araştırmanın özgün sorusu şudur: **Aynı yazılım hatası hakkındaki kanıtlar Standard Context yerine açık ve yapılandırılmış bir Çapraz-Bileşen Bağımlılık Grafiği (CCDG) ile sunulduğunda, LLM'nin kök neden teşhis doğruluğu artar mı?**

Hipotez H1: CCDG koşulunda vaka-düzeyi tam teşhis doğruluğu Standard Context koşulundan daha yüksektir.

Hipotez H0: CCDG ve Standard Context arasında vaka-düzeyi tam teşhis doğruluğu açısından anlamlı fark yoktur.

Girişte kullanılacak kaynaklar:
1. Just, R., Jalali, D., & Ernst, M. D. (2014). Defects4J: A Database of Existing Faults to Enable Controlled Testing Studies for Java Programs. Proceedings of ISSTA.
2. Guo, D., et al. (2020). GraphCodeBERT: Pre-training Code Representations with Data Flow. arXiv:2009.08366.
3. Qwen. (2024). Qwen2.5 Technical Report. arXiv:2412.15115.
4. Lewis, P., et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS.
5. Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS.
6. Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR.
7. Xia, C. S., et al. (2023). Less is More: Frequent Comprehensive Evaluation of LLMs for Code. [bibliographic metadata to be verified before final submission].
8. Zhuo, T. Y., et al. (2024). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR.
9. RepairAgent authors. (2025). RepairAgent: An Autonomous, LLM-Based Agent for Program Repair. ICSE.
10. Yao, Y., et al. (2022/2023). BugBuilder: An Automated Approach to Building Bug Repository. IEEE.
11. [One additional software-fault-localization/LLM study selected during final literature verification.]

> Kaynaklar yalnızca Giriş bölümünde numaralı olarak kullanılacaktır. Yöntem, Bulgular, Sonuç ve Tartışma bölümlerinde yeni kaynak numarası eklenmeyecek; yöntem ve sonuç ifadeleri doğrudan bu çalışmanın deneysel kayıtlarına dayanacaktır.

## Amaç

Amaç, LLM tabanlı yazılım hata teşhisinde çapraz-bileşen bağımlılıklarının açık ve yapılandırılmış biçimde temsil edilmesinin kök neden teşhis doğruluğu üzerindeki etkisini kontrollü, tekrarlanabilir ve istatistiksel olarak test etmektir.

## Yöntem

### Deneysel Birim

Bir bağımsız gerçek yazılım hatası birincil deneysel birimdir. Beş seed, aynı vakanın tekrarlı üretim koşullarıdır; bağımsız vaka sayısını artırmaz.

### Koşullar

- Standard Context: hata kanıtları, kod parçaları ve gerekli açıklamalar standart metinsel bağlamla sunulur.
- CCDG Context: aynı temel kanıta ek olarak bileşenler ve aralarındaki bağımlılık ilişkileri açık bir CCDG temsiliyle sunulur.

### Model ve Dondurulmuş Ayarlar

- Model: Qwen/Qwen2.5-3B-Instruct
- Revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
- Quantization: none; loading precision: FP16 (pinned source checkpoint stores BF16 weights)
- Pre-inference change note: the GPTQ variant failed the sampling smoke test and reported newly initialized layer parameters before any study records were written. It was replaced with the official checkpoint at an exact revision. Experimental cases, prompts, seeds, context conditions and analysis plan were unchanged.
- Temperature: 0.2
- Top-p: 1.0
- Sampling: true
- Max new tokens: 256
- Seeds: 42, 43, 44, 45, 46

### Pilot

4 vaka × 2 koşul × 5 seed = 40 inference.

### Confirmatory Benchmark

16 bağımsız vaka × 2 koşul × 5 seed = 160 inference.

### Vaka-Düzeyi Sonuç

Bir koşul, beş seed'in en az üçünde evaluator tarafından tam teşhis doğru bulunduğunda vaka düzeyinde başarılı kabul edilir.

### Birincil İstatistik

Paired exact two-sided McNemar test, alpha=0.05.

Birincil etki:
P(CCDG doğru, Standard yanlış) − P(Standard doğru, CCDG yanlış)

%95 güven aralığı:
Newcombe-style yaklaşım ve Wilson skor aralıklarının iki discordant orana uygulanmış biçimi.

## Veri ve Doğrulama

Vaka kayıtlarında provenance, fixed revision, root cause, operation evidence, dependency evidence, CCDG ve contamination-risk metadata tutulur. Ground truth iki koşulun prompt/context render'ına dahil edilmez. Prompt, system prompt ve context SHA-256 hashleri inference metadata'sında saklanır.

## Bulgular

Bu bölüm yalnızca gerçek pilot ve confirmatory artifactleri tamamlandıktan sonra doldurulacaktır.

### Pilot

- Toplam koşu: 40
- Parse başarı oranı: [artifact]
- Standard seed-pass: [artifact]
- CCDG seed-pass: [artifact]
- Vaka-düzeyi sonuç: [artifact]
- QA bayrakları: [artifact]

### Confirmatory

- Toplam koşu: 160
- Standard doğru vaka sayısı: [artifact]
- CCDG doğru vaka sayısı: [artifact]
- McNemar discordant pairs: [artifact]
- Exact p-değeri: [artifact]
- Paired risk difference: [artifact]
- %95 CI: [artifact]

## Sonuç ve Tartışma

Nihai yorum yalnızca gözlenen sonuçlara dayanacaktır. Pozitif sonuç, CCDG'nin incelenen örneklem ve frozen model/quantization koşulları altında teşhis doğruluğuna katkı sağladığını destekleyebilir; negatif sonuç ise bu koşullarda açık bağımlılık temsilinin ek fayda sağlamadığını gösterebilir. Hiçbir sonuç, tüm LLM'ler veya tüm yazılım projeleri için genellenmez.

Contamination riskinin yüksek olarak işaretlendiği kamuya açık Defects4J vakalarında sonuçların yorumlanması ayrıca sınırlandırılacaktır. Bu etiket eğitim verisinde bulunmayı kanıtlamaz; yalnızca kamusal maruziyet olasılığının yüksek olduğunu gösterir.

## Sınırlılıklar

- Frozen model küçük sayılabilecek 3B parametreli bir modeldir ve GPTQ-4bit quantization kullanır.
- Confirmatory havuz 16 bağımsız vakadan oluşur; etki tahmini örneklem alanıyla sınırlıdır.
- Kamuya açık Defects4J vakaları için training-data contamination kesin olarak gözlenemez.
- CCDG oluşturma sürecindeki insan anotasyonu yanlış/eksik ilişki riski taşır.
- Sonuçlar yalnızca seçilen model, prompt, inference backend ve vaka dağılımı için doğrudan geçerlidir.

## Kaynakça

Kaynakça, son rapor üretiminde Giriş bölümündeki numaralandırmayla birebir eşleştirilecek ve yalnızca doğrulanmış bibliyografik bilgiler kullanılacaktır. Deney sonucu ortaya çıktıktan sonra rapora yeni bilimsel kaynak eklenmeyecektir.
