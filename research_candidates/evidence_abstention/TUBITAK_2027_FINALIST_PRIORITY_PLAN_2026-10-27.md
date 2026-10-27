# TÜBİTAK 2204-A 2027 finalist hedefli yürütme planı

**Son güncelleme:** 27 Ekim 2026  
**Tek hedef:** Bu araştırmayı 2027 TÜBİTAK 2204-A başvurusu için tamamlanmış, tekrarlanabilir ve jüri önünde savunulabilir hâle getirmek. Finalistlik hedefi çalışma önceliğidir; sonuç garanti edilemez.

## Resmî çerçeve

- Çağrı sayfası ve takvim: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
- 2027 proje rehberi: https://tubitak.gov.tr/sites/default/files/2026-10/2204A_proje_rehberi_2027.pdf
- Başvuru kapanışı: **4 Ocak 2027, saat 17.30 (Türkiye saati)**. Başvuru için proje tamamlanmış olmalıdır; yalnızca fikir veya devam eden bir prototip yeterli değildir.
- 2027 rehberi Yazılım Projeleri bölümünde bilimsel yöntem, uygun veri toplama ve analiz, detaylı literatür, sonuçların tartışılması ve ürünün yanında yazılım geliştirme sürecinden çıkan bulguların önemini vurgular. Yalnızca bir arayüz yapmak araştırmanın bilimsel katkısını tek başına karşılamaz.
- TÜBİTAK sayfasının şu anda bağladığı değerlendirme formları ön değerlendirmede problem/soru %20, yöntem %20, yaratıcılık/etki %30, sonuçlar/tartışma %30; bölge/finalde ise sırasıyla %15, %10, %15, %20 ve sunum/projeye hâkimiyet %40 ağırlıklarını gösteriyor. Son başvuru öncesinde sayfada daha yeni form yayımlanıp yayımlanmadığı tekrar kontrol edilmelidir.

## Araştırma kimliği

**Rapor başlığı adayı:** Yazılım Hata Teşhisinde Kanıt Yeterliliğinin Büyük Dil Modellerinin Cevap Vermekten Kaçınma Davranışına Etkisi

**Ana alan:** Yazılım.  
**Önerilen tematik alan:** Yapay Zekâ. Bu eşleştirme, 2027 rehberinde bulunan tematik alanlar ve projenin nihai amacı üzerinden başvuru öncesinde son kez doğrulanmalıdır.

**Araştırma sorusu:** Gerçek açık kaynak yazılım kusurlarında, kanıt yetersiz olduğunda kaçınmaya izin veren P1 politikası, teşhisi zorunlu kılan P0 politikasına kıyasla E3/yetersiz kanıt altında kanıtla desteklenmeyen kesin kök neden teşhislerini azaltıyor mu? Bu olası azalmanın yanıt kapsamı ve E1'deki gereksiz kaçınma maliyeti nedir?

Bu bir model üretme yarışması veya marka tanıtımı değildir. Önceden eğitilmiş bir dil modeli yalnızca araştırma aracı olarak kullanılır. Projenin bilimsel katkısı, kontrollü kanıt paketleri, bağımsız değerlendirme, önceden belirlenmiş ölçüt ve gerçek bulgulardır. Genel abstention fikrinin yeni olduğu ya da bu protokolün alanında ilk olduğu iddia edilmeyecektir.

## Deney tasarımı — korunacak ana çerçeve

- Her bağımsız kusur için E1/yeterli, E2/kısmi ve E3/yetersiz kanıt paketleri; her paket için P0 ve P1 politikası: toplam altı hücre.
- Hedef 80 bağımsız vaka/8'den fazla upstream proje; asgari doğrulayıcı eşik 60 bağımsız vaka ve en az 8 proje. 60 vaka 360, 80 vaka 480 ham çıktı demektir; bunlar planlama sayılarıdır.
- Birincil sonlanım E3'te kanıtla desteklenmeyen kesin teşhis oranıdır. Eşleştirilmiş P0/P1 karşılaştırması, iki taraflı exact McNemar testi, risk farkı ve %95 güven aralığı ile raporlanır.
- Teşhisin gerçek kök nedenle doğru eşleşmesi, kanıtla desteklenmesi ve modelin kaçınma kararı farklı ölçülerdir. Doğru tahmin, paketteki kanıt yetersizse otomatik olarak destekli teşhis sayılmaz.
- Her vaka için aynı kayıtlı Python/runtime ortamında buggy revizyon hedef testte başarısız, fixed revizyon aynı hedef testte başarılı olmalıdır. Kurulum/ortam hatası geçerli vaka kanıtı değildir.
- Gold root cause paneli ile kanıt yeterliliği paneli ayrık olmalı. Kanıt puanlayıcıları gizli kök nedeni, düzeltme yamasını ve E1/E2/E3 etiketini görmemelidir. İlk bireysel puanlar, anlaşmazlıklar ve adjudication kayıtları korunmalıdır.
- Kalibrasyon vakaları ana örneklemden ayrı tutulmalı; ön kayıt ve hash dondurma gerçek model çıktıları görülmeden yapılmalıdır.

## Model ve prototip kapsamı

1. prototype/ altındaki Gradio arayüzü yalnızca tek örnek için keşifsel mühendislik demosudur. Bu arayüzdeki çıktı ana doğrulayıcı veri kümesine eklenmez.
2. Prototipin system prompt'u, P0/P1 politika metinleri, kanıt öğesi kimlikleri ve çıktı şeması Stage 3 araştırma sözleşmesiyle eşleştirildi. E1/E2/E3 etiketi prompt'a verilmez.
3. JSON/kanıt ID kontrolü semantik destek kanıtı değildir. Hatalı çıktı otomatik düzeltilmez; modelin kararını sonradan abstain'e çevirmek gibi bir post-processing ana deney ölçümüne eklenmez.
4. Araştırma çıktılarının resmi kaynağı sadece research_candidates/evidence_abstention/kaggle_stage3_p0_p1.py olacaktır. Ön kontrol ve çalışma manifesti açıkça izin vermeden doğrulayıcı inference başlatılamaz.
5. Bu kod düzenlemesinin ardından da gerçek model ağırlıklarının yüklenmesi, CUDA/runtime fingerprint'i ve canlı inference henüz doğrulanmış sayılmaz.

## 27 Ekim itibarıyla kesin durum

- Kabul edilmiş bağımsız doğrulayıcı vaka: **0**.
- Ana çalışmanın doğrulayıcı model çıktısı: **0**.
- Kalibrasyon verisi ve doğrulanabilir ön kayıt: tamamlanmadı.
- Tam model/tokenizer/CUDA runtime doğrulaması: tamamlanmadı.
- Ana deney manifestinde inference izni kapalı, dataset gate açık ve vaka sicili boş kalmalıdır.

Bu yüzden bugün halüsinasyonun azaldığı, P1'in daha iyi olduğu veya hipotezin doğrulandığı söylenemez. Bu ifadeler ancak önceden belirlenen analiz ve bağımsız puanlamadan sonra kullanılabilir.

## İş paketleri ve karar noktaları

| Dönem | İş paketi | Çıkış koşulu |
|---|---|---|
| 27–31 Ekim | Prompt/şema uyumunu koru; prototipin saf mantık testlerini hazırla; ana deney kapısını kapalı tut. | Testler için gözlenebilir ve tekrar çalıştırılabilir kayıt; üretim prompt'u ile sessiz sapma yok. |
| 28 Ekim–7 Kasım | Maruz kalınmamış hata adaylarını, lisansları ve kaynak/buggy/fixed hedef testlerini doğrula; iki ayrık insan panelini kesinleştir. | Kabul kriterlerini geçebilecek vaka havuzu ve panel iş akışı somut kanıtlarla görülür. |
| 7 Kasım karar noktası | En az 60 vaka/8 proje yolunda gerçekçi hız olup olmadığını sayıyla değerlendir. | Hedef yakalanamıyorsa sonuç görüldükten sonra kapı gevşetilmez; inference öncesinde protokol değişikliği ve yeni etiketleme/ön kayıt yapılarak çalışma keşifsel fizibilite projesi olarak yeniden tasarlanabilir. Bu, doğrulayıcı iddia hakkı vermez. |
| 8–21 Kasım | Vaka kabulü, üç iç içe kanıt paketi, panel kalibrasyonu, ön kayıt ve hash dondurma. | Tüm kapılar kapanmadan model çalıştırılmaz. |
| 22 Kasım–7 Aralık | Yalnızca kapılar kapanırsa, sabit model/runtime ile ana 6-hücreli deney. | Ham çıktı, sıra, prompt/packet/output hash'i ve runtime kayıtları eksiksiz. |
| 8–20 Aralık | Kör puanlama, anlaşma/adjudication, exact McNemar, risk farkı ve güven aralıkları. | Analiz kodu, ham puan ve sonuç tablosu bağımsız olarak denetlenebilir. |
| 21–28 Aralık | Sonuçlara dayanan rapor, sınırlılıklar, literatür karşılaştırması ve şekiller. | Amaç-yöntem-bulgular-sonuç bölümleri birbiriyle tutarlı; negatif/kararsız sonuçlar da dürüstçe raporlu. |
| 29 Aralık–3 Ocak | Öğrenci sunum/poster provası; proje rehberi ve güncel şablonla son kontrol; başvuru sistemine yükleme. | Her iddia ve sayı kaynak ham kayıtla eşleşir; başvuru 4 Ocak 17.30'dan önce tamamlanır. |

Bu takvim agresiftir ve başarı garantisi değildir. En önemli risk, kabul edilmiş vaka sayısının hâlâ sıfır olmasıdır. Takvim sıkıştığı için kalite, bağımsızlık, lisans veya maruziyet kuralları gevşetilmeyecektir.

## TÜBİTAK odaklı son kontrol

- Problem/soru: problem, hipotez, amaç ve birincil ölçüt tek paragrafta anlaşılır.
- Yöntem: örneklem birimi, dışlamalar, E1/E2/E3, P0/P1, körleme, analiz ve geçersiz çıktı kuralları yeniden üretilebilir biçimde belgeli.
- Yaratıcılık/etki: yakın literatürle fark dar ve kaynaklı; bir ürün arayüzü tek başına özgün katkı sayılmıyor.
- Sonuç/tartışma: yalnızca gerçek ham kayıtlarla desteklenen bulgular; belirsizlik, sınırlılıklar ve geçerlilik tehditleri açık.
- Sunum/hâkimiyet: öğrenci model kodunu, prompt eşlemesini, vaka kabulünü, kör puanlamayı ve istatistiği kendisi açıklayabilmeli; danışman/uzman desteği öğrencinin kendi katkısının yerine geçmemeli.
- Etik/bütünlük: kaynaklar atıflı; lisanslar kayıtlı; önceki maruziyet dışlamaları korunmuş; eski DİJİTALİKİZ/CCDG sonuçları bu çalışmanın verisi olarak kullanılmıyor.

## Resmî kaynaklar

1. TÜBİTAK 2204-A 2026–2027 çağrısı ve başvuru takvimi: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
2. TÜBİTAK 2027 Proje Rehberi, özellikle 1.2 Tematik Alanlar ve 3.6.12 Yazılım Projeleri: https://tubitak.gov.tr/sites/default/files/2026-10/2204A_proje_rehberi_2027.pdf
3. Resmî sayfanın şu anda bağladığı ön değerlendirme formu: https://tubitak.gov.tr/sites/default/files/2025-11/on_degerlendirme_kriterleri_2025_web.pdf
4. Resmî sayfanın şu anda bağladığı bölge/final formu: https://tubitak.gov.tr/sites/default/files/2025-11/sergi_kriterleri_2025_web.pdf
