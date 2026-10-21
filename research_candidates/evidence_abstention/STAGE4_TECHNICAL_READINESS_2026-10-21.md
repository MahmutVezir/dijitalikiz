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

## 5. Aşama geçiş kararı

**Aşama 4 teknik scaffolding başlatıldı. Pilot inference yapılmadı ve yapılmamalı.** Şu an sıfır kabul edilmiş vaka bulunduğundan model pilotu çalıştırmak, önceden belirlenmiş veri ve yöntem kapılarını ihlal eder. Teknik hazırlık ile pilotun tamamlanmasını ayrı raporluyoruz. Aşama 4'ün pilot kısmı kabul edilmiş veri havuzu, dondurma ve onay koşulları tamamlanana kadar açık kalır. Bu durum deney başarısı veya başarısızlığı değildir.
