import gradio as gr
import os
from math import ceil




def verifier_dossier(chemin):
    if os.path.isdir(chemin):
        return f"✅ Dossier trouvé : {chemin}"
    else:
        return f"❌ Dossier introuvable : {chemin}"

def charger_images_dossier(chemin):
    if not os.path.isdir(chemin):
        return f"❌ Dossier introuvable : {chemin}", []

    # On accepte jpg/png/jpeg/webp
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    fichiers = []
    for ext in extensions:
        fichiers.extend(glob.glob(os.path.join(chemin, ext)))

    fichiers = sorted(fichiers)[:20]  # On limite à 20 max
    return f"✅ {len(fichiers)} image(s) trouvée(s)", fichiers

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
        height: 34px !important;           /* pile la hauteur utile */
        line-height: 34px !important;      /* aligne le texte dedans */
        padding: 0 10px !important;        /* petit espace horizontal */
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
    /* Vise tous les conteneurs autour du textarea */
        .status-text,
        .status-text > div,
        .status-text > div > div {
            height: 39px !important;
            padding: 0 !important;
            margin: 0 !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
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