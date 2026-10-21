# TÜBİTAK 2204-A ön değerlendirme ve bölge/final kontrol listesi

**Kontrol tarihi:** 21 Ekim 2026  
**Tek hedef:** 2027 TÜBİTAK 2204-A’da finalistlik düzeyinde tamamlanmış araştırma sunmak.  
**Resmî referans:** [TÜBİTAK 2204-A yarışma sayfası](https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi) — bu sayfanın bağladığı [ön değerlendirme formu PDF'si](https://tubitak.gov.tr/sites/default/files/2025-11/on_degerlendirme_kriterleri_2025_web.pdf).

**Ön değerlendirme formu** ağırlıkları: problem/araştırma sorusu %20, yöntem %20, yaratıcılık/etki %30, sonuçlar/tartışma %30. **Bölge/final aşaması formunda** ağırlıklar farklıdır: problem/araştırma sorusu %15, yöntem %10, yaratıcılık/etki %15, sonuçlar/tartışma %20, sunum ve projeye hâkimiyet %40. Bu sayılar başarı tahmini değildir; her aşamanın gerekliliklerini ayrı denetlemek için kullanılır.

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


## 6. Bölge / final değerlendirmesi — ayrı ölçütler

Resmî [Bölge/Final Aşaması Değerlendirme Formu](https://tubitak.gov.tr/sites/default/files/2025-11/sergi_kriterleri_2025_web.pdf), sunum ve projeye hâkimiyet bölümüne toplam ağırlığın **%40'ını** verir. Finalistlik hedefinde yazılı rapor tek başına yeterli bir hazırlık planı değildir.

### Problem / ihtiyaç ve araştırma sorusu — %15
- [ ] Araştırma sorusu, amaç ve ölçülebilir hedefler kısa ve tutarlı biçimde açıklanabiliyor.
- [ ] Çalışmanın ana alanı ve problem seçimi gerekçelendirilebiliyor.

### Yöntem — %10
- [ ] E1/E2/E3 ve P0/P1 koşulları, vaka seçimi ve bağımsızlık birimi örneksiz değil, somut bir vaka üzerinden açıklanabiliyor.
- [ ] Birincil ölçütün neden “kanıtla desteklenmeyen kesin teşhis” olduğu ve gerçek kök neden doğruluğundan neden ayrı tutulduğu savunulabiliyor.

### Yaratıcılık ve etki — %15
- [ ] Yakın literatürdeki çalışmalar ile bu araştırmanın farkı, kaynaklarla birlikte ve abartısız biçimde savunulabiliyor.
- [ ] Olası etki, yalnızca ölçülmüş bulgulara ve makul uygulamalara dayandırılıyor.

### Sonuçlar ve tartışma — %20
- [ ] Ana sonuç ve belirsizlik/CI, gerçek veriden hesaplanıp tekrar üretilebiliyor.
- [ ] Çelişkili, olumsuz veya istatistiksel olarak belirsiz bulgular saklanmıyor.
- [ ] Sonuçların hangi bağlamlara genellenemeyeceği açıklanabiliyor.

### Sunum ve projeye hâkimiyet — %40
- [ ] Öğrencinin projeyi gerçekten kendisinin şekillendirdiği ve gerçekleştirdiği, karar kayıtları ve açıklamayla gösterilebiliyor.
- [ ] Model, veri kaynağı, kanıt paketleri, puanlama, istatistik ve temel kodun işleyişi jüriye sözlü olarak anlatılabiliyor.
- [ ] Neden bu model/veri/ölçüt seçildiği; alternatiflerin ve başarısız denemelerin neden dışlandığı açıklanabiliyor.
- [ ] Sunum/poster, rapordaki yöntem ve gerçek sonuçlarla birebir uyumlu.
- [ ] Jüri sorularına cevap verirken ölçülmemiş iddia, yanlış kesinlik veya sonuçları olduğundan büyük gösterme yapılmıyor.

## 7. Etik ve bilimsel bütünlük — eleme riski

Resmî formlar veri bütünlüğü ihlali (uydurma/çarpıtma), kaynak göstermeme, gerekli izin belgelerinin eksikliği, kişisel veri gizliliği ihlali ve projenin öğrenci tarafından geliştirilmediğinin tespiti gibi durumlarda elenme riskini açıkça belirtir. Bu nedenle:
- [ ] Kullanılan her kaynak uygun biçimde atıflandırıldı.
- [ ] Her veri/çıktı için köken ve bütünlük kayıtları tutuldu.
- [ ] Öğrencinin katkısı, öğretmen/danışman desteğinden ayrıştırılarak açıklandı.
- [ ] Gerekli olabilecek izinler ve rapor şablonu başvuru öncesi güncel rehberden doğrulandı.

## Güncel karar

Ön değerlendirme kontrolünün yanında, bölge/final aşamasında sunum ve projeye hâkimiyet hazırlığı da baştan plana dâhil edilmiştir. Bununla birlikte, gerçek vaka kümesi ve deney sonucu bulunmadığı için bu kutuların sonuçlar/tekrarlanabilirlik kısmı bugün kapatılamaz.
