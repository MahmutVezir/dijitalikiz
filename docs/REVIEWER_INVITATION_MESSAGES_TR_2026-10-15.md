# Bağımsız değerlendirici davet mesajları (Türkçe)

**Koordinatör için:** A ve B mesajlarını iki farklı kişiye ayrı ayrı gönder. Her kişiye yalnızca kendi ZIP dosyasını ekle. Türkçe yönergeyi ayrı dosya olarak ekle. Bu belgedeki metin şablondur; henüz herhangi bir değerlendiricinin kabul ettiği veya puanlama yaptığı anlamına gelmez.

## Değerlendirici A

Merhaba. TÜBİTAK 2204-A araştırma projem kapsamında, yazılım hataları hakkında bir dil modelinin ürettiği yanıtları bağımsız biçimde değerlendirmem gerekiyor. Çalışma, önceden üretilmiş 160 yanıtın sonradan yapılan keşifsel değerlendirmesidir; senden model çalıştırmanı veya kod yazmanı istemiyorum.

Değerlendirmeye bağımsız olarak katkı sunabilir misin? Uygun olursan lütfen yalnızca sana özel A paketini ve Türkçe yönergeyi kullan. Her yanıt için yönergede belirtilen altı alanı doldurman, kısa bir kanıt gerekçesi yazman ve 160 kaydın tamamını bitirmen gerekiyor. Lütfen paket dışındaki kaynakları veya cevap anahtarını arama ve diğer değerlendiriciyle yanıtları tartışma. İlk puan dosyanı teslim ettikten sonra değiştirmemeni rica ediyorum.

Ekler: yalnızca sana atanmış A ZIP dosyası ve ayrı Türkçe yönerge dosyası. Lütfen A ZIP dosyasını başka kişiye iletme.

Bu değerlendirme tarihsel deneyin bilgi-eşitliği kusurunu geriye dönük gidermez ve tek başına CCDG'nin nedensel etkisini kanıtlamaz. Katılamayacaksan sorun değil; lütfen yalnızca uygun olup olmadığını bildir.

## Değerlendirici B

Merhaba. TÜBİTAK 2204-A araştırma projem kapsamında, yazılım hataları hakkında bir dil modelinin ürettiği yanıtları bağımsız biçimde değerlendirmem gerekiyor. Çalışma, önceden üretilmiş 160 yanıtın sonradan yapılan keşifsel değerlendirmesidir; senden model çalıştırmanı veya kod yazmanı istemiyorum.

Değerlendirmeye bağımsız olarak katkı sunabilir misin? Uygun olursan lütfen yalnızca sana özel B paketini ve Türkçe yönergeyi kullan. Her yanıt için yönergede belirtilen altı alanı doldurman, kısa bir kanıt gerekçesi yazman ve 160 kaydın tamamını bitirmen gerekiyor. Lütfen paket dışındaki kaynakları veya cevap anahtarını arama ve diğer değerlendiriciyle yanıtları tartışma. İlk puan dosyanı teslim ettikten sonra değiştirmemeni rica ediyorum.

Ekler: yalnızca sana atanmış B ZIP dosyası ve ayrı Türkçe yönerge dosyası. Lütfen B ZIP dosyasını başka kişiye iletme.

Bu değerlendirme tarihsel deneyin bilgi-eşitliği kusurunu geriye dönük gidermez ve tek başına CCDG'nin nedensel etkisini kanıtlamaz. Katılamayacaksan sorun değil; lütfen yalnızca uygun olup olmadığını bildir.

## Koordinatör için kontrol listesi

- Özel eşleme/anahtar JSON dosyalarını hiçbir değerlendiriciye gönderme veya depoya yükleme.
- Bir kişiye yalnızca A, diğerine yalnızca B ZIP'ini gönder.
- İki ilk değerlendirme dosyası kilitlenene kadar puanları veya cevap anahtarını paylaşma.
- Dönen JSONL dosyalarını ilgili orijinal ZIP'e karşı scripts/validate_semantic_review_submission.py ile doğrula.
- Bu aracın PASS sonucu yalnızca dosya tamlığı ve değişmez alanları gösterir; semantik doğruluk, bağımsızlık veya ground truth kanıtı değildir.
- İlk puanları koru; uyuşmazlık çözümünü ayrı bir adjudication kaydında tut.
