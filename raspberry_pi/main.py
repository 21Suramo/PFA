# raspberry_pi/main.py

import cv2
import pytesseract
import requests
import time
from datetime import datetime

# 📡 Configuration
API_URL = "http://localhost:5000/data"
CAMERA_INDEX = 0
DELAY_SECONDS = 5

# 📌 Coordonnées des ROIs (à calibrer)
ROI_TEMPERATURE = (100, 50, 300, 120)
ROI_PRESSION = (100, 150, 300, 220)

# 📷 Initialisation de Tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_roi(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, config='--psm 7 -c tessedit_char_whitelist=0123456789.')
    return text.strip()

def send_to_api(temp, press):
    payload = {
        "temperature": temp,
        "pression": press,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.ok:
            print(f"[{datetime.now()}] ✅ Données envoyées : Temp={temp}, Press={press}")
        else:
            print(f"[{datetime.now()}] ❌ API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur réseau : {e}")

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Impossible d'accéder à la webcam.")
        return

    print("📽️ Lecture en cours... Ctrl+C pour arrêter.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Échec de capture.")
                continue

            # Extraction des ROIs
            x1, y1, x2, y2 = ROI_TEMPERATURE
            roi_temp = frame[y1:y2, x1:x2]

            x1, y1, x2, y2 = ROI_PRESSION
            roi_press = frame[y1:y2, x1:x2]

            # OCR
            temp_text = extract_text_from_roi(roi_temp)
            press_text = extract_text_from_roi(roi_press)

            send_to_api(temp_text, press_text)
            time.sleep(DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
