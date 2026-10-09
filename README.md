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
- Confirmatory vaka seçimi model çıktılarından bağımsız yapılır. Pilot sonrasında scoring protokolünde gerekli görülen değişiklikler tarih ve gerekçeleriyle kaydedilir; önceden kayıtlı kararlar gibi sunulmaz.

## Ana bileşenler

- `dijitalikiz/models.py`: vaka, CCDG, ground truth ve tanı veri modelleri
- `dijitalikiz/context.py`: Standard/CCDG bağlam oluşturma
- `dijitalikiz/evaluation.py`: frozen deterministik skorlayıcı
- `scripts/run_pilot.py`: 40 frozen inference kaydını fail-closed üretir
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

**4 vaka × 2 koşul × 5 seed = 40 inference kaydı**

Model: `Qwen/Qwen2.5-3B-Instruct`

Exact revision:
`aa8e72537993ba99e69dfaafa59ed015b17504d1`

Precision: FP16 at load time (the pinned source checkpoint stores BF16 weights); quantization: none.

Before any pilot inference, the former GPTQ checkpoint was rejected after the loader reported newly initialized layer parameters and stochastic generation failed with invalid sampling probabilities. The official Qwen2.5-3B-Instruct checkpoint was therefore frozen instead. Cases, prompts, context renderer, seeds, generation settings, evaluator, and statistics plan are unchanged; no study records existed at the time of this change.

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
- Native PyTorch FP16 inference (AutoGPTQ/Optimum are not used)

### Kaggle execution

Desteklenen otomatik execution lane: **Actions → Kaggle Frozen Pilot**.

Workflow:
1. `execute_inference=true` verilmeden bilimsel inference başlamaz.
2. Exact Git commit private Kaggle kernel içine paketlenir.
3. CUDA preflight, environment capture, frozen audit ve model load gate çalışır.
4. 40 inference kaydı oluşturulur.
5. evaluator, case-level analysis, QA, JSONL ve SHA-256 artifact manifest üretilir.
6. GitHub workflow indirilen artifact manifestini bağımsız doğrular.
7. Sonuçlar GitHub Actions artifact'ı olarak saklanır; `main` branch'e deney çıktısı yazılmaz.

Normal `main` push'ları bilimsel inference başlatmaz.

## Bilimsel sınırlar

- Pilot gerçek inference verisi oluşmadan doğruluk veya hipotez sonucu açıklanmaz.
- Pilot 4 vaka olduğu için main benchmark power hesabı pilot sonucuna göre geriye dönük ayarlanamaz.
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

1. Gerçek 40 pilot inference'ının tamamlanması.
2. Pilot artifact'inin integrity/QA kontrolünden geçmesi.
3. Bağımsız confirmatory vaka havuzunun provenance + ground truth + CCDG + contamination denetimleriyle oluşturulması.
4. Power varsayımının önceden dondurulması ve final case sayısının buna uyması.
5. Confirmatory inference ve exact McNemar analizi.
6. Gerçek sonuçlarla TÜBİTAK raporunun doldurulması.

Bu kapılar tamamlanmadan proje bilimsel olarak bitmiş ilan edilmez.

## Confirmatory benchmark status — 2026-10-09

### Frozen pilot: completed and integrity-checked

- GitHub Actions run: [37968099402](https://github.com/MahmutVezir/dijitalikiz/actions/runs/37968099402).
- Pilot source commit: `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5`.
- Artifact ID: `11634641753`; GitHub artifact SHA-256: `b12594415894d5cac18442d3bd6c505e843b1a14027272c1afa398a59101aca0`.
- All 40 expected inference records are present. The JSONL export contains 40 records; all outputs parse, and no parse failures were reported.
- An independent review of the downloaded artifact verified its internal SHA-256/size inventory and found no missing or unlisted files.
- Under the pilot's strict complete-diagnostic endpoint, Standard passed 0/20 and CCDG passed 0/20; no pilot case reached the 3-of-5 majority threshold. This is pilot diagnostic evidence, not the confirmatory hypothesis result.

### Confirmatory benchmark: frozen

The confirmatory manifest is now `frozen`, with 16 independent cases, five seeds per case, and two conditions: **16 × 2 × 5 = 160 inference records**. Pilot cases are excluded. The design's power values are assumptions declared for planning, not estimates derived from confirmatory outcomes.

The pilot source commit and confirmatory launch commit are different: `d50adaf9b6d0b017a5d30c9ebd9dd404988dbfb5` and `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`, respectively. This is recorded explicitly because the confirmatory manifest and runner were frozen after the pilot artifact was verified. The shared experimental core at these commits was checked: `dijitalikiz/context.py`, `dijitalikiz/models.py`, `dijitalikiz/evaluation.py`, the prompt and system-prompt files, the pilot manifest, and the pinned requirements file have identical Git blob SHAs. The confirmatory bundle records its own exact source commit and bundle checksum.

**Scoring-protocol amendment:** the primary confirmatory endpoint is root-cause correctness against predeclared aliases. The repository records that pilot outputs were consulted for scoring-protocol diagnostics and that this amendment was made on 2026-10-09 before confirmatory outputs were examined. This is a documented post-pilot amendment; the TÜBİTAK report must not describe the endpoint as fully preregistered before any model outputs were seen. Case selection itself remains independent of model outputs.

### Execution status and next gate

The launch trigger commit is `e1e083f5400432b98143bdb35ff2c5b435ea8f6e`. Its completed workflow state and the 160-record confirmatory artifact have not yet been independently verified in this review. No confirmatory result is claimed until all 160 records, the primary analysis, QA report, and SHA-256 artifact manifest pass validation.
