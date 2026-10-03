# RSC-Bench — Aşama 4 Prompt Freeze Gate

**Protocol:** v1.0  
**Aşama:** 4 — Prompt Freeze  
**Durum:** BLOCKED / FREEZE-READY

## Amaç

Ana deneyde kullanılacak promptların anlamsal olarak sabitlenmesini, canonicalization sonrası SHA-256 hash değerlerinin kayda alınmasını ve freeze sonrasında değişikliklerin otomatik olarak yakalanmasını sağlamak.

## Freeze ön koşulları

Prompt freeze aşağıdaki koşulların tamamı sağlanmadan `FROZEN` olarak işaretlenmemelidir:

1. Stage 3 gerçek model teknik pilotu tamamlanmış olmalı.
2. Standard ve CCDG koşullarında model çıktısının JSON ayrıştırması doğrulanmış olmalı.
3. Output schema doğrulaması tamamlanmış olmalı.
4. Run metadata kayıtlarının eksiksiz olduğu doğrulanmış olmalı.
5. Model sağlayıcısı ve **tam model ID/checkpoint** kaydedilmiş olmalı; dinamik `latest` alias kullanılmamalı.
6. Pilot vakalarının ana veri setine dahil edilmediği doğrulanmış olmalı.
7. Primary matcher kriterinin prompt freeze öncesinde değiştirilmediği veya değiştirildiyse protokol değişikliği olarak kaydedildiği doğrulanmış olmalı.
8. Bu kontrolden sonra promptlarda anlamsal değişiklik yapılmamalı.

## Mevcut blokaj

Bu çalışma alanında gerçek model pilotu henüz çalıştırılmadı. Ayrıca `configs/model.yaml` içinde gerçek sabit model ID'si henüz belirlenmedi ve çalışma ortamında `OPENAI_API_KEY` bulunmuyor.

Bu nedenle `prompts/manifests/prompt_freeze.json` **FROZEN yapılmamıştır**. Mevcut durum bilinçli olarak `UNFROZEN` bırakılmıştır.

## Freeze işlemi

Ön koşullar tamamlandıktan sonra:

```bash
python scripts/freeze_prompts.py
```

Ardından doğrulama:

```bash
PYTHONPATH=src python -c "from pathlib import Path; from rscbench.freeze import verify_frozen; verify_frozen(Path('.')); print('Frozen prompt hashes verified.')"
```

Freeze sonrası prompt dosyalarındaki anlamsal değişiklikler hash mismatch üreterek deney yürütmesini engeller.

## Bilimsel kural

Prompt freeze, pilot sonuçlarını ana hipotezi destekleyecek şekilde değiştirmek için kullanılmayacaktır. Freeze sonrasında yalnızca gerçek teknik hata düzeltmeleri, ayrı değişiklik kaydı ve protokol değerlendirmesiyle ele alınabilir.
