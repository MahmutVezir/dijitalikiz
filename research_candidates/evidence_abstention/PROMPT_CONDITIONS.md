# Prompt koşulları — sürüm 0.1

Bu iki koşulun dışında prompt'a vaka, kanıt veya sistem davranışı eklenmez. Yalnızca POLICY_INSTRUCTION satırı P0/P1 arasında değişir. Her istekte aynı OUTPUT_SCHEMA.json uygulanır; hiçbir örnek vaka/cevap prompt içine few-shot olarak eklenmez.

## Ortak system prompt

~~~text
You are analyzing a software defect using the evidence packet supplied in the user message.
Base factual claims only on information in that packet. Do not use external tools, web search, retrieval, or code execution. Do not claim to have run tests. Distinguish a plausible hypothesis from a cause supported by the packet. Return exactly one valid JSON object matching the provided output schema, without Markdown fences or text outside the JSON.
~~~

## Ortak user prompt şablonu

~~~text
Task: Assess the likely root cause of the reported software defect.

Policy instruction:
{POLICY_INSTRUCTION}

Evidence packet:
{CASE_EVIDENCE_PACKET}

Use evidence item IDs when referring to packet evidence. Do not cite information that is not present in the packet. If abstaining, leave root_cause as an empty string and list the specific evidence that would distinguish the plausible causes. Return only the JSON object defined by the schema.

JSON schema:
{OUTPUT_SCHEMA_JSON}
~~~

## P0 — zorunlu teşhis

~~~text
Choose and state one single most likely root cause. Do not abstain. If the evidence is incomplete, still give the most likely diagnosis and identify which supplied evidence led you to it.
~~~

## P1 — seçici teşhis / kaçınma izni

~~~text
Give a root-cause diagnosis only when the evidence packet sufficiently supports and distinguishes it from plausible alternatives. If the packet is insufficient or contradictory, abstain rather than guess, and list the specific additional evidence needed to distinguish the alternatives.
~~~

## Kullanım kuralları

- Model, model card / revision dışında haricî bağlam veya retrieval almaz.
- Aynı hata için E1/E2/E3 paketleri tüm ortak bağlamı korur; yalnızca önceden belirlenen kanıt öğeleri çıkarılır/değiştirilir.
- Fixed patch, gold label, issue/PR kimliği, upstream çözüm bağlantısı veya çözüm başlığı prompt'ta bulunmaz.
- Model ham çıktısı aynen saklanır. JSON hatasında otomatik düzeltme ya da yeniden üretim yoktur.
- P0/P1 işlem sırası her vaka için sabit bir seed ile karıştırılır. Her istek sıfır geçmişle başlar.
