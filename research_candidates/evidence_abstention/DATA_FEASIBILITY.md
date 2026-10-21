# Aşama 2 — Veri fizibilitesi ve vaka seçimi

**Denetim tarihi:** 20 Ekim 2026  
**Aşama sonucu:** Kaynak-kümesi fizibilitesi için **koşullu geçiş**.  
**Kapsam:** Kamuya açık veri kaynakları, upstream metadata yapısı, birkaç kayıt örneğinin şema denetimi ve dahil etme/dışlama kuralları. Bu belge, her vaka için testlerin fiilen çalıştırıldığı anlamına gelmez.

## 1. Karar özeti

**Birincil aday kaynak: BugsInPy.** İnceleme anındaki upstream master commit'i 11c5f1eea954a42132cfd06bf257766a7963e0fd altında 17 proje klasöründe 501 hata klasörü sayıldı. Her örnek için bug.info, bug_patch.txt ve çalışma betikleri gibi dosyalar bulunması, kontrollü bir vaka havuzu oluşturmayı uygulanabilir kılıyor. BugsInPy'nin amacı gerçek dünya Python kusurlarını kontrollü ve tekrarlanabilir araştırmalar için sunmaktır. Resmî depo: https://github.com/soarsmu/BugsInPy

**Önemli sınır:** 501, ham kayıt sayısıdır; deney kabul koşullarını geçen vaka sayısı değildir. Bu aşamada hiçbir vaka için bug/fixed testlerinin uçtan uca çalıştırıldığı iddia edilmiyor.

**Yedek kaynak: Defects4J 3.0.1.** Resmî depo 854 etkin ve 10 kullanımdan kaldırılmış hata kaydı bildiriyor. Hata raporu, buggy/fixed commit, değiştirilmiş sınıflar ve tetikleyici test metadata'sı gibi faydalı alanları vardır. Java 11 ve zaman dilimi dâhil çalışma ortamı hassasiyetleri bulunduğundan, BugsInPy yeterli sayıda geçerli vaka sağlamazsa alternatif olarak düşünülmelidir. Kaynak: https://github.com/rjust/defects4j

**Birincil kaynak olarak seçilmeyen: SWE-bench Verified.** Bu benchmark issue-to-patch çözme görevine odaklanır; doğrudan kanıt yeterliliğiyle kök neden teşhisi ölçmek için hazırlanmış değildir. Ayrıca 23 Şubat 2026 tarihli OpenAI denetimi, özellikle modelin sık başarısız olduğu ve incelenen 138 problemin en az %59,4'ünde test tasarımı veya problem tanımına ilişkin önemli sorunlar bulunduğunu raporlamış; veri/çözüm kontaminasyonu hakkında da uyarıda bulunmuştur. Bu oran 500 örneğin tamamına genellenmemelidir. Kaynak: https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/

## 2. BugsInPy ham kayıt sayımı

Sayımlar upstream API'deki proje klasörleri ve her projenin bugs klasörleri üzerinden yapıldı. Bu, ham klasör sayımıdır; test başarısı veya lisans uygunluğu sayımı değildir.

| Proje | Hata klasörü |
|---|---:|
| PySnooper | 3 |
| ansible | 18 |
| black | 23 |
| cookiecutter | 4 |
| fastapi | 16 |
| httpie | 5 |
| keras | 45 |
| luigi | 33 |
| matplotlib | 30 |
| pandas | 169 |
| sanic | 5 |
| scrapy | 40 |
| spacy | 10 |
| thefuck | 32 |
| tornado | 16 |
| tqdm | 9 |
| youtube-dl | 43 |
| **Toplam** | **501 / 17 proje** |

Pandas ham havuzun yaklaşık üçte birini oluşturduğu için, yalnızca en büyük projeden örnekleme yapmak doğru olmaz. Vaka seçimi birden fazla projeyi kapsamalı ve analizde proje kümelenmesini dikkate almalıdır.

## 3. Kayıt biçimi için sınırlı teknik örnek denetimi

Aşağıdaki kayıtlar, kaynak formatını ve gerekli metadata öğelerini kontrol etmek için açıldı. Bunlar **teknik format örnekleridir; nihai araştırma örneklemi değildir**. Dosya/patch incelemesine maruz kaldıkları için doğrulayıcı deneyde kullanılmamalıdırlar.

| Vaka | Metadata'da görülen bilgiler | Bu aşamadaki sonuç |
|---|---|---|
| BugsInPy black, bug 1 | Python 3.8.3; buggy/fixed commit kimlikleri; tests/test_black.py; özel test çalıştırma betiği; patch dosyası | Metadata biçimi mevcut. Test yürütülmedi; lisans, güncel ortam ve kontaminasyon incelemesi yapılmadı. Nihai deneyden hariç. |
| BugsInPy tqdm, bug 1 | Python 3.6.9; buggy/fixed commit kimlikleri; tqdm/tests/tests_contrib.py; hedefli pytest komutu; patch dosyası | Metadata biçimi mevcut. Test yürütülmedi; lisans, güncel ortam ve kontaminasyon incelemesi yapılmadı. Nihai deneyden hariç. |
| BugsInPy youtube-dl, bug 1 | Python 3.7.0; buggy/fixed commit kimlikleri; test/test_utils.py; hedefli unittest komutu; patch dosyası | Metadata biçimi mevcut. Test yürütülmedi; depo/bağımlılık durumu, lisans ve kontaminasyon incelemesi yapılmadı. Nihai deneyden hariç. |
| BugsInPy httpie, bug 1 | Python 3.7.3; buggy/fixed commit kimlikleri; tests/test_downloads.py; hedefli pytest komutu; patch dosyası | Metadata mevcut, ancak eski depo URL'si yönlendirme/taşınma nedeniyle ek kaynak çözümlemesi gerektiriyor. Nihai deneyden hariç. |

Makine tarafından erişilen metadata dosyalarındaki buggy_commit_id, fixed_commit_id, test_file, Python sürümü ve test betiği alanları; kontrollü vaka oluşturmanın ön koşullarına işaret eder. Ancak bu alanlar tek başına kök nedenin tekil olduğunu ya da testin bu çalışma ortamında bugün geçip kaldığını kanıtlamaz.

## 4. Vaka kabul protokolü

Bir vaka ana deney havuzuna ancak tüm zorunlu kapılardan geçerse alınabilir:

1. **Kaynak ve lisans:** Kaynak depo, kullanılan commit'ler ve ilgili proje lisansı kayıt altına alınır. Veri kümesi deposu için tek bir kapsayıcı lisans varsayılmaz; kaynak kod/patch bu araştırma deposuna kopyalanmaz, yalnızca gereken atıf ve metadata saklanır.
2. **Sürüm doğrulama:** Buggy ve fixed commit'ler erişilebilir ve birbirinden farklı olmalıdır. Fixed commit'in gerçekten belirtilen upstream hatayı düzelttiği incelenmelidir.
3. **Tekrarlanabilir test:** Aynı hedefli test, buggy sürümde beklenen hatayı göstermeli ve fixed sürümde geçmelidir. Çevre/bağımlılık kaynaklı ilgisiz test hatası vakayı geçersiz kılar.
4. **Kök neden kanıtı:** Kök neden kaynak kodu, test davranışı ve düzeltme diff'i üzerinden yazılı olarak gerekçelendirilmelidir. Gerekirse iki bağımsız değerlendirici kullanılır. Birbirinden bağımsız birden fazla kök nedeni olan vakalar dışlanır veya ayrı alt vakalara bölünmesi gerekçelendirilir.
5. **Kanıt seviyelerinin geçerliliği:** E1 (yeterli), E2 (kısmi) ve E3 (yetersiz) paketleri, model çıktıları görülmeden hazırlanır. Bir vakadaki paketler arasında yalnızca önceden tanımlanan kanıt öğeleri değişmelidir; sahte veya hatalı kanıt eklenmez. E2/E3'te birden fazla makul açıklamanın hâlâ mümkün olduğu bağımsız biçimde doğrulanmalıdır.
6. **Sızıntı kontrolü:** Model girdisinden gold patch, fixed commit, PR/issue kimliği, çözülmüş test adı, açıklayıcı test adı ve doğrudan cevabı gösteren metadata çıkarılır. Yine de kamusal eğitim verisiyle kontaminasyonun sıfır olduğu iddia edilemez.
7. **Örnek bağımsızlığı:** Aynı kök nedeni, aynı upstream PR'ı veya aynı hata ailesini temsil eden kopyalar bağımsız vaka sayılmaz. Aynı vaka tekrarları da bağımsız örnek olarak sayılmaz.
8. **Kayıt ve tekrar üretilebilirlik:** Her vakaya değişmez bir ID, veri kaynağı, buggy/fixed revizyonları, ortam sürümleri, test günlüklerinin hash'leri, dışlama nedeni ve veri paketi hash'leri atanır.

## 5. Örneklem hedefi ve durdurma kuralı

Aşama 3 tasarımı, ana araştırma için önceki fizibilite eşiğinden daha katı bir hedef belirledi:
- **Hedef: 80 kabul edilmiş bağımsız vaka; doğrulayıcı alt sınır: 60 vaka ve en az 8 ayrı upstream proje.**
- Bu sayılara yalnızca buggy-fail/fixed-pass, lisans, gold root cause, E1/E2/E3 kanıt yeterliliği ve sızıntı kontrolünden geçmiş vakalar dâhildir; 501 ham kaydın tamamı dâhil sayılmaz.
- N<60 veya 8 projeden az durumda çalışma doğrulayıcı kabul edilmeyecek, keşifsel/fizibilite olarak raporlanacak. Sonuç görüldükten sonra gevşek kurallarla örnek doldurulmayacak.
- N=80 hedefi, Aşama 3 analiz planındaki varsayımsal McNemar güç duyarlılığına dayanır; küçük etkileri saptama garantisi değildir.

## 6. CI smoke kontrolü ve tamamlanmayan doğrulama

CI üzerinde iki ayrı aday denendi:
- **PySnooper-1:** Python 3.8.18 kurulumu sonrasında sözde buggy commit hedef regresyon testini geçti. Beklenen buggy-fail/fixed-pass çifti sağlanmadı; aday reddedildi.
- **tqdm-1:** ilk denemede fixed tarafı test dosyası geçişinden dolayı başarısız oldu. Hata kaydı, yanlış kaynak dosyasının yüklenmesi olasılığını gösterdi. İş akışına repo checkout'undan kaynak import eden açık `PYTHONPATH` eklendi. Sonraki CI çalışmasında buggy revision'da hedef test başarısız, fixed revision'da aynı test başarılı oldu: [başarılı smoke run](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759). Bu yalnızca bir teknik smoke doğrulamasıdır; kaynak metadata Python 3.6.9 kaydederken CI Python 3.8.18 kullandı. Bu sebeple **tam sürüm ortamında yeniden üretim doğrulanmadı** ve vaka, önceki metadata/patch incelemesi nedeniyle doğrulayıcı örneklemden kalıcı olarak dışlanır.

İlk denemelerde Python 3.8.1, Ubuntu 24.04 runner'ında bulunmadığından setup aşamasında başarısızlık yaşandı; bu da hata yeniden üretimi sayılmaz. İlgili kayıtlar:
- https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460135014
- https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460540758
- https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759

Sonuç: **bir vaka çifti smoke koşullarında çalıştı; doğrulayıcı deney için kabul edilmiş vaka sayısı hâlâ sıfır olarak kaydedilir.** En az 60 vaka/8 proje için her vaka özelinde doğru buggy/fixed revizyon, kayıtlı ortam sürümü, lisans, gold root cause, kanıt seviyeleri ve sızıntı incelemesi gerekir.

## 7. Aşama 2 nihai kararı

**Veri kaynağı fizibilitesi: GEÇTİ (koşullu).** Yeterli büyüklükte bir ham Python hata havuzu ve kullanılabilir sürüm/test metadata'sı bulundu.

**Doğrulanmış deney veri kümesi: HENÜZ HAZIR DEĞİL.** Bu aşamada 60 bağımsız vakanın ve 8 ayrı projenin kabul koşullarını geçtiği iddia edilemez; smoke dışında vakaların test çiftleri fiilen doğrulanmadı, proje lisansları tek tek doğrulanmadı ve model eğitim verisi kontaminasyonu sıfırlanmadı.

**Aşama 2 kararı: KAYNAK FİZİBİLİTESİ TAMAMLANDI (KOŞULLU) — OPERASYONEL VAKA DOĞRULAMA KAPISI GEÇİLMEDİ.** Şu ana kadarki smoke adaylarından hiçbiri kabul edilmedi; 60 bağımsız vaka / 8 proje doğrulanmış değildir. Model çıkarımı kapalıdır. Bir sonraki aşama tasarım olarak tamamlanabilir, ancak deney yürütmeye hazır değildir.


## 8. Sonraki operasyonel doğrulama yolu

Kaynak dokümantasyonu, BugsInPy'nin kontrollü hata yeniden üretimi için `bugsinpy-checkout`, `bugsinpy-compile` ve `bugsinpy-test` komutlarını ve ortamı sabitlemek için Docker kullanımını tarif eder ([resmî upstream README](https://github.com/soarsmu/BugsInPy/blob/11c5f1eea954a42132cfd06bf257766a7963e0fd/README.md)). Bu nedenle önceki smoke'ta görülen Python 3.6.9/3.8.18 farkı kabul edilebilir standart değildir.

Her yeni aday için: (1) metadata ve kaynak/lisans kaydı, (2) belirtilen ortamı kurma veya farkı gerekçeli ve açıkça raporlama, (3) aynı hedef testin buggy sürümde beklenen kusuru göstermesi ve fixed sürümde geçmesi, (4) günlüklerin hash'lenmesi, (5) kök neden ile E1/E2/E3 kanıt paketlerinin en az iki bağımsız inceleyici tarafından model çıktısından önce doğrulanması, (6) sızıntı ve maruziyet kontrolü uygulanır. Başarısızlık ortam/kurulum kaynaklıysa “buggy fail” olarak sayılmaz; aday reddedilir veya araştırma örnekleminden ayrı, açık bir teknik sorun olarak tutulur.

Ölçek hedefi değişmedi: **en az 60 kabul edilmiş vaka ve 8 upstream proje, hedef 80**. Bu belge yayınlı upstream komutlarını kaydedip doğrulama planını netleştirir; 60 vakanın çalıştırıldığını iddia etmez. Örneklem eşiği sağlanana kadar Aşama 2'nin veri-kabul kapısı açık kalır ve Aşama 4 LLM çıkarım kapısı kapalı tutulur.


## 9. Metadata envanteri otomasyonu — 21 Ekim 2026

Ham havuzun tamamını tutarlı biçimde taranabilir hale getirmek amacıyla scripts/inventory_bugsinpy_candidates.py ve birim testleri eklendi. .github/workflows/evidence-abstention-metadata-inventory.yml, BugsInPy revizyonu 11c5f1eea954a42132cfd06bf257766a7963e0fd üzerinde bug.info, project.info, bug_patch.txt, run_test.sh ve setup.sh dosyalarına ilişkin SHA-256 bütünlük özetlerini ve temel metadata alanlarını CSV envanterine çıkarır.

Bu otomasyon yalnızca metadata envanteri üretir:
- buggy/fixed testlerini çalıştırmaz;
- kök neden veya kanıt seviyelerini değerlendirmez;
- lisans, eğitim verisi kontaminasyonu veya sızıntı incelemesi yapmaz;
- LLM çağırmaz ve hiçbir vakayı kabul edilmiş deney verisi olarak işaretlemez;
- daha önce maruz kalınan beş fizibilite örneğini kalıcı dışlama olarak işaretler.

Başarılı envanter üretimi, 501 ham metadata kaydının listelenebildiğini gösterebilir; 501'in de, herhangi bir alt kümenin de doğrulayıcı deney için uygun olduğunu göstermez. CI artifact'ı geldiğinde ilk kullanım amacı metadata eksikliği ve kaynak/proje dağılımını tarayarak insan ve ortam doğrulaması için yeni, önceden incelenmemiş adayları seçmektir. Aşama 2'nin operasyonel kabul kapısı 60 bağımsız vaka ve 8 proje doğrulanana kadar açık kalır.


## 10. Gerçek metadata envanteri sonucu — 21 Ekim 2026

[GitHub Actions envanter çalışması](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618065599) pinned BugsInPy revizyonunda başarıyla envanter ve artifact üretti. Sonuç raporu: [METADATA_INVENTORY_RESULT_2026-10-21.md](METADATA_INVENTORY_RESULT_2026-10-21.md).

| Çıktı | Sonuç |
|---|---:|
| Ham metadata vaka kaydı | 501 |
| Upstream proje | 17 |
| Temel metadata kapısı geçen | 500 |
| Temel metadata kapısı geçmeyen | 1 |
| Test çifti fiilen doğrulanan | 0 |
| Kabul edilmiş doğrulayıcı vaka | 0 |

Metadata kapısını geçemeyen tek kayıt **BugsInPy-keras-12**: kaynak metadata aynı Git commit'ini buggy ve fixed olarak göstermektedir. Kayıt sessizce kabul edilmedi; dışlama/inceleme gerektiren metadata sorunu olarak tutuldu. İş akışı beş önceden incelenmiş örneği de kalıcı dışlama olarak etiketledi.

Envanter CSV'sinin SHA-256 değeri 069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb olarak kaydedildi. CSV metadata ve dosya hash'leri içerir; patch/source code kopyası, insan kök-neden kararı veya test sonuçları içermez.

**Aşama 2 kararı değişmedi:** metadata kaynak envanteri tamamlandı; operasyonel vaka doğrulama kapısı hâlâ açık. 501 ham kayıt, 500 metadata-kalifiye aday, 60 doğrulanmış vaka veya deney örneklemi olarak raporlanamaz.


### 10.1 Smoke tekrar denetimi uyarısı

Daha önceki [run 39461858759](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39461858759) bir kez buggy-fail/fixed-pass verdiği için olumlu tek koşu olarak kaydedilmişti. Ancak 21 Ekim'deki yeniden çalıştırma [run 39618666531](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618666531), buggy revizyonda beklenen hata gözlendikten sonra fixed revizyondaki hedef testi **başarısız** buldu: TypeError: 'int' object is not subscriptable (tqdm/tests/tests_contrib.py::test_enumerate). Dolayısıyla bu smoke sonucu tekrarlanabilir değildir; önceki tek olumlu çalıştırma bir kabul ölçütü olarak kullanılamaz. Metadata Python 3.6.9 kaydederken her iki smoke koşusu da Python 3.8.18 kullandı. Vaka zaten incelenmiş olduğu için doğrulayıcı örneklemden kalıcı olarak dışlanmaya devam eder.

Bu bulgu otomasyon/ortam farkını çözmez. Smoke workflow artık her belge değişikliğinde otomatik çalışmayacak; yalnızca elle dispatch edildiğinde çalıştırılabilir. Eski denemelerin kayıtları saklanır.
