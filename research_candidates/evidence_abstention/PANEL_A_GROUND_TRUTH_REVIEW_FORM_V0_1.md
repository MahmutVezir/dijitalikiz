# Panel A — bağımsız teknik kök neden doğrulama formu

**Sürüm:** 0.1 taslak  
**Durum:** Panel A ve danışman incelemesi, kalibrasyon ve ön kayıt gerekir. Model inference izni vermez.

## 1. Erişim ve körleme

Panel A, kaynak kodu ve teknik doğrulama kanıtını inceleyerek olası gerçek kök neden mekanizmasını belirler. Panel A üyeleri Panel B'de görev alamaz.

İzinli materyaller: sabitlenmiş upstream repository ve exact base/fix commit kimlikleri; issue/task açıklaması; hedefli test kaynağı; sabit ortam manifesti; base-fail/fix-pass ham stdout/stderr, exit code ve artifact hash kayıtları.

Panel A model yanıtlarını, P0/P1 sonuçlarını veya Panel B puanlarını görmez. Panel B'ye gidecek pakette repo/issue/PR/commit, patch, fix ve gold neden bilgisi bulunamaz.

## 2. İnceleyici ve vaka

- Pseudonymous case ID:
- Reviewer ID (gerçek isim değil):
- İnceleme tarihi (UTC):
- Form sürümü:
- Çıkar çatışması: [ ] Yok [ ] Var — görevi reddet
- Önceden erişim/inceleme: [ ] Yok [ ] Var — kısıtlı kayıtta açıkla
- Bu vakada teknik reproduksiyon veya paket hazırlama yaptım mı? [ ] Hayır [ ] Evet

Gerçek isim, e-posta, telefon, imza veya kurum içi özel bilgiler Git deposuna yazılmaz. Kimlik ve onay kayıtları ayrı, erişimi kısıtlı yerde tutulur.

## 3. Kaynak ve provenance kontrolü

| Kontrol | Sonuç (PASS / FAIL / UNCLEAR) | Kanıt referansı ve açıklama |
|---|---|---|
| Dataset row ve upstream repository eşleşiyor | | |
| Exact base commit doğrulandı | | |
| Fix commit ve PR/base ilişkisi doğrulandı | | |
| Issue/task aynı hata mekanizmasını tarif ediyor | | |
| Hedefli test aynı base ve fix revizyonlarında kullanıldı | | |
| Ortam, dependency ve komut eşitliği doğrulandı | | |
| Base'de hedefli test beklenen şekilde FAIL | | |
| Fix'te aynı test beklenen şekilde PASS | | |
| Ham stdout/stderr, exit code ve artifact hash mevcut | | |
| Lisans ve changed-file provenance ayrı incelendi | | |
| Fork/transfer/ortak upstream/duplicate issue riski incelendi | | |
| Önceden pipeline-debug veya hedef-test troubleshooting maruziyeti yok | | |

Dataset kartındaki lisans bildirimi upstream kodun lisansını otomatik belirlemez. Belirsiz lisans/provenance PASS sayılamaz.

## 4. Kök neden analizi

**Gözlenen hata davranışı (semptomdan ayrı):**

**Teknik mekanizma:** Hatanın oluşmasına neden olan kod/işlem mekanizmasını nedensel biçimde açıklayın.

**Nedensel zincir:**
1.
2.
3.

**Doğrudan kaynak kanıtları:** Her iddia için dosya/konum/commit/test referansı.

**Fix'in mekanizmayı neden düzelttiği:**

**Alternatif açıklamalar:** Gerçek mekanizmaya ek olarak en az iki teknik açıdan makul ve ayırt edilebilir alternatif tanımlayın. Üç seviyeli E1/E2/E3 tasarımı için bu koşul zorunludur.

| Aday mekanizma kodu | Teknik açıklama | Neden makul? | Hangi gözlenebilir kanıt bu açıklamayı eler? |
|---|---|---|---|
| M1 | | | |
| M2 | | | |
| M3 | | | |

Gerçek mekanizma eşleme anahtarı ayrı, erişim kontrollü dosyada saklanır. Panel B'ye hangi M kodunun gerçek neden olduğu açıklanmaz.

## 5. Bağımsız karar

Yalnızca birini seçin:

- [ ] PASS — teknik kök neden ve reproduksiyon doğrulandı.
- [ ] FAIL — teknik iddia/reproduksiyon doğrulanamadı.
- [ ] UNCLEAR — kanıt karar vermek için yetersiz.
- [ ] EXCLUDE — lisans, provenance, maruziyet, bağımsızlık veya başka dışlama nedeni var.

**Gerekçe:**

**Eksik kanıt / gerekli ek inceleme:**

**Üç ayrı makul mekanizma tanımlanabildi mi?** [ ] Evet [ ] Hayır  
Hayır ise vaka E1/E2/E3 doğrulayıcı tasarımına zorla sokulmaz.

## 6. Kilitleme ve uyuşmazlık

- İlk bağımsız karar kilitlendi mi? [ ] Evet [ ] Hayır
- Kilitli form SHA-256:
- İkinci Panel A reviewer ID:
- İlk iki karar aynı mı? [ ] Evet [ ] Hayır
- Adjudication gerekli mi? [ ] Evet [ ] Hayır
- Adjudicator ID (Panel A dışından):
- Adjudication gerekçesi ve sonucu:
- İlk kararların değiştirilemez kayıt referansları:

İlk bağımsız kararlar silinmez veya adjudication sonucu ile değiştirilmez. Adjudication ayrı kayıt olarak saklanır.

## 7. Sınırlar

Bu formu tamamlamak tek başına vaka kabulü değildir. Panel B kör kanıt yeterliliği incelemesi, lisans/provenance denetimi, dış denetçi onayı, registry doğrulaması ve diğer protokol kapıları ayrıca gerekir.

Reviewer attestation:
- [ ] Yalnızca izinli kaynakları inceledim.
- [ ] Model çıktısı veya diğer panelin puanlarını görmedim.
- [ ] Çıkar çatışması ve önceki maruziyetimi açıkladım.
- [ ] Kararımı kayıtlı kanıta dayandırdım.

Bu form araştırma taslağıdır; kurumsal/etik onay veya hukuki uygunluk yerine geçmez.
