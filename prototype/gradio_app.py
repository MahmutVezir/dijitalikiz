"""Gradio interface for the evidence-cited Qwen demo."""
import json
import gradio as gr
from evidence_abstention_model import EvidencePacket, get_model


def analyze(code: str, traceback: str, context: str, policy: str):
    report = get_model().analyze(
        EvidencePacket(code=code or "", traceback=traceback or "", context=context or ""),
        policy=policy,
    )
    if report.get("decision") == "diagnose":
        headline, detail = "Teşhis adayı", report.get("root_cause", "")
    elif report.get("decision") == "abstain":
        headline, detail = "Yeterli kanıt yok — cevap vermekten kaçınıldı", report.get("rationale", "")
    else:
        headline, detail = "Geçerli teşhis üretilemedi", report.get("validation_error", "Model çıktısı doğrulanamadı.")
    return headline, detail, json.dumps(report, ensure_ascii=False, indent=2)


with gr.Blocks(title="Kanıt Tabanlı Hata Teşhisçisi") as demo:
    gr.Markdown(
        "# Kanıt Tabanlı Hata Teşhisçisi\n"
        "Qwen2.5-3B-Instruct tabanlı mühendislik prototipi. P1 politikasında kanıt yetersizse model kaçınabilir. "
        "JSON/kanıt referansı denetimi semantik doğruluğu kanıtlamaz; bu arayüz araştırma sonucu değildir."
    )
    with gr.Row():
        with gr.Column():
            code = gr.Textbox(label="İlgili kod", lines=10)
            trace = gr.Textbox(label="Hata mesajı / traceback", lines=8)
            context = gr.Textbox(label="Ek bağlam (isteğe bağlı)", lines=4)
            policy = gr.Radio(["P1", "P0"], value="P1", label="Yanıt politikası",
                              info="P1: kanıt yetersizse kaçın. P0: teşhis vermeye çalış.")
            run = gr.Button("Hata analizi yap", variant="primary")
        with gr.Column():
            headline = gr.Textbox(label="Sonuç", interactive=False)
            detail = gr.Textbox(label="Açıklama", lines=5, interactive=False)
            output = gr.Code(label="Denetlenebilir JSON", language="json")
    run.click(analyze, inputs=[code, trace, context, policy], outputs=[headline, detail, output])
    gr.Markdown("Bu arayüz public share açmaz. Gizli anahtar/parola girmeyin; model çıktıları insan tarafından doğrulanmalıdır.")

if __name__ == "__main__":
    demo.launch(share=False, inline=True)
