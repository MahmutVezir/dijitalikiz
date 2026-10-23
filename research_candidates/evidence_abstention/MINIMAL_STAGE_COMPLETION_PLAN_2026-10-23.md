# Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ — En Az Aşamalı Tamamlama Planı

**Güncelleme:** 23 Ekim 2026  
**Amaç:** TÜBİTAK 2204-A'ya bilimsel olarak savunulabilir, gerçek sonuçlara dayalı bir çalışma sunmak. Bu belge yürütme planıdır; deney sonucu değildir.

## Gerçek durum (depo kayıtlarına göre)

- Araştırma sorusu, literatür başlangıç taraması, E1/E2/E3 kanıt yeterliliği koşulları ve P0/P1 politikaları tanımlı.
- Qwen adapter'ı, abstention karar katmanı, kalibrasyon yardımcıları, çıktı doğrulaması ve no-inference kapısı için yazılım prototipi var; CPU/CI testleri yazılım davranışını doğruluyor, model başarısını değil.
- BugsInPy metadata kuyrukları ve teknik tarama hatları mevcut. Güncel intake V10, 100 metadata adayı / 14 upstream proje olarak kaydedilmiş. Metadata adayı deney vakası değildir.
- Doğrulayıcı vaka sicili boş: 0 kabul edilmiş vaka.
- Sabitlenmiş Qwen runtime için gerçek GPU yükleme doğrulaması henüz tamamlanmış değil.
- Bağımsız değerlendirici puanları, kalibrasyon etiketleri, denetlenebilir ön kayıt ve gerçek çalışma sonuçları yok.
- Bu nedenle resmî çıkarım izni kapalı kalmalıdır. Bu dosyayı eklemek veya CI'ın yeşil olması çıkarım izni vermez.

## Aşama 1 — Veri ve bağımsız doğrulamayı kapat

**Çıktı:** Önceden maruz kalınmamış, doğrulanmış vaka sicili ve kör E1/E2/E3 kanıt paketleri.

1. EXPOSURE_UNION_2026-10-23.json ile tüm kalıcı dışlamaları uygulayan güncel V10 kuyruğunu ve kaynağın sabit revizyonunu doğrula.
2. Vaka adaylarını birer kez teknik olarak tara. Teknik buggy-fail/fixed-pass sinyali yalnızca insan incelemesine adaylık verir; otomatik kabul yoktur.
3. Her aday için exact Python sürümü, buggy revizyonda hedef test başarısızlığı, fixed revizyonda aynı testin başarısı, hash'lenmiş günlükler, patch/root-cause ilişkisi, lisans, bağımsızlık, maruziyet ve bilgi sızıntısı kontrollerini tamamla.
4. En az 60 kabul edilmiş vaka ve en az 8 upstream proje (hedef 80) sağlanmazsa doğrulayıcı çalışma başlamaz.
5. Birbirinden farklı iki kök-neden değerlendiricisi ve ayrı, kimlik/gold-kök-neden bilgisi görmeyen iki kanıt-yeterliliği değerlendiricisi gerekir. İsimler yerine ilk aşamada benzersiz takma kimlikler kullanılabilir; fakat gerçek bağımsız insanlar olmalıdır. Otomatik model puanlaması bu şartın yerine geçmez.
6. Panel B, model çıktısı görülmeden E1/E2/E3 paketlerini hazırlar, uyuşmazlıkları ve ilk puanları kaydeder. E3 etiketi prompta verilmez.

**Kapı:** Vaka sicili yalnızca tüm zorunlu kanıtlar ve bağımsız insan kararları tamamlanınca güncellenir. Bu aşamada mevcut sicili doldurmak için hiçbir aday otomatik kabul edilmemelidir.

## Aşama 2 — Protokolü dondur, modeli doğrula ve deneyi yürüt

**Çıktı:** Denetlenebilir ön kayıt, sabit runtime, ham model çıktıları ve eksiksiz yürütme günlüğü.

1. UNCERTAINTY_EXPERIMENT_MANIFEST.json, UNCERTAINTY_RUNTIME_LOCK.json, istemler, çıktı şeması, rubrik, analiz planı ve kalibrasyon verisinin SHA-256 değerlerini hesapla ve doğrula.
2. Qwen/Qwen2.5-3B-Instruct ve tokenizer'ı sabit revision ile gerçek hedef GPU ortamında çıktı üretmeden yükle; sürümleri, chat template'i, dtype'ı ve runtime fingerprint'ini kaydet.
3. Ayrı, bağımsız insan incelemesiyle etiketlenmiş kalibrasyon/validasyon kümesini oluştur. Eşikler sonuç örneklemine bakılmadan seçilip dondurulmalı. Kalibrasyon verisi yoksa güven skoru olasılık olarak raporlanamaz.
4. Protokolü ilk doğrulayıcı model yanıtından önce kamuya açık veya zaman damgalı, değişiklik geçmişi denetlenebilir bir yere kaydet. Sadece taslak dosya bulunması ön kayıt sayılmaz.
5. Ayrı ve açık yürütme izni alındıktan sonra E1/E2/E3 × P0/P1 koşullarını sabit model ve seed politikasıyla yürüt. Her ham yanıt, hata, seed, istem/kanıt hash'i ve runtime bilgisi saklanır. Sessiz JSON düzeltmesi veya seçerek çıktı silme yapılmaz.

**Kapı:** Veri, bağımsız inceleme, kalibrasyon, runtime, hash ve ön kayıt şartlarının tamamı kanıtla geçtiği doğrulanmadan inference manifesti kapalı kalır.

## Aşama 3 — Kör değerlendirme, analiz ve başvuru dosyasını tamamla

**Çıktı:** Tekrarlanabilir analiz, sınırlılıkları içeren sonuç raporu ve resmî şablona uygun PDF.

1. Her model çıktısını en az iki bağımsız değerlendirici rubriğe göre puanlar; ilk puanlar, uyuşmazlıklar ve adjudication ayrı kaydedilir.
2. Birincil analiz: E3 koşulunda kanıtla desteklenmeyen kesin teşhis oranı için vaka eşleştirmeli P1−P0 risk farkı, iki taraflı exact McNemar testi ve %95 güven aralığı.
3. İkincil ölçütler: gerçek kök neden doğruluğu, görünen kanıta dayalı destek, cevap kapsamı, E1'de gereksiz kaçınma ve istenen ek kanıtın ayırt ediciliği. Başarısız/uygunsuz çıktılar önceden belirlenmiş kurala göre raporlanır; sonradan seçilerek çıkarılmaz.
4. Sonuçlar hipotezi desteklemese bile aynen raporlanır. Modelin kendi bildirdiği güven, kalibre edilmiş olasılık diye sunulmaz.
5. Raporu güncel TÜBİTAK 2204-A çağrı/rehber/şablonuyla karşılaştır; kaynakça, etik, yöntem, veri, sınırlılıklar ve PDF bütünlüğünü kontrol et.

## Durdurma ve karar kuralları

- **GO:** Bütün veri, bağımsız insan incelemesi, runtime, kalibrasyon, hash ve ön kayıt kapıları kanıtla geçti.
- **HOLD:** En az bir kapı açık; modelin doğrulayıcı çıktıları alınmaz.
- **NO-GO:** Hedef örneklem ya da bağımsız panel makul sürede sağlanamıyorsa, mevcut çalışma doğrulayıcı deney olarak sunulmaz. Daha küçük keşifsel çalışma ancak sonuçlar görülmeden yeniden tasarlanmış ve açıkça keşifsel olarak etiketlenmiş ayrı protokolle yapılabilir.

## Kritik insan bağımlılığı

Bu proje yalnızca kod yazarak tamamlanamaz. Şu anda en büyük blokaj, gerçek ve bağımsız uzman değerlendirmesidir: kök neden için iki kişi ve kanıt yeterliliği için bunlardan farklı iki kişi gerekir. Kullanıcı tarafından gerçekten yürütülmeyen incelemeleri yapılmış gibi kaydetmek, otomatik kabul üretmek veya sentetik değerlendirmeyi insan değerlendirmesi olarak göstermek yasaktır.

## Bir sonraki somut adım

Önce V10 metadata-only intake için son başarılı/başarısız Actions koşusunu ve artefakt bütünlüğünü denetle; ardından yeni maruziyet yaratmadan teknik sinyalleri insan inceleme kuyruğuna aktar. İnsan paneli sağlanana kadar doğrulayıcı vaka sayısı sıfır olarak kalır. Sonraki iş, daha fazla aday taramadan önce bağımsız reviewer panelini fiilen kurmaktır.
