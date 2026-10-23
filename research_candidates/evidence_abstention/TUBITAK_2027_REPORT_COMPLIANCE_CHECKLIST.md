# TÜBİTAK 2204-A 2027 — Rapor Uygunluk Kontrol Listesi

**Durum:** Hazırlık kontrol listesi; nihai proje raporu değildir.  
**Son gözden geçirme:** 23 Ekim 2026  
**Resmî kaynak:** https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi  
**2027 proje rehberi PDF:** https://tubitak.gov.tr/sites/default/files/2026-10/2204A_proje_rehberi_2027.pdf

## Başvuru uygunluğu ve tamamlanmış proje şartı

- [ ] Araştırma gerçek veriyle yürütülmüş, analiz edilmiş ve sonuçlandırılmış.
- [ ] Rapor, plan veya prototipi tamamlanmış deney gibi göstermiyor.
- [ ] Öğrencinin özgün katkısı, danışman/yardımcıların katkısından ayrıştırılmış.
- [ ] Daha önce aynı veya benzer içerikle başka yarışmaya başvuru yapılmadığı ekip tarafından doğrulanmış.
- [ ] Öğrenci(ler) ve varsa danışmanın ARBİS kayıtları güncel.
- [ ] Ana alan ve tematik alan seçimi raporun gerçek amacıyla tutarlı.
- [ ] Gerekli izinler veya onamlar gerekiyorsa alınmış ve raporda belirtilmiş.

TÜBİTAK'ın 2026–2027 çağrısı, proje rehberine uygun hazırlanmış **tamamlanmış** projelerle başvuru yapılmasını ister; fikir aşamasındaki veya devam eden projelerle başvuru yapılmaması gerektiğini belirtir. Son başvuru tarihi 4 Ocak 2027, saat 17.30'dur. Kaynak: resmî çağrı sayfası.

## Başlık ve özet

- [x] Mevcut proje başlığı: **Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ**.
- [x] Başlık 7 kelimedir; 15 kelime sınırının altındadır.
- [ ] Nihai özet 150–250 kelime aralığında.
- [ ] Özet, sonuçlar elde edildikten sonra güncellenecek.
- [ ] Özet yöntem, yürütülen deney, temel bulgular ve sonuçları kısaca verecek.
- [ ] Özet içinde kaynakça, ayrıntılı yorum ve deneyden elde edilmemiş iddialar bulunmayacak.
- [ ] Özet altında en fazla 5 anahtar kelime yer alacak.

## Raporun beklenen iskeleti

Rehberin “Proje Raporu Nasıl Yazılır?” bölümüne ve resmî yazım şablonuna göre final dosyası hazırlanırken aşağıdaki bölümler kontrol edilmeli:

1. Proje adı
2. İçindekiler
3. Giriş — problem, araştırma sorusu, hipotez, hedefli literatür değerlendirmesi ve çalışmanın benzer işlerden ayrılan yönü
4. Yöntem — veri seçimi, vaka kabul ölçütleri, E1/E2/E3 kanıt seviyeleri, P0/P1 koşulları, sabit model ve runtime, kör puanlama, dışlamalar ve analiz planı
5. Bulgular — gerçekten yürütülen koşullar, örneklem sayıları, ham/adjudike ölçümler, başarısız/uygunsuz çıktılar ve önceden belirlenmiş istatistiksel analiz
6. Sonuç ve tartışma — araştırma sorusuna yanıt, önceki çalışmalarla karşılaştırma, belirsizlikler, sınırlılıklar ve hipotezin desteklenip desteklenmediği
7. Öneriler — uygulanabilir sonuçlar ve gelecek araştırma adımları
8. Kaynakça — güncel rehberdeki kaynak yazım kurallarına uygun

Tablo, grafik ve şekiller numaralandırılmalı, açıklanmalı ve ana metinde açıkça anılmalı.

## Bu çalışma için alan seçimi

- **Ana alan adayı:** Yazılım.
- **Tematik alan adayı:** Yapay Zekâ.
- Bu tercih, projenin amacıyla son kez karşılaştırılmalı; TYBS'ye başvurudan sonra alan değişikliği yapılamadığı için otomatik varsayım olarak bırakılmamalı.

## Bu çalışma için bilimsel içerik kapıları

- [ ] En az 60 bağımsız ve kabul edilmiş hata vakası; hedef 80.
- [ ] En az 8 ayrı upstream yazılım projesi.
- [ ] Her vaka için doğru sürümlerde buggy-fail / fixed-pass test çifti ve hash'lenmiş kayıtlar.
- [ ] Kalıcı maruziyet dışlamaları uygulanmış ve denetlenmiş.
- [ ] Kök neden puanlaması için iki bağımsız değerlendirici.
- [ ] Kanıt yeterliliği için bu ilk panelden ayrı iki bağımsız ve kör değerlendirici.
- [ ] Ana çalışma protokolü, analiz planı ve gerekli artefakt hash'leri sonuçlardan önce dondurulmuş.
- [ ] Gerçek Qwen/tokenizer/GPU çalışma ortamı doğrulanmış.
- [ ] Protokolün denetlenebilir ön kaydı ve ayrı yürütme izni mevcut.
- [ ] Gerçek çıktı verisi ve kör/adjudike puanlar üretilmiş.
- [ ] Analiz, veri temelli olarak tekrar üretilebilir biçimde tamamlanmış.

## Yasaklı raporlama kestirmeleri

- Metadata adayı sayısını kabul edilmiş deney vakası diye raporlamak.
- Sentetik test sonuçlarını LLM performans sonucu olarak sunmak.
- Modelin kendi beyan ettiği güven değerini kalibre edilmiş olasılık diye adlandırmak.
- Daha önce maruz kalınmış/debug edilmiş vakaları doğrulayıcı örnekleme geri almak.
- Deney başlamadıysa “hipotez doğrulandı”, “halüsinasyon azaldı” veya “sistem başarıyla doğrulandı” demek.
- Sonuçları gördükten sonra birincil ölçütü, dışlamaları veya örneklem eşiğini sessizce değiştirmek.

## Mevcut durum — 23 Ekim 2026

Bu kontrol listesi oluşturulurken doğrulayıcı vaka sicilinde 0 kabul edilmiş vaka, bu çalışma için 0 doğrulayıcı model çıktısı ve 0 kalibrasyon gözlemi bulunuyordu. V10 listesi metadata-only 100 adaydır; uzak CI/runner sonucu halen doğrulanmamıştı. Bu dosya sadece başvuruya giden sonlandırma ölçütlerini listeler; proje tamamlanmış sayılmaz.

## Rehberin dayanak noktaları

- Resmî yarışma sayfası: başvuru şartları, tamamlama şartı, son tarih, başvuru alanları ve şablon bağlantısı.
- 2027 Proje Rehberi, “3.3. Proje Raporu Nasıl Yazılır?”: başlık, özet, giriş, yöntem, bulgular, sonuç/tartışma ve kaynakça.
- 2027 Proje Rehberi, “3.6.12. Yazılım Projelerinde Dikkat Edilmesi Gereken Önemli Noktalar”: bilimsel yöntem, ölçülebilir veri ve analiz, özgünlük, uygulanabilirlik ve raporlanabilirlik.
