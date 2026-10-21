# Ön teknik vaka incelemesi — BugsInPy-black-3

**Durum:** Teknik açıdan umut verici aday; **kabul edilmiş doğrulayıcı vaka değildir**.  
**Kohort:** Önceden dondurulmuş ilk 120 metadata adayının ilk sekizli teknik tarama partisi.  
**Kaynak BugsInPy revizyonu:** `11c5f1eea954a42132cfd06bf257766a7963e0fd`  
**Teknik tarama koşusu:** [GitHub Actions run 39651002472](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39651002472)  
**İndirilen vaka artefaktı:** ID `12369751588`; run artefaktında `artifact-audit.json` ham sinyalleri ve checksum listesini içerir.

## Sabit metadata ve kaynak izi

- BugsInPy proje/vaka kimliği: `black` / `3`
- Kayıtta belirtilen Python: `3.8.3`
- Beklenen buggy commit: `8126b4f6a9342290de4655e6a8a78cd288ce7daa`
- Beklenen fixed commit: `7a14a37981862ef418f3cdb4a7e2375856f97529`
- `bug.info` SHA-256 (teknik tarama artefaktındaki baytlar): `09ac24b9d2f0224396ef78dd9ef288d4d4605acda48494400b908dfb8c4790cc`
- `run_test.sh` komutu: `python -m unittest -q tests.test_black.BlackTestCase.test_invalid_config_return_code`
- `bug.info` ve `run_test.sh` upstream BugsInPy deposunun sabit revizyonunda doğrulandı; hedef test günlükleri Python `3.8.3` ortamını bildiriyor.

## Kaynak kod ve testten görülen olası kök neden

Buggy sürümde `black.py` içindeki `--config` seçeneğinin Click parametre türü `click.Path(exists=False, ...)` olarak ayarlanmış. Düzeltme yaması `exists=False` değerini `exists=True` yapıyor. İlgili test, geçersiz/yok bir yapılandırma yolu verildiğinde beklenen CLI çıkış kodunun 2 olduğunu sınar. Ham buggy logunda gerçek çıkış kodu 1 geliyor; log, mevcut olmayan geçici yapılandırma dosyası açılmaya çalışılırken `Error reading configuration file` hatasını içeriyor. Fixed tarafta aynı hedefli test geçiyor.

Bu, doğru yönde bir **hedef regresyon testi sinyali**dir: geçersiz yolun parametre doğrulamasında mı yoksa dosya okunurken mi ele alındığı değişiyor. Ancak bu ön not, iki bağımsız insan değerlendiricinin kök neden kararı yerine geçmez. Testin tam beklentisi ve buggy/fixed çalışma ağacı farkı insan incelemesinde kayıtlara dayalı olarak tekrar doğrulanmalıdır.

## Otomatik teknik sinyaller — run 39651002472

- Buggy hedef test çıkış kodu: `1`
- Fixed hedef test çıkış kodu: `0`
- Buggy test-failure imzası: `true`
- Fixed geçiş işareti: `true`
- Metadata ile Python runtime eşleşmesi: `true`
- Artefakt bütünlüğü denetimi: `integrity_pass=true`
- Otomatik ortam/fixture uyarısı: `false`
- Otomatik tam çift sinyali: `true`

Bu alanlar otomasyon raporundan aktarılmıştır; bilimsel vaka kabul kararı değildir. `integrity_pass` yalnızca artefaktın denetim kapsamındaki bütünlüğünü ifade eder.

İlgili SHA-256 değerleri:
- `buggy-test.log`: `6b4a7e70c0b4678e7cfed38887f31f8ddea81a94b7fb1971fb843e761e526f3e`
- `fixed-test.log`: `11b870b56982a54cd1a0293015807cf6435177ae40d74d4f189bf1818ab6ce78`
- `buggy-runtime-fingerprint.txt`: `d1430cf15702c47640f910ac307b86634e989ddcd277505db0e5c939ac2f7a21`
- `fixed-runtime-fingerprint.txt`: `4644a53e519611d47a35468e1da4522218d9e2a73bb928f9a26675f1d043d36d`

## Lisans ilk kontrolü

Buggy commit'te `psf/black/LICENSE` içeriği MIT lisansıdır. Kaynak dosyanın GitHub blob SHA-1'i `7a9b891f713e1d0a522f042a28f28ba0c5f390d4` olarak elde edildi; bu SHA-1, SHA-256 ile karıştırılmamalıdır. Nihai lisans kaydı yine tam inceleyici formunda proje kaynağı/revizyonu ve atıf yükümlülüğüne göre onaylanmalıdır.

## Açık kalan tüm kapılar

- [ ] En az iki bağımsız ground-truth inceleyicisinin ayrı kararları ve gerekçeli uzlaşma/adjudication kaydı
- [ ] Bu vaka için prior exposure ve aynı bug ailesi/PR/duplicate bağımsızlık incelemesi
- [ ] Hedef testin doğrulama niyeti ve düzeltme farkının bağımsız teknik incelemesi
- [ ] E1/E2/E3 kanıt paketlerinin model çıktısı olmadan üretilmesi ve **başka** iki bağımsız değerlendirici tarafından onaylanması
- [ ] İstemlerden patch, fixed commit, issue/PR kimliği ve cevabı açığa çıkaran metadata sızıntısının denetlenmesi
- [ ] Üç kanıt paketinin SHA-256 değerleri, karar kayıtları ve nihai vaka kabul kaydı
- [ ] Global readiness preflight: en az 60 kabul edilmiş vaka / 8 upstream proje; hedef 80

**Son karar:** `candidate_not_accepted`. Bu kayıt `CASE_REGISTRY.json` içinde kabul edilmiş vaka sayısını artırmaz. Daha önce teknik tarama amacıyla açıldığı için artık önceden belirlenmiş kohort düzeninde belgelenen bir adaydır; insan onayı olmadan deney girdisi/confirmatory case olarak kullanılamaz.
