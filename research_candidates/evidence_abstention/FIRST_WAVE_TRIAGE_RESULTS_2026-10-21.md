# İlk dalga teknik tarama — sonuç ve karar

**Tarih:** 21 Ekim 2026  
**Dal:** `research/evidence-abstention-draft-2026-10-19`  
**GitHub Actions:** [Run 39644280706](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39644280706)  
**Karar:** İş akışı ve artefakt denetimleri tamamlandı; hiçbir vaka ana deney havuzuna kabul edilmedi. Model çıkarımı yapılmadı.

## Ne doğrulandı?

Yedi teknik tarama işi de GitHub Actions içinde tamamlandı. Her vaka için ham günlükler, hedef testin sayısal çıkış kodları, özet ve artefakt denetimi üretildi. Artefakt hash kontrolleri çalışma sırasında geçti. Bu, doğrulama iş akışının çalıştığına dair kanıttır; vakaların araştırma ölçütlerini karşıladığının kanıtı değildir.

| Vaka | Otomatik tarama sinyali | Otomatik denetimde ortam/harness uyarısı | Karar |
|---|---|---|---|
| BugsInPy-black-2 | Buggy-fail/fixed-pass ham işareti var | Hayır | İnsan incelemesi gerekli; kalıcı dışlama |
| BugsInPy-fastapi-1 | Ham işaret var | Evet | Buggy başarısızlığı hedef hataya bağlanamaz; kalıcı dışlama |
| BugsInPy-luigi-1 | Tam çift işareti yok | Evet | Geçerli test çifti gösterilemedi; kalıcı dışlama |
| BugsInPy-sanic-1 | Ham işaret var | Evet | Buggy başarısızlığı hedef hataya bağlanamaz; kalıcı dışlama |
| BugsInPy-scrapy-1 | Buggy-fail/fixed-pass ham işareti var | Hayır | İnsan incelemesi gerekli; kalıcı dışlama |
| BugsInPy-thefuck-1 | Tam çift işareti yok | Evet | Geçerli test çifti gösterilemedi; kalıcı dışlama |
| BugsInPy-tornado-1 | Buggy-fail/fixed-pass ham işareti var | Hayır | İnsan incelemesi gerekli; kalıcı dışlama |

“Ortam/harness uyarısı yok” ifadesi yalnızca otomatik örüntü denetiminin bu uyarıyı üretmediği anlamına gelir; insan tarafından kök neden doğrulaması veya vaka kabulü değildir. Üç ham olumlu işaret de kaynak kodu, test davranışı ve düzeltme diff'i üzerinden ayrıca incelenmeden geçerli kabul edilemez.

## Örnekleme ve kontaminasyon kararı

Bu yedi vaka, doğrulama iş akışını kurarken hedef testleri ve sonuç örüntülerini incelemek amacıyla kullanıldı. Bu nedenle **ana doğrulayıcı analizden kalıcı olarak dışlanır**. Önceden belirtilen dışlama listesi genişletilmeden bu vakalar tekrar aday havuzuna alınmayacaktır.

- Bu run sonrasında kabul edilmiş bağımsız doğrulayıcı vaka: **0**
- Farklı upstream proje sayısına sahip kabul edilmiş vaka: **0**
- Model çıkarımı: **yapılmadı**
- Etki büyüklüğü, McNemar testi veya güven aralığı: **hesaplanmadı**; deney verisi yoktur.

## Aşama kararı

**Teknik doğrulama alt işi tamamlandı. Veri doğrulama aşaması tamamlanmadı.** Metadata envanterindeki kayıtların ham sayısı, çalışan buggy-fail/fixed-pass test çiftlerinin sayısı değildir. Sıradaki gerekli iş, önceden açığa çıkarılmış vakalardan bağımsız adayları belirlemek; kaynak ve lisansı, tekrarlanabilir test çiftini, kök neden kanıtını, E1/E2/E3 paketlerinin geçerliliğini ve sızıntı/ön maruziyet koşullarını bağımsız biçimde denetlemektir. İki ayrı, birbirinden bağımsız değerlendirici paneli olmadan hiçbir vaka `accepted_for_confirmatory=true` olarak işaretlenmemelidir.

Bu kayıt hiçbir model performansı veya bilimsel hipotez sonucu iddia etmez.