#!/usr/bin/env python
"""Interface unifiée : onglet Viewer + onglet Batch Caption."""

import gradio as gr
from pathlib import Path
import shutil
import traceback

# ---------- 1.  On ré-utilise le viewer ----------
from caption_viewer_UI_dev import (
    build_manual_viewer_tab,      # ta fonction renommée
    get_all_drives,               # déjà prêt
)

# ---------- 2.  On va ré-utiliser la génération de main_caption ----------
from main_caption import (
    generate_caption,
    CAPTION_PREFIX,
    TEMP_DIR,
    create_timestamped_dir,
)

# ---------- 3.  Petit utilitaire pour le flux de logs ----------
def caption_stream(input_dir: str, user_prefix: str = ""):
    """Parcourt le dossier et yield les logs pour affichage temps réel."""
    try:
        folder = Path(input_dir)
        if not folder.exists():
            yield f"❌ Dossier introuvable : {folder}"
            return

        images = sorted([p for p in folder.iterdir() if p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}])
        if not images:
            yield "⚠️ Aucune image trouvée."
            return

        TEMP_DIR.mkdir(parents=True, exist_ok=True)

        logs = f"🔎 {len(images)} image(s) détectée(s)…\n\n"
        yield logs                       # 1ᵉʳ affichage

        # préfixe : si l'utilisateur en a fourni un, on l'utilise ; sinon on
        # reprend la constante CAPTION_PREFIX définie dans main_caption.py
        prefix = user_prefix if user_prefix.strip() else CAPTION_PREFIX
        for idx, img in enumerate(images, 1):

            try:
                brut = generate_caption(img)
                caption = f"{CAPTION_PREFIX}{brut}"
                caption = f"{prefix}{brut}"
                (TEMP_DIR / f"{img.stem}.txt").write_text(caption, encoding="utf-8")
                line = f"✔︎ ({idx}/{len(images)}) {img.name}"
            except Exception as e:
                line = f"⚠️ ({idx}/{len(images)}) {img.name} ignorée : {e}"

            logs += line + "\n"
            yield logs                   # rafraîchit la textbox

        # ---- fusion finale dans un dossier horodaté ----
        out_dir = create_timestamped_dir(Path(__file__).parent / "output")
        for img in images:
            shutil.move(str(img), out_dir / img.name)
            shutil.move(str(TEMP_DIR / f"{img.stem}.txt"), out_dir / f"{img.stem}.txt")

        logs += f"\n🏁 Terminé → {out_dir}"
        yield logs
    except Exception:
        yield "❌ ERREUR :\n" + traceback.format_exc()

# ---------- 4.  Construction du 2ᵉ onglet ----------
def build_batch_caption_tab():
    with gr.Column(elem_classes=["center-column"]):
        gr.Markdown("# ⚙️ Batch caption (Florence-2)")
        folder_in = gr.Textbox(
            label="Folder with images",
            value="input/",
            interactive=True,
        )
        prefix_in = gr.Textbox(
            label='Prefix to prepend to every caption (optional)',
            placeholder='e.g. "JosianneLoRAv2, "',
            value="",                    # si vide → on garde le CAPTION_PREFIX par défaut
            interactive=True,
        )
        run_btn = gr.Button("🚀 Generate captions")
        log_box = gr.Textbox(
            label="Console output",
            lines=20,
            interactive=False,
        )

        run_btn.click(
            caption_stream,          # ← appelle la fonction ci-dessus
            inputs=[folder_in, prefix_in],
            outputs=[log_box],
        )

# ---------- 5.  CSS commun (on reprend celui du viewer) ----------
GLOBAL_CSS = """
/* remis en format colonne lisible */
.narrow-input { max-width: 1500px; margin: auto; }
.center-column { max-width: 1500px; margin: auto; padding: 20px; background: #2c2c2c; border-radius: 10px; }
.load-btn { width: 200px; height: 40px; margin-right: 10px; }
/* champ statut + bouton parfaitement alignés (40 px) */
.status-text, .status-text textarea,
.status-text > div, .status-text > div > div {
    height: 40px !important;
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
.status-text textarea {
    line-height: 40px !important;
    color: #aaffaa;
    font-weight: bold;
    resize: none !important;
    padding: 0 10px !important;
}
"""

# ---------- 6.  Assemblage final ----------
with gr.Blocks(css=GLOBAL_CSS) as demo:
    with gr.Tabs():
        with gr.TabItem("⚙️ Batch caption"):
            build_batch_caption_tab()     # ← nouveau
        with gr.TabItem("🖼️ Manual viewer"):
            build_manual_viewer_tab()     # ← ton premier onglet

# ---------- 7.  Lancement ----------
if __name__ == "__main__":
    demo.launch(allowed_paths=get_all_drives(), debug=True)
