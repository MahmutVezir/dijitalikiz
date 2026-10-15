# TÜBİTAK 2204-A — kör anlamsal değerlendirme yönergesi

**Çalışma türü:** Tarihsel 160 model yanıtının sonradan, keşifsel ve koşul etiketleri gizlenmiş değerlendirmesi.  
**Bu görev yeni doğrulayıcı deney değildir.** Puanlar mevcut dondurulmuş literal-alias sonuçlarının yerine geçmeyecektir.

## Hangi dosya kullanılacak?

Koordinatör yalnızca size atanmış değerlendirici paketini gönderecektir:
- Değerlendirici A: `semantic_review_reviewer_A.zip`
- Değerlendirici B: `semantic_review_reviewer_B.zip`

Yalnızca kendi ZIP'inizi inceleyin. Diğer değerlendiricinin ZIP'ini istemeyin veya açmayın. Koordinatörün özel eşleme/anahtar dosyalarını almayın, istemeyin veya paylaşmayın.

ZIP içinde `README_REVIEWER.md` ve `review_packet.jsonl` vardır. README, İngilizce etiket değerlerini ve alanları tanımlar. Her JSONL satırı ayrı bir JSON nesnesidir: ilk satır paket üstbilgisi, kalan 160 satır yanıt değerlendirmeleridir.

## Bağımsızlık ve körlük

1. Diğer değerlendiriciyle kararları, vakaları veya olası cevapları konuşmadan önce kendi 160 satırınızı tamamlayın.
2. Yanıtın hangi deney koşulundan üretildiğini tahmin etmeye çalışmayın ve tahmin ettiyseniz bile herhangi bir alana yazmayın.
3. Verilen problem özetini, numaralı temel olguları veya model yanıtını değiştirmeyin.
4. Yalnızca her yanıt satırındaki `review` nesnesinin altı alanını doldurun. `review_id` ve `case_ref` değerleri aynen korunmalıdır.
5. Paket cevap anahtarı ve doğrudan kaynak bağlantıları içermemek için tasarlanmıştır. Bu nedenle kararınızı sağlanan özet/temel olgulara dayandırın. Kaynak kodu bağımsız biçimde doğruladığınızı ileri sürmeyin.

## Etiketler

Etiketleri aşağıdaki yazımıyla kullanın:

| Alan | İzin verilen değerler |
|---|---|
| `root_cause_correctness` | `correct`, `partially_correct`, `incorrect`, `unscorable` |
| `component_localization` | `correct`, `partially_correct`, `incorrect`, `unscorable` |
| `evidence_consistency` | `consistent`, `partially_consistent`, `inconsistent`, `unscorable` |
| `dependency_reasoning` | `correct`, `partially_correct`, `incorrect`, `not_applicable`, `unscorable` |
| `overall_diagnostic_status` | `correct`, `partially_correct`, `incorrect`, `unscorable` |
| `reviewer_notes_with_evidence` | Serbest metin; kısa gerekçe ve ilgili kanıt kimliği |

Kök neden için:
- **correct:** Model, temel nedensel hata mekanizmasını verilen kanıtla tutarlı biçimde açıklar. Birebir terim eşleşmesi gerekmez; anlamca eşdeğer açıklama kabul edilir.
- **partially_correct:** Bileşenin veya mekanizmanın önemli bir kısmı doğrudur; ancak kritik bir nedensel unsur eksik ya da hatalıdır.
- **incorrect:** Açıklama verilen kanıtla çelişir, yanlış mekanizma belirtir veya ilgili kök nedeni desteklemez.
- **unscorable:** Yanıt veya sunulan kanıt, makul bir karar vermeyi gerçekten engeller. Bu etiketi yalnızca zor/kararsız olduğu için kullanmayın.

Belirtiyi tekrar etmek, yalnızca etkilenen bileşeni söylemek, kendinden emin yazmak veya bir doğru terimi alternatifler arasında saymak tek başına doğru teşhis sayılmaz. İstenen mekanizmayı açıklayıp açıklamadığına karar verin.

## Gerekçe yazımı

Her satırda `reviewer_notes_with_evidence` alanına bir-üç cümle yazın. Gerekçenin hangi sunulmuş bilgiye dayandığını açıkça belirtin; örneğin “problem özeti” veya “B2 temel olgusu”. Yalnızca “doğru” / “yanlış” yazmayın. Paket dışında bulunan kaynak kod, test adı veya kök neden tahminini kanıt olarak eklemeyin.

## Dosyayı tamamlama ve teslim

1. Orijinal ZIP'i değiştirmeyin. Önce `review_packet.jsonl` dosyasının kopyasını oluşturun.
2. Her yanıta ait yalnızca `review` alanlarını doldurun; her satırı geçerli JSON olarak tutun. JSONL satırlarını birleştirmeyin.
3. Tamamladığınız dosyayı `reviewer_A_completed.jsonl` veya `reviewer_B_completed.jsonl` gibi ayrı bir adla kaydedin.
4. 160 yanıtın tamamı için altı alanı gözden geçirin; boş kalan alanları tamamlayın. Kararınız gerçekten verilemiyorsa uygun `unscorable` değerini kullanın ve gerekçeyi yazın.
5. Dosyayı yalnızca koordinatöre gönderin. İlk karar dosyanız teslimden sonra değiştirilmeyecek şekilde kilitlenmelidir.
6. Her iki değerlendiricinin ilk dosyaları da kilitlenmeden koordinatör anahtarları açılmayacak ve anlaşmazlıklar tartışılmayacaktır. İlk puanlar, sonraki hakemlikte değiştirilmeyecek; ayrı bir adjudication kaydı oluşturulacaktır.

## Bilimsel sınırlar

Bu, önceden görülmüş çıktılara uygulanan **post-hoc keşifsel** bir değerlendirmedir. Sonuçlar yeni bir doğrulayıcı deney gibi sunulmayacaktır. Beş tekrar, beş bağımsız yazılım vakası değildir. Bu değerlendirme, tarihsel koşulların bilgi içeriği eşit olmadığı gerçeğini geriye dönük düzeltemez ve CCDG'nin bağımsız nedensel etkisini tek başına kanıtlayamaz.
