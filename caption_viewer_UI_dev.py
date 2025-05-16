import gradio as gr
import os
import string
from math import ceil
from pathlib import Path
import glob

MAX_IMAGES = 20

def get_all_drives():
    drives = []
    for letter in string.ascii_uppercase:
        path = f"{letter}:\\"
        if Path(path).exists():
            drives.append(path)
    return drives

# NOUVEAU : pour pagination
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
    return images_prompts  # On retourne tout !

def afficher_images(contenu, page):
    # contenu : liste [(img, txt), ...]
    total_images = len(contenu)
    nb_pages = ceil(total_images / MAX_IMAGES)
    debut = (page - 1) * MAX_IMAGES
    fin = debut + MAX_IMAGES
    page_contenu = contenu[debut:fin]
    image_values = []
    prompt_values = []
    for img, txt in page_contenu:
        image_values.append(img)
        prompt_values.append(txt)
    # Compléter si moins d’images sur la page
    image_values += [None] * (MAX_IMAGES - len(image_values))
    prompt_values += [""] * (MAX_IMAGES - len(prompt_values))
    status = f"✅ {total_images} image(s) trouvée(s) — page {page}/{nb_pages}" if total_images else "⚠️ Aucun fichier image trouvé"
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
            # --- Ajout : dropdown page (caché si une seule page)
            page_select_top = gr.Dropdown(
                choices=[],
                value=None,
                label="Page",
                visible=False,
                interactive=True,   # <-- C'est ça qui permet de changer la valeur
            )
            

            # 20 lignes d’images + prompts (comme avant)
            rows = []
            images = []
            textboxes = []
            for numero_case in range(MAX_IMAGES):
                with gr.Row(visible=False) as ligne:
                    champ_image = gr.Image(label=f"Image {numero_case+1}", show_label=False, height=200)
                    champ_texte = gr.Textbox(label="", lines=4, max_lines=10, show_label=False)
                    images.append(champ_image)
                    textboxes.append(champ_texte)
                    rows.append(ligne)

            page_select_bottom = gr.Dropdown(
                choices=[],
                value=None,
                label="Page",
                visible=False,
                interactive=True,
            )
            
        # --- VARIABLE D’ÉTAT pour stocker toutes les images chargées
        global_etat_images = gr.State([])
        global_page = gr.State(1)

        # Quand on clique charger
        def bouton_charger(dossier):
            contenu = charger_images_et_prompts(dossier)
            total_images = len(contenu)
            nb_pages = ceil(total_images / MAX_IMAGES) if total_images else 1
            pages_choices = [str(i + 1) for i in range(nb_pages)] if nb_pages > 1 else []
            nombre_lignes_visibles = min(MAX_IMAGES, total_images)
            # --- Updates
            liste_updates_rows = []
            liste_updates_images = []
            liste_updates_textes = []
            outputs = afficher_images(contenu, 1)
            for numero_case in range(MAX_IMAGES):
                visible = True if numero_case < nombre_lignes_visibles else False
                liste_updates_rows.append(gr.update(visible=visible))
                liste_updates_images.append(gr.update(value=outputs[1+numero_case], visible=visible))
                liste_updates_textes.append(gr.update(value=outputs[1+MAX_IMAGES+numero_case], visible=visible))
            return (
                outputs[0],   # status
                contenu,      # state images
                1,            # state page
                gr.update(choices=pages_choices, value="1" if nb_pages > 1 else None, visible=(nb_pages > 1)),  # top
                gr.update(choices=pages_choices, value="1" if nb_pages > 1 else None, visible=(nb_pages > 1)),  # bottom
                *liste_updates_rows,
                *liste_updates_images,
                *liste_updates_textes,
            )

        def on_page_select(etat_images, page_str):
            if page_str is None:
                updates_rows = []
                updates_images = []
                updates_texts = []
                for numero_case in range(MAX_IMAGES):
                    updates_rows.append(gr.update(visible=False))
                    updates_images.append(gr.update(value=None, visible=False))
                    updates_texts.append(gr.update(value="", visible=False))
                return (
                    "",  # le status
                    *updates_rows,
                    *updates_images,
                    *updates_texts,
                    None,  # valeur page_select_top
                    None,  # valeur page_select_bottom
                )
            numero_page = int(page_str)
            tuple_sortie = afficher_images(etat_images, numero_page)
            nombre_total_images = len(etat_images)
            decalage = (numero_page - 1) * MAX_IMAGES
            nombre_champs_visibles = min(MAX_IMAGES, max(0, nombre_total_images - decalage))
            updates_rows = []
            updates_images = []
            updates_texts = []
            for numero_case in range(MAX_IMAGES):
                visible = True if numero_case < nombre_champs_visibles else False
                updates_rows.append(gr.update(visible=visible))
                updates_images.append(gr.update(value=tuple_sortie[1 + numero_case], visible=visible))
                updates_texts.append(gr.update(value=tuple_sortie[1 + MAX_IMAGES + numero_case], visible=visible))
            return (
                tuple_sortie[0],
                *updates_rows,
                *updates_images,
                *updates_texts,
                page_str,   # valeur page_select_top
                page_str,   # valeur page_select_bottom
            )
        
        load_button.click(
            bouton_charger,
            inputs=[folder_input],
            outputs=[status_output, global_etat_images, global_page, page_select_top, page_select_bottom] + rows + images + textboxes
        )
        page_select_top.change(
            on_page_select,
            inputs=[global_etat_images, page_select_top],
            outputs=[status_output] + rows + images + textboxes + [page_select_top, page_select_bottom]
        )
        page_select_bottom.change(
            on_page_select,
            inputs=[global_etat_images, page_select_bottom],
            outputs=[status_output] + rows + images + textboxes + [page_select_top, page_select_bottom]
        )

        # Quand on change de page
        




    interface.launch(allowed_paths=get_all_drives())

if __name__ == "__main__":
    start_ui()