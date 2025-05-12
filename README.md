# Florence 2 Caption Tool

Génère automatiquement des descriptions détaillées (captions) pour toutes les images placées dans le dossier **`input/`** et écrit chaque résultat dans **`output/`** sous le même nom + `.txt`.

> ⚡ Optimisé : GPU CUDA, FP16, SDPA & modèle local (PromptGen v2).  
> 🪶 Léger : aucun poids de modèle n’est versionné dans Git.

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

