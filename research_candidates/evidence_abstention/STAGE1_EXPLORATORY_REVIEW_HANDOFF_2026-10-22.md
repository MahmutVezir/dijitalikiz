# İnsan incelemesi devir paketi — 22 Ekim 2026

**Durum:** Yalnızca keşifsel kök-neden incelemesi için. Doğrulayıcı örnekleme uygun değil.

Toplam **10 teknik sinyal** var: önceki V8 grubundaki 4 kayıt ve workflow doğrulaması sırasında çalıştırılmış ikinci gruptaki 6 kayıt. Bu vakaların tamamı maruziyet nedeniyle doğrulayıcı örneklemden kalıcı olarak dışlandı.

| Kaynak grup | Teknik sinyal | Doğrulayıcı kabul |
|---|---:|---:|
| V8 ilk grup | 4 aday | 0 |
| V8 offset-8 grubu | 6 aday | 0 |
| **Toplam** | **10** | **0** |

Teknik sinyaller: buggy sürümde kaydedilmiş hedef test başarısızlığı ve fixed sürümde geçiş. İki V8 ikinci-grup vakasında iki taraf da test-harness/bağımlılık hatasıyla kaldı; bunlar insan kök-neden incelemesine alınmadı.

## Zorunlu değerlendirme ayrımı

Kök-neden paneli en az iki bağımsız inceleyiciyle buggy/fixed kaynak, test ve patch kanıtını değerlendirebilir. Kanıt-yeterliliği paneli ayrı ve bu panelle çakışmayan en az iki kişiden oluşmalıdır; yalnızca anonimleştirilmiş kanıt paketi ile anonim model yanıtlarını görmelidir.

**Kamuya açık bir GitHub dosyası kör değerlendirme sağlamaz.** Kanıt-yeterliliği paneline başlamadan önce özel/erişim kontrollü depolamada vaka adı, commit, patch, issue/PR ve gold label içermeyen ayrı paket hazırlanmalıdır. İnceleyici kimlikleri veya onayları mevcut değildir; bu dosya onları atamaz.

Ayrıntılı teknik kayıtlar: [JSON handoff](STAGE1_EXPLORATORY_REVIEW_HANDOFF_2026-10-22.json). Maruziyet kaydı: [addendum](EXPOSURE_EXCLUSION_ADDENDUM_2026-10-22.json).
