import cv2
import pytesseract
import requests
import time

# Configuration des zones ROI
TEMP_ROI = (100, 100, 200, 50)    # (x, y, w, h) à adapter selon ton écran
PRESS_ROI = (100, 200, 200, 50)

API_URL = "http://localhost:8000/add_reading"  # Adapter si l’API est sur un autre host

def extract_text_from_roi(frame, roi):
    x, y, w, h = roi
    roi_img = frame[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray, config='--psm 7').strip()

def main():
    cap = cv2.VideoCapture(0)  # 0 = première webcam USB
    if not cap.isOpened():
        print("Erreur: webcam introuvable.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        temperature = extract_text_from_roi(frame, TEMP_ROI)
        pressure = extract_text_from_roi(frame, PRESS_ROI)

        print(f"Temp: {temperature} | Press: {pressure}")

        try:
            requests.post(API_URL, json={
                "temperature": temperature,
                "pressure": pressure
            })
            print("✅ Données envoyées à l'API")
        except Exception as e:
            print(f"Erreur d’envoi : {e}")

        time.sleep(5)  # pause de 5 secondes entre les captures

if __name__ == "__main__":
    main()
