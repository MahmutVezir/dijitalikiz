# Protokol taslağı — Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ

**Durum:** Araştırma taslağı; ön kayıt değildir. Deney yürütülmedi. Model çıkarımına izin verilmemiştir.  
**Proje:** Belirsizlik Altında Cevap Vermekten Kaçınan Yapay Zekâ  
**Depo sınırı:** Bu araştırma DİJİTALİKİZ'in eski TÜBİTAK deneylerinden ayrı yürütülür. Ana proje verileri ve sonuçları değiştirilmez.

## 1. Problem

Büyük dil modelleri yazılım hata raporlarından kök neden teşhisi üretebilir. Kanıt eksikken kesin görünen ancak desteklenmeyen açıklamalar vermeleri mümkündür. Bu yüzden teşhisin gizli gerçek kök nedenle örtüşmesi ile teşhisin modelin gördüğü kanıt tarafından desteklenmesi ayrı kavramlardır.

## 2. Araştırma soruları

**RQ1 (birincil):** Bağımsız değerlendiricilerin kanıtı yetersiz bulduğu yazılım hata vakalarında, cevap vermekten kaçınmaya izin veren politika, zorunlu teşhis politikasına kıyasla kanıtla desteklenmeyen kesin teşhis oranını azaltır mı?

**RQ2:** Kanıt yeterli, kısmi ve yetersiz düzeylere kontrollü biçimde indirildiğinde teşhis doğruluğu, kanıtsal destek, yanıt kapsamı ve uygun kaçınma nasıl değişir?

**RQ3 (ikincil):** Model kaçındığında, teşhis için gerekli ayırt edici eksik kanıtı doğru tanımlayabilir mi?

## 3. Önceden belirlenmiş hipotez taslağı

- **H1:** Yetersiz kanıt koşulunda kaçınmaya izin verilen politika, kanıtla desteklenmeyen kesin teşhis oranını azaltır.
- **H2:** Kanıt azaldıkça kanıtla desteklenen teşhis oranı düşer; kaçınma oranının artması beklenebilir ancak garanti değildir.
- **H3 (keşifsel):** Kaçınma sırasında istenen ek kanıt, bağımsız değerlendiricilerin belirlediği ayırt edici kanıtla örtüşür.

Nihai hipotezler, sistematik literatür taraması ve protokol incelemesi tamamlanınca deney sonuçları görülmeden dondurulur.

## 4. Taslak deney tasarımı

### Kanıt seviyeleri

- **E1 — Yeterli:** Kaynaklarla doğrulanmış kök nedeni makul alternatiflerden ayırmak için yeterli kanıt.
- **E2 — Kısmi:** Önceden belirlenen ayırt edici kanıt öğelerinden bir veya daha fazlası çıkarılmış.
- **E3 — Yetersiz:** Birden fazla makul kök neden mümkün; güvenilir tek teşhis, bağımsız değerlendiricilerce kanıtlanamıyor.

Mümkün olduğunda paketler iç içe tasarlanır: E3, E2'nin; E2, E1'in alt kümesidir. Kanıt seviyeleri model çıktısına bakılmadan etiketlenir.

### Karşılaştırılan politikalar

- **P0 — Zorunlu teşhis:** Model mevcut kanıttan tek bir en olası kök neden önermelidir.
- **P1 — Seçici teşhis:** Kanıt destekliyorsa teşhis verir; yetersizse açıkça kaçınır ve hangi kanıtın gerekli olduğunu belirtir.

Aynı model, aynı vaka, aynı üretim ayarları ve eşleştirilmiş istem şablonları kullanılmalıdır. Prompt dışında kasıtlı fark bırakılmamalıdır.

## 5. Vaka seçimi ve doğrulama

Vaka ancak şu koşullarda kabul edilebilir:
- Açık kaynak lisansı ve kaynak deposu belirlenebilir.
- Hata pre-fix revizyonda hedefli testle yeniden üretilebilir.
- Fixed revizyonda aynı test beklenen biçimde geçer.
- Kök neden kod, test ve düzeltme kanıtıyla doğrulanabilir.
- Kanıt paketleri model davranışına bakmadan hazırlanabilir.
- Vaka, DİJİTALİKİZ'in pilot, confirmatory, kalibrasyon ve önceden incelenmiş adaylarından bağımsızdır.

Model girdisinden issue/PR kimlikleri, upstream bağlantılar, fixed commit, patch, çözülmüş test adı ve gold label çıkarılmalıdır. Bunun modelin eğitim verisinde hiç bulunmadığını kanıtlamadığı açıkça raporlanır.

## 6. Değerlendirme

En az iki bağımsız değerlendirici önerilir. Kaynak-kodla ground truth, kanıt yeterliliği ve model yanıtı puanlaması birbirinden ayrılmalıdır. Mümkün olduğunda yanıt puanlayıcıları politika koşuluna körlenir.

Her yanıt için ayrı kaydedilecek boyutlar:
1. **Karar:** teşhis / açık kaçınma / biçim dışı veya kararsız.
2. **Teşhis doğruluğu:** doğru / kısmen doğru / yanlış / puanlanamaz.
3. **Kanıtsal destek:** sunulan kanıtla destekli / gerçek kök nedenle örtüşse de kanıtla desteklenmiyor / çelişkili-desteksiz / kararsız.
4. **Eksik kanıt isteği:** ayırt edici / kısmen ilgili / ilgisiz / uygulanamaz.

İkinci bir LLM veya anahtar kelime eşleştirmesi, kaynak kanıtı ve insan değerlendirmesinin yerine geçmez.

## 7. Ölçütler ve istatistik

**Birincil sonlanım:** E3 koşulunda kanıtla desteklenmeyen kesin teşhis oranı; P0 ile P1 arasında eşleştirilmiş karşılaştırma.

**İkincil sonlanımlar:** desteklenen teşhis oranı, gerçek kök neden doğruluğu, uygun kaçınma, E1'de gereksiz kaçınma, yanıt kapsamı, seçici hata ve istenen ek kanıtın uygunluğu.

İstatistik planı, bağımsız vaka birimini korumalıdır; aynı vakaya ait tekrarlar bağımsız örnek sayılmaz. Güven aralığı, eşleştirilmiş test/bootstrap yöntemi, çoklu karşılaştırma yaklaşımı ve eksik/bozuk çıktılar için kurallar önceden belirlenmelidir.

Örneklem ve birincil analiz taslağı Aşama 3 belgelerinde belirlenmiştir: hedef 80 bağımsız vaka; doğrulayıcı alt sınır 60 vaka ve en az 8 upstream proje. Ayrıntı için STAGE3_EXPERIMENT_DESIGN.md, ANALYSIS_PLAN_STAGE3.md ve EXPERIMENT_MANIFEST_STAGE3.json geçerlidir. Bu hedefler, vaka kabul kapıları geçilmeden örneklemin hazır olduğu anlamına gelmez.

## 8. Model ve yürütme kapıları

Model revizyonu, tokenizer, chat template, runtime, donanım, quantization, sıcaklık, top-p, token sınırı, prompt hash'leri, rastgele sıra, yeniden deneme kuralları, veri manifesti ve analiz kodu ayrı bir dondurulmuş protokolde kaydedilmelidir.

Aşağıdakiler tamamlanmadan inference yapılmaz:
1. Sistematik literatür taraması ve yakın çalışma karşılaştırması.
2. Bağımsız vaka havuzunun lisans/provenance ve kaynak-kod doğrulaması.
3. Kanıt yeterliliği etiketlerinin model çıktısından bağımsız insan incelemesi.
4. Rubrik ve değerlendirici kalibrasyonu.
5. Örneklem/güç analizi, birincil ölçüt ve istatistik planı.
6. Model/prompt/runtime dondurması ve checksum kontrolleri.
7. Danışman/araştırmacı protokol incelemesi.

## 9. Geçerlilik tehditleri

Eğitim verisi sızıntısı; birden fazla olası kök neden; kanıt seviyesinin öznel olması; isteme özgü sonuçlar; tek modelden genelleme yapma; vaka ve dil çeşitliliğinin sınırlılığı; aynı vakadaki tekrar bağımlılığı ve puanlayıcıların politika koşulunu tahmin edebilmesi.

## 10. DİJİTALİKİZ ile sınır

DİJİTALİKİZ bağımlılık bilgisinin temsil biçiminin hata teşhisine etkisini inceler. Bu yeni proje kanıt yeterliliği ve cevap/kaçınma kararını inceler. Araştırma soruları ayrı olsa da aynı genel alana yakındırlar; bu nedenle veri, kod, puanlama ve istatistik dosyaları otomatik olarak yeniden kullanılamaz.

Yeni proje bu depoda ayrı dalda yürütülür. DİJİTALİKİZ'in ana dalı ve mevcut TÜBİTAK raporu bu çalışma için değiştirilmez. Yeni proje için henüz deney sonucu veya başarı iddiası yoktur.

## 11. Kaynaklar

- Wen et al. (2025), *Know Your Limits: A Survey of Abstention in Large Language Models*. https://aclanthology.org/2025.tacl-1.26/
- Madhusudhan et al. (2025), *Do LLMs Know When to NOT Answer?* https://aclanthology.org/2025.coling-main.627/
- Zhang & Wu (2026), *Do LLMs Know When Evidence is Insufficient?* https://www.techscience.com/cmc/v89n1/68467
- Zhai et al. (2026), *Abstain-R1*. https://aclanthology.org/2026.findings-acl.985/
- Zhou et al. (2026), *Task Abstention for Large Language Models in Code Generation*. https://arxiv.org/abs/2605.17029
- Sharma & David (2025), *Assessing Correctness in LLM-Based Code Generation via Uncertainty Estimation*. https://arxiv.org/abs/2502.11620
- Torun et al. (2026), *Evaluation of LLM-Based Software Engineering Tools*. https://arxiv.org/abs/2604.24621

## 12. Aşama 2 — veri kaynağı fizibilitesi ve vaka kabul kapısı

20 Ekim 2026 tarihli veri-kaynağı denetimi, birincil aday olarak BugsInPy'yi seçti. Upstream master ref'i 11c5f1eea954a42132cfd06bf257766a7963e0fd sabitlenmişken 17 proje altında 501 ham hata klasörü sayıldı. Bu ham sayı, deney kriterlerini geçen vaka sayısı değildir. Denetimin özeti DATA_FEASIBILITY.md; format örnekleri FEASIBILITY_FORMAT_SAMPLE.csv dosyasındadır.

### Kaynak kararı
- **Birincil aday:** BugsInPy (Python; 17 proje; 501 ham hata klasörü).
- **Yedek:** Defects4J (Java; 854 etkin, 10 kullanımdan kaldırılmış hata kaydı bildiriliyor; ortam sürümü ve zaman dilimi dikkat gerektirir).
- **Birincil kaynak olarak kullanılmayacak:** SWE-bench Verified; issue-to-patch görevine odaklıdır ve 2026 tarihli denetimde kontaminasyon/test kalitesi riskleri bildirilmiştir.

### Vaka kabul kapısı
Her vaka için buggy ve fixed commit'leri, hedefli test, kaynak proje lisansı, kök neden açıklaması, kanıt seviyeleri ve veri sızıntısı kontrolü kayıt altına alınmadan örnek havuzuna kabul yapılmaz. Test, izole ortamda buggy sürümde beklenen fail sonucunu ve fixed sürümde pass sonucunu göstermelidir. İki revizyonda farklı, ilgisiz çevresel hata varsa vaka kabul edilmez. E1/E2/E3 kanıt paketleri model çıktıları görülmeden hazırlanır ve bağımsız biçimde incelenir.

Hedef, en az 40 kabul edilmiş bağımsız hata; asgari uygulanabilirlik eşiği ise en az 30 vaka ve en az 5 upstream projedir. Bu, istatistiksel güç garantisi değildir. Eşik karşılanmazsa sonuçlar görüldükten sonra kabul kuralları gevşetilmez.

Dört kayıt üzerinde yalnızca metadata/format kontrolü yapıldı: BugsInPy black-1, tqdm-1, httpie-1 ve youtube-dl-1. Patch dosyalarına bakıldığı için bu dört vaka doğrulayıcı deneyden kalıcı olarak dışlanır. Hiçbirine runtime testi uygulanmadı. Bu araç ortamında Docker bulunmadığından ve kaynak kayıtlar eski Python sürümleri istediğinden buggy/fixed test çifti burada yürütülemedi.

**Aşama 2 kararı:** Kaynak-kümesi fizibilitesi koşullu olarak geçti; doğrulanmış deney veri kümesi henüz hazır değil. Vaka düzeyindeki tekrarlanabilirlik, lisans ve sızıntı kapıları kapanana kadar model çıkarımı yasaktır.


## 13. Aşama 3 — deney tasarımı bağlantıları ve kilit

Aşama 3 tasarımı şu yeni belgelerde yer alır:
- `STAGE3_EXPERIMENT_DESIGN.md` — E1/E2/E3 × P0/P1 eşleştirilmiş deney tasarımı.
- `PROMPT_CONDITIONS.md` — politika dışındaki prompt öğelerini sabit tutan P0/P1 istemleri.
- `OUTPUT_SCHEMA.json` — ham cevap/kaçınma çıktısı için JSON sözleşmesi.
- `ANALYSIS_PLAN_STAGE3.md` — birincil sonlanım, exact McNemar/RD/CI ve örneklem duyarlılığı.
- `EXPERIMENT_MANIFEST_STAGE3.json` — hedef 80; en az 60 doğrulanmış vaka, en az 8 proje; `case_ids=[]` ve `inference_allowed=false`.

Aşama 3, **tasarım belgelendirmesi olarak tamamlandı**; bu, ön kayıt veya model çalıştırma izni değildir. BugsInPy-tqdm-1 smoke denemesi Python 3.8.18 ile buggy-fail/fixed-pass verdi fakat veri metadata'sı Python 3.6.9 kaydetti ve vaka ön incelemeye maruz kaldı; bu nedenle ana örnekleme dahil edilmez. Doğrulayıcı veri kümesi onaylanana, E1/E2/E3 paketleri ve puanlama kuralları hash ile dondurulana kadar LLM inference kapalıdır. Repo ayrımı için `REPO_SCOPE_SPLIT.md` ve iki klasördeki `MANIFEST.json` dosyaları yetkilidir.
