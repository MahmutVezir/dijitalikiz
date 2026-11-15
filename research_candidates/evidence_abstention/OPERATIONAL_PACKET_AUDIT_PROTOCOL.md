# Operasyonel kanıt-paketi denetimi — taslak v0.1

**Durum: uygulanabilir veri sözleşmesi taslağı; bağımsız anlamsal doğrulayıcı henüz yok.** Bu dosya ön kayıt veya canlı çıkarım izni değildir.

## Amaç ve ayrım

Deneydeki E1/E2/E3 etiketleri analiz ve sonradan adjudication için saklanır. Bunlar model prompt'una, runtime packet doğrulayıcısına veya karar politikasına aktarılmaz. Özellikle E3 etiketinden doğrudan abstain kararı vermek sonucu tautolojik hâle getirir.

`operational_packet_validator.py` yalnızca paketin yapısal bütünlüğünü doğrular: anonim paket kimliği, benzersiz kanıt öğesi ID'leri, içerik hash'leri, kaynak snapshot hash'leri ve paket manifest hash'i. **Bu kontrol kanıtın kök nedeni ayırt etmeye yeterli olduğunu söylemez.** Paket `valid` olsa dahi karar politikası, bağımsız destek/çelişki incelemesi mevcut değilse abstain etmelidir.

## Paket sözleşmesi

- Top-level alanlar yalnızca `schema_version`, `packet_id`, `evidence_items`, `packet_sha256` olabilir.
- `packet_id`, gerçek vaka adını içermeyen `PACKET_...` anonim kimliği olmalıdır.
- Her kanıt öğesi `id`, `kind`, `content`, `content_sha256`, `source_snapshot_sha256` alanlarını taşır. Kanıt ID'leri benzersizdir.
- `packet_sha256`, `packet_sha256` alanı dışarıda bırakılarak canonical JSON üzerinde SHA-256 olmalıdır.
- Vaka kimliği, gold root cause, E1/E2/E3/condition etiketi, patch, fixed commit, issue/PR veya çözüm başlığı bu runtime paketine konmaz.
- Bir paket hash doğrulamasından geçse bile anlamsal kanıt değerlendirmesi, çelişki tespiti ve iddia-destek kapsamı denetimini tamamlamış sayılmaz.

## Üretim kararındaki zorunlu sinyaller

Canlı adapter'a aktarılacak `EvidenceAudit` şu alanları taşır: paket doğrulama durumu, modelin kullanabileceği kanıt ID'leri, bağımsız claim-support coverage, bağımsız self-check-conflict ve explicit-contradiction sinyalleri. İlk alan yapısal doğrulayıcıdan gelir. Son üç sinyal için bağımsız ve önceden tanımlanmış bir runtime checker gerekir; modelin kendi gerekçesini tek başına doğrulanmış kabul etmek yeterli değildir.

Bu taslakta son üç sinyalin geçerli, bağımsız bir üreticisi henüz uygulanmış/ölçülmüş değildir. Eksik olan herhangi bir sinyal kapalı karara gider ve modelin teşhis üretmesine izin vermez. Sinyaller tamamlanmadan canlı deney başlatılmamalıdır.

## Körleme ve kayıt

Kanıt-yeterliliği paneli model yanıtı, patch, fixed code, gold root cause veya hidden E-level condition görmeden, anonim paketleri incelemelidir. Kamuya açık GitHub deposu bu körlemeyi sağlayamaz; bağımsız panel başlamadan önce erişim kontrollü ayrı depoda paket hazırlanmalıdır. İnceleyicilerin kimlikleri ve anlaşmazlık kayıtları gerçek kişiler tarafından tamamlanmalıdır.

Her paket için packet SHA-256, kaynak snapshot SHA-256'ları, validator sürümü/hash'i, validator raporu ve tüm hata nedenleri saklanır. Validator hiç bir upstream vaka için kabul kararı vermez ve model çıkarımı çağırmaz.


## 9. Üç kanıt düzeyinin dış packet-set sözleşmesi — 15 Kasım 2026 taslağı

Tek bir operasyonel vaka için üç ayrı inner packet, yalnızca erişim kontrollü araştırma hazırlama alanında bir dış packet-set manifestiyle bağlanabilir. Yeni `implementation/evidence_level_packet_set.py` bu dış sözleşmenin salt-yapısal doğrulayıcısıdır.

- Her inner packet, bu belgedeki mevcut `evidence_items` sözleşmesine uymalıdır.
- Dış nesne yalnızca `schema_version`, anonim `packet_set_id`, `packets` ve `packet_set_sha256` alanlarını içerir. `packets` anahtarları E1/E2/E3 seviyelerini tutar.
- Inner packet'ler birbirinden farklı anonim `packet_id` taşır. Dış wrapper araştırma hazırlama/denetim dosyasıdır; **model prompt'una veya runtime decision input'una verilmez**. Çalıştırıcı yalnızca o koşul için seçilmiş tek inner packet içeriğini görmelidir.
- Validator her inner paketin kendi hash/provenans/yapı kontrollerini çağırır; kanıt ID kümelerinin E3 ⊂ E2 ⊂ E1 olmasını, aynı ID'nin tüm seviyelerde aynı içerik ve source snapshot hash'ini korumasını, komşu seviyelerin gerçekten farklı kanıt ID'leri taşımasını ve dış packet-set hash'inin doğrulanmasını ister.
- Dışarıdan dondurulmuş beklenen SHA-256 verilirse eşleşme zorunludur. Herhangi bir inner packet geçersizse veya ilişki bozulmuşsa tüm set fail-closed biçimde reddedilir.

Bu yeni kod henüz ana `kaggle_stage3_p0_p1.py` runner'ına entegre edilmemiştir. Runner halen legacy `code/trace/context` veri formatını kullanır. Eski `items/source_uri` ve operasyonel `evidence_items/source_snapshot_sha256` biçimleriyle aynıymış gibi varsayılmamalıdır. Yeni sözleşme, SWE-rebench doğrulayıcı runner'ı ve manifesti sürümlenmeden confirmatory veri üzerinde kullanıma hazır değildir.

**Semantik sınır:** Validator paketlerin gerçekten üç farklı kanıt seviyesini oluşturup oluşturmadığına karar vermez. E1/E2/E3 etiketi, Panel B'nin model çıktısı öncesindeki bağımsız mekanizma/kanıt değerlendirmesinden gelir. Paket-set valid olması yalnızca hash ve yapısal ilişkilerin doğru olduğunu gösterir; kök nedeni, alternatiflerin makullüğünü veya kanıt yeterliliğini otomatik onaylamaz.

**Mevcut çalışma durumu:** Yalnızca sentetik ünite testleri yazılmıştır. Gerçek vaka, insan puanlaması, model çağrısı veya inference yoktur. Kodun CI testi henüz doğrulanmamıştır. Registry boş ve inference kapısı kapalıdır.
