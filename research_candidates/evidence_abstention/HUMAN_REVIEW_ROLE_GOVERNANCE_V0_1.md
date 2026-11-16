# İnsan değerlendirmesi — rol ayrımı, körleme ve yönetişim

**Sürüm:** 0.1 taslak — 16 Kasım 2026  
**Durum:** Danışman/kurum incelemesi, panel onayı, etik/izin değerlendirmesi ve ön kayıt tamamlanmadı. Model inference izni değildir.

## 1. Amaç

Bu belge, teknik ground truth, kanıt yeterliliği, model yanıtı puanlama ve dış denetim rollerinin birbirine karışmasını önlemek için hazırlanmıştır.

## 2. Önerilen rol haritası

| Rol | Asgari sayı | Erişim | Yasaklanan roller |
|---|---:|---|---|
| Panel A — teknik ground truth | 2 | Exact source, base/fix, issue, test ve reproduksiyon kayıtları | Panel B; model yanıtı puanlama |
| Panel B — kör kanıt yeterliliği | 2 | Modelin gördüğü anonim paket ve M1/M2/M3 mekanizma listesi | Panel A; source/gold; model yanıtı; confirmatory analyst |
| Panel A adjudicator | Gerektiğinde 1 | Panel A uyuşmazlık kayıtları ve teknik kanıt | Panel B; bağımsız dış denetçi |
| Panel B adjudicator | Gerektiğinde 1 | İki Panel B ilk puanı ve anonim paket | Panel A; source/gold; model yanıtı |
| Teknik validator / paket hazırlayıcı | Atanmış kişiler | Kaynak, test, fix, paket oluşturma | Panel B; confirmatory analyst |
| Yanıt puanlama ekibi (geçici Panel C önerisi) | En az 2 | Anonim model yanıtı ve modelin gördüğü paket | Panel A/B; gold source; confirmatory analyst |
| Confirmatory analyst | En az 1 | Kilitlenmiş anonim ham çıktı ve önceden belirlenmiş analiz planı | Gold cause, source/fix, Panel A/B ilk puanları ve koşul anahtarı analiz kilitlenene kadar |
| Bağımsız dış denetçi | 1+ | Panel B kilidinden sonra artifact authenticity, provenance, lisans/reproduction ve rol kayıtları | Panel A/B, adjudicator, teknik reviewer, packet preparer ve analyst |

**Panel C notu:** Mevcut belgelerde “Panel B” adı hem kanıt yeterliliği hem model yanıtı adjudication için kullanılıyor. Bu rol çakışmasıdır. Bu taslak, model yanıtı puanlaması için ayrı ve koşul/gold körlüğü olan geçici “Panel C” önerir. Bu adlandırma ve rol henüz manifest/protokole onaylı değişiklik olarak işlenmemiştir. Danışman ve araştırma ekibi bu ayrımı karara bağlamadan model inference yapılmamalıdır.

## 3. Çalışma sırası

1. Danışman ve uygun okul/kurum sorumlusu ile yöntem, yaşa uygun gözetim, izin ve gizlilik gerekliliklerini belirle.
2. Panel A ve Panel B adaylarının uzmanlık, bağımsızlık, çıkar çatışması ve önceki erişimini kontrol et. Kimlikler yalnızca kısıtlı kimlik anahtarında tutulur.
3. Panel A iki bağımsız reviewer ile teknik doğrulama yapar; ilk kararları ayrı ayrı kilitler.
4. Panel A en az üç makul ve ayırt edilebilir mekanizma (bir gerçek neden + en az iki alternatif) tanımlar. Gerçek mekanizma anahtarı Panel B'den ayrı saklanır.
5. Paket hazırlayıcı, modelin göreceği anonim evidence packet'i üretir. Repo/issue/PR, patch/fix, gold cause, level label, cevap veya koşul bilgisi model-facing packet'ten çıkarılır. İçerik ve hash sabitlenir.
6. Panel B iki bağımsız reviewer ile aynı anonim paketi ve karıştırılmış M kodlu alternatifleri inceler. Her karar kanıt ID ve gerekçe ile kaydedilir. Panel B model yanıtını ve gold cause'u görmez.
7. Panel B ilk kararları kilitlenir. Uyuşmazlık varsa önceden belirlenmiş üçüncü kişi adjudication yapar; ilk kararlar korunur.
8. Panel B karar kilidinden sonra gizli Panel A anahtarı açılır ve E1/E2/E3 kuralları uygulanır. E1 için tek hayatta kalan mekanizma gerçek gold ile eşleşmelidir.
9. Dış denetçi, Panel B kilidinden sonra artifact authenticity ve kaynak/rol kayıtlarını kontrol eder; ilk panel kararlarını değiştiremez.
10. Tüm vaka kabul şartları ve en az 60 farklı upstream projeden 60 bağımsız vaka sağlanmadan doğrulayıcı model inference yapılmaz.
11. Model yanıtlarının puanlanması Panel A/B'den ayrı bir ekipte yapılmalıdır. Bu ekip için Panel C önerisi protokol/manifestte resmi olarak onaylanmalı; koşul körlüğünün uygulanabilirliği test edilmelidir.
12. Analiz anahtarı ve confirmatory analyst erişimi önceden kayıtlı analiz kilitlerine göre yönetilir.

## 4. Körleme ve erişim matrisi

| Materyal | Panel A | Panel B | Teknik validator / hazırlayıcı | Yanıt puanlama ekibi (önerilen C) | Analyst |
|---|---:|---:|---:|---:|---:|
| Repo/issue/PR/fix source | Evet | Hayır | Evet | Hayır | Hayır |
| Base/fix test logs | Evet | Hayır | Evet | Hayır | Hayır |
| Gold root cause | Evet | Hayır | Gerektiği kadar | Hayır | Hayır |
| Model-facing anonymized packet | Hazırlık için | Evet | Evet | Evet | Kilit sonrası |
| M1/M2/M3 alternatives | Evet | Evet | Evet | Hayır | Hayır |
| Hidden E1/E2/E3 key | Evet, anahtar sorumlusu | Hayır | Hayır | Hayır | Analiz kilidine kadar hayır |
| Raw model response | Hayır | Hayır | Hayır | Evet | Evet, kilit kurallarına göre |
| P0/P1 condition key | Hayır | Hayır | Hayır | Mümkünse hayır | Analiz planına göre kilit sonrası |

Bu matris nihai protokol kararı değildir. Yanıt puanlama ekibinin ham response ve policy-blinding tasarımı ayrıca dondurulmalıdır.

## 5. Önceden erişim ve proje sahibinin rolü

Bir kişinin vaka issue/PR/source/fix/gold cause içeriğini önceden görmesi o kişiyi o vaka için kör Panel B, yanıt puanlayıcısı, confirmatory analyst veya bağımsız dış denetçi olmaktan çıkarabilir. Önceden maruziyetin kapsamı kaydedilir.

Proje sahibi koordinasyon, belge takibi ve erişim yönetimi yapabilir. Önceden gördüğü adaylarda kör reviewer veya bağımsız dış denetçi rolü üstlenemez. Önceden pipeline-debug veya hedef test troubleshooting için açılmış vakalar mevcut protokole göre confirmatory havuzdan çıkarılır.

## 6. Değerlendirici uygunluğu ve çıkar çatışması

Her değerlendirici için aşağıdakiler kısıtlı ayrı kayıtta tutulur:
- pseudonymous reviewer ID;
- ilgili alan/uzmanlık ve deneyim özeti;
- atandığı rol ve izin verilen erişim;
- çıkar çatışması ve önceki repo/vaka/model erişim beyanı;
- gönüllü katılım ve gerekli izin/consent durumu;
- eğitim/kalibrasyon ve form sürümü.

Akademik unvan tek başına yeterlilik kanıtı değildir. Gereksiz kişisel veri istenmez.

## 7. Reşit olmayan araştırmacı için gözetim ve gizlilik

Proje sahibi reşit olmadığı için insan katılımcıların görevlendirilmesi, gönüllü katılım, veri saklama ve olası kurumsal izin/veli veya okul gözetimi gereklilikleri danışman ve ilgili kurumla önceden kontrol edilmelidir. Bu belge hukuki/etik onay yerine geçmez.

İmzalı formlar, gerçek isimler, e-posta/telefon ve kurum içi bilgiler GitHub deposuna eklenmez. Repository yalnızca anonim reviewer ID, rol, form sürümü, kilitli karar hash'i ve kişisel veri içermeyen denetim kayıtlarını barındırabilir.

## 8. Uyuşmazlık ve inter-rater agreement

- İki bağımsız puanlayıcının ilk kararları ayrı ve değiştirilemez biçimde kaydedilir.
- Adjudication ilk kararları silmez; ayrı kayıt üretir.
- Panel A teknik kök neden kararları ve Panel B kanıt yeterliliği kararları ayrı analiz edilir.
- İki rater ve nominal kategorilerde Cohen kappa değerlendirilebilir; ordinal/missing/multiple-rater tasarımında ağırlıklı kappa veya Krippendorff alpha gerekçelendirilmelidir.
- Ham yüzde anlaşma, kategori prevalansı, uyuşmazlık ve adjudication oranı istatistikle birlikte raporlanmalıdır.
- Kalibrasyon vakaları confirmatory cohort'a dahil edilmez.

## 9. Mevcut protokolle çözülmesi gereken çelişki

Mevcut SWE_REBENCH_V2_EXPERIMENT_MANIFEST_V0_1.json Panel B'yi evidence sufficiency paneli olarak tanımlar. EVIDENCE_TIER_OPERATIONALIZATION_DRAFT_2026-11-15.md de Panel B'yi model yanıtını görmeyen kanıt paneli olarak tanımlar. Ancak SWE_REBENCH_V2_OUTPUT_ADJUDICATION_RUBRIC_V0_1.md Panel B'ye ham model yanıtını gösterir. RATER_AGREEMENT_PROTOCOL.md içindeki evidence_support görevi de model yanıtı puanlaması içerir.

Bunlar aynı kişiler/rol ise körleme bozulur. Bu nedenle:
1. Kanıt yeterliliği Panel B ve model yanıtı puanlama ekibi ayrılmalı.
2. Model yanıtı puanlama ekibinin adı/erişim/ölçütleri protokol ve manifestte resmi olarak güncellenmeli.
3. Puanlama ekibi koşul ve gold cause körlüğü açısından test edilmeli.
4. Rater agreement planı rol ve ölçeklere göre revize edilmeli.
5. Değişiklikler mentor/bağımsız reviewer onayı ve preregistration öncesi tamamlanmalı.

## 10. Onay kontrol listesi

- [ ] Danışman/kurum gözetimi ve gerekli etik/izin süreci netleştirildi.
- [ ] Panel A reviewer yeterliliği/bağımsızlığı onaylandı.
- [ ] Panel B reviewer yeterliliği/bağımsızlığı onaylandı.
- [ ] Panel A ve Panel B kimlik kümeleri ayrık.
- [ ] Yanıt puanlama rolü Panel B'den ayrıldı ve resmi protokole işlendi.
- [ ] Reviewer form ve rubrikleri kalibre edildi.
- [ ] Uyuşmazlık/adjudication prosedürü onaylandı.
- [ ] Erişim/anonimleştirme ve hash kilitleme prosedürü denendi.
- [ ] Preregistration ve artifact freeze tamamlandı.

Bu belgelerin GitHub'a eklenmesi, gerçek değerlendiricilerin atanmış/onaylanmış olduğu anlamına gelmez.
