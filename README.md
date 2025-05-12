# Florence 2 Caption Tool

Génère automatiquement des descriptions détaillées des images via Florence 2. 

> ⚡ Optimisé : GPU CUDA, FP16, SDPA & modèle local (PromptGen v2).  


---

## ✨ Fonctionnalités

| Fonction | Détail |
|----------|--------|
| **Batch** | Traite toutes les images `.png`, `.jpg`, `.jpeg`, `.webp` du dossier `input/`. |
| **Modèle local** | Télécharge **une seule fois** le checkpoint *Florence‑2‑base‑PromptGen‑v2.0* dans `models/FlorencePromptGen/`, puis fonctionne hors‑ligne. |
| **GPU / CPU** | Utilise automatiquement le GPU CUDA (fp16). Bascule en CPU si aucun GPU n’est dispo. |
| **Préfixe personnalisé** | Ajoutez une chaîne (ex. `"Norman, "`) devant chaque caption via `CAPTION_PREFIX`. |
| **Logs propres** | Warnings & logs verbeux (timm, transformers) filtrés ; affichage clair du progrès. |
| **Tolérance aux erreurs** | Ignore les images illisibles sans interrompre le batch, signale les fichiers problématiques. |

---

## 📂 Structure du projet
Effectue un captionning de toutes les images presentes dans **`input/`** et écrit chaque résultat dans **`output/`** sous le même nom + `.txt`.

## Utilisation

Placez vos images dans **`input/`**, puis lancez **`start.bat`**
