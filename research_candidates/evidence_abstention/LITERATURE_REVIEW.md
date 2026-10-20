# Literatür taraması — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Tarama tarihi:** 20 Ekim 2026  
**Durum:** İlk tarama; sistematik derleme değildir.

## İlk sonuç

Cevaptan kaçınma (abstention), seçici tahmin, kanıt yeterliliği ve LLM güven kalibrasyonu üzerine yayınlar mevcuttur. Bu nedenle “yapay zekâ ne zaman cevap vermemeli?” tek başına yeni bir bilimsel katkı değildir. Projenin özgünlüğü ancak yakın çalışmaların tam metinleri, veri kümeleri ve değerlendirme yöntemleri sistematik biçimde karşılaştırıldıktan sonra değerlendirilebilir.

## İlgili çalışmalar

### 1. Know Your Limits: A Survey of Abstention in Large Language Models
Wen et al. (2025), Transactions of the Association for Computational Linguistics.
https://aclanthology.org/2025.tacl-1.26/
Genel abstention yöntemleri, benchmarklar ve değerlendirme ölçütlerini özetler. Projemiz için genel alanda özgünlük iddiasını sınırlar.

### 2. Do LLMs Know When to NOT Answer? Investigating Abstention Abilities of Large Language Models
Madhusudhan et al. (COLING 2025).
https://aclanthology.org/2025.coling-main.627/
Cevaplanabilir ve cevaplanamaz sorularda modelin abstention becerisini inceler. Sadece “cevap ver / verme” karşılaştırması yeterli özgünlük sağlamaz.

### 3. Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention Calibration in Retrieval-Augmented Generation
Zhang & Wu (2026).
https://www.techscience.com/cmc/v89n1/68467
Tam, kısmi, ilgisiz, bulunmayan ve çelişkili kanıt koşullarında cevap ve abstention davranışını ele alır. Kontrollü kanıt azaltma yaklaşımıyla doğrudan kavramsal örtüşme bulunduğundan, farklılığımız dikkatle kanıtlanmalıdır.

### 4. Abstain-R1: Calibrated Abstention and Post-Refusal Clarification via Verifiable RL
Zhai, Liang & Kang (Findings of ACL 2026).
https://aclanthology.org/2026.findings-acl.985/
Kaçınma ve kaçınma sonrası eksik bilgi açıklamasını ele alır. Eksik kanıtı tanımlama tek başına yeni katkı olarak sunulmamalıdır.

### 5. Task Abstention for Large Language Models in Code Generation
Zhou et al. (2026).
https://arxiv.org/abs/2605.17029
Kod üretiminde görevden kaçınma ve risk kontrolünü inceler. Yazılım alanında abstention çalışması olduğu için “yazılım alanında ilk” iddiası kurulamaz.

### 6. Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation
Sharma & David (2025).
https://arxiv.org/abs/2502.11620
Kod üretimi doğruluğunu belirsizlik tahminiyle değerlendirmeyi ve kaçınmayı inceler. Belirsizlik sinyaliyle cevapları filtrelemek tek başına özgün değildir.

### 7. Evaluation of LLM-Based Software Engineering Tools: Practices, Challenges, and Future Directions
Torun et al. (2026).
https://arxiv.org/abs/2604.24621
Yazılım mühendisliği araçlarının değerlendirilmesindeki açık uçlu çıktı, ground truth ve tekrar üretilebilirlik sorunlarını tartışır.

## Geçici aday araştırma boşluğu

Gerçek açık kaynak yazılım kusurlarında kök nedenin kaynak kod, test ve düzeltme kayıtlarıyla doğrulanması; modelin gördüğü kanıtın kontrollü azaltılması; teşhis doğruluğu ile kanıtsal desteğin ayrı puanlanması; ve uygun kaçınma ile gereksiz kaçınmanın aynı protokolde ölçülmesi, araştırmaya değer bir bileşim olabilir. Bunun özgün olduğu henüz kanıtlanmamıştır.

## Sistematik taramada aranacak dizgiler

- ("bug localization" OR "fault localization" OR "root cause diagnosis") AND (abstention OR "selective prediction" OR answerability)
- ("software debugging" OR "bug diagnosis") AND ("insufficient evidence" OR uncertainty OR calibration)
- ("LLM" AND software engineering) AND ("selective risk" OR "risk-coverage" OR abstention)
- (evidence ablation OR evidence sufficiency) AND software engineering AND LLM
- (software defect diagnosis OR bug report) AND (confidence calibration OR abstain OR refusal)

ACL Anthology, arXiv, ACM Digital Library, IEEE Xplore, Springer ve atıf ağları aranmalıdır. Her çalışma için görev, veri, model, kanıt müdahalesi, abstention politikası, değerlendirme birimi, ölçütler ve sınırlılıklar tablosu tutulmalıdır.

## Kaynakların ve iddiaların sınırı

Bu ilk tarama özgünlüğü kanıtlamaz ve başarı, finalistlik ya da yayın garantisi vermez. Bazı kaynaklar için tam metin ve yöntem ayrıntıları ayrıca incelenmelidir. Sonuçlar literatür beklentilerine göre şekillendirilmemeli; sıfır ve olumsuz bulgular da raporlanmalıdır.
