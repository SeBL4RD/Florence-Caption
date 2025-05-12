@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion


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



venvflor\Scripts\python main_caption.py
cmd /k