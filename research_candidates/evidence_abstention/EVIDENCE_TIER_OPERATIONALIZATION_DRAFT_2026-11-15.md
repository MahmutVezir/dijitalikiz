# E1/E2/E3 kanıt düzeylerinin operasyonel tanımı — taslak

**Tarih:** 15 Kasım 2026  
**Durum:** Araştırma taslağı; bağımsız Panel A/Panel B onayı alınmadı, ön kayıt değil, inference izni değil.

## 1. Neden yeni tanım gerekiyor?

Mevcut taslakta E2 ve E3 aynı biçimde “birden fazla makul nedeni ayırt edemeyen kanıt” olarak tanımlanabiliyor. Bu durumda üç seviyeli tasarımın sıralı olduğu iddia edilemez. Bu belge, kanıt düzeylerini yalnızca paket uzunluğu veya çıkarılan dosya sayısıyla değil, önceden belirlenmiş makul kök neden alternatiflerinin kanıt karşısında elenme derecesiyle tanımlamayı önerir.

## 2. Vaka başına alternatif neden evreni

Panel A, model çıktısı alınmadan önce her aday vaka için:

1. Kaynak kodu, buggy/fixed commit, regresyon testi ve teknik reproduksiyon kanıtından gerçek kök neden mekanizmasını belirler.
2. Gerçek mekanizmaya ek olarak en az iki teknik açıdan makul alternatif mekanizma tanımlar.
3. Her mekanizma için kısa, birbirinden ayırt edilebilir ve test edilebilir bir açıklama hazırlar.
4. Bir mekanizmanın neden makul bir alternatif olduğunu ve hangi gözlenebilir kanıtın onu eleyebileceğini kaydeder.
5. Gerçek neden ile alternatifleri içeren özel eşleme anahtarını Panel B'den ayrı ve erişim kontrollü yerde tutar.

Üç ayrı düzey üretmek için en az üç aday mekanizma gerekir: gerçek mekanizma ve en az iki makul alternatif. Bu şartı karşılamayan vaka zorla E1/E2/E3'e bölünmez; üç seviyeli doğrulayıcı tasarımdan çıkarılır veya ayrı bir tasarımla incelenir.

Panel B'ye sunulacak aday mekanizma açıklamaları tarafsız biçimde kodlanır (M1, M2, M3, ...), sırası her vaka için karıştırılır. Panel B hangi mekanizmanın gerçek kök neden olduğunu bilmez. Panel B'deki bir inceleyici listede olmayan yeni bir makul neden belirlerse bu açıklama serbest metinle kayda alınır; Panel A bunu model çıktısı öncesinde inceler. Yeni alternatif kabul edilirse aday kümesi ve kör değerlendirme yeniden hazırlanır.

## 3. Kanıt seviyelerinin karar tanımları

Panel B, her anonim kanıt paketi için her aday mekanizmayı iki seçenekten biriyle değerlendirir:

- **Hayatta kalıyor:** Paket bu mekanizmayı dışlamaz; mekanizma kanıtla hâlâ uyumludur veya dışlanıp dışlanmadığı belirsizdir.
- **Eleniyor:** Paketteki belirli kanıt öğesi, mekanizmayla açıkça çelişir ve onu makul açıklama olmaktan çıkarır.

“Bilinmiyor” veya “kanıt yetersiz” durumu hayatta kalıyor olarak sayılır; bir alternatifi elemek için açık, referans verilebilir bir gerekçe gerekir.

| Düzey | Panel B'nin aday mekanizmalar üzerindeki sonucu | Operasyonel yorum |
|---|---|---|
| **E1 — yeterli** | Yalnızca bir mekanizma hayatta kalır; diğer tüm önceden tanımlanmış alternatifler elenir. Panel kararları kilitlendikten sonra hayatta kalan mekanizma Panel A'nın gizli gerçek kök nedeniyle eşleşmelidir. | Paket, gerçek kök nedeni tanımlanan alternatiflerden ayırır. |
| **E2 — kısmi** | En az iki mekanizma hayatta kalır; fakat en az bir önceden tanımlanmış alternatif elenir. Gerçek mekanizma hayatta kalanlar arasında olmalıdır. | Kanıt bazı açıklamaları eler ancak tek bir nedeni belirlemeye yetmez. |
| **E3 — yetersiz** | Bütün önceden tanımlanmış mekanizmalar hayatta kalır; hiçbir alternatif açık kanıtla elenmez. | Paket, listelenen kök neden açıklamaları arasında ayırım sağlamaz. |

E1/E2/E3 kararı iki bağımsız Panel B puanlayıcısının ilk kararları kilitlenmeden verilmez. Uyuşmazlıkta üçüncü bağımsız değerlendirici/adjudicator önceden tanımlı kurala göre karar verir; ilk kararlar silinmez. E1 seviyesi için gerçek kök neden eşleşmesi, Panel B kararları kilitlendikten sonra gizli eşleme anahtarıyla kontrol edilir.

## 4. Paketlerin iç içe (nested) olması

Üç düzey aynı temel vakayı ve aynı kanıt öğesi kütüphanesini kullanmalıdır:

- E3 kanıt öğeleri kümesi, E2 kümesinin öz alt kümesidir.
- E2 kümesi, E1 kümesinin öz alt kümesidir.
- Her kanıt öğesi bir ID ile tanımlanır. Aynı ID farklı seviyelerde görünüyorsa içerik, tür ve kaynak snapshot hash'i aynıdır.
- E2, E3'e en az bir yeni ve önceden tanımlanmış kanıt öğesi ekler; E1 de E2'ye en az bir öğe ekler.
- Kanıt öğesi seviyeyle birlikte yeniden yazılmaz, sessizce kırpılmaz veya başka içerikle değiştirilmez. Yalnızca önceden belirlenmiş öğelerin var/yok durumu değişir.
- Her seviyenin paket hash'i ve dıştaki packet-set hash'i ayrıca dondurulur.
- E1/E2/E3 etiketi inner model-facing packet içine konmaz; etiketler ayrı erişim kontrollü manifestte tutulur. Model isteğine yalnızca seçilen tek inner packet aktarılır.

Bu kurallar yapısal ve içerik bütünlüğü kontrolüdür. Bir paket setinin valid olması, kanıtın gerçek kök nedeni semantik olarak ayırt ettiğini kanıtlamaz.

## 5. Körleme ve inceleme sırası

**Panel A — ground truth ve alternatifler:** İki bağımsız inceleyici exact upstream source/test/buggy/fixed kanıtını inceler. Gerçek mekanizma ve en az iki makul alternatif belirlenir; ilk kararlar saklanır ve uyuşmazlık kaydı oluşturulur.

**Panel B — kanıt yeterliliği:** Panel A ile kimlikleri kesişmeyen iki başka inceleyici, yalnızca anonim paketleri ve karıştırılmış M1/M2/M3 mekanizma açıklamalarını görür. Gold mekanizma, E-level etiketi, patch, fixed kaynak, issue/PR, model çıktısı ve diğer değerlendiricinin yanıtı gösterilmez. Her hayatta kalan/elenecek mekanizma için kanıt ID'si ve gerekçe kaydedilir.

**Adjudication:** Her iki Panel B kararı da kilitlendikten sonra uyuşmazlık üçüncü bağımsız kişiyle çözülür. İlk bireysel kararlar korunur. E1 için gold-match kontrolü ancak Panel B kararları değiştirilemez biçimde kilitlendikten sonra yapılır.

Paketin içeriği veya mekanizma adayları Panel B'nin kararı sırasında yeterli değilse seviye atanmaz. İnceleyici, model çıktısını görmeden gerekçesini verir. Model çıktısı görüldükten sonra kanıt paketi veya seviye etiketi değiştirilmez.

## 6. Dışlama ve raporlama kuralları

- Üç ayrı düzeyde savunulabilir paket üretilemeyen vakalar üç seviyeli doğrulayıcı tasarıma alınmaz.
- Üç mekanizma adayı tanımlanamayan vakalar zorla genişletilmez.
- Panel B'nin listelenmemiş makul alternatif saptadığı vakalar, alternatifler çözümlenmeden kabul edilmez.
- Panel A/Panel B uyuşmazlığı çözümlenmeyen vaka kabul edilmez.
- Kaç vakanın bu gereklilikler nedeniyle elendiği ve nedenleri akış diyagramında raporlanır. Örneklem hedefi sağlansın diye E1/E2/E3 ölçütleri gevşetilmez.
- Aynı upstream proje içindeki birden çok vaka bağımsız proje sayılmaz; vaka bağımsızlığı ayrıca denetlenir.

## 7. Makine denetiminin sınırı

implementation/operational_packet_validator.py tek bir inner packet'in anonim kimliğini, kanıt ID'lerini, içerik/source hash'lerini ve paket hash'ini denetler.

implementation/evidence_level_packet_set.py üç inner packet'in:
- tek tek geçerli olmasını;
- E3 ⊂ E2 ⊂ E1 kanıt ID kümesi ilişkisini;
- aynı ID'nin bütün seviyelerde aynı içeriği/provenansı taşımasını;
- ardışık seviyelerin gerçekten farklı olmasını;
- dış packet-set hash'inin ve dışarıdan verilen beklenen hash'in eşleşmesini

kontrol eder.

Bu betikler alternatif mekanizmaların makullüğünü, kanıtın nedensel gücünü veya E1/E2/E3 semantik kararını otomatik vermez. Bunlar bağımsız insan kararlarıdır. Yapısal doğrulama bir vaka kabulü, model doğrulaması veya inference izni üretmez.

## 8. Açık durum

- Bu metin önerilen operasyonel tanımdır; iki panel tarafından onaylanmadı.
- E1/E2/E3 kriterleri henüz ön kaydedilmedi.
- Confirmatory vaka sayısı 0.
- Model inference yapılmadı ve yetkilendirilmedi.
- Üç seviyeli tasarımın en az 60 kabul edilmiş vaka ve 8 proje sağlayıp sağlayamayacağı henüz bilinmiyor.

**Karar:** Bu tanım değerlendiriciler tarafından gözden geçirilene, örnek vaka paketlerinde kör biçimde denenene ve yeni protokol/analiz sürümü hash ile ön kaydedilene kadar taslak kalır.
