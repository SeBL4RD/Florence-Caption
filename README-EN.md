# Florence 2 Caption Tool

Automatically generates detailed image descriptions using Florence 2.  
Ideal for building datasets for model training  
(**Stable Diffusion**, **Flux**, **HiDream**, etc.)

> ⚡ Optimized for GPU (CUDA, FP16, SDPA) and local model execution (PromptGen v2)

---

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