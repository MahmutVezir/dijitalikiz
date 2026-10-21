# Kör puanlayıcılar arası uyum protokolü — v0.1

**Durum:** Şablon ve analiz betiği; gerçek insan puanı henüz yok. Kalibrasyon/ön kayıt tamamlanmadı.

## Görev kimliği ve körleme

Model yanıtları puanlayıcılara rastgele üretilmiş opak `task_id` ile gösterilir. Görev dosyasında koşul/P0-P1 etiketi, vaka kimliği, gerçek kök neden, buggy/fixed commit veya kanıt yeterlilik etiketi bulunmaz. Puanlamayı yöneten sorumlu kişi task map'i kilitli ayrı dosyada tutar. Önce bağımsız puanlar kilitlenir; ancak bundan sonra task map, kök neden ve kanıt paketi kararıyla adjudication yapılır.

## Ayrı paneller

- `ground_truth`: iki bağımsız değerlendirici model çıktısının kök neden doğruluğunu kaynak/test/düzeltmeyle karşılaştırabilir; kök neden doğruluğu dışında kanıtsal destek puanı vermez.
- `evidence_support`: iki farklı değerlendirici yalnızca modelin gördüğü kanıt paketi ve anonim model çıktısını görür; gold root cause, kaynak patch'i ve koşul etiketi görmez. Karar, kanıtsal destek, kaçınma ve eksik kanıt talebini puanlar.
- Bu iki panelin reviewer ID kümeleri kesişemez. Her boyutta bütün görevler için aynı iki rater kullanılır; anlaşmazlık sonradan adjudike edilir ama ilk puanlar korunur.

## Cohen kappa ve belirsizlik

`scripts/analyze_evidence_abstention_rater_agreement.py` ham anlaşma, beklenen şans anlaşması, Cohen kappa, kategori sayıları ve görev kimliklerini yeniden örnekleyen 2.000 tekrarlı sabit tohumlu bootstrap %95 yüzdelik aralığı hesaplar. Kategori prevalansı kappa'yı etkileyebilir; bu yüzden kappa tek başına doğruluk sayılmaz ve ham anlaşma/kategori sayımlarıyla beraber sunulur. Bootstraptaki %95'ten az tekrar hesaplanabilir kappa üretirse güven aralığı verilmez.

Bu doğrulayıcı panel dosyası için asgari görev sayısı 360'dır (en az 60 vaka × 6 koşul hücresi). 480 görev, 80 vaka hedefidir. Kalibrasyonda kullanılan vakalar ana doğrulayıcı örnekleme girmez. Sentetik testler sadece hesaplama kodunu denetler; insan uyum verisi değildir.

Şablon `BLINDED_RATER_SCORES_TEMPLATE.csv` boş başlık dosyasıdır. `rating_status=locked_independent` harici satır kabul edilmez. Uyum raporu doğru puanlama anlamına gelmez ve sicile vaka kabul etmez.
