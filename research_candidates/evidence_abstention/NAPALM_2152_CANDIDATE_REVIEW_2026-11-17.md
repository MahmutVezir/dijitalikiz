# NAPALM #2152 — aday teknik inceleme ve Stage 2 kararı

**İnceleme tarihi:** 17 Kasım 2026  
**Ana kohort sırası:** 19  
**Dataset instance:** `napalm-automation__napalm-2152`  
**Dataset row SHA-256:** `badc723c07fe415e42d9e329529f9669932f43f18d2d0a61907f17d983c3f555`  
**Dataset revision:** `fb9aa226b2ce37c708ea7732e7b980abacdadb67`  
**Issue:** [napalm-automation/napalm #2151](https://github.com/napalm-automation/napalm/issues/2151)  
**Fix PR:** [napalm-automation/napalm #2152](https://github.com/napalm-automation/napalm/pull/2152)

## 1. Karar

- **Stage 2 teknik sonucu:** geçti — exact frozen dataset selector, sabitlenmiş Python ortamında buggy base üzerinde gerçek assertion failure, exact fixed revision üzerinde aynı selector için gerçek pass verdi.
- **Statik kapsam/provenans sınıfı:** koşullu bug adayı. PR'ın eklediği Cisco NX-OS çıktı fixture'ının dosya düzeyindeki kaynağı ve yeniden dağıtım hakkı kanıtlanmış değil.
- **Stage 3:** başlatılmadı. Fixture provenance/lisans incelemesi, bağımlılıkların tam hukuki kapsamı, bağımsızlık/related-defect ve researcher/model exposure incelemesi ile insan adjudication kapıları açık.
- **Nihai vaka kabulü:** verilmedi. Accepted-case sayısı değişmedi; **0**.
- **Model çalıştırma sınırı:** model yükleme, inference, fine-tuning veya eğitim yapılmadı.

Stage 2 teknik geçişi tek başına vaka kabulü değildir; bu karar sadece teknik yeniden üretim kapısını kapatır.

## 2. Frozen dataset kimliği ve hedef test

Parquet SHA-256: `7416e352008b35480c82610cf4f5edf160dd269ed6bf382a22bd4c17daed24b9`.

Dataset row:
- `instance_id`: `napalm-automation__napalm-2152`
- `repo`: `napalm-automation/napalm`
- `base_commit`: `d0d2a3e70d21d0556de71ab0462bd71a1450f820`
- `created_at`: `2024-11-04 21:41:29` (PR zamanı; issue #2151 daha önce oluşturulmuştur)
- `language`: Python
- `license`: Apache-2.0
- `FAIL_TO_PASS` selector sayısı: 1

Exact selector (parametrik node ID korunarak):
```
test/nxos_ssh/test_getters.py::TestGetter::test_get_facts[issue2151]
```

Row SHA-256, geçici runner ortamında immutable Parquet revision'ından seçilen kaydın canonical JSON temsili üzerinde doğrulandı. Final artifact'e Parquet, canonical row veya issue problem statement kopyalanmadı; yalnızca row hash ve sınırlı metadata özeti kaydedildi.

## 3. Kaynak kodu ve defect-specific oracle

Exact upstream base:
`d0d2a3e70d21d0556de71ab0462bd71a1450f820`

Exact fixed revision:
`a3781b83e02cb7ea87da948d82e0c9ee4d91a39a`

Base NX-OS SSH source blob SHA-1:
`7206756d4ed5562ad08958e1b5119bf31a0b85bc`

Fixed NX-OS SSH source blob SHA-1:
`5a71662a8f32bb0d39419a88f43300ce4491a833`

Base parser, `show version` satırlarında `"NXOS: "` ifadesini arayıp eşleşen satırın üçüncü token'ını `os_version` olarak kullanıyordu. Bu koşul hem:

- `NXOS: version 10.3(5) [Maintenance Release]`
- `Host NXOS: version 10.3(5)`

satırlarını eşleştiriyor. İkinci satırın üçüncü token'ı `version` olduğu için ilk doğru değer eziliyordu. PR düzeltmesi, yalnızca `line.strip().startswith("NXOS: version")` koşulunu kabul ederek ikincil `Host NXOS` satırını dışarıda bırakıyor.

Hedef test, yalnızca import/collection veya tip kontrolü yapmıyor: NAPALM'in `wrap_test_cases` sarmalayıcısı `get_facts()` sonucunu beklenen JSON ile karşılaştırıyor ve `os_version` alanındaki uyuşmazlıkta assertion üretiyor. Bu nedenle oracle hedeflenen parser hatasına duyarlı.

## 4. Pinned exact-selector tekrarının kanıtı

**Canonical GitHub Actions run:** [44127350027](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44127350027)  
**Job ID:** `134194652784`  
**Branch head:** `3a7af28b64057b9109f98e82f6a8ae7cdad7bb45`  
**Workflow:** `.github/workflows/napalm-2151-stage2-pinned.yml`

| Kontrol | Buggy base | Fixed revision |
|---|---|---|
| Exact frozen selector | 1/1 çalıştırıldı | Aynı selector 1/1 çalıştırıldı |
| Beklenen sonuç | Gerçek assertion failure | Pass |
| `os_version` | Gerçek: `version`; beklenen: `10.3(5)` | `10.3(5)` |
| Runner sözleşmesi | `base-fail` doğrulandı | `fixed-pass` doğrulandı |

Pinned ortam:
- CPython 3.11.9
- pip 24.3.1
- pytest 8.3.5
- NAPALM 5.0.0
- 51 external distribution lock girdisi; editable NAPALM kaynak kurulumu ile toplam 52 dağıtım
- Lock/freeze karşılaştırması birebir geçti.
- `pip check`: `No broken requirements found.`
- 52 dağıtımın tamamında lisans metaverisi bulundu; eksik metaveri sayısı 0.

Lisans metaverisinin bulunması, lisans şartlarının hukuki olarak onaylandığı anlamına gelmez. Bu kontrol yalnızca envanterin tamamlığını gösterir.

### Test patch kapsamı

Base commit'e uygulanan geçici test-only patch, tam PR diff'i değil, yalnızca altı yeni issue2151 test-fixture dosyasını içeriyordu:
- `expected_result.json`
- `show_hostname.txt`
- `show_hosts.txt`
- `show_interface_status.txt`
- `show_inventory___json.txt`
- `show_version.txt`

Git denetiminde altı dosyanın tamamı untracked olarak görüldü; tracked production değişikliği yoktu. `production_code_changed=false` doğrulandı. Exact fixed revision'a geçerken geçici fixture dosyaları temizlendi.

## 5. Kanıt paketi ve bütünlük

**Canonical artifact:** [napalm-2151-pinned-exact-selector-evidence](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44127350027/artifacts/14348056824)  
**Artifact ID:** `14348056824`  
**Boyut:** 8,575 byte  
**ZIP SHA-256:** `b2d6934038baf751a43ec890fa1a98763bfc10f27b1dd60b3f47aea24f2ff30d`

Artifact indirildi ve ayrıca bağımsız olarak incelendi:
- 16 arşiv girdisi.
- İç `SHA256SUMS.txt` manifestinde 15 dosya.
- 15/15 iç SHA-256 kontrolü geçti.
- Parquet, canonical row, problem statement, ham test logu/stdout, Cisco fixture dosyaları, fixture patch içeriği, full PR patch veya upstream test harness içermiyor.
- Base tarafındaki assertion, artifact'te yalnızca şu sınırlı alanlarla temsil ediliyor: field=`os_version`, actual=`version`, expected=`10.3(5)`. Ham test stdout'u runner'ın geçici alanında silindi.

**Bağımsız minimal sentetik reproducer:** [run 44125927347](https://github.com/MahmutVezir/dijitalikiz/actions/runs/44125927347), job `134189555802`, artifact ID `14347028101`, SHA-256 `854793c9a5a9f12b08ab612ca78a0dfe13dc8d51788d3900d4d5bc5315edaa0d`. Yalnızca iki parser-relevant sentetik NX-OS satırı kullanıldı; base üzerinde beklenen assertion failure, fixed revision üzerinde pass alındı. Bu test dataset'in original selector'ı olarak sayılmıyor; yalnızca bağımsız destekleyici reproducer.

**Superseded/noncanonical artifacts:** Önceki geniş keşif artifact'i `14345838155` ve ara sanitize denemesi `14349135019` nihai kanıt paketi olarak kullanılmamalı veya dağıtılmamalı. İlk paket Parquet ve upstream dosya içeriklerini; ara paket ise ham device-facts test çıktısını içeriyordu. Canonical referans yalnızca `14348056824` numaralı temiz pakettir.

## 6. Açık fixture provenance/lisans kapısı

Issue #2151'in rapor ettiği ham örnek:
- Cisco Nexus 9000 C93180YC-FX3.
- Cisco copyright satırı 2002–2024.

PR #2152'nin eklediği `show_version.txt`:
- Nexus 3048.
- Farklı serial/uptime ve cihaz metaverisi.
- Cisco copyright satırı 2002–2017.

İki metin parser davranışı açısından gerekli şu iki satırı içeriyor; ancak cihaz capture'larının aynı kaynaktan geldiği gösterilmedi. Base commit'in kök lisansı Apache-2.0 ve kök `NOTICE` dosyası mevcut olsa da bunlar PR fixture'ındaki Cisco cihaz çıktısının kaynağını veya yeniden dağıtım yetkisini kendiliğinden kanıtlamaz. Bu nedenle fixture provenance konusu açık kalır.

Bu Stage 2 tekrarında fixture yalnızca runner'ın geçici alanında tutuldu; final artifact'e kopyalanmadı. Bu teknik karar, açık hukuki/provenans kapısını kapatmaz.

## 7. Sonraki aşama ve nihai sınırlamalar

Napalm teknik Stage 2 geçişi olarak ilerleme defterine işlenir. Ancak Stage 3 başlamadan önce:
1. Cisco PR fixture'ının provenansı, lisans/NOTICE kapsamı ve yeniden dağıtım koşulları çözülmeli veya fixture bağımsız, lisans açısından temiz ve aynı kusuru koruyan bir test verisiyle ikame edilmesinin protokol açısından uygunluğu ayrıca değerlendirilmelidir.
2. 51 doğrudan/dolaylı external dependency için yalnızca metadata mevcudiyeti değil, exact-base kurulum kapsamı ve lisans şartları incelenmelidir.
3. Proje bağımsızlığı, related-defect kümelenmesi ve araştırmacı/model exposure-train contamination kapıları incelenmelidir.
4. Gold mekanizma, alternatifler ve E1/E2/E3 için ayrı insan adjudication yapılmalıdır.
5. Complete case-acceptance record, şema doğrulaması ve fail-closed registry kontrolü geçmeden final acceptance verilmemelidir.

**Nihai kayıt:** Stage 2 teknik geçişi = evet; Stage 3 = başlamadı; final accepted case = hayır. Toplam kabul edilmiş bağımsız vaka sayısı 0 olarak korunur. Model inference/training yetkisi verilmemiştir.
