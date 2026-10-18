# TÜBİTAK 2204-A 2027 kılavuz uygunluk denetimi — 15 Ekim 2026

## Resmî kaynaklar

- Yarışma sayfası ve 2026–2027 çağrı duyurusu: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi
- 2027 Proje Rehberi (PDF): https://tubitak.gov.tr/sites/default/files/2026-09/lise_proje_rehberi_2027_onaya_sunulan.pdf
- 2026–2027 Çağrı metni (PDF): https://tubitak.gov.tr/sites/default/files/2026-09/Ek-1b_2204_A_cagri_metni_2026-2027_17.08.2026_onaya_sunulan_v2.pdf

## Doğrulanmış çağrı koşulları

Resmî yarışma sayfasında 2027 dönemi başvuru aralığı 23 Eylül 2026–4 Ocak 2027 olarak yayımlanmıştır. Sistem kapanışı 4 Ocak 2027 saat 17.30'dur. Başvuru TYBS üzerinden yapılır.

Çağrı metninin 4.2.4–4.2.6 maddelerinde:
- Raporun yarışma sayfasındaki **Proje Yazım Şablonu** kullanılarak Türkçe hazırlanması ve tek PDF olarak yüklenmesi,
- Raporun tüm başlıklarla birlikte **2–20 sayfa** olması,
- Özetin **150–250 kelime** olması,
- Proje adının **en fazla 15 kelime** olması
istenmektedir.

## Taslakta makineyle denetlenebilen ölçütler

TUBITAK_REPORT_DRAFT.md üzerindeki 15 Ekim 2026 sürümünde:
- Başlık 11 kelime: **uygun** (en fazla 15).
- Özet 191 kelime: **uygun** (150–250).
- Anahtar kelime satırında beş terim bulunuyor: **uygun** (2027 Proje Rehberi, §3.3, basılı s. 69; özetin altında en fazla beş kelimeden oluşan anahtar kelimeler isteniyor). Bu gereklilik resmî rehber PDF'sinden doğrulanmıştır; DOCX şablonunun görsel stilleri hâlâ incelenememiştir.
- Amaç, giriş, yöntem, bulgular, sonuç/tartışma, öneriler, kaynaklar ve ekler başlıkları bulunuyor.
- İlk denetimde ayrı bir içindekiler bölümü yoktu; bu güncellemede taslak gezinme amaçlı bir içindekiler listesi eklenmiştir. Nihai Word/PDF çıktısında gerçek sayfa numaralı içindekiler şablon içinde yenilenmelidir.
- Mevcut içerik Markdown'dır ve son şablonda dizgilenmiş PDF değildir. Bu nedenle sayfa sayısı, kenar boşlukları, yazı tipi, satır aralığı ve son PDF'nin 2–20 sayfa sınırında kaldığı henüz **doğrulanmış değildir**.
- Resmî sayfa, şablon indirme bağlantısı yayımlar. Bu oturumda bağlantıdan indirilebilir şablon dosyası alınamadı; GitHub Actions'taki fetch-official-template işi de çalıştırılmış adım olmadan başarısız oldu. Dolayısıyla rapor şablonla son biçimine getirilmiş gibi sunulmamalıdır.
- Nihai başvuru öncesinde tek PDF açılarak kontrol edilmeli; TYBS yüklemesinde belge adları, sayfa ve boyut sınırlamaları çağrı metnine göre ayrıca doğrulanmalıdır.

## Alan ve tematik alan uyumu

Resmî rehber, ana alanlar arasında **Yazılım**'ı saymaktadır. Tematik alanlar arasında **Yapay Zekâ** ve **Dijital İkiz** ayrı seçeneklerdir.

Rehberin “Dijital İkiz” açıklaması, fiziksel varlık/sistem/süreç ile sanal eşini ve sensörlerden gelen gerçek zamanlı verilerle sürekli güncellemeyi tarif eder. Mevcut proje ise sabit yazılım hata vakalarında bir LLM'ye sunulan bağlam temsillerini karşılaştıran, çevrimdışı ve statik bir deneydir; gerçek zamanlı sensör verisiyle güncellenen fiziksel sistem eşleniği oluşturmamaktadır. Bu nedenle **Ana Alan: Yazılım / Tematik Alan: Yapay Zekâ** seçimi mevcut tasarıma daha iyi uymaktadır. Bu bir kaynak temelli öneridir; nihai seçimin sorumluluğu başvuru sahiplerindedir ve başvuru sonrası değiştirilemez.

## Tarihsel ve insan değerlendirmesi durumuna ilişkin raporlama kısıtları

- Tarihsel birincil sonuçlar dondurulmuş kalır: her koşul 0/80, vaka düzeyinde 0/16, exact iki taraflı McNemar p=1,00, gözlenen eşleştirilmiş fark 0.
- İki kör paket bütünlük denetiminden geçmiştir; fakat değerlendirme alanları boştur. Gerçek insan puanı bulunmadığından semantik başarı oranı veya Cohen kappa raporlanamaz.
- İnsan puanları elde edilirse bunlar sonradan yapılan **post-hoc keşifsel** değerlendirme olarak ayrılacaktır; tarihsel birincil sonucu değiştirmeyecek ve bilgi-paritesi kusurunu düzeltmeyecektir.
- V2 protokolü status=draft, model_inference_permitted=false, boş vaka listesi ve tüm gerekli kapılar pending durumundadır. Yeni model çıkarımı yapılmış gibi gösterilemez.

## Çıkış kararı

Taslak, başlık ve özet uzunluğu gibi bazı metinsel gereklilikleri karşılıyor; ancak **nihai başvuru dosyası hazır değil**. Kalan zorunlu kalite kapıları: resmi yazım şablonuna aktarma, sayfa numaralı içindekileri yenileme, PDF sayfa ve açılabilirlik kontrolü, öğrenci tarafından tüm teknik iddiaların son doğrulaması, gerçek değerlendirici katılımı varsa alınan dosyaların denetimi ve en son TYBS yükleme kurallarının kontrolüdür.

## Sonradan eklenen durum düzeltmesi — 18 Ekim 2026

Bu denetimdeki “şablon indirilemedi ve biçimlendirme doğrulanmadı” cümleleri **15 Ekim'deki ara durumu** anlatır; güncel durum olarak okunmamalıdır. Resmî 2026–2027 Word şablonu daha sonra başarıyla alındı ve rapor yeniden derlendi. Son doğrulanmış derleme kaydı: [workflow run 38929963765](https://github.com/MahmutVezir/dijitalikiz/actions/runs/38929963765), artifact ID `12058990129`. İlgili ayrıntılı güncel denetim: `docs/TUBITAK_REPORT_BUILD_AUDIT_2026-10-16.md`.

Bu son derlemede rapor DOCX/PDF'si 10 sayfa olarak doğrulanıp görsel olarak incelendi. Bununla birlikte proje başvurusu henüz gönderilmiş değildir: öğrenci/okul/danışman bilgileri, kaynakların son insan kontrolü, ÜYZ kullanım beyanının gerçek kullanımla eşleşmesi ve TYBS başvuru alanları öğrenci/başvuru sahibi tarafından onaylanmalıdır. Bilimsel sonuç ve sınırlar değişmemiştir; Standard 0/80, CCDG 0/80 ve bilgi-paritesi kusuru korunur. V2 hâlâ taslak ve inference izni kapalıdır.
