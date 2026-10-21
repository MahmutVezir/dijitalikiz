# Aşama 4 teknik hazırlık ve geçiş denetimi

**Denetim tarihi:** 21 Ekim 2026
**Dal:** research/evidence-abstention-draft-2026-10-19
**Karar:** Aşama 4 teknik preflight altyapısı başlatıldı; pilot inference KAPALI. Bu kayıt deney sonucu değildir.

## 1. Nerede kalmıştık?

- **Aşama 1:** Hedefli literatür ve ön özgünlük taraması tamamlandı; sistematik derleme veya özgünlük kanıtı değildir.
- **Aşama 2:** Kaynak fizibilitesi koşullu tamamlandı. BugsInPy upstream'inde 17 projede 501 ham hata klasörü sayıldı. Ham sayı kabul edilmiş vaka sayısı değildir. Kabul edilmiş bağımsız doğrulayıcı vaka sayısı **0**.
- **Aşama 3:** E1/E2/E3 × P0/P1 tasarımı ve analiz planı belgelendi. Bu, ön kayıt veya inference izni değildir.
- **Aşama 4:** Boş vaka sicili, runtime adayı, puanlama rubriği taslağı, salt-okunur fail-closed preflight denetimi ve CI testi eklendi.

## 2. Model adayı düzeltmesi

Önceki manifestte GPTQ-Int4 checkpoint'i aday olarak yazılmıştı. Depodaki tarihsel ana dal README'si, önceki GPTQ yüklemesinde başlatılmış parametreler ve geçersiz örnekleme olasılıkları görüldüğünü; ardından resmi, kuantize edilmemiş Qwen/Qwen2.5-3B-Instruct checkpoint'ine geçildiğini kaydediyor. Yeni çalışma için aday revizyon aa8e72537993ba99e69dfaafa59ed015b17504d1, FP16 ve kuantizasyon yok olarak güncellendi.

Bu bir tasarım düzeltmesidir, doğrulanmış runtime sonucu değildir. Model kartı/lisans incelemesi, exact model-tokenizer yükleme denetimi ve runtime fingerprint hâlâ açık kapılardır. İnference yapılmamıştır.

## 3. Teknik eklemeler

- CASE_REGISTRY.json: doğrulayıcı vaka sicili; bilerek boş.
- RUNTIME_LOCK.json: model/runtime adayı ve inference yapılmadığına ilişkin kayıt.
- RUBRIC_AND_ADJUDICATION.md: iki bağımsız puanlayıcı için rubrik taslağı.
- scripts/evidence_abstention_preflight.py: salt-okunur fail-closed kapı denetimi; model yüklemez, inference yapmaz ve dosya değiştirmez.
- tests/test_evidence_abstention_preflight.py: boş veri/hash kapılarının kapalı kaldığını doğrulayan birim testleri.
- .github/workflows/evidence-abstention-preflight.yml: yalnızca test ve rapor modu; model çağrısı, secret veya veri indirme adımı yok.

## 4. İnference öncesi açık engeller

1. En az 60 kabul edilmiş bağımsız vaka ve en az 8 ayrı upstream proje; hedef 80 vaka.
2. Her kabul edilen vakanın kayıtlı ortamda aynı hedef test için buggy-fail/fixed-pass günlükleri.
3. Kaynak/lisans, gold truth, E1/E2/E3 yeterlilik, sızıntı ve önceki inceleme maruziyeti incelemeleri.
4. İki bağımsız değerlendiricinin rubrik kalibrasyonu ve adjudication onayı.
5. Model kartı/lisansı, exact model-tokenizer yüklemesi ve runtime fingerprint.
6. Prompt, şema, analiz planı, tasarım, rubrik, runtime ve vaka sicili için doğrulanmış SHA-256 değerleri.
7. Deney çıktıları alınmadan önce doğrulanabilir protokol ön kaydı.
8. Tüm kapılardan sonra ayrı ve açık yürütme izni.

Komutlar:

    python -m unittest discover -s tests -p 'test_evidence_abstention_preflight.py' -v
    python scripts/evidence_abstention_preflight.py
    python scripts/evidence_abstention_preflight.py --require-ready

İkinci komut blokajları raporlar. Üçüncü komut kapılardan herhangi biri açıksa sıfır dışı kodla durur. Hiçbiri inference yapmaz.

## 5. Otomatik doğrulama kanıtı

GitHub Actions [run 39615830978](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39615830978) branch head commit `2f558aa2e69eed57a51dce4373918224f6807179` üzerinde başarıyla tamamlandı. Üç fail-closed preflight birim testi geçti. Rapor modu **ready=false**, **0 kabul edilmiş vaka**, **0 proje** ve **16 açık blokaj** kaydetti. Başlıca blokajlar: 60 vaka/8 proje eşiği, doğrulanmış protokol ön kaydı, iki değerlendiricili kalibrasyon, exact model/tokenizer/runtime kontrolü ve yedi SHA-256 dondurma girdisi. Workflow rapor modunda çalıştığı için bu beklenen blokajlar CI'ı kırmadı; inference yapılmadı.

Bu CI sonucu yalnızca denetleyicinin kapalı veri durumunda doğru biçimde blokaj raporladığını gösterir. Veri veya model davranışının doğrulandığı anlamına gelmez.

## 6. Aşama geçiş kararı

**Aşama 4 teknik scaffolding ve CI testi tamamlandı. Pilot inference yapılmadı ve yapılmamalı.** Şu an sıfır kabul edilmiş vaka bulunduğundan model pilotu çalıştırmak, önceden belirlenmiş veri ve yöntem kapılarını ihlal eder. Teknik hazırlık ile pilotun tamamlanmasını ayrı raporluyoruz. Aşama 4'ün pilot kısmı kabul edilmiş veri havuzu, dondurma ve onay koşulları tamamlanana kadar açık kalır. Bu durum deney başarısı veya başarısızlığı değildir.


## Aşama 2 envanter güncellemesi — 21 Ekim 2026

[Metadata inventory workflow](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618065599) pinned BugsInPy revizyonunda 501 ham metadata kaydı ve 17 proje saydı. Asgari metadata alanları 500 kayıtta tamam, bir kayıtta buggy/fixed commit kimlikleri aynı. Bu workflow test çalıştırmadı; doğrulayıcı vakalar hâlâ 0. Ayrıntı: METADATA_INVENTORY_RESULT_2026-10-21.md.


## 7. Dışlanan smoke vakasının tekrar sonucu

[Run 39618666531](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618666531) esnasında BugsInPy-tqdm-1 için fixed sürüm testi TypeError: 'int' object is not subscriptable nedeniyle başarısız oldu. Aynı vaka için daha önceki olumlu smoke koşusu bu nedenle tekrarlanabilir kabul edilmemelidir. Metadata ile smoke runtime arasındaki Python sürüm farkı sürüyor (3.6.9'a karşı 3.8.18). Bu vaka daha önce açıldığı için kalıcı olarak dışlanmıştır. Smoke iş akışının otomatik push tetiklemesi kaldırıldı; gelecekte yalnızca elle istenirse tanılama amaçlı çalıştırılabilir.

En son no-inference preflight [run 39618666271](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618666271) başarılıydı ancak ready=false, 0 kabul edilmiş vaka/proje ve 16 açık blokaj bildirdi. Bu beklenen sonuçtur ve inference izni değildir.


## Son durum teyidi — 21 Ekim 2026

Bu belgenin yazıldığı günün en son kaydedilmiş no-inference kontrolü [Actions run 39619057132](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39619057132) başarıyla tamamlanmıştır. Başarılı CI yalnızca test ve salt-okunur preflight raporlamasının çalıştığını gösterir; deney hazır sayılmaz. Run raporundaki karar ready=false olarak kalır; kabul edilmiş doğrulayıcı vaka sayısı 0 ve yeni çalışma için model çıkarımı yapılmış değildir.

Repo giriş sayfası artık bu araştırmayı tek aktif TÜBİTAK 2204-A odağı olarak sunar. Bu belgesel düzenleme hiçbir veri/ön kayıt/runtime kapısını otomatik kapatmaz ve inference izni vermez.


## Sıkılaştırılmış vaka-kabul kapısı — 21 Ekim 2026

Ön kontrol betiği, accepted_for_confirmatory=true olarak işaretlenen her vaka için şu alanları da zorunlu tutacak şekilde sıkılaştırıldı: vaka kaynağındaki Python sürümü ile gerçekten çalışan runtime sürümünün tam eşleşmesi; buggy tarafında hedef hatanın yeniden üretildiğini belirten açık sonuç; fixed tarafında aynı hedef testin geçtiğini belirten açık sonuç; doğrulanmış test çifti; E1/E2/E3 incelemesi; her iki test günlükü için artifact referansı ve SHA-256; runtime fingerprint SHA-256; kök-neden kanıt referansı. Setup veya ortam hatası, buggy-fail kanıtı kabul edilmeyecektir.

Bu değişiklik mevcut vaka sayısını artırmaz ve hiçbir vaka kabul etmez. Birim testleri özellikle runtime uyumsuzluğu ve buggy tarafta hedef hatanın yeniden üretilememesi durumlarında sicilin fail-closed kalmasını sınayacak şekilde genişletildi. Yeni CI sonucu görülene kadar bu kod değişikliğinin doğrulaması “bekliyor” kabul edilmelidir; yeni çalışma için inference hâlâ kapalıdır.
