# RSC-Bench

**LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**

Bu repository, TÜBİTAK 2204-A araştırma projesinin deney yazılımı ve veri altyapısıdır.

## Bilimsel kapsam

Araştırma sorusu:

> Yapılandırılmış çapraz-bileşen bağlamının LLM'ye sunulması, React-Supabase gibi çok bileşenli yazılım entegrasyonlarında kök neden hata teşhis doğruluğunu standart bağlama kıyasla değiştirir mi?

Birincil karşılaştırma:

- `standard`: I_base standart bağlam olarak sunulur.
- `ccdg`: Aynı I_base, bağımlılık ilişkileri açıkça temsil edilen CCDG ile sunulur.

CCDG'nin yeni semantik bilgi eklememesi temel metodolojik ilkedir: `CCDG = f(I_base)`. Her CCDG kaydı canonical `I_base` SHA-256 hash'ini taşır ve doğrulama sırasında eşleşmesi zorunludur.

Birincil çıktı ölçütü, önceden tanımlanmış deterministik ground-truth matcher ile hesaplanan binary root-cause diagnosis accuracy'dir.

## Deney ilkeleri

- Tek sabit LLM/checkpoint kullanılacaktır.
- Model ve üretim metadata'sı kaydedilecektir.
- R=5 tekrar/vaka/koşul planlanmaktadır; tekrarlar bağımsız vaka değildir.
- Pilot vakalar ana veri setine alınmayacaktır.
- Promptlar canonicalization + SHA-256 ile dondurulacaktır.
- Ana sonuçlarda LLM-as-a-judge, cosine similarity veya serbest string similarity birincil metrik değildir.
- Ana veri setinde gerçek ve bağımsız doğrulanabilir vakalar önceliklidir.
- Contamination sıfır olduğu varsayılmayacak; ölçülebilen sınırlılıklar raporlanacaktır.
- Ana deneyden önce pilot verisine dayalı Monte Carlo güç analizi yapılacaktır.
- İstatistiksel analiz vaka içi bağımlılığı dikkate alacaktır; GLMM önceden belirlenmiş aday analizdir.

## Aşama durumu

**Aşama 1 pilot altyapısı teknik olarak tamamlandı; prompt freeze ve gerçek model pilotu henüz yapılmadı.**

Sıradaki aşamalar:

1. Deney Protokolü v1.0
2. Pilot yazılım altyapısı — tamamlandı
3. Pilot veri hazırlığı — sıradaki aşama
4. Teknik doğrulama
5. Prompt freeze
6. Monte Carlo güç analizi
7. Ana veri setinin kilitlenmesi
8. Kör ana deney
9. Deterministik matcher
10. GLMM analizi
11. Bilimsel raporlama

Bu repository şu aşamada ana veri setini toplamaz ve ana deneyi çalıştırmaz.

## Source of truth

GitHub repository araştırmanın yazılım source of truth'udur. Çalışma ortamları yalnızca test, doğrulama, hesaplama ve analiz için kullanılmalıdır.

## Güvenlik

Gerçek API anahtarları, tokenlar, parolalar veya kişisel bilgiler repository'ye yazılmaz. Secret'lar environment/secret manager üzerinden sağlanır.

## Stage 3 — real-model technical pilot

The repository now contains an OpenAI Responses API client and `scripts/run_real_pilot.py`.
Real execution is deliberately opt-in: `RSCBENCH_ALLOW_REAL_PILOT=1` is required, and
`configs/model.yaml` must contain an exact fixed model ID rather than a dynamic alias.
The real run writes provenance-complete JSONL records to `outputs/real_pilot_runs.jsonl`.
This stage is still a technical pilot and is not evidence for H0/H1.

The OpenAI client uses the Responses API. The current OpenAI documentation states that the
Responses API is the recommended replacement for the sunset Assistants API. Model IDs,
parameters and response metadata are recorded rather than inferred from aliases.

## Aşama 4 — Prompt Freeze Gate

Aşama 4 için freeze mekanizması ve ön koşul kontrolü hazırlanmıştır. Ancak gerçek model teknik pilotu henüz çalıştırılmadığı ve exact fixed model ID ile API kimlik bilgileri henüz belirlenmediği için prompt manifesti bilinçli olarak `UNFROZEN` bırakılmıştır. Bu, bilimsel protokol gereğidir; ana deney promptları pilot doğrulaması tamamlanmadan dondurulmaz.

Kontrol:

```bash
python scripts/check_prompt_freeze_ready.py
```
