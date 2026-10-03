# dijitalikiz

Bu proje, araştırma metninde tanımlanan metodolojiyi uygulayan ilk çalışan bir çerçevedir.

Amaç:
- aynı temel hata bilgisini farklı temsillerle sunma,
- standart bağlam ile CCDG bağlamını ayırt etme,
- yapılandırılmış çıkışların otomatik değerlendirmesini sağlama,
- pilot deneyler için tekrarlanabilir RSC-Bench benzeri bir örnek tasarlama.

## Proje yapısı

- `dijitalikiz/models.py`: vaka, bağımlılık grafı ve ground-truth veri yapıları
- `dijitalikiz/context.py`: standard ve CCDG bağlam üretimi
- `dijitalikiz/evaluation.py`: yapılandırılmış LLM çıktısının otomatik eşleştirilmesi
- `dijitalikiz/cli.py`: örnek vakayı render etme ve değerlendirme yapma arayüzü
- `data/sample_cases/supabase_rls_case.json`: örnek gerçekçi RLS vaka örneği
- `tests/test_rsc_bench.py`: temel doğrulama testleri

## Çalıştırma

Kurulum:

```bash
python -m pip install -e .
```

Örnek vakayı render etme:

```bash
python -m dijitalikiz --case data/sample_cases/supabase_rls_case.json --mode render
```

Örnek değerlendirme:

```bash
python -m dijitalikiz --case data/sample_cases/supabase_rls_case.json --mode evaluate
```

Test çalıştırma:

```bash
pytest -q
```

## Araştırma metodolojisi

Bu proje, aşağıdaki ana fikri somutlaştırır:

- `I_base`: aynı temel bilgi, ortak semantik yapı olarak korunur.
- `Standard Context`: bilgi sıradan metin olarak verilir.
- `CCDG Context`: aynı bilgi bağımlılık graflarıyla daha açıklayıcı şekilde sunulur.
- `ground_truth`: vaka için otomatik karşılaştırma için yapılandırılmış hedef alanlar tanımlar.
- `evaluation.py`: LLM çıktısını deterministik kurallarla değerlendirir.

Bu proje, ana deney için gerekli protokolün temelini kurar; pilot aşamasında prompt dondurma, vaka ayrımı ve tekrar kontrolü için genişletilebilir.

## Geliştirme notları

- Bu çerçeve, gerçek GitHub issue/PR kaynaklarından toplanan vaka verileriyle beslenebilir.
- Her vaka için ayrıntılı `ccdg` bağımlılık listesi ve `ground_truth` alanları eklenmelidir.
- Ana deneyde promtlar, model metadata ve hash bilgisi loglanmalıdır.
- Deneyler için GLMM benzeri istatistik modeli ve power analysis eklenebilir.
