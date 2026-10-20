# Kullanılabilir varlıklar: yeniden kullanım politikası

Bu dizin yalnızca yeni araştırmanın proje planlarını içerir; eski DİJİTALİKİZ sonuçları/deney verileri yeni çalışmanın bilimsel kanıtı değildir. Yetkili kapsam haritası: [REPO_SCOPE_SPLIT.md](../REPO_SCOPE_SPLIT.md). Dışlama listesi: [DO_NOT_USE_AS_EVIDENCE/README.md](../DO_NOT_USE_AS_EVIDENCE/README.md).

## Bu proje için doğrudan kullanılabilir

- Bu yeni araştırmaya özel literatür, fizibilite, prompt, output schema, deney tasarımı ve analiz planı dosyaları.
- Yeni ve bağımsız BugsInPy vakaları, yalnızca kaynak/lisans, buggy-fail/fixed-pass, gold root cause, E-level packet ve kontaminasyon kapılarını geçtikten sonra.
- Yeni proje için yazılan, inference çalıştırmayan vaka smoke test'i; yalnızca teknik test çifti denetimi içindir.
- Eski dokümanlardaki kör puanlama, hash ve fail-closed kontrol ilkeleri; yeni görev için bağımsız protokole uyarlanarak.

## Sadece ilham/şablon — doğrudan kopyalanamaz

Eski docs/, schemas/, scripts/, tests/ ve dijitalikiz/ altındaki içeriklerin çoğu eski problem tanımı, vaka şeması veya çıktılara bağlıdır. Bunlardan veri, karar kuralları, sonuç veya runner doğrudan devralınmaz. Kullanılacak kod yeni protokole göre gözden geçirilip yeniden test edilir.

## Şimdilik kullanılmayan

Eski data/**, RSC-Bench-*.zip, kaggle/confirmatory_kernel.py, eski confirmatory/pilot sonuçları ve TÜBİTAK raporları yeni proje örneklemi/sonucu değildir. Eski format inceleme vakaları da dışlanmıştır.
