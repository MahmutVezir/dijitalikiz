# Kör insan değerlendirmesi — paket teslim denetimi

**Tarih:** 15 Ekim 2026 (UTC)  
**Kapsam:** Tarihsel deneyin 160 mevcut çıktısına yönelik v1.2 kör değerlendirme ZIP'leri ve kaynak arşivinin bütünlüğü.  
**Durum:** Dosya ve eşleme bütünlüğü denetlendi; insan puanlaması henüz alınmadı.

## Denetim sonucu

Gerçek ZIP/arşiv baytları üzerinde SHA-256, ZIP bütünlüğü, arşiv manifesti, cevap eşlemesi ve kör paket alanları kontrol edildi. Bağımsız denetim betiği `scripts/audit_blinded_exploratory_packet_artifacts.py` bu üç arşiv ve iki özel koordinatör eşleme dosyası üzerinde `PASS` döndürdü.

| Artefakt | Boyut | SHA-256 |
|---|---:|---|
| Tarihsel doğrulayıcı arşiv | 292,742 bayt | `e54ad960f141f3fadcfbdd88528f89d9fc0727c0c5e5062250d94da9cb0943bd` |
| Değerlendirici A v1.2 | 34,860 bayt | `0604919587fe8063b294c9ca5848d6a5843b683df68de8b66cbb9894ff61fdb0` |
| Değerlendirici B v1.2 | 33,843 bayt | `c247950cdf55be67da4adce934397fc558e168c9f74781b550cc56bb1ced81fb` |

## Gerçekten doğrulananlar

- ZIP bütünlük testi her üç dosyada da geçti.
- Tarihsel arşivin manifestindeki 212 dosyanın tamamında varlık, bayt uzunluğu ve SHA-256 eşleşti: **212/212; 0 uyuşmazlık**.
- Arşivde 160 benzersiz vaka-koşul-tohum kaydı ve 16 bağımsız vaka bulundu.
- A ve B ZIP'lerinin her birinde yalnızca `README_REVIEWER.md` ile `review_packet.jsonl` var; her biri 160 yanıt, 16 anonim vaka referansı ve 160 benzersiz inceleme kimliği içeriyor.
- İki değerlendiricinin paketlerinin yanıt çoklu-kümesi aynı; sıralama farklıdır (160 satırdaki konumların yalnızca 1'i aynıdır).
- Her değerlendirici için özel anahtarla yapılan arşiv eşlemesinde ham çıktı hash'i, prompt/context hash'leri, kaynak commit'i ve anonim vaka referansı kontrolleri ayrı ayrı **160/160** eşleşti.
- Değerlendiriciye gösterilen yanıtlarda yasaklanmış kaynak/koşul/seed/cevap anahtarı alanı tespit edilmedi; doğrudan URL bulunan satır sayısı 0.
- İki pakette de önceden doldurulmuş insan puanı yoktur.

Bu doğrulamalar dosya bütünlüğünü ve paketin kaynak arşiviyle eşlemesini kanıtlar; model teşhislerinin doğru olduğunu veya paketlerin kusursuz körlendiğini kanıtlamaz. Teknik metinler bazı vakaları/koşulları tahmin ettirebilir.

## Teslim prosedürü

1. Değerlendirici A'ya yalnızca A ZIP'i, Değerlendirici B'ye yalnızca B ZIP'i verilir.
2. İki değerlendirici ilk puanlarını birbirleriyle konuşmadan bağımsız biçimde tamamlar.
3. Her model yanıtı için `review` alanındaki altı alan doldurulur. Gerekçe, paketteki problem özeti veya `B1`, `B2` gibi sunulmuş temel olguya dayanır. Pakette kaynak kod gösterilmediği için gerekçeler kaynak koddan bağımsız doğrulama yapıldığını iddia etmemelidir.
4. Tamamlanmış ilk puan dosyaları değişiklik yapılmadan kilitlenir ve koordinatöre ayrı ayrı teslim edilir.
5. İki ilk dosya da kilitlenene kadar koordinatör anahtarları paylaşılmaz ve değerlendiriciler sonuç tartışmaz. Sonrasında anlaşmazlıklar ayrı bir hakemlik kaydında ele alınır; ilk puanlar korunur.
6. Gerçek puan dosyaları gelmeden Cohen kappa/ağırlıklı kappa, değerlendiriciler arası anlaşma veya semantik başarı sonucu hesaplanmaz.

## Bilimsel yorum sınırı

Bu, daha önce görülmüş 160 çıktıya uygulanan **sonradan ve keşifsel** değerlendirmedir. Tarihsel literal-alias sonucu değiştirilmez: Standard 0/80, CCDG 0/80; 16 vakanın hiçbirinde 3/5 çoğunluk başarısı yoktur; exact iki taraflı McNemar p=1.00. İnsan puanlaması tarihsel koşullardaki bilgi-paritesi kusurunu geriye dönük düzeltmez ve CCDG'nin nedensel etkisini kanıtlayamaz.

**Yeni model çıkarımı yapılmadı.** V2 manifesti taslak ve `model_inference_permitted=false` durumunda kalır.

## Özel anahtar güvenliği

`semantic_review_key_private_A.json` ve `semantic_review_key_private_B.json` özel koordinatör dosyalarıdır. Bunları değerlendiricilere göndermeyin, depoya eklemeyin veya rapor eki olarak yayımlamayın. Denetim betiği eşlemeleri yalnızca bellekte okur ve raporda vaka kimliği, koşul, tohum veya anahtar içeriği yazdırmaz.

## Tekrarlama

Denetim betiği beş yerel girdi alır: tarihsel arşiv ZIP'i, iki değerlendirici ZIP'i ve iki özel koordinatör anahtarı. Betik dosya özetlerini, ZIP içeriğini, manifesti ve tüm kayıt eşlemelerini doğrular; bir sapmada başarısız çıkar. Özel koordinatör dosyalarını yerel ve depo dışı tutun.

## CI sınırı

GitHub Actions runner smoke run `38779073729`, ikinci denemede de `failure` ile sonlandı; iş kaydında yürütülmüş adım yoktu. Bu, paket denetim betiğinin yerel PASS sonucundan ayrıdır ve depo `pytest` paketinin geçtiği anlamına gelmez. GitHub Status sayfası kontrol sırasında Actions için genel bir kesinti bildirmiyordu; depoya/hesaba özgü nedeni kullanılan bağlantıyla kanıtlamak mümkün olmadı.
