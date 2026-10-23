# Proje güncel durumu ve en az aşamalı yürütme planı

**Tarih:** 23 Ekim 2026  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**TÜBİTAK hedefi:** 2027 TÜBİTAK 2204-A  
**Karar:** Proje hedefi korunuyor; bilimsel deney tamamlanmış değil. Bu belge, güncel durum ve sonraki işleri tek yerde toplar; ön kayıt veya deney sonucu değildir.

## Yönetici özeti

Projenin araştırma sorusu, hedefli literatür notları, deney tasarımı, veri tarama/çıkarma kuralları ve yazılım prototipi büyük ölçüde belgelendi. Ancak **0 kabul edilmiş bağımsız vaka, 0 doğrulayıcı model çıktısı, tamamlanmamış insan incelemeleri, boş kalibrasyon verisi ve doğrulanmamış tam CUDA/runtime yüklemesi** nedeniyle araştırma hipotezi hakkında sonuç verilemiyor.

Bir önceki mühendislik smoke çalışmasında 10 çıktı (P0: 5; P1: 5) üretildi fakat iki koşulda da 0/5 açık kaçınma görülmüştü. Bu çalışma maruziyet, prompt sızıntısı ve runtime uyumsuzluğu nedeniyle doğrulayıcı çalışmadan dışlanmıştır; yalnızca mühendislik tanılamasıdır. Ayrıntı: [EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md](EXPLORATORY_ENGINEERING_REPORT_2026-10-23.md).

## Ne tamamlandı?

- Araştırma sorusu ve aday bilimsel katkı tanımlandı; literatür taramasının hedefli olduğu ve özgünlüğün kanıtlanmadığı açıklandı.
- BugsInPy sabit revizyonunda 501 ham metadata kaydı / 17 upstream proje envanteri oluşturuldu; bu kabul edilmiş örneklem değildir.
- 100 aday / 13 proje içeren metadata-only V9 intake üretildi. V9 offset-0 ve offset-8 taramalarında incelenen toplam 16 vaka, teknik iş akışının doğrulamasında kullanıldıkları için doğrulayıcı örneklemden kalıcı biçimde dışlandı. Bu intake'te kalan adaylar da yalnızca metadata adayıdır.
- Qwen yapılandırılmış yanıt adapter'ı, katı JSON ayrıştırma, çoklu aday entropy/lexical disagreement sinyalleri, kalibrasyon arayüzü, Brier/ECE metrikleri, kanıt paketi/hash auditor'ı ve fail-closed inference kapısı oluşturuldu.
- Karar katmanı; kanıt desteği/çelişki sinyalleri veya kalibrasyon eksikse teşhis üretmek yerine kaçınıyor.
- Semantik auditor prompt/parser arayüzü ve adapter eşlemesi eklendi; giriş doğrulamaları da sıkılaştırıldı. Modülün 12 sentetik birim testi izole yerel koşuda geçti. Bu, GitHub Actions'ın/adapter'ın tam test paketinin geçtiği veya anlamsal kararların insan puanlarına göre doğru olduğu anlamına gelmez; gerçek Qwen auditor çağrısı ve kör insan doğrulaması hâlâ yapılmadı. Ayrıntı: [SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md](SEMANTIC_EVIDENCE_AUDIT_PROTOCOL_2026-10-23.md).
- Tarihsel DİJİTALİKİZ/CCDG veri ve sonuçları yeni araştırmadan ayrıldı; bunlar yeni çalışmanın kanıtı olarak kullanılmayacak.

## Ne kaldı?

| Blokaj | Mevcut durum | Kapanış ölçütü |
|---|---|---|
| Doğrulayıcı vaka havuzu | 0 kabul | En az 60 bağımsız vaka, en az 8 upstream proje; hedef 80. Her vaka için aynı hedef testte buggy-fail/fixed-pass ve gerçek kayıtlı Python sürümü. |
| Kök neden/provenance | Tam bağımsız inceleme yapılmadı | Her vaka için iki bağımsız insan incelemesi, lisans/kök neden/patch-test ilişkisi ve uyuşmazlık kaydı. |
| E1/E2/E3 kanıt yeterliliği | Tamamlanmadı | Farklı ve bağımsız iki kişilik kör panel; altın kök neden ve koşul etiketi gösterilmeden paket onayı. |
| Semantik auditor | Arayüz eklendi; doğrulanmadı | Ayrı kalibrasyon vakalarında kör insan puanlarına karşı validasyon; bilinen yanıt/etiket sızıntısı olmaması. |
| Model/runtime | Aday kilitli fakat doğrulanmadı | Tam Qwen/tokenizer revision, chat template, Python/PyTorch/Transformers/CUDA ayarları ve yükleme artefaktı kontrolü. |
| Güven kalibrasyonu | Veri boş | Bağımsız etiketli calibration split, önceden belirlenmiş metrik/eşik seçimi, hash ile dondurma. |
| Ön kayıt ve izin | Taslak/kapalı | Son protokol ve hash manifesti sonuçlar görülmeden denetlenebilir kayıtla yayımlanmalı; ayrıca açık yürütme izni. |
| CI/runner | Son durum için tüm test adımları kanıtı tamamlanmış değil | Gerçek runner atanmalı, yeni birimin test logu ve iş artefaktı incelenmeli. İş runner'a başlamadıysa “test geçti” sayılmaz. |
| Resmî rapor | Final sonuçlar yok | Yöntem, gerçek sonuç, sınırlılıklar, dışlamalar, kaynakça ve resmi şablon kontrolü. |
| Başvuru uygunluğu | Öğrenci/ekip beyanı gerekiyor | Son çağrı koşullarını ve daha önceki/benzer yarışma başvurularını öğrenci ve danışman kayıtlarından doğrulama; bunu otomatik doldurmak mümkün değil. |

## En az sayıda aşamayla tamamlama

### Aşama 1 — Veri, yöntem ve çalıştırma kapılarını kapat

1. GitHub Actions runner sorununu ayır: basit no-inference iş akışı gerçekten adımları çalıştırıyor mu? Sonra tüm birim testlerini çalıştır ve ham logu/arşivi denetle.
2. Tarama kuyruğunda önceden açılmamış vakaları belirlenmiş sırayla işle; teknik test sinyali verenleri otomatik kabul etme.
3. İki ayrık insan panelini fiilen oluştur ve vaka başına kaynak/lisans/kök neden/kanıt paketlerini gözden geçir.
4. Semantik auditor'ı ayrı bir kalibrasyon bölmesinde, kör insan değerlendirmelerine karşı doğrula. İnsan doğrulaması olmadan auditor sinyali “kalibre edilmiş güven” değildir.
5. Model/tokenizer/runtime'ı çıktı üretmeden denetle; tüm prompt, şema, analiz, vaka, calibration, auditor ve runtime dosyalarının hash'lerini dondur; protokolü sonuçlardan önce kaydet.
6. En az 60 kabul edilmiş bağımsız vaka / 8 proje şartı ve diğer kapılar sağlanmadan inference çalıştırma. 4 Kasım iç kontrolünde bu eşik sağlanmıyorsa açık bir go/no-go kararı al; eşiği sessizce gevşetme.

**Aşama 1 çıkışı:** audit edilebilir veri sicili, bağımsız değerlendirici kayıtları, geçerli kalibrasyon/runtime, hash manifesti, kayıtlı protokol ve açık izin.

### Aşama 2 — Deneyi yürüt ve bilimsel sonucu üret

1. Aynı sabit model ve runtime ile kabul edilen her vakada E1/E2/E3 × P0/P1 koşullarını çalıştır.
2. En az 60 vaka için 360, 80 vaka için 480 çıktının ham metnini, seed/prompt/kanıt hash'lerini, model sürümünü ve şema hatalarını sakla. Bunlar planlanan sayılardır, gerçekleşmiş çıktı sayısı değildir.
3. Koşullara kör bağımsız puanlama yap; kök neden doğruluğu, görünen kanıt desteği ve karar/kaçınma etiketlerini ayrı kaydet.
4. Önceden planlanmış birincil sonuç için eşleştirilmiş risk farkı, iki taraflı exact McNemar testi ve %95 güven aralığını hesapla; E1 gereksiz kaçınma ve yanıt kapsamını da raporla.

**Aşama 2 çıkışı:** gerçek veri, ham çıktılar, kör puanlama, istatistik, tekrarlanabilir analiz artefaktları ve sınırlılıklar.

### Aşama 3 — TÜBİTAK raporu ve teslim

1. Gerçek bulguları, sıfır/olumsuz sonuçları ve metodolojik sınırlılıklarıyla yaz.
2. 2026–2027 resmi proje raporu şablonuna yerleştir; başlık, özet, anahtar kelime, kaynakça, sayfa biçimi, izinler ve bütünlük kontrollerini resmî belgelerle doğrula.
3. Öğrenci, danışman ve ekip uygunluk beyanlarını tamamla; TYBS'de başvuruyu son günün öncesinde gözden geçir.

Resmî çağrı sayfasında başvuru dönemi 23 Eylül 2026–4 Ocak 2027; kapanış **4 Ocak 2027 saat 17.30 (Türkiye saati)** olarak ilan edilmiştir: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi. Yarışmaya başvurunun tamamlanmış proje üzerinden yapılması gerekir.

## Korunacak bilimsel kurallar

- Önceden incelenen teknik/debug vakaları doğrulayıcı örnekleme geri alınmaz.
- Ham aday sayısı, CI'ın yeşil olması, prompt yazılması ve sentetik birim testleri gerçek deney sonucu değildir.
- Yapısal hash/referans kontrolü, semantik destek doğrulaması değildir.
- Modelin kendi verdiği 0.95 gibi güven beyanları kalibre edilmiş olasılık sayılmaz.
- E1/E2/E3 altın etiketleri, gold kök neden ve patch çalışma zamanı kararına sızdırılmaz.
- Hipotez, birincil ölçüt veya dışlama kuralları sonuç görüldükten sonra değiştirilmez.
- Türkiye finalisti olma hedefi korunur ancak garanti verilemez.

## Nihai durum

**Yazılım prototipi var; bilimsel etkinlik henüz ölçülmedi.** En büyük dış bağımlılıklar bağımsız değerlendiriciler, yeterli ve kabul edilmiş gerçek vaka havuzu, semantik auditor validasyonu ve gerçek GPU/runtime doğrulamasıdır. Bu işler tamamlanmadan projeye “halüsinasyon azaltıldı” veya “hipotez doğrulandı” denmeyecektir.
