# Aday vaka manuel inceleme rehberi

**Amaç:** BugsInPy adayını deney siciline almadan önce gerekli kanıtı aynı sırada, denetlenebilir biçimde toplamak. Bu belge ve [JSON form şablonu](CASE_REVIEW_INTAKE_TEMPLATE.json) bir vakayı kabul etmez.

## İnceleme sırası

1. **Maruziyet ve bağımsızlık:** Vakanın patch/issue/test bilgilerini önceden açıp açmadığımızı, başka bir vaka/PR ile aynı kök nedene bağlı olup olmadığını kaydet. Önceden incelenmiş fizibilite/smoke vakaları ana doğrulayıcı örnekleme geri alınmaz.
2. **Kaynak ve lisans:** BugsInPy metadata revizyonu, proje kaynağı, buggy/fixed commit, lisans dosyasının aynı/uygun revizyondaki yolu ve hash’i, atıf/yayım kısıtları.
3. **Exact runtime ve test çifti:** Metadata Python sürümünü aynen kullan. Checkout ve compile kurulum hatalarını hedef test başarısızlığı olarak sayma. Aynı hedef regresyon testi buggy sürümde hedeflenen kusuru göstermeli, fixed sürümde geçmeli. Her iki ham günlük ve runtime fingerprint saklanmalı.
4. **Kök neden ground truth:** Kaynak, regresyon testi ve düzeltme kanıtıyla kök neden tanımlanmalı. İki bağımsız inceleyici birbirinden bağımsız karar vermeli. Uyuşmazlıkta ilk kararlar korunarak adjudication yapılmalı.
5. **E1/E2/E3 paketleri:** Model çıktıları alınmadan aynı vaka için kanıt paketleri hazırlanmalı ve hash’lenmeli. E1 kök nedeni makul alternatiflerden ayırmalı; E2 önceden tanımlanmış ayırt edici kanıtın bir kısmını kaldırmalı; E3 tek kök nedeni seçmeye yetmemeli ve en az iki makul açıklamayı açık bırakmalı. Paketler hatalı veya yanıltıcı kanıtla manipüle edilmemeli.
6. **Bilgi sızıntısı/kontaminasyon:** Patch/fixed commit/issue-PR kimlikleri ve cevabı doğrudan gösteren metadata incelenmeli. Kamuya açık model eğitim verisindeki kontaminasyonun sıfır olduğu iddia edilmemeli; yapılan denetim ve kalan risk açıkça kaydedilmeli.
7. **Bağımsız kör puanlama paneli:** Kök neden panelini ve kanıt yeterliliği panelini farklı pseudonymous reviewer ID’leri oluşturmalı. İki panelin kimlikleri kesişmemeli; böylece kanıt puanlayıcıları gizli gold kök nedeni görmemeli.
8. **Son kabul kararı:** Formdaki eksik alan, bilinmeyen karar veya hash eksikliği otomatik onay değildir. Yalnızca tüm vaka kapıları tamamlandıktan sonra sicil kaydı hazırlanır; global preflight yine en az 60 bağımsız kabul edilmiş vaka ve en az 8 upstream proje şartını arar (hedef 80).

## Sonuç sınıfları

- `not_run`: test henüz denenmedi.
- `environment_error`: ortam/kurulum hedef hata gösterimini geçersiz kılıyor; vaka geçmez.
- `target_failure_reproduced`: hedef regresyon testi buggy sürümde hedeflenen hata biçimiyle başarısız.
- `target_test_passed`: aynı test fixed sürümde geçiyor.
- `not_reviewed`: insan incelemesi yapılmadı.
- `accepted_for_confirmatory=true`: sadece nihai insan kararı ve kanıtlar kaydedildikten sonra; kuyruk veya CI otomatik bunu asla yapmaz.

## Kırmızı çizgi

GitHub Actions'ın yeşil olması, modelin iyi sonuç vereceği veya vakanın bilimsel olarak kabul edildiği anlamına gelmez. Form doldurmak, kayıt imzalamak veya bir kanıt referansı eklemek kendi başına doğrulama değildir; hakem kararının gerekçesi ve dayanağı saklanmalıdır.
