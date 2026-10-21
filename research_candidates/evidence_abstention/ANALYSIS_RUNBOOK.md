# Sonuç analizi runbook'u — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Durum:** Kod ve alan sözleşmesi taslağı; gerçek çıktı analizi yapılmadı. Yeni model çıkarımı kapalıdır.

## Çalıştırma kapısı

Yalnızca `CASE_REGISTRY.json` içinde en az 60 `accepted_for_confirmatory=true` vaka ve en az 8 farklı upstream proje bulunursa analiz yürütülür (hedef 80). `EXPERIMENT_MANIFEST_STAGE3.json` içindeki `case_ids`, kabul edilmiş sicil kayıtlarıyla birebir eşleşmelidir. CSV, her vaka için E1/E2/E3 × P0/P1 altı hücrenin tamamını ve yalnızca son/adjudike edilmiş puanları içermelidir. Önceden maruz kalınan 13 vaka kod içinde de reddedilir.

## CSV alan sözleşmesi

`ADJUDICATED_RESULTS_TEMPLATE.csv` boş bir başlıktır; araştırma verisi içermez.

- `decision`: `diagnose`, `abstain` veya `invalid_output`.
- `root_cause_accuracy`: `correct`, `partially_correct`, `incorrect` veya `unscorable`.
- `evidence_support`: `supported`, `partially_supported`, `unsupported`, `contradicted` veya `uncertain`.
- `missing_evidence_quality`: `discriminative`, `partially_relevant`, `irrelevant_or_unavailable`, `not_applicable` veya `unscored`.
- `unsupported_definitive_diagnosis`: yalnızca E3 için insan kararıyla 0/1; E1/E2 için boş. Geçersiz JSON/eksik çıktı otomatik olarak güvenli puanlanmaz.
- `adjudication_status`: `final`; açık uyuşmazlık veya eksik satır doğrulayıcı analize girmez.

## Birincil istatistik

`RD = rate(P1) - rate(P0)` E3'te kanıtla desteklenmeyen kesin teşhisler için raporlanır; negatif RD P1 lehine daha düşük gözlenen orana işaret eder. İki yönlü exact McNemar p-değeri, uyumsuz çiftler üzerinde koşullu binom hesabıyla elde edilir.

%95 RD güven aralığı, her politika oranı için ayrı 97,5% exact Clopper–Pearson aralıklarını birleştiren **konservatif Bonferroni aralığıdır**. Bu, eşleştirilmiş verilere dayalı test-inverting bir aralık değildir; eşzamanlı iki marjinal aralığın kapsamasını en az %95 sağlayan muhafazakâr seçimdir. Dolayısıyla aralık ile McNemar p-değeri eşik yakınında birebir uyumlu olmayabilir. Bu yöntem gerçek sonuçlar görülmeden kaydedilmiştir ve sonradan daha dar aralık seçilmeyecektir.

Bu ayrım, eşleştirilmiş ikili veride güven aralığının p-değeriyle tutarlı olması için özel yöntemler gerektiğini tartışan literatür dikkate alınarak açıkça yazıldı: Fay & Lumbard (2021), *Confidence Intervals for Difference in Proportions for Matched Pairs Compatible with Exact McNemar's or Sign Tests*, https://pmc.ncbi.nlm.nih.gov/articles/PMC9447366/.

## Çıktı

JSON raporu girdi hash'lerini, N/proje sayısını, P0/P1 oranlarını, RD ve konservatif %95 CI'ı, exact McNemar p-değerini, E1/E2/E3 × politika tanımlayıcılarını ve her upstream projeyi sırayla dışlayan duyarlılık tahminlerini içerir. Bunlar gerçek insan puanlarından üretilmeden sonuç sayılmaz.
