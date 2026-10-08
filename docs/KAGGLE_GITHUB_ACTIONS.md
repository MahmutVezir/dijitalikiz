# GitHub Actions -> Kaggle

Bu proje Kaggle'ı yalnızca uzak GPU hesaplama ortamı olarak kullanır. Supabase, Vercel
ve web uygulaması çalışma zamanı bu entegrasyonun parçası değildir.

## Bir kere yapılacak GitHub ayarı

Repository Settings -> Secrets and variables -> Actions -> New repository secret:

- KAGGLE_API_TOKEN: Kaggle API ayarlarından oluşturulan güncel API token.
- KAGGLE_USERNAME: Kaggle kullanıcı adınız.

Token repository dosyalarına yazılmaz.

Kaggle CLI güncel sürümlerinde KAGGLE_API_TOKEN doğrudan non-interactive kimlik
doğrulaması için desteklenir. Legacy KAGGLE_USERNAME/KAGGLE_KEY yöntemi de desteklenir.

## Çalıştırma

GitHub -> Actions -> Kaggle Pilot -> Run workflow.

Workflow:

1. Çalıştırılan Git commit'ini exact-source olarak arşivler.
2. Kaggle Kernel metadata'sını geçici olarak oluşturur.
3. Kernel'i NvidiaTeslaT4 GPU ile Kaggle'a push eder.
4. Kaggle üzerinde aynı commit'teki frozen pilot kodunu çalıştırır.
5. Preflight, model-load smoke test, integrity audit, 30 inference ve finalization zincirini
   çalıştırır.
6. Pilot çıktılarını GitHub Actions artifact'i olarak indirilebilir hale getirir.

Workflow push/schedule ile kendiliğinden inference başlatmaz; yalnızca manuel
workflow_dispatch ile çalışır.

## Bilimsel güvenlik

Kaggle tarafında çalıştırılan kaynak commit source_commit.txt ile kaydedilir.
Model, revision, prompt hash, system prompt hash, seed'ler, vaka listesi ve generation
ayarları repository'deki frozen pilot manifestinden gelir.

Bu workflow ana benchmarkı çalıştırmaz. Sadece frozen 30-run pilot içindir.

## Çıktılar

Başarılı çalışmada artifact içinde en az şunlar bulunur:

- pilot_records.jsonl
- pilot_evaluation.json
- case_level_analysis.json
- pilot_artifact_manifest.json
- environment.json

Pilot sonucu tamamlanmadan veya integrity audit geçmeden sonuçlar bilimsel sonuç olarak
yorumlanmamalıdır.
