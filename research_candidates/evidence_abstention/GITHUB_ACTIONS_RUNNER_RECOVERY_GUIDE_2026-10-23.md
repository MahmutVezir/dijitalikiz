# GitHub Actions runner kurtarma ve V10 doğrulama rehberi

**Tarih:** 23 Ekim 2026  
**Amaç:** V10 metadata doğrulama iş akışının gerçekten runner üzerinde çalıştığını kanıtlamak. Bu rehber bilimsel vaka kabulü veya model çalıştırma izni değildir.

## Gözlenen durum

V10 metadata tekrarlanabilirlik iş akışı: [run 39985336539](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39985336539). İlk denemede iş başarısız görünmesine rağmen GitHub API adım listesini boş döndürdü ve log indirme çağrısı BlobNotFound ile sonuçlandı. Failed jobs yeniden çalıştırıldı; run yeniden tamamlanmış/başarısız duruma geldi ancak yine adımlar ve yüklenmiş artefaktlar görünmüyordu.

**Yorum sınırı:** Bu kayıt ne kontrol betiğinin başarılı ne de başarısız test edildiğini gösterir. Runner adımı yoksa test adımı çalışmış sayılmaz. Bu rehber hesap/billing/izin kaynaklı bir nedenin bulunduğunu iddia etmez; aşağıdaki maddeler olası işletim engellerini denetleme sırasıdır.

## 1. Depo sahibinin kontrol etmesi gerekenler

1. Depo → **Actions** → **Evidence abstention V10 metadata reproducibility** iş akışını aç.
2. En yeni çalıştırmayı aç; işin runner'a atanıp atanmadığına, **Steps** listesinin boş olup olmadığına ve logların açılıp açılmadığına bak.
3. Depo → **Settings → Actions → General** bölümünde GitHub Actions'ın etkin olduğunu, organizasyon/depo politikasının iş akışını engellemediğini ve gerekli eylemlere izin verildiğini kontrol et. İş akışı yalnızca contents: read izni ister.
4. Depo özel olduğundan, hesabın/organizasyonun **Billing & plans / Actions** kullanım ve dakika sınırlarını kontrol et. Burada bir engel olduğu henüz kanıtlanmış değildir; yalnızca doğrulanması gereken olası bir sebeptir.
5. Depodaki iş akışı ubuntu-latest GitHub-hosted runner kullanır; özel bir self-hosted runner grubuna ihtiyaç duymaz.
6. Gerekirse V10 iş akışını GitHub Actions arayüzünden **Run workflow** ile yeniden başlat. Gerçek adımlar görünmeden “CI geçti” veya “kod testi bozuk” sonucu çıkarma.

## 2. Başarılı bir uzak çalıştırma ne göstermeli?

Uzak run içinde aşağıdaki adımlar görünmeli:

1. Repository checkout ve Python 3.11 kurulumu.
2. Metadata inventory, queue, intake, V10 gate ve pytest bootstrap regression test logları.
3. BugsInPy kaynağının sabit revizyona (11c5f1eea954a42132cfd06bf257766a7963e0fd) checkout edilmesi.
4. 501 satırlı envanterin, 407 satırlı kuyruğun ve sabit 100 adaylık V10 intake'in yeniden oluşturulması.
5. V10 verifier raporunun üretimi ve içeriğinin indirilip incelenebilmesi.

Beklenen temel sabitler:
- Inventory SHA-256: 069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb
- Queue SHA-256: 91c926665752e0e44c6a4ba499422d2af23c6156f4d61b675e29ca0288a27ece
- V10 intake: 100 ID, 14 upstream proje.
- Seçilen intake ile 93 kimlikli geçmiş maruziyet birleşiminin kesişimi: 0.

Ayrıca evidence-abstention-v10-builder-diagnostics ve evidence-abstention-v10-reproducibility adlı artefaktların oluştuğu kontrol edilmeli. Artefakt yoksa job başarılı kabul edilmez.

## 3. Bu iş akışının sınırı

Bu iş akışı yalnızca metadata oluşturucularını ve doğrulayıcıyı test eder. Buggy/fixed upstream test çiftlerini çalıştırmaz, LLM yüklemez, model çıktısı üretmez ve vaka sicilini kabul edilen vakalarla doldurmaz. Uzak doğrulamanın geçmesi de tek başına bilimsel vaka kabulü değildir.

## 4. Runner düzeldikten sonraki sıra

1. Önce yalnızca V10 metadata iş akışını geçir ve ham loglar/artefakt hash'lerini denetle.
2. Ardından teknik aday taraması için ayrı, açıkça seçilmiş V10 teknik batch çalıştırma adımlarını kullan. Başka bir workflow'u doğrulamak için açılan adaylar doğrulayıcı örneklemden kalıcı çıkarılır.
3. Her adayın buggy-fail/fixed-pass çıktısı, runtime eşleşmesi, artefakt hash'leri ve bağımsız Panel A/Panel B kararları tamamlanmadan vaka siciline kabul kaydı ekleme.
4. En az 60 bağımsız kabul edilmiş vaka / 8 upstream proje, sabit protokol, exact model-runtime ve ayrı yürütme izni gerçekleşmeden doğrulayıcı model çıkarımı başlatma.

**Kayıt durumu:** Runner sebebi belirlenmiş değildir. Buradaki kontrol adımları depo sahibinin GitHub arayüzünden doğrulaması içindir; hiçbir adımın yapılmış olduğu varsayılmaz.
