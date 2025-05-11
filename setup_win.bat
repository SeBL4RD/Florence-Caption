@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion


@REM if not exist "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\model.pth" (
@REM     echo Le modèle XTTSv2 n'existe pas. Téléchargement en cours...
@REM     mkdir "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2" 2>nul
@REM     bitsadmin /transfer XTTSModelDownload /priority HIGH "https://huggingface.co/coqui/XTTS-v2/resolve/main/model.pth?download=true" "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\model.pth"
@REM     bitsadmin /transfer XTTSHashDownload /priority HIGH "https://huggingface.co/coqui/XTTS-v2/resolve/main/hash.md5?download=true" "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\hash.md5"
@REM     bitsadmin /transfer XTTSConfigDownload /priority HIGH "https://huggingface.co/coqui/XTTS-v2/resolve/main/config.json?download=true" "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\config.json"
@REM     bitsadmin /transfer XTTSVocabDownload /priority HIGH "https://huggingface.co/coqui/XTTS-v2/resolve/main/vocab.json?download=true" "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\vocab.json"
@REM     bitsadmin /transfer XTTSSpeakerDownload /priority HIGH "https://huggingface.co/coqui/XTTS-v2/resolve/main/speakers_xtts.pth?download=true" "%USERPROFILE%\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2\speakers_xtts.pth"
@REM     echo Téléchargement terminé.
@REM ) else (
@REM     echo Le modèle XTTSv2 existe déjà.
@REM )

MiaoshouAI/Florence‑2‑base‑PromptGen‑v2.0

REM Venv
if not exist "venvflor" (
    echo Création de venvflor...
    python -m venv venvflor
    echo Installation des packages pour venvflor...
    venvflor\Scripts\python.exe -m pip install --upgrade pip
    
    venvflor\Scripts\python.exe -m pip install -r requirements.txt
    venvflor\Scripts\python.exe -m pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu126
    
    echo Installation terminée pour venvflor.
) else (
    echo L'environnement venvflor existe déjà.
)



cmd /k