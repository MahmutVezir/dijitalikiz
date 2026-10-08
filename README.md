# dijitalikiz

**LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**

Bu depo, Standard Context ile açık ve yapılandırılmış Cross-Component Dependency Graph (CCDG) temsilinin LLM tabanlı kök neden teşhisine etkisini kontrollü deneyle ölçmek için kullanılan araştırma altyapısıdır. Projenin aktif çalışma mimarisi yalnızca GitHub + Python + Kaggle + Hugging Face + sabit LLM checkpoint'inden oluşur. Supabase ve Vercel bu araştırmanın çalışma zamanı altyapısı değildir; veri setindeki gerçek yazılım vakalarında geçmeleri deneysel içerik olarak korunabilir.

## Araştırma tasarımı

- Aynı vaka için Standard ve CCDG koşulları karşılaştırılır.
- Ground truth hiçbir model bağlamına verilmez.
- Model, checkpoint/revision ve generation ayarları dondurulmuştur.
- Her vaka/koşul için 5 seed kullanılır.
- Seed'ler bağımsız vaka değildir; birincil analiz birimi yazılım vakasıdır.
- Vaka düzeyinde başarı, 5 seed'in en az 3'ünde tam tanı doğruluğudur.
- Birincil karşılaştırma exact iki taraflı McNemar testiyle yapılır.
- Pilot sonuçları görülmeden ana benchmark vaka seçimi veya sonuç lehine değişiklik yapılmamalıdır.

## Ana bileşenler

- `dijitalikiz/models.py`: vaka, CCDG, ground truth ve tanı çıktısı veri modelleri
- `dijitalikiz/context.py`: Standard/CCDG bağlam üretimi ve leakage kontrolünün temeli
- `dijitalikiz/evaluation.py`: dondurulmuş deterministik skorlayıcı
- `scripts/run_pilot.py`: 30 frozen inference kaydını fail-closed biçimde üretir
- `scripts/model_load_preflight.py`: deneysel üretim yapmadan frozen model/GPTQ yükleme smoke testini çalıştırır
- `scripts/build_pilot_artifact_manifest.py`: tamamlanan pilot çıktılarının SHA-256 bütünlük manifestini üretir
- `scripts/evaluate_pilot.py`: inference kayıtlarını skorlar; modeli yeniden çalıştırmaz
- `scripts/analyze_case_level.py`: pilot evaluation çıktısından vaka düzeyi analiz ve McNemar testi üretir
- `scripts/audit_pilot_integrity.py`: model/prompt/context/hash/schema bütünlüğünü fail-closed denetler
- `scripts/power_mcnemar.py`: eşleştirilmiş binary sonuçlar için power analizi
- `scripts/validate_benchmark_manifest.py`: confirmatory benchmark freeze koşullarını doğrular
- `docs/MAIN_BENCHMARK_SELECTION.md`: ana benchmark vaka seçimini model çıktılarından bağımsız olarak dondurur
- `docs/ANALYSIS_PLAN.md`: önceden belirlenmiş analiz planı
- `docs/CONTAMINATION_AUDIT.md`: model contamination denetim protokolü
- `data/pilot/pilot_manifest.json`: dondurulmuş pilot konfigürasyonu

## Pilot

Dondurulmuş pilot tasarımı:

**3 vaka × 2 koşul × 5 seed = 30 inference kaydı**

Model:
`Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4`

Exact checkpoint revision:
`68c4276063d1496cdf13d0b8e8221f899bfa77f7`

Frozen system prompt: `data/pilot/SYSTEM_PROMPT.txt` (SHA-256 pinned in manifest)

Generation:
- temperature = 0.2
- top_p = 1.0
- do_sample = true
- max_new_tokens = 256
- seeds = 42, 43, 44, 45, 46

Çalıştırma:

```bash
python -m pip install -r requirements-pilot.txt
python scripts/run_pilot.py
python scripts/evaluate_pilot.py
python scripts/analyze_case_level.py \
  --evaluation data/pilot/pilot_evaluation.json \
  --case-ids commons-math-defects4j-MATH-927 commons-math-defects4j-MATH-950 commons-math-defects4j-MATH-988 \
  --output data/pilot/case_level_analysis.json
```

Yerel ortamı kaydetmek için:

```bash
python scripts/capture_environment.py
```

İnference başlamadan veya kayıtlar taşınmadan önce bütünlük kontrolü:

```bash
python scripts/audit_pilot_integrity.py
```

Tamamlanan pilot için bütün 30 kaydı zorunlu kılan audit:

```bash
python scripts/audit_pilot_integrity.py --require-complete
```

Beklenen inference kayıt sayısı 30'dur. Eksik inference dosyaları veya incomplete evaluation nihai vaka düzeyi analizi tarafından reddedilir.

## Bilimsel sınırlar

- Pilot doğruluk sonucu henüz depoda bulunmamaktadır.
- Pilot 3 vakadan oluştuğu için effect-size/power varsayımını tek başına güvenilir biçimde belirlemez.
- Main benchmark için vaka sayısı, önceden belirlenmiş power varsayımı ve bağımsız vaka seçimiyle belirlenmelidir.
- Pilot contamination audit tamamlandı: MATH-927 ve MATH-988 yüksek, MATH-950 orta risk olarak sınıflandırıldı; bu etiketler eğitimde gerçekten görülmüş olunduğunu kanıtlamaz.
- Gerçek kaynak/fix/provenance bilgileri doğrulanmadan sentetik veya yeniden oluşturulmuş vaka gerçek vaka olarak etiketlenmez.
- Fine-tuning ana pilot deneyinin parçası değildir.

## Aktif çalışma mimarisi

```text
GitHub -> GitHub Actions -> Kaggle GPU -> Hugging Face checkpoint -> LLM inference
                                              |
                                              v
                              Standard Context vs CCDG Context
                                              |
                                              v
                                  deterministic evaluation
                                              |
                                              v
                                   case-level analysis
                                              |
                                              v
                                  exact McNemar analysis
```

Bu repo bir web uygulaması/backend projesi değildir. Supabase, Vercel, Next.js, PostgreSQL veya authentication katmanı deney için gerekli değildir. `data/` altında Supabase/Vercel gibi ürün adları geçen hata vakaları varsa bunlar araştırılan yazılım sisteminin parçaları olarak korunur; altyapı bağımlılığı anlamına gelmez.

## Test ve CI

Aktif `tests/` test paketi GitHub Actions üzerinde çalıştırılır. CI ayrıca dondurulmuş pilot konfigürasyonunun bütünlük audit'ini yürütür.

Yerel test:

```bash
pytest -q
```

Legacy RSC-Bench içeriği mevcut araştırma paketinin aktif test kapsamı değildir; mevcut CI yalnızca bu projenin `tests/` paketini çalıştırır.

## Mimari sınır

Aşağıdaki kural araştırma tamamlanana kadar korunur:

> Deneysel metodolojiye, tekrarlanabilirliğe veya ölçülebilirliğe doğrudan katkısı olmayan yeni bir servis projeye eklenmez.

Bu nedenle frontend, hosted database, authentication ve deployment katmanları kapsam dışıdır. Ayrıntılı karar kaydı `docs/ARCHITECTURE.md` dosyasındadır.

## Mevcut durum ve sonraki zorunlu adımlar

Kod ve protokol tarafının frozen pilot için gerekli güvenlik kontrolleri tamamlanmıştır. Gerçek deney verisi hâlâ üretilmemiştir; kalan deneysel işlemler:

1. Yerel makinede 30 pilot inference'ı gerçekten çalıştırmak.
2. `pilot_evaluation.json` üretmek ve parse/schema/duplicate sonuçlarını incelemek.
3. Pilot contamination audit sonuçlarını ana benchmark vaka seçiminde dikkate almak.
4. Power varsayımını ve main benchmark vaka sayısını dondurmak.
5. Bağımsız ana benchmark vakalarını provenance + ground truth + CCDG ile tamamlamak.
6. Ana inference'ı çalıştırmak.
7. Önceden tanımlı exact McNemar analizini uygulamak.
8. Gerçek sonuçlarla TÜBİTAK raporunu doldurmak.

Bu adımların hiçbiri inference veya bağımsız kanıt olmadan varsayımsal sonuçlarla doldurulmamalıdır.
