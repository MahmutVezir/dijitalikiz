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

CI üzerinde iki adayın test çifti smoke olarak denendi; hiçbiri vaka kabul kapısını geçmedi:
- **PySnooper-1:** Python 3.8.18 kurulumu sonrasında sözde buggy commit hedef regresyon testini geçti. Bu, beklenen buggy-fail/fixed-pass çiftinin sağlanmadığını gösterir; aday reddedildi.
- **tqdm-1:** buggy sürümde test beklenen şekilde başarısız oldu; ancak fixed sürümde aynı test `TypeError: 'int' object is not subscriptable` ile başarısız oldu. Ayrıca runtime Python 3.8.18 iken metadata Python 3.6.9 kaydediyor. Bu nedenle aday kabul edilmedi; sabitlenmiş test/ortam eşleşmesi yeniden incelenmeden tekrar denenmiş sayılmaz.

İlk denemelerde Python 3.8.1, Ubuntu 24.04 runner'ında bulunmadığından setup aşamasında başarısızlık yaşandı; bu da hata yeniden üretimi sayılmaz. Çalıştırma kayıtları:
- https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460135014
- https://github.com/MahmutVezir/dijitalikiz/actions/runs/39460540758

Bu CI sonuçları, BugsInPy kaynağının varlığını değil, bu iki örneğin henüz bu çalışmanın doğrulayıcı vaka şartlarını sağlamadığını gösterir. Her aday için doğru test-revision eşleşmesi, buggy-fail/fixed-pass, exact runtime, lisans ve ground-truth/sızıntı kapısı gerekir.

## 7. Aşama 2 nihai kararı

**Veri kaynağı fizibilitesi: GEÇTİ (koşullu).** Yeterli büyüklükte bir ham Python hata havuzu ve kullanılabilir sürüm/test metadata'sı bulundu.

**Doğrulanmış deney veri kümesi: HENÜZ HAZIR DEĞİL.** Bu aşamada 30 veya 40 vakanın kabul koşullarını geçtiği iddia edilemez; testler fiilen yürütülmedi, proje lisansları tek tek doğrulanmadı ve model eğitim verisi kontaminasyonu sıfırlanmadı.

**Aşama 2 kararı: KAYNAK FİZİBİLİTESİ TAMAMLANDI (KOŞULLU) — OPERASYONEL VAKA DOĞRULAMA KAPISI GEÇİLMEDİ.** Şu ana kadarki smoke adaylarından hiçbiri kabul edilmedi; 60 bağımsız vaka / 8 proje doğrulanmış değildir. Model çıkarımı kapalıdır. Bir sonraki aşama tasarım olarak tamamlanabilir, ancak deney yürütmeye hazır değildir.
