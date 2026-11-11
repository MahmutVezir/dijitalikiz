# V11 Batch 0 — vaka denetimi (11 Kasım 2026)

## Kapsam ve karar

Bu kayıt, BugsInPy'nin sabitlenmiş `11c5f1eea954a42132cfd06bf257766a7963e0fd` sürümünden önceden belirlenmiş 100 adaylık tarama havuzunun ilk sekiz teknik adayını kapsar. Sekiz aday sekiz ayrı upstream projeden seçilmiştir. Seçim sırası test sonuçları görülmeden dondurulmuştur; örneklem rastgele değildir ve doğrulayıcı veri kümesi değildir.

- Teknik vaka arşivlerinin SHA-256 bütünlüğü: **8/8 geçti**.
- Buggy sürüm başarısız / fixed sürüm başarılı teknik sinyali: **5 aday**.
- Test başlamadan ortam/kurulum engeli: **3 aday**.
- Doğrulayıcı vaka siciline kabul: **0**.
- Model çıkarımı veya eğitimi: **yapılmadı**.
- Lisans, kök neden, kanıt seviyesi, sızıntı ve bağımsız insan incelemeleri: **tamamlanmadı**.

Makine tarafından üretilen başarılı workflow sonucu, her hedef testin başarılı olduğu veya bir vakanın bilimsel olarak kabul edildiği anlamına gelmez. Vaka bazlı sonuç ve arşiv kimliklerinin tekil kaydı `V11_RUN13_EVIDENCE_INDEX_2026-11-11.json` dosyasındadır.

## Beş teknik sinyal

| Vaka | Python | Buggy / fixed hedef test çıkışı | Teknik gözlem |
|---|---:|---:|---|
| Ansible-7 | 3.6.9 | 1 / 0 | VLAN değiştirmede buggy sürüm istenmeyen ek `no name` komutu üretti. |
| Black-9 | 3.8.3 | 1 / 0 | Python 2 tarzı `print(a, file=sys.stderr)` ifadesi buggy parser'da işlenemedi. |
| FastAPI-9 | 3.8.3 | 1 / 0 | OpenAPI gövde şeması beklenen `application/vnd.api+json` yerine `application/json` verdi. |
| Keras-8 | 3.7.3 | 1 / 0 | Paylaşılan katmanlı heterojen derinlik grafında concatenate şekilleri uyuşmadı. |
| Scrapy-7 | 3.8.3 | 1 / 0 | URL yolundaki boşluk buggy sürümde `%20` olarak kaldı; sabit sürüm hedef testi geçti. |

Bunlar yalnızca mühendislik düzeyinde buggy/fixed ayrımı sinyalidir. Kaynak kod yamalarının ve test davranışının bağımsız uzmanlarca incelenmesi gerekir.

## Üç ortam engeli

| Vaka | Engel | Sonuç |
|---|---|---|
| Luigi-8 | Test toplama sırasında `ModuleNotFoundError: No module named 'luigi'`; kaynak paketi sanal ortama kurulmamıştı. | Bug sonucuna çevrilemez; proje paketi kurulumu için düzeltme hazırlandı. |
| Matplotlib-7 | Eski easy_install yolu NumPy 2.5.4 kaynak arşivinden `setup.py` bulamadı. | Hedef test başlamadı; rastgele NumPy sürümü pinlenmedi. |
| Pandas-6 | Eski C uzantısı GCC 13'te `-Werror=array-bounds` nedeniyle derlenemedi; ardından pytest eklentisi yerel pandas uzantısını içe aktaramadı. | Hedef test başlamadı; yalnızca bu uyarıyı hata olmaktan çıkaran kontrollü compiler bayrağı eklendi. |

## Bu denetimden çıkan kod düzeltmeleri

1. **Luigi kaynak kurulumu:** Matris oluşturucu artık Black ve Matplotlib gibi Luigi için de kaynak paketi kurulumunu işaretliyor. Regresyon testi eklendi.
2. **Pandas derleme uyumluluğu:** Yalnızca Pandas adayında hem buggy hem fixed derlemesine `-Wno-error=array-bounds` ekleniyor; kullanılan bayrak vaka arşivine yazılıyor. Diğer derleyici uyarıları için genel bir susturma yapılmıyor.
3. **Kısaltılmış Git SHA karşılaştırması:** BugsInPy metadata'sındaki 7+ karakterlik kısaltma, checkout'tan gelen tam SHA'nın gerçek önekiyse eşleşme kabul ediliyor. Başka SHA'lar hâlâ uyarı üretiyor. İki regresyon testi eklendi.
4. **Runner pipe hatası:** Önceki koşudaki `make --version | head -n 1` / `pipefail` kaynaklı SIGPIPE, `sed -n '1p'` ile daha önce düzeltilmişti; 11 Kasım V11 ana dal koşusu bu düzeltmeden sonra tamamlandı.
5. **Kanıt arşivleme:** Her vaka için kaynak repository URL'si, commit kimlikleri, test komutu, sonuç sınıfı, artifact kimliği ve SHA-256 kalıcı JSON siciline yazılıyor.

Bu değişiklikler `research/2026-11-11-v11-durable-case-audit-fixes` dalında hazırlanmıştır. PR ve otomatik test sonuçları ayrıca kontrol edilmelidir.

## Saklama ve lisans

GitHub Actions arşivlerinin tamamı 11 Aralık 2026 tarihinde sona erecek. Kalıcı JSON sicili proje deposunda kalır; ancak bu sicil ham logların veya üçüncü taraf kaynak kodunun yerini tutmaz. Üçüncü taraf projelerin tam kaynak kodu ve worktree patch dosyaları, ilgili lisans koşulları incelenmeden `dijitalikiz` deposuna kopyalanmayacaktır. Bunun yerine upstream repo adresi ve tam commit kimlikleriyle kaynak tekrar üretilebilir biçimde sabitlenir.

Bu nedenle “sekiz vaka sonsuza dek ham dosyalarıyla saklandı” denemez. Şu anda garanti edilen şey, seçim ve sürüm provenansının, test komutlarının, teknik durumun ve arşiv SHA-256 referanslarının tek özel depo içindeki kalıcı kaydıdır. Ham GitHub artifact dosyaları son kullanma tarihinden önce indirilmelidir.

## Bilimsel kapı

Mevcut durumda hiçbir vaka doğrulayıcı veri kümesine alınmamıştır. Sıradaki kapılar: (i) lisans ve yeniden dağıtım kontrolü, (ii) iki bağımsız inceleyicinin buggy/fixed commit ve kök neden onayı, (iii) hedef testin gerçekten hata mekanizmasını ölçtüğünün doğrulanması, (iv) E1/E2/E3 kanıt seviyelerinin kör değerlendirme ile sınıflandırılması, (v) sızıntı ve önceki maruziyet kontrolü, (vi) protokol ve prompt hash'lerinin ön kayıtla dondurulmasıdır.

En az 60 bağımsız kabul edilmiş vaka ve en az sekiz upstream proje eşiği sağlanmadan model çıkarımı başlatılmamalıdır. Eşiği karşılamak için vaka ölçütleri sonuçlar görüldükten sonra gevşetilmemelidir.
