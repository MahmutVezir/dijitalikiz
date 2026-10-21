# Rubrik ve kör değerlendirme protokolü — v0.1 taslak

**Durum:** Taslak; bağımsız değerlendirici kalibrasyonu yapılmadı, protokol dondurulmadı ve ön kayıt değildir.
**Tarih:** 21 Ekim 2026

## 1. Ayrı tutulacak üç boyut

Her model yanıtı üç ayrı boyutta puanlanır: (1) karar: teşhis, açık kaçınma veya biçim dışı/yorumlanamayan çıktı; (2) gizli kök neden doğruluğu; (3) teşhisin yalnızca modelin gördüğü kanıt paketiyle desteklenip desteklenmediği.

Model gizli kök nedeni tesadüfen doğru tahmin etse bile paket makul alternatifleri ayırt etmiyorsa yanıt kanıtla desteklenen teşhis sayılmaz. E3 birincil sonlanımı bu ayrımı korur.

## 2. Kök neden doğruluğu

- **Correct:** Doğrulanmış gold root cause ile maddi olarak aynı mekanizma.
- **Partially correct:** Mekanizmanın önemli bir bölümünü belirtiyor, ancak kritik ayrıntıyı kaçırıyor veya alternatifleri ayırt edemiyor.
- **Incorrect:** Gold root cause ile çelişiyor veya ilgisiz bir neden sunuyor.
- **Unscorable:** Anlam veya referans kanıt, güvenilir puanlamaya yetmiyor.

Parafrazlar sabit bir anahtar sözcük eşleşmesine göre reddedilmez; eşdeğer teknik açıklamalar gerekçeyle kabul edilir.

## 3. Kanıtsal destek

- **Supported:** Paket teşhisi makul alternatiflerden ayıracak yeterli kanıt içeriyor ve yanıt bu kanıta dayanıyor.
- **Partially supported:** Bazı ifadeler destekleniyor ancak kritik nedensel bağlantı eksik.
- **Unsupported:** İddia sunulmayan varsayıma dayanıyor veya paket alternatifleri ayırt etmiyor.
- **Contradicted:** Yanıt, pakette açıkça bulunan kanıtla çelişiyor.
- **Uncertain:** Kesin karar için yeterli bilgi yok; adjudication gerekiyor.

E3 için kesin teşhislerden unsupported veya contradicted olanlar, vaka/politika düzeyinde unsupported_definitive_diagnosis=1 sayılır. Gold root cause ile eşleşmek kanıt desteğinin yerine geçmez.

## 4. Kaçınma ve eksik kanıt talebi

Kaçınma kararı ancak açıkça teşhis verilmediğinde kodlanır; abstain yanıtında root_cause boş olmalıdır. Eksik kanıt talebi, vaka gold panelinin yanıtları görmeden belirlediği ayırt edici kanıt listesine göre discriminative, partially relevant, irrelevant/unavailable veya not applicable olarak sınıflanır.

Geçersiz JSON otomatik düzeltilmez ve yeniden üretilmez. Ham çıktı korunur. Ham metinde kesin teşhis iddiası varsa kanıt desteği açısından ayrıca puanlanabilir; kural tüm koşullara aynı uygulanır.

## 5. Körleme ve adjudication

1. Her çıktı rastgele yanıt kimliğiyle sunulur; P0/P1 etiketi mümkün olduğu ölçüde puanlayıcılardan gizlenir.
2. En az iki bağımsız insan puanlayıcı önce birbirinden bağımsız puanlarını kilitler.
3. Gold paneli kaynak kodu, buggy/fixed sürüm, test ve düzeltme kanıtını görebilir. Kanıt desteği puanlayıcıları yalnızca modelin gördüğü paket ile anonim yanıtı görür.
4. Uyuşmazlık üçüncü bir değerlendirici veya belgelenmiş adjudication toplantısıyla çözülür. İlk bireysel puanlar silinmez.
5. Kategorik ölçütler için Cohen kappa, sıralı ölçütler için mümkünse ağırlıklı kappa ve güven aralığı raporlanır. Ham anlaşma oranı ve karışıklık tablosu da verilir.
6. Kalibrasyonda kullanılan tüm vakalar ana doğrulayıcı örneklemden kalıcı olarak dışlanır.

Bu rubrik ancak iki bağımsız değerlendirici tarafından gözden geçirilip onaylandıktan, kalibrasyon tamamlandıktan ve hash manifestte dondurulduktan sonra frozen kabul edilir. Mevcut durum taslaktır.
