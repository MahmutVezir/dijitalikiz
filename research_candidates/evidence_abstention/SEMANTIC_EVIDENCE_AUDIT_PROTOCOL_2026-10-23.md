# Anlamsal kanıt denetçisi — uygulama ve doğrulama protokolü

**Tarih:** 23 Ekim 2026  
**Durum:** Arayüz ve yapısal doğrulama kodu eklendi; bağımsız doğrulama tamamlanmadı. **Bu belge ön kayıt değildir ve deney/çıkarım izni vermez.**

## Amaç

Paket denetleyicisi bir kanıt paketinin bütünlüğünü, alanlarını ve referans kimliklerini kontrol eder; tek başına bir kök neden iddiasının kanıtlarla gerçekten desteklenip desteklenmediğini değerlendiremez. Karar katmanının gerektirdiği `supported_claim_coverage`, `self_check_conflict` ve `explicit_contradiction` sinyallerinin eksik olduğu durumda doğru davranış cevap vermekten kaçınmaktır.

Yeni `implementation/semantic_evidence_auditor.py` dosyası, görünür bir aday yanıtı ve görünür kanıt öğelerini değerlendirici modele iletecek istemi ve yapısal çıktı denetimini tanımlar. `qwen_uncertainty_adapter.py` içindeki `evidence_audit_with_semantic_report` işlevi, geçerli bir değerlendirme çıktısını karar katmanının kullandığı sinyallere dönüştürür. Bozuk/eksik değerlendirme çıktısı yapısal paketi yanlış biçimde “geçersiz” işaretlemek yerine sinyalleri bilinmiyor bırakır; karar katmanı bu durumda teşhis üretmez.

## Girdi sınırı ve bilgi sızıntısı

Denetçi yalnızca şu girdileri görmelidir:
- modelin ürettiği yapılandırılmış aday yanıt;
- modele gösterilmiş kanıt öğelerinin kimlikleri ve içerikleri.

Girdi yükü altın kök neden etiketini, E1/E2/E3 koşul etiketini, düzeltme yamasını, fixed sürüm kaynak kodunu, gizli cevap anahtarını, deney koşulunu veya model çıktısından elde edilmiş sonradan puanları içermemelidir. Oluşturucu bu alanları yanıt şemasından dışlar ve kanıt içeriğini güvenilmeyen veri olarak işaretler; buna rağmen tam bilgi sızıntısı güvencesi ancak oluşturulan gerçek istemlerin gözden geçirilmesiyle verilebilir.

Denetçinin ayrı bir istem rolünde çalıştırılması onu bağımsız bir hakem yapmaz. Aynı Qwen modelinin özdenetimi, üretilen cevapla ortak hata yapabilir. Bu sebeple denetçi çıktısı *hakikat etiketi* değil, doğrulanması gereken bir çalışma zamanı tahminidir.

## Dondurulması önerilen çıktı şeması

Üst düzey alanlar:
- `claims`: en az 1, en fazla 16 atomik ve denetlenebilir iddia;
- `self_check_conflict`: model yanıtındaki maddi iddiaların kendi aralarında çelişip çelişmediği;
- `explicit_contradiction`: görünür kanıtın iddialardan en az biriyle açıkça çelişip çelişmediği.

Her iddia tam olarak `claim_id`, `claim`, `status`, `evidence_refs`, `rationale` alanlarını taşımalıdır. Durumlar:
- `supported`: görünür kanıt iddiayı doğrudan destekliyor;
- `partial`: iddianın yalnızca bir bölümü destekleniyor veya önemli ayrım eksik;
- `unsupported`: görünür kanıt iddiayı desteklemiyor;
- `contradicted`: görünür kanıt iddiayla açıkça çelişiyor.

Referanslar paketteki var olan kimliklerle eşleşmelidir. Desteklenmiş, kısmen desteklenmiş ve çelişkili iddialar en az bir kanıt referansı vermelidir. Herhangi bir bilinmeyen referans, yinelenen iddia kimliği, beklenmeyen alan, geçersiz tür veya tutarsız çelişki bayrağı bütün değerlendirmeyi başarısız kılar.

İlklendirme/kalibrasyon deneyinde önceden onaylanırsa kapsam hesabı `supported=1`, `partial=0.5`, `unsupported=0`, `contradicted=0` olarak tanımlanabilir. Bu kapsama skoru gerçek doğruluk olasılığı değildir; yalnızca denetçinin etiketlerine dayanan bir özet sinyaldir ve bağımsız insan puanlarıyla doğrulanmadan karar eşiğinde kullanılmamalıdır.

## Doğrulama adımları

1. **Şema ve bütünlük testleri:** Birim testleri JSON biçimi, zorunlu alanlar, bilinmeyen/tekrarlanan kanıt kimlikleri, bozuk türler ve fail-closed davranışı sınar. Bu testler kod davranışını sınar, anlamsal doğruluğu kanıtlamaz.
2. **Kör referans verisi:** Pilot/kalibrasyon vakaları için iki bağımsız değerlendirici görünür kanıt ve iddiaları kör şekilde puanlar. Hakemler altın kök neden, koşul etiketi veya diğer hakemin kararını görmez. Uyuşmazlıklar önceden belirlenmiş prosedürle çözülür; ilk notlar korunur.
3. **Eğitim/kalibrasyon ayrımı:** Denetçi istemi veya eşikleri geliştirmek için kullanılan vakalar doğrulayıcı örneklemde yeniden kullanılmaz. Ayrım mümkün olduğunca vaka ve upstream proje düzeyinde yapılır; aynı hata ailesinin kopyaları farklı bölmelere dağıtılmaz.
4. **Geçerlik raporu:** İnsan-denetçi anlaşması, destek kapsamı farkları, çelişki tespitinin duyarlılık/özgüllük ölçüleri, eksik/biçim dışı sonuç oranı ve hata türleri raporlanır. Örneklem yetersizse eşik doğrulanmış olarak adlandırılmaz.
5. **Eşik ve kilitleme:** Bağımsız kalibrasyon verisi ve önceden tanımlanmış seçim kuralı olmadan eşikler dondurulmuş kabul edilmez. Eşikler doğrulayıcı sonuçları görülmeden kaydedilir.
6. **Araştırma kullanımı:** Anlamsal denetçi birincil sonucun yerine geçmez. Birincil sonucun kök neden doğruluğu ve kanıtsal desteği, koşullara kör bağımsız insan değerlendiricilerce puanlanmalıdır. Denetçi sinyali yalnızca önceden dondurulmuş sistem kararının parçası olabilir.

## Bu sürümün gerçek durumu

- Kod: arayüz, sıkı JSON çözümleyicisi, kanıt referansı denetimi ve adapter bağlantısı eklendi.
- Sentetik yazılım testleri: input validation sıkılaştırması sonrası 12 test izole yerel koşuda geçti. GitHub Actions/full adapter test paketinin durumu doğrulanmadı; bu testler anlamsal karar kalitesini ölçmez.
- Gerçek Qwen denetçi çağrısı: çalıştırılıp doğrulanmadı.
- İnsanla karşılaştırmalı anlamsal doğrulama: yapılmadı.
- Kalibrasyon verisi/eşikleri: boş ve dondurulmamış.
- Doğrulayıcı vakalar/ön kayıt: hâlâ 0 kabul edilmiş vaka ve ön kayıt yok.

Bu nedenle bu kod, tasarım boşluğunu daraltan bir uygulama bileşenidir; projenin halüsinasyonu azalttığını veya güven skorunun kalibre edildiğini göstermez.
