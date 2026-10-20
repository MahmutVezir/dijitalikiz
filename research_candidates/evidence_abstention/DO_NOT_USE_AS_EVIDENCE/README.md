# Bu yeni araştırmada bilimsel veri/sonuç olarak kullanma

Bu klasör kasıtlı olarak bir **dışlama politikası** içerir; eski araştırma dosyalarını buraya taşımıyoruz, çünkü ana depodaki geçmiş korunmalıdır. Dosya/klasör sınıflandırmasının tam ve yetkili listesi: [REPO_SCOPE_SPLIT.md](../REPO_SCOPE_SPLIT.md).

## Kesin dışlama alanları

- `data/benchmark/**`, `data/calibration/**`, `data/candidates/**`, `data/candidate_case_drafts/**`, `data/pilot/**`, `data/followup_v2/**`, `data/incident_audits/**`
- `RSC-Bench-pilot-v1.0-stage4-gated/**`, `RSC-Bench-pilot-v1.0-stage4-gated.zip`, `rsc-bench-v0.1.zip`
- `kaggle/confirmatory_kernel.py`
- `dijitalikiz/**` ve proje-özel `scripts/**`: yeni deneyde doğrudan çalışma/puanlama motoru olarak kullanılmaz. Genel yöntem örüntüleri ancak inceleme ve bağımsız yeniden uygulamadan sonra yararlanılabilir.
- Eski benchmark ve deney şemaları `schemas/**`: yeni protokole olduğu gibi taşınmaz.
- Eski sonuç/rapor belgeleri `docs/CONFIRMATORY_RESULTS_2026-10-09.md`, `docs/HISTORICAL_EXPERIMENT_SCIENTIFIC_AUDIT_2026-10-15.md`, `docs/PILOT_*.md`, `docs/FINAL_*.md`, `docs/TUBITAK_*.md`.
- Önceden görüntülenmiş format örnekleri: BugsInPy black-1, tqdm-1, httpie-1, youtube-dl-1 ve PySnooper-1. Bunlar ana doğrulayıcı örneklem dışında kalır.

## Gerekçe

Bu öğeler farklı bir araştırma sorusu, eski vaka havuzları, geçmişte incelenmiş/kalibrasyonda kullanılmış kayıtlar ve farklı puanlama varsayımları içerir. Bunları yeni projeye aktarmak vaka bağımsızlığı, veri sızıntısı ve bilimsel izlenebilirlik sorunları doğurabilir.

Bu dışlama, geçmiş deneyin değersiz olduğu veya dosyaların depodan silineceği anlamına gelmez. Sadece yeni çalışmanın kanıtı olarak kullanılamayacakları anlamına gelir. Model çıkarımı, bağımsız yeni vaka listesi ve doğrulama kapıları kapanana kadar kapalıdır.
