# Araştırma adayı: Kanıt yetersizliğinde yazılım hata teşhisi ve cevaptan kaçınma

**Durum:** Fikir ve literatür taraması aşamasında. Ön kayıt değildir; deney yürütülmemiştir.

**Önemli ayrım:** Bu klasör, DİJİTALİKİZ'in dondurulmuş TÜBİTAK araştırmasının parçası değildir. Mevcut pilot/confirmatory sonuçlarını, kodu, manifestlerini veya raporunu değiştirmez. Bu klasör ayrı bir Git dalında tutulur; ana dala birleştirilmesi ya da mevcut TÜBİTAK başvurusuna eklenmesi önerilmez.

## Araştırma fikri

Gerçek yazılım kusurlarında, teşhis için sunulan kanıt kontrollü olarak azaltılır. Modelden ya her durumda tek bir kök neden önermesi ya da kanıt yetersiz olduğunda cevap vermekten kaçınabilmesi istenir. İnceleme, yalnızca modelin gerçek kök nedeni tahmin edip etmediğini değil, yanıtının sunulan kanıtla desteklenip desteklenmediğini de ayırır.

**Önerilen çalışma başlığı:** Gerçek Yazılım Hatalarında Kanıt Yetersizliği Altında Büyük Dil Modellerinin Cevaptan Kaçınma Güvenilirliği

## Literatür taramasından ilk sonuç

Genel LLM abstention, kanıt yeterliliği ve kod üretiminde görevden kaçınma başlıklarında yakın çalışmalar mevcuttur. Bu nedenle genel “model ne zaman cevap vermemeli?” sorusu özgün katkı olarak sunulamaz. Olası dar katkı, kaynakları ve düzeltilmiş kök nedenleri bağımsız biçimde doğrulanmış gerçek yazılım hatalarında, kanıt eksiltmenin teşhis desteği ve cevap/kaçınma kararına etkisini ölçmektir. Bunun da özgünlüğü henüz kesinleşmiş değildir; daha sistematik bir tarama gerekir.

## Planlanan araştırma ayrımı

- **Görev:** Kod üretimi değil, gerçek yazılım hatasının kök nedenini teşhis etme.
- **Müdahale:** Her hata için kanıt paketini önceden belirlenmiş üç düzeyde kontrollü ve kademeli olarak azaltma.
- **Karşılaştırma:** Zorunlu teşhis istemi ile kanıt yetersizliğinde kaçınmaya izin veren istem.
- **Değerlendirme:** Teşhis doğruluğu ile verilen yanıtın mevcut kanıt tarafından desteklenmesini ayrı ayrı puanlama.
- **Ana birim:** Bağımsız yazılım hatası. Aynı hata üzerindeki tekrar üretimleri ayrı bağımsız vakalar sayılmaz.

## Mevcut çalışma için güvenlik sınırları

1. DİJİTALİKİZ'in TÜBİTAK 2204-A raporu ve mevcut doğrulama işleri önceliklidir. Bu aday yüzünden mevcut projeye yeni deney/özellik eklenmemelidir.
2. Yeni vaka havuzu; DİJİTALİKİZ'in tarihsel pilot, confirmatory, kalibrasyon ve daha önce teknik olarak incelenmiş adaylarından ayrı olmalıdır.
3. Bu taslak için model çıkarımı, eğitim, Kaggle/GPU işi veya yeni sonuç üretimi yapılmamıştır.
4. Örneklem büyüklüğü, model revizyonu, istatistik ve karar eşikleri kaynak taraması, veri fizibilitesi ve ayrı bir pilot planı tamamlanmadan dondurulamaz.
5. Genel abstention alanında veya yazılım kod üretiminde ilk olma iddiası yapılmayacaktır.

## Dosyalar

- LITERATURE_REVIEW.md — yakın çalışmalar ve ön özgünlük değerlendirmesi.
- PROTOCOL_DRAFT.md — aday araştırma sorusu, deney tasarımı, değerlendirme ve ilerleme kapıları.

Bu klasörün durumu yalnızca araştırma taslağıdır. Hiçbir deney sonucu, insan hakemliği veya dış akademik onay iddia edilmemektedir.
