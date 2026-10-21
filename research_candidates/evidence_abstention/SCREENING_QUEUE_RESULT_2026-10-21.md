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


## Dondurulmuş ilk 120 adaylık cohort

[SCREENING_COHORT_120_2026-10-21.json](SCREENING_COHORT_120_2026-10-21.json) güncel 487 adaylı kuyruğun ilk 120 sıra numarasını sabitler. Toplam 17 proje, **0 çalıştırılmış test çifti / 0 kabul edilmiş vaka / 0 LLM çıkarımı**. Bu intake sırası rastgele örneklem değildir; vakalar reddedilirse sıradaki yedek adaylar 121. kuyruk sırasından aynı kural ile incelenecektir. Bu cohort'un hiçbir üyesi henüz kabul edilmiş veri olarak kullanılmıyor.

## İlk-dalga teknik doğrulama v6 — devam eden

[Actions run 39641682522](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39641682522) workflow aracını doğrulamak için kullanılan ve ana örnekleme kalıcı olarak alınmayacak vakaları yeniden çalıştırıyor. İki tamamlanmış artefakt indirildi ve yerelde SHA-256 doğrulandı:

- Black-2: artifact ID `12364903680`, ZIP SHA-256 `11b5765f3b9b948d03b166aee0037c643c151f560e9126a492a1c6e44139972f`. Python 3.8.3 eşleşti; explicit `tests/data/fmtonoff4.py` fixture'ının kaynağı ve kopyası aynı SHA-256 verdi; buggy hedef test formatlama farkında başarısız, fixed hedef testi geçti. `artifact-audit.json`: integrity pass, bug-specific automated signal present, manual review required, accepted=false.
- FastAPI-1: artifact ID `12366405628`, ZIP SHA-256 `ddb400a073cc718b442e150701f3728d3375863d55c1cd73b2a8da51da9bfb45`. Python 3.8.3 eşleşti; buggy hedef test `exclude_defaults` parametresinde TypeError verdi, fixed hedef testi geçti. `artifact-audit.json`: integrity pass, signal present, manual review required, accepted=false.

Bu ikisi de workflow-debug vakaları olduğundan **kalıcı dışlama** statüsündedir; gerçek örneklem sayısını artırmaz. Diğer beş matris işinin tamamlanması bekleniyor; tamamlanmış artefaktlar geldikçe aynı hash/log denetimi uygulanacaktır. Run'ın yeşil olması veya hedef testi geçmesi tek başına lisans, kök neden, kanıt yeterliliği, sızıntı veya bağımsız insan puanlaması kapılarını geçmez.
