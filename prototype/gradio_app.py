"""Gradio interface for an exploratory, evidence-cited bug-diagnosis demo."""
import json
import gradio as gr
from evidence_abstention_model import EvidencePacket, get_model


def analyze(code: str, traceback: str, context: str, policy: str):
    try:
        report = get_model().analyze(
            EvidencePacket(code=code or "", traceback=traceback or "", context=context or ""),
            policy=policy,
        )
    except Exception as exc:
        report = {
            "status": "execution_error",
            "decision": "not_available",
            "message": str(exc),
            "research_status": "no_model_result",
        }
    decision = report.get("decision")
    if decision == "diagnose":
        headline = "Model teşhis sundu"
        detail = report.get("root_cause", "")
        if report.get("status") == "invalid_evidence_references":
            headline = "Uyarı: teşhis var, ancak kanıt referansları geçersiz"
    elif decision == "abstain":
        headline, detail = "Model cevap vermekten kaçındı", report.get("rationale", "")
    elif decision == "invalid_output":
        headline, detail = "Geçersiz model çıktısı", report.get("validation_error", "")
    else:
        headline, detail = "Çalıştırma sonucu yok", report.get("message", "Rapor üretilemedi.")
    return headline, detail, json.dumps(report, ensure_ascii=False, indent=2)


with gr.Blocks(title="Kanıt Tabanlı Hata Teşhisçisi") as demo:
    gr.Markdown(
        "# Kanıt Tabanlı Hata Teşhisçisi\n"
        "TÜBİTAK araştırması için keşifsel mühendislik arayüzü. P0/P1 istemleri ve çıktı şeması "
        "ana Stage 3 sözleşmesiyle eşleştirilmiştir. Bu arayüzden alınan sonuçlar doğrulayıcı örnekleme "
        "veya araştırma sonucu olarak kullanılmaz. Kanıt ID kontrolü semantik doğruluğu kanıtlamaz."
    )
    with gr.Row():
        with gr.Column():
            code = gr.Textbox(label="İlgili kaynak kodu (zorunlu)", lines=10)
            trace = gr.Textbox(label="Hata mesajı / traceback (zorunlu)", lines=8)
            context = gr.Textbox(label="Ek bağlam (isteğe bağlı)", lines=4)
            policy = gr.Radio(
                ["P1", "P0"], value="P1", label="Yanıt politikası",
                info="P1: yeterli kanıt yoksa kaçın. P0: en olası teşhisi belirt."
            )
            run = gr.Button("Tek örneği analiz et", variant="primary")
        with gr.Column():
            headline = gr.Textbox(label="Sonuç", interactive=False)
            detail = gr.Textbox(label="Açıklama", lines=5, interactive=False)
            output = gr.Code(label="Denetlenebilir JSON", language="json")
    run.click(analyze, inputs=[code, traceback, context, policy], outputs=[headline, detail, output])
    gr.Markdown(
        "Kişisel veri, gizli anahtar veya özel kod girmeyin. Uygulama public share açmaz. "
        "Ham çıktılar demo ekranında kalır; semantik değerlendirme bağımsız insan puanlaması gerektirir."
    )

if __name__ == "__main__":
    demo.launch(share=False, inline=True)
