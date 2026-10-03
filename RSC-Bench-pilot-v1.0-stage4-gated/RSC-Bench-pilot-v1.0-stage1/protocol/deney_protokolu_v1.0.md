# Deney Protokolü v1.0 — Pilot Hazırlık Sürümü

## 1. Araştırma sorusu

Yapılandırılmış çapraz-bileşen bağlamının LLM'ye sunulması, React-Supabase gibi çok bileşenli yazılım entegrasyonlarında kök neden hata teşhis doğruluğunu standart bağlama kıyasla değiştirir mi?

## 2. Hipotezler

**H0:** CCDG kullanımı ile Standard Context kullanımı arasında kök neden teşhis doğruluğu bakımından anlamlı fark yoktur.

**H1:** CCDG kullanımı ile Standard Context kullanımı arasında kök neden teşhis doğruluğu bakımından anlamlı fark vardır.

H1 yönlü değildir. CCDG daha iyi, aynı veya daha kötü sonuç verebilir.

## 3. Deneysel değişken

Bağımsız değişken: representation format.

- `standard`
- `ccdg`

Her iki koşulda da aynı temel semantik bilgi (`I_base`) kullanılmalıdır.

CCDG, yeni deneysel bilgi eklemek yerine I_base içindeki çapraz-bileşen bağımlılıklarını açık biçimde temsil eder. CCDG kaydında `base_input_sha256` tutulur ve bu değer canonical I_base hash ile eşleşmek zorundadır.

## 4. Birincil bağımlı değişken

Ground-truth-matched root-cause diagnosis accuracy:

- `1` = önceden tanımlı kurallara göre doğru
- `0` = yanlış

Birincil değerlendirme deterministik matcher ile yapılır. String similarity, cosine similarity ve LLM-as-a-judge birincil metrik değildir.

## 5. Model

Birincil deneyde tek sabit LLM/checkpoint kullanılacaktır. Kaydedilecek metadata mümkün olduğunca şunları içerir:

- provider
- exact model/checkpoint/snapshot ID
- experiment date
- API version
- temperature
- top_p
- max output tokens
- seed (yalnızca gerçekten destekleniyorsa)
- system prompt hash
- user prompt hash
- tool configuration
- mevcut diğer provenance metadata'sı

Dinamik model alias'ı tek başına yeterli değildir.

## 6. RSC-Bench vaka yapısı

Her vaka mümkün olduğunca şu alanları içerir:

- `case_id`
- `source`
- `source.url`
- `source.publication_date`
- `technology`
- `error_description`
- `I_base`
- `ground_truth`
- `ground_truth_evidence`
- `CCDG`
- `contamination`

Gizli API anahtarları, tokenlar, parolalar ve kişisel bilgiler veri setine alınmaz.

## 7. Gerçek vaka önceliği

Ana veri setinde gerçek, kamuya açık ve bağımsız doğrulanabilir vakalar önceliklidir. Öncelikli kaynaklar GitHub Issues, GitHub Pull Requests, Stack Overflow, Supabase/public teknik kaynaklar ve uygun diğer kamuya açık teknik hata kaynaklarıdır.

Sentetik veya reconstructed vakalar ana kanıt kaynağı değildir. Gerektiğinde mekanizma, hassasiyet veya contamination analizlerinde ikincil kullanım alanına sahiptir.

## 8. Pilot

Pilot yalnızca teknik doğrulama içindir:

- schema validation
- CCDG validation
- JSON parsing
- output validation
- ground-truth açıklığı
- prompt teknik doğrulaması
- API/model bağlantısı
- metadata logging
- R=5 tekrar altyapısı
- vaka içi varyansın ön değerlendirmesi
- gerekirse insan değerlendirici uyumu

Pilot sonucu ana hipotezi destekleyen kanıt olarak kullanılmaz.

Pilot vakaları ana veri setinden kalıcı olarak dışlanır.

## 9. Prompt freeze

Pilot sırasında prompt teknik doğrulama için geliştirilebilir. Teknik işleyiş doğrulandıktan sonra promptlar canonicalization → SHA-256 hash → freeze sürecinden geçirilir.

Freeze sonrasında anlamsal değişiklik yapılamaz. Teknik bug düzeltmeleri ayrı değişiklik kaydıyla yapılır.

## 10. Tekrarlar

Planlanan tekrar sayısı: **R=5 / vaka / koşul**.

Tekrarlar aynı vaka içinde nested observations'dır ve bağımsız vaka gibi analiz edilmez.

## 11. Güç analizi

Ana vaka sayısı pilot sonrası belirlenecektir. Pilot çıktılarından baseline accuracy, CCDG accuracy, within-case variance ve repeat variability gibi parametreler elde edilerek Monte Carlo simulation-based power analysis yapılacaktır.

Hedefler:

- alpha = 0.05
- power = 0.80

## 12. İstatistiksel analiz

Tekrarlı binary sonuçlar ve vaka içi bağımlılık dikkate alınacaktır. GLMM önceden belirlenmiş aday analizdir:

`logit(P(Yij=1)) = β0 + β1 Conditionij + ui`

Burada `i` vaka, `j` tekrar, `Condition` Standard/CCDG ve `ui` vaka etkisidir.

Nihai analiz yöntemi ana sonuçlar görüldükten sonra sonuç lehine seçilmeyecektir.

## 13. Kör değerlendirme

Otomatik matcher koşuldan bağımsız çalışmalıdır. Standard ve CCDG koşullarının aynı I_base kullandığı ayrıca hash ile doğrulanır; CCDG grafiğinin kaynak vaka ile bağlantısı referans bütünlüğü ve allowed relation kontrolleriyle doğrulanır. İnsan değerlendirmesi kullanılırsa körleme, değerlendirici ataması ve anlaşmazlık çözümü önceden tanımlanmalıdır.

## 14. Contamination

Model eğitim verisiyle örtüşmenin tamamen sıfır olduğu iddia edilmez. Mümkün olduğunda daha yeni vakalar, bağımsız doğrulanabilir kaynaklar ve kontrollü sentetik varyantlar kullanılabilir. Contamination sınırlılık olarak raporlanır.

## 15. Araştırma tarafsızlığı

CCDG'nin daha başarılı olması önceden varsayılmaz. Sonuçlar CCDG lehine, fark yok veya CCDG aleyhine olabilir. Veri seçimi, prompt, metrik ve analiz yöntemi sonuçlara bakılarak değiştirilmez.

## 16. Durum

Birincil matcher şu anda üç çıktı alanını birlikte eşleştirir: `diagnosed_component`, `root_cause_class`, `affected_entity`. Ground truth içindeki `operation` ve `required_relation` alanları korunur ancak mevcut model-output şeması bunları istemediği için birincil accuracy kriterine sessizce dahil edilmez. Bu karar prompt freeze öncesinde değiştirilecekse protokol değişikliği olarak kaydedilmelidir.

Bu belge pilot hazırlık sürümüdür. Ana veri seti, ana deney ve ana sonuç üretimi henüz başlatılmamıştır.

## Pilot v1.1 — Gerçek vaka seçimi

Aşama 2'de dört gerçek ve herkese açık teknik vaka pilot veri setine alınmıştır. Vaka kaynakları GitHub Issues ve GitHub Discussions'tır. Her vaka için gözlenen problem `I_base` içinde, doğrulanmış kök neden ise ayrı `ground_truth.jsonl` kaydında tutulur. Böylece model-facing context, kaynağın çözüm cümlesini doğrudan kopyalamaz.

Pilot vakaları teknik doğrulama amacıyla kullanılacak ve ana RSC-Bench veri setine kalıcı olarak alınmayacaktır. Kaynaklar ve seçim gerekçeleri `dataset/pilot/REAL_PILOT_SOURCES.md` içinde tutulur.

Gerçek vaka seçimi için minimum kriterler:
- kamuya açık ve bağımsız olarak erişilebilir kaynak;
- gözlenen semptomun açıkça tarif edilmesi;
- kök nedenin kaynakta açık veya izlenebilir biçimde doğrulanması;
- birden fazla bileşen arasında anlamlı bağımlılık bulunması;
- gizli bilgi, API anahtarı, parola veya kişisel verinin veri setine taşınmaması.

Bu aşamadaki dört vaka: Supabase JWT generator/runtime mismatch, Supabase Studio/Edge Function response contract mismatch, Supavisor zombie client-handler leak ve Supabase Storage/S3 CopyObject metadata directive omission.
