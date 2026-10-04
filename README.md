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


## Güncel araştırma durumu

- Pilot tasarımı donduruldu: 3 vaka × 2 koşul × 5 seed = 30 inference kaydı.
- Model/checkpoint ve generation ayarları `data/pilot/pilot_manifest.json` içinde sabittir.
- Pilot değerlendirmesi çalıştırılmadan ana benchmark başlatılmamalıdır.
- Birincil analiz birimi yazılım vakasıdır; seed'ler bağımsız vaka değildir.
- Bir vaka, 5 seed'in en az 3'ünde tam tanı doğruluğu sağlanırsa koşul altında başarılı kabul edilir.
- Ana karşılaştırma için exact iki taraflı McNemar testi ve önceden belirlenmiş power varsayımı kullanılacaktır.
- Model contamination riski ayrıca denetlenmelidir; `unknown` riski `low` kabul edilmez.
- `docs/ANALYSIS_PLAN.md` doğrulama analiz planını, `docs/CONTAMINATION_AUDIT.md` contamination denetim protokolünü tanımlar.
- Gerçek inference sonuçları bu depoda henüz bulunmamaktadır; bu nedenle henüz doğruluk sonucu iddia edilmemektedir.
