#!/bin/bash

# Encodage UTF-8 par défaut
export LANG=en_US.UTF-8

# Nom du dossier de l'environnement virtuel
VENV_DIR="venvflor"

# Vérifie si le venv existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Création de $VENV_DIR..."
    python3 -m venv "$VENV_DIR"

    echo "Installation des packages pour $VENV_DIR..."
    source "$VENV_DIR/bin/activate"

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu126

    echo "Installation terminée pour $VENV_DIR."
    deactivate
else
    echo "L'environnement $VENV_DIR existe déjà."
fi

# Active l'environnement et exécute le script Python
source "$VENV_DIR/bin/activate"
python main_caption.py
