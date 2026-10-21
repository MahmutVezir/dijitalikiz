# BugsInPy metadata envanteri — 21 Ekim 2026

**Kaynak revizyonu:** 11c5f1eea954a42132cfd06bf257766a7963e0fd  
**GitHub Actions:** [Evidence Abstention Metadata Inventory — run 39618065599](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39618065599)  
**Artifact:** evidence-abstention-bugsinpy-metadata-inventory (ID 12352753722; ZIP SHA-256: 119393370b22235e6eb56d79410e74c219507025b95a3979665cd4f3a2b01fb4)  
**Envanter CSV SHA-256:** 069e649a37a12cd495ad08a82377f76f0b4518b3fd138380321dc53b15663dcb  
**Özet JSON SHA-256:** c248f556399b2c229ac47b5824479509c984bac8b0d4570b408eabfca52fe4c0

## 1. Gerçekleşen otomatik sonuç

- Ham metadata envanterindeki hata kayıtları: **501**
- Kaynak projeleri: **17**
- Temel metadata alanları tamam görünen kayıtlar: **500**
- Temel metadata kapısını geçemeyen kayıtlar: **1**
- Önceden maruz kalınma nedeniyle kalıcı dışlanan fizibilite örnekleri: **5**
- Buggy-fail/fixed-pass test çifti bu iş akışında doğrulanan: **0**
- Lisans/ground-truth/E1-E2-E3/leakage incelemesi bu iş akışında tamamlanan: **0**
- Kabul edilmiş doğrulayıcı vaka: **0**
- LLM çıkarımı: **yapılmadı**

“Metadata tamam” ifadesi yalnızca Python sürümü, farklı buggy/fixed commit kimlikleri, test dosyası ve test komutu gibi asgari metadata alanlarının mevcut ve tutarlı olması anlamına gelir. Testin gerçekten çalıştığı, kök nedenin doğrulandığı veya vakanın araştırmaya alınabileceği anlamına gelmez.

## 2. Bulunan metadata sorunu

**BugsInPy-keras-12**, aynı commit'i hem buggy hem fixed revizyon olarak kaydetmiş:

- Python metadata sürümü: 3.7.3
- Buggy commit: 6dff721a3a8755356b2e89d02ef63ad8ab38ec95
- Fixed commit: 6dff721a3a8755356b2e89d02ef63ad8ab38ec95
- Test dosyası metadata'sı: tests/keras/metrics_test.py

Bu durumda iki ayrı sürüm karşılaştırması yapılamaz. Vaka envanterde tutuldu, ancak metadata-incomplete olarak işaretlendi; doğrulayıcı veri olarak kabul edilmedi.

## 3. Kaynak dağılımı

| Upstream proje | Ham kayıt |
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
| **Toplam** | **501** |

Pandas tek başına 169/501 ham kaydı oluşturuyor. Bu nedenle örneklemi sadece en büyük projeden seçmekten kaçınılmalı; proje başına örneklem sınırı ve proje kümelenmesi analizde korunmalı.

## 4. Yorum ve sonraki kapı

Bu çalışma metadata envanterini doğrulamış ve yeni vakaların sistematik taranmasını mümkün kılmıştır. Fakat Stage 2'nin operasyonel veri kabulü tamamlanmamıştır. Her aday için lisans, kaynak ve önceki inceleme, aynı hedef testin buggy sürümde başarısız/fixed sürümde başarılı olması, kök neden kanıtı, E1/E2/E3 yeterliliği, veri sızıntısı ve iki bağımsız değerlendirici incelemesi ayrı ayrı gerekir.

Hedef değişmedi: **en az 60 kabul edilmiş bağımsız vaka ve 8 proje; hedef 80 vaka**. Envanter dosyasındaki tüm accepted_for_confirmatory alanları false'tur. Hiçbir kabul koşulu sonradan gevşetilmemelidir. Bu sonuç bir deney sonucu değil, kaynak/metadata taramasının teknik sonucudur.
