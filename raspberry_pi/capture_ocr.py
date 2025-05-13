from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import pytesseract
import threading
import time
import requests
from datetime import datetime

# Configuration Flask
app = Flask(__name__)
CORS(app)

# Configuration caméra et OCR
CAMERA_INDEX = 0
API_URL = "http://localhost:5000/data"
DELAY_SECONDS = 1

ROI_TEMPERATURE = (100, 50, 300, 120)  # (x1, y1, x2, y2)
ROI_PRESSION = (100, 150, 300, 220)

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Caméra partagée entre OCR et stream
cap = cv2.VideoCapture(CAMERA_INDEX)
lock = threading.Lock()

# --- OCR FUNCTIONS ---

def extract_text(roi):
    if roi is None or roi.size == 0:
        return ""  # On retourne rien si l'image est vide
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return pytesseract.image_to_string(
        thresh, config='--psm 7 -c tessedit_char_whitelist=0123456789.'
    ).strip()

def send_to_api(temp, press):
    payload = {
        "temperature": temp,
        "pression": press,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        res = requests.post(API_URL, json=payload, timeout=5)
        if res.ok:
            print(f"[{datetime.now()}] ✅ Envoyé : {payload}")
        else:
            print(f"❌ API error: {res.status_code}")
    except Exception as e:
        print(f"❌ Exception réseau : {e}")

def ocr_loop():
    while True:
        with lock:
            ret, frame = cap.read()
        if not ret:
            continue

        x1, y1, x2, y2 = ROI_TEMPERATURE
        roi_temp = frame[y1:y2, x1:x2]

        x1, y1, x2, y2 = ROI_PRESSION
        roi_press = frame[y1:y2, x1:x2]

        temp = extract_text(roi_temp)
        press = extract_text(roi_press)

        print(f"[{datetime.now()}] OCR : Temp = '{temp}' | Press = '{press}'")

        if temp and press:
            send_to_api(temp, press)

        time.sleep(DELAY_SECONDS)

# --- FLASK ROUTES ---

@app.route('/')
def status():
    return jsonify({"status": "capture_ocr en cours"})

@app.route('/set_rois', methods=['POST'])
def set_rois():
    data = request.get_json()
    try:
        global ROI_TEMPERATURE, ROI_PRESSION

        temp = list(map(int, data.get("temp", ROI_TEMPERATURE)))
        press = list(map(int, data.get("press", ROI_PRESSION)))

        # Vérification de format correct
        if len(temp) != 4 or len(press) != 4:
            return jsonify({"error": "Format incorrect pour les ROIs"}), 400

        # Vérification d’ordre logique : x1 < x2 et y1 < y2
        for label, roi in [("température", temp), ("pression", press)]:
            x1, y1, x2, y2 = roi
            if x2 <= x1 or y2 <= y1:
                return jsonify({"error": f"Coordonnées invalides pour la ROI {label} (x2<=x1 ou y2<=y1)"}), 400

        # Vérification par rapport à la taille de l’image
        with lock:
            ret, frame = cap.read()
        if not ret:
            return jsonify({"error": "Impossible de lire la caméra pour vérifier les ROIs"}), 500

        height, width, _ = frame.shape
        for label, roi in [("température", temp), ("pression", press)]:
            x1, y1, x2, y2 = roi
            if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
                return jsonify({"error": f"ROI {label} dépasse les dimensions de la caméra ({width}x{height})"}), 400

        # Si tout est bon, on enregistre
        ROI_TEMPERATURE = temp
        ROI_PRESSION = press
        print(f"🔁 Zones mises à jour : temp={ROI_TEMPERATURE}, press={ROI_PRESSION}")
        return jsonify({"message": "✅ Zones mises à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/video_feed')
def video_feed():
    def gen_frames():
        while True:
            with lock:
                success, frame = cap.read()
            if not success:
                continue
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- LANCEMENT ---

if __name__ == "__main__":
    try:
        threading.Thread(target=ocr_loop, daemon=True).start()
        app.run(host="0.0.0.0", port=5050)
    finally:
        cap.release()
