# Tarihsel Deneyin Bilimsel Hata Denetimi — 15 Ekim 2026

## Denetim kapsamı

Bu denetim, dondurulmuş tarihsel deneyin bağlam oluşturucularını, puanlayıcı kodunu, aktif vaka manifestini, ham arşivdeki vaka kanıtlarını ve doğrulama durumunu inceler. **Yeni model çıkarımı yapılmadı; ham çıktılar, tarihsel manifest, prompt hash'leri veya doğrulayıcı sonuçlar değiştirilmedi.** Bu dosya sonradan yapılan bir yöntem denetimidir; bağımsız hakem değerlendirmesi veya yeni bir doğrulayıcı sonuç değildir.

## Yönetici sonucu

Tarihsel çalışma kodu çalışmış ve 160 çıktı üretmiştir; ancak mevcut veriyle “CCDG gösteriminin bağımsız nedensel etkisi” hakkında güvenilir bir etki iddiası yapılamaz. Bunun iki temel nedeni vardır:

1. **Bilgi-paritesi kusuru:** tarihsel Standard Context açık hata açıklamasını içerirken CCDG Context aynı alanı sunmaz ve bunun yerine bağımlılık kenarları ekler. Dolayısıyla bilgi içeriği ile temsil biçimi birlikte değişir.
2. **Ölçüm geçerliliği kusuru:** birincil skor semantik muhakemeyi değil, kök-neden alias'ının normalize edildikten sonra açıklamada bitişik bir ifade olarak bulunmasını ölçer. Doğru parafrazlar kaçabilir; olumsuzlanan veya alternatifler arasında yalnızca anılan alias ise yanlış geçiş üretebilir.

Bunlar yalnızca yazılım hatası değildir. İlk sorun deney tasarımı/construct validity, ikinci sorun ölçüm aracının geçerliliği problemidir. Tarihsel sıfır başarı sonucu bu nedenlerle hipotezi çözümlememiştir.

## 1. Kanıtlanmış tarihsel sonuçlar — değiştirilmeden korunacak

- Pilot: 40 inference kaydı.
- Dondurulmuş doğrulayıcı deney: 16 bağımsız vaka × 2 koşul × 5 tohum = 160 çıktı.
- Standard Context: 0/80 alias geçişi.
- CCDG Context: 0/80 alias geçişi.
- Vaka düzeyinde çoğunluk kuralı (5 çıktının en az 3'ü): her iki koşulda 0/16.
- Exact iki taraflı McNemar: p = 1,00; uyumsuz vaka çifti yok.
- Eşleştirilmiş risk farkı: 0,00; dondurulmuş analizde %95 aralık yaklaşık [-0,1936; 0,1936].
- Tarihsel arşiv: 212/212 manifest dosyası ve 160/160 deney kaydı SHA-256/boyut yönünden doğrulandı; parse hatası ve ham çıktı hash uyuşmazlığı yok.
- Arşiv SHA-256: e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd.

**Yorum:** p=1,00 eşdeğerlik kanıtı değildir. Her iki koşulda da başarının sıfır olması ve uyumsuz çift bulunmaması, testin bu ölçüm aracıyla koşullar arasındaki farkı ayırt edemediğini gösterir. “CCDG etkisizdir” sonucu çıkarılamaz.

Kaynak dosyalar: docs/CONFIRMATORY_RESULTS_2026-10-09.md, data/benchmark/confirmatory_result_summary.json ve tarihsel GitHub arşivi.

## 2. Deney tasarımı kusuru: koşullar aynı bilgiyi almıyor

dijitalikiz/context.py içindeki gerçek tarihsel oluşturucular:

- render_standard_context() şunları içerir: Source, Technology, Error description, I_base.
- render_ccdg_context() şunları içerir: Source, Technology, Dependencies (CCDG kenarları), I_base; açık Error description bölümü yoktur.

Bu, iki koşulun basitçe aynı olguları iki farklı biçimde gösterdiği anlamına gelmez. Standard koşul açık hata açıklamasını alırken CCDG koşulu kenar listesi ekler. Gerçek arşiv vaka kayıtlarında yapılan yeniden hesaplama 16/16 vakada aynı örüntüyü doğruladı: Standard'da hata açıklaması alanı var, CCDG'de yok; I_base ve kaynak/teknoloji bilgisi her iki bağlamda da aynı.

**Bilimsel etki:** koşullar arasındaki sonuç farkı olsaydı bile bunu grafik biçimine tek başına atfetmek mümkün olmayacaktı. Hiç fark görülmemiş olması da karıştırıcı değişkeni ortadan kaldırmaz.

**Düzeltme:** tarihsel çıktılara müdahale etme. Yeni bir çalışmada A/B/C koşullarında temel bağlam bayt düzeyinde aynı olmalı; B ve C aynı bağımlılık kenarlarının aynı kaynak, hedef, yön, ilişki türü ve açıklama ayrıntılarını içermeli. Yalnızca kenarların ifade biçimi B ile C arasında değişmeli. B–C birincil karşılaştırma olmalı.

## 3. Ölçüm aracı kusuru: literal alias, semantik doğruluk değildir

scripts/evaluate_confirmatory.py içindeki root_cause_alias_match() fonksiyonu root_cause_class ile explanation alanlarını birleştirir, küçük harfe ve alfanümerik sözcük dizisine normalize eder ve önceden belirlenmiş alias'lardan herhangi birini bitişik ifade olarak arar.

Bu davranış deterministik ve tekrar üretilebilir; fakat “modelin kök neden açıklaması anlamca doğru mu?” sorusunun tam karşılığı değildir.

| Durum | Eşleştiricinin olası davranışı | Ölçüm riski |
|---|---|---|
| Model doğru mekanizmayı parafraz eder, fakat alias ifadesini kullanmaz | Başarısız | Yanlış negatif |
| Model doğru ifadeyi “sebep bu değildir” diye olumsuzlar | Geçiş olabilir | Yanlış pozitif |
| Model birden fazla hipotez verir ve alias bunlardan birinde geçer | Geçiş olabilir | Yanlış pozitif |
| Model semptomu doğru anlatır ama nedensel mekanizmayı belirlemez | Alias'a bağlıdır | Kısmi doğruluğu ölçemez |

tests/test_scoring_matcher_characterization.py bu hata sınıflarını **sentetik** örneklerle sınar. Testler puanlayıcı davranışını tarif eder; gerçek model çıktılarında semantik doğruluk veya puanlayıcı duyarlılığı/özgüllüğü ölçmez. Gerçek insan hakemlerinin puanları henüz yoktur.

### Gerçek tarihsel çıktılardan dört inceleme adayı

160 kaydın arşivlenmiş, ayrıştırılmış çıktılarında; Standard koşulu, seed 42 için aşağıdaki dört yanıt dondurulmuş alias eşleştiricisinde **eşleşme üretmedi**. Özetlenen açıklamalar kök neden mekanizmasıyla anlamca uyumlu görünebilir; bu nedenle insan hakeminin incelemesi gereken olası yanlış-negatif örneklerdir. **Bunlar insan tarafından puanlanmış “doğru” yanıtlar değildir** ve burada gerçek semantik doğruluk sonucu olarak sayılmamalıdır.

| Vaka / kayıt | Modelin yanıtında açıklanan mekanizma | Literal alias sonucu | İnceleme neden gerekli? |
|---|---|---|---|
| MATH-305 / Standard / seed 42 | MathUtils.distance içindeki int biriktiricisinin kare farkları toplarken taşmaya yol açması | Eşleşme yok | Dondurulmuş ground truth, kareli uzaklık biriktiricisindeki tamsayı taşmasını tanımlar; yanıt bunu farklı sözcüklerle anlatır. |
| CLOSURE-14 / Standard / seed 42 | finally içinden geçen exception yolu ile normal fall-through ayrımının kaybolması ve ControlFlowGraph kenarlarının yanlış etiketlenmesi | Eşleşme yok | Ground truth, exception yolunun unconditional kenar olarak etiketlenmesini tanımlar; yanıt mekanizmayı anlatıyor gibi görünse de alias dizgesini kullanmaz. |
| MATH-393 / Standard / seed 42 | Çoklu başlangıç optimizer'ının kaydedilmiş en iyi optimum yerine sarılmış optimizer durumunu döndürmesi | Eşleşme yok | Yanıt, beklenen en iyi sonucun döndürülmemesini anlatır fakat sabit alias'la aynı metinsel ifade değildir. |
| TIME-12 / Standard / seed 42 | Calendar.ERA dikkate alınmadığı için BC tarih dönüşümlerinde yılın yanlış üretilmesi | Eşleşme yok | Yanıt kök neden ve etkiyi söyler; ayrıca “fix” ifadesi içerir. Bu, girdideki çözüm ipuçlarıyla etkileşim riskini de gösterir. |

Bu dört kayıt için tespit edilen şey **matcher'ın başarısız sınıflandırmasıdır**; modelin semantik olarak kesin doğru olduğu değil. Kör ve bağımsız iki insan değerlendirmesi, gerekçeler ve daha sonra kaynak-kod adjudication olmadan false-negative oranı, doğruluk, kappa veya CCDG lehine bir sonuç hesaplanamaz. Eski skor değişmez.

**Düzeltme:** tarihsel ölçüt değiştirilmeyecek. 160 çıktıya uygulanacak insan puanlaması sonradan yapılan keşifsel analiz olarak tutulacak. Yeni doğrulayıcı deneyde doğru/kısmen doğru/yanlış/değerlendirilemez rubriği bağımsız, kaynak kanıtları incelenmiş kalibrasyon vakalarında test edilip inference öncesinde dondurulmalı.

## 4. Girdi ipuçları ve kök nedenin bağlamdan tahmin edilebilirliği

Gerçek tarihsel vaka JSON'ları ayrıca incelendi. error_description alanları birçok vakada yalnızca semptomu değil, nedensel mekanizmayı da açıkça tarif eder. Bazı I_base maddeleri daha da ileri giderek “before the fix”, “the corrected …”, “the fix changes/removes/introduces …” gibi ifadeler içerir.

Dondurulmuş manifestteki 16 aktif vaka için tekrar üretilebilir sözcüksel tarama şu sonucu verdi:

- Açık hata açıklaması Standard bağlamda: 16/16; CCDG bağlamda: 0/16.
- I_base olguları her iki tarihsel bağlamda: 16/16 aynı.
- Tam ground_truth.root_cause veya dondurulmuş alias'lardan hiçbiri bağlam içinde tam literal ifade olarak bulunmadı. Bu, **anlamsal ipucu bulunmadığını göstermez**; yalnızca exact-phrase taramasıdır.
- I_base içinde “fix/fixed/corrected/before the fix” gibi açık düzeltme ifadesi bulunan vaka sayısı: 7/16.
- Daha geniş bir sözcüksel taramada previously, restoration, introduces, removes, changes, applies gibi çözüm yönlü ipuçları görülen vaka sayısı: 5/16; bunların bazıları bir önceki grupta da bulunur. Birleşik olarak en az 8/16 vakada bu taramanın işaretlediği bir düzeltme/iyileştirme ipucu bulunur.

Açık düzeltme ipuçlarına örnekler:

| Vaka | Bağlamdaki ifade | Neden önemlidir |
|---|---|---|
| CLOSURE-14 | I_base B4: “The fix changes the generated branch from UNCOND to ON_EX…” | Hem hedef mekanizmayı hem de doğru ve yanlış kenar etiketlerini doğrudan belirtir. |
| CLOSURE-4 | I_base B4: “The corrected cycle detector handles constructor interfaces as inheritance edges.” | Çözümün neyi düzelttiğini açıkça söyler. |
| CLOSURE-6 | I_base B4: “The fix removes obsolete constructor hacks…” | Doğru çözüm yönünü açıklar. |
| MATH-305 | I_base B3: “The int-array overload accumulated squared differences in an int before the fix.” | Hata mekanizmasının ana parçalarını doğrudan verir. |
| MATH-859 | I_base B4: “The fix aligns interface semantics and concrete implementation behavior.” | Hatanın hangi sözleşme tutarsızlığıyla ilgili olduğunu daraltır. |
| MATH-924 | I_base B4: “The fix introduces a diagonal matrix representation for vector weights.” | Alternatif çözümün biçimini açıklar. |
| TIME-12 | I_base B4: “The fix applies ISO proleptic-year conversion…” | Düzeltme yöntemini doğrudan belirtir. |

Bu, modelin eğitim verisinde bu vakaları gördüğünün kanıtı değildir. Buradaki sorun deney girdisinin görevi ne ölçüde cevapladığıdır. Tarihsel koşullarda I_base ortak olduğundan, bu ipuçları tek başına Standard–CCDG farkını açıklamaz; fakat deneyin daha geniş “kök neden teşhisi” görevini ölçme gücünü ve genellenebilirliğini sınırlar. Üstelik açık hata açıklamasının yalnızca Standard'a verilmesi, aynı ipuçlarının iki koşul arasında eşit biçimde sağlanmadığı anlamına gelir.

**Düzeltme:** eski girdileri sonradan düzeltme. V2 için vaka seçerken problem açıklamasını gözlenen belirti/sözleşme ihlali düzeyinde yaz; düzeltme commit'i, test adı, gold label, beklenen kök neden, “fix”, “corrected”, çözüm sonrası davranış ve testin hedeflediği özel kök neden bağlamdan çıkarılmalı. Bu kurallar otomatik sözcük taramasıyla yetinmemeli; iki bağımsız kişi kaynak kayıtlarını ve render edilmiş son promptları gözden geçirmeli.

## 5. Vaka ve veri envanteri

Manifest ve rubrik 16 vaka tanımlar. Tarihsel arşivde cases klasöründe 17 JSON dosyası vardır; commons-math-defects4j-MATH-844.json dosyası aktif manifest/rubrik listesinde değildir. Bu eski bir dışlama dosyasıdır, aktif 160 çıktılık örneklemin parçası değildir. Deney değerlendirmesi frozen manifestteki case ID'leri döngüye alır; dolayısıyla dosyanın klasörde bulunması tek başına modele gönderildiği anlamına gelmez. Bununla birlikte envanter raporunda aktif ve dışlanmış dosyaların açıkça ayrılması iyi uygulamadır.

Tüm 16 tarihsel vaka yüksek kamuya açık olma/contamination riski olarak etiketlenmiştir. Bu, eğitim kümesinde bulunduklarının kanıtı değildir. Kaynak revizyonları, düzeltme kanıtları ve vaka anotasyonları daha önce kayda alınmış olsa da bu denetim her dış projedeki kod geçmişini baştan bağımsız biçimde yeniden çalıştırmış değildir; ground-truth kalitesinin bağımsız kaynak doğrulaması hâlâ ayrı bir görevdir.

## 6. İstatistiksel birim ve örneklem yeterliliği

Beş seed aynı yazılım hatasının tekrarlı model çıktılarıdır; beş bağımsız hata gibi sayılmamaları doğru karardır. Tarihsel analiz istatistiksel birimi vaka olarak kullanmıştır.

Buna karşılık 16 vaka için kaydedilen tasarım gücü, Standard-only uyumsuzluk olasılığı 0,05 ve CCDG-only uyumsuzluk olasılığı 0,60 gibi çok büyük ve yönlü bir fark varsayımına bağlıydı. Bu sayılar önceden belirlenmiş tasarım varsayımlarıdır; gözlenen etki tahmini değildir. Böyle bir senaryoda 80% civarında güç hesaplanmış olması, daha ılımlı etkiler için yeterli gücü kanıtlamaz. Sonuç taban etkisi göstermiştir; tekrar sayısını artırmak bağımsız vaka sayısının yerini tutmaz.

V2 için mevcut 61 vaka/915 çıktı hedefi de yalnızca varsayılan uyumsuz çift olasılıkları altında yaklaşık 80% güç veren bir planlama senaryosudur; bu olasılıklar tarihsel sonuçlardan tahmin edilmemiştir. Yeterli, bağımsız, kaynakla doğrulanmış 61 vaka sağlanamıyorsa doğrulayıcı iddia yapılmamalı.

## 7. Yazılım kusuru, deney kusuru ve ölçüm kusuru — ayrım

| Sorun | Sınıf | Etki | Doğrulama/düzeltme |
|---|---|---|---|
| Standard ve CCDG renderlarının farklı bilgi alanları taşıması | Deney tasarımı / construct validity | Grafik gösteriminin bağımsız etkisi belirlenemez | V2 renderer parite testleri: ortak alanlar aynı; B/C kenar üçlüleri birebir eşdeğer |
| Literal-alias eşleştiricisinin anlamı ölçmemesi | Ölçüm geçerliliği | Doğru parafraz reddedilebilir, yanlış cevap kabul edilebilir | Kaynak temelli insan kalibrasyonu; iki hakem; kappa/ham uyum |
| Bazı vaka bağlamlarında düzeltme ipuçları bulunması | Girdi geçerliliği / leakage riski | Modelden bağımsız kök neden muhakemesi iddiası zayıflar | V2 vaka kılavuzu ve son prompt incelemesi; fix/test/gold ipuçları bağlam dışı |
| Aynı hata için 5 seed'in bağımsız gözlem sayılması | İstatistiksel analiz hatası olurdu; tarihsel analizde bu yapılmadı | Sahte büyük örneklem ve yapay kesinlik | Vaka başına 3/5 çoğunluk ve eşleştirilmiş analiz; yeni örneklem bağımsız vakalardan |
| 16 vakalık tasarımın yüksek, yönlü etki varsayımına dayanması | Örneklem/güç sınırlılığı | Daha küçük etkiler kaçabilir | V2 güç duyarlılığı, gerçekçi senaryolar, 61 vaka hedefi veya daha dar iddia |
| Runner adımı olmadan CI sonuçlarını “test başarısız” veya “test başarılı” saymak | Yazılım doğrulama/kanıt sorunu | Kod kalitesi hakkında desteklenmeyen iddia | Runner kimliği ve gerçek pytest çıktısı şart; steps=[] test sonucu değildir |
| Kamuya açık vakaların eğitimde bulunması olasılığı | Contamination riski | Genellenebilirlik ve model ezberleme riski | Muhafazakâr etiketleme; eğitim görmüş olduğunu kanıtlamadan kesin iddia kurmamak |

## 8. GitHub test ve V2 kapı durumu

PR #29, kör değerlendirme paketlerinden açık cevap anahtarını ve doğrudan kaynak/proje kimliklerini kaldıracak düzeltmelerle birleştirilmiştir. PR #30, denetim betiği ile dört regresyon testini eklemiştir; main commit'i şu an 7c40800274472fa672baf8909c406a9b18e2964e'dir. Buna rağmen main-branch merge run 38785788347 iş kaydı runner_id=0, boş runner adı ve sıfır adım göstermektedir. Dolayısıyla testlerin GitHub runner'ında çalıştığı doğrulanmamıştır. Bu, testlerin geçtiği ya da pytest hatası verdiği anlamına gelmez.

V2 manifesti hâlen status=draft, model_inference_permitted=false ve case_ids=[] durumundadır. Kalibrasyon havuzundaki yedi vakanın bağımsız ground-truth hakemliği pending_independent_review olarak kayıtlıdır. Bu denetim hiçbir V2 çıkarımına izin vermez.

## 9. Önerilen bilimsel yol

Kısa dönem (4 Kasım iç hedefi) için en uygulanabilir yol:

1. Dondurulmuş sonuçları ve bu denetimi raporda birlikte sun; CCDG etkisi hakkında kesin olumlu veya olumsuz iddia kurma.
2. Eski 160 çıktının koşul-kör ve ayrı sıralı anlamsal puanlamasını gerçek iki değerlendiriciyle yap. Sonuçlar keşfedicidir; bu işlem eski bilgi-paritesi sorununu çözmez.
3. Runner sorunu giderildiğinde PR #29 ve tarihsel denetim kodunun hedefli testlerini, ardından tam pytest ve tüm veri doğrulayıcılarını çalıştır.
4. V2 tasarımını yalnızca 61 uygun yeni vaka, bağımsız kaynak/doğrulama, skor kalibrasyonu, eşit bağlam, tokenizer ve model/runtime kapıları gerçek kanıtla tamamlanınca dondur. Aksi hâlde V2'yi tamamlanmış doğrulayıcı deney olarak sunma.

Bu yaklaşım hipotezi terk etmek değildir. Mevcut veriyle cevaplanamayan bir soruyu cevaplanmış gibi sunmaktan kaçınır ve yeni deneyde hangi değişkenin test edildiğini daha net hale getirir.
