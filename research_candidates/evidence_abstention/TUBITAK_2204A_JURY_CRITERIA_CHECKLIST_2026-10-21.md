# TÜBİTAK 2204-A jüri ön değerlendirme kontrol listesi

**Kontrol tarihi:** 21 Ekim 2026  
**Tek hedef:** 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde tamamlanmış araştırma sunmak.  
**Resmî referans:** [TÜBİTAK 2204-A yarışma sayfası](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi) — bu sayfanın bağladığı [ön değerlendirme formu PDF'si](https://tubitak.gov.tr/sites/default/files/2025-11/on_degerlendirme_kriterleri_2025_web.pdf).

Formun gösterdiği önem ağırlıkları: problem/araştırma sorusu %20, yöntem %20, yaratıcılık/etki %30, sonuçlar/tartışma %30. Bu sayılar başarı tahmini değildir; çalışmayı denetlemek için kontrol yapısıdır.

## 1. Problem / ihtiyaç ve araştırma sorusu — %20

- [x] Ana soru açık: E3 yetersiz kanıt koşulunda seçici kaçınma, zorunlu teşhise göre desteklenmeyen kesin teşhisi azaltıyor mu?
- [x] Gözlenebilir hedef/ölçüt taslakta tanımlı: E3 altında unsupported definitive diagnosis farkı.
- [ ] Alan seçimi ve tema, güncel rehberdeki tanımlarla uyum açısından danışmanla son kez kontrol edilecek.
- [ ] Araştırma ihtiyacı, yakın literatürle açıkça karşılaştırılacak; genel LLM abstention fikrinin yeni olduğu iddia edilmeyecek.
- [ ] Amaç, alt hedefler ve değerlendirme ölçütleri nihai raporda birebir eşleşecek.

**Durum:** Araştırma sorusu ve ölçüt taslağı var; özgünlük gerekçesinin son denetimi ve alan eşlemesi kapanmadı.

## 2. Yöntem — %20

- [x] E1/E2/E3 kanıt seviyesi × P0/P1 politika düzeni belgeli.
- [x] Birincil vaka düzeyi ölçütü, eşleştirilmiş analiz yaklaşımı ve geçersiz çıktı ilkeleri taslakta.
- [x] Fail-closed, read-only no-inference readiness denetimi mevcut.
- [ ] En az 60 bağımsız vaka ve 8 proje (hedef 80) kabul koşullarını geçmeli.
- [ ] Her vaka exact kayıtlı ortamda buggy-fail/fixed-pass olmalı; hata ortam/kurulum kaynaklı olmamalı.
- [ ] Gold root cause ve E1/E2/E3 paketleri model çıktılarından önce iki bağımsız değerlendirmeyle doğrulanmalı.
- [ ] Değerlendirici rubriği dondurulmalı, kalibrasyon tamamlanmalı ve kalibrasyon vakaları ana örneklemden dışlanmalı.
- [ ] Model/tokenizer/runtime fingerprint'i doğrulanmalı; analiz, istem, şema, rubrik, runtime ve vaka manifesti hash'leri dondurulmalı.
- [ ] Protokol doğrulanabilir biçimde önceden kaydedilmeli; ancak bundan sonra çıkarım izni ayrıca incelenmeli.

**Durum:** Tasarım belgeleri var; deney yürütmeye hazır değil.

## 3. Yaratıcılık ve etki — %30

- [x] Çalışmanın katkı iddiası sınırlı tanımlı: yazılım hata teşhisinde kontrollü kanıt yetersizliği ve seçici kaçınma karşılaştırması.
- [x] Bilinen önceki abstention araştırmalarının bulunduğu açıkça yazıldı.
- [ ] Hedefli literatür taraması, yakın yöntem ve görevleri; veri, kanıt manipülasyonu, birincil ölçüt ve değerlendirme farklarıyla karşılaştırmalı tabloya dönüştürülecek.
- [ ] Katkı “ilk/benzersiz model” değil; kontrollü değerlendirme yöntemi ve ölçülebilir güvenilirlik sorununa ilişkin deneysel bulgu olarak savunulacak.
- [ ] Gerçek etki, güvenilmez kesin teşhislerin önlenmesi ve gerekli kanıt talebinin niteliği üzerinden açıklanacak; ölçülmemiş toplumsal fayda gerçekleşmiş sonuç diye sunulmayacak.
- [ ] Sonucun desteklediği en dar iddia seçilecek; model, görev veya veri alanı dışına genelleme sınırları yazılacak.

**Durum:** Savunulabilir aday katkı var; yakın literatür karşılaştırması ve gerçek sonuçlara dayalı etki tartışması tamamlanmadı.

## 4. Sonuçlar ve tartışma — %30

- [ ] En az kabul eşiğini geçen vaka kümesi ve tüm kabul/dışlama akışı raporlanmalı.
- [ ] Gerçek model çıktıları, bozuk/eksik sonuçlar ve ham kayıt hash'leri korunmalı.
- [ ] İki bağımsız puanlayıcının ilk puanları, anlaşma ve adjudication sonuçları saklanmalı.
- [ ] Birincil endpoint, McNemar testi, risk farkı ve %95 güven aralığı gerçek veriden hesaplanmalı.
- [ ] E1'de gereksiz kaçınma, cevap kapsamı ve kök neden doğruluğu ikincil sonuçlar olarak ayrı raporlanmalı.
- [ ] Sonuçlar hipoteze uymasa bile değiştirilmeden verilmeli; belirsizlik ve sınırlılıklar tartışılmalı.
- [ ] Deney/analiz ikinci bir kişi tarafından, sabitlenmiş kayıtlar üzerinden yeniden kontrol edilmeli.
- [ ] Nihai rapor resmî yazım şablonuna uygun ve başvuruya hazır hâle getirilmeli.

**Durum:** Deney yapılmadı; sonuç bölümü henüz yok. Buraya özet istatistik, grafik veya model performansı uydurularak eklenmeyecek.

## 5. Veri bütünlüğü ve elenme riski

- [ ] Bütün kaynaklar atıflandırılmalı ve lisans şartları kontrol edilmeli.
- [ ] Hiçbir vaka, model çıktısı gördükten sonra avantajlı olacak şekilde kabul edilmeyecek/dışlanmayacak.
- [ ] Eski DİJİTALİKİZ pilot/confirmatory/kalibrasyon kayıtları yeni projenin sonucu veya örneklemi olarak kullanılmayacak.
- [ ] Model adı/markası proje adında veya rapor kapağında tanıtım amacıyla öne çıkarılmayacak.
- [ ] İnsan değerlendirmesi için gerekli etik/izin/onam koşulları resmî rehber ve danışmanla kontrol edilecek.
- [ ] Proje ekibinin katkısı açıkça tanımlanacak; başvuru yalnızca tamamlanmış ve öğrenci tarafından şekillendirilmiş çalışmanın gerçek durumunu yansıtacak.

## Bugünkü karar

**Proje jüriye hazır değil.** Özellikle %30 ağırlıklı sonuçlar/tartışma bölümü gerçek verisiz tamamlanamaz. Öncelik, doküman görünümünü güzelleştirmek değil; vaka kapısını, değerlendirme kalitesini ve gerçek deney sonuçlarını kanıtla kapatmaktır. Başvurunun tamamlanmış proje gerektirdiğini belirten güncel [TÜBİTAK çağrı sayfası](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi) takip edilmelidir.
