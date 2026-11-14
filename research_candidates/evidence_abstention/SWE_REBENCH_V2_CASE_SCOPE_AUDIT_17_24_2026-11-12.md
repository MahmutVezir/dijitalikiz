# SWE-rebench V2 vaka kapsamı ve PR/issue eşleştirme denetimi: 17–24. kayıtlar

**Denetim tarihi:** 12 Kasım 2026  
**Cohort:** 12 Kasım 2026 tarihinde dondurulmuş 96 projelik birincil aday havuzunun 17–24. satırları.  
**Amaç:** Seçilen upstream PR/issue kayıtlarının yazılım hata düzeltmesi olup olmadığını, araştırmanın kök neden teşhisi kapsamına uygunluğunu ve cohort'taki sabit base commit ile eşleşmesini değerlendirmek.  
**Yöntem:** GitHub PR/issue metadata'sı, immutable base SHA karşılaştırması, changed-file listeleri ve patch yapısının statik incelenmesi.  
**Yürütme sınırı:** Bu denetimde upstream kaynak checkout edilmedi; test/build çalıştırılmadı; paket kurulmadı; model yüklenmedi, inference veya fine-tuning yapılmadı.

## Yönetici özeti

- **PR/base commit eşleşmesi: 8/8 exact match.**
- **Geçici bug adayı: 4/8** — SkyPilot, PyThaiNLP, Modin, Robot Framework Robocop. **Koşullu bug adayı: 1/8** — NAPALM; PR test fixture'ının issue'daki ham cihaz çıktısıyla kimliği eşleşmiyor ve kaynak/provenans belirsiz.
- **Katı bug-kök-neden örnekleminden dışlama: 3/8** — SQLMesh (improvement/feature), ARMI (feature request; PR açıkça features), CrossGL (enhancement).
- **Kabul edilmiş doğrulayıcı vaka: 0.** Geçici olarak tutulan hiçbir kayıt henüz test çiftinin kusura duyarlılığı, tam dosya/lisans kapsamı, kök neden ve insan değerlendirmeleri yönünden kabul edilmedi.
- Bu 8 kaydın sınıflandırması 96 kayıtlık cohort'un geneline genellenemez.

## Kayıt bazında kararlar

| # | Cohort instance / depo | PR ve bağlı issue | Base SHA | PR/issue kapsamı | Ön karar |
|---:|---|---|---|---|---|
| 17 | 'skypilot-org__skypilot-5985' — [skypilot-org/skypilot](https://github.com/skypilot-org/skypilot) | [PR #5985](https://github.com/skypilot-org/skypilot/pull/5985), [issue #5981](https://github.com/skypilot-org/skypilot/issues/5981) | Exact | Kubernetes/SSH context adlarında lstrip('ssh-') karakter kümesi davranışı nedeniyle önek dışındaki karakterlerin de silinebilmesi; üretim kodunda gerçek önek kaldırma yardımcı fonksiyonuna geçiş ve ilgili test güncellemesi. | **Geçici bug adayı** |
| 18 | 'tobikodata__sqlmesh-3654' — cohort adı [TobikoData/sqlmesh](https://github.com/SQLMesh/sqlmesh) deposuna yönleniyor | [PR #3654](https://github.com/SQLMesh/sqlmesh/pull/3654), [issue #3629](https://github.com/SQLMesh/sqlmesh/issues/3629) | Exact | Python modellerinde global değişken/bağımlılık çözümlemesini isteğe bağlı kılan davranış. PR başlığı Feat; issue etiketi Improvement. Repo, cohort'taki eski TobikoData adı yerine SQLMesh organizasyonuna taşınmış; sabit base SHA değişmemiş. | **Dışla: improvement/feature** |
| 19 | 'napalm-automation__napalm-2152' — [napalm-automation/napalm](https://github.com/napalm-automation/napalm) | [PR #2152](https://github.com/napalm-automation/napalm/pull/2152), [issue #2151](https://github.com/napalm-automation/napalm/issues/2151) | Exact | NX-OS 10.3(5) sürüm satırının regex ile yanlış ayrıştırılması; parser düzeltmesi eklenmiş. Ancak issue yorumundaki ham çıktı ile PR'ın yeni fixture'ı farklı cihaz/yıl/seri/uptime/System version bilgileri taşıyor; kaynak ve issue-test eşleştirmesi net değil. | **Koşullu bug adayı — fixture/provenans hold** |
| 20 | 'terrapower__armi-2121' — [terrapower/armi](https://github.com/terrapower/armi) | [PR #2121](https://github.com/terrapower/armi/pull/2121), [issue #2089](https://github.com/terrapower/armi/issues/2089) | Exact | Veritabanından yükleme sonrası simetrik çekirdeği tam çekirdeğe genişletmek için yeni ayar davranışı. Issue feature request; PR şablonunda Change Type: features açıkça seçilmiş. | **Dışla: feature request** |
| 21 | 'pythainlp__pythainlp-1046' — [PyThaiNLP/pythainlp](https://github.com/PyThaiNLP/pythainlp) | [PR #1046](https://github.com/PyThaiNLP/pythainlp/pull/1046), [issue #1004](https://github.com/PyThaiNLP/pythainlp/issues/1004) | Exact | Tayca tone_detector fonksiyonunun ครับ ve ค่ะ örneklerinde ton sınıflandırmasını yanlış yapması; algoritma koşulları ve regresyon örnekleri düzeltiliyor. Issue bug etiketi taşıyor. | **Geçici bug adayı** |
| 22 | 'modin-project__modin-7554' — [modin-project/modin](https://github.com/modin-project/modin) | [PR #7554](https://github.com/modin-project/modin/pull/7554), [issue #7553](https://github.com/modin-project/modin/issues/7553) | Exact | AutoSwitchBackend ayarı kapalıyken groupby işleminin backend pinleme yolunda NotImplementedError vermesi; query compiler davranışı ve parametreli regresyon testleri düzeltiliyor. | **Geçici bug adayı** |
| 23 | 'crossgl__crosstl-201' — [CrossGL/crosstl](https://github.com/CrossGL/crosstl) | [PR #201](https://github.com/CrossGL/crosstl/pull/201), [issue #187](https://github.com/CrossGL/crosstl/issues/187) | Exact | DirectX backend'e ASSIGN_XOR (^=) operatörü desteği ekleniyor. Issue enhancement olarak etiketli; değişiklik yeni dil/backend işlevi kazandırıyor. | **Dışla: enhancement** |
| 24 | 'marketsquare__robotframework-robocop-1374' — [MarketSquare/robotframework-robocop](https://github.com/MarketSquare/robotframework-robocop) | [PR #1374](https://github.com/MarketSquare/robotframework-robocop/pull/1374), [issue #1371](https://github.com/MarketSquare/robotframework-robocop/issues/1371) | Exact | robocop format --check biçimlendirme gerektiren dosyalar olsa da 0 çıkış kodu veriyor; formatter/CLI çıkış kodu ve regresyon testleri düzeltiliyor. | **Geçici bug adayı** |

## Geçici olarak tutulan kayıtlar için sonraki test-uygunluğu soruları

Bu tablo kabul kararı değildir. Teknik yeniden üretim kapısına gelindiğinde her aday için ilgili base/buggy ve fixed commit'lerde aynı hedef testin kusuru gerçekten sınadığının ayrıca gösterilmesi gerekir. Özellikle:

- **SkyPilot:** Değişiklik çok sayıda üretim dosyasındaki prefix dönüşümünü kapsıyor; seçilecek tek hedef test, lstrip kaynaklı yanlış kırpma davranışına doğrudan duyarlı olmalı.
- **NAPALM:** Issue yorumundaki raw output ile PR fixture'ı aynı değil: issue 2002–2024 Cisco copyright, Nexus9000 C93180YC-FX3, seri ABC12345DE, uptime 1 gün 1 saat 11 dakika 11 saniye ve System version 10.2(6) içeriyor; PR fixture'ı 2002–2017 copyright, Nexus 3048, seri TM6012EC74B, uptime 50 gün 5 saat 9 dakika 7 saniye ve System version 7.0(3)I4(7) içeriyor. Ortak kritik satır `NXOS: version 10.3(5) [Maintenance Release]`. Bu, parser kusurunu mantıken destekler ama fixture'ın issue'daki ham çıktı olduğunu kanıtlamaz. Fixture'ı yeniden dağıtım için kopyalama; önce minimal sentetik testle base/fixed davranışını izole et ve upstream testin aynı kusura duyarlı olduğunu doğrula.
- **PyThaiNLP:** Ton sınıflandırma regresyon örnekleri sabit runtime ve sabit dilbilimsel referansla doğrulanmalı.
- **Modin:** AutoSwitchBackend açık/kapalı matrisi ve gerçek NotImplementedError yolu hedef testte açıkça kapsanmalı.
- **Robocop:** --check modunda değiştirilecek dosya varken çıkış kodunun 1, değişiklik yokken 0 olduğu doğrudan test edilmeli.

SQLMesh, ARMI ve CrossGL kayıtları provenance için korunur; ancak önceden belirlenen katı 'mevcut yazılım kusurunu düzeltme' ölçütüne göre ana bug-kök-neden örneklemine alınmaz.

## Karar ve sınırlar

- PR/base commit provenance: **8/8 exact match**.
- Geçici bug adayı: **4**; koşullu bug adayı: **1** (NAPALM).
- Katı bug örnekleminden dışlanan: **3**.
- Kabul edilmiş doğrulayıcı vaka/proje: **0/0**.
- Lisans: Bu belge 17–24 kayıtlarının exact-commit kök LICENSE veya dosya bazlı lisans denetimini tamamlamaz. Ayrı kaynak lisansı/NOTICE incelemesi gerekir.
- Test: Hiçbir upstream test çalıştırılmadı; FAIL_TO_PASS metadata alanı test geçerliliği kanıtı sayılmadı.
- İnsan değerlendirmesi: Kök neden ve E1/E2/E3 yeterlilik panelleri yapılmadı.
- Model: Model yükleme, inference ve fine-tuning yapılmadı.

**Bir sonraki sınırlı iş paketi:** cohort'un 25–32. satırlarına aynı PR/base SHA/issue-tipi taramasını uygulamak. NAPALM #2152, raw-output/fixture uyuşmazlığı çözülene ve minimal sentetik fail-to-pass testi kanıtlanana kadar teknik kabul kuyruğunda bekletilir. Önceden belirlenmiş dahil etme/dışlama ölçütleri değiştirilmemeli. Upstream test çalıştırma ancak gerekli lisans/provenance kapıları tamamlandıktan sonra başlayabilir.

Bu belge metadata ve statik patch incelemesidir; hukuki uygunluk görüşü, doğrulanmış veri kümesi, kabul edilmiş vaka kaydı veya deney sonucu değildir.
