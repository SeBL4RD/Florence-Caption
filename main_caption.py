#!/usr/bin/env python

from pathlib import Path
import warnings
import logging

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor, set_seed
from huggingface_hub import snapshot_download
from PIL import UnidentifiedImageError

# ---------------------------------------------------------------------------
#  Paramètres généraux
# ---------------------------------------------------------------------------
CAPTION_PREFIX = "Norman, "        # laisse chaîne vide "" si tu ne veux rien



# ───────────────────────── 1. Silencer les messages parasites ──────────
warnings.filterwarnings(
    "ignore",
    message="Importing from timm.models.layers is deprecated",
    category=FutureWarning,
)
logging.getLogger("transformers").setLevel(logging.ERROR)

# ───────────────────────── 2. Dossiers et modèles ───────────────────────
ROOT_DIR     = Path(__file__).parent           # dossier du script
INPUT_DIR    = ROOT_DIR / "input"
OUTPUT_DIR   = ROOT_DIR / "output"
MODELS_DIR   = ROOT_DIR / "models" / "FlorencePromptGen"
MODEL_REPO   = "MiaoshouAI/Florence-2-base-PromptGen-v2.0"
PROMPT_TOKEN = "<MORE_DETAILED_CAPTION>"

DEVICE       = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE        = torch.float16 if DEVICE == "cuda" else torch.float32

# ───────────────────────── 3. Téléchargement éventuel du modèle ─────────
if not MODELS_DIR.exists():
    print("Téléchargement du modèle (une seule fois)…")
    snapshot_download(
        repo_id=MODEL_REPO,
        local_dir=MODELS_DIR,
        local_dir_use_symlinks=False,
    )

# ───────────────────────── 4. Chargement du modèle & processor ──────────
print("Chargement du modèle…")
model = (
    AutoModelForCausalLM.from_pretrained(
        MODELS_DIR,
        trust_remote_code=True,
        torch_dtype=DTYPE,
        attn_implementation="sdpa",
        low_cpu_mem_usage=True,
    )
    .to(DEVICE)
    .eval()
)

processor = AutoProcessor.from_pretrained(MODELS_DIR, trust_remote_code=True)

# ───────────────────────── 5. Fonction caption ──────────────────────────
@torch.inference_mode()
def generate_caption(image_path: Path, seed: int = 100) -> str:
    """Retourne le caption Florence‑2 pour une image."""
    set_seed(seed)
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        PROMPT_TOKEN,
        image,
        return_tensors="pt",
        do_rescale=False,
    ).to(DEVICE, DTYPE)

    output_ids = model.generate(
        **inputs,
        max_new_tokens=1024,
        num_beams=3,
        do_sample=True,
    )

    text = processor.batch_decode(output_ids, skip_special_tokens=False)[0]
    return text.replace("<s>", "").replace("</s>", "").strip()

# ───────────────────────── 6. Boucle sur le dossier input/ ──────────────
def main() -> None:
    # Création du dossier output/ s'il n'existe pas
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Extensions d’images acceptées
    extensions = {".png", ".jpg", ".jpeg", ".webp"}

    images = [p for p in INPUT_DIR.iterdir() if p.suffix.lower() in extensions]
    if not images:
        print(f"Aucune image trouvée dans {INPUT_DIR}")
        return

    print(f"{len(images)} image(s) trouvée(s). Génération des captions…\n")

    for image_path in images:
        try:
            brut_caption   = generate_caption(image_path)
        except (UnidentifiedImageError, OSError) as err:
            # ←  message si l’image est illisible
            print(f"⚠️  {image_path.name} ignorée : {err}")
            continue

        final_caption = f"{CAPTION_PREFIX}{brut_caption}"
        (OUTPUT_DIR / f"{image_path.stem}.txt").write_text(final_caption, encoding="utf-8")

        # ←  message pour chaque image traitée avec succès
        print(f"✔︎ {image_path.name} → {image_path.stem}.txt")


    print("\nTerminé !")

# ────────────────────────── 7. Point d’entrée ───────────────────────────
if __name__ == "__main__":
    main()
