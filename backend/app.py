from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, insert_reading, get_all_readings, get_latest_reading
import cv2
from flask import Response, stream_with_context

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['POST'])
def add_reading():
    data = request.get_json()
    try:
        temperature = float(data.get('temperature'))
        pression = float(data.get('pression'))
        timestamp = data.get('timestamp')
        insert_reading(timestamp, temperature, pression)
        return jsonify({"message": "✅ Données enregistrées"}), 200
    except Exception as e:
        return jsonify({"error": f"❌ Données invalides: {e}"}), 400

@app.route('/data', methods=['GET'])
def get_all():
    readings = get_all_readings()
    return jsonify(readings)

@app.route('/data/latest', methods=['GET'])
def get_latest():
    latest = get_latest_reading()
    return jsonify(latest if latest else {})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
# Initialiser la caméra
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(gen_frames()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')