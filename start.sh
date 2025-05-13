#!/bin/bash

echo "🚀 Lancement dans 3 terminaux séparés..."

# Terminal 1 : BACKEND FLASK
lxterminal --title="Backend Flask" --working-directory=~/PFA/backend \
  --command="bash -c 'source ./venv/bin/activate && python app.py; exec bash'" &

# Terminal 2 : FRONTEND STATIC SERVER
lxterminal --title="Frontend" --working-directory=~/PFA/frontend \
  --command="bash -c 'python3 -m http.server 8001; exec bash'" &

# Terminal 3 : RASPBERRY OCR
lxterminal --title="OCR Capture" --working-directory=~/PFA/raspberry_pi \
  --command="bash -c 'source ./venv/bin/activate && python capture_ocr.py; exec bash'" &

echo "✅ Lancement terminé. Les fenêtres vont s’ouvrir."

