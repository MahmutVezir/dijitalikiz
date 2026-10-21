# Aşama 2 — V5 teknik ekranlama batch denetimi ve V6 devri (21 Ekim 2026)

## Karar özeti

[GitHub Actions run 39663084349](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39663084349) sekiz vakalık, önceden sıralanmış V5 teknik ekranlama grubunu tamamladı. Freeze job ve sekiz case job'u başarılı sonlandı. Artefaktların her birinde kaynak metadata Python sürümü ile vaka-ortamı Python sürümü eşleşiyor.

**Teknik ekranlama sonucu: 7/8 adayda otomatik buggy-fail/fixed-pass sinyali; 1/8 adayda iki taraf da başarısız.** Bu, çalışma hattının belirli bir vaka kümesinde test komutlarını çalıştırabildiğine ilişkin teknik sinyaldir; 7 kabul edilmiş araştırma vakası demek değildir.

Bu batch workflow'u doğrulamak ve ham sonuçları incelemek için kullanıldığından **sekiz adayın tamamı, sonucu ne olursa olsun, doğrulayıcı örneklemden kalıcı olarak çıkarıldı**. Hiçbiri kabul edilmiş vaka sayısına eklenmedi. V6 manifesti bu sekiz adayı ve önceki 32 maruziyet vakasını dışlayarak donduruldu.

## Artefakt sonuçları

| Vaka | Metadata/runtime Python | Buggy hedef testi | Fixed hedef testi | Teknik sinyal | ZIP SHA-256 |
|---|---:|---:|---:|---|---|
| BugsInPy-ansible-3 | 3.6.9 / 3.6.9 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `b622b3b8e3e7ec009eeb2f2ee06e7f6ae678f031395247358a451c2634323f72` |
| BugsInPy-youtube-dl-3 | 3.7.0 / 3.7.0 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `b637bdc217f44d80a02ea3b8034022e48adac1ddd3051e72b34cbb4d706f5865` |
| BugsInPy-cookiecutter-4 | 3.6.9 / 3.6.9 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `9bde47a152bf2be784ec230ecf4af6d99491b90868def5436d298988799a83b5` |
| BugsInPy-tqdm-3 | 3.6.9 / 3.6.9 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `680249b763f4a1b204a84a9176f3b36336a2e960908b4d6029e6957af6d1ba29` |
| BugsInPy-fastapi-4 | 3.8.3 / 3.8.3 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `901991e7fa5d4a4a9f20226afab9dc371a2908a7546a6f6d21a4098b8f5bdf3f` |
| BugsInPy-keras-3 | 3.7.3 / 3.7.3 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `b0508d94200cf9c6a5c8827d79ff4e59c45afdeff1a5bf0e4d80004ad9c371ba` |
| BugsInPy-black-5 | 3.8.3 / 3.8.3 | exit 1 | exit 0 | Sinyal var; insan incelemesi gerekir | `f0b5db59617db33e2a271704866c767b2e0d90978c5d8761fc93f6af755a8362` |
| BugsInPy-httpie-4 | 3.7.3 / 3.7.3 | exit 1 | exit 1 | **Eşleşen çift yok**; fixed taraftaki hata açıklanmalı | `4ef0daba8fe3d6cf58e3856cc093de2c47823503089740549501fb7d5c40edf6` |

Her ZIP içindeki `summary.json`, ham test günlükleri, runtime fingerprint'leri, checkout/compile kayıtları, worktree değişiklik özetleri ve `artifact-audit.json` incelenebilir. ZIP hash'leri bu incelemede indirilen arşivlerden yeniden hesaplandı.

## Yorum sınırları

- Yedi otomatik sinyal, patch'in bildirilen kök nedeni gerçekten test edildiği anlamına tek başına gelmez. Her test hatası ham günlükteki assertion/exception ile patch ve kaynak test arasındaki ilişki üzerinden incelenmelidir.
- Httpie-4 için buggy ve fixed tarafların ikisi de exit 1 verdiğinden bu vaka şu an teknik eşleşme kapısını geçmiyor. Bu sonuç, upstream bug'ın geçersiz olduğunu kanıtlamaz; mevcut test/ortam koşulunun doğrulayıcı çift üretmediğini gösterir.
- Artifact bütünlüğü ve runtime eşleşmesi, lisans/atıf, kök neden ground truth'u, kanıt seviyeleri, sızıntı, önceki maruziyet veya bağımsız insan değerlendirmesi yerine geçmez.
- Bu sekiz vakanın tamamı workflow doğrulama amacıyla kullanıldığı için V6 dışlama listesine alındı.

## V6 intake dondurma

- Dosya: [SCREENING_COHORT_120_V6_2026-10-21.json](SCREENING_COHORT_120_V6_2026-10-21.json)
- Kaynak BugsInPy queue SHA-256: `d03d2331a902f32cbb1f11922f9dda69fa51d2070b8a3cb07f1a9a689529cd1c`
- V6 seçim kuralı: sabit queue sırasını koru; önceki 32 ve V5 teknik batch'inde kullanılan 8 vaka dahil toplam 40 maruziyet ID'sini atla; sıradaki 120 adayı al.
- V6 adayları 15 upstream projeye dağılmıştır; proje başına sayılar eşit değildir ve bu sıra rastgele örneklem değildir.
- Workflow `.github/workflows/evidence-abstention-cohort-batch1.yml` V6 dosyasını doğrular ve ilk sekiz adayı teknik olarak tarar. Metadata/test sonucu otomatik kabul yaratmaz.
- V6 batch CI: [run 39664581005](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39664581005). Freeze job başarılı; son kontrolde Luigi-4, Pandas-3, Sanic-4 ve Matplotlib-3 çalışıyor; Scrapy-4, spaCy-3, TheFuck-4 ve Tornado-4 kuyrukta. Bu aşamada V6 için vaka sonucu veya kabul kararı yok.

## Aşama 2 çıkış kapısı

| Kapı | Durum |
|---|---|
| Kaynak metadata envanteri ve deterministik aday kuyruğu | Tamamlandı; metadata-only |
| Runtime eşleşmesi ve hedef test komutu çalıştırma hattı | V5 batch'inde 8/8 runtime eşleşti; 7/8 buggy-fail/fixed-pass sinyali |
| V6 maruziyet temiz intake sırası | Oluşturuldu; CI doğrulaması bekleniyor |
| En az 60 bağımsız doğrulanmış vaka / en az 8 proje | **0 kabul edilmiş vaka; karşılanmadı** |
| Lisans/provenance incelemesi | Açık |
| İki bağımsız kök-neden değerlendiricisi | Açık |
| Ayrı, kesişmeyen iki kanıt-yeterliliği değerlendiricisi | Açık |
| E1/E2/E3 paketleri, sızıntı ve önceki maruziyet denetimi | Açık |
| Model çıkarımı | Kapalı; yapılmadı |

**Sonuç:** Aşama 2'nin metadata envanteri ve ekranlama altyapısı ilerletildi; bilimsel vaka kümesi henüz kurulmadı. V6 ilk sekiz adayın ham artefaktları incelendikten sonra uygun görülenler insan değerlendirmesine gönderilmeli; aday sırası sonuçlara göre değiştirilmemelidir. 60/8 eşiğine ulaşılmazsa veri fizibilitesi başarısız/keşifsel olarak raporlanmalı, eşik geriye dönük düşürülmemelidir.
