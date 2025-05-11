import torch
import argparse
from transformers import AutoModelForCausalLM, AutoProcessor, set_seed
from PIL import Image
from pathlib import Path
from huggingface_hub import snapshot_download
import warnings
import logging

warnings.filterwarnings("ignore", message="Importing from timm.models.layers is deprecated")
warnings.filterwarnings("ignore", category=FutureWarning, message=r".*Florence2LanguageForConditionalGeneration.*")
warnings.simplefilter("ignore", FutureWarning)
logging.getLogger("transformers").setLevel(logging.ERROR)


# python main_caption.py "F:\ComfyUI_windows_portable\ComfyUI\output\ComfyUI_00903_.png"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE  = torch.float16
LOCAL_DIR = Path("models/FlorencePromptGen")

if not LOCAL_DIR.exists():
    snapshot_download(
        repo_id="MiaoshouAI/Florence-2-base-PromptGen-v2.0",
        local_dir=LOCAL_DIR,
        local_dir_use_symlinks=False    # copie réelle, pas de liens
    )


model_path = LOCAL_DIR
prompts = {"more_detailed_caption": "<MORE_DETAILED_CAPTION>"}

model = AutoModelForCausalLM.from_pretrained(
    LOCAL_DIR,
    trust_remote_code=True,
    torch_dtype=DTYPE,
    attn_implementation="sdpa",
    low_cpu_mem_usage=True
).to(DEVICE)

processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)

@torch.inference_mode()
def caption(path, seed=100):
    set_seed(seed)
    image = Image.open(path).convert("RGB")
    inputs = processor(prompts["more_detailed_caption"], image,
                       return_tensors="pt", do_rescale=False).to(DEVICE, DTYPE)
    ids = model.generate(**inputs, max_new_tokens=1024,
                         num_beams=3, do_sample=True)
    txt = processor.batch_decode(ids, skip_special_tokens=False)[0]
    return txt.replace("<s>", "").replace("</s>", "").strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("img")
    args = parser.parse_args()
    print(caption(args.img))
