# Aday doğrulama kuyruğu sonucu — 21 Ekim 2026

**Durum:** Metadata tabanlı önceliklendirme tamamlandı; vaka doğrulama ve bilimsel kabul tamamlanmadı.  
**Dal:** `research/evidence-abstention-draft-2026-10-19`  
**BugsInPy revizyonu:** `11c5f1eea954a42132cfd06bf257766a7963e0fd`  
**İş akışı:** [Evidence Abstention Metadata Inventory run 39631244221](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39631244221)  
**GitHub artifact:** `evidence-abstention-bugsinpy-screening-queue`, ID `12359746306`, 30 gün saklama; ZIP SHA-256 `6998f8c5141469f028f1ee7cda1708813ee592edd22ca57a0dbeea0cffb9f23c`.

## Çıktı sayımları

| Ölçüt | Sonuç |
|---|---:|
| Girdi ham metadata satırı | 501 |
| Kuyruğa alınan aday | 495 |
| Kuyruktaki upstream proje | 17 |
| İlk tarama grubu (en fazla 5/proje) | 80 |
| Sonraki tarama kuyruğu | 415 |
| Önceden açıldığı için kalıcı dışlama | 5 |
| Metadata/commit tutarsızlığı nedeniyle kuyruk dışında | 1 |
| Bu iş akışında çalıştırılan buggy/fixed test çifti | 0 |
| Bu iş akışında incelenen lisans | 0 |
| Bu iş akışında incelenen kök neden/kanıt seviyesi | 0 |
| Kabul edilmiş doğrulayıcı vaka | **0** |
| Yeni proje için LLM çıkarımı | **Yapılmadı** |

İlk tarama grubu proje bazında dengeli sırayla ilerler; bu **örnekleme veya kabul işlemi değildir**. Proje başına beşten az aday olan projelerde elde bulunan kadar kayıt vardır. Kuyruk, vaka doğrulaması başladığında tek bir büyük projeyi önce bitirmek yerine farklı kaynak projeleri erkenden incelemeye yardım eder.

## Hash'ler ve artefakt doğrulaması

- Screening queue CSV SHA-256: `19dbc7cdc00a20614d37a80b62aa567427359100ceb1b5c3a3e8cf9441b61d92`
- Screening queue summary JSON SHA-256: `95e53f71a8b51132d9d40d660a30b9bf41fac1133a7ed76dccfed3799446c24d`
- Inventory CSV SHA-256: `069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb`
- Inventory summary JSON SHA-256: `c248f556399b2c229ac47b5824479509c984bac8b0d4570b408eabfca52fe4c0`

İş akışı çıktısı yerel olarak açılıp kontrol edildi: ZIP bütünlüğü, beklenen dört dosya, satır sayıları, proje sayısı ve SHA-256 değerleri eşleşti.

## Otomatik testler

- Screening queue birim testleri: 2 test geçti.
- Metadata inventory testleri: 3 test geçti.
- Aynı committeki genel no-inference CI: [run 39631244423](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39631244423), repository/configuration job'ı; önceki tamamlanmış genel doğrulama [run 39630902173](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39630902173) içinde `pytest -q` 265 test geçişi kaydetti.
- Güncel no-inference readiness [run 39631244475](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39631244475): preflight testleri geçti; `ready=false`, 0 kabul edilmiş vaka/proje ve 16 engel.

Birim testlerinin geçmesi, BugsInPy hata vakalarının test çiftlerinin doğrulandığı anlamına gelmez.

## Sonraki teknik adım

Kuyrukta ilk grup 80 adaydır; hepsi manuel incelemeye alınmaya hazır metadata adaylarıdır ama henüz hiçbiri test/ground-truth/lisans/kanıt kapısını geçmemiştir. Her birinde belirtilen Python sürümünün ve bağımlılıkların tekrarlanabilir ortamı kurulmalı; buggy tarafındaki hedef hata ve fixed tarafındaki geçiş ayrı günlük ve fingerprint ile doğrulanmalıdır. Kurulum hatası, hedef hata olarak sayılmamalıdır.

Kabul hedefi aynı: **en az 60 bağımsız vaka ve en az 8 proje; hedef 80 vaka**. Bu rapor kaynak taramasını ileri götürür, fakat deney hazır olma statüsünü değiştirmez.


## Exact-runtime diagnostic update — run 39632366228

The already-exposed `BugsInPy-tqdm-1` case was run under the metadata-recorded Python 3.6.9. The buggy-side target test failed with the expected `TypeError: 'int' object is not subscriptable` (and reported a live-instance teardown error); the fixed-side target test passed. The case remains permanently excluded from confirmatory analysis and does not increase the accepted-case count.

The smoke artifact ZIP checksum from the GitHub artifact service is recorded, but its initial internal `SHA256SUMS` used runner-absolute paths and is not portable. A follow-up workflow change now creates relative checksums and validates them before uploading future artifacts. This note does not claim that those amended workflow steps have already completed successfully; their validation is pending the next run.
