# Florence 2 Caption Tool

Génère automatiquement des descriptions détaillées des images via Florence 2. 
Outil conçu pour la creation de dataset d'images pour les entrainements (Stable Diffusion, Flux, HiDream, etc...)

> ⚡ Optimisé : GPU CUDA, FP16, SDPA & modèle local (PromptGen v2).  


## Requirements
❗ Windows seulement pour le moment.

Python 3.10 : https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
Cochez "Add PATH to envirronement" lors de l'installation, puis redemarrez Windows.

Une carte Nvidia (recente) de preference, meme avec peu de Vram.

---

## ✨ Fonctionnalités

| Fonction | Détail |
|----------|--------|
| **Batch** | Traite toutes les images `.png`, `.jpg`, `.jpeg`, `.webp` du dossier `input/`. |
| **Modèle local** | Télécharge **une seule fois** le checkpoint *Florence‑2‑base‑PromptGen‑v2.0* dans `models/FlorencePromptGen/`, puis fonctionne hors‑ligne. |
| **GPU / CPU** | Utilise automatiquement le GPU CUDA (fp16). Bascule en CPU si aucun GPU n’est dispo. |
| **Préfixe personnalisé** | Ajoutez une chaîne (ex. `"Norman, "`) devant chaque caption via `CAPTION_PREFIX`. |
| **Logs propres** | Warnings & logs verbeux (timm, transformers) filtrés ; affichage clair du progrès. |

---

## 📂 Structure du projet
Effectue un captionning de toutes les images presentes dans **`input/`** et écrit chaque résultat dans **`output/`** sous le même nom + `.txt`.

## Utilisation

Placez vos images dans **`input/`**, puis lancez **`start.bat`**


---


## 🙏 Crédits

- [Microsoft / Florence-2](https://huggingface.co/microsoft)
- [MiaoshouAI / Florence‑2 PromptGen v2.0](https://huggingface.co/MiaoshouAI/Florence-2-base-PromptGen-v2.0)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [timm](https://github.com/huggingface/pytorch-image-models)