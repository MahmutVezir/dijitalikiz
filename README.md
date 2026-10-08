# dijitalikiz

**LLM Tabanlı Çapraz-Bileşen Hata Teşhisinde Yapılandırılmış Bağımlılık Temsilinin Etkisinin Deneysel İncelenmesi**

Bu depo, Standard Context ile açık ve yapılandırılmış Cross-Component Dependency Graph (CCDG) temsilinin LLM tabanlı kök neden teşhisine etkisini kontrollü deneyle ölçmek için kullanılan araştırma altyapısıdır. Aktif çalışma mimarisi GitHub + Python + Kaggle + Hugging Face + sabit LLM checkpoint'inden oluşur. Supabase ve Vercel deney runtime'ı değildir.

## Araştırma tasarımı

- Aynı vaka için Standard ve CCDG koşulları karşılaştırılır.
- Ground truth hiçbir model bağlamına verilmez.
- Model checkpoint/revision ve frozen generation ayarları korunur.
- Her vaka/koşul için 5 seed kullanılır.
- Birincil analiz birimi yazılım vakasıdır; seed bağımsız vaka değildir.
- Vaka düzeyinde başarı, 5 seed'in en az 3'ünde tam tanı doğruluğudur.
- Birincil karşılaştırma exact iki taraflı McNemar testiyle yapılır.
- Pilot sonuçları görülmeden ana benchmark lehine protokol değiştirilemez.

## Ana bileşenler

- `dijitalikiz/models.py`: vaka, CCDG, ground truth ve tanı veri modelleri
- `dijitalikiz/context.py`: Standard/CCDG bağlam oluşturma
- `dijitalikiz/evaluation.py`: frozen deterministik skorlayıcı
- `scripts/run_pilot.py`: 30 frozen inference kaydını fail-closed üretir
- `scripts/finalize_pilot.py`: audit → evaluation → case-level analysis → QA → checksum zinciri
- `scripts/pilot_preflight.py`, `scripts/model_load_preflight.py`: execution gate'leri
- `scripts/audit_pilot_integrity.py`: model/prompt/context/hash/schema bütünlüğü
- `scripts/build_pilot_artifact_manifest.py`, `scripts/validate_pilot_artifact_manifest.py`: artifact bütünlüğü
- `scripts/create_candidate.py`, `scripts/list_candidates.py`: aday havuzu yönetimi
- `scripts/validate_benchmark_manifest.py`: confirmatory benchmark freeze gate'i
- `scripts/power_mcnemar.py`: power analizi
- `docs/MAIN_BENCHMARK_SELECTION.md`: ana benchmark seçimi ve freeze kuralları
- `docs/ANALYSIS_PLAN.md`: önceden belirlenmiş istatistik planı
- `docs/CONTAMINATION_AUDIT.md`: contamination risk protokolü
- `data/pilot/pilot_manifest.json`: frozen pilot konfigürasyonu

## Frozen pilot

**3 vaka × 2 koşul × 5 seed = 30 inference kaydı**

Model: `Qwen/Qwen2.5-3B-Instruct-GPTQ-Int4`

Exact revision:
`68c4276063d1496cdf13d0b8e8221f899bfa77f7`

Generation:
- temperature = 0.2
- top_p = 1.0
- do_sample = true
- max_new_tokens = 256
- seeds = 42, 43, 44, 45, 46

Runtime:
- Python 3.11
- torch 2.2.1
- transformers 4.43.2
- accelerate 0.33.0
- optimum 1.17.1
- auto-gptq 0.7.1

### Kaggle execution

Desteklenen otomatik execution lane: **Actions → Kaggle Frozen Pilot**.

Workflow:
1. `execute_inference=true` verilmeden bilimsel inference başlamaz.
2. Exact Git commit private Kaggle kernel içine paketlenir.
3. CUDA preflight, environment capture, frozen audit ve model load gate çalışır.
4. 30 inference kaydı oluşturulur.
5. evaluator, case-level analysis, QA, JSONL ve SHA-256 artifact manifest üretilir.
6. GitHub workflow indirilen artifact manifestini bağımsız doğrular.
7. Sonuçlar GitHub Actions artifact'ı olarak saklanır; `main` branch'e deney çıktısı yazılmaz.

Normal `main` push'ları bilimsel inference başlatmaz.

## Bilimsel sınırlar

- Pilot gerçek inference verisi oluşmadan doğruluk veya hipotez sonucu açıklanmaz.
- Pilot 3 vaka olduğu için main benchmark power hesabı pilot sonucuna göre geriye dönük ayarlanamaz.
- Pilot vakaları confirmatory benchmark'a dahil edilemez.
- Gerçek provenance, ground truth ve CCDG kanıtı olmadan vaka confirmatory olarak işaretlenemez.
- Sentetik/yeniden oluşturulmuş kayıtlar gerçek Defects4J vakası gibi etiketlenmez.
- Fine-tuning frozen pilotun parçası değildir.

## CI

Yerel test:
```bash
pytest -q
```

GitHub Actions ayrıca frozen pilot audit'i, tüm vaka/candidate doğrulaması ve benchmark manifest freeze gate'ini çalıştırır.

## Mevcut bilimsel durum

Kod/protokol tarafı frozen pilot için hazırdır. Ancak bilimsel çalışma henüz sonuç-complete değildir. Zorunlu deneysel kapılar:

1. Gerçek 30 pilot inference'ının tamamlanması.
2. Pilot artifact'inin integrity/QA kontrolünden geçmesi.
3. Bağımsız confirmatory vaka havuzunun provenance + ground truth + CCDG + contamination denetimleriyle oluşturulması.
4. Power varsayımının önceden dondurulması ve final case sayısının buna uyması.
5. Confirmatory inference ve exact McNemar analizi.
6. Gerçek sonuçlarla TÜBİTAK raporunun doldurulması.

Bu kapılar tamamlanmadan proje bilimsel olarak bitmiş ilan edilmez.
