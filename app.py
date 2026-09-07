"""
app.py — Flask bridge between carepass.html (frontend) and the Python backend.

Run with:
    python app.py

Then open in your browser:
    http://127.0.0.1:5000

    

import os
from flask import Flask, jsonify, send_from_directory

from database import init_db
from face_service import scan_face

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "carepass.html")


@app.route("/api/scan", methods=["POST"])
def api_scan():
    result = scan_face()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
"""

import os
import cv2
from flask import Flask, Response, jsonify, send_from_directory

from database import init_db
from face_service import scan_face

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
init_db()


def generate_frames():
    """Generator function to stream webcam frames for the live HTML preview."""
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
    cap.release()


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "carepass.html")


@app.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/api/scan", methods=["POST"])
def api_scan():
    result = scan_face()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    