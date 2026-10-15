# Araştırma Yolu Kararı — 15 Ekim 2026

## Karar

**Ana yol: A — tarihsel araştırmayı dürüstçe tamamlamak ve eski 160 çıktıyı sonradan, koşul etiketleri gizlenmiş anlamsal incelemeye açmak.**

Bu seçim, A yolunun CCDG etkisini nedensel olarak kanıtlayacağı anlamına gelmez. A yolu mevcut kanıtı bozmadan en kısa sürede savunulabilir bir araştırma sonucu elde etmenin yoludur: tarihsel çalışmanın ölçüm aracının taban etkisi, koşullar arasındaki bilgi-paritesi kusuru ve kaynak girdilerindeki çözüm ipuçları belgelenir; insan değerlendirmesi gerçekten yapılırsa yalnızca keşifsel sonuç olarak raporlanır.

**B — üç koşullu, bilgi-eşitliği sağlanmış doğrulayıcı deney — bilimsel olarak en iyi sonraki deneydir, ancak bugün çalıştırmaya hazır değildir.** Manifestte vaka listesi boş, yedi kalibrasyon adayı bağımsız hakem bekliyor ve tüm model/runtime/tokenizer/ön kayıt kapıları açık. 4 Kasım iç hedefine kadar bu eksiklerin kanıtla kapatılabildiği varsayılamaz. Bu yüzden model çıkarımı kapalı kalır.

**C — araştırma sorusunu ölçüm aracı geçerliliğine dönüştürmek — yalnızca koşullu yedek plandır.** A yolu sırasında toplanacak değerlendirme, literal-alias aracının yanlış pozitif/yanlış negatif davranışını inceleyen daha dar bir araştırma sorusuna dönüşmeye elverişli olabilir. Ancak insan değerlendirmesi olmadan bu dönüşüm tamamlanmış sayılmaz; başlık değiştirmek tek başına bilimsel katkı oluşturmaz.

## Üç yolun karşılaştırması

| Ölçüt | A — Tarihsel çalışmayı tamamla | B — Yeni bilgi-eşitliği deneyini yap | C — Araştırma sorusunu ölçüm geçerliliğine daralt |
|---|---|---|---|
| Tarihsel veriyi koruma | Yüksek uyum; çıktılar ve skorlar değişmez | Yüksek uyum; yeni örneklem ayrı kalır | Yüksek uyum; eski sonuç yalnızca bağlamdır |
| CCDG'nin nedensel etkisini ölçme | Hayır; geçmiş deney bilgi-eşitliği sağlamaz | Evet, ancak yalnızca uygun koşullar ve geçerli ölçümle | Hayır; odak puanlama aracının davranışıdır |
| Bugünkü hazır oluş | Arşiv mevcut; bağımsız insan değerlendirmesi bekliyor | Hazır değil: 0 kabul edilmiş v2 vakası; kalibrasyon ve teknik kapılar açık | Henüz hazır değil; A yolundaki insan puanlarına bağımlı |
| Yeni veri/insan emeği | İki bağımsız değerlendirici; sonra ayrı kaynak-kod temelli hakemlik | En az 61 bağımsız vaka planı, iki hakem, kalibrasyon ve teknik çalışma | İki bağımsız değerlendirici; olası üçüncü hakem |
| 4 Kasım iç hedefine uygunluk | En uygulanabilir | Şu an yüksek başarısızlık/yarım kalma riski | Ancak puanlar gerçekten toplanırsa olası |
| Temel bilimsel risk | Keşifsel yeniden puanlamanın doğrulayıcı kanıt gibi sunulması | Eksik/kalitesiz vaka havuzu veya zayıf güç; çoklu kapı ihlali | Eski çıktılarla ölçüm aracını kalibre edip aynı veride doğrulama iddia etmek |
| Jüri önünde savunulabilir iddia | “Tarihsel sonlanım bu ölçüm ve tasarımla soruyu çözmedi; sınırlılıklar denetlenmiş ve sonraki deney tasarımı tanımlanmıştır.” | “Aynı bağımlılık bilgisi düz metin ve CCDG olarak sunulduğunda vaka düzeyi başarı farkı ölçüldü.” — ancak çalışma gerçekten tamamlanırsa | “Literal eşleştiricinin insan anlamsal değerlendirmesiyle uyumu ve hata türleri incelendi.” — ancak gerçek anotasyonlarla |

## Mevcut araştırma tam olarak nerede yanlış/yetersiz?

Bu kusurları birbirinden ayırmak gerekir:

1. **Deney tasarımı / construct validity:** tarihsel Standard renderer açık hata açıklamasını 16/16 vakada verir; CCDG renderer bunu 0/16 vakada verir ve bunun yerine bağımlılık kenarları ekler. Bu nedenle temsil biçimi ile bilgi içeriği aynı anda değişmiştir. Tarihsel deney grafiğin bağımsız etkisini belirleyemez.
2. **Ölçüm geçerliliği:** birincil literal-alias kuralı semantik değerlendirici değildir. Dört gerçek tarihsel çıktı (MATH-305, CLOSURE-14, MATH-393, TIME-12; Standard/seed 42) mekanizmayı açıklıyor gibi görünen ifadeler içerdiği halde hiçbir alias eşleşmesi üretmedi. Bunlar olası yanlış-negatif adaylarıdır, fakat henüz insan hakemlerince doğru puanı almamıştır.
3. **Girdi ipucu / leakage riski:** I_base alanı iki koşulda ortaktır; buna rağmen 7/16 vakada “fix/corrected/before the fix” türü açık ifadeler, daha geniş bir taramada da 5/16 vakada başka çözüm-yönlü ifadeler bulundu (gruplar örtüşüyor; birleşim 8/16). Bu sayılar sözcüksel tarama işaretleridir; eğitim verisi bulaşmasının kanıtı değildir.
4. **Örneklem ve istatistik:** 16 bağımsız vaka kullanmak, beş seed'i bağımsız gözlem saymamak açısından doğrudur. Ancak tasarım gücü 0,05 Standard-only ve 0,60 CCDG-only gibi çok büyük, yönlü uyumsuzluk varsayımlarına bağlıydı. Bu, daha küçük etkiler için yeterli güç göstermez.
5. **Ground truth ve insan değerlendirmesi:** tarihsel vaka açıklamaları, CCDG anotasyonları ve kök neden etiketleri bağımsız insan değerlendirmesinden geçerek yeniden doğrulanmış değildir. Eski cevaplara insan puanları henüz toplanmamıştır. Boş formlar tamamlanmış hakemlik değildir.
6. **Yazılım doğrulama:** denetim betiği ve dört regresyon testi PR #30 ile main'e girmiştir, ancak GitHub Actions runner'ı adım başlatmadığı için tam depo pytest ve veri doğrulayıcılarının başarıyla çalıştığı söylenemez. İzole yerel denetim harness'i 4/4 senaryoda geçmiştir; bu CI yerine geçmez.
7. **V2 çıkarım kapısı:** data/followup_v2/protocol_manifest.json status=draft, model_inference_permitted=false, case_ids=[] durumundadır. Kalibrasyon havuzundaki 7/7 vaka bağımsız ground-truth incelemesi bekliyor. Çıkarım yapmak şu anda bilimsel olarak yetkilendirilmiş değildir.

## A yolundaki kör anlamsal incelemenin geçerli yorum sınırları

İki değerlendiriciye ayrı, koşul/seed alanları ve canonical cevap anahtarı çıkarılmış v1.2 paketleri verilmelidir. Her biri bağımsız biçimde ilk puanlarını ve kanıt gerekçelerini kilitlemelidir. Aynı anonim vaka referansları, sıralama farklı olduğu için, ancak puanlama tamamlandıktan sonra vaka düzeyinde hizalama yapılmasını sağlar.

Paketlerde beklenen kök neden ve doğrudan kaynak URL'leri yoktur. Bu, cevaba yönlendirmeyi azaltır; fakat incelemecilerin yalnızca sunulmuş problem özeti ve numaralı I_base maddeleri üzerinden karar vermesi anlamına gelir. Teknik içerik vaka/koşul tahminine yine izin verebilir. Bu yüzden bu işlem **mükemmel körleme garantisi veren kaynak-kod doğrulaması değildir**. Birincil bağımsız puanlar kilitlendikten sonra ayrı bir adjudicator kaynak revizyonu ve regresyon kanıtını incelemeli, uyuşmazlıkları ayrı kayda geçirmelidir. İlk puanlar değiştirilmemelidir.

Raporlanacaklar: her etiketin sayısı, ham değerlendirici anlaşma oranı, uygun olduğunda Cohen kappa (sınıf dağılımı ve belirsizlikleriyle birlikte), anlaşmazlıklar, değerlendirilemez yanıtlar ve adjudication kararları. Cohen kappa, insan puanları toplanmadan hesaplanamaz. Herhangi bir sonuç eski literal-alias sonucunun yerine geçmez; sonuçlar **post-hoc keşifsel** olarak etiketlenir.

## B yoluna geçiş için fail-closed kabul ölçütleri

B yalnızca aşağıdaki koşulların tümü kanıtla tamamlandığında yeniden değerlendirilir:

- 61 farklı ve yeni bağımsız yazılım hatası için gerçek kaynak/fix revizyonu, test kanıtı, lisans ve kök neden kanıtı mevcut; pilot, eski doğrulayıcı ve kalibrasyon örneklemiyle örtüşme yok.
- Problem açıklaması ve I_base, çözüm/test adı/gold label/known fix ifadesi gibi cevap ipuçlarını taşımayacak biçimde iki kişi tarafından gözden geçirilmiş.
- A/B/C koşullarındaki temel bağlam birebir aynı; B ve C'de kenar uçları, yönü, ilişki etiketi ve detayları eşit; tek planlı fark temsildir.
- Ölçüm rubriği bağımsız kalibrasyon kümesinde iki gerçek değerlendirici tarafından denenmiş; önceden belirlenen anlaşma/kappa eşikleri karşılanmış; anlaşmazlık çözümü dondurulmuş.
- Sample-size duyarlılığı açık varsayımlarla raporlanmış. 61 vaka hedefi varsayımsal uyumsuz çift olasılıkları içindir, gözlenen etki tahmini değildir.
- Model revision, tokenizer, runtime/GPU, prompt ve bütün son render edilmiş bağlamların token sayımı, chat-template token sınırı, tek-örnek çıkarım ve JSON şeması kontrolleri başarıyla tamamlanmış.
- Case listesi, prompt'lar, randomize çalışma çizelgesi, istatistik planı, dışlama kuralları ve bunların hash'leri inference öncesinde dondurulmuş.

Bir kapı bile başarısızsa yeni toplu inference başlatılmaz. Bu karar model performansı hakkında bir sonuç değil, deney bütünlüğü gereğidir.

## Türkiye derecesi projelerinden çıkarılabilecek gerçek ders

2022–2026 ulusal derece karşılaştırması docs/TUBITAK_WINNER_BENCHMARK_2022_2026.md dosyasında kaynak sınırlılıklarıyla verilmiştir. Ödül kazanmış bir projenin başlığı veya haberi, kendi başına iyi yöntem uyguladığını kanıtlamaz; birçok proje için tam teknik rapor erişilebilir değildi. Buna rağmen yarışmanın resmî çağrısı ve sayfada halen bağlantısı verilen değerlendirme formları, problemin açık anlatılmasını, uygun yöntemi, sonucu/etkiyi, doğruluk ve tekrarlanabilirliği ve öğrencinin kendi çalışmasına hâkimiyetini ölçülebilir biçimde gösterme ihtiyacını ortaya koyar.

Bizim projeye aktarılacak ders, daha büyük model veya daha uzun rapor değildir: birincil soruyla ölçüm aracını hizalamak, doğru karşılaştırma kurmak, her iddia için izlenebilir kanıt sunmak ve çözümlenemeyen sonucu da açıkça bildirmektir. Bu yaklaşım ödül garantisi vermez; ama bilimsel iddiayı savunulabilir kılar.

## Nihai karar ve hedef

4 Kasım iç hedefi için A yolunu ana çalışma kabul ediyorum; kör semantik değerlendirmeyi ancak gerçek kişiler tamamladığında keşifsel bulgu olarak eklemek. B gelecekteki en güçlü nedensel testtir ama bugün vaka havuzu ve kapılar tamamlanmadığı için çalıştırılmayacaktır. C sadece A değerlendirmesi gerçek bir araştırma sorusu olan ölçüm-geçerliliği analizine dönüşürse düşünülebilir; başlık değiştirme tek başına kabul edilmez.

Resmî 2204-A son başvuru tarihi, güncel TÜBİTAK çağrı sayfasında 4 Ocak 2027 saat 17.30 olarak belirtilmektedir. Başvuru öncesinde sayfa, form ve tematik alan seçenekleri yeniden doğrulanmalıdır.
