import gradio as gr
import os
from math import ceil




def verifier_dossier(chemin):
    if os.path.isdir(chemin):
        return f"✅ Dossier trouvé : {chemin}"
    else:
        return f"❌ Dossier introuvable : {chemin}"



def start_ui():
    with gr.Blocks(css="""
    .narrow-input {
        max-width: 1500px;          /* ceci est un commentaire CSS */
        margin: auto;               # centre le champ
    }
    .center-column {
        max-width: 1500px;
        margin: auto;
        padding: 20px;
        background-color: #2c2c2c;
        border-radius: 10px;
    }
    .small-left-button {
        width: 200px;
        margin-left: 0;
        margin-right: 1000px;
    }
    .statut-message {
        height: 40px;
        display: flex;
        align-items: center;
        border: none !important;
        background-color: transparent !important;
        color: #aaffaa;
        font-weight: bold;
        padding-left: 10px;
        box-shadow: none !important;
    }
    .load-btn {
        height: 40px;
        width: 200px;
        margin-left: 0;
        margin-right: 10px;
    }

    .status-text textarea {
        height: 36px !important;          /* hauteur égale au bouton */
        line-height: 36px !important;     /* alignement vertical du texte */
        padding: 0 8px !important;        /* petit padding horizontal */
        font-size: 14px;
        
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        color: #aaffaa;
        font-weight: bold;
        resize: none !important;
    }
    .status-text {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .status-text > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    """) as interface:
        with gr.Column(elem_classes=["center-column"]):
            gr.Markdown("# 🖥️ Mon interface Gradio de test")
            
            
            folder_input = gr.Textbox(
                label="Dossier contenant les images", # Affiche un titre au-dessus
                placeholder="Exemple : ./images", # Affiche un texte grisé à l’intérieur du champ
                value=".",  # Valeur par défaut du champ
                interactive=True, # Permet à l'utilisateur de modifier le champ
                elem_classes=["narrow-input"]  # <-- c’est ça qui lie le CSS à ce champ
            )

            with gr.Row():
                load_button = gr.Button("🔍 Charger les images", elem_classes=["load-btn"])
                status_output = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    lines=1,
                    max_lines=1,
                    value="",
                    scale=4,
                    elem_classes=["status-text"]
                )


            # Et ensuite tu fais le .click()
            load_button.click(
                fn=verifier_dossier,
                inputs=[folder_input],
                outputs=[status_output]
            )
                
    interface.launch()

if __name__ == "__main__":
    start_ui()