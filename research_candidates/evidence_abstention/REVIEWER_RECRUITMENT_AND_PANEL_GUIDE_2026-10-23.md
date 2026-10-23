# Bağımsız değerlendirici bulma ve inceleme paketi

**Sürüm:** 0.1-draft  
**Tarih:** 23 Ekim 2026  
**Durum:** Hazırlık rehberi; herhangi bir bağımsız değerlendirme yapılmış değildir. Bu dosya değerlendirici atamaz, vaka kabul etmez ve çıkarım izni vermez.

## Amaç ve kritik kural

Çalışmanın geçerli olabilmesi için birbirinden bağımsız iki inceleme paneli gerekir. Her panelde en az iki gerçek insan bulunmalı ve iki panelin üyeleri kesişmemelidir. Öğrencinin kendisi, aynı vakanın kaynak/düzeltme ayrıntılarını daha önce incelemiş biri veya araştırma çıktısını üretmiş model, bağımsız insan puanlayıcısının yerini alamaz.

İnceleme kapasitesi bulunamazsa değerlendiriciler yapılmış gibi yazılmaz. Gerekli kapılar tamamlanmadığında çalışma doğrulayıcı deney olarak başlatılmaz; süre nedeniyle kabul kuralları gevşetilmez.

## Panel A — kök neden, kaynak ve lisans

**İki bağımsız değerlendirici.** Uygun kişiler yazılım mühendisliği, Python testleri, hata ayıklama, bakım/provenance veya açık kaynak lisansları konusunda deneyimli bir öğretmen, araştırmacı ya da profesyonel olabilir.

Panel A her aday için ayrı ayrı şu soruları yanıtlar:
1. Kaynak ve sabit BugsInPy revizyonu doğru mu; buggy/fixed commit'ler gerçekten farklı mı?
2. Kayıtlı Python ortamında aynı hedef test buggy sürümde hedef kusuru gösteriyor ve fixed sürümde geçiyor mu?
3. Başarısızlık gerçekten hedef kusurdan mı kaynaklanıyor, yoksa kurulum/bağımlılık/fixture/harness sorunu mu?
4. Hata mekanizması kaynak kod, test ve düzeltme değişikliğiyle tutarlı mı?
5. Kaynak, lisans ve atıf/provenance bilgileri doğrulanabilir mi?
6. Vaka daha önce açılmış, teknik taramada görülmüş, aynı kök nedenin kopyası veya başka şekilde kirlenmiş mi?
7. İki bağımsız değerlendiricinin kararı ve gerekçesi ne; uyuşmazlık varsa nasıl çözüldü?

Panel A karar sınıfları: ACCEPT, HOLD veya REJECT. Bir teknik buggy-fail/fixed-pass sinyali tek başına ACCEPT anlamına gelmez.

## Panel B — kanıt yeterliliği ve yanıt puanlama

**Panel A'dan farklı iki bağımsız değerlendirici.** Bu panel, kök nedeni veya düzeltmeyi ortaya çıkaran içerikleri görmemelidir. Panel B üyeleri vaka kimliği, upstream proje adı, buggy/fixed commit, fix/patch, gold kök neden, gizli E1/E2/E3 etiketi ve mümkün olduğunca P0/P1 koşulunu görmez.

Panel B'ye yalnızca:
- modelin gerçekten göreceği kanıt paketi;
- paketteki kanıt ID'leri ve kaynak bağlamı;
- anonim yanıt ID'si ve modelin ham yanıtı;
- dondurulmuş puanlama rubriği

verilir.

Panel B, her paketin tek kök nedeni diğer makul açıklamalardan ayırmaya yeterli olup olmadığını bağımsız gerekçeyle puanlar. Model çıktıları elde edildikten sonra kök neden doğruluğu gold Panel A kaydına göre ayrı bir süreçte değerlendirilir. Panel B'nin varlığı veya kararı, semantik auditor modelinin geçerli olduğunu otomatik olarak kanıtlamaz.

## E1/E2/E3 paketlerinin hazırlanması

1. Panel A kök neden doğruluğunu kaynak/test/fix kanıtından belirler.
2. Bir paket yazarı, model çıktıları görülmeden aynı vaka için üç kanıt paketi hazırlar.
3. Panel B paketleri, kimlik ve gizli koşul bilgisi olmadan inceler.
4. E1 ayırt edici kanıt içerir; E2'de önceden belirlenmiş ayırt edici kanıtın bir kısmı eksiktir; E3 birden fazla makul açıklamayı açık bırakır.
5. Yanıltıcı kanıt üretmek, gold yanıtı pakete sızdırmak veya E3'ü yapay şekilde hatalı içerikle bozmak yasaktır.
6. Paketler ve ID listeleri hash'lenip dondurulur. Değişiklikler tarihçe ve gerekçesiyle kaydedilir.

## Bağımsızlık, gizlilik ve kayıt

- Her panel üyesi pseudonymous bir reviewer ID kullanır; gerçek kimlikler kısıtlı bir kayıtta saklanır.
- Her kişi önce bağımsız puanını kilitler; birbirinin kararını görmeden önce gerekçesini kaydeder.
- İlk puanlar silinmez. Adjudication gerekiyorsa gerekçe, tarih ve nihai karar ayrıca saklanır.
- Panel B'ye gold kök neden, patch veya modelin görmediği kanıtlar paylaşılmaz.
- İnsan isimleri, kişisel e-postalar ve özel yazışmalar açık GitHub deposuna commit edilmez.
- İnceleme formu doldurmak veya birine e-posta göndermek tek başına bilimsel onay değildir; kararlar gerçek kanıta dayanmalıdır.

## İncelemeye davet metni

**Konu:** TÜBİTAK 2204-A yazılım hata teşhisi araştırması için bağımsız inceleme katkısı

Merhaba,

Lise düzeyinde yürüttüğüm 2027 TÜBİTAK 2204-A araştırmasında, büyük dil modellerinin yazılım hata teşhisi sırasında kanıt yetersiz olduğunda cevap vermekten kaçınma davranışını inceliyorum. Araştırmanın bilimsel geçerliliğini korumak için kaynak/test/düzeltme kanıtını veya modelin gördüğü kanıtın yeterliliğini bağımsız olarak değerlendirebilecek kişilere ulaşmaya çalışıyorum.

Bağımsız bir inceleme paneline katkı sunmayı değerlendirir misiniz? Panel rolüne göre ya (A) kaynak, hedef test, kök neden ve lisans/provenance kanıtlarının incelenmesi ya da (B) vaka kimliği ve gerçek kök neden gizlenmiş kanıt paketlerinin yeterliliğinin değerlendirilmesi söz konusu olacaktır. İki rolün bilgi erişimi farklıdır; aynı kişi iki panele birden katılamaz. İnceleme protokolü, karar ölçütleri ve örnek formlar önceden paylaşılacaktır.

İlginiz varsa hangi panel rolünün uzmanlığınıza uygun olduğunu ve olası çıkar çatışması ya da önceki vaka maruziyeti bulunup bulunmadığını bildirmeniz yeterlidir. Vaka kabulü veya araştırma sonucu konusunda peşinen bir beklenti yoktur; belirsiz ya da olumsuz kararlar da kayıt altına alınacaktır.

Zaman ayırdığınız için teşekkür ederim.

Saygılarımla,  
[Öğrenci adı ve okul bilgisi, kişisel e-posta/iletişim bilgileri yalnızca doğrudan yazışmada]

## Gönderim öncesi kontrol

- [ ] Alıcı, rol için uygun uzmanlığa sahip.
- [ ] Alıcının daha önce ilgili adayları, düzeltmeleri veya model çıktısını görüp görmediği soruldu.
- [ ] Panel A ve Panel B üyeleri birbirinden farklı.
- [ ] Kısıtlı kişisel bilgiler depoya yazılmadı.
- [ ] Gönderilen metin sonuç veya finalistlik garantisi ima etmiyor.
- [ ] Kabul edilen vakalar hakkında kararlar yalnızca belgelenmiş kanıta dayanıyor.
