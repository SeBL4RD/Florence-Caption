import gradio as gr
import os
from math import ceil
from pathlib import Path
import glob

MAX_IMAGES = 20

def charger_images_et_prompts(chemin: str):
    images_prompts = []
    dossier_path = Path(chemin)
    if not dossier_path.exists():
        return []
    for img_path in sorted(dossier_path.glob("*")):
        if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            txt_path = img_path.with_suffix(".txt")
            texte = txt_path.read_text(encoding="utf-8") if txt_path.exists() else ""
            images_prompts.append((str(img_path), texte))
    return images_prompts[:MAX_IMAGES]

def afficher_images(chemin):
    if not os.path.isdir(chemin):
        return "❌ Dossier introuvable : " + chemin, *([None]*MAX_IMAGES), *([None]*MAX_IMAGES)
    contenu = charger_images_et_prompts(chemin)
    status = f"✅ {len(contenu)} image(s) trouvée(s)" if contenu else "⚠️ Aucun fichier image trouvé"
    # Remplir les sorties
    image_values = []
    prompt_values = []
    for img, txt in contenu:
        image_values.append(img)
        prompt_values.append(txt)
    # Compléter à 20 si moins
    image_values += [None] * (MAX_IMAGES - len(image_values))
    prompt_values += [None] * (MAX_IMAGES - len(prompt_values))
    return status, *image_values, *prompt_values

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
                label="Dossier contenant les images",
                placeholder="Exemple : ./images",
                value=".",
                interactive=True,
                elem_classes=["narrow-input"]
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
            # 20 lignes d’images + prompts
            images = []
            textboxes = []
            for i in range(MAX_IMAGES):
                with gr.Row():
                    img = gr.Image(label=f"Image {i+1}", show_label=False, height=200)
                    txt = gr.Textbox(label="", lines=4, max_lines=10, show_label=False)
                    images.append(img)
                    textboxes.append(txt)
            # Clic : remplit les 20 images + 20 champs
            load_button.click(
                fn=afficher_images,
                inputs=[folder_input],
                outputs=[status_output] + images + textboxes
            )
    interface.launch(
    allowed_paths=[
        r"F:\Stable Diffusion\TRAIN LoRA 2024\Leah_v6_SDXL_1024 FLUX$\img\40_le@hp0nyv41 woman"
    ]
)

if __name__ == "__main__":
    start_ui()