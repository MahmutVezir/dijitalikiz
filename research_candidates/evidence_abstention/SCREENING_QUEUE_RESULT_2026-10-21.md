# Aday doğrulama kuyruğu sonucu — 21 Ekim 2026

**Durum:** Metadata önceliklendirmesi ve otomasyon kontrolleri geçti; bilimsel vaka kabulü tamamlanmadı.  
**Dal:** `research/evidence-abstention-draft-2026-10-19`  
**BugsInPy revizyonu:** `11c5f1eea954a42132cfd06bf257766a7963e0fd`  
**Son başarılı envanter/kuyruk/artefakt-test koşusu:** [Actions run 39640796171](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39640796171)  
**GitHub artifact:** `evidence-abstention-bugsinpy-screening-queue`, ID `12363279778`, artifact ZIP SHA-256 `bb5be61baf9102f607fdbc51db34c7b07262ed4dcb548fe0eff8cff24b88f048`.

## Güncel sayımlar

| Ölçüt | Sonuç |
|---|---:|
| Girdi ham metadata satırı | 501 |
| Asgari metadata alanları geçen kayıt | 500 |
| Metadata/commit tutarsızlığı nedeniyle kuyruk dışında | 1 |
| Önceden açılma/fizibilite nedeniyle kalıcı dışlama | 5 |
| Workflow doğrulaması için kullanılan vaka nedeniyle kalıcı dışlama | 8 |
| **Kuyruğa alınan metadata adayı** | **487** |
| Kuyruktaki upstream proje | 17 |
| İlk tarama grubu (`project_round ≤ 5`) | 78 |
| Sonraki tarama kuyruğu | 409 |
| Gerçek buggy/fixed test çifti bu metadata iş akışında çalıştırıldı | 0 |
| Bu metadata iş akışında lisans/kök neden/kanıt seviyesi incelemesi | 0 |
| **Kabul edilmiş doğrulayıcı vaka** | **0** |
| Yeni proje için LLM çıkarımı | **Yapılmadı** |

İlk tarama grubu dengeli bir **inceleme sırasıdır**, rastgele örneklem ya da kabul edilmiş vaka kümesi değildir. Beş önceki maruziyet vakası ve sekiz workflow-debug vakası artık kuyrukta yer almıyor. Böylece doküman ile kuyruğun aynı dışlama kurallarını izlediği test edildi.

## Artefaktlar ve hash'ler

Güncel dört dosyalı artifact ZIP yerel olarak açıldı; ZIP bütünlüğü temizdi. Metadata envanteri ve kuyruk satır/proje sayıları kontrol edildi.

- Screening queue CSV: `d03d2331a902f32cbb1f11922f9dda69fa51d2070b8a3cb07f1a9a689529cd1c`
- Screening queue summary JSON: `0c3c2a1858243282dd1af5390709828677b11e576fb9fb9be811b5db9213310c`
- Inventory CSV: `069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb`
- Inventory summary JSON: `c248f556399b2c229ac47b5824479509c984bac8b0d4570b408eabfca52fe4c0`
- Artifact ZIP: `bb5be61baf9102f607fdbc51db34c7b07262ed4dcb548fe0eff8cff24b88f048`

İndirilebilir güncel dosyalar:
- [Metadata envanteri CSV](sandbox:/mnt/data/bugsinpy-metadata-inventory.csv)
- [487 adaylı güncel tarama kuyruğu CSV](sandbox:/mnt/data/bugsinpy-screening-queue.csv)
- [Kuyruk özeti JSON](sandbox:/mnt/data/bugsinpy-screening-queue-summary.json)
- [Metadata envanteri özeti JSON](sandbox:/mnt/data/bugsinpy-metadata-inventory-summary.json)

## Otomatik testler

Run `39640796171` içinde:
- Metadata envanter testleri: 3 geçti.
- Kuyruk oluşturucu testleri: 2 geçti.
- Artefakt denetleyici testleri: 5 geçti.
- Kuyruk oluşturma: 487 aday, 17 proje; workflow-inference yapılmadı.

Bu testler kodun ve artefakt bütünlüğü araçlarının davranışını sınar. Adayların kendilerinin hata testleri çalıştırılmış, lisansları incelenmiş veya kök nedenleri onaylanmış değildir.

## Ayrı ilk-dalga teknik denetimi

[İlk-dalga koşusu 39638198482](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39638198482), tam yedi vakada ham buggy/fixed test günlükleri üretti. Dört vakada (FastAPI-1, Scrapy-1, Sanic-1, Tornado-1) hedef davranışla tutarlı görünen buggy tarafı başarısızlığı ve fixed tarafı geçişi var; Black-2'de buggy başarısızlığı eksik test fixture'ından kaynaklanıyor; Luigi-1 ile TheFuck-1'de hedef test başlamadan/çalışırken eksik bağımlılık veya test eklentisi ortam sorunları var. Bunların tümü workflow doğrulama örnekleri olduğundan **kalıcı dışlama** durumundadır ve 487 aday kuyruğuna dahil değildir. Hiçbirine kabul statüsü verilmedi.

## Sıradaki bilimsel kapı

Kuyruktaki adaylar için sabit metadata sürümü, exact Python runtime, aynı hedef testte buggy-fail/fixed-pass, lisans, patch/kök neden ground truth'u, E1/E2/E3 paketleri, önceki maruziyet ve sızıntı kontrolleri gerçek artefaktlarla doğrulanmalı. Kaynak kurulum/eklenti hatası, buggy sürümde hedef hata sayılmaz. Vaka kabul kararı insan incelemeleri bitince, kapalı sicile ayrı kayıt olarak girilir.

Hedef değişmedi: **en az 60 bağımsız kabul edilmiş vaka ve en az 8 upstream proje; hedef 80 vaka**. Bu rapor metadata kuyruğunu günceller fakat araştırma hazır olma kapısını kapatmaz.
