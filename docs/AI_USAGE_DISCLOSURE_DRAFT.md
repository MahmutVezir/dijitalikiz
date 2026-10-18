# Üretken Yapay Zekâ Kullanım Beyanı — TASLAK

**Durum:** Başvuru öncesinde öğrenci tarafından gözden geçirilmeli, gerçek kullanım kayıtlarıyla doğrulanmalı ve 2026–2027 TYBS alanlarıyla eşleştirilmelidir. Nihai beyan yerine doğrudan kopyalanmamalıdır.

## Taslak beyan

Bu araştırmanın geliştirme sürecinde OpenAI ChatGPT, destekleyici bir araştırma ve yazılım geliştirme aracı olarak kullanılmıştır. Kullanım kapsamı; araştırma sorusunun ve deney planının açıklığa kavuşturulması, alternatif deney tasarımlarının değerlendirilmesi, Python kodu ve otomatik test taslaklarının hazırlanması, GitHub Actions doğrulama akışlarının hata ayıklanması, veri bütünlüğü kontrollerinin ve araştırma belgelerinin hazırlanması ile rapor dilinin gözden geçirilmesini içermektedir. Ayrıca bazı sentetik yazılım-test örnekleri ve doğrulama yardımcı betikleri ÜYZ desteğiyle hazırlanmıştır; bunlar ampirik model performansı verisi olarak kullanılmamış ve test amaçlı oldukları açıkça işaretlenmiştir.

Pilot ve doğrulayıcı deneydeki model yanıtları, sabitlenen Qwen/Qwen2.5-3B-Instruct modelinin dondurulmuş deney koşullarında ürettiği kayıtlardır. ChatGPT tarafından yazılan kod ve değerlendirme yardımcıları, bu kayıtları oluşturmak için kullanılan deney çalıştırıcısından ayrıdır. Dondurulmuş ham yanıtlar sonradan değiştirilmemiştir; sonuçların raporlanmasında temel alınan dosya ve hash kayıtları korunmuştur. Mevcut birincil ölçüt her iki koşulda da taban etkisi göstermiştir ve araştırmanın anlamsal hipotezini doğrulamamıştır. Bu nedenle ÜYZ desteği, hipotezi doğru göstermek için veri seçmek veya sonuçları yönlendirmek amacıyla kullanılmamıştır.

ÜYZ tarafından önerilen kod, test, açıklama ve metinler tek başına doğrulanmış bilimsel kanıt olarak kabul edilmemelidir. Kaynakların, uygulamanın, veri kökeninin, analizlerin ve nihai yorumların doğruluğunu kontrol etme; projenin yöntemini ve sınırlılıklarını anlama ve çalışmayı değerlendirme kuruluna bağımsız biçimde açıklama sorumluluğu başvuru sahibi öğrenci(ler)e aittir. Bu beyan, başvuruda kullanılan tüm ÜYZ araçları ve gerçek kullanım kapsamı son kez kontrol edilerek tamamlanacaktır.

## Başvuru öncesi kontrol listesi

- [ ] TÜBİTAK'ın güncel rehberini oku: https://tubitak.gov.tr/tr/kurumsal/hakkimizda/uretken-yapay-zeka-rehberi
- [ ] TYBS'deki ÜYZ kullanımı alanlarını kontrol et ve istenen beyanı o alanlara uygun şekilde yap.
- [ ] Bu taslakta yer alan her iddianın gerçek kullanım süreciyle örtüştüğünü doğrula; eksik veya hatalı ifadeleri düzelt.
- [ ] Kullanılan tüm ÜYZ araçlarını doğru adlarıyla ve destek kapsamıyla belirt.
- [ ] ChatGPT tarafından yazılan kod ve testlerin öğrenci tarafından incelendiğini, çalıştırıldığını ve açıklandığını doğrula; henüz yapılmadıysa yapılmış gibi yazma.
- [ ] İnsan tarafından doğrulanmamış aday değerlendirmelerini veya semantik etiketlemeyi tamamlanmış hakem incelemesi olarak tanıtma.
- [ ] Gizli erişim anahtarları, özel hesap bilgileri, kişisel veriler veya gizli verileri ÜYZ sistemlerine girmediğini doğrula.
- [ ] Nihai rapor, ekler ve başvuru formundaki beyanın birbiriyle tutarlı olduğundan emin ol.

## Kapsam sınırı

Bu dosya bir taslaktır; tek başına TÜBİTAK kurallarına uyumun kanıtı veya doldurulmuş başvuru beyanı değildir. TÜBİTAK, önemli ölçüde ÜYZ kullanımının şeffaf biçimde beyan edilmesini ve ortaya çıkan içeriğin doğruluğu, özgünlüğü ve etik uygunluğu için başvuru sahibinin sorumluluk almasını öngörür.


## Kapsam güncellemesi — 18 Ekim 2026

Bu taslak, aşağıdaki güncel geliştirme faaliyetleri de gerçek kullanımla karşılaştırılarak değerlendirilmelidir:

- ChatGPT (GPT-6), takip çalışmasının A/B/C bilgi-paritesi kurallarını, kaynak-vaka kabul kapılarını ve TÜBİTAK 2204-A uygunluk kontrol matrisini hazırlamak/düzenlemek için destek aracı olarak kullanıldı.
- V2 bağlam render'larının eşitliği ve kaynak/ground-truth sızıntısını sınayan Python test taslakları oluşturuldu ve no-inference CI ile kontrol edildi.
- İki bağımsız puanlayıcının gerçek değerlendirmeleri geldiğinde tam uzlaşma ve Cohen kappa hesaplamak amacıyla geçici bir yardımcı Python aracı ve sentetik birim testleri prototiplendi. Kod incelemesinde, projenin mevcut `scripts/validate_scoring_calibration.py` doğrulayıcısının daha kapsamlı, manifest ve kaynak kanıtına bağlı tek kalibrasyon kapısı olduğu belirlendi; yinelenen prototip PR #61 ana dala alınmadan kapatıldı. Mevcut doğrulayıcıda asgari 0,80 tam uzlaşma ve 0,70 Cohen kappa eşiklerinin aşağı çekilmesini engelleyen ek sertleştirme PR #65'te test ediliyor. Bu geliştirmeler gerçek puan, uzlaşma veya adjudication üretmedi.
- Sabitlenmiş upstream commit, regresyon testleri, lisans/NOTICE dosyaları ve CI artefaktlarının bazı masa başı teknik kontrolleri ve bu kontrollerin dokümantasyonu için destek kullanıldı. Bunlar bağımsız insan kaynak incelemesi, hakemlik veya yasal görüş yerine geçmez.
- Kaynak denetiminde bulunan ve açıkça belirtilen test blokajları kapatılmış gibi sunulmadı. Yeni V2 model çıkarımı, eğitim, GPU ya da Kaggle koşusu bu yardım faaliyetleriyle başlatılmadı.

Bu maddeler, nihai beyanın yerine otomatik olarak kopyalanacak hazır doğruluk iddiaları değildir. Öğrenci, gerçekten kullanılan araç/sürüm, hangi rapor bölümü veya süreç aşamasında yardım alındığı ve son olarak hangi değişikliklerin kendi kontrolünden geçtiğini doğrulamalı; yanlış, eksik ya da yapılmamış bir işi anlatan maddeyi düzeltmeli veya kaldırmalıdır.
