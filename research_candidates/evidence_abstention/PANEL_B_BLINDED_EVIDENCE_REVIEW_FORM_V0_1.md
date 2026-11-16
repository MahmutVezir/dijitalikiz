# Panel B — kör kanıt yeterliliği değerlendirme formu

**Sürüm:** 0.1 taslak  
**Durum:** Bağımsız Panel B ve danışman incelemesi, kalibrasyon ve ön kayıt gerektirir. Model inference izni değildir.

## 1. Görev ve körleme

Panel B, modelin gerçekten göreceği anonim kanıt paketinin önceden tanımlanmış makul kök neden mekanizmalarını ne ölçüde ayırt ettiğini değerlendirir. Görevi gerçek kök nedeni tahmin etmek veya model yanıtını puanlamak değildir.

Panel B üyeleri Panel A, teknik reproduksiyon, paket hazırlama, gold-cause adjudication ve dış denetçi rollerinden ayrı olmalıdır. Kaynak repo/issue/PR, patch, buggy/fixed commit, gerçek kök neden, gizli E1/E2/E3 etiketi, P0/P1 koşulu veya model çıktısını görmemelidir.

## 2. İnceleyici ve görev kimliği

- Anonim task ID:
- Reviewer pseudonymous ID:
- İnceleme tarihi (UTC):
- Form/rubric sürümü:
- Çıkar çatışması: [ ] Yok [ ] Var — görevi reddet
- Önceden kaynak/gold erişimi: [ ] Yok [ ] Var — görevi reddet
- Model çıktısı veya P0/P1 koşulunu gördüm mü? [ ] Hayır [ ] Evet — incelemeyi durdur

Gerçek isim, iletişim bilgisi, imza veya kişisel bilgi Git deposuna yazılmaz. Kimlik/izin kayıtları ayrı ve kısıtlı tutulur.

## 3. Gösterilen materyalin kontrolü

Yalnızca şu içerikler verilmelidir:
1. Modelin göreceği aynı anonim evidence packet (aynı içerik ve hash).
2. M1, M2, M3… şeklinde kodlanmış ve sırası karıştırılmış aday mekanizma açıklamaları. Bu liste Panel B'nin değerlendirme aracıdır; model girdisine eklenmez.
3. Kanıt öğesi ID listesi ve anonim referanslar.

Gösterilmemesi gerekenler: upstream repository, issue/PR URL veya proje adı; kaynak patch/fixed commit/gerçek gold root cause; Panel A'nın gerçek neden M kodu; E1/E2/E3 koşul etiketi; model cevabı, P0/P1 veya prompt metaverisi; diğer değerlendiricinin puanları.

- Anonymous packet ID:
- Packet SHA-256:
- Gösterilen kanıt öğesi ID'leri:
- Gösterilen aday mekanizma kodları:
- Kimlik sızıntısı fark ettim mi? [ ] Hayır [ ] Evet — görevi durdur

## 4. Her aday mekanizmayı ayrı değerlendirme

Her mekanizma için yalnızca şu kararlardan birini verin:

- **SURVIVES:** Görünen paket bu mekanizmayı dışlamıyor; mekanizma kanıtla uyumlu veya dışlanıp dışlanmadığı belirsiz.
- **ELIMINATED:** Paketteki belirli kanıt, mekanizmayla açıkça çelişiyor ve bu mekanizmayı makul açıklama olmaktan çıkarıyor.

“Bilmiyorum”, “kanıt yetersiz”, eksik dosya veya belirsizlik SURVIVES olarak kaydedilir. Bir alternatifi elemek için belirli kanıt öğesi ID'si ve gerekçe zorunludur.

| Mekanizma kodu | Karar (SURVIVES / ELIMINATED) | Kanıt öğesi ID(leri) | Gerekçe |
|---|---|---|---|
| M1 | | | |
| M2 | | | |
| M3 | | | |
| Yeni alternatif (varsa) | | | |

**Listede bulunmayan yeni makul mekanizma var mı?** [ ] Hayır [ ] Evet  
Varsa açıklayın ve hangi kanıtla uyumlu olduğunu belirtin. Panel A bu yeni alternatifi model çıktısı olmaksızın incelemelidir. Yeni alternatif kabul edilirse mevcut kör değerlendirme durdurulur; aday mekanizma listesi/paket seti yeniden hazırlanır.

## 5. Kanıt düzeyi kararı

Karar, bağımsız mekanizma puanları kilitlendikten sonra verilir. Gerçek mekanizmanın M kodu Panel B'ye açıklanmaz.

- **E1 — ayırt edici/yeterli:** Tam olarak bir aday mekanizma SURVIVES; diğer bütün önceden tanımlı makul alternatifler ELIMINATED. Daha sonra Panel A'nın gizli gold eşlemesiyle hayatta kalan tek mekanizmanın gerçek mekanizma olduğu doğrulanmalıdır.
- **E2 — kısmi:** En az iki mekanizma SURVIVES ve en az bir alternatif ELIMINATED. Gizli eşlemede gerçek mekanizma hayatta kalanlar arasında olmalıdır.
- **E3 — ayırt edici değil/yetersiz:** Bütün önceden tanımlı mekanizmalar SURVIVES; hiçbir alternatif açık kanıtla elenmemiştir.
- **UNASSIGNABLE:** Paket bozuk/eksik, körlük ihlali var, aday mekanizmalar anlaşılmaz veya karar güvenilir biçimde verilemiyor.

Seçilen karar: [ ] E1 [ ] E2 [ ] E3 [ ] UNASSIGNABLE

**Karar gerekçesi:**

**Belirsizlik/eksik bilgi:**

**Model çıktısını görmeden mi karar verdim?** [ ] Evet [ ] Hayır

## 6. Bağımsız kilitleme

- İlk karar kilitlendi mi? [ ] Evet [ ] Hayır
- Kilitli form SHA-256:
- Reviewer pseudonymous ID:
- Zaman damgası (UTC):
- Paket hash'i ile gösterilen içerik eşleşiyor mu? [ ] Evet [ ] Hayır

İlk kararlar diğer değerlendiriciye veya adjudicator'a gösterilmeden önce kilitlenmelidir. Uyuşmazlık varsa üçüncü bağımsız adjudicator atanır. İlk kararlar korunur; adjudication ayrı dosyada tutulur.

## 7. Panel B onayı ve sınırlar

- [ ] Kaynak kimliği, patch, fixed source, gold cause, hidden level ve model output görmedim.
- [ ] Diğer değerlendiricinin kararını görmedim.
- [ ] Her ELIMINATED kararı için kanıt ID ve gerekçe verdim.
- [ ] Belirsizliği alternatifleri elemek yerine SURVIVES olarak kaydettim.
- [ ] Çıkar çatışması ve önceki maruziyet durumumu açıkladım.

Panel B'nin kararı semantik kanıt yeterliliği değerlendirmesidir. Yapısal hash doğrulayıcıları bunun yerine geçmez. Panel B onayı tek başına vaka kabulü veya inference izni oluşturmaz.

Bu form taslaktır; bağımsız panel kalibrasyonu ve protokol onayı tamamlanmadan doğrulayıcı veri toplamada kullanılmamalıdır.
