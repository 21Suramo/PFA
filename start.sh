#!/bin/bash

echo "⏳ Démarrage du backend Flask..."
cd backend
source ../venv_backend/bin/activate  # ou adapte selon ton environnement
python app.py &
FLASK_PID=$!

sleep 2

echo "⏳ Démarrage du script de capture OCR..."
cd ../raspberry_pi
source ../venv_raspberry/bin/activate  # adapte selon ton venv
python capture_ocr.py

# Pour arrêter Flask à la fin (si capture_ocr se termine un jour)
kill $FLASK_PID
