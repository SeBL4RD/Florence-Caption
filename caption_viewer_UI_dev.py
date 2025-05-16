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
        margin-right: 800px;
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
                load_button = gr.Button("🔍 Charger les images", elem_classes=["small-left-button"])

            # Ajoute ceci AVANT le .click()
            status_output = gr.Textbox(
                label="Statut",
                interactive=False,
                visible=True,
                value=""
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