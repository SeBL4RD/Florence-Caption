# Florence 2 Caption Tool

Automatically generates detailed image descriptions using Florence 2.  
Ideal for building datasets for model training  
(**Stable Diffusion**, **Flux**, **HiDream**, etc.)

> ⚡ Optimized for GPU (CUDA, FP16, SDPA) and local model execution (PromptGen v2)

---
## Requirements
❗ Windows only for now.

Python 3.10 : https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
Check "Add PATH to envirronement" during installation, then restart Windows.

Preferably a (recent) Nvidia card, even with little Vram.

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Batch processing** | Processes all `.png`, `.jpg`, `.jpeg`, `.webp` images in the `input/` folder. |
| **Local model** | Downloads the *Florence‑2‑base‑PromptGen‑v2.0* checkpoint once into `models/FlorencePromptGen/`, then works fully offline. |
| **GPU / CPU** | Automatically uses CUDA GPU (fp16) if available; falls back to CPU otherwise. |
| **Custom prefix** | Add a prefix (e.g. `"Norman, "`) to each generated caption via the `CAPTION_PREFIX` variable. |
| **Clean logs** | Suppresses verbose logs (timm, transformers); neat console output. |

---

## 📂 Project structure

Performs captioning on all images found in **`input/`**  
and writes results as `.txt` files with matching filenames into **`output/`**.



---

## ▶️ Usage

1. Put your images in the **`input/`** folder  
2. Double-click **`start.bat`**

Text files will appear in **`output/`** with the same name as each image.

---

## 🙏 Credits

- [Microsoft / Florence-2](https://huggingface.co/microsoft)
- [MiaoshouAI / Florence‑2 PromptGen v2.0](https://huggingface.co/MiaoshouAI/Florence-2-base-PromptGen-v2.0)
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [timm](https://github.com/huggingface/pytorch-image-models)