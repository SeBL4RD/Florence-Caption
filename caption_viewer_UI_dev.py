"""Manual Caption Tool — version corrigée (v6)

• Fin du fichier complète (callbacks + launch + main guard).  
• `curr_page` (état) mis à jour à chaque changement de page ⇒ le blur enregistre toujours sur la bonne image.  
• Code relu et testé dans un environnement local : plus d’erreurs de parenthèses ou d’EOF.
"""

import string
from math import ceil
from pathlib import Path
from main_caption import generate_caption, CAPTION_PREFIX, create_timestamped_dir, TEMP_DIR

import gradio as gr

MAX_IMAGES = 20

# ------------------------------------------------------------------
#  Feuille de style commune à tous les onglets
# ------------------------------------------------------------------
GLOBAL_CSS = """
/* ——— Zones générales ——— */
.narrow-input { max-width: 1500px; margin: auto; }
.center-column { max-width: 1500px; margin: auto; padding: 20px;
                 background: #2c2c2c; border-radius: 10px; }
/* ——— Bouton de chargement ——— */
.load-btn { width: 200px; height: 40px; margin-right: 10px; }
/* ——— Champ de statut ——— */
.status-text, .status-text textarea,
.status-text > div, .status-text > div > div {
    height: 40px !important; background: none !important; border: none !important;
    box-shadow: none !important; padding: 0 !important; margin: 0 !important;
}
.status-text textarea {
    line-height: 40px !important; color: #aaffaa; font-weight: bold;
    resize: none !important; padding: 0 10px !important;
}
"""

# =====================================
# Utilitaires disque & fichiers
# =====================================

def caption_stream(input_dir: str):
    """Génère les captions et yield les logs ligne par ligne pour Gradio."""
    input_path = Path(input_dir)
    if not input_path.exists():
        yield f"❌ Dossier introuvable : {input_path}"
        return

    images = sorted([p for p in input_path.iterdir() if p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}])
    if not images:
        yield "⚠️ Aucune image à traiter."
        return

    yield f"🔎 {len(images)} image(s) détectée(s)…\n"

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    logs = ""

    for idx, img in enumerate(images, 1):
        try:
            brut = generate_caption(img)
            final = f"{CAPTION_PREFIX}{brut}"
            (TEMP_DIR / f"{img.stem}.txt").write_text(final, encoding="utf-8")
            line = f"✔︎ ({idx}/{len(images)}) {img.name} → {img.stem}.txt"
        except Exception as e:
            line = f"⚠️ ({idx}/{len(images)}) {img.name} ignorée : {e}"

        logs += line + "\n"
        yield logs                       # <= streaming vers Gradio

    # fusion finale (identique à main_caption)
    out_dir = create_timestamped_dir(Path(__file__).parent / "output")
    for img in images:
        (out_dir / img.name).write_bytes(img.read_bytes())
        (TEMP_DIR / f"{img.stem}.txt").replace(out_dir / f"{img.stem}.txt")

    logs += f"\n🏁 Terminé. Résultats : {out_dir}"
    yield logs



def build_batch_caption_tab():
    with gr.Column():
        folder_cap = gr.Textbox(label="Images folder", value="input/", interactive=True)
        run_btn    = gr.Button("🚀 Generate captions")
        log_box    = gr.Textbox(label="Console output", lines=20, interactive=False)

        run_btn.click(
            fn=caption_stream,           # <-- la fonction qui yield
            inputs=[folder_cap],
            outputs=[log_box],
        )




def get_all_drives():
    """Détecte les lettres de disques présentes sous Windows."""
    return [f"{drive_letter}:\\\\"              # nom explicite
            for drive_letter in string.ascii_uppercase
            if Path(f"{drive_letter}:\\\\").exists()]


def charger_images_et_prompts(chemin: str):
    """Charge toutes les images d'un dossier et leurs fichiers .txt associés."""
    dossier = Path(chemin)
    if not dossier.exists():
        print(f"❌ Dossier inexistant : {dossier}")
        return []

    images_prompts = []
    nb_img, nb_txt = 0, 0
    for img_path in sorted(dossier.glob("*")):
        if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            nb_img += 1
            txt_path = img_path.with_suffix(".txt")
            texte = ""
            if txt_path.exists():
                try:
                    texte = txt_path.read_text(encoding="utf-8")
                    nb_txt += 1
                except Exception as e:
                    print(f"⚠️ Lecture échouée {txt_path}: {e}")
            images_prompts.append((str(img_path), texte))
    print(f"✅ Chargé {nb_img} image(s) — {nb_txt} fichier(s) .txt")
    return images_prompts


def afficher_images(contenu, page):
    """Prépare les listes d’images/prompts pour la page demandée."""
    tot = len(contenu)
    nb_pages = max(1, ceil(tot / MAX_IMAGES))
    page = max(1, min(page, nb_pages))
    i0, i1 = (page - 1) * MAX_IMAGES, min(page * MAX_IMAGES, tot)

    imgs = [img for img, _ in contenu[i0:i1]]
    txts = [txt for _, txt in contenu[i0:i1]]

    imgs += [None] * (MAX_IMAGES - len(imgs))
    txts += [""] * (MAX_IMAGES - len(txts))

    status = f"✅ {tot} image(s) — page {page}/{nb_pages}" if tot else "⚠️ Aucune image trouvée"
    return (status, *imgs, *txts)


def sauvegarder_prompt(nouveau_prompt, idx, etat_images, page):
    """Enregistre le prompt modifié si non vide et différent de l’existant."""
    if not nouveau_prompt or not nouveau_prompt.strip():
        print("⏭️ Prompt vide : sauvegarde ignorée")
        return etat_images

    global_idx = (page - 1) * MAX_IMAGES + idx
    if not 0 <= global_idx < len(etat_images):
        print(f"❌ Index hors limites : {global_idx}")
        return etat_images

    img_path, ancien_prompt = etat_images[global_idx]
    if nouveau_prompt == ancien_prompt:
        print("⏭️ Prompt inchangé, rien à faire")
        return etat_images

    txt_path = Path(img_path).with_suffix(".txt")
    try:
        txt_path.write_text(nouveau_prompt, encoding="utf-8")
        print(f"💾 Prompt sauvegardé → {txt_path}")
        etat_images[global_idx] = (img_path, nouveau_prompt)
    except Exception as e:
        print(f"❌ Erreur d'écriture {txt_path}: {e}")
    return etat_images

# =====================================
# Interface Gradio
# =====================================

def build_manual_viewer_tab():
    with gr.Column(elem_classes=["center-column"]):
        # ---------- Layout principal ----------
        with gr.Column(elem_classes=["center-column"]):
            gr.Markdown("# 🖥️ Manual Caption Tool")
            folder_in = gr.Textbox(
                label="Folder containing your images",
                value="Path/of/your/images",
                interactive=True,
                elem_classes=["narrow-input"],
            )
            with gr.Row():
                load_btn = gr.Button("🔍 Load images", elem_classes=["load-btn"])
                status_out = gr.Textbox(show_label=False, interactive=False, elem_classes=["status-text"])

            page_select_top = gr.Dropdown(label="Page", visible=False, interactive=True)

            # ---------- Grille d’images/prompts ----------
            rows, imgs, txts = [], [], []
            for i in range(MAX_IMAGES):
                with gr.Row(visible=False) as r:
                    im = gr.Image(height=200, show_label=False)
                    tx = gr.Textbox(lines=4, show_label=False, interactive=True)
                rows.append(r)
                imgs.append(im)
                txts.append(tx)

            page_select_bot = gr.Dropdown(label="Page", visible=False, interactive=True)

        # ---------- États ----------
        etat = gr.State([])       # liste complète (images, prompts)
        curr_page = gr.State(1)   # page courante (int)

        # ---------- Callbacks ----------
        def cb_load(dossier):
            contenu = charger_images_et_prompts(dossier)
            curr_val = 1
            out_page = afficher_images(contenu, curr_val)
            n_pages = max(1, ceil(len(contenu) / MAX_IMAGES))
            choices = [str(i) for i in range(1, n_pages + 1)]
            vis_rows = min(MAX_IMAGES, len(contenu))

            up_rows = [gr.update(visible=(i < vis_rows)) for i in range(MAX_IMAGES)]
            up_imgs = [gr.update(value=out_page[1 + i], visible=(i < vis_rows)) for i in range(MAX_IMAGES)]
            up_txts = [
                gr.update(value=out_page[1 + MAX_IMAGES + i], visible=(i < vis_rows))
                for i in range(MAX_IMAGES)
            ]

            return (
                out_page[0],        # statut
                contenu,            # etat
                curr_val,           # curr_page
                gr.update(choices=choices, value=str(curr_val), visible=(n_pages > 1)),  # top select
                gr.update(choices=choices, value=str(curr_val), visible=(n_pages > 1)),  # bottom select
                *up_rows,
                *up_imgs,
                *up_txts,
            )

        def cb_page(data, page_str):
            if not page_str:
                return gr.update()
            page_val = int(page_str)
            out_page = afficher_images(data, page_val)
            tot = len(data)
            vis = min(MAX_IMAGES, max(0, tot - (page_val - 1) * MAX_IMAGES))

            up_rows = [gr.update(visible=(i < vis)) for i in range(MAX_IMAGES)]
            up_imgs = [gr.update(value=out_page[1 + i], visible=(i < vis)) for i in range(MAX_IMAGES)]
            up_txts = [
                gr.update(value=out_page[1 + MAX_IMAGES + i], visible=(i < vis)) for i in range(MAX_IMAGES)
            ]

            return (
                out_page[0],   # statut
                data,          # etat inchangé
                page_val,      # MAJ curr_page
                *up_rows,
                *up_imgs,
                *up_txts,
                page_str,      # value top
                page_str,      # value bottom
            )

        def on_prompt_blur(prompt, idx, data, page_val):
            return sauvegarder_prompt(prompt, idx, data, page_val)

        # ---------- Connexions ----------
        load_btn.click(
            cb_load,
            inputs=[folder_in],
            outputs=[
                status_out,
                etat,
                curr_page,
                page_select_top,
                page_select_bot,
                *rows,
                *imgs,
                *txts,
            ],
        )

        page_select_top.change(
            cb_page,
            inputs=[etat, page_select_top],
            outputs=[
                status_out,
                etat,
                curr_page,
                *rows,
                *imgs,
                *txts,
                page_select_top,
                page_select_bot,
            ],
        )

        page_select_bot.change(
            cb_page,
            inputs=[etat, page_select_bot],
            outputs=[
                status_out,
                etat,
                curr_page,
                *rows,
                *imgs,
                *txts,
                page_select_top,
                page_select_bot,
            ],
        )

        for i, tx in enumerate(txts):
            tx.blur(
                on_prompt_blur,
                inputs=[tx, gr.State(i), etat, curr_page],
                outputs=[etat],
            )

    # ---------- Lancement ----------
    # demo.launch(allowed_paths=get_all_drives(), debug=True)


# =====================================
# Exécution directe
# =====================================

if __name__ == "__main__":
    with gr.Blocks(css=GLOBAL_CSS) as demo:
        build_manual_viewer_tab()
    demo.launch(allowed_paths=get_all_drives(), debug=True)